"""
Exceptions: Exceções customizadas do pacote neurociencia_edu.

Hierarquia:
    NeurocienciaEduError (base)
    ├── ConfigurationError
    ├── DataError
    │   ├── DataNotFoundError
    │   ├── DataValidationError
    │   └── DataAnonymizationError
    ├── ProcessingError
    │   ├── FitError
    │   ├── ConvergenceError
    │   └── InsufficientDataError
    └── AnalysisError
        ├── StatisticalTestError
        └── SimulationError
"""

from __future__ import annotations

from typing import Any, Optional


class NeurocienciaEduError(Exception):
    """Exceção base do pacote neurociencia_edu.

    Args:
        message: Mensagem de erro.
        details: Detalhes adicionais (opcional).
    """

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ConfigurationError(NeurocienciaEduError):
    """Erro de configuração."""


class DataError(NeurocienciaEduError):
    """Erro relacionado a dados."""


class DataNotFoundError(DataError):
    """Dados não encontrados."""


class DataValidationError(DataError):
    """Dados inválidos."""


class DataAnonymizationError(DataError):
    """Erro na anonimização de dados."""


class ProcessingError(NeurocienciaEduError):
    """Erro de processamento."""


class FitError(ProcessingError):
    """Erro no ajuste de modelo."""


class ConvergenceError(ProcessingError):
    """Modelo não convergiu."""


class InsufficientDataError(ProcessingError):
    """Dados insuficientes para a operação."""


class AnalysisError(NeurocienciaEduError):
    """Erro de análise."""


class StatisticalTestError(AnalysisError):
    """Erro em teste estatístico."""


class SimulationError(AnalysisError):
    """Erro em simulação."""
