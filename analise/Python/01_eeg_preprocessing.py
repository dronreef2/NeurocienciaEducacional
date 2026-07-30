"""
01_eeg_preprocessing.py
Pipeline de pré-processamento de EEG para os projetos P03 e P05.

Baseado em:
- Luck (2014). An Introduction to the Event-Related Potential Technique.
- Cohen (2014). Analyzing Neural Time Series Data.
- Mike Cohen tutorials (mikexcohen.com)

Pré-processamento:
1. Carregar dados brutos
2. Configurar montage e referência
3. Filtrar (passa-banda + notch)
4. Remover canais ruins
5. ICA para remoção de artefatos
6. Re-referenciar
7. Epochar (segmentar em torno de eventos)
8. Rejeitar trials ruins
9. Salvar dados processados

Uso:
    python 01_eeg_preprocessing.py --input dados/raw/P03/subj01.vhdr
    python 01_eeg_preprocessing.py --input dados/raw/P03/ --batch
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import logging

# Adicionar path para importar setup
sys.path.insert(0, str(Path(__file__).resolve().parent))
from setup import (
    PATHS, LOG, EEG_CONFIG, ERP_COMPONENTS, check_dependencies, install_dependencies
)


# ============================================================
# Verificar dependências antes de prosseguir
# ============================================================
def ensure_dependencies() -> None:
    """Garante que MNE e outras deps estão instaladas."""
    try:
        import mne
        import numpy
        import pandas
        import scipy
        import matplotlib
    except ImportError as e:
        LOG.error(f"Dependência faltando: {e.name}")
        LOG.info("Instalando dependências...")
        install_dependencies()
        # Tentar novamente
        global mne, np, pd
        import mne
        import numpy as np
        import pandas as pd


# Imports após verificação
ensure_dependencies()
import mne
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt


# ============================================================
# 1. Carregar dados
# ============================================================
def load_eeg(input_path: Path) -> "mne.io.Raw":
    """Carrega arquivo de EEG.

    Suporta: BrainVision (.vhdr/.eeg/.vmrk), EDF (.edf), BIDS (.bdf), FIF (.fif)

    Args:
        input_path: Caminho do arquivo

    Returns:
        Objeto mne.io.Raw com os dados
    """
    LOG.info(f"Carregando: {input_path}")

    ext = input_path.suffix.lower()

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

    LOG.info(f"  Dados: {raw.n_times} samples, {raw.info['sfreq']} Hz, "
             f"{len(raw.ch_names)} canais, {raw.times[-1]:.1f} s")
    return raw


# ============================================================
# 2. Configurar montage e referência
# ============================================================
def setup_montage(raw: "mne.io.Raw") -> "mne.io.Raw":
    """Configura montage (posições dos eletrodos).

    Args:
        raw: objeto Raw

    Returns:
        Raw com montage setada
    """
    LOG.info("Configurando montage...")

    try:
        # Tentar montage padrão baseado no nome dos canais
        montage = mne.channels.make_standard_montage(EEG_CONFIG["montage"])
        raw.set_montage(montage, on_missing="warn")
        LOG.info(f"  Montage {EEG_CONFIG['montage']} setada com sucesso")
    except Exception as e:
        LOG.warning(f"  Erro ao setar montage: {e}")
        LOG.warning("  Continuando sem montage (análise ainda possível)")

    return raw


# ============================================================
# 3. Filtrar
# ============================================================
def filter_data(raw: "mne.io.Raw") -> "mne.io.Raw":
    """Aplica filtros passa-banda e notch.

    Args:
        raw: objeto Raw

    Returns:
        Raw filtrado
    """
    LOG.info(f"Filtrando: {EEG_CONFIG['l_freq']}-{EEG_CONFIG['h_freq']} Hz + "
             f"notch {EEG_CONFIG['notch_freq']} Hz")

    raw.filter(
        l_freq=EEG_CONFIG["l_freq"],
        h_freq=EEG_CONFIG["h_freq"],
        method="fir",
        phase="zero",
        fir_design="firwin",
    )

    raw.notch_filter(
        freqs=[EEG_CONFIG["notch_freq"]],
        method="spectrum_fit",
    )

    return raw


# ============================================================
# 4. Remover canais ruins
# ============================================================
def remove_bad_channels(raw: "mne.io.Raw", threshold: float = 0.4) -> "mne.io.Raw":
    """Identifica e remove canais ruins (>40% artefatos).

    Args:
        raw: objeto Raw
        threshold: Limite de flatness/std (canais piores que isso são removidos)

    Returns:
        Raw com canais ruins removidos
    """
    LOG.info("Identificando canais ruins...")

    # Detectar canais ruins por flatness
    bad_channels_by_flat = []
    for ch in raw.ch_names:
        ch_data = raw.get_data(picks=[ch])[0]
        # Flatness baixa = muita repetição = ruim
        from scipy.stats import kurtosis
        kurt = kurtosis(ch_data)
        if kurt < threshold:
            bad_channels_by_flat.append(ch)

    if bad_channels_by_flat:
        raw.info["bads"] = bad_channels_by_flat
        LOG.info(f"  {len(bad_channels_by_flat)} canais marcados como ruins: {bad_channels_by_flat[:5]}"
                 f"{'...' if len(bad_channels_by_flat) > 5 else ''}")
    else:
        LOG.info("  Nenhum canal ruim identificado")

    return raw


# ============================================================
# 5. ICA
# ============================================================
def run_ica(raw: "mne.io.Raw", n_components: int = 20) -> Tuple["mne.io.Raw", "mne.preprocessing.ICA"]:
    """Aplica ICA para remoção de artefatos (olhos, músculo).

    Args:
        raw: objeto Raw (filtrado)
        n_components: número de componentes ICA

    Returns:
        Raw limpo, objeto ICA
    """
    LOG.info(f"Aplicando ICA com {n_components} componentes...")

    ica = mne.preprocessing.ICA(
        n_components=n_components,
        method="fastica",
        max_iter="auto",
        random_state=42,  # reprodutibilidade
    )

    # Ajustar ICA nos dados filtrados
    ica.fit(raw)

    # Detectar componentes de olho automaticamente
    eog_indices, eog_scores = ica.find_bads_eog(raw, threshold=0.5)
    LOG.info(f"  Componentes EOG detectados: {eog_indices[:5]}"
             f"{'...' if len(eog_indices) > 5 else ''}")

    # Detectar componentes de músculo
    muscle_indices, muscle_scores = ica.find_bads_muscle(raw, threshold=0.5)
    LOG.info(f"  Componentes muscle detectados: {muscle_indices[:5]}"
             f"{'...' if len(muscle_indices) > 5 else ''}")

    # Excluir
    ica.exclude = list(set(eog_indices + muscle_indices))
    LOG.info(f"  Excluindo {len(ica.exclude)} componentes")

    # Aplicar
    raw_clean = ica.apply(raw)

    return raw_clean, ica


# ============================================================
# 6. Re-referenciar
# ============================================================
def set_reference(raw: "mne.io.Raw") -> "mne.io.Raw":
    """Aplica referência average (ou outra, configurada em EEG_CONFIG).

    Args:
        raw: objeto Raw

    Returns:
        Raw com referência aplicada
    """
    LOG.info(f"Aplicando referência: {EEG_CONFIG['reference']}")

    if EEG_CONFIG["reference"] == "average":
        raw.set_eeg_reference("average", projection=False)
    else:
        LOG.warning(f"Referência {EEG_CONFIG['reference']} não implementada, usando average")
        raw.set_eeg_reference("average", projection=False)

    return raw


# ============================================================
# 7. Epochar
# ============================================================
def create_epochs(
    raw: "mne.io.Raw",
    event_id: Optional[dict] = None,
    tmin: Optional[float] = None,
    tmax: Optional[float] = None,
) -> "mne.Epochs":
    """Cria epochs em torno de eventos.

    Args:
        raw: objeto Raw
        event_id: dict mapeando nome do evento para ID
        tmin: início do epoch (relativo ao evento)
        tmax: fim do epoch

    Returns:
        Epochs
    """
    LOG.info("Criando epochs...")

    tmin = tmin if tmin is not None else EEG_CONFIG["tmin"]
    tmax = tmax if tmax is not None else EEG_CONFIG["tmax"]

    # Encontrar eventos
    events = mne.find_events(raw, stim_channel="STI 014", verbose="ERROR")
    LOG.info(f"  Eventos encontrados: {len(events)}")
    LOG.info(f"  Tipos únicos: {np.unique(events[:, 2])}")

    # Default event_id para leitura (P03)
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
        baseline=EEG_CONFIG["baseline"],
        preload=True,
        reject=EEG_CONFIG["reject"],
    )

    LOG.info(f"  Epochs criados: {len(epochs)} trials")
    LOG.info(f"  Trials rejeitados: {epochs.drop_log_stats()}")

    return epochs


# ============================================================
# 8. Salvar resultados
# ============================================================
def save_processed(
    raw_clean: "mne.io.Raw",
    ica: "mne.preprocessing.ICA",
    epochs: "mne.Epochs",
    output_dir: Path,
    subject_id: str,
) -> None:
    """Salva dados processados.

    Args:
        raw_clean: Raw processado
        ica: objeto ICA
        epochs: Epochs criados
        output_dir: diretório de saída
        subject_id: ID do sujeito
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    LOG.info(f"Salvando em: {output_dir}")

    # Salvar raw limpo
    raw_clean.save(
        output_dir / f"{subject_id}_raw.fif",
        overwrite=True
    )
    LOG.info(f"  ✅ Raw salvo")

    # Salvar ICA
    ica.save(output_dir / f"{subject_id}_ica.fif")
    LOG.info(f"  ✅ ICA salvo")

    # Salvar epochs
    epochs.save(
        output_dir / f"{subject_id}_epo.fif",
        overwrite=True
    )
    LOG.info(f"  ✅ Epochs salvos")

    # Salvar relatório de pré-processamento
    report = f"""=== RELATÓRIO DE PRÉ-PROCESSAMENTO ===
Sujeito: {subject_id}
Data: {pd.Timestamp.now()}
Versão MNE: {mne.__version__}

=== Configuração ===
Frequência de amostragem: {EEG_CONFIG['sfreq']} Hz
Filtro: {EEG_CONFIG['l_freq']}-{EEG_CONFIG['h_freq']} Hz + notch {EEG_CONFIG['notch_freq']} Hz
Referência: {EEG_CONFIG['reference']}
Baseline: {EEG_CONFIG['baseline']}
Rejeição: amplitude > 100 µV

=== Canais ===
Total: {len(raw_clean.ch_names)}
Ruins (excluídos): {raw_clean.info['bads']}

=== ICA ===
Componentes totais: {ica.n_components_}
Componentes EOG: {len([i for i in ica.exclude if i in ica.find_bads_eog(raw_clean)[0]])}
Componentes muscle: {len([i for i in ica.exclude if i in ica.find_bads_muscle(raw_clean)[0]])}

=== Epochs ===
Trials totais: {len(epochs.events)}
Trials aceitos: {len(epochs)}
Trials rejeitados: {len(epochs.events) - len(epochs)}
"""

    with open(output_dir / f"{subject_id}_preprocessing_report.txt", "w") as f:
        f.write(report)
    LOG.info(f"  ✅ Relatório salvo")


