"""Pré-processamento de sinais EEG."""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from neurociencia_edu.exceptions import ConfigurationError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def preprocess_eeg(
    raw: np.ndarray,
    sfreq: float,
    l_freq: float = 0.1,
    h_freq: float = 40.0,
    notch: float = 60.0,
    order: int = 4,
) -> np.ndarray:
    """Pré-processa sinal EEG com filtros padrão.

    Args:
        raw: Array (n_channels, n_samples) com sinal EEG em volts.
        sfreq: Taxa de amostragem em Hz.
        l_freq: Frequência de corte passa-alta.
        h_freq: Frequência de corte passa-baixa.
        notch: Frequência do filtro notch.
        order: Ordem do filtro Butterworth.

    Returns:
        Sinal filtrado com mesma forma do input.
    """
    if sfreq <= 0:
        raise ConfigurationError(f"sfreq must be > 0, got {sfreq}")
    if l_freq >= h_freq:
        raise ConfigurationError(f"l_freq must be < h_freq, got l_freq={l_freq}, h_freq={h_freq}")

    logger.debug(f"Preprocessing EEG: shape={raw.shape}, sfreq={sfreq}, band=[{l_freq}, {h_freq}]Hz")
    data = raw.copy().astype(float)

    if l_freq > 0:
        b, a = butter(order, l_freq / (sfreq / 2), btype="high")
        data = filtfilt(b, a, data, axis=1)

    if h_freq < sfreq / 2:
        b, a = butter(order, h_freq / (sfreq / 2), btype="low")
        data = filtfilt(b, a, data, axis=1)

    if notch > 0 and notch < sfreq / 2:
        b, a = iirnotch(notch, Q=30, fs=sfreq)
        data = filtfilt(b, a, data, axis=1)

    return data
