"""
neurociencia_edu.eeg.preprocessing
Módulo refatorado de pré-processamento de EEG.
Baseado em: Luck (2014), Cohen (2014), Mike Cohen tutorials.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import mne
import numpy as np
import pandas as pd
from scipy.stats import kurtosis

from neurociencia_edu import DEFAULT_SFREQ, DEFAULT_L_FREQ, DEFAULT_H_FREQ, DEFAULT_NOTCH_FREQ

logger = logging.getLogger(__name__)


# ============================================================
# 1. Carregar dados
# ============================================================
def load_raw(input_path: str | Path) -> mne.io.Raw:
    """Carrega arquivo de EEG.

    Suporta: BrainVision (.vhdr), EDF (.edf), BIDS (.bdf), FIF (.fif)

    Args:
        input_path: Caminho do arquivo.

    Returns:
        Objeto mne.io.Raw com os dados.

    Raises:
        FileNotFoundError: Se o arquivo não existe.
        ValueError: Se o formato não é suportado.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    ext = input_path.suffix.lower()
    logger.info(f"Carregando: {input_path}")

    if ext == ".vhdr":
        raw = mne.io.read_raw_brainvision(input_path, preload=True)
    elif ext == ".edf":
        raw = mne.io.read_raw_edf(input_path, preload=True)
    elif ext == ".bdf":
        raw = mne.io.read_raw_bdf(input_path, preload=True)
    elif ext in (".fif", ".fif.gz"):
        raw = mne.io.read_raw_fif(input_path, preload=True)
    else:
        raise ValueError(f"Formato não suportado: {ext}")

    logger.info(
        f"  Dados: {raw.n_times} samples, "
        f"{raw.info['sfreq']} Hz, "
        f"{len(raw.ch_names)} canais, "
        f"{raw.times[-1]:.1f} s"
    )
    return raw


# ============================================================
# 2. Configurar montage
# ============================================================
def setup_montage(
    raw: mne.io.Raw,
    montage_name: str = "standard_1020",
) -> mne.io.Raw:
    """Configura montage (posições dos eletrodos).

    Args:
        raw: Objeto Raw.
        montage_name: Nome do montage (e.g. "standard_1020", "standard_1005").

    Returns:
        Raw com montage setada.
    """
    logger.info(f"Configurando montage: {montage_name}")
    try:
        montage = mne.channels.make_standard_montage(montage_name)
        raw.set_montage(montage, on_missing="warn")
        logger.info(f"  ✅ Montage {montage_name} setada")
    except Exception as e:
        logger.warning(f"  ⚠️ Erro: {e}")
    return raw


# ============================================================
# 3. Filtrar
# ============================================================
def filter_raw(
    raw: mne.io.Raw,
    l_freq: float = DEFAULT_L_FREQ,
    h_freq: float = DEFAULT_H_FREQ,
    notch_freq: float = DEFAULT_NOTCH_FREQ,
) -> mne.io.Raw:
    """Aplica filtros passa-banda e notch.

    Args:
        raw: Objeto Raw.
        l_freq: Frequência de corte passa-alta (Hz).
        h_freq: Frequência de corte passa-baixa (Hz).
        notch_freq: Frequência do notch (Hz, 0 para pular).

    Returns:
        Raw filtrado.
    """
    logger.info(f"Filtrando: {l_freq}-{h_freq} Hz + notch {notch_freq} Hz")
    raw = raw.copy()
    raw.filter(
        l_freq=l_freq,
        h_freq=h_freq,
        method="fir",
        phase="zero",
        fir_design="firwin",
    )
    if notch_freq > 0:
        raw.notch_filter(freqs=[notch_freq], method="spectrum_fit")
    return raw


# ============================================================
# 4. Remover canais ruins
# ============================================================
def detect_bad_channels(
    raw: mne.io.Raw,
    kurtosis_threshold: float = 0.4,
) -> list[str]:
    """Identifica canais ruins baseado em kurtose.

    Args:
        raw: Objeto Raw.
        kurtosis_threshold: Limite inferior de kurtose (canais com kurtose < são marcados).

    Returns:
        Lista de nomes de canais ruins.
    """
    bad_channels = []
    for ch in raw.ch_names:
        ch_data = raw.get_data(picks=[ch])[0]
        kurt = kurtosis(ch_data)
        if kurt < kurtosis_threshold:
            bad_channels.append(ch)
    return bad_channels


# ============================================================
# 5. ICA
# ============================================================
def run_ica(
    raw: mne.io.Raw,
    n_components: int = 20,
    random_state: int = 42,
) -> tuple[mne.io.Raw, mne.preprocessing.ICA]:
    """Aplica ICA e remove artefatos automaticamente.

    Args:
        raw: Objeto Raw (filtrado).
        n_components: Número de componentes.
        random_state: Seed para reprodutibilidade.

    Returns:
        Raw limpo, objeto ICA.
    """
    logger.info(f"Aplicando ICA com {n_components} componentes...")
    from mne.preprocessing import ICA

    ica = ICA(
        n_components=n_components,
        method="fastica",
        max_iter="auto",
        random_state=random_state,
    )
    ica.fit(raw)

    eog_idx, _ = ica.find_bads_eog(raw, threshold=0.5)
    muscle_idx, _ = ica.find_bads_muscle(raw, threshold=0.5)

    logger.info(f"  EOG: {len(eog_idx)} componentes, Muscle: {len(muscle_idx)} componentes")
    ica.exclude = list(set(eog_idx + muscle_idx))

    raw_clean = ica.apply(raw.copy())
    return raw_clean, ica