# ============================================================
# Pipeline principal
# ============================================================
def process_subject(input_path: Path, output_root: Path, projeto: str) -> None:
    """Pipeline completo para um sujeito.

    Args:
        input_path: caminho do arquivo bruto
        output_root: diretório raiz de saída
        projeto: identificador do projeto (P03, P05, etc.)
    """
    subject_id = input_path.stem.split("_")[0]  # ex: "subj01"
    output_dir = output_root / "processed" / projeto / subject_id

    LOG.info(f"\n{'='*60}")
    LOG.info(f"Processando sujeito: {subject_id}")
    LOG.info(f"{'='*60}")

    # 1. Carregar
    raw = load_eeg(input_path)

    # 2. Montage
    raw = setup_montage(raw)

    # 3. Filtrar
    raw = filter_data(raw)

    # 4. Remover canais ruins
    raw = remove_bad_channels(raw)

    # 5. ICA
    raw_clean, ica = run_ica(raw)

    # 6. Re-referenciar
    raw_clean = set_reference(raw_clean)

    # 7. Epochar
    epochs = create_epochs(raw_clean)

    # 8. Salvar
    save_processed(raw_clean, ica, epochs, output_dir, subject_id)

    LOG.info(f"✅ Sujeito {subject_id} processado com sucesso\n")


