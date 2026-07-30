# ============================================================
# Snakefile — workflow alternativo ao Makefile
#
# Snakemake é mais poderoso que Make para pipelines de análise:
# - Detecta dependências automaticamente
# - Paralelização nativa
# - Suporte a conda/envs
# - Relatórios HTML automáticos
# - Integração com clusters (SLURM, SGE)
#
# Uso:
#   snakemake --cores 4           # rodar tudo com 4 cores
#   snakemake -n                  # dry run
#   snakemake --dag | dot -Tpng > dag.png  # visualizar DAG
#   snakemake --report report.html  # relatório HTML
# ============================================================

import yaml
from pathlib import Path

# Carregar configuração
configfile: "analise/config/config.yaml"

# Incluir regras de outros Snakefiles (modular)
include: "analise/rules/preprocessing.smk" if Path("analise/rules/preprocessing.smk").exists() else None

# ============================================================
# Targets finais (outputs que o usuário quer)
# ============================================================
rule all:
    input:
        # P01 — Análise Temática
        "resultados/P01/relatorio.txt",
        "resultados/P01/05_wordcloud.png",

        # P02 — ANCOVA
        "resultados/P02/relatorio.txt",
        "resultados/P02/13_tabela_resultados.csv",

        # P03 — EEG
        "resultados/P03/relatorio.txt",
        "resultados/P03/02_erp_N170.png",
        "resultados/P03/03_topografia_N170.png",

        # P04 — SEM
        "resultados/P04/relatorio.txt",
        "resultados/P04/05_modelo_sem.png",

        # P05 — LGCM
        "resultados/P05/relatorio.txt",
        "resultados/P05/05_trajetorias_preditas.png",

        # Relatório global
        "resultados/relatorio_global.html",

# ============================================================
# Regras
# ============================================================

# --- P01: Análise Temática -----------------------------------
rule p01_at_pipeline:
    """Pipeline completo de Análise Temática do P01."""
    input:
        transcricoes = "dados/raw/P01/"
    output:
        relatorio = "resultados/P01/relatorio.txt",
        wordcloud = "resultados/P01/05_wordcloud.png",
        codebook = "resultados/P01/07_codebook_inicial.csv"
    log:
        "logs/p01_at_pipeline.log"
    threads: 1
    resources:
        mem_mb = 4000
    script:
        "analise/R/01_at_pipeline.R"

# --- P02: ANCOVA ---------------------------------------------
rule p02_ancova:
    """ANCOVA 2x4 do P02 com post-hoc e tamanho de efeito."""
    input:
        dados = "dados/processed/P02/p02_clean.csv"
    output:
        relatorio = "resultados/P02/relatorio.txt",
        tabela = "resultados/P02/13_tabela_resultados.csv",
        plot = "resultados/P02/10_emmeans_stroop.png"
    log:
        "logs/p02_ancova.log"
    threads: 1
    resources:
        mem_mb = 4000
    script:
        "analise/R/02_anova_p02.R"

# --- P03: EEG Pré-processamento ------------------------------
rule p03_eeg_preprocessing:
    """Pré-processamento de EEG do P03 (batch)."""
    input:
        raw = "dados/raw/P03/"
    output:
        epochs = expand(
            "dados/processed/P03/subj{i:02d}/subj{i:02d}_epo.fif",
            i=range(1, config["p03_n_subjects"] + 1)
        )
    log:
        "logs/p03_preprocessing.log"
    threads: config["threads"]
    resources:
        mem_mb = 8000
    script:
        "analise/Python/01_eeg_preprocessing.py"

# --- P03: ERP Analysis ---------------------------------------
rule p03_erp_analysis:
    """Análise de ERPs do P03 (grand average, topografia, permutation)."""
    input:
        epochs = "dados/processed/P03/"
    output:
        relatorio = "resultados/P03/relatorio.txt",
        metrics = "resultados/P03/00_metricas_componentes.csv",
        plot_n170 = "resultados/P03/02_erp_N170.png",
        plot_topo_n170 = "resultados/P03/03_topografia_N170.png"
    log:
        "logs/p03_erp.log"
    threads: config["threads"]
    resources:
        mem_mb = 8000
    script:
        "analise/Python/02_eeg_erp_analysis.py"

