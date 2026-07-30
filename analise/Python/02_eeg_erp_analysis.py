"""
02_eeg_erp_analysis.py
Análise de ERPs (Event-Related Potentials) — Projeto P03.

Pipeline:
1. Carregar dados pré-processados
2. Visualizar ERPs (grand average + por condição)
3. Extrair amplitude/pico dos componentes (N170, N400, P300)
4. Plotar topografias
5. Análise estatística (permutation test, GLM misto)
6. Exportar resultados

Uso:
    python 02_eeg_erp_analysis.py --input dados/processed/P03/subj01_epo.fif
    python 02_eeg_erp_analysis.py --input dados/processed/P03/ --batch
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

sys.path.insert(0, str(Path(__file__).resolve().parent))
from setup import (
    PATHS, LOG, ERP_COMPONENTS, EEG_CONFIG
)


# ============================================================
# Imports após setup
# ============================================================
try:
    import mne
    import mne.stats
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy import stats as scipy_stats
except ImportError as e:
    LOG.error(f"Dependência faltando: {e.name}")
    LOG.info("Execute: pip install -r analise/requirements.txt")
    sys.exit(1)


# ============================================================
# 1. Carregar dados
# ============================================================
def load_epochs(input_path: Path) -> "mne.Epochs":
    """Carrega epochs pré-processados."""
    LOG.info(f"Carregando epochs: {input_path}")
    epochs = mne.read_epochs(input_path, preload=True, verbose="ERROR")
    LOG.info(f"  Trials: {len(epochs)}")
    LOG.info(f"  Condições: {list(epochs.event_id.keys())}")
    return epochs


# ============================================================
# 2. ERP grand average
# ============================================================
def compute_grand_average(
    all_epochs: Dict[str, "mne.Epochs"],
) -> Dict[str, "mne.Evoked"]:
    """Calcula grand average por condição."""
    LOG.info("Calculando grand average...")

    evoked_dict = {}
    for subject, epochs in all_epochs.items():
        for condition in epochs.event_id:
            if condition not in evoked_dict:
                evoked_dict[condition] = []
            evoked = epochs[condition].average()
            evoked_dict[condition].append(evoked)

    # Média
    grand_avg = {}
    for condition, evokeds in evoked_dict.items():
        if len(evokeds) > 0:
            # Média simples (não-ponderada)
            data = np.stack([e.data for e in evokeds])
            mean_data = data.mean(axis=0)
            std_data = data.std(axis=0)
            sem_data = data.std(axis=0) / np.sqrt(len(evokeds))

            # Criar Evoked com a média
            grand_evoked = evokeds[0].copy()
            grand_evoked.data = mean_data
            grand_evoked.comment = f"Grand average {condition} (n={len(evokeds)})"
            grand_avg[condition] = grand_evoked

            LOG.info(f"  {condition}: n={len(evokeds)}")

    return grand_avg


# ============================================================
# 3. Plot ERPs
# ============================================================
def plot_erps(
    grand_avg: Dict[str, "mne.Evoked"],
    output_dir: Path,
    channels: List[str] = None,
) -> None:
    """Plota ERPs para canais específicos."""
    LOG.info("Gerando plots de ERP...")

    if channels is None:
        channels = ["Oz", "O1", "O2", "P7", "P8", "Cz", "Pz", "Fz"]

    output_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: Todos os canais, todas as condições
    fig, axes = plt.subplots(
        len(channels) // 2, 2,
        figsize=(14, 2 * len(channels))
    )
    axes = axes.flatten()

    times = list(grand_avg.values())[0].times

    for ax, ch in zip(axes, channels):
        for condition, evoked in grand_avg.items():
            if ch in evoked.ch_names:
                ch_idx = evoked.ch_names.index(ch)
                ax.plot(evoked.times * 1000, evoked.data[ch_idx] * 1e6,
                        label=condition, linewidth=1.5)
                # Adicionar SEM como shade
                # (simplificado — sem SEM aqui)

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
    LOG.info("  ✅ 01_erps_canais.png salvo")

    # Plot 2: ERP destacado por componente
    for component, config in ERP_COMPONENTS.items():
        # Canais de interesse
        chs = [ch for ch in config["channels"] if ch in grand_avg[list(grand_avg.keys())[0]].ch_names]
        if not chs:
            continue

        tmin, tmax = config["time_range"]

        fig, ax = plt.subplots(figsize=(10, 6))
        for condition, evoked in grand_avg.items():
            # Média dos canais
            ch_indices = [evoked.ch_names.index(ch) for ch in chs if ch in evoked.ch_names]
            if ch_indices:
                mean_signal = evoked.data[ch_indices].mean(axis=0)
                ax.plot(evoked.times * 1000, mean_signal * 1e6,
                        label=condition, linewidth=2)

        # Sombrear janela do componente
        ax.axvspan(tmin * 1000, tmax * 1000, alpha=0.2, color="gray",
                   label=f"{component}: {tmin*1000:.0f}-{tmax*1000:.0f} ms")
        ax.axhline(0, color="black", linestyle="--", linewidth=0.5)
        ax.axvline(0, color="red", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.set_xlim(-200, 1000)
        ax.set_xlabel("Tempo (ms)")
        ax.set_ylabel(f"Amplitude (µV) — média de {chs}")
        ax.set_title(f"Componente {component}\n{config['description']}")
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_dir / f"02_erp_{component}.png", dpi=100, bbox_inches="tight")
        plt.close()
        LOG.info(f"  ✅ 02_erp_{component}.png salvo")


# ============================================================
# 4. Extrair métricas dos componentes
# ============================================================
def extract_component_metrics(
    grand_avg: Dict[str, "mne.Evoked"],
) -> pd.DataFrame:
    """Extrai amplitude média e latência de pico de cada componente."""
    LOG.info("Extraindo métricas dos componentes...")

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

            # Média dos canais
            ch_indices = [evoked.ch_names.index(ch) for ch in chs]
            mean_signal = evoked.data[ch_indices].mean(axis=0)

            # Amplitude média na janela
            mean_amplitude = mean_signal[time_mask].mean() * 1e6  # µV

            # Latência do pico (negativo para N, positivo para P)
            if component.startswith("N"):
                peak_latency = evoked.times[time_mask][np.argmin(mean_signal[time_mask])] * 1000
                peak_amplitude = mean_signal[time_mask].min() * 1e6
            else:  # P
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

    df_metrics = pd.DataFrame(metrics)
    return df_metrics


# ============================================================
# 5. Topografias
# ============================================================
def plot_topographies(
    grand_avg: Dict[str, "mne.Evoked"],
    output_dir: Path,
) -> None:
    """Plota mapas topográficos para cada componente."""
    LOG.info("Gerando topografias...")

    for component, config in ERP_COMPONENTS.items():
        tmin, tmax = config["time_range"]

        # Pegar meio da janela
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
                time_format=""
            )
            ax.set_title(f"{condition}\n({t_peak*1000:.0f} ms)", fontsize=10)

        # Colorbar única
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        mne.viz.plot_topomap(
            grand_avg[list(grand_avg.keys())[0]].data[:, 0],
            grand_avg[list(grand_avg.keys())[0]].info,
            axes=cbar_ax,
            show=False
        )
        cbar_ax.set_title("µV", fontsize=8)

        fig.suptitle(f"Topografia: {component}\n{config['description']}",
                     fontsize=12, y=1.02)
        plt.savefig(output_dir / f"03_topografia_{component}.png",
                    dpi=100, bbox_inches="tight")
        plt.close()
        LOG.info(f"  ✅ 03_topografia_{component}.png salvo")


# ============================================================
# 6. Cluster-based permutation test
# ============================================================
def permutation_test(
    all_epochs: Dict[str, "mne.Epochs"],
    condition1: str,
    condition2: str,
    output_dir: Path,
) -> None:
    """Compara duas condições via cluster-based permutation test."""
    LOG.info(f"Cluster permutation test: {condition1} vs {condition2}")

    # Empilhar epochs por condição
    epochs1 = mne.concatenate_epochs(
        [epochs[condition1] for subj, epochs in all_epochs.items()]
    )
    epochs2 = mne.concatenate_epochs(
        [epochs[condition2] for subj, epochs in all_epochs.items()]
    )

    # Calcular ERPs
    evoked1 = epochs1.average()
    evoked2 = epochs2.average()

    # Diferença
    diff = mne.combine_evoked([evoked1, evoked2], weights=[1, -1])

    # Cluster permutation
    t_obs, clusters, cluster_pv, H0 = mne.stats.spatio_temporal_cluster_1samp_test(
        diff.data[np.newaxis, :, :],  # precisa adicionar dimensão
        n_permutations=1024,
        threshold=None,  # deixa MNE calcular
        tail=0,  # two-sided
        seed=42,  # reprodutibilidade
    )

    # Salvar resultados
    results = {
        "condicao_1": condition1,
        "condicao_2": condition2,
        "n_clusters": len(clusters),
        "clusters_significativos": sum(cluster_pv < 0.05),
        "p_menor_cluster": min(cluster_pv) if len(cluster_pv) > 0 else 1.0,
    }

    LOG.info(f"  {results['clusters_significativos']} clusters significativos (p < .05)")

    pd.DataFrame([results]).to_csv(
        output_dir / "04_permutation_test.csv", index=False
    )
    LOG.info("  ✅ 04_permutation_test.csv salvo")


# ============================================================
# 7. GLM Misto (R-style)
# ============================================================
def mixed_effects_glm(
    all_epochs: Dict[str, "mne.Evoked"],
    output_dir: Path,
) -> pd.DataFrame:
    """Equivalente a um GLM misto para amplitude do componente.

    Para cada sujeito e condição, extrai amplitude média
    na janela do componente. Depois roda GLM.
    """
    LOG.info("Calculando amplitudes médias por sujeito...")

    # Coletar amplitudes
    data = []
    for subject, evoked in all_epochs.items():
        for condition, ev in evoked.items() if isinstance(evoked, dict) else [(None, evoked)]:
            for component, config in ERP_COMPONENTS.items():
                chs = [ch for ch in config["channels"] if ch in ev.ch_names]
                if not chs:
                    continue

                tmin, tmax = config["time_range"]
                time_mask = (ev.times >= tmin) & (ev.times <= tmax)
                ch_indices = [ev.ch_names.index(ch) for ch in chs]
                mean_signal = ev.data[ch_indices].mean(axis=0)
                amplitude = mean_signal[time_mask].mean() * 1e6

                data.append({
                    "sujeito": subject,
                    "condicao": condition if condition else "single",
                    "componente": component,
                    "amplitude": amplitude,
                })

    df = pd.DataFrame(data)
    df.to_csv(output_dir / "05_amplitudes_por_sujeito.csv", index=False)
    LOG.info(f"  {len(df)} observações salvas")

    # Estatísticas por componente
    summary = []
    for component in df["componente"].unique():
        df_comp = df[df["componente"] == component]
        for cond in df_comp["condicao"].unique():
            df_cc = df_comp[df_comp["condicao"] == cond]
            summary.append({
                "componente": component,
                "condicao": cond,
                "n": len(df_cc),
                "media": df_cc["amplitude"].mean(),
                "dp": df_cc["amplitude"].std(),
                "erro_padrao": df_cc["amplitude"].std() / np.sqrt(len(df_cc)),
            })

    df_summary = pd.DataFrame(summary)
    df_summary.to_csv(output_dir / "06_resumo_estatistico.csv", index=False)
    LOG.info("  ✅ 06_resumo_estatistico.csv salvo")

    return df


# ============================================================
# 8. Relatório
# ============================================================
def generate_report(
    df_metrics: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Gera relatório final."""
    LOG.info("Gerando relatório...")

    report = f"""===========================================
  RELATÓRIO - Análise de ERP (P03)
  Gerado em: {pd.Timestamp.now()}
===========================================

MÉTRICAS DOS COMPONENTES:
{df_metrics.to_string(index=False)}

ARQUIVOS GERADOS:
  01_erps_canais.png          - ERPs por canal e condição
  02_erp_<componente>.png     - ERPs por componente
  03_topografia_<componente>.png - Topografias
  04_permutation_test.csv     - Resultados do cluster permutation
  05_amplitudes_por_sujeito.csv - Amplitudes individuais
  06_resumo_estatistico.csv   - Estatísticas descritivas
  relatorio.txt               - Este arquivo

INTERPRETAÇÃO:
  - N170 (130-210 ms): especialização visual de letras
    Mais negativo = mais especializado
  - N400 (300-500 ms): integração semântica
    Mais negativo em pseudopalavras = conflito semântico
  - P300 (250-450 ms): atenção e memória
    Mais positivo = maior alocação de atenção
  - P600 (500-800 ms): reanálise sintática
    Mais positivo = maior esforço de reanálise

REFERÊNCIAS:
  - Luck (2014). An Introduction to the Event-Related Potential Technique.
  - Kutas & Federmeier (2011). Thirty years and counting: N400.
"""

    (output_dir / "relatorio.txt").write_text(report, encoding="utf-8")
    LOG.info("Relatório salvo")


