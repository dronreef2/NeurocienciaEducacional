"""
Tests for the neurociencia_edu package.
"""

import pytest
import numpy as np


def test_version():
    """Verifica que a versão está definida."""
    from neurociencia_edu import __version__
    assert __version__ == "0.1.0"


def test_imports():
    """Verifica que os módulos principais importam."""
    from neurociencia_edu import (
        ERP_WINDOWS,
        ERP_CHANNELS,
        DEFAULT_SFREQ,
        DEFAULT_L_FREQ,
        DEFAULT_H_FREQ,
    )
    assert DEFAULT_SFREQ > 0
    assert "N170" in ERP_WINDOWS
    assert "N400" in ERP_WINDOWS


def test_paths():
    """Verifica que os paths do projeto são Path objects."""
    from neurociencia_edu import (
        PROJETO_ROOT,
        ANALISE_DIR,
        DADOS_DIR,
        RESULTADOS_DIR,
    )
    from pathlib import Path
    assert isinstance(PROJETO_ROOT, Path)
    assert isinstance(ANALISE_DIR, Path)


def test_mediation_basic():
    """Testa análise de mediação com dados sintéticos."""
    from neurociencia_edu.stats import mediation_analysis

    np.random.seed(42)
    n = 200
    X = np.random.randn(n)
    M = 0.5 * X + np.random.randn(n) * 0.5
    Y = 0.3 * X + 0.3 * M + np.random.randn(n) * 0.5

    result = mediation_analysis(X, M, Y, n_bootstrap=100)

    # Efeito indireto deve ser próximo de 0.15 (0.5 * 0.3)
    assert abs(result.indirect - 0.15) < 0.1
    # Efeito direto deve ser próximo de 0.3
    assert abs(result.c_prime - 0.3) < 0.2
    # a e b devem estar próximos dos verdadeiros
    assert abs(result.a - 0.5) < 0.2
    assert abs(result.b - 0.3) < 0.2


def test_cohens_d():
    """Testa cálculo de Cohen's d."""
    from neurociencia_edu.stats import cohens_d

    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = np.random.normal(0.5, 1, 100)

    d = cohens_d(x, y)
    # d deve ser próximo de -0.5 (x menor que y)
    assert -0.7 < d < -0.3


def test_erp_components():
    """Testa configuração dos componentes ERP."""
    from neurociencia_edu.eeg import ERP_COMPONENTS
    from neurociencia_edu import ERP_WINDOWS, ERP_CHANNELS

    assert set(ERP_COMPONENTS.keys()) == {"N170", "N400", "P300", "P600"}
    for comp in ERP_COMPONENTS.values():
        assert "time_range" in comp
        assert "channels" in comp
        assert "description" in comp


def test_bids_participant_ids(tmp_path):
    """Testa listagem de participantes BIDS."""
    from neurociencia_edu.io.bids import participant_ids

    # Criar estrutura
    (tmp_path / "sub-01").mkdir()
    (tmp_path / "sub-02").mkdir()
    (tmp_path / "sub-03").mkdir()
    (tmp_path / "not_a_subject.txt").touch()

    ids = participant_ids(tmp_path)
    assert ids == ["sub-01", "sub-02", "sub-03"]


def test_bids_load(tmp_path):
    """Testa carregamento de dataset BIDS."""
    from neurociencia_edu.io.bids import load_bids_dataset, create_bids_structure

    create_bids_structure(
        tmp_path,
        project_name="test",
        participants=["01", "02"],
        modalities=["eeg"],
    )

    dataset = load_bids_dataset(tmp_path)
    assert dataset["participants"] == ["sub-01", "sub-02"]
    assert "eeg" in dataset["modalities"]
