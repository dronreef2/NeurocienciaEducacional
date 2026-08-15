"""Drift detection entre versões de datasets.

Calcula PSI (Population Stability Index) e KS test para detectar
mudanças significativas em distribuições entre duas versões.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def psi(
    baseline: np.ndarray,
    current: np.ndarray,
    bins: int = 10,
) -> float:
    """Calcula o Population Stability Index (PSI).

    Args:
        baseline: Array 1D com valores de referência.
        current: Array 1D com valores atuais.
        bins: Número de bins para discretização.

    Returns:
        PSI value. Interpretação:
            - < 0.1: sem mudança significativa
            - 0.1-0.2: mudança moderada
            - > 0.2: mudança significativa

    Examples:
        >>> import numpy as np
        >>> baseline = np.random.randn(1000)
        >>> current = np.random.randn(1000) + 0.5  # shifted
        >>> psi(baseline, current) > 0.1
        True
    """
    baseline = np.asarray(baseline)
    current = np.asarray(current)

    if len(baseline) < bins or len(current) < bins:
        raise ValueError(f"Amostras muito pequenas (precisa >= {bins} pontos)")

    # Definir bins baseado no baseline
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.unique(np.quantile(baseline, quantiles))
    if len(edges) < 3:
        logger.warning("Poucos bins únicos, retornando PSI=0")
        return 0.0

    # Calcular proporções por bin
    baseline_counts, _ = np.histogram(baseline, bins=edges)
    current_counts, _ = np.histogram(current, bins=edges)

    # Adicionar epsilon para evitar divisão por zero
    baseline_pct = (baseline_counts + 1e-6) / (len(baseline) + 1e-6 * bins)
    current_pct = (current_counts + 1e-6) / (len(current) + 1e-6 * bins)

    # PSI = sum((current - baseline) * ln(current / baseline))
    psi_value = float(np.sum((current_pct - baseline_pct) * np.log(current_pct / baseline_pct)))

    logger.info(f"PSI = {psi_value:.4f} ({'significativo' if psi_value > 0.2 else 'moderado' if psi_value > 0.1 else 'estável'})")
    return psi_value


def ks_test(
    baseline: np.ndarray,
    current: np.ndarray,
) -> dict:
    """Executa Kolmogorov-Smirnov test entre duas distribuições.

    Args:
        baseline: Array 1D com valores de referência.
        current: Array 1D com valores atuais.

    Returns:
        Dict com statistic e p_value.

    Examples:
        >>> import numpy as np
        >>> baseline = np.random.randn(100)
        >>> current = np.random.randn(100) + 1.0
        >>> result = ks_test(baseline, current)
        >>> result['p_value'] < 0.05
        True
    """
    baseline = np.asarray(baseline)
    current = np.asarray(current)

    result = scipy_stats.ks_2samp(baseline, current)
    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "significant": result.pvalue < 0.05,
    }


def drift_report(
    baseline_df: pd.DataFrame,
    current_df: pd.DataFrame,
    columns: Optional[list[str]] = None,
    bins: int = 10,
) -> dict:
    """Gera relatório de drift entre dois datasets.

    Args:
        baseline_df: DataFrame de referência.
        current_df: DataFrame atual.
        columns: Colunas para analisar (None = todas numéricas).
        bins: Número de bins para PSI.

    Returns:
        Dict com PSI, KS test, e status para cada coluna.
    """
    if columns is None:
        columns = baseline_df.select_dtypes(include=[np.number]).columns.tolist()

    report = {
        "n_baseline": len(baseline_df),
        "n_current": len(current_df),
        "columns_analyzed": [],
        "drift_detected": False,
    }

    for col in columns:
        if col not in baseline_df.columns or col not in current_df.columns:
            logger.warning(f"Coluna '{col}' não existe em ambos os DataFrames")
            continue

        baseline_col = baseline_df[col].dropna().values
        current_col = current_df[col].dropna().values

        if len(baseline_col) == 0 or len(current_col) == 0:
            continue

        try:
            psi_value = psi(baseline_col, current_col, bins=bins)
            ks = ks_test(baseline_col, current_col)

            col_report = {
                "psi": psi_value,
                "ks_statistic": ks["statistic"],
                "ks_p_value": ks["p_value"],
                "psi_status": "significativo" if psi_value > 0.2 else "moderado" if psi_value > 0.1 else "estável",
                "ks_significant": ks["significant"],
            }
            report[col] = col_report
            report["columns_analyzed"].append(col)

            if psi_value > 0.2 or ks["significant"]:
                report["drift_detected"] = True
        except Exception as e:
            logger.warning(f"Erro ao analisar coluna '{col}': {e}")

    return report
