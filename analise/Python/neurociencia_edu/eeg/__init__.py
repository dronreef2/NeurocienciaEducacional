"""Módulo de EEG do pacote neurociencia_edu."""
from neurociencia_edu.eeg._preprocess import preprocess_eeg
from neurociencia_edu.eeg._erp import compute_erp

__all__ = ["preprocess_eeg", "compute_erp"]
