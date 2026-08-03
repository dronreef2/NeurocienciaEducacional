"""
05_bayesian_analysis.py
Versão executável do notebook Bayesian Analysis
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

np.random.seed(42)
print("Bibliotecas carregadas")

# 1. Simular dados
n = 200
X = np.random.gamma(shape=2, scale=5, size=n)
W = np.random.normal(5, 1.5, size=n)
M = 0.4 * X + 0.2 * W + np.random.normal(0, 1, size=n)
Y = 0.3 * X + 0.5 * M - 0.15 * W + np.random.normal(0, 1, size=n)

df = pd.DataFrame({"X_uso_ia": X, "M_engajamento": M, "Y_fe": Y, "W_letram": W})
print(f"\nN = {len(df)}")
print(df.describe())

# 2. OLS frequentista
X_mat = sm.add_constant(df[["X_uso_ia"]])
ols_M = sm.OLS(df["M_engajamento"], X_mat).fit()
print(f"\nOLS (M ~ X): beta_XM = {ols_M.params['X_uso_ia']:.3f}, p = {ols_M.pvalues['X_uso_ia']:.4f}")

XY_mat = sm.add_constant(df[["X_uso_ia", "M_engajamento"]])
ols_Y = sm.OLS(df["Y_fe"], XY_mat).fit()
print(f"OLS (Y ~ X + M):")
print(f"  beta_XY = {ols_Y.params['X_uso_ia']:.3f}, p = {ols_Y.pvalues['X_uso_ia']:.4f}")
print(f"  beta_MY = {ols_Y.params['M_engajamento']:.3f}, p = {ols_Y.pvalues['M_engajamento']:.4f}")

# 3. Aproximação Bayesiana via Bootstrap
print("\n=== APROXIMAÇÃO BAYESIANA (Bootstrap) ===")
n_boot = 2000
boot_results = []
for _ in range(n_boot):
    idx = np.random.choice(len(df), size=len(df), replace=True)
    boot_df = df.iloc[idx]
    ols_M_b = sm.OLS(boot_df["M_engajamento"], sm.add_constant(boot_df[["X_uso_ia"]])).fit()
    ols_Y_b = sm.OLS(boot_df["Y_fe"], sm.add_constant(boot_df[["X_uso_ia", "M_engajamento"]])).fit()
    indirect = ols_M_b.params["X_uso_ia"] * ols_Y_b.params["M_engajamento"]
    boot_results.append({
        "beta_XM": ols_M_b.params["X_uso_ia"],
        "beta_XY": ols_Y_b.params["X_uso_ia"],
        "beta_MY": ols_Y_b.params["M_engajamento"],
        "indirect": indirect,
        "total": ols_Y_b.params["X_uso_ia"] + indirect
    })

boot_df = pd.DataFrame(boot_results)
print("\nMédias posteriores (bootstrap):")
print(boot_df.mean())
print("\nIC 95% (percentis 2.5% e 97.5%):")
print(boot_df.quantile([0.025, 0.975]))

# 4. Probabilidade posterior
prob_indirect_positive = (boot_df["indirect"] > 0).mean()
print(f"\nP(indireto > 0) = {prob_indirect_positive:.3f}")

# 5. Visualização
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
params_to_plot = ["beta_XM", "beta_XY", "beta_MY", "indirect", "total"]
for i, param in enumerate(params_to_plot):
    ax = axes.flatten()[i]
    ax.hist(boot_df[param], bins=40, density=True, alpha=0.7, color="#667eea", edgecolor="black")
    ax.axvline(0, color="red", linestyle="--", linewidth=1.5)
    ax.axvline(boot_df[param].mean(), color="green", linestyle="--", linewidth=2,
               label=f"Média={boot_df[param].mean():.3f}")
    ax.set_title(param, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
axes.flatten()[5].axis("off")
plt.tight_layout()
plt.savefig("resultados/figura5_posteriores_bayes.png", dpi=200, bbox_inches="tight")
print("\n✅ Figura 5 salva: resultados/figura5_posteriores_bayes.png")
plt.close()

# Conclusão
print("\n=== CONCLUSÃO ===")
print(f"Efeito indireto (X→M→Y): {boot_df['indirect'].mean():.3f} [{boot_df['indirect'].quantile(0.025):.3f}, {boot_df['indirect'].quantile(0.975):.3f}]")
print(f"P(indireto > 0) = {prob_indirect_positive*100:.1f}%")
print(f"\nInterpretação: o efeito de mediação é {'plausível' if prob_indirect_positive > 0.9 else 'incerto' if prob_indirect_positive > 0.5 else 'improvável'}.")
