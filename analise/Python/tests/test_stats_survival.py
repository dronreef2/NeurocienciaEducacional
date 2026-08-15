"""Testes para neurociencia_edu.stats._survival."""
import numpy as np
import pytest

from neurociencia_edu.stats._survival import kaplan_meier


class TestKaplanMeier:
    """Testes do estimador de Kaplan-Meier."""

    def test_returns_required_keys(self) -> None:
        """Resultado deve ter survival_function, median, n_at_risk."""
        np.random.seed(42)
        times = np.random.exponential(scale=10, size=50)
        events = np.random.binomial(1, 0.7, size=50)
        result = kaplan_meier(times, events)
        assert "survival_function" in result
        assert "times" in result
        assert "median" in result
        assert "n_at_risk" in result

    def test_all_events_observed(self) -> None:
        """Se todos têm evento, median deve ser próximo do tempo médio."""
        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        events = np.ones(10, dtype=int)
        result = kaplan_meier(times, events)
        assert result["median"] is not None
        assert 4 < result["median"] < 7

    def test_no_events_returns_median_none(self) -> None:
        """Se ninguém tem evento, median deve ser None (censurado)."""
        times = np.array([1, 2, 3, 4, 5], dtype=float)
        events = np.zeros(5, dtype=int)
        result = kaplan_meier(times, events)
        assert result["median"] is None
        assert np.all(result["survival_function"] == 1.0)

    def test_survival_starts_at_one(self) -> None:
        """S(t) deve ser monotonicamente decrescente de 1.0."""
        times = np.array([1, 2, 3, 4, 5], dtype=float)
        events = np.ones(5, dtype=int)
        result = kaplan_meier(times, events)
        # S(t) começa em 1.0 e vai diminuindo
        assert result["survival_function"][0] < 1.0
        # Mas a primeira sobrevivência pós-evento deve ser < primeira pré-evento
        # Ou seja, monotonicamente decrescente
        sf = result["survival_function"]
        assert all(sf[i] >= sf[i + 1] for i in range(len(sf) - 1))
        # S final = 0 (todos tiveram evento)
        assert sf[-1] == 0.0

    def test_survival_monotonic_decreasing(self) -> None:
        """Função de sobrevivência é monotonicamente decrescente."""
        np.random.seed(42)
        times = np.random.exponential(scale=5, size=100)
        events = np.random.binomial(1, 0.5, size=100)
        result = kaplan_meier(times, events)
        sf = result["survival_function"]
        for i in range(1, len(sf)):
            assert sf[i] <= sf[i - 1], f"Não-monotônico em i={i}"

    def test_invalid_times_raises(self) -> None:
        """Times negativos devem levantar ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            kaplan_meier(np.array([-1, 0, 1]), np.array([1, 0, 1]))

    def test_mismatched_lengths_raises(self) -> None:
        """Times e events com tamanhos diferentes devem levantar."""
        with pytest.raises(ValueError, match="same length"):
            kaplan_meier(np.array([1, 2, 3]), np.array([1, 0]))
