"""
neurociencia_edu: Pipeline de análise para o Programa de Pesquisa em Neurociência Educacional.

Este é o package principal que organiza os módulos de análise:
- neurociencia_edu.eeg: Pré-processamento e análise de EEG/ERP
- neurociencia_edu.stats: Análises estatísticas (LGCM, SEM, etc.)
- neurociencia_edu.io: Leitura/escrita de dados
- neurociencia_edu.dashboard: Interface Streamlit

Exemplo de uso:
    >>> from neurociencia_edu.eeg import preprocess_subject
    >>> from neurociencia_edu.stats import mediation_analysis
    >>> from neurociencia_edu.io import load_bids_dataset
"""

__version__ = "0.1.0"
__author__ = "Programa de Pesquisa em Neurociência Educacional (UFRN/CERES)"
__email__ = "pesquisa@neurociencia.edu"
__license__ = "MIT"

# Imports principais
from pathlib import Path

# Paths do projeto
PROJETO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ANALISE_DIR = PROJETO_ROOT / "analise"
DADOS_DIR = ANALISE_DIR / "dados"
RESULTADOS_DIR = ANALISE_DIR / "resultados"

# Configuração padrão
DEFAULT_SFREQ = 250
DEFAULT_L_FREQ = 0.1
DEFAULT_H_FREQ = 30.0
DEFAULT_NOTCH_FREQ = 60.0

# Janelas dos componentes ERP (em segundos)
ERP_WINDOWS = {
    "N170": (0.13, 0.21),
    "N400": (0.30, 0.50),
    "P300": (0.25, 0.45),
    "P600": (0.50, 0.80),
}

# Canais de interesse para cada componente
ERP_CHANNELS = {
    "N170": ["P7", "P8", "O1", "O2"],
    "N400": ["Cz", "CPz", "Pz"],
    "P300": ["Cz", "Pz", "Fz"],
    "P600": ["Pz", "CPz"],
}

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "PROJETO_ROOT",
    "ANALISE_DIR",
    "DADOS_DIR",
    "RESULTADOS_DIR",
    "DEFAULT_SFREQ",
    "DEFAULT_L_FREQ",
    "DEFAULT_H_FREQ",
    "DEFAULT_NOTCH_FREQ",
    "ERP_WINDOWS",
    "ERP_CHANNELS",
]