# ============================================================
# 6. Re-referenciar
# ============================================================
def set_reference(
    raw: mne.io.Raw,
    reference: str = "average",
) -> mne.io.Raw:
    """Aplica referência average.

    Args:
        raw: Objeto Raw.
        reference: Tipo de referência.

    Returns:
        Raw com referência.
    """
    if reference == "average":
        raw.set_eeg_reference("average", projection=False)
    return raw


# ============================================================
# 7. Epochar
# ============================================================
def create_epochs(
    raw: mne.io.Raw,
    event_id: dict[str, int] | None = None,
    tmin: float = -0.2,
    tmax: float = 1.0,
    baseline: tuple[float, float] = (-0.2, 0.0),
    reject: dict | None = None,
) -> mne.Epochs:
    """Cria epochs em torno de eventos.

    Args:
        raw: Objeto Raw.
        event_id: Dict de condição -> ID.
        tmin: Início do epoch.
        tmax: Fim do epoch.
        baseline: Baseline em segundos.
        reject: Critérios de rejeição.

    Returns:
        Epochs.
    """
    if reject is None:
        reject = {"eeg": 100e-6}

    events = mne.find_events(raw, stim_channel="STI 014", verbose="ERROR")
    logger.info(f"Eventos encontrados: {len(events)}")

    if event_id is None:
        event_id = {
            "palavra_papel": 1,
            "pseudopalavra_papel": 2,
            "palavra_tela": 3,
            "pseudopalavra_tela": 4,
        }

    epochs = mne.Epochs(
        raw,
        events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        baseline=baseline,
        preload=True,
        reject=reject,
    )
    logger.info(f"Epochs criados: {len(epochs)} trials")
    return epochs


# ============================================================
# 8. Salvar
# ============================================================
def save_processed(
    raw_clean: mne.io.Raw,
    ica: mne.preprocessing.ICA,
    epochs: mne.Epochs,
    output_dir: str | Path,
    subject_id: str,
) -> None:
    """Salva dados processados e relatório.

    Args:
        raw_clean: Raw processado.
        ica: Objeto ICA.
        epochs: Epochs criados.
        output_dir: Diretório de saída.
        subject_id: ID do sujeito.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_clean.save(output_dir / f"{subject_id}_raw.fif", overwrite=True)
    ica.save(output_dir / f"{subject_id}_ica.fif")
    epochs.save(output_dir / f"{subject_id}_epo.fif", overwrite=True)

    # Relatório
    report = _make_preprocessing_report(raw_clean, ica, epochs, subject_id)
    (output_dir / f"{subject_id}_preprocessing_report.txt").write_text(report)
    logger.info(f"✅ Sujeito {subject_id} salvo em {output_dir}")


def _make_preprocessing_report(
    raw: mne.io.Raw,
    ica: mne.preprocessing.ICA,
    epochs: mne.Epochs,
    subject_id: str,
) -> str:
    """Gera relatório textual do pré-processamento."""
    return f"""=== RELATÓRIO DE PRÉ-PROCESSAMENTO ===
Sujeito: {subject_id}
MNE versão: {mne.__version__}

=== Configuração ===
Filtro: {DEFAULT_L_FREQ}-{DEFAULT_H_FREQ} Hz + notch {DEFAULT_NOTCH_FREQ} Hz
Referência: average
Baseline: -0.2 a 0.0 s

=== Canais ===
Total: {len(raw.ch_names)}
Ruins: {raw.info['bads']}

=== ICA ===
Componentes: {ica.n_components_}
Excluídos: {len(ica.exclude)}

=== Epochs ===
Trials totais: {len(epochs.events)}
Trials aceitos: {len(epochs)}
Rejeitados: {len(epochs.events) - len(epochs)}
"""


# ============================================================
# Pipeline principal
# ============================================================
def preprocess_subject(
    input_path: str | Path,
    output_root: str | Path,
    projeto: str = "P03",
    n_components_ica: int = 20,
) -> None:
    """Pipeline completo de pré-processamento para um sujeito.

    Args:
        input_path: Caminho do arquivo bruto.
        output_root: Diretório raiz de saída.
        projeto: ID do projeto (P03, P05).
        n_components_ica: Número de componentes ICA.
    """
    input_path = Path(input_path)
    output_root = Path(output_root)
    subject_id = input_path.stem.split("_")[0]
    output_dir = output_root / "processed" / projeto / subject_id

    logger.info(f"{'='*60}")
    logger.info(f"Processando: {subject_id}")
    logger.info(f"{'='*60}")

    raw = load_raw(input_path)
    raw = setup_montage(raw)
    raw = filter_raw(raw)

    bads = detect_bad_channels(raw)
    if bads:
        raw.info["bads"] = bads
        logger.info(f"Canais ruins: {bads}")

    raw_clean, ica = run_ica(raw, n_components=n_components_ica)
    raw_clean = set_reference(raw_clean)
    epochs = create_epochs(raw_clean)
    save_processed(raw_clean, ica, epochs, output_dir, subject_id)

    logger.info(f"✅ {subject_id} concluído")