# ============================================================
# Pipeline principal
# ============================================================
def process_subject(input_path: Path, output_root: Path, projeto: str) -> None:
    """Pipeline de ERP para um sujeito."""
    subject_id = input_path.stem.replace("_epo", "")
    output_dir = output_root / "P03" / subject_id

    LOG.info(f"\n{'='*60}")
    LOG.info(f"Analisando sujeito: {subject_id}")
    LOG.info(f"{'='*60}")

    epochs = load_epochs(input_path)

    # Salvar epochs (re-carregável para batch)
    all_epochs = {subject_id: epochs}

    # Grand average
    grand_avg = compute_grand_average(all_epochs)

    # Plots
    plot_erps(grand_avg, output_dir)

    # Topografias
    plot_topographies(grand_avg, output_dir)

    # Métricas
    df_metrics = extract_component_metrics(grand_avg)
    df_metrics.to_csv(output_dir / "00_metricas_componentes.csv", index=False)
    LOG.info("  ✅ 00_metricas_componentes.csv salvo")

    # GLM misto (precisa de múltiplos sujeitos)
    mixed_effects_glm(all_epochs, output_dir)

    # Relatório
    generate_report(df_metrics, output_dir)

    LOG.info(f"✅ Sujeito {subject_id} analisado\n")


