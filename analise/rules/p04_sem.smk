# ============================================================
# rules/p04_sem.smk
# Regras para SEM do P04
# ============================================================

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
        "../R/03_sem_p04.R"

rule p04_sem_report:
    """Relatório R Markdown do P04."""
    input:
        relatorio = "resultados/P04/relatorio.txt"
    output:
        html = "resultados/P04/report.html"
    params:
        rmd = "../R/notebooks/04_sem_visualization.Rmd"
    shell:
        """
        R -e "rmarkdown::render('{params.rmd}', output_file='{output.html}')" \
            2>&1 | tee logs/p04_sem_report.log
        """
