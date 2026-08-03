"""
06_mixed_effects_models.py
Versão executável do notebook Mixed Effects Models
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.mixed_linear_model import MixedLM

np.random.seed(42)
print("Bibliotecas carregadas")

# 1. Simular dados longitudinais P05
n_children = 200
n_waves = 5
n_schools = 10

child_ids = np.repeat(np.arange(n_children), n_waves)
wave_ids = np.tile(np.arange(n_waves), n_children)
school_ids = np.repeat(np.random.randint(0, n_schools, size=n_children), n_waves)
sexo = np.repeat(np.random.choice([0, 1], size=n_children, p=[0.5, 0.5]), n_waves)
ses = np.repeat(np.random.normal(0, 1, size=n_children), n_waves)
school_effect = np.repeat(np.random.normal(0, 0.5, size=n_schools), 20 * n_waves)[:n_children*n_waves]
child_intercept = np.repeat(np.random.normal(0, 1, size=n_children), n_waves)
child_slope = np.repeat(np.random.normal(0, 0.3, size=n_children), n_waves)
idade_c = wave_ids.astype(float) - 2

fe_score = (
    50
    + 2 * idade_c
    + child_intercept
    + child_slope * idade_c
    + 3 * ses
    + 1.5 * sexo
    + school_effect
    + np.random.normal(0, 2, size=n_children*n_waves)
)

df_long = pd.DataFrame({
    "child_id": child_ids,
    "wave": wave_ids,
    "school_id": school_ids,
    "idade_c": idade_c,
    "sexo": sexo,
    "ses": ses,
    "fe_score": fe_score,
})

print(f"\nN total: {len(df_long)}")
print(f"N crianças: {df_long['child_id'].nunique()}")
print(f"N escolas: {df_long['school_id'].nunique()}")
print(df_long.head())

# 2. OLS (ingênuo)
X_ols = sm.add_constant(df_long[["idade_c", "sexo", "ses"]])
ols_model = sm.OLS(df_long["fe_score"], X_ols).fit()
print("\n=== OLS (ingênuo) ===")
print(f"  idade_c: β = {ols_model.params['idade_c']:.3f}, p = {ols_model.pvalues['idade_c']:.4f}")
print(f"  ses: β = {ols_model.params['ses']:.3f}, p = {ols_model.pvalues['ses']:.4f}")
print(f"  sexo: β = {ols_model.params['sexo']:.3f}, p = {ols_model.pvalues['sexo']:.4f}")
print(f"  R² = {ols_model.rsquared:.3f}, AIC = {ols_model.aic:.1f}")

# 3. Mixed Model
print("\n=== Mixed Model (intercept + slope aleatórios) ===")
mixed_model = MixedLM.from_formula(
    "fe_score ~ idade_c + sexo + ses",
    groups="child_id",
    re_formula="~idade_c",
    data=df_long
)
mixed_result = mixed_model.fit(reml=True)
print(mixed_result.summary().tables[1])
print(f"\nAIC: OLS = {ols_model.aic:.1f} | Mixed = {mixed_result.aic:.1f}")
print(f"✓ Mixed-Effects {'melhor' if mixed_result.aic < ols_model.aic else 'pior'} (menor AIC = melhor)")

# 4. Three-level (escola > criança)
print("\n=== Three-level (escola como grupo) ===")
try:
    model_3l = MixedLM.from_formula(
        "fe_score ~ idade_c + sexo + ses",
        groups="school_id",
        re_formula="~idade_c",
        data=df_long
    )
    result_3l = model_3l.fit(reml=True)
    print(result_3l.summary().tables[1])
except Exception as e:
    print(f"Three-level falhou: {e}")

# 5. Visualização
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Trajetórias
ax = axes[0]
sample_children = np.random.choice(n_children, 30, replace=False)
for cid in sample_children:
    sub = df_long[df_long["child_id"] == cid].sort_values("wave")
    ax.plot(sub["idade_c"], sub["fe_score"], alpha=0.4, color="gray")
mean_traj = df_long.groupby("idade_c")["fe_score"].mean()
ax.plot(mean_traj.index, mean_traj.values, color="red", linewidth=3, label="Média geral")
ax.set_xlabel("Idade centralizada")
ax.set_ylabel("FE (inibição)")
ax.set_title("Trajetórias individuais (N=200)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Coeficientes
ax = axes[1]
params = mixed_result.params.iloc[1:]
colors = ["#27ae60" if p < 0.05 else "#95a5a6" for p in mixed_result.pvalues.iloc[1:]]
ax.barh(range(len(params)), params.values, color=colors, edgecolor="black")
ax.set_yticks(range(len(params)))
ax.set_yticklabels(params.index)
ax.axvline(0, color="red", linestyle="--")
ax.set_xlabel("Coeficiente")
ax.set_title("Efeitos fixos (verde = p<0.05)", fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/figura7_mixed_effects.png", dpi=200, bbox_inches="tight")
print("\n✅ Figura 7 salva: resultados/figura7_mixed_effects.png")
plt.close()

# Conclusões
print("\n=== CONCLUSÕES ===")
print(f"β_idade_c = {mixed_result.params['idade_c']:.3f} → Crescimento de {mixed_result.params['idade_c']:.2f} pts/ano")
print(f"β_ses = {mixed_result.params['ses']:.3f} → Efeito do SES")
print(f"SD intercepto aleatório = {mixed_result.cov_re.iloc[0,0]**0.5:.3f}")
print(f"SD slope aleatório = {mixed_result.cov_re.iloc[1,1]**0.5:.3f}")
print(f"\nVariabilidade individual: {'alta' if mixed_result.cov_re.iloc[0,0]**0.5 > 0.5 else 'moderada'}")
