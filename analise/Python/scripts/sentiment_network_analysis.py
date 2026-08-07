"""
sentiment_network_analysis.py
Análise de sentimento + análise de rede dos 5 temas do P01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re
import json
from collections import Counter, defaultdict
from itertools import combinations
import networkx as nx
from datetime import datetime

print("=" * 70)
print("  ANÁLISE DE SENTIMENTO + REDE — TRANSCRIÇÕES P01")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 1. Carregar dados
# ============================================================
BASE = Path("/workspace/01-projeto-qualitativo-criancas-ia/dados/piloto")
TRANSCRICOES_DIR = BASE / "transcricoes"
CODEBOOK_PATH = BASE / "codebook" / "codebook-piloto.csv"

# Carregar transcrições
transcripts = {}
for f in TRANSCRICOES_DIR.glob("*.txt"):
    transcripts[f.stem] = f.read_text()

codebook = pd.read_csv(CODEBOOK_PATH)

print(f"\n  Transcrições carregadas: {len(transcripts)}")
print(f"  Códigos no codebook: {len(codebook)}")

# ============================================================
# 2. Léxico de sentimento PT-BR (simplificado)
# ============================================================
print("\n" + "=" * 70)
print("2. Análise de Sentimento (léxico PT-BR simplificado)")
print("=" * 70)

# Léxico básico de sentimento (PT-BR)
lexicon_pos = {
    "legal", "bom", "boa", "gostei", "gosto", "gostar", "ajud", "ajuda",
    "inteligente", "fácil", "divertid", "explica", "explicar", "legal",
    "óbvio", "ótimo", "ótima", "maravilhos", "incríve", "ótimo", "satisfeit",
    "feliz", "contente", "aprend", "aprendi", "aprendeu", "sabe", "sabia",
    "consegu", "consegui", "conseguiu", "legal", "amig", "amigo", "amiga",
    "irmã", "irmão", "mãe", "pai", "família", "prefer", "preferi"
}

lexicon_neg = {
    "ruim", "péssimo", "difícil", "odeio", "odiei", "detesto", "chato",
    "chata", "errado", "errada", "erro", "confund", "confuso", "confusa",
    "demora", "demorou", "lento", "lenta", "cansad", "cansada", "cansado",
    "triste", "bravo", "brava", "irritad", "chatead", "preocupad",
    "err", "errei", "errou", "confund", "não entendo", "não sei",
    "não gosto", "não gost", "preferia", "preferiria"
}

# Palavras intensificadoras
intensifiers = {"muito", "mais", "menos", "pouco", "pouca", "bem", "tão", "tanto"}

def analyze_sentiment_pt(text):
    """Analisa sentimento de um texto em PT-BR."""
    text_lower = text.lower()
    words = re.findall(r"\w+", text_lower)

    pos_count = sum(1 for w in words if any(p in w for p in lexicon_pos))
    neg_count = sum(1 for w in words if any(n in w for n in lexicon_neg))

    # Frases negativas
    if "não gosto" in text_lower or "não gost" in text_lower:
        neg_count += 2
    if "não entendo" in text_lower:
        neg_count += 2

    total = pos_count + neg_count
    if total == 0:
        return 0, 0, 0
    return pos_count, neg_count, (pos_count - neg_count) / total

# Analisar cada transcrição
print("\n  Sentimento por participante:")
sentimentos = {}
for cid, text in transcripts.items():
    pos, neg, score = analyze_sentiment_pt(text)
    sentimentos[cid] = {"positivo": pos, "negativo": neg, "score": score}
    print(f"    {cid}: {pos} positivos, {neg} negativos, score = {score:+.2f}")

# Sentimento médio
scores = [s["score"] for s in sentimentos.values()]
print(f"\n  Score médio: {np.mean(scores):+.3f} (DP = {np.std(scores):.3f})")

# ============================================================
# 3. Análise de rede: co-ocorrência de códigos
# ============================================================
print("\n" + "=" * 70)
print("3. Análise de rede: co-ocorrência de códigos por participante")
print("=" * 70)

# Para cada participante, ver quais códigos co-ocorrem
participant_codes = defaultdict(set)
for _, row in codebook.iterrows():
    codigo = row["codigo"]
    parts = str(row["participantes"]).split(";")
    for p in parts:
        p = p.strip()
        if p:
            participant_codes[p].add(codigo)

# Construir rede: códigos conectados se co-ocorrem no mesmo participante
G = nx.Graph()

# Adicionar nós (códigos) com atributo de tema
tema_map = {
    "usa_pronome_pessoal": "Antropomorfização",
    "atribui_inteligencia": "Antropomorfização",
    "atribui_emocoes": "Antropomorfização",
    "distincao_robot": "Antropomorfização",
    "deteccao_erro_imediata": "Detecção de Erro",
    "deteccao_erro_diferida": "Detecção de Erro",
    "correcao_tutor": "Detecção de Erro",
    "reporta_erro_professor": "Detecção de Erro",
    "confianca_alta": "Confiança Calibrada",
    "confianca_baixa": "Confiança Calibrada",
    "confianca_calibrada": "Confiança Calibrada",
    "compara_humano": "Comparação Humana",
    "comparacao_continua": "Comparação Humana",
    "atribuicao_amizade": "Comparação Humana",
    "preferencia_professor": "Preferência Contextual",
    "uso_estrategico": "Preferência Contextual",
    "limitacao_percebida": "Preferência Contextual",
}

# Cores por tema
tema_colors = {
    "Antropomorfização": "#e74c3c",
    "Detecção de Erro": "#3498db",
    "Confiança Calibrada": "#27ae60",
    "Comparação Humana": "#9b59b6",
    "Preferência Contextual": "#f39c12",
}

for codigo in codebook["codigo"].unique():
    if codigo in tema_map:
        G.add_node(codigo, tema=tema_map[codigo], color=tema_colors[tema_map[codigo]])

# Adicionar arestas: peso = quantos participantes têm ambos os códigos
for p, codes in participant_codes.items():
    codes_in_net = [c for c in codes if c in G.nodes]
    for c1, c2 in combinations(codes_in_net, 2):
        if G.has_edge(c1, c2):
            G[c1][c2]["weight"] += 1
        else:
            G.add_edge(c1, c2, weight=1)

print(f"  Nós: {G.number_of_nodes()}")
print(f"  Arestas: {G.number_of_edges()}")

# Remover códigos isolados
isolated = list(nx.isolates(G))
G.remove_nodes_from(isolated)
print(f"  Nós isolados removidos: {len(isolated)}")

# ============================================================
# 4. Métricas de centralidade
# ============================================================
print("\n" + "=" * 70)
print("4. Métricas de centralidade")
print("=" * 70)

degree_cent = nx.degree_centrality(G)
betweenness_cent = nx.betweenness_centrality(G, weight="weight")
closeness_cent = nx.closeness_centrality(G)
eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000, weight="weight")

# Top 10 por centralidade de grau
print("\n  Top 10 por centralidade de grau:")
top_degree = sorted(degree_cent.items(), key=lambda x: -x[1])[:10]
for codigo, cent in top_degree:
    tema = tema_map.get(codigo, "?")
    print(f"    {codigo:<30} (T={tema[:15]:<15}): {cent:.3f}")

# Top 5 por betweenness (intermediação)
print("\n  Top 5 por betweenness (intermediação):")
top_betw = sorted(betweenness_cent.items(), key=lambda x: -x[1])[:5]
for codigo, cent in top_betw:
    tema = tema_map.get(codigo, "?")
    print(f"    {codigo:<30} (T={tema[:15]:<15}): {cent:.3f}")

# Densidade
density = nx.density(G)
print(f"\n  Densidade da rede: {density:.3f}")

# Componentes conectados
components = list(nx.connected_components(G))
print(f"  Componentes conectados: {len(components)}")
for i, comp in enumerate(components):
    if len(comp) > 2:
        print(f"    Componente {i+1}: {len(comp)} códigos: {list(comp)[:5]}...")

# Clusters
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))
print(f"\n  Comunidades detectadas (modularity): {len(communities)}")
for i, comm in enumerate(communities):
    print(f"    Comunidade {i+1}: {len(comm)} códigos: {list(comm)[:5]}")

# ============================================================
# 5. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("5. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Painel A: Rede de co-ocorrência
ax = axes[0, 0]
pos = nx.spring_layout(G, k=2, seed=42, weight="weight")
colors = [G.nodes[n].get("color", "gray") for n in G.nodes]
sizes = [300 + 500*degree_cent[n] for n in G.nodes]

nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes, alpha=0.8, ax=ax)
edges = G.edges(data=True)
weights = [e[2]["weight"] for e in edges]
nx.draw_networkx_edges(G, pos, width=[w*0.8 for w in weights], alpha=0.4, ax=ax, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)

ax.set_title("Rede de co-ocorrência de códigos\n(tamanho = grau, cor = tema)", fontweight="bold")
ax.axis("off")

# Legenda de cores
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=tema) for tema, color in tema_colors.items()]
ax.legend(handles=legend_elements, loc="upper left", fontsize=8)

# Painel B: Centralidade de grau por tema
ax = axes[0, 1]
tema_centrality = defaultdict(list)
for codigo, cent in degree_cent.items():
    tema = tema_map.get(codigo, "?")
    tema_centrality[tema].append(cent)

temas_ord = list(tema_centrality.keys())
means = [np.mean(tema_centrality[t]) for t in temas_ord]
sems = [np.std(tema_centrality[t])/np.sqrt(len(tema_centrality[t])) for t in temas_ord]

ax.barh(temas_ord, means, xerr=sems, color=[tema_colors[t] for t in temas_ord], edgecolor="black", capsize=5)
ax.set_xlabel("Centralidade de grau média")
ax.set_title("Centralidade por tema", fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

# Painel C: Sentimento por participante
ax = axes[1, 0]
cids = list(sentimentos.keys())
scores_arr = [sentimentos[c]["score"] for c in cids]
colors_sent = ["#27ae60" if s > 0 else "#e74c3c" if s < 0 else "#95a5a6" for s in scores_arr]
bars = ax.bar(cids, scores_arr, color=colors_sent, edgecolor="black")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_ylabel("Score de sentimento")
ax.set_title("Sentimento por participante\n(verde = positivo, vermelho = negativo)", fontweight="bold")
ax.grid(True, axis="y", alpha=0.3)

for bar, score in zip(bars, scores_arr):
    ax.text(bar.get_x() + bar.get_width()/2,
            score + (0.02 if score > 0 else -0.05),
            f"{score:+.2f}", ha="center", fontweight="bold")

# Painel D: Top 10 códigos por centralidade de autovetor
ax = axes[1, 1]
top_eig = sorted(eigenvector_cent.items(), key=lambda x: -x[1])[:10]
codes_eig = [c[0] for c in top_eig]
vals_eig = [c[1] for c in top_eig]
colors_eig = [tema_map.get(c, "?") and tema_colors[tema_map.get(c, "?")] for c in codes_eig]
ax.barh(range(len(codes_eig)), vals_eig, color=colors_eig, edgecolor="black")
ax.set_yticks(range(len(codes_eig)))
ax.set_yticklabels(codes_eig, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel("Centralidade de autovetor")
ax.set_title("Top 10 códigos (autovetor)\nimportância global na rede", fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

plt.suptitle("Análise de Sentimento + Rede de Códigos (P01)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura17_sentiment_network.png", dpi=200, bbox_inches="tight")
print("✅ Figura 17 salva: resultados/figura17_sentiment_network.png")
plt.close()

# ============================================================
# 6. Salvar resultados
# ============================================================
print("\n" + "=" * 70)
print("6. SALVANDO RESULTADOS")
print("=" * 70)

resultados = {
    "data_analise": datetime.now().isoformat(),
    "sentimento": sentimentos,
    "rede": {
        "n_nos": G.number_of_nodes(),
        "n_arestas": G.number_of_edges(),
        "densidade": float(density),
        "n_componentes": len(components),
        "n_comunidades": len(communities),
    },
    "centralidade": {
        codigo: {
            "grau": float(degree_cent[codigo]),
            "betweenness": float(betweenness_cent[codigo]),
            "closeness": float(closeness_cent[codigo]),
            "autovetor": float(eigenvector_cent[codigo]),
        }
        for codigo in G.nodes
    },
    "top_grau": [{"codigo": c, "centralidade": float(v)} for c, v in top_degree],
    "top_betweenness": [{"codigo": c, "centralidade": float(v)} for c, v in top_betw],
    "comunidades": [list(c) for c in communities],
}

# Limpar NaN
def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items() if not (isinstance(v, float) and np.isnan(v))}
    elif isinstance(obj, float) and np.isnan(obj):
        return None
    return obj

output_path = Path("resultados/relatorio_sentiment_network.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(clean(resultados), f, indent=2, ensure_ascii=False, default=str)

print(f"✅ Relatório salvo: {output_path}")

# ============================================================
# 7. Conclusões
# ============================================================
print("\n" + "=" * 70)
print("7. CONCLUSÕES")
print("=" * 70)
print(f"""
ANÁLISE DE SENTIMENTO:
  Score médio: {np.mean(scores):+.3f}
  Range: [{min(scores):+.2f}, {max(scores):+.2f}]

ANÁLISE DE REDE:
  Nós (códigos): {G.number_of_nodes()}
  Arestas (co-ocorrências): {G.number_of_edges()}
  Densidade: {density:.3f}
  Comunidades: {len(communities)}

CÓDIGO MAIS CENTRAL (grau): {top_degree[0][0]}
  Centralidade = {top_degree[0][1]:.3f}

CÓDIGO PONTE (betweenness): {top_betw[0][0]}
  Conecta diferentes sub-redes

IMPLICAÇÕES:
  1. O tema mais central é '{tema_map.get(top_degree[0][0], "?")}'
  2. A rede tem {len(communities)} sub-estruturas
  3. O sentimento varia entre crianças (heterogeneidade)
  4. Códigos co-ocorrem formando clusters temáticos
""")
