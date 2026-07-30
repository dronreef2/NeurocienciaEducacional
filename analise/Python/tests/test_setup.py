"""
tests/test_setup.py
Testes unitários para o setup Python e configuração EEG.
Framework: pytest
"""

import sys
from pathlib import Path
import pytest

# Adicionar path para importar setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from setup import (
    PATHS, LOG, EEG_CONFIG, ERP_COMPONENTS,
    check_dependencies, setup_logging
)


# ============================================================
# Test: paths são criados
# ============================================================
def test_paths_criados():
    """Todos os paths devem existir ou poder ser criados."""
    for name, path in PATHS.items():
        if isinstance(path, Path):
            assert path.exists() or path.parent.exists(), f"Path {name} ({path}) não existe"


# ============================================================
# Test: configuração EEG tem valores esperados
# ============================================================
def test_eeg_config_sfreq():
    """Frequência de amostragem deve estar em range razoável."""
    assert 100 <= EEG_CONFIG["sfreq"] <= 1000
    assert isinstance(EEG_CONFIG["sfreq"], int)


def test_eeg_config_filter():
    """Filtros devem ser consistentes."""
    assert EEG_CONFIG["l_freq"] < EEG_CONFIG["h_freq"]
    assert EEG_CONFIG["l_freq"] >= 0
    assert EEG_CONFIG["h_freq"] <= 100  # Nyquist


def test_eeg_config_baseline():
    """Baseline deve estar dentro da janela do epoch."""
    assert EEG_CONFIG["baseline"][0] < EEG_CONFIG["baseline"][1]
    assert EEG_CONFIG["baseline"][0] >= EEG_CONFIG["tmin"]
    assert EEG_CONFIG["baseline"][1] <= EEG_CONFIG["tmax"]


def test_eeg_config_tmin_tmax():
    """Janela do epoch deve ser razoável."""
    assert EEG_CONFIG["tmin"] < EEG_CONFIG["tmax"]
    assert EEG_CONFIG["tmax"] - EEG_CONFIG["tmin"] <= 3.0  # não mais que 3s


# ============================================================
# Test: componentes ERP
# ============================================================
def test_erp_components_definidos():
    """Todos os componentes ERP principais devem estar definidos."""
    expected = ["N170", "N400", "P300", "P600"]
    for comp in expected:
        assert comp in ERP_COMPONENTS, f"Componente {comp} não definido"


def test_erp_component_structure():
    """Cada componente deve ter time_range, channels, description."""
    for comp_name, config in ERP_COMPONENTS.items():
        assert "time_range" in config, f"{comp_name}: falta time_range"
        assert "channels" in config, f"{comp_name}: falta channels"
        assert "description" in config, f"{comp_name}: falta description"

        # time_range deve ser tupla de 2 floats crescentes
        tmin, tmax = config["time_range"]
        assert tmin < tmax, f"{comp_name}: time_range inválido"
        assert 0 <= tmin <= 1.0, f"{comp_name}: tmin fora do range"


def test_erp_components_nao_sobrepoem():
    """Componentes devem ter janelas aproximadamente separadas."""
    n170_range = ERP_COMPONENTS["N170"]["time_range"]
    n400_range = ERP_COMPONENTS["N400"]["time_range"]
    # N170 termina antes de N400 começar (ou pelo menos não muito antes)
    # Permitir overlap leve
    assert n170_range[1] < n400_range[1] or n170_range[0] < n400_range[0]


# ============================================================
# Test: dependências
# ============================================================
def test_check_dependencies_retorna_dict():
    """check_dependencies deve retornar dict."""
    status = check_dependencies()
    assert isinstance(status, dict)
    assert len(status) > 0


def test_check_dependencies_status_keys():
    """Cada dependência deve ter chaves esperadas."""
    status = check_dependencies()
    for pkg, info in status.items():
        assert "installed" in info
        assert "description" in info
        assert isinstance(info["installed"], bool)


# ============================================================
# Test: logging
# ============================================================
def test_setup_logging_default():
    """Logger padrão deve ser configurável."""
    logger = setup_logging()
    assert logger is not None
    assert logger.level >= 0  # algum nível


def test_setup_logging_with_file(tmp_path):
    """Logger deve aceitar arquivo."""
    log_file = tmp_path / "test.log"
    logger = setup_logging(log_file=log_file)
    logger.info("test message")

    # Verificar que log foi escrito
    assert log_file.exists()
    content = log_file.read_text()
    assert "test message" in content


def test_setup_logging_levels():
    """Logger deve respeitar níveis."""
    import logging
    logger = setup_logging(level=logging.WARNING)
    assert logger.level == logging.WARNING
