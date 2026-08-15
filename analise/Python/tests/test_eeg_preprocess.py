"""Testes para neurociencia_edu.eeg._preprocess."""
import numpy as np
import pytest

from neurociencia_edu.eeg._preprocess import preprocess_eeg


class TestPreprocessEEG:
    """Testes do pré-processamento de EEG."""

    def test_output_shape_matches_input(self) -> None:
        """Output deve ter mesma forma do input."""
        raw = np.random.randn(32, 5000) * 1e-6
        clean = preprocess_eeg(raw, sfreq=500)
        assert clean.shape == raw.shape

    def test_highpass_removes_dc_offset(self) -> None:
        """Passa-alta deve remover offset DC."""
        raw = np.ones((32, 5000)) * 5e-6
        clean = preprocess_eeg(raw, sfreq=500, l_freq=1.0)
        assert abs(clean.mean()) < 1e-6

    def test_lowpass_smoothing(self) -> None:
        """Passa-baixa deve suavizar ruído de alta frequência."""
        t = np.arange(2000) / 500.0
        signal = 1e-6 * np.sin(2 * np.pi * 5 * t)
        noise = np.random.randn(32, 2000) * 5e-6
        raw = signal[None, :] + noise
        clean = preprocess_eeg(raw, sfreq=500, l_freq=0.1, h_freq=10.0)
        assert clean.var() < raw.var()

    def test_invalid_sfreq_raises(self) -> None:
        """sfreq <= 0 deve levantar ConfigurationError."""
        from neurociencia_edu.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError, match="sfreq"):
            preprocess_eeg(np.zeros((32, 100)), sfreq=0)

    def test_invalid_freq_range_raises(self) -> None:
        """l_freq >= h_freq deve levantar ConfigurationError."""
        from neurociencia_edu.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError, match="l_freq"):
            preprocess_eeg(np.zeros((32, 100)), sfreq=500, l_freq=40, h_freq=10)

    def test_no_filters_returns_unchanged_shape(self) -> None:
        """Sem filtros (l=0, h=sfreq/2), shape preservado."""
        raw = np.random.randn(8, 1000) * 1e-6
        clean = preprocess_eeg(raw, sfreq=100, l_freq=0, h_freq=49, notch=0)
        assert clean.shape == raw.shape
