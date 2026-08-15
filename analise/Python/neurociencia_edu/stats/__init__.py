"""Módulo de estatística do pacote neurociencia_edu."""
from neurociencia_edu.stats._trends import mann_kendall
from neurociencia_edu.stats._power import power_analysis
from neurociencia_edu.stats._irt import fit_rasch
from neurociencia_edu.stats._survival import kaplan_meier

__all__ = ["mann_kendall", "power_analysis", "fit_rasch", "kaplan_meier"]
