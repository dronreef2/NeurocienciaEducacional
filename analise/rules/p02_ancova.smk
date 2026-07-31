# ============================================================
# rules/p02_ancova.smk
# Regras para ANCOVA do P02
# ============================================================

rule p02_ancova:
    """ANCOVA 2x4 do P02."""
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
        "../R/02_anova_p02.R"

rule p02_ancova_report:
    """Relatório R Markdown do P02."""
    input:
        relatorio = "resultados/P02/relatorio.txt"
    output:
        html = "resultados/P02/report.html"
    params:
        rmd = "../R/notebooks/02_ancova_report.Rmd"
    shell:
        """
        R -e "rmarkdown::render('{params.rmd}', output_file='{output.html}')" \
            2>&1 | tee logs/p02_ancova_report.log
        """
