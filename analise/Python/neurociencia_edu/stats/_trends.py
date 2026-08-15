"""Testes estatísticos de tendência.

Fornece implementações de testes não-paramétricos para detectar
tendências monotônicas em séries temporais.
"""
from __future__ import annotations

import numpy as np
from scipy import stats as scipy_stats


def mann_kendall(x: np.ndarray) -> tuple[float, float]:
    """Executa o teste de Mann-Kendall para tendência monotônica.

    O teste de Mann-Kendall é um teste não-paramétrico usado para
    detectar tendências em séries temporais. É robusto a outliers e
    não assume normalidade dos dados.

    Args:
        x: Array 1D com a série temporal a ser testada.

    Returns:
        Tupla (z, p_value) onde:
            - z: estatística Z do teste (positiva = tendência crescente,
              negativa = decrescente).
            - p_value: probabilidade de observar a tendência sob H0
              (ausência de tendência).

    Examples:
        >>> import numpy as np
        >>> x = np.array([1, 2, 3, 4, 5])
        >>> z, p = mann_kendall(x)
        >>> z > 0
        True
        >>> p < 0.05
        True
    """
    x = np.asarray(x, dtype=float)
    n = len(x)

    if n < 2:
        return 0.0, 1.0

    # Calcular S (soma dos sinais)
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += int(np.sign(x[j] - x[i]))

    # Variância de S sob H0
    var_s = n * (n - 1) * (2 * n + 5) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0.0

    p_value = 2.0 * (1.0 - scipy_stats.norm.cdf(abs(z)))
    return float(z), float(p_value)
