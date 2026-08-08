"""
13_item_analysis.py
Análise Clássica de Itens (CTT) para P05
Avalia qualidade de itens do questionário
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("  ANÁLISE DE ITENS (CTT) — P05")
print("=" * 70)

# ============================================================
# 1. Simular respostas a 30 itens
# ============================================================
print("\n1. Simulando respostas (500 respondentes, 30 itens Likert 0-4)")

np.random.seed(42)
n = 500
n_itens = 30

# Habilidade latente
theta = np.random.normal(0, 1, n)

# Dificuldade dos itens (mix de fáceis, médios, difíceis + 2 problemáticos)
dificuldades = np.concatenate([
    np.random.normal(-1.5, 0.3, 5),   # muito fáceis
    np.random.normal(-0.5, 0.3, 10),  # fáceis
    np.random.normal(0, 0.3, 10),     # médios
    np.random.normal(1.0, 0.3, 3),    # difíceis
    np.random.normal(0, 0.3, 2),      # 2 problemáticos (baixa discriminação)
])

# Discriminação (item 28 e 29 serão ruins)
discriminacao = np.ones(n_itens) * 1.0
discriminacao[28] = 0.2  # ruim
discriminacao[29] = 0.3  # ruim

# Modelo contínuo
probabilidades = 1 / (1 + np.exp(-(discriminacao * theta[:, None] - dificuldades[None, :])))
# Para Likert 0-4, sortear categoria
respostas = np.zeros((n, n_itens), dtype=int)
for j in range(n_itens):
    for i in range(n):
        # Probabilidade de resposta "correta" (alta = bom)
        p = probabilidades[i, j]
        # Mapeia para 0-4
        respostas[i, j] = np.random.choice([0, 1, 2, 3, 4], p=[0.2, 0.2, 0.2, 0.2, 0.2])

# Tornar respostas mais realistas
for j in range(n_itens):
    p_base = 1 / (1 + np.exp(-(theta - dificuldades[j])))
    for i in range(n):
        # Prob de resposta 4 (melhor) é proporcional a p_base
        p4 = p_base[i] * 0.6
        p3 = p_base[i] * 0.3
        p2 = (1 - p_base[i]) * 0.5
        p1 = (1 - p_base[i]) * 0.3
        p0 = (1 - p_base[i]) * 0.2
        ps = np.array([p0, p1, p2, p3, p4])
        ps = ps / ps.sum()
        respostas[i, j] = np.random.choice(5, p=ps)

df = pd.DataFrame(respostas, columns=[f"item_{i+1:02d}" for i in range(n_itens)])

print(f"  N = {n}")
print(f"  N itens = {n_itens}")
print(f"  Média geral: {df.values.mean():.2f}")
print(f"  DP geral: {df.values.std():.2f}")

# ============================================================
# 2. Estatísticas por item
# ============================================================
print("\n" + "=" * 70)
print("2. Estatísticas por item")
print("=" * 70)

print(f"\n{'Item':<8} | {'M':<6} | {'DP':<6} | {'r-corr':<8} | {'α sem item':<12} | {'Classif'}")
print("-" * 80)

total_score = df.sum(axis=1)
cronbach_full = (n_itens / (n_itens - 1)) * (1 - df.var().sum() / df.sum(axis=1).var())

print(f"  {'Alpha total:':<40} {cronbach_full:.3f}\n")

for j in range(n_itens):
    item = df.iloc[:, j]
    media = item.mean()
    dp = item.std()
    r_corr = item.corr(total_score)

    # Alpha sem o item
    df_sem = df.drop(df.columns[j], axis=1)
    cronbach_sem = (df_sem.shape[1] / (df_sem.shape[1] - 1)) * (1 - df_sem.var().sum() / df_sem.sum(axis=1).var())

    if r_corr < 0.3:
        classif = "❌ PROBLEMÁTICO"
    elif media < 1.0 or media > 3.5:
        classif = "⚠️ Extremo"
    elif r_corr < 0.4:
        classif = "Medíocre"
    else:
        classif = "✅ Bom"

    flag = " ⭐" if j in [28, 29] else ""
    print(f"  {j+1:02d}    | {media:.2f}  | {dp:.2f}  | {r_corr:+.3f}   | {cronbach_sem:.3f}        | {classif}{flag}")

# ============================================================
# 3. Análise fatorial exploratória (EFA)
# ============================================================
print("\n" + "=" * 70)
print("3. Análise Fatorial (EFA)")
print("=" * 70)

from numpy.linalg import svd

# Matriz de correlação
corr = df.corr()
autovalores, _ = np.linalg.eig(corr)
autovalores = np.real(autovalores)
autovalores_sorted = np.sort(autovalores)[::-1]

# Critério de Kaiser (autovalores > 1)
n_fatores_kaiser = (autovalores_sorted > 1).sum()
print(f"  Critério de Kaiser (>1): {n_fatores_kaiser} fatores")
print(f"  Variância explicada: {autovalores_sorted[:n_fatores_kaiser].sum() / n_itens * 100:.1f}%")

# Scree plot data
print(f"\n  Top 5 autovalores:")
for i, av in enumerate(autovalores_sorted[:5], 1):
    var_pct = av / n_itens * 100
    cum_pct = autovalores_sorted[:i].sum() / n_itens * 100
    print(f"    F{i}: λ = {av:.2f} ({var_pct:.1f}% var, {cum_pct:.1f}% cumulativa)")

# ============================================================
# 4. Índice de dificuldade e discriminação
# ============================================================
print("\n" + "=" * 70)
print("4. Índices de dificuldade e discriminação")
print("=" * 70)

# Dividir em grupos (27% superior vs 27% inferior)
corte_sup = np.percentile(total_score, 73)
corte_inf = np.percentile(total_score, 27)
g_sup = df[total_score >= corte_sup]
g_inf = df[total_score <= corte_inf]

print(f"\n{'Item':<8} | {'Dif (p)':<10} | {'Disc (D)':<12} | {'Interpretação'}")
print("-" * 70)

for j in range(n_itens):
    p = df.iloc[:, j].mean() / 4  # índice de dificuldade (0-1)
    disc = g_sup.iloc[:, j].mean() - g_inf.iloc[:, j].mean()  # índice de discriminação

    if p < 0.2:
        dif_class = "muito difícil"
    elif p < 0.4:
        dif_class = "difícil"
    elif p < 0.6:
        dif_class = "médio"
    elif p < 0.8:
        dif_class = "fácil"
    else:
        dif_class = "muito fácil"

    if disc < 0.2:
        disc_class = "ruim"
    elif disc < 0.3:
        disc_class = "medíocre"
    elif disc < 0.4:
        disc_class = "boa"
    else:
        disc_class = "excelente"

    flag = " ⭐" if j in [28, 29] else ""
    print(f"  {j+1:02d}    | {p:.3f}     | {disc:.3f}      | {dif_class} / {disc_class}{flag}")

# ============================================================
# 5. Recomendações
# ============================================================
print("\n" + "=" * 70)
print("5. Recomendações")
print("=" * 70)

# Identificar itens problemáticos
items_problema = []
for j in range(n_itens):
    item = df.iloc[:, j]
    r_corr = item.corr(total_score)
    p = item.mean() / 4

    if r_corr < 0.3 or p < 0.2 or p > 0.8:
        items_problema.append((j+1, r_corr, p))

print(f"\n  Itens com problemas: {len(items_problema)}/{n_itens}")
for item_id, r, p in items_problema:
    problemas = []
    if r < 0.3:
        problemas.append("baixa correlação")
    if p < 0.2:
        problemas.append("muito difícil")
    if p > 0.8:
        problemas.append("muito fácil")
    print(f"    Item {item_id}: {', '.join(problemas)}")

# Sugerir remoções
items_remover = [j+1 for j, r, p in items_problema if r < 0.3]
print(f"\n  Sugestão: remover itens {items_remover}")
print(f"  Alpha após remoção: ver cálculo abaixo")

if items_remover:
    df_limpo = df.drop([f"item_{i:02d}" for i in items_remover], axis=1)
    if df_limpo.shape[1] > 1:
        alpha_pos = (df_limpo.shape[1] / (df_limpo.shape[1] - 1)) * (1 - df_limpo.var().sum() / df_limpo.sum(axis=1).var())
        print(f"  Alpha com itens removidos: {alpha_pos:.3f}")
        print(f"  Melhoria: {alpha_pos - cronbach_full:+.3f}")
    else:
        print(f"  Não é possível calcular alpha com 1 item")

# ============================================================
# 6. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("6. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel A: Distribuição do escore total
ax = axes[0, 0]
ax.hist(total_score, bins=30, color="#667eea", edgecolor="black", alpha=0.7)
ax.axvline(total_score.mean(), color="red", linestyle="--", label=f"Média = {total_score.mean():.1f}")
ax.set_xlabel("Escore total")
ax.set_ylabel("Frequência")
ax.set_title("Distribuição dos escores totais", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel B: Correlação item-total
ax = axes[0, 1]
correlacoes = [df.iloc[:, j].corr(total_score) for j in range(n_itens)]
cores = ["#e74c3c" if c < 0.3 else "#27ae60" for c in correlacoes]
ax.bar(range(1, n_itens+1), correlacoes, color=cores, edgecolor="black")
ax.axhline(0.3, color="red", linestyle="--", label="Mínimo aceitável")
ax.set_xlabel("Item")
ax.set_ylabel("Correlação item-total")
ax.set_title("Correlação item-total\n(vermelho = problemático)", fontweight="bold")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)

# Painel C: Scree plot
ax = axes[1, 0]
ax.plot(range(1, min(11, n_itens+1)), autovalores_sorted[:10], "o-", linewidth=2, markersize=8)
ax.axhline(1, color="red", linestyle="--", label="Critério de Kaiser")
ax.set_xlabel("Fator")
ax.set_ylabel("Autovalor")
ax.set_title("Scree Plot", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel D: Dificuldade × Discriminação
ax = axes[1, 1]
ps = [df.iloc[:, j].mean() / 4 for j in range(n_itens)]
ds = [g_sup.iloc[:, j].mean() - g_inf.iloc[:, j].mean() for j in range(n_itens)]
colors_disc = ["#e74c3c" if d < 0.3 else "#27ae60" for d in ds]
ax.scatter(ps, ds, c=colors_disc, s=80, edgecolor="black", alpha=0.7)
ax.axhline(0.3, color="red", linestyle="--", alpha=0.5)
ax.set_xlabel("Índice de dificuldade (p)")
ax.set_ylabel("Índice de discriminação (D)")
ax.set_title("Dificuldade × Discriminação", fontweight="bold")
ax.grid(True, alpha=0.3)

# Destacar itens problemáticos
for j in [28, 29]:
    ax.annotate(f"item {j+1}", (ps[j], ds[j]), xytext=(5, 5), textcoords="offset points",
                fontweight="bold", color="red")

plt.suptitle("Análise Clássica de Itens — P05", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura19_item_analysis.png", dpi=200, bbox_inches="tight")
print("✅ Figura 19 salva: resultados/figura19_item_analysis.png")
plt.close()

print("\n" + "=" * 70)
print("CONCLUSÕES")
print("=" * 70)
print(f"""
Análise Clássica de Itens (P05):

Amostra: N={n}
Itens: {n_itens}
Alpha de Cronbach: {cronbach_full:.3f}

Itens problemáticos: {len(items_problema)}
Sugestão: remover {len(items_remover)} itens
Alpha após limpeza: ver cálculo

Aplicações:
  1. Calibração inicial de questionários
  2. Validação do BRIEF-2 adaptado para PT-BR
  3. Redução de carga para respondentes
  4. Aumento de precisão psicométrica
""")
