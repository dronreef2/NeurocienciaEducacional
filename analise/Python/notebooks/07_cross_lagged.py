"""
07_cross_lagged.py
Cross-Lagged Panel Model (CLPM) — P05
Análise de relações bidirecionais longitudinais entre variáveis
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.regression.mixed_linear_model import MixedLM

np.random.seed(42)
print("=" * 60)
print("  CROSS-LAGGED PANEL MODEL (CLPM) — P05")
print("=" * 60)

# ============================================================
# 1. Simular dados longitudinais bidirecionais
# ============================================================
print("\n1. Simulando dados P05 (5 ondas, N=200)...")

n = 200
n_waves = 5
wave_ids = np.tile(np.arange(n_waves), n)
child_ids = np.repeat(np.arange(n), n_waves)

# Constrói série temporal com cross-lag
# X (uso IA) influencia Y (FE) na onda seguinte e vice-versa

# Initialize
X = np.zeros(n * n_waves)
Y = np.zeros(n * n_waves)

# Set T1 (baseline)
X[wave_ids == 0] = np.random.normal(0, 1, n)
Y[wave_ids == 0] = 0.3 * X[wave_ids == 0] + np.random.normal(0, 1, n)

# Generate subsequent waves
for t in range(1, n_waves):
    mask_t = wave_ids == t
    mask_prev = wave_ids == (t - 1)

    # X_t = 0.5 * X_{t-1} + 0.2 * Y_{t-1} + ruido  (efeito cross-lag de Y em X)
    X[mask_t] = (
        0.5 * X[mask_prev]
        + 0.2 * Y[mask_prev]
        + np.random.normal(0, 0.5, n)
    )

    # Y_t = 0.3 * X_{t-1} + 0.5 * Y_{t-1} + ruido  (efeito cross-lag de X em Y)
    Y[mask_t] = (
        0.3 * X[mask_prev]
        + 0.5 * Y[mask_prev]
        + np.random.normal(0, 0.5, n)
    )

df = pd.DataFrame({
    "child_id": child_ids,
    "wave": wave_ids,
    "X_uso_ia": X,
    "Y_fe": Y,
})

print(f"  N observações: {len(df)}")
print(f"  N crianças: {df['child_id'].nunique()}")
print(f"  N ondas: {df['wave'].nunique()}")
print(df.head(10))

# ============================================================
# 2. Correlação cross-sectional
# ============================================================
print("\n2. Correlações cross-sectional por onda:")
for t in range(n_waves):
    sub = df[df["wave"] == t]
    r = sub["X_uso_ia"].corr(sub["Y_fe"])
    print(f"  T{t+1}: r = {r:.3f}")

# ============================================================
# 3. CLPM simplificado (wave-to-wave)
# ============================================================
print("\n3. CLPM — Regressões cruzadas (wave-to-wave):")
print("=" * 50)

results_clpm = []
for t in range(1, n_waves):
    sub_t = df[df["wave"] == t].set_index("child_id")
    sub_prev = df[df["wave"] == (t - 1)].set_index("child_id")

    # Juntar X_{t-1}, Y_{t-1} com X_t, Y_t
    panel = sub_t[["X_uso_ia", "Y_fe"]].join(
        sub_prev[["X_uso_ia", "Y_fe"]],
        rsuffix="_prev"
    )

    # Regressão 1: X_t = b0 + b1*X_{t-1} + b2*Y_{t-1} (efeito cross-lag Y->X)
    X_lag_Y = sm.OLS(
        panel["X_uso_ia"],
        sm.add_constant(panel[["X_uso_ia_prev", "Y_fe_prev"]])
    ).fit()
    print(f"\n  Onda T{t}->T{t+1}: X_t ~ X_{{t-1}} + Y_{{t-1}}")
    print(f"    Y_{{t-1}} -> X_t: β = {X_lag_Y.params['Y_fe_prev']:.3f}, p = {X_lag_Y.pvalues['Y_fe_prev']:.4f}")

    # Regressão 2: Y_t = b0 + b1*X_{t-1} + b2*Y_{t-1} (efeito cross-lag X->Y)
    Y_lag_X = sm.OLS(
        panel["Y_fe"],
        sm.add_constant(panel[["X_uso_ia_prev", "Y_fe_prev"]])
    ).fit()
    print(f"  Onda T{t}->T{t+1}: Y_t ~ X_{{t-1}} + Y_{{t-1}}")
    print(f"    X_{{t-1}} -> Y_t: β = {Y_lag_X.params['X_uso_ia_prev']:.3f}, p = {Y_lag_X.pvalues['X_uso_ia_prev']:.4f}")

    results_clpm.append({
        "wave": t + 1,
        "cross_lag_Y_to_X": X_lag_Y.params["Y_fe_prev"],
        "cross_lag_Y_to_X_p": X_lag_Y.pvalues["Y_fe_prev"],
        "cross_lag_X_to_Y": Y_lag_X.params["X_uso_ia_prev"],
        "cross_lag_X_to_Y_p": Y_lag_X.pvalues["X_uso_ia_prev"],
    })

# ============================================================
# 4. Média dos coeficientes cross-lag
# ============================================================
print("\n4. Média dos efeitos cross-lag (entre todas as transições):")
df_clpm = pd.DataFrame(results_clpm)
print(f"  Y -> X: β_médio = {df_clpm['cross_lag_Y_to_X'].mean():.3f} "
      f"(p médio = {df_clpm['cross_lag_Y_to_X_p'].mean():.4f})")
print(f"  X -> Y: β_médio = {df_clpm['cross_lag_X_to_Y'].mean():.3f} "
      f"(p médio = {df_clpm['cross_lag_X_to_Y_p'].mean():.4f})")

# ============================================================
# 5. Visualização
# ============================================================
print("\n5. Gerando visualização...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Painel A: Coeficientes por onda
ax = axes[0]
ax.errorbar(
    df_clpm["wave"],
    df_clpm["cross_lag_Y_to_X"],
    yerr=df_clpm["cross_lag_Y_to_X_p"],
    marker="o", label="Y → X (FE→Uso IA)", capsize=5
)
ax.errorbar(
    df_clpm["wave"] + 0.1,
    df_clpm["cross_lag_X_to_Y"],
    yerr=df_clpm["cross_lag_X_to_Y_p"],
    marker="s", label="X → Y (Uso IA→FE)", capsize=5
)
ax.axhline(0, color="red", linestyle="--", alpha=0.5)
ax.set_xlabel("Onda de destino")
ax.set_ylabel("Coeficiente cross-lag")
ax.set_title("Efeitos cross-lag por onda (CLPM)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel B: Trajetórias médias
ax = axes[1]
mean_X = df.groupby("wave")["X_uso_ia"].mean()
mean_Y = df.groupby("wave")["Y_fe"].mean()
ax.plot(mean_X.index, mean_X.values, "o-", label="X (Uso IA)", linewidth=2, markersize=8)
ax.plot(mean_Y.index, mean_Y.values, "s-", label="Y (FE)", linewidth=2, markersize=8)
ax.set_xlabel("Onda")
ax.set_ylabel("Média")
ax.set_title("Trajetórias médias", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/figura8_clpm.png", dpi=200, bbox_inches="tight")
print("  Figura 8 salva: resultados/figura8_clpm.png")
plt.close()

# ============================================================
# 6. Conclusões
# ============================================================
print("\n" + "=" * 60)
print("CONCLUSÕES:")
print("=" * 60)

x_to_y = df_clpm["cross_lag_X_to_Y"].mean()
y_to_x = df_clpm["cross_lag_Y_to_X"].mean()

print(f"""
Cross-lagged panel model (CLPM) para P05:

EFEITO X → Y (Uso de IA → Função Executiva):
  β = {x_to_y:.3f}
  Interpretação: crianças que usam mais IA no tempo t tendem a ter
  {'maior' if x_to_y > 0 else 'menor'} FE no tempo t+1

EFEITO Y → X (FE → Uso de IA):
  β = {y_to_x:.3f}
  Interpretação: crianças com {'maior' if y_to_x > 0 else 'menor'} FE
  no tempo t tendem a usar {'mais' if y_to_x > 0 else 'menos'} IA no t+1

IMPLICAÇÕES PARA O MANUSCRITO P05:
1. Discutir direcionalidade das relações
2. Comparar com modelos de causalidade reversa
3. Usar Random-Intercept CLPM (RI-CLPM) para separar within/between
4. Considerar variáveis de confusão (idade, SES, escola)
""")
