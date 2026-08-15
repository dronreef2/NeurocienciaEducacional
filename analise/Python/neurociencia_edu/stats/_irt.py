"""Item Response Theory — Modelo de Rasch (1PL).

Implementação do modelo logístico de 1 parâmetro para ajuste
de dados binários (acerto/erro) em testes educacionais.
"""
from __future__ import annotations

import numpy as np
from neurociencia_edu.exceptions import FitError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def fit_rasch(
    responses: np.ndarray,
    max_iter: int = 200,
    tol: float = 1e-3,
) -> dict:
    """Ajusta o modelo de Rasch 1PL via JMLE.

    Args:
        responses: Matriz (n_subjects, n_items) binária.
        max_iter: Máximo de iterações.
        tol: Tolerância para convergência.

    Returns:
        Dict com theta, b, se_theta, se_b.
    """
    responses = np.asarray(responses)

    if responses.ndim != 2:
        raise ValueError(f"responses must be 2D, got {responses.ndim}D")

    if not np.all(np.isin(responses, [0, 1])):
        raise ValueError("responses must be binary (0 or 1)")

    n_subjects, n_items = responses.shape
    logger.info(f"Fitting Rasch model: n_subjects={n_subjects}, n_items={n_items}")

    # Se todos os sujeitos acertam todos os itens, retornar valores sentinela
    if np.all(responses == 1):
        theta = np.zeros(n_subjects)
        b = np.full(n_items, -10.0)
    elif np.all(responses == 0):
        theta = np.zeros(n_subjects)
        b = np.full(n_items, 10.0)
    else:
        # Inicialização melhorada: logit da proporção de acerto
        p_obs = responses.mean(axis=0)
        p_obs = np.clip(p_obs, 0.01, 0.99)
        b = -np.log(p_obs / (1 - p_obs))

        p_subj = responses.mean(axis=1)
        p_subj = np.clip(p_subj, 0.01, 0.99)
        theta = np.log(p_subj / (1 - p_subj))
        theta -= theta.mean()

        converged = False
        for iteration in range(max_iter):
            theta_old = theta.copy()
            b_old = b.copy()

            # M-step: theta
            for i in range(n_subjects):
                grad = 0.0
                hess = 0.0
                for j in range(n_items):
                    p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
                    p = np.clip(p, 1e-10, 1 - 1e-10)
                    grad += responses[i, j] - p
                    hess += -p * (1 - p)
                if hess < -1e-10:
                    theta[i] = theta[i] - grad / hess
            theta -= theta.mean()

            # M-step: b
            for j in range(n_items):
                grad = 0.0
                hess = 0.0
                for i in range(n_subjects):
                    p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
                    p = np.clip(p, 1e-10, 1 - 1e-10)
                    grad += -(responses[i, j] - p)
                    hess += -p * (1 - p)
                if hess < -1e-10:
                    b[j] = b[j] - grad / hess

            delta = max(np.max(np.abs(theta - theta_old)), np.max(np.abs(b - b_old)))
            if delta < tol:
                logger.info(f"Converged at iteration {iteration + 1} (delta={delta:.6f})")
                converged = True
                break

        if not converged:
            logger.warning(f"Rasch did not converge after {max_iter} iters (delta={delta:.6f})")

    # Erros padrão
    se_theta = np.zeros(n_subjects)
    for i in range(n_subjects):
        info = 0.0
        for j in range(n_items):
            p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
            info += p * (1 - p)
        se_theta[i] = 1.0 / np.sqrt(info) if info > 0 else np.nan

    se_b = np.zeros(n_items)
    for j in range(n_items):
        info = 0.0
        for i in range(n_subjects):
            p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
            info += p * (1 - p)
        se_b[j] = 1.0 / np.sqrt(info) if info > 0 else np.nan

    return {
        "theta": theta,
        "b": b,
        "se_theta": se_theta,
        "se_b": se_b,
    }
