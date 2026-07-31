"""
neurociencia_edu.eeg.erp
Módulo refatorado de análise de ERPs.
"""

from __future__ import annotations

import logging
from pathlib import Path

import mne
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

from neurociencia_edu import ERP_WINDOWS, ERP_CHANNELS

logger = logging.getLogger(__name__)


# Componentes ERP
ERP_COMPONENTS = {
    name: {
        "time_range": ERP_WINDOWS[name],
        "channels": ERP_CHANNELS[name],
        "description": _get_erp_description(name),
    }
    for name in ERP_WINDOWS
}


def _get_erp_description(name: str) -> str:
    """Retorna descrição do componente ERP."""
    descriptions = {
        "N170": "Especialização visual de letras/palavras",
        "N400": "Integração semântica",
        "P300": "Atenção e memória de trabalho",
        "P600": "Reanálise sintática/semântica",
    }
    return descriptions.get(name, "")


# ============================================================
# Carregar
# ============================================================
def load_epochs(input_path: str | Path) -> mne.Epochs:
    """Carrega epochs pré-processados.

    Args:
        input_path: Caminho do arquivo *_epo.fif.

    Returns:
        Epochs.
    """
    logger.info(f"Carregando: {input_path}")
    epochs = mne.read_epochs(input_path, preload=True, verbose="ERROR")
    logger.info(f"  Trials: {len(epochs)}")
    logger.info(f"  Condições: {list(epochs.event_id.keys())}")
    return epochs


# ============================================================
# Grand average
# ============================================================
def compute_grand_average(
    all_epochs: dict[str, mne.Epochs],
) -> dict[str, mne.Evoked]:
    """Calcula grand average por condição.

    Args:
        all_epochs: Dict subject_id -> Epochs.

    Returns:
        Dict condition -> Evoked (grand average).
    """
    logger.info("Calculando grand average...")
    evoked_dict: dict[str, list[mne.Evoked]] = {}

    for subject, epochs in all_epochs.items():
        for condition in epochs.event_id:
            evoked_dict.setdefault(condition, []).append(epochs[condition].average())

    grand_avg = {}
    for condition, evokeds in evoked_dict.items():
        if not evokeds:
            continue
        data = np.stack([e.data for e in evokeds])
        grand_evoked = evokeds[0].copy()
        grand_evoked.data = data.mean(axis=0)
        grand_evoked.comment = f"Grand average {condition} (n={len(evokeds)})"
        grand_avg[condition] = grand_evoked
        logger.info(f"  {condition}: n={len(evokeds)}")

    return grand_avg


