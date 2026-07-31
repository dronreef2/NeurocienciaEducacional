"""
neurociencia_edu.eeg: Módulos para pré-processamento e análise de EEG/ERP.
"""

from neurociencia_edu.eeg.preprocessing import (
    preprocess_subject,
    filter_raw,
    run_ica,
    create_epochs,
    save_processed,
)
from neurociencia_edu.eeg.erp import (
    compute_grand_average,
    extract_component_metrics,
    plot_erps,
    plot_topographies,
    permutation_test,
    load_epochs,
    ERP_COMPONENTS,
)

__all__ = [
    "preprocess_subject",
    "filter_raw",
    "run_ica",
    "create_epochs",
    "save_processed",
    "compute_grand_average",
    "extract_component_metrics",
    "plot_erps",
    "plot_topographies",
    "permutation_test",
    "load_epochs",
    "ERP_COMPONENTS",
]
