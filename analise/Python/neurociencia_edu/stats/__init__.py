"""
neurociencia_edu.stats
Módulos para análises estatísticas avançadas.
"""

from neurociencia_edu.stats.mediation import (
    mediation_analysis,
    bootstrap_mediation,
    cohens_d,
)

__all__ = [
    "mediation_analysis",
    "bootstrap_mediation",
    "cohens_d",
]
