"""
neurociencia_edu.stats.mediation
Análise de mediação (Baron & Kenny + bootstrap).
"""

from __future__ import annotations

import logging
from typing import NamedTuple

import numpy as np
from sklearn.linear_model import LinearRegression

logger = logging.getLogger(__name__)


class MediationResult(NamedTuple):
    """Resultado da análise de mediação."""
    a: float  # X → M
    b: float  # M → Y (controlando X)
    c: float  # X → Y (efeito total)
    c_prime: float  # X → Y (efeito direto, controlando M)
    indirect: float  # a * b
    total: float  # c
    proportion_mediated: float  # indirect / c
    ci_lower: float  # IC 95% inferior do efeito indireto
    ci_upper: float  # IC 95% superior
    p_indirect: float


def mediation_analysis(
    X: np.ndarray,
    M: np.ndarray,
    Y: np.ndarray,
    n_bootstrap: int = 5000,
    ci_level: float = 0.95,
    seed: int = 42,
) -> MediationResult:
    """Análise de mediação com bootstrap.

    Args:
        X: Variável independente (n,).
        M: Mediador (n,).
        Y: Variável dependente (n,).
        n_bootstrap: Número de amostras bootstrap.
        ci_level: Nível do IC (default 0.95).
        seed: Seed para reprodutibilidade.

    Returns:
        MediationResult com todos os coeficientes.
    """
    X = np.asarray(X).flatten()
    M = np.asarray(M).flatten()
    Y = np.asarray(Y).flatten()
    n = len(X)

    # Efeito total (c)
    c = LinearRegression().fit(X.reshape(-1, 1), Y).coef_[0]

    # Caminho a (X → M)
    a = LinearRegression().fit(X.reshape(-1, 1), M).coef_[0]

    # Caminhos b e c' (X, M → Y)
    XM = np.column_stack([X, M])
    coef_b = LinearRegression().fit(XM, Y).coef_
    c_prime, b = coef_b[0], coef_b[1]

    # Efeito indireto
    indirect = a * b
    proportion_mediated = (indirect / c * 100) if c != 0 else 0.0

    # Bootstrap
    rng = np.random.default_rng(seed)
    indirect_boot = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.choice(n, n, replace=True)
        X_b, M_b, Y_b = X[idx], M[idx], Y[idx]
        try:
            a_b = LinearRegression().fit(X_b.reshape(-1, 1), M_b).coef_[0]
            b_b = LinearRegression().fit(np.column_stack([X_b, M_b]), Y_b).coef_[1]
            indirect_boot[i] = a_b * b_b
        except Exception:
            indirect_boot[i] = np.nan

    indirect_boot = indirect_boot[~np.isnan(indirect_boot)]
    alpha = 1 - ci_level
    ci_lower = np.percentile(indirect_boot, 100 * alpha / 2)
    ci_upper = np.percentile(indirect_boot, 100 * (1 - alpha / 2))

    # p-valor (proporção de b amostras com sinal oposto)
    if indirect >= 0:
        p_indirect = 2 * np.mean(indirect_boot <= 0)
    else:
        p_indirect = 2 * np.mean(indirect_boot >= 0)
    p_indirect = min(p_indirect, 1.0)

    return MediationResult(
        a=a, b=b, c=c, c_prime=c_prime,
        indirect=indirect, total=c,
        proportion_mediated=proportion_mediated,
        ci_lower=ci_lower, ci_upper=ci_upper,
        p_indirect=p_indirect,
    )


def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    """Calcula Cohen's d para两组独立.

    Args:
        x: Amostra 1.
        y: Amostra 2.

    Returns:
        Cohen's d.
    """
    nx, ny = len(x), len(y)
    pooled_sd = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2))
    if pooled_sd == 0:
        return 0.0
    return (np.mean(x) - np.mean(y)) / pooled_sd


def bootstrap_mediation(
    X: np.ndarray,
    M: np.ndarray,
    Y: np.ndarray,
    n_bootstrap: int = 5000,
    seed: int = 42,
) -> np.ndarray:
    """Distribuição bootstrap do efeito indireto.

    Args:
        X, M, Y: Variáveis.
        n_bootstrap: Número de amostras.
        seed: Seed.

    Returns:
        Array com efeito indireto em cada amostra bootstrap.
    """
    n = len(X)
    rng = np.random.default_rng(seed)
    indirects = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.choice(n, n, replace=True)
        result = mediation_analysis(X[idx], M[idx], Y[idx], n_bootstrap=10, seed=seed + i)
        indirects[i] = result.indirect
    return indirects