def main() -> None:
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Pipeline de pré-processamento de EEG"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Arquivo de entrada (.vhdr, .edf, .bdf) ou diretório (com --batch)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PATHS["dados_processados"],
        help="Diretório de saída",
    )
    parser.add_argument(
        "--projeto",
        type=str,
        default="P03",
        choices=["P03", "P05"],
        help="Projeto (P03 = EEG leitura, P05 = coorte)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Processar todos os arquivos do diretório de entrada",
    )

    args = parser.parse_args()

    # Se for batch, processar todos os arquivos
    if args.batch or args.input.is_dir():
        if not args.input.is_dir():
            LOG.error(f"Para --batch, --input deve ser diretório: {args.input}")
            sys.exit(1)

        # Encontrar arquivos .vhdr
        arquivos = list(args.input.glob("*.vhdr")) + \
                   list(args.input.glob("*.edf")) + \
                   list(args.input.glob("*.bdf"))

        if not arquivos:
            LOG.error(f"Nenhum arquivo de EEG encontrado em {args.input}")
            sys.exit(1)

        LOG.info(f"Encontrados {len(arquivos)} arquivos para processar")

        for arquivo in arquivos:
            try:
                process_subject(arquivo, args.output, args.projeto)
            except Exception as e:
                LOG.error(f"Erro processando {arquivo}: {e}")
                continue

        LOG.info(f"\n{'='*60}")
        LOG.info(f"Pipeline concluído: {len(arquivos)} sujeitos processados")
        LOG.info(f"{'='*60}")
    else:
        # Processar um único arquivo
        process_subject(args.input, args.output, args.projeto)


if __name__ == "__main__":
    main()
