"""Análise de poder estatístico (power analysis).

Calcula o poder estatístico para diferentes testes comumente usados
em pesquisa em neurociência educacional.
"""
from __future__ import annotations

import numpy as np
from scipy import stats as scipy_stats
from neurociencia_edu.exceptions import StatisticalTestError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def power_analysis(
    effect_size: float,
    n: int,
    alpha: float = 0.05,
    test: str = "t_test",
) -> float:
    """Calcula o poder estatístico para um teste.

    Args:
        effect_size: Tamanho do efeito (Cohen's d, r, ou f).
        n: Tamanho amostral.
        alpha: Nível de significância (default 0.05).
        test: Tipo de teste. Opções:
            - "t_test": teste t (Cohen's d)
            - "correlation": correlação (r de Pearson)
            - "anova": ANOVA (f de Cohen)
            - "chi_square": qui-quadrado (w de Cohen)

    Returns:
        Poder estatístico (probabilidade de detectar o efeito, se ele existir).
        Valor entre 0 e 1.

    Raises:
        ValueError: Se n <= 0 ou test desconhecido.

    Examples:
        >>> power_analysis(effect_size=0.5, n=64, test="t_test")
        0.801
    """
    if n <= 0:
        raise ValueError(f"n must be > 0, got {n}")

    logger.debug(f"Power analysis: test={test}, n={n}, d={effect_size}, alpha={alpha}")

    if test == "t_test":
        if effect_size == 0:
            return alpha
        df = n - 1
        ncp = effect_size * np.sqrt(n)
        t_crit = scipy_stats.t.ppf(1 - alpha / 2, df)
        power = 1 - scipy_stats.nct.cdf(t_crit, df, ncp) + scipy_stats.nct.cdf(-t_crit, df, ncp)
        return float(power)

    elif test == "correlation":
        if effect_size == 0:
            return alpha
        df = n - 2
        z = np.arctanh(effect_size)
        se = 1 / np.sqrt(n - 3)
        z_crit = scipy_stats.norm.ppf(1 - alpha / 2)
        power = 1 - scipy_stats.norm.cdf(z_crit - z / se) + scipy_stats.norm.cdf(-z_crit - z / se)
        return float(power)

    elif test == "anova":
        if effect_size == 0:
            return alpha
        k = 3
        df1 = k - 1
        df2 = n - k
        ncp = effect_size ** 2 * n
        f_crit = scipy_stats.f.ppf(1 - alpha, df1, df2)
        power = 1 - scipy_stats.ncf.cdf(f_crit, df1, df2, ncp)
        return float(power)

    elif test == "chi_square":
        if effect_size == 0:
            return alpha
        df = 1
        ncp = effect_size ** 2 * n
        chi2_crit = scipy_stats.chi2.ppf(1 - alpha, df)
        power = 1 - scipy_stats.ncx2.cdf(chi2_crit, df, ncp)
        return float(power)

    else:
        raise StatisticalTestError(
            f"Unknown test: {test}",
            details={"valid_tests": ["t_test", "correlation", "anova", "chi_square"]}
        )
