"""
00_setup.py
Setup global do projeto Python — instala MNE, configura paths,
define constantes usadas em todos os scripts.

Uso: import sys; sys.path.append("Python"); from setup import *
"""

import os
import sys
from pathlib import Path
import logging
from typing import Optional

# ============================================================
# 1. Paths do projeto
# ============================================================
PROJETO_ROOT = Path(__file__).resolve().parent.parent.parent  # /workspace
ANALISE_DIR = PROJETO_ROOT / "analise"
PYTHON_DIR = ANALISE_DIR / "Python"
DADOS_DIR = ANALISE_DIR / "dados"
RESULTADOS_DIR = ANALISE_DIR / "resultados"

PATHS = {
    "projeto_root": PROJETO_ROOT,
    "analise": ANALISE_DIR,
    "python": PYTHON_DIR,
    "dados_brutos": DADOS_DIR / "raw",
    "dados_processados": DADOS_DIR / "processed",
    "resultados": RESULTADOS_DIR,
}

# Criar diretórios
for name, path in PATHS.items():
    if isinstance(path, Path) and not path.exists():
        path.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. Logging estruturado
# ============================================================
def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """Configura logging estruturado.

    Args:
        level: Nível de log (logging.INFO, logging.DEBUG, etc.)
        log_file: Arquivo para salvar logs (opcional)

    Returns:
        Logger configurado
    """
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger("neurociencia_edu")
    logger.setLevel(level)
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (opcional)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Logger global
LOG = setup_logging()


# ============================================================
# 3. Verificação de dependências
# ============================================================
def check_dependencies() -> dict:
    """Verifica se as dependências principais estão instaladas.

    Returns:
        Dict com status de cada package
    """
    dependencies = {
        "mne": "EEG/ERP analysis",
        "numpy": "Computação numérica",
        "pandas": "Manipulação de dados",
        "scipy": "Computação científica",
        "matplotlib": "Visualização",
        "scikit-learn": "Machine learning (P04)",
    }

    status = {}
    for package, description in dependencies.items():
        try:
            __import__(package)
            status[package] = {"installed": True, "description": description}
        except ImportError:
            status[package] = {"installed": False, "description": description}

    return status


def install_dependencies() -> None:
    """Instala dependências faltantes via pip."""
    import subprocess

    LOG.info("Instalando dependências faltantes...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r",
        str(ANALISE_DIR / "requirements.txt")
    ])


# ============================================================
# 4. Configurações de EEG
# ============================================================
EEG_CONFIG = {
    "sfreq": 250,  # Hz, frequência de amostragem
    "l_freq": 0.1,  # Hz, passa-alta
    "h_freq": 30.0,  # Hz, passa-baixa
    "notch_freq": 60.0,  # Hz, notch para ruído elétrico
    "tmin": -0.2,  # s, baseline
    "tmax": 1.0,  # s, pós-estímulo
    "baseline": (-0.2, 0.0),  # tupla em segundos
    "reject": dict(eeg=100e-6),  # rejeitar trials com amplitude > 100 µV
    "montage": "standard_1020",  # montage padrão
    "n_channels": 32,  # número de eletrodos
    "reference": "average",  # tipo de referência
}

# Componentes ERP de interesse
ERP_COMPONENTS = {
    "N170": {
        "time_range": (0.13, 0.21),  # 130-210 ms
        "channels": ["P7", "P8", "O1", "O2"],
        "description": "Reconhecimento visual de letras/palavras",
    },
    "N400": {
        "time_range": (0.30, 0.50),  # 300-500 ms
        "channels": ["Cz", "CPz", "Pz"],
        "description": "Integração semântica",
    },
    "P300": {
        "time_range": (0.25, 0.45),  # 250-450 ms
        "channels": ["Cz", "Pz", "Fz"],
        "description": "Atenção e memória",
    },
    "P600": {
        "time_range": (0.50, 0.80),  # 500-800 ms
        "channels": ["Pz", "CPz"],
        "description": "Reanálise sintática/semântica",
    },
}


# ============================================================
# 5. Verificação inicial
# ============================================================
if __name__ == "__main__":
    LOG.info("=" * 50)
    LOG.info("Setup do projeto — Programa de Pesquisa")
    LOG.info("=" * 50)
    LOG.info(f"Diretório raiz: {PROJETO_ROOT}")
    LOG.info(f"Diretório de análise: {ANALISE_DIR}")

    LOG.info("\nVerificando dependências...")
    status = check_dependencies()

    missing = []
    for package, info in status.items():
        emoji = "✅" if info["installed"] else "❌"
        LOG.info(f"  {emoji} {package} ({info['description']})")
        if not info["installed"]:
            missing.append(package)

    if missing:
        LOG.warning(f"\n{len(missing)} dependências faltando: {', '.join(missing)}")
        LOG.info("Para instalar: pip install -r analise/requirements.txt")
    else:
        LOG.info("\n✅ Todas as dependências estão instaladas!")

    LOG.info("\nConfiguração de EEG:")
    for key, value in EEG_CONFIG.items():
        LOG.info(f"  {key}: {value}")

    LOG.info("\nComponentes ERP de interesse:")
    for component, config in ERP_COMPONENTS.items():
        LOG.info(f"  {component} ({config['time_range'][0]*1000:.0f}-{config['time_range'][1]*1000:.0f} ms): {config['description']}")
