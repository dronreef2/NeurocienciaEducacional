"""Testes para neurociencia_edu.stats._power."""
import pytest

from neurociencia_edu.stats._power import power_analysis


class TestPowerAnalysis:
    """Testes do cálculo de poder estatístico."""

    def test_ttest_high_n_high_power(self) -> None:
        """t-test com n=100, d=0.5 → power > 0.90."""
        p = power_analysis(effect_size=0.5, n=100, test="t_test")
        assert 0.90 < p < 1.0, f"Esperado power > 0.90, obtido {p:.3f}"

    def test_ttest_low_n_low_power(self) -> None:
        """t-test com n=10, d=0.2 → power < 0.30."""
        p = power_analysis(effect_size=0.2, n=10, test="t_test")
        assert p < 0.30, f"Esperado power < 0.30, obtido {p:.3f}"

    def test_correlation_default(self) -> None:
        """Correlação r=0.3, n=50 → power moderado."""
        p = power_analysis(effect_size=0.3, n=50, test="correlation")
        assert 0.30 < p < 0.90, f"power={p:.3f}"

    def test_anova_medium_effect(self) -> None:
        """ANOVA f=0.25, n=50 → power ~0.50."""
        p = power_analysis(effect_size=0.25, n=50, test="anova")
        assert 0.20 < p < 0.80

    def test_zero_effect_zero_power(self) -> None:
        """Effect size zero deve dar power = alpha."""
        p = power_analysis(effect_size=0.0, n=100, test="t_test")
        assert abs(p - 0.05) < 0.01

    def test_invalid_test_raises(self) -> None:
        """Test inválido deve levantar StatisticalTestError."""
        from neurociencia_edu.exceptions import StatisticalTestError
        with pytest.raises(StatisticalTestError, match="Unknown test"):
            power_analysis(effect_size=0.5, n=50, test="invalid")

    def test_invalid_n_raises(self) -> None:
        """N <= 0 deve levantar ValueError."""
        with pytest.raises(ValueError, match="n must be"):
            power_analysis(effect_size=0.5, n=0, test="t_test")