# --- P04: SEM -----------------------------------------------
rule p04_sem:
    """SEM com mediação do P04."""
    input:
        dados = "dados/processed/P04/p04_clean.csv"
    output:
        relatorio = "resultados/P04/relatorio.txt",
        plot = "resultados/P04/05_modelo_sem.png"
    log:
        "logs/p04_sem.log"
    threads: 1
    resources:
        mem_mb = 4000
    script:
        "analise/R/03_sem_p04.R"

# --- P05: LGCM ----------------------------------------------
rule p05_lgcm:
    """LGCM/LGMM do P05 (coorte longitudinal)."""
    input:
        dados = "dados/processed/P05/p05_long.csv"
    output:
        relatorio = "resultados/P05/relatorio.txt",
        trajetorias = "resultados/P05/05_trajetorias_preditas.png"
    log:
        "logs/p05_lgcm.log"
    threads: 1
    resources:
        mem_mb = 4000
    script:
        "analise/R/04_lgcm_p05.R"

# --- Relatório global ---------------------------------------
rule relatorio_global:
    """Gera relatório HTML agregando resultados de todos os projetos."""
    input:
        p01 = "resultados/P01/relatorio.txt",
        p02 = "resultados/P02/relatorio.txt",
        p03 = "resultados/P03/relatorio.txt",
        p04 = "resultados/P04/relatorio.txt",
        p05 = "resultados/P05/relatorio.txt"
    output:
        html = "resultados/relatorio_global.html"
    log:
        "logs/relatorio_global.log"
    run:
        from datetime import datetime
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório Global — Programa de Pesquisa</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1f77b4; }}
        h2 {{ color: #ff7f0e; border-bottom: 2px solid #ff7f0e; padding-bottom: 5px; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .timestamp {{ color: #7f7f7f; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>📊 Relatório Global — Programa de Pesquisa</h1>
    <p class="timestamp">Gerado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <h2>🟢 P01 — Análise Temática (Khanmigo)</h2>
    <pre>{Path(input.p01).read_text(encoding='utf-8', errors='ignore')}</pre>

    <h2>🟡 P02 — Gamificação (ANCOVA)</h2>
    <pre>{Path(input.p02).read_text(encoding='utf-8', errors='ignore')}</pre>

    <h2>🔴 P03 — EEG / ERP (Bandeira)</h2>
    <pre>{Path(input.p03).read_text(encoding='utf-8', errors='ignore')}</pre>

    <h2>🟣 P04 — IA Generativa × FE (SEM)</h2>
    <pre>{Path(input.p04).read_text(encoding='utf-8', errors='ignore')}</pre>

    <h2>🔵 P05 — Coorte Longitudinal (LGCM)</h2>
    <pre>{Path(input.p05).read_text(encoding='utf-8', errors='ignore')}</pre>

    <hr>
    <p><small>Programa de Pesquisa em Neurociência Educacional — UFRN/CERES</small></p>
</body>
</html>"""
        Path(output.html).write_text(html, encoding="utf-8")

# ============================================================
# Utilitários
# ============================================================
rule clean:
    """Limpa todos os resultados (CUIDADO: irreversível)."""
    shell:
        "rm -rf resultados/* logs/* dados/processed/*"

rule clean_results:
    """Limpa apenas resultados (mantém dados processados)."""
    shell:
        "rm -rf resultados/*"

rule status:
    """Mostra status dos arquivos."""
    shell:
        """
        echo "=== STATUS DO PROJETO ==="
        echo "Dados brutos: $(find dados/raw -type f 2>/dev/null | wc -l) arquivos"
        echo "Dados processados: $(find dados/processed -type f 2>/dev/null | wc -l) arquivos"
        echo "Resultados: $(find resultados -type f 2>/dev/null | wc -l) arquivos"
        echo ""
        echo "Tamanho total: $(du -sh dados resultados 2>/dev/null)"
        """

rule dag:
    """Gera visualização do DAG de execução."""
    shell:
        "snakemake --dag | dot -Tpng > resultados/dag.png"