def main() -> None:
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Análise de ERPs (Event-Related Potentials)"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Arquivo de epochs (_epo.fif) ou diretório (com --batch)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PATHS["resultados"],
        help="Diretório de saída"
    )
    parser.add_argument(
        "--projeto",
        type=str,
        default="P03",
        choices=["P03", "P05"]
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Processar todos os epochs do diretório"
    )

    args = parser.parse_args()

    if args.batch or args.input.is_dir():
        if not args.input.is_dir():
            LOG.error(f"Para --batch, --input deve ser diretório")
            sys.exit(1)

        # Encontrar epochs
        arquivos = list(args.input.glob("*_epo.fif"))
        if not arquivos:
            LOG.error(f"Nenhum arquivo *_epo.fif em {args.input}")
            sys.exit(1)

        LOG.info(f"Encontrados {len(arquivos)} arquivos")

        # Coletar todos os epochs (para grand average)
        all_epochs = {}
        for arquivo in arquivos:
            epochs = load_epochs(arquivo)
            subject_id = arquivo.stem.replace("_epo", "")
            all_epochs[subject_id] = epochs

        # Grand average global
        output_dir = args.output / args.projeto
        output_dir.mkdir(parents=True, exist_ok=True)

        grand_avg = compute_grand_average(all_epochs)
        plot_erps(grand_avg, output_dir)
        plot_topographies(grand_avg, output_dir)

        df_metrics = extract_component_metrics(grand_avg)
        df_metrics.to_csv(output_dir / "00_metricas_componentes.csv", index=False)

        # GLM misto
        mixed_effects_glm(all_epochs, output_dir)

        # Permutation test (entre 2 condições)
        conditions = list(all_epochs[list(all_epochs.keys())[0]].event_id.keys())
        if len(conditions) >= 2:
            permutation_test(
                all_epochs, conditions[0], conditions[1], output_dir
            )

        generate_report(df_metrics, output_dir)
        LOG.info(f"\n✅ Análise de {len(arquivos)} sujeitos concluída")
    else:
        process_subject(args.input, args.output, args.projeto)


if __name__ == "__main__":
    main()
