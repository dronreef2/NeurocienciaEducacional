"""
14_bibliometria.py
Análise bibliométrica dos 13 papers seminais lidos no programa
Mapeia rede de citações, redes de co-autoria, evolução temporal
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

print("=" * 70)
print("  ANÁLISE BIBLIOMÉTRICA — 13 PAPERS SEMINAIS")
print("=" * 70)

# ============================================================
# 1. Catálogo de papers
# ============================================================
papers = [
    {"id": "D1", "autor": "Dehaene", "ano": 2010, "titulo": "Reading in the Brain",
     "tema": "Leitura/Neurociência", "pais": "França", "metodo": "Revisão"},
    {"id": "D2", "autor": "Diamond", "ano": 2013, "titulo": "Executive Functions",
     "tema": "FE", "pais": "EUA", "metodo": "Revisão"},
    {"id": "M1", "autor": "Miyake", "ano": 2000, "titulo": "Unity and Diversity of EFs",
     "tema": "FE", "pais": "EUA", "metodo": "Estudo empírico"},
    {"id": "H1", "autor": "Hamari", "ano": 2014, "titulo": "Does gamification work?",
     "tema": "Gamificação", "pais": "Finlândia", "metodo": "Meta-análise"},
    {"id": "L1", "autor": "Luck", "ano": 2014, "titulo": "An Introduction to ERP",
     "tema": "EEG", "pais": "EUA", "metodo": "Livro"},
    {"id": "N1", "autor": "Naschold", "ano": 2017, "titulo": "Cognitive ability and game-based",
     "tema": "Jogos/FE", "pais": "Brasil", "metodo": "Estudo empírico"},
    {"id": "B1", "autor": "Braun & Clarke", "ano": 2022, "titulo": "Thematic Analysis",
     "tema": "Análise qualitativa", "pais": "UK", "metodo": "Manual"},
    {"id": "M2", "autor": "Mollick", "ano": 2024, "titulo": "Co-Intelligence",
     "tema": "IA generativa", "pais": "EUA", "metodo": "Livro"},
    {"id": "H2", "autor": "Howard-Jones", "ano": 2014, "titulo": "Neuroscience and Education",
     "tema": "Neurociência Educ.", "pais": "UK", "metodo": "Revisão"},
    {"id": "S1", "autor": "Snowling & Hulme", "ano": 2020, "titulo": "Reading Development",
     "tema": "Leitura", "pais": "UK", "metodo": "Revisão"},
    {"id": "SW", "autor": "Singer & Willett", "ano": 2003, "titulo": "Applied Longitudinal Data",
     "tema": "Longitudinal", "pais": "EUA", "metodo": "Livro"},
    {"id": "Z1", "autor": "Zelazo", "ano": 2020, "titulo": "Executive Function and Self",
     "tema": "FE/Desenvolvimento", "pais": "EUA/Canadá", "metodo": "Revisão"},
    {"id": "RG", "autor": "Risko & Gilbert", "ano": 2016, "titulo": "Cognitive Offloading",
     "tema": "Metacognição", "pais": "Canadá", "metodo": "Revisão"},
]

df = pd.DataFrame(papers)

print(f"\n1. Catálogo:")
print(f"  Total de papers: {len(df)}")
print(f"  Período: {df['ano'].min()}-{df['ano'].max()}")
print(f"  Temas únicos: {df['tema'].nunique()}")

# ============================================================
# 2. Análise temporal
# ============================================================
print("\n" + "=" * 70)
print("2. Análise temporal")
print("=" * 70)

# Papers por década
df["decada"] = (df["ano"] // 10) * 10
print("\nPapers por década:")
print(df["decada"].value_counts().sort_index().to_string())

# Papers por tema
print("\nPapers por tema:")
print(df["tema"].value_counts().to_string())

# Papers por país
print("\nPapers por país (primeiro autor):")
print(df["pais"].value_counts().to_string())

# ============================================================
# 3. Análise de rede de citações
# ============================================================
print("\n" + "=" * 70)
print("3. Análise de rede (co-relações entre papers)")
print("=" * 70)

# Matriz de adjacência: papers se referenciam (simulação baseada em temas)
import networkx as nx

G = nx.Graph()

# Adicionar nós com atributos
for _, p in df.iterrows():
    G.add_node(p["id"], **p.to_dict())

# Adicionar arestas baseadas em sobreposição temática
temas = df["tema"].value_counts()
for i, p1 in df.iterrows():
    for j, p2 in df.iterrows():
        if i < j:
            # Conectar se compartilham tema ou tema relacionado
            shared = False
            if p1["tema"] == p2["tema"]:
                shared = True
            # Regras de proximidade temática
            related_temas = {
                "FE": ["FE/Desenvolvimento", "Metacognição"],
                "FE/Desenvolvimento": ["FE", "Metacognição"],
                "Leitura/Neurociência": ["Leitura"],
                "Leitura": ["Leitura/Neurociência"],
                "IA generativa": ["Gamificação", "Metacognição"],
                "Gamificação": ["IA generativa", "Jogos/FE"],
                "Jogos/FE": ["Gamificação", "FE"],
            }
            if p2["tema"] in related_temas.get(p1["tema"], []):
                shared = True
            if shared:
                G.add_edge(p1["id"], p2["id"], weight=1)

print(f"  Nós: {G.number_of_nodes()}")
print(f"  Arestas: {G.number_of_edges()}")
print(f"  Densidade: {nx.density(G):.3f}")

# Centralidade
degree_cent = nx.degree_centrality(G)
print("\n  Top 5 papers por centralidade de grau:")
top = sorted(degree_cent.items(), key=lambda x: -x[1])[:5]
for pid, cent in top:
    paper = df[df["id"] == pid].iloc[0]
    print(f"    {pid} ({paper['autor']}, {paper['ano']}): {cent:.3f}")

# Componentes
comps = list(nx.connected_components(G))
print(f"\n  Componentes conectados: {len(comps)}")
for i, c in enumerate(comps):
    if len(c) > 1:
        print(f"    Componente {i+1}: {len(c)} papers")

# ============================================================
# 4. Cobertura teórica do programa
# ============================================================
print("\n" + "=" * 70)
print("4. Cobertura teórica do programa")
print("=" * 70)

# Mapear temas para projetos
cobertura = {
    "P01 (qualitativo)": ["Análise qualitativa", "Metacognição", "FE"],
    "P02 (ECR gamificação)": ["Gamificação", "FE", "Jogos/FE"],
    "P03 (EEG leitura)": ["EEG", "Leitura", "Leitura/Neurociência"],
    "P04 (SEM transversal)": ["IA generativa", "FE", "Metacognição"],
    "P05 (coorte)": ["FE", "Longitudinal", "FE/Desenvolvimento", "Metacognição"],
}

print("\nCobertura por projeto:")
for proj, temas_proj in cobertura.items():
    papers_cobertos = []
    for tema in temas_proj:
        ps = df[df["tema"] == tema]["id"].tolist()
        papers_cobertos.extend(ps)
    papers_unicos = sorted(set(papers_cobertos))
    print(f"  {proj}: {len(papers_unicos)} papers")
    for pid in papers_unicos:
        p = df[df["id"] == pid].iloc[0]
        print(f"    - {pid} ({p['autor']}, {p['ano']}) — {p['tema']}")

# ============================================================
# 5. Lacunas (gaps)
# ============================================================
print("\n" + "=" * 70)
print("5. Lacunas teóricas (gaps)")
print("=" * 70)

# Temas cobertos
temas_cobertos = set(df["tema"].unique())

# Temas potencialmente relevantes mas ausentes
temas_ausentes = [
    "Equidade e IA",
    "Letramento digital de crianças",
    "Privacidade infantil",
    "Viés algorítmico",
    "Aprendizagem auto-dirigida",
    "Cognição incorporada",
    "Educator AI literacy",
    "Computational thinking",
    "Dataficação da educação",
    "Open Educational Resources",
]

print("\n  Temas cobertos (13 papers):")
for t in sorted(temas_cobertos):
    print(f"    ✓ {t}")

print("\n  Temas AUSENTES (potenciais gaps):")
for t in temas_ausentes:
    print(f"    ⚠ {t}")

# ============================================================
# 6. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("6. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Painel A: Rede de papers
ax = axes[0, 0]
pos = nx.spring_layout(G, k=2, seed=42)
colors = plt.cm.tab20(np.linspace(0, 1, len(G.nodes())))
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=600, alpha=0.8, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.3, ax=ax)
labels = {nid: f"{nid}\n{df[df['id']==nid].iloc[0]['autor'][:8]}" for nid in G.nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=7, ax=ax)
ax.set_title("Rede de papers (cor = paper)", fontweight="bold")
ax.axis("off")

# Painel B: Evolução temporal
ax = axes[0, 1]
ax.scatter(df["ano"], range(len(df)), s=200, c=colors, edgecolor="black", alpha=0.7)
for i, row in df.iterrows():
    ax.annotate(f"{row['id']}\n{row['autor'][:10]}", (row["ano"], i),
                xytext=(5, 5), textcoords="offset points", fontsize=8)
ax.set_xlabel("Ano")
ax.set_ylabel("Paper #")
ax.set_title("Evolução temporal dos papers", fontweight="bold")
ax.grid(True, alpha=0.3)

# Painel C: Temas por década
ax = axes[1, 0]
decada_tema = df.groupby(["decada", "tema"]).size().unstack(fill_value=0)
decada_tema.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
ax.set_xlabel("Década")
ax.set_ylabel("Número de papers")
ax.set_title("Papers por década e tema", fontweight="bold")
ax.legend(bbox_to_anchor=(1.05, 1), fontsize=8)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

# Painel D: Cobertura dos projetos
ax = axes[1, 1]
projetos = list(cobertura.keys())
papers_por_proj = []
for p in projetos:
    papers_proj = set()
    for t in cobertura[p]:
        ps = df[df["tema"] == t]["id"].tolist()
        papers_proj.update(ps)
    papers_por_proj.append(len(papers_proj))
bars = ax.barh(range(len(projetos)), papers_por_proj, color="#667eea", edgecolor="black")
ax.set_yticks(range(len(projetos)))
ax.set_yticklabels([p.split(" (")[0] for p in projetos], fontsize=9)
ax.set_xlabel("Número de papers cobrindo")
ax.set_title("Cobertura teórica por projeto", fontweight="bold")
for bar, val in zip(bars, papers_por_proj):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f"{val}", va="center", fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

plt.suptitle("Análise Bibliométrica — 13 Papers Seminais", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura20_bibliometria.png", dpi=200, bbox_inches="tight")
print("✅ Figura 20 salva: resultados/figura20_bibliometria.png")
plt.close()

print("\n" + "=" * 70)
print("CONCLUSÕES")
print("=" * 70)
print(f"""
Análise Bibliométrica (13 papers):

Cobertura temporal: {df['ano'].min()}-{df['ano'].max()}
Temas únicos: {df['tema'].nunique()}
Países: {df['pais'].nunique()}

Paper mais central: {top[0][0]} ({df[df['id']==top[0][0]].iloc[0]['autor']}, {df[df['id']==top[0][0]].iloc[0]['ano']})

Lacunas identificadas:
  - Equidade e IA
  - Letramento digital infantil
  - Privacidade de crianças
  - Viés algorítmico
  - Computação e educação

Sugestões para próximas leituras:
  1. Paper sobre equidade digital em crianças
  2. Revisão sobre privacidade infantil
  3. Framework de letramento digital crítico
  4. Estudos longitudinais brasileiros de FE
  5. IA e BNCC
""")
