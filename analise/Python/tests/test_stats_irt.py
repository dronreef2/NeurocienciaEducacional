"""Testes para neurociencia_edu.stats._irt."""
import numpy as np
import pytest

from neurociencia_edu.stats._irt import fit_rasch


class TestFitRasch:
    """Testes do ajuste do modelo de Rasch (1PL)."""

    def test_returns_dict_with_required_keys(self) -> None:
        """fit_rasch deve retornar dict com theta, b, se_theta, se_b."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert "theta" in result
        assert "b" in result
        assert "se_theta" in result
        assert "se_b" in result

    def test_theta_shape_matches_n_subjects(self) -> None:
        """theta deve ter n=100."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert result["theta"].shape == (100,)

    def test_b_shape_matches_n_items(self) -> None:
        """b (dificuldade) deve ter n=10."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert result["b"].shape == (10,)

    def test_easy_item_has_negative_b(self) -> None:
        """Item fácil (todos acertam) deve ter b negativo."""
        responses = np.ones((50, 5), dtype=int)
        result = fit_rasch(responses)
        assert result["b"][0] < 0

    def test_hard_item_has_positive_b(self) -> None:
        """Item difícil (ninguém acerta) deve ter b positivo."""
        responses = np.zeros((50, 5), dtype=int)
        result = fit_rasch(responses)
        assert result["b"][4] > 0

    def test_known_pattern_recovers_parameters(self) -> None:
        """Padrão conhecido: alta habilidade acerta tudo."""
        np.random.seed(42)
        high = (np.random.rand(20, 5) < 0.9).astype(int)
        low = (np.random.rand(20, 5) < 0.1).astype(int)
        responses = np.vstack([high, low])
        result = fit_rasch(responses)
        high_thetas = result["theta"][:20].mean()
        low_thetas = result["theta"][20:].mean()
        assert high_thetas > low_thetas

    def test_invalid_shape_raises(self) -> None:
        """Array 1D deve levantar ValueError."""
        with pytest.raises(ValueError, match="2D"):
            fit_rasch(np.array([1, 0, 1, 0]))

    def test_non_binary_raises(self) -> None:
        """Respostas não-binárias devem levantar ValueError."""
        with pytest.raises(ValueError, match="binary"):
            fit_rasch(np.array([[0, 1], [2, 0]]))
