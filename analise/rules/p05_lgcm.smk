# ============================================================
# rules/p05_lgcm.smk
# Regras para LGCM do P05
# ============================================================

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
        "../R/04_lgcm_p05.R"

rule p05_lgcm_report:
    """Relatório R Markdown do P05."""
    input:
        relatorio = "resultados/P05/relatorio.txt"
    output:
        html = "resultados/P05/report.html"
    params:
        rmd = "../R/notebooks/03_lgcm_visualization.Rmd"
    shell:
        """
        R -e "rmarkdown::render('{params.rmd}', output_file='{output.html}')" \
            2>&1 | tee logs/p05_lgcm_report.log
        """
