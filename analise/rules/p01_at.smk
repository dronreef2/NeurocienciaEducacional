# ============================================================
# rules/p01_at.smk
# Regras para Análise Temática do P01
# ============================================================

# Regra P01: Análise Temática
rule p01_at_pipeline:
    """Pipeline de Análise Temática (P01)."""
    input:
        transcricoes = expand("dados/raw/P01/{participante}.txt",
                              participante=config.get("p01_participantes", []))
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
        "../R/01_at_pipeline.R"

# Regra P01: Relatório R Markdown
rule p01_at_report:
    """Gera relatório HTML do P01 via R Markdown."""
    input:
        relatorio = "resultados/P01/relatorio.txt"
    output:
        html = "resultados/P01/report.html"
    log:
        "logs/p01_at_report.log"
    params:
        rmd = "../R/notebooks/01_at_exploratory.Rmd"
    shell:
        """
        R -e "rmarkdown::render('{params.rmd}', output_file='{output.html}')" \
            2>&1 | tee {log}
        """
