# ============================================================
# rules/p03_eeg.smk
# Regras para EEG/ERP do P03
# ============================================================

# Etapa 1: Pré-processamento
rule p03_eeg_preprocessing:
    """Pré-processamento de EEG do P03 (batch)."""
    input:
        raw_dir = "dados/raw/P03"
    output:
        epochs = expand(
            "dados/processed/P03/subj{i:02d}/subj{i:02d}_epo.fif",
            i=range(1, config.get("p03_n_subjects", 30) + 1)
        )
    log:
        "logs/p03_preprocessing.log"
    threads: config.get("threads", 4)
    resources:
        mem_mb = 8000
    params:
        projeto = "P03"
    script:
        "../Python/01_eeg_preprocessing.py"

# Etapa 2: Análise de ERPs
rule p03_erp_analysis:
    """Análise de ERPs do P03."""
    input:
        epochs = rules.p03_eeg_preprocessing.output.epochs
    output:
        relatorio = "resultados/P03/relatorio.txt",
        metrics = "resultados/P03/00_metricas_componentes.csv",
        plot_n170 = "resultados/P03/02_erp_N170.png",
        plot_topo_n170 = "resultados/P03/03_topografia_N170.png"
    log:
        "logs/p03_erp.log"
    threads: config.get("threads", 4)
    resources:
        mem_mb = 8000
    params:
        projeto = "P03"
    script:
        "../Python/02_eeg_erp_analysis.py"

# Regra combinada: P03 completo
rule p03_full:
    """Pipeline completo do P03 (preprocess + ERP)."""
    input:
        rules.p03_eeg_preprocessing.output.epochs,
        rules.p03_erp_analysis.output.relatorio
