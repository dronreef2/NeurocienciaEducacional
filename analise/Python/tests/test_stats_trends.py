"""Testes para neurociencia_edu.stats._trends.mann_kendall."""
import numpy as np
import pytest

from neurociencia_edu.stats._trends import mann_kendall


class TestMannKendall:
    """Testes do teste de Mann-Kendall para tendência."""

    def test_increasing_trend_is_significant(self) -> None:
        """Série crescente deve ter p-value baixo."""
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        z, p = mann_kendall(x)
        assert z > 0, f"Esperado z > 0 para tendência crescente, obtido {z}"
        assert p < 0.05, f"Esperado p < 0.05, obtido {p}"

    def test_decreasing_trend_is_significant(self) -> None:
        """Série decrescente deve ter z negativo."""
        x = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], dtype=float)
        z, p = mann_kendall(x)
        assert z < 0
        assert p < 0.05

    def test_no_trend_high_pvalue(self) -> None:
        """Série aleatória deve ter p-value alto (sem tendência)."""
        np.random.seed(123)  # seed que gera série sem tendência clara
        x = np.random.randn(50)  # mais samples = mais robusto
        z, p = mann_kendall(x)
        assert p > 0.05, f"Esperado p > 0.05 para ruído, obtido {p}"

    def test_constant_series_returns_zero(self) -> None:
        """Série constante deve retornar z=0, p=1."""
        x = np.array([5, 5, 5, 5, 5], dtype=float)
        z, p = mann_kendall(x)
        assert z == 0.0
        assert p == 1.0

    def test_short_series_minimum_length(self) -> None:
        """Série com n=3 deve funcionar."""
        x = np.array([1, 2, 3], dtype=float)
        z, p = mann_kendall(x)
        assert isinstance(z, float)
        assert isinstance(p, float)
