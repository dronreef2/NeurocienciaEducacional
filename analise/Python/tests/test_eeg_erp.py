"""Testes para neurociencia_edu.eeg._erp."""
import numpy as np
import pytest

from neurociencia_edu.eeg._erp import compute_erp


class TestComputeERP:
    """Testes do cálculo de ERP."""

    def test_output_shape(self) -> None:
        """ERP médio deve ter shape (n_channels, n_times)."""
        n_trials, n_channels, n_times = 30, 32, 500
        trials = np.random.randn(n_trials, n_channels, n_times) * 1e-6
        times = np.linspace(-0.2, 1.0, n_times)
        erp = compute_erp(trials, times)
        assert erp.shape == (n_channels, n_times)

    def test_grand_average_is_mean(self) -> None:
        """ERP sem baseline deve ser a média dos trials."""
        n_trials, n_channels, n_times = 10, 4, 100
        trials = np.random.randn(n_trials, n_channels, n_times)
        times = np.linspace(-0.1, 0.5, n_times)
        erp = compute_erp(trials, times, baseline=None)
        np.testing.assert_array_almost_equal(erp, trials.mean(axis=0))

    def test_baseline_correction(self) -> None:
        """Baseline deve ser subtraído da média."""
        n_trials, n_channels, n_times = 20, 4, 200
        trials = np.random.randn(n_trials, n_channels, n_times) * 1e-6 + 5e-6
        times = np.linspace(-0.2, 0.5, n_times)
        erp = compute_erp(trials, times, baseline=(-0.2, 0.0))
        baseline_mask = (times >= -0.2) & (times < 0.0)
        baseline_mean = erp[:, baseline_mask].mean()
        assert abs(baseline_mean) < 1e-7

    def test_no_baseline_keeps_offset(self) -> None:
        """Sem baseline, offset é preservado."""
        n_trials, n_channels, n_times = 5, 2, 100
        offset = 3e-6
        trials = np.ones((n_trials, n_channels, n_times)) * offset
        times = np.linspace(-0.1, 0.5, n_times)
        erp = compute_erp(trials, times, baseline=None)
        assert abs(erp.mean() - offset) < 1e-9

    def test_3d_input_required(self) -> None:
        """Input deve ser 3D."""
        with pytest.raises(ValueError, match="3D"):
            compute_erp(np.zeros((10, 100)), np.linspace(0, 1, 100))

    def test_times_length_mismatch(self) -> None:
        """times deve ter mesmo tamanho do último dim de trials."""
        trials = np.zeros((10, 4, 100))
        times = np.linspace(0, 1, 50)
        with pytest.raises(ValueError, match="times length"):
            compute_erp(trials, times)
