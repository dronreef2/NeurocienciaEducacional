"""
Snakefile principal para o Programa de Pesquisa em Neurociência Educacional
Orquestra toda a pipeline: dados → validação → análise → relatórios

Uso:
  snakemake --cores 4                    # Roda tudo
  snakemake --cores 4 resultados/P01_report.html   # Alvo específico
  snakemake --cores 4 --use-conda         # Com conda envs
"""

import os
from pathlib import Path

# ============================================================
# Configuração
# ============================================================
WORKDIR = Path("/workspace")
SCRIPTS = WORKDIR / "analise" / "Python" / "scripts"
NOTEBOOKS = WORKDIR / "analise" / "Python" / "notebooks"
RESULTS = WORKDIR / "resultados"
DATA = WORKDIR / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto"
SYNTHETIC = WORKDIR / "dados_sinteticos"

# Criar diretórios
RESULTS.mkdir(parents=True, exist_ok=True)
SYNTHETIC.mkdir(parents=True, exist_ok=True)

# ============================================================
# Regra principal
# ============================================================

rule all:
    input:
        # Dados sintéticos
        f"{SYNTHETIC}/P01_diarios_sinteticos.csv",
        f"{SYNTHETIC}/P02_dados_sinteticos.csv",
        f"{SYNTHETIC}/P04_dados_sinteticos.csv",
        f"{SYNTHETIC}/P05_dados_longitudinais_sinteticos.csv",
        # Validação
        f"{RESULTS}/validacao_dados.json",
        # Análises
        f"{RESULTS}/relatorio_analise_piloto.json",
        f"{RESULTS}/relatorio_mixed_models.json",
        f"{RESULTS}/relatorio_sentiment_network.json",
        # Figuras principais
        f"{RESULTS}/figura12_analise_piloto.png",
        f"{RESULTS}/figura13_mixed_models_diarios.png",
        f"{RESULTS}/figura17_sentiment_network.png",
        f"{RESULTS}/figura20_bibliometria.png",
    output:
        f"{RESULTS}/pipeline_report.txt"
    shell:
        "echo 'Pipeline completa: {{input}}' > {{output}}"
        "date >> {RESULTS}/pipeline_report.txt"

# ============================================================
# Etapa 1: Dados sintéticos
# ============================================================

rule synthetic_data:
    output:
        p01 = f"{SYNTHETIC}/P01_diarios_sinteticos.csv",
        p02 = f"{SYNTHETIC}/P02_dados_sinteticos.csv",
        p04 = f"{SYNTHETIC}/P04_dados_sinteticos.csv",
        p05 = f"{SYNTHETIC}/P05_dados_longitudinais_sinteticos.csv",
        p03_papel = f"{SYNTHETIC}/P03_eeg_papel.npy",
        p03_tela = f"{SYNTHETIC}/P03_eeg_tela.npy",
    script:
        f"{SCRIPTS}/gerar_dados_sinteticos.py"

# ============================================================
# Etapa 2: Validação
# ============================================================

rule validate_pilot:
    input:
        diarios = f"{DATA}/diarios",
    output:
        f"{RESULTS}/validacao_dados.json"
    script:
        f"{SCRIPTS}/validar_dados_piloto.py"

# ============================================================
# Etapa 3: Análise estatística do piloto
# ============================================================

rule analyze_pilot:
    input:
        codebook = f"{DATA}/codebook/codebook-piloto.csv",
        diarios = f"{DATA}/diarios",
    output:
        json = f"{RESULTS}/relatorio_analise_piloto.json",
        fig = f"{RESULTS}/figura12_analise_piloto.png",
    script:
        f"{SCRIPTS}/analise_piloto_real.py"

# ============================================================
# Etapa 4: Mixed models
# ============================================================

rule mixed_models:
    input:
        diarios = f"{DATA}/diarios"
    output:
        json = f"{RESULTS}/relatorio_mixed_models.json",
        fig = f"{RESULTS}/figura13_mixed_models_diarios.png",
    script:
        f"{SCRIPTS}/mixed_models_diarios.py"

# ============================================================
# Etapa 5: Sentimento + rede
# ============================================================

rule sentiment_network:
    input:
        transcricoes = f"{DATA}/transcricoes",
        codebook = f"{DATA}/codebook/codebook-piloto.csv",
    output:
        json = f"{RESULTS}/relatorio_sentiment_network.json",
        fig = f"{RESULTS}/figura17_sentiment_network.png",
    script:
        f"{SCRIPTS}/sentiment_network_analysis.py"

# ============================================================
# Etapa 6: Bibliometria
# ============================================================

rule bibliometria:
    output:
        f"{RESULTS}/figura20_bibliometria.png"
    script:
        f"{NOTEBOOKS}/14_bibliometria.py"

# ============================================================
# Etapa 7: Relatório consolidado
# ============================================================

rule consolidated_report:
    input:
        expand(f"{RESULTS}/{f}" for f in [
            "validacao_dados.json",
            "relatorio_analise_piloto.json",
            "relatorio_mixed_models.json",
            "relatorio_sentiment_network.json",
        ])
    output:
        f"{RESULTS}/relatorio_consolidado.md"
    run:
        import json
        from pathlib import Path
        from datetime import datetime

        lines = ["# Relatório Consolidado\n",
                f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
                "## Sumário Executivo\n"]

        for f in input:
            if Path(f).exists():
                with open(f) as fp:
                    data = json.load(fp)
                name = Path(f).stem
                lines.append(f"### {name}\n")
                if isinstance(data, dict):
                    for k, v in list(data.items())[:5]:
                        lines.append(f"- **{k}:** {v}")
                lines.append("")

        Path(output[0]).write_text("\n".join(lines))

# ============================================================
# Limpeza
# ============================================================

rule clean_all:
    shell:
        "rm -rf {RESULTS}/* && echo 'Limpo!'"

# ============================================================
# Help
# ============================================================

rule help:
    run:
        print("""
Snakemake Pipeline - Programa de Pesquisa em Neurociência Educacional

Regras disponíveis:
  synthetic_data      Gera dados sintéticos para os 5 projetos
  validate_pilot       Valida dados reais do piloto
  analyze_pilot        Análise estatística completa do piloto
  mixed_models         Mixed-effects nos diários
  sentiment_network    Análise de sentimento + rede
  bibliometria         Análise bibliométrica
  consolidated_report  Relatório consolidado em Markdown
  clean_all            Limpa todos os resultados
  all                  Roda tudo

Exemplos:
  snakemake --cores 4                          # Tudo
  snakemake --cores 4 analyze_pilot            # Só análise do piloto
  snakemake --cores 4 consolidated_report       # Só relatório
  snakemake --cores 4 --dry-run                # Dry run
        """)
