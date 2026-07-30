"""
tests/test_eeg_pipeline.py
Testes para o pipeline de pré-processamento e análise de EEG.
"""

import sys
from pathlib import Path
import pytest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ============================================================
# Fixtures
# ============================================================
@pytest.fixture
def synthetic_raw():
    """Cria dados de EEG sintéticos para testes."""
    try:
        import mne
    except ImportError:
        pytest.skip("MNE não instalado")

    # Criar raw sintético
    sfreq = 250  # Hz
    n_channels = 32
    duration = 60  # segundos
    n_samples = int(sfreq * duration)

    # Gerar dados aleatórios
    data = np.random.randn(n_channels, n_samples) * 1e-6  # µV

    # Criar info
    ch_names = [f"EEG {i:03d}" for i in range(1, n_channels + 1)]
    ch_types = ["eeg"] * n_channels
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

    raw = mne.io.RawArray(data, info)
    return raw


@pytest.fixture
def synthetic_epochs(synthetic_raw):
    """Cria epochs sintéticos."""
    try:
        import mne
    except ImportError:
        pytest.skip("MNE não instalado")

    # Adicionar eventos
    sfreq = synthetic_raw.info["sfreq"]
    n_events = 50
    events = np.zeros((n_events, 3), dtype=int)
    events[:, 0] = np.linspace(100, len(synthetic_raw.times) - 1000, n_events)
    events[:, 2] = np.random.choice([1, 2, 3], n_events)  # 3 condições

    epochs = mne.Epochs(
        synthetic_raw,
        events,
        event_id={"cond1": 1, "cond2": 2, "cond3": 3},
        tmin=-0.2,
        tmax=1.0,
        baseline=(-0.2, 0.0),
        preload=True,
        reject=None,  # não rejeitar para teste
    )
    return epochs


# ============================================================
# Test: imports
# ============================================================
def test_mne_importa():
    """MNE deve importar corretamente."""
    try:
        import mne
        assert mne.__version__ >= "1.0"
    except ImportError:
        pytest.skip("MNE não instalado")


def test_numpy_pandas_importam():
    """Numpy e pandas devem estar disponíveis."""
    import numpy
    import pandas
    assert numpy.__version__ >= "1.20"
    assert pandas.__version__ >= "1.0"


# ============================================================
# Test: pipeline de pré-processamento
# ============================================================
def test_filter_aplica(synthetic_raw):
    """Filtro deve aplicar sem erros."""
    try:
        import mne
    except ImportError:
        pytest.skip("MNE não instalado")

    raw_filt = synthetic_raw.copy().filter(l_freq=1.0, h_freq=30.0)
    assert raw_filt.n_times == synthetic_raw.n_times
    # Dados devem ter sido modificados
    assert not np.allclose(raw_filt._data, synthetic_raw._data)


def test_notch_filter(synthetic_raw):
    """Notch filter deve aplicar."""
    raw_notch = synthetic_raw.copy().notch_filter(freqs=[60.0])
    assert raw_notch.n_times == synthetic_raw.n_times


def test_ica_fit(synthetic_raw):
    """ICA deve ajustar."""
    try:
        from mne.preprocessing import ICA
    except ImportError:
        pytest.skip("MNE.preprocessing não disponível")

    ica = ICA(n_components=10, method="fastica", random_state=42)
    ica.fit(synthetic_raw.filter(l_freq=1.0, h_freq=30.0))
    assert ica.n_components_ == 10


def test_epochs_create(synthetic_raw):
    """Epochs devem ser criados."""
    try:
        import mne
    except ImportError:
        pytest.skip("MNE não instalado")

    sfreq = synthetic_raw.info["sfreq"]
    n_events = 30
    events = np.zeros((n_events, 3), dtype=int)
    events[:, 0] = np.linspace(100, len(synthetic_raw.times) - 1000, n_events)
    events[:, 2] = 1

    epochs = mne.Epochs(
        synthetic_raw,
        events,
        event_id={"event": 1},
        tmin=-0.2,
        tmax=1.0,
        baseline=(-0.2, 0.0),
        preload=True,
        reject=None,
    )
    assert len(epochs) == n_events


# ============================================================
# Test: ERP analysis
# ============================================================
def test_grand_average(synthetic_epochs):
    """Grand average deve calcular."""
    evoked = synthetic_epochs.average()
    assert evoked.data.shape[0] == len(synthetic_epochs.ch_names)
    assert evoked.data.shape[1] > 0


def test_extract_metrics():
    """Métricas dos componentes devem ser extraídas."""
    # Simular grand average
    times = np.linspace(-0.2, 1.0, 301)
    n_channels = 32
    data = np.random.randn(n_channels, len(times)) * 1e-6

    # Simular N170 (negativo em 150ms)
    ch_occipital = [15, 16, 17, 18]
    n170_idx = np.argmin(np.abs(times - 0.15))
    data[ch_occipital, n170_idx] = -5e-6

    # Calcular amplitude média em 130-210 ms
    mask = (times >= 0.13) & (times <= 0.21)
    amplitude_n170 = data[ch_occipital][:, mask].mean() * 1e6

    # Deve ser próximo de -5 µV
    assert -7 < amplitude_n170 < -3


def test_topography_creation():
    """Topografia deve poder ser plotada."""
    try:
        import mne
    except ImportError:
        pytest.skip("MNE não instalado")

    # Criar info
    ch_names = mne.channels.make_standard_montage("standard_1020").ch_names
    info = mne.create_info(ch_names=ch_names, sfreq=250, ch_types="eeg")
    info.set_montage("standard_1020")

    # Dados sintéticos
    data = np.random.randn(len(ch_names), 1) * 1e-6

    # Tentar plotar (mas não salvar)
    fig = mne.viz.plot_topomap(data[:, 0], info, show=False)
    assert fig is not None


# ============================================================
# Test: permutation test
# ============================================================
def test_cluster_permutation():
    """Cluster permutation deve funcionar com dados sintéticos."""
    try:
        import mne
        from mne.stats import spatio_temporal_cluster_1samp_test
    except ImportError:
        pytest.skip("MNE stats não disponível")

    # Dados: sujeitos x canais x tempo
    n_subjects = 10
    n_channels = 20
    n_times = 100

    # Condição 1: ruído
    X1 = np.random.randn(n_subjects, n_channels, n_times) * 1e-6

    # Condição 2: ruído + efeito
    X2 = np.random.randn(n_subjects, n_channels, n_times) * 1e-6
    X2[:, 5:10, 30:50] += 2e-6  # efeito em canais 5-10, tempo 30-50

    # Diferença
    X = X1 - X2

    # Cluster permutation
    t_obs, clusters, cluster_pv, H0 = spatio_temporal_cluster_1samp_test(
        X, n_permutations=100, seed=42
    )

    # Deve retornar estrutura esperada
    assert t_obs.shape == (n_channels, n_times)
    assert len(clusters) > 0
    assert len(cluster_pv) == len(clusters)
