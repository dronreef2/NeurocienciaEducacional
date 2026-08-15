"""Testes para neurociencia_edu.stats._drift."""
import numpy as np
import pandas as pd
import pytest

from neurociencia_edu.stats._drift import psi, ks_test, drift_report


class TestPSI:
    """Testes do Population Stability Index."""

    def test_same_distribution_low_psi(self) -> None:
        """Mesma distribuição deve ter PSI próximo de 0."""
        np.random.seed(42)
        baseline = np.random.randn(1000)
        current = np.random.randn(1000)
        result = psi(baseline, current, bins=10)
        assert result < 0.1, f"Esperado PSI < 0.1, obtido {result}"

    def test_shifted_distribution_high_psi(self) -> None:
        """Distribuição deslocada deve ter PSI > 0.1."""
        np.random.seed(42)
        baseline = np.random.randn(1000)
        current = np.random.randn(1000) + 2.0  # shift de 2
        result = psi(baseline, current, bins=10)
        assert result > 0.1, f"Esperado PSI > 0.1, obtido {result}"

    def test_small_samples_raises(self) -> None:
        """Amostras pequenas devem levantar erro."""
        with pytest.raises(ValueError, match="muito pequenas"):
            psi(np.array([1, 2, 3]), np.array([4, 5, 6]), bins=10)


class TestKSTest:
    """Testes do Kolmogorov-Smirnov test."""

    def test_same_distribution_not_significant(self) -> None:
        """Mesma distribuição não deve ser significativa."""
        np.random.seed(42)
        baseline = np.random.randn(100)
        current = np.random.randn(100)
        result = ks_test(baseline, current)
        assert result["p_value"] > 0.05

    def test_different_distribution_significant(self) -> None:
        """Distribuições diferentes devem ser significativas."""
        np.random.seed(42)
        baseline = np.random.randn(100)
        current = np.random.randn(100) + 1.5
        result = ks_test(baseline, current)
        assert result["p_value"] < 0.05
        assert bool(result["significant"]) is True

    def test_returns_dict(self) -> None:
        """Resultado deve ser dict com chaves esperadas."""
        np.random.seed(42)
        result = ks_test(np.random.randn(50), np.random.randn(50))
        assert "statistic" in result
        assert "p_value" in result
        assert "significant" in result


class TestDriftReport:
    """Testes do relatório consolidado."""

    def test_no_drift_same_data(self) -> None:
        """Mesmo dataset não deve ter drift."""
        np.random.seed(42)
        df = pd.DataFrame({
            "x": np.random.randn(500),
            "y": np.random.randn(500),
        })
        report = drift_report(df, df.copy())
        assert report["drift_detected"] is False
        assert "x" in report["columns_analyzed"]

    def test_drift_in_one_column(self) -> None:
        """Mudança em uma coluna deve detectar drift."""
        np.random.seed(42)
        baseline = pd.DataFrame({"x": np.random.randn(500)})
        current = pd.DataFrame({"x": np.random.randn(500) + 3.0})  # shift
        report = drift_report(baseline, current)
        assert report["drift_detected"] is True
        assert "x" in report["columns_analyzed"]
        assert report["x"]["psi"] > 0.1

    def test_specific_columns(self) -> None:
        """Deve analisar só colunas especificadas."""
        np.random.seed(42)
        df = pd.DataFrame({
            "a": np.random.randn(100),
            "b": np.random.randn(100),
            "c": np.random.randn(100),
        })
        report = drift_report(df, df.copy(), columns=["a", "c"])
        assert "a" in report["columns_analyzed"]
        assert "b" not in report["columns_analyzed"]