# ============================================================
# Plot ERPs
# ============================================================
def plot_erps(
    grand_avg: dict[str, mne.Evoked],
    output_dir: str | Path,
    channels: list[str] | None = None,
) -> None:
    """Plota ERPs por canal e condição.

    Args:
        grand_avg: Dict condition -> Evoked.
        output_dir: Diretório de saída.
        channels: Lista de canais a plotar.
    """
    if channels is None:
        channels = ["Oz", "O1", "O2", "P7", "P8", "Cz", "Pz", "Fz"]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(len(channels) // 2, 2, figsize=(14, 2 * len(channels)))
    axes = axes.flatten()
    times = list(grand_avg.values())[0].times

    for ax, ch in zip(axes, channels):
        for condition, evoked in grand_avg.items():
            if ch in evoked.ch_names:
                ch_idx = evoked.ch_names.index(ch)
                ax.plot(evoked.times * 1000, evoked.data[ch_idx] * 1e6,
                        label=condition, linewidth=1.5)
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        ax.axvline(0, color="red", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.set_xlim(-200, 1000)
        ax.set_xlabel("Tempo (ms)")
        ax.set_ylabel("Amplitude (µV)")
        ax.set_title(ch)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "01_erps_canais.png", dpi=100, bbox_inches="tight")
    plt.close()


# ============================================================
# Métricas dos componentes
# ============================================================
def extract_component_metrics(
    grand_avg: dict[str, mne.Evoked],
) -> pd.DataFrame:
    """Extrai amplitude média e latência de pico de cada componente.

    Args:
        grand_avg: Dict condition -> Evoked.

    Returns:
        DataFrame com colunas: condicao, componente, canais, amplitude_media,
        amplitude_pico, latencia_pico_ms, janela_ms.
    """
    metrics = []

    for condition, evoked in grand_avg.items():
        for component, config in ERP_COMPONENTS.items():
            chs = [ch for ch in config["channels"] if ch in evoked.ch_names]
            if not chs:
                continue

            tmin, tmax = config["time_range"]
            time_mask = (evoked.times >= tmin) & (evoked.times <= tmax)
            if not time_mask.any():
                continue

            ch_indices = [evoked.ch_names.index(ch) for ch in chs]
            mean_signal = evoked.data[ch_indices].mean(axis=0)
            mean_amplitude = mean_signal[time_mask].mean() * 1e6

            if component.startswith("N"):
                peak_latency = evoked.times[time_mask][np.argmin(mean_signal[time_mask])] * 1000
                peak_amplitude = mean_signal[time_mask].min() * 1e6
            else:
                peak_latency = evoked.times[time_mask][np.argmax(mean_signal[time_mask])] * 1000
                peak_amplitude = mean_signal[time_mask].max() * 1e6

            metrics.append({
                "condicao": condition,
                "componente": component,
                "canais": ", ".join(chs),
                "amplitude_media": mean_amplitude,
                "amplitude_pico": peak_amplitude,
                "latencia_pico_ms": peak_latency,
                "janela_ms": f"{tmin*1000:.0f}-{tmax*1000:.0f}",
            })

    return pd.DataFrame(metrics)


# ============================================================
# Topografias
# ============================================================
def plot_topographies(
    grand_avg: dict[str, mne.Evoked],
    output_dir: str | Path,
) -> None:
    """Plota mapas topográficos para cada componente."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for component, config in ERP_COMPONENTS.items():
        tmin, tmax = config["time_range"]
        t_peak = (tmin + tmax) / 2

        n_conditions = len(grand_avg)
        fig, axes = plt.subplots(1, n_conditions, figsize=(4 * n_conditions, 4))
        if n_conditions == 1:
            axes = [axes]

        for ax, (condition, evoked) in zip(axes, grand_avg.items()):
            evoked.plot_topomap(
                times=[t_peak],
                axes=ax,
                show=False,
                colorbar=False,
                time_format="",
            )
            ax.set_title(f"{condition}\n({t_peak*1000:.0f} ms)", fontsize=10)

        fig.suptitle(f"Topografia: {component}\n{config['description']}",
                     fontsize=12, y=1.02)
        plt.savefig(output_dir / f"03_topografia_{component}.png",
                    dpi=100, bbox_inches="tight")
        plt.close()


# ============================================================
# Cluster permutation
# ============================================================
def permutation_test(
    all_epochs: dict[str, mne.Epochs],
    condition1: str,
    condition2: str,
    output_dir: str | Path,
    n_permutations: int = 1024,
) -> pd.DataFrame:
    """Compara duas condições via cluster-based permutation test.

    Args:
        all_epochs: Dict subject_id -> Epochs.
        condition1: Nome da condição 1.
        condition2: Nome da condição 2.
        output_dir: Diretório de saída.
        n_permutations: Número de permutações.

    Returns:
        DataFrame com resultados.
    """
    logger.info(f"Cluster permutation: {condition1} vs {condition2}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    epochs1 = mne.concatenate_epochs(
        [epochs[condition1] for epochs in all_epochs.values()]
    )
    epochs2 = mne.concatenate_epochs(
        [epochs[condition2] for epochs in all_epochs.values()]
    )

    evoked1 = epochs1.average()
    evoked2 = epochs2.average()
    diff = mne.combine_evoked([evoked1, evoked2], weights=[1, -1])

    t_obs, clusters, cluster_pv, _ = mne.stats.spatio_temporal_cluster_1samp_test(
        diff.data[np.newaxis, :, :],
        n_permutations=n_permutations,
        threshold=None,
        tail=0,
        seed=42,
    )

    results = pd.DataFrame([{
        "condicao_1": condition1,
        "condicao_2": condition2,
        "n_clusters": len(clusters),
        "clusters_significativos": sum(cluster_pv < 0.05),
        "p_menor_cluster": min(cluster_pv) if len(cluster_pv) > 0 else 1.0,
    }])
    results.to_csv(output_dir / "04_permutation_test.csv", index=False)
    return results
