# ============================================================
# rules/common.smk
# Regras comuns e funções utilitárias compartilhadas
# ============================================================

import os
from pathlib import Path

# Diretórios do projeto
PROJETO_ROOT = Path(workflow.basedir).parent.parent
ANALISE_DIR = PROJETO_ROOT / "analise"
RESULTADOS_DIR = PROJETO_ROOT / "resultados"
LOG_DIR = PROJETO_ROOT / "logs"
DADOS_DIR = PROJETO_ROOT / "dados"

# Criar diretórios
for d in [RESULTADOS_DIR, LOG_DIR,
          DADOS_DIR / "raw", DADOS_DIR / "processed"]:
    d.mkdir(parents=True, exist_ok=True)

# Função helper para paths
def resultado_path(projeto, arquivo):
    return str(RESULTADOS_DIR / projeto / arquivo)

def log_path(script_name):
    return str(LOG_DIR / f"{script_name}.log")

# Wildcard constraints
wildcard_constraints:
    projeto=r"P\d{2}",
    arquivo=r"[\w\.\-]+",

# ============================================================
# Regra: criar estrutura de diretórios
# ============================================================
rule setup_dirs:
    """Cria estrutura de diretórios do projeto."""
    output:
        raw_dir = directory(str(DADOS_DIR / "raw")),
        processed_dir = directory(str(DADOS_DIR / "processed")),
        results_dir = directory(str(RESULTADOS_DIR)),
        log_dir = directory(str(LOG_DIR))
    run:
        for d in [output.raw_dir, output.processed_dir,
                  output.results_dir, output.log_dir]:
            os.makedirs(d, exist_ok=True)

# ============================================================
# Regra: instalar dependências Python
# ============================================================
rule install_python_deps:
    """Instala dependências Python via Poetry."""
    output:
        touch_file = touch(str(ANALISE_DIR / ".deps_installed"))
    log:
        str(LOG_DIR / "install_python_deps.log")
    shell:
        "poetry install --no-interaction 2>&1 | tee {log}"

# ============================================================
# Regra: instalar dependências R
# ============================================================
rule install_r_deps:
    """Instala dependências R."""
    output:
        touch_file = touch(str(ANALISE_DIR / ".rdeps_installed"))
    log:
        str(LOG_DIR / "install_r_deps.log")
    shell:
        """
        R -e 'options(repos=c(CRAN="https://cran.r-project.org"))' \
           -e 'install.packages(c("tidyverse", "tidytext", "lavaan", "emmeans", "afex", "psych"))' \
           2>&1 | tee {log}
        """

# ============================================================
# Regra: rodar testes
# ============================================================
rule test_python:
    """Roda testes Python (pytest)."""
    output:
        report = "resultados/test_report_py.html"
    log:
        str(LOG_DIR / "test_python.log")
    shell:
        """
        poetry run pytest analise/Python/neurociencia_edu/tests/ \
            --html={output.report} --self-contained-html \
            2>&1 | tee {log}
        """

rule test_r:
    """Roda testes R (testthat)."""
    output:
        report = "resultados/test_report_r.html"
    log:
        str(LOG_DIR / "test_r.log")
    shell:
        """
        R -e "testthat::test_dir('analise/R/tests/testthat', reporter='html')" 2>&1 \
            | tee {log}
        """

# ============================================================
# Regra: lint
# ============================================================
rule lint:
    """Roda linters em Python e R."""
    output:
        touch_file = touch("resultados/.lint_ok")
    log:
        str(LOG_DIR / "lint.log")
    shell:
        """
        echo "=== Lint Python ===" && \
        poetry run ruff check analise/Python/ 2>&1 | tee {log} && \
        echo "=== Lint R ===" && \
        R -e "lintr::lint_dir('analise/R/R/')" 2>&1 | tee -a {log} && \
        touch {output.touch_file}
        """

# ============================================================
# Regra: relatório global
# ============================================================
rule relatorio_global:
    """Gera relatório HTML global agregando todos os projetos."""
    input:
        p01 = "resultados/P01/relatorio.txt",
        p02 = "resultados/P02/relatorio.txt",
        p03 = "resultados/P03/relatorio.txt",
        p04 = "resultados/P04/relatorio.txt",
        p05 = "resultados/P05/relatorio.txt"
    output:
        "resultados/relatorio_global.html"
    run:
        from datetime import datetime
        from pathlib import Path as P
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório Global — Programa de Pesquisa</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">
    <style>body {{ max-width: 1200px; }}</style>
</head>
<body>
    <h1>📊 Relatório Global — Programa de Pesquisa</h1>
    <p><small>Gerado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</small></p>

    <nav>
        <ul>
            <li><a href="#p01">P01 — Análise Temática</a></li>
            <li><a href="#p02">P02 — ANCOVA</a></li>
            <li><a href="#p03">P03 — EEG/ERP</a></li>
            <li><a href="#p04">P04 — SEM</a></li>
            <li><a href="#p05">P05 — LGCM</a></li>
        </ul>
    </nav>

    <section id="p01"><h2>🟢 P01 — Análise Temática (Khanmigo)</h2>
    <pre>{P(input.p01).read_text(encoding='utf-8', errors='ignore')}</pre></section>

    <section id="p02"><h2>🟡 P02 — Gamificação (ANCOVA)</h2>
    <pre>{P(input.p02).read_text(encoding='utf-8', errors='ignore')}</pre></section>

    <section id="p03"><h2>🔴 P03 — EEG / ERP (Bandeira)</h2>
    <pre>{P(input.p03).read_text(encoding='utf-8', errors='ignore')}</pre></section>

    <section id="p04"><h2>🟣 P04 — IA Generativa × FE (SEM)</h2>
    <pre>{P(input.p04).read_text(encoding='utf-8', errors='ignore')}</pre></section>

    <section id="p05"><h2>🔵 P05 — Coorte Longitudinal (LGCM)</h2>
    <pre>{P(input.p05).read_text(encoding='utf-8', errors='ignore')}</pre></section>

    <hr>
    <p><small>Programa de Pesquisa em Neurociência Educacional — UFRN/CERES</small></p>
</body>
</html>"""
        P(output[0]).write_text(html, encoding="utf-8")
