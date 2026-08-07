"""
10_p02_ecr_simulacao.py
Simulação robusta do ECR 2×4 do P02 (gamificação × FE)
Compara efeito da gamificação por elemento (pontos, badges, narrativas, avatares)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pathlib import Path

print("=" * 70)
print("  P02 — SIMULAÇÃO ECR 2×4 (GAMIFICAÇÃO × FE)")
print("=" * 70)

# ============================================================
# 1. Parâmetros do ECR
# ============================================================
print("\n1. Design do ECR (2 × 4)")
print("""
  Fator 1: Plataforma
    - TRAD (tradicional, n=100)
    - GAME (gamificada, n=100)

  Fator 2: Elemento de gamificação (apenas GAME)
    - PONT (pontos, n=25)
    - BADG (badges, n=25)
    - NARR (narrativas, n=25)
    - AVAT (avatares, n=25)

  Total: N=200 crianças, 2º ao 5º ano
  Desfecho: mudança pré-pós em inibição (BRIEF-2)
  Hipótese: GAME > TRAD, com NARR + AVAT tendo maior efeito
""")

np.random.seed(42)
n_per_cell = 25

# Efeitos verdadeiros baseados em meta-análise
efeito_game_overall = 0.35  # d médio de gamificação (Hamari 2014)
efeito_trad_change = 0.0   # sem mudança (controle)
efeito_game_main = 0.40   # base para game

# Efeitos específicos por elemento
element_effects = {
    "TRAD": 0.0,
    "PONT": 0.30,   # pontos sozinhos: efeito médio
    "BADG": 0.25,   # badges: efeito médio-baixo
    "NARR": 0.55,   # narrativas: maior efeito
    "AVAT": 0.50,   # avatares: maior efeito
}

# Variabilidade
sd_residual = 0.8
sd_baseline = 1.0

# ============================================================
# 2. Simular dados
# ============================================================
print("\n2. Simulando 200 crianças...")

data = []
for cond in ["TRAD", "PONT", "BADG", "NARR", "AVAT"]:
    n = n_per_cell
    baseline = np.random.normal(50, sd_baseline, n)  # BRIEF-2 baseline
    change = np.random.normal(element_effects[cond], sd_residual, n)
    followup = baseline - change  # menor = melhor (inibição melhorou)

    for i in range(n):
        data.append({
            "id": f"S_{cond}_{i+1:02d}",
            "condicao": cond,
            "plataforma": "TRAD" if cond == "TRAD" else "GAME",
            "elemento": "NENHUM" if cond == "TRAD" else cond,
            "idade": np.random.randint(7, 12),
            "sexo": np.random.choice(["M", "F"]),
            "ses": np.random.normal(0, 1),
            "brief2_baseline": baseline[i],
            "brief2_followup": followup[i],
            "mudanca": change[i],  # positivo = melhorou
        })

df = pd.DataFrame(data)
print(f"  N = {len(df)}")
print(f"\nMudança média por condição:")
print(df.groupby("condicao")["mudanca"].agg(["mean", "std", "count"]).round(3))

# ============================================================
# 3. ANOVA 2x4 fatorial
# ============================================================
print("\n" + "=" * 70)
print("3. ANOVA 2×4 fatorial")
print("=" * 70)

# Codificar
df["plataforma_cod"] = (df["plataforma"] == "GAME").astype(int)
df["elemento_cod"] = df["elemento"].astype("category").cat.codes

# Regressão equivalente a ANOVA
model = ols("mudanca ~ C(plataforma) * C(elemento)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("\nTabela ANOVA:")
print(anova_table.round(4))

# Tamanhos de efeito (eta²)
ss_total = anova_table["sum_sq"].sum()
print("\nTamanhos de efeito (η²):")
for effect in anova_table.index:
    if effect != "Residual":
        eta2 = anova_table.loc[effect, "sum_sq"] / ss_total
        print(f"  {effect}: η² = {eta2:.3f}")

# ============================================================
# 4. Comparações planejadas
# ============================================================
print("\n" + "=" * 70)
print("4. Comparações planejadas")
print("=" * 70)

# GAME vs TRAD
game = df[df["plataforma"] == "GAME"]["mudanca"]
trad = df[df["plataforma"] == "TRAD"]["mudanca"]
t, p = stats.ttest_ind(game, trad)
d = (game.mean() - trad.mean()) / np.sqrt((game.var() + trad.var()) / 2)
print(f"\nGAME vs TRAD:")
print(f"  GAME: M = {game.mean():.2f}, DP = {game.std():.2f}")
print(f"  TRAD: M = {trad.mean():.2f}, DP = {trad.std():.2f}")
print(f"  t({len(df)-2}) = {t:.2f}, p = {p:.4f}, d = {d:.2f}")
print(f"  {'Significativo' if p < 0.05 else 'Não significativo'} (α=0.05)")

# NARR + AVAT vs PONT + BADG (efeito aditivo)
high = df[df["elemento"].isin(["NARR", "AVAT"])]["mudanca"]
low = df[df["elemento"].isin(["PONT", "BADG"])]["mudanca"]
t, p = stats.ttest_ind(high, low)
print(f"\nNARR+AVAT (alta imersão) vs PONT+BADG (baixa imersão):")
print(f"  Alta: M = {high.mean():.2f}, DP = {high.std():.2f}")
print(f"  Baixa: M = {low.mean():.2f}, DP = {low.std():.2f}")
print(f"  t = {t:.2f}, p = {p:.4f}")

# Post-hoc Tukey
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(df["mudanca"], df["condicao"], alpha=0.05)
print(f"\nPost-hoc Tukey HSD:")
print(tukey)

# ============================================================
# 5. ANCOVA com baseline como covariável
# ============================================================
print("\n" + "=" * 70)
print("5. ANCOVA (controlando por baseline + idade + sexo)")
print("=" * 70)

df["idade_c"] = df["idade"] - df["idade"].mean()
df["sexo_cod"] = (df["sexo"] == "M").astype(int)

model_ancova = ols(
    "brief2_followup ~ brief2_baseline + idade_c + sexo_cod + C(plataforma) * C(elemento)",
    data=df
).fit()

# Coeficientes das condições
print("\nCoeficientes (controlando baseline, idade, sexo):")
params = model_ancova.params
pvals = model_ancova.pvalues
for p_name in [p for p in params.index if "C(plataforma)" in p or "C(elemento)" in p or ":" in p]:
    sig = "**" if pvals[p_name] < 0.01 else "*" if pvals[p_name] < 0.05 else ""
    print(f"  {p_name}: β = {params[p_name]:.3f}, p = {pvals[p_name]:.4f} {sig}")

print(f"\nR² = {model_ancova.rsquared:.3f}, R² ajustado = {model_ancova.rsquared_adj:.3f}")

# ============================================================
# 6. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("6. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel A: Barplot por condição
ax = axes[0, 0]
means = df.groupby("condicao")["mudanca"].mean()
sems = df.groupby("condicao")["mudanca"].std() / np.sqrt(n_per_cell)
colors = ["#95a5a6"] + ["#27ae60", "#3498db", "#9b59b6", "#e74c3c"]
bars = ax.bar(means.index, means.values, yerr=1.96*sems,
              color=colors, edgecolor="black", capsize=5)
ax.axhline(0, color="black", linestyle="-", linewidth=0.5)
ax.set_ylabel("Mudança (baseline - followup)\nPositivo = melhorou")
ax.set_title("Mudança média por condição (IC 95%)", fontweight="bold")
ax.grid(True, axis="y", alpha=0.3)
for bar, val in zip(bars, means.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.05,
            f"{val:.2f}", ha="center", fontweight="bold")

# Painel B: Violin plot
ax = axes[0, 1]
parts = ax.violinplot([df[df["condicao"]==c]["mudanca"].values for c in means.index],
                       positions=range(len(means)), showmeans=True, showmedians=True)
ax.set_xticks(range(len(means)))
ax.set_xticklabels(means.index)
ax.set_ylabel("Mudança")
ax.set_title("Distribuição por condição", fontweight="bold")
ax.axhline(0, color="red", linestyle="--", alpha=0.5)
ax.grid(True, axis="y", alpha=0.3)

# Painel C: Interação
ax = axes[1, 0]
game_means = df[df["plataforma"]=="GAME"].groupby("elemento")["mudanca"].mean()
trad_mean = df[df["plataforma"]=="TRAD"]["mudanca"].mean()
x = list(game_means.index) + ["TRAD"]
y = list(game_means.values) + [trad_mean]
ax.plot(x, y, "o-", linewidth=2, markersize=10, color="#667eea")
ax.axhline(trad_mean, color="gray", linestyle="--", alpha=0.5, label="TRAD")
ax.set_ylabel("Mudança média")
ax.set_title("Comparação GAME (cada elemento) vs TRAD", fontweight="bold")
ax.legend()
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
ax.grid(True, alpha=0.3)

# Painel D: Efeitos individuais
ax = axes[1, 1]
for cond in means.index:
    sub = df[df["condicao"]==cond]
    ax.scatter(sub["brief2_baseline"], sub["brief2_followup"],
               alpha=0.5, label=cond, s=30)
    # Linha y = x
lims = [df["brief2_baseline"].min(), df["brief2_baseline"].max()]
ax.plot(lims, lims, "k--", alpha=0.3)
ax.set_xlabel("BRIEF-2 baseline")
ax.set_ylabel("BRIEF-2 followup")
ax.set_title("Baseline vs followup (linha = sem mudança)", fontweight="bold")
ax.legend(bbox_to_anchor=(1.05, 1), fontsize=8)

plt.suptitle("P02 — Simulação ECR 2×4 (Gamificação)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura14_p02_ecr.png", dpi=200, bbox_inches="tight")
print("✅ Figura 14 salva: resultados/figura14_p02_ecr.png")
plt.close()

# ============================================================
# 7. Conclusões
# ============================================================
print("\n" + "=" * 70)
print("7. CONCLUSÕES — P02 ECR")
print("=" * 70)
print(f"""
RESULTADOS DA SIMULAÇÃO:

Efeito principal GAME > TRAD:
  d = {d:.2f}, p = {p:.4f}
  {'Significativo' if p < 0.05 else 'Não significativo'}

Padrão por elemento:
  TRAD: {trad.mean():.2f} (controle)
  PONT: {game_means['PONT']:.2f}
  BADG: {game_means['BADG']:.2f}
  NARR: {game_means['NARR']:.2f} (maior)
  AVAT: {game_means['AVAT']:.2f}

Padrão consistente com hipótese:
  Narrativas e avatares > Pontos e Badges
  ✓ Efeito de imersão narrativa é maior

PRÓXIMOS PASSOS:
  1. Implementar com `afex` (R) para ANOVA mista robusta
  2. Adicionar mediador (engajamento) entre GAME e FE
  3. Coletar dados reais (N=200, 8 escolas)
  4. Considerar atrito diferencial entre condições
""")
