"""Análise de sobrevivência — Kaplan-Meier."""
from __future__ import annotations

import numpy as np
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def kaplan_meier(
    times: np.ndarray,
    events: np.ndarray,
) -> dict:
    """Calcula o estimador de Kaplan-Meier.

    Args:
        times: Array 1D com tempos observados.
        events: Array 1D binário (1=evento, 0=censurado).

    Returns:
        Dict com times, survival_function, median, n_at_risk.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)

    if len(times) != len(events):
        raise ValueError(f"times and events must have same length, got {len(times)} vs {len(events)}")
    if np.any(times < 0):
        raise ValueError("times must be non-negative")
    if not np.all(np.isin(events, [0, 1])):
        raise ValueError("events must be binary (0 or 1)")

    n = len(times)
    unique_times = np.sort(np.unique(times[events == 1]))

    survival = []
    n_at_risk = []
    s_t = 1.0

    for t in unique_times:
        n_risk = np.sum(times >= t)
        d_t = np.sum((times == t) & (events == 1))
        s_t = s_t * (1 - d_t / n_risk) if n_risk > 0 else s_t
        survival.append(s_t)
        n_at_risk.append(n_risk)

    survival = np.array(survival)
    n_at_risk = np.array(n_at_risk)

    median_idx = np.where(survival <= 0.5)[0]
    median = float(unique_times[median_idx[0]]) if len(median_idx) > 0 else None

    logger.info(f"Kaplan-Meier: n={n}, events={events.sum()}, median={median}")

    return {
        "times": unique_times,
        "survival_function": survival,
        "median": median,
        "n_at_risk": n_at_risk,
    }
