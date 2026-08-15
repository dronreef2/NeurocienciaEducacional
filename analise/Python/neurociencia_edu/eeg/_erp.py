"""Cálculo de Event-Related Potentials (ERP)."""
from __future__ import annotations

import numpy as np
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def compute_erp(
    trials: np.ndarray,
    times: np.ndarray,
    baseline: tuple[float, float] | None = (-0.2, 0.0),
) -> np.ndarray:
    """Calcula o ERP médio (grand average) com correção de baseline.

    Args:
        trials: Array (n_trials, n_channels, n_times).
        times: Array (n_times,) com vetor de tempos em segundos.
        baseline: Tupla (início, fim) em segundos. None = sem correção.

    Returns:
        Array (n_channels, n_times) com ERP médio.
    """
    if trials.ndim != 3:
        raise ValueError(f"trials must be 3D (n_trials, n_channels, n_times), got {trials.ndim}D")
    if trials.shape[2] != len(times):
        raise ValueError(
            f"times length ({len(times)}) must match trials.shape[2] ({trials.shape[2]})"
        )

    logger.debug(f"Computing ERP: shape={trials.shape}, baseline={baseline}")

    erp = trials.mean(axis=0)

    if baseline is not None:
        b_start, b_end = baseline
        mask = (times >= b_start) & (times <= b_end)
        if not np.any(mask):
            logger.warning(f"No samples in baseline window {baseline}")
            return erp
        baseline_mean = erp[:, mask].mean(axis=1, keepdims=True)
        erp = erp - baseline_mean

    return erp
