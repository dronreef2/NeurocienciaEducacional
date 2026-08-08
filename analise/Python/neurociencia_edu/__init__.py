"""
neurociencia_edu
================

Educational Neuroscience Research Program.

A Python package for analyzing data from research on:
- Executive functions (BRIEF-2, Stroop, TMT)
- EEG/ERP (MNE-Python)
- IRT (Item Response Theory)
- SEM (Structural Equation Modeling)
- Mixed-effects models
- Bayesian analysis
- Network analysis

Submodules:
    eeg      — EEG/ERP preprocessing and analysis
    stats    — Statistical models (SEM, IRT, ANCOVA, mediation)
    io       — Data I/O (BIDS-like)
    dashboard — Streamlit dashboards
"""

__version__ = "0.1.0"
__author__ = "[Your Name]"
__email__ = "[your-email]@ufrn.br"

# Imports principais
try:
    from .eeg.preprocessing import preprocess_eeg
    from .eeg.erp import compute_erp
    from .stats.ancova import run_ancova
    from .stats.mediation import run_mediation
    from .stats.sem import run_sem
    from .io.bids import load_transcripts
except ImportError:
    # Optional dependencies not installed
    pass

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "preprocess_eeg",
    "compute_erp",
    "run_ancova",
    "run_mediation",
    "run_sem",
    "load_transcripts",
]
