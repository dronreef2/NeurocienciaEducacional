"""
01_tutorial_basico.py
TUTORIAL 1: Introdução ao programa

Objetivos:
- Entender a estrutura do repositório
- Carregar dados do piloto
- Visualizar informações básicas
- Fazer uma primeira análise

Pré-requisitos: Python 3.11+, pandas, matplotlib
Tempo estimado: 15 minutos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("  TUTORIAL 1 — Introdução ao Programa")
print("=" * 70)

# ============================================================
# PASSO 1: Estrutura do projeto
# ============================================================
print("""
PASSO 1: Estrutura do projeto

Este programa segue uma estrutura modular por projeto:

  NeurocienciaEducacional/
  ├── 00-fundamentos/      # Teoria, leitura, glossário
  ├── 01-projeto-...       # P01 (qualitativo)
  ├── 02-projeto-...       # P02 (ECR)
  ├── 03-projeto-...       # P03 (EEG)
  ├── 04-projeto-...       # P04 (SEM)
  ├── 05-projeto-...       # P05 (coorte)
  ├── docs/                # Documentação
  ├── analise/             # Código de análise
  ├── resultados/          # Outputs
  └── streamlit_app.py     # Dashboard entry point

Cada projeto tem sua própria pasta com:
  - protocolo/projeto-detalhado.md
  - dados/ (raw, processed)
  - pre-registro
  - análises específicas
""")

# ============================================================
# PASSO 2: Carregar dados do piloto
# ============================================================
print("\n" + "=" * 70)
print("PASSO 2: Carregar dados do piloto P01")
print("=" * 70)

# Construir caminho para os dados
BASE = Path("/workspace/01-projeto-qualitativo-criancas-ia/dados/piloto")

# Carregar diários
diarios_list = []
for f in sorted((BASE / "diarios").glob("*.csv")):
    df = pd.read_csv(f)
    df["data"] = pd.to_datetime(df["data"])
    diarios_list.append(df)
    print(f"  ✓ Carregado: {f.name} ({len(df)} registros)")

diarios = pd.concat(diarios_list, ignore_index=True)
print(f"\nTotal: {len(diarios)} registros de uso")

# ============================================================
# PASSO 3: Explorar dados
# ============================================================
print("\n" + "=" * 70)
print("PASSO 3: Explorar dados (estatísticas descritivas)")
print("=" * 70)

print("\nPor participante:")
stats = diarios.groupby("participante_id").agg(
    sessoes=("duracao_min", "count"),
    total_min=("duracao_min", "sum"),
    media_min=("duracao_min", "mean"),
    maximo=("duracao_min", "max"),
).round(2)
print(stats)

print("\nPor atividade:")
atividades = diarios["atividades"].value_counts()
print(atividades)

# ============================================================
# PASSO 4: Visualizar
# ============================================================
print("\n" + "=" * 70)
print("PASSO 4: Criar uma visualização")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Painel 1: Uso diário por criança
ax = axes[0]
for cid in diarios["participante_id"].unique():
    sub = diarios[diarios["participante_id"] == cid].sort_values("data")
    ax.plot(sub["data"], sub["duracao_min"], "o-", label=cid, alpha=0.7)

ax.set_xlabel("Data")
ax.set_ylabel("Duração (min)")
ax.set_title("Uso diário do Khanmigo")
ax.legend()
ax.grid(True, alpha=0.3)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Painel 2: Atividades por criança
ax = axes[1]
contagem = diarios.groupby(["participante_id", "atividades"]).size().unstack(fill_value=0)
contagem.plot(kind="bar", stacked=True, ax=ax, color=["#667eea", "#27ae60", "#f39c12", "#e74c3c"])
ax.set_xlabel("Participante")
ax.set_ylabel("Número de sessões")
ax.set_title("Atividades por criança")
ax.legend(title="Atividade", bbox_to_anchor=(1.05, 1))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("tutorial_1_resultado.png", dpi=150, bbox_inches="tight")
print("✅ Figura salva: tutorial_1_resultado.png")

# ============================================================
# PASSO 5: Primeira análise estatística
# ============================================================
print("\n" + "=" * 70)
print("PASSO 5: Primeira análise (uso médio por criança)")
print("=" * 70)

medias = diarios.groupby("participante_id")["duracao_min"].mean()
print("\nUso médio (min) por criança:")
for cid, media in medias.items():
    print(f"  {cid}: {media:.1f} min")

geral = diarios["duracao_min"].mean()
print(f"\nMédia geral: {geral:.1f} min")

# Quem usa mais?
mais = medias.idxmax()
menos = medias.idxmin()
print(f"\nQuem mais usa: {mais} ({medias[mais]:.1f} min)")
print(f"Quem menos usa: {menos} ({medias[menos]:.1f} min)")

# ============================================================
# PASSO 6: Próximos passos
# ============================================================
print("\n" + "=" * 70)
print("PRÓXIMOS PASSOS")
print("=" * 70)
print("""
Agora que você já explorou os dados básicos, pode:

1. 📊 Rodar análise estatística completa:
   python3 analise/Python/scripts/analise_piloto_real.py

2. 🎨 Abrir o dashboard interativo:
   streamlit run streamlit_app.py

3. 📖 Ler o manuscrito draft:
   cat docs/manuscritos/P01-manuscrito-rascunho-v1.md

4. 🧪 Rodar os testes:
   cd analise/Python && python3 -m pytest tests/

5. 🔬 Explorar outros notebooks:
   ls analise/Python/notebooks/

Bons estudos! 🚀
""")
