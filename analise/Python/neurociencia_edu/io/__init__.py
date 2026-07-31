"""
neurociencia_edu.io
Módulos para entrada/saída de dados (BIDS, CSV, etc.).
"""

from neurociencia_edu.io.bids import (
    load_bids_dataset,
    create_bids_structure,
    participant_ids,
)

__all__ = [
    "load_bids_dataset",
    "create_bids_structure",
    "participant_ids",
]
