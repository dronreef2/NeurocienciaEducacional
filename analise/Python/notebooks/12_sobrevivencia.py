"""
from neurociencia_edu.stats import kaplan_meier
12_sobrevivencia.py
Análise de Sobrevivência (Kaplan-Meier + Cox) — aplicação para P05

Pergunta: quanto tempo até a criança atingir um critério de letramento?
          Quais fatores predizem isso?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("  ANÁLISE DE SOBREVIVÊNCIA — P05 (TEMPO ATÉ CRITÉRIO)")
print("=" * 70)

# ============================================================
# 1. Simular dados
# ============================================================
print("\n1. Simulando dados de coorte...")

np.random.seed(42)
n = 200

# Covariáveis
sexo = np.random.choice([0, 1], n)
ses = np.random.normal(0, 1, n)
uso_ia = np.random.normal(0, 1, n)  # uso médio de IA
baseline_fe = np.random.normal(50, 10, n)

# Tempo até critério (em meses desde T1)
# Hazard depende de FE baseline e uso de IA
log_hazard = -0.5 + 0.3 * sexo - 0.4 * ses - 0.2 * uso_ia - 0.05 * (baseline_fe - 50)
hazard = np.exp(log_hazard)

# Tempo até evento (censura = não atingiu até T5)
time = np.random.exponential(1/hazard)
censored = (time > 50) | (np.random.rand(n) < 0.20)  # 5 anos OU dropout
time_obs = np.where(censored, 50, np.minimum(time, 50))
evento = (~censored).astype(int)  # 1 = atingiu, 0 = censurado

df = pd.DataFrame({
    "child_id": range(1, n+1),
    "sexo": sexo,
    "ses": ses,
    "uso_ia": uso_ia,
    "baseline_fe": baseline_fe,
    "tempo": time_obs,
    "evento": evento,
})

print(f"  N = {n}")
print(f"  Eventos (atingiu critério): {df['evento'].sum()} ({df['evento'].mean()*100:.1f}%)")
print(f"  Censurados: {(df['evento']==0).sum()}")
print(f"  Tempo médio: {df['tempo'].mean():.1f} meses")
print(f"  Tempo mediano: {df['tempo'].median():.1f} meses")

# ============================================================
# 2. Kaplan-Meier
# ============================================================
print("\n" + "=" * 70)
print("2. Curva de Kaplan-Meier")
print("=" * 70)

def kaplan_meier(tempos, eventos):
    """Calcula estimador Kaplan-Meier."""
    dados = sorted(zip(tempos, eventos))
    n = len(dados)
    sobrevive = []
    t_unique = sorted(set(tempos))
    surv_at = 1.0
    risco = n

    for t in t_unique:
        # Eventos neste tempo
        n_eventos_t = sum(1 for tm, ev in dados if tm == t and ev == 1)
        n_cens_t = sum(1 for tm, ev in dados if tm == t and ev == 0)
        if risco > 0:
            surv_at *= (1 - n_eventos_t / risco)
        sobrevive.append(surv_at)
        risco -= (n_eventos_t + n_cens_t)

    return np.array(t_unique), np.array(sobrevive)

# KM global
t_km, s_km = kaplan_meier(df["tempo"].values, df["evento"].values)

# Por sexo
t_m, s_m = kaplan_meier(
    df[df["sexo"]==1]["tempo"].values,
    df[df["sexo"]==1]["evento"].values
)
t_f, s_f = kaplan_meier(
    df[df["sexo"]==0]["tempo"].values,
    df[df["sexo"]==0]["evento"].values
)

print(f"  Sobrevida em 12 meses: {s_km[np.argmin(abs(t_km-12))]:.3f}" if any(t==12 for t in t_km) else f"  Tempo mínimo: {t_km[0]:.0f} meses")
print(f"  Sobrevida em 24 meses: {s_km[np.argmin(abs(t_km-24))]:.3f}" if any(t==24 for t in t_km) else "  N/A")
print(f"  Mediana de tempo: {df['tempo'].median():.1f} meses")

# Log-rank test (simplificado)
def logrank_test(tempos1, eventos1, tempos2, eventos2):
    """Log-rank test simplificado."""
    all_times = sorted(set(tempos1) | set(tempos2))
    O1 = E1 = V = 0
    n1 = len(tempos1)
    n2 = len(tempos2)
    for t in all_times:
        d1 = sum(1 for tm, ev in zip(tempos1, eventos1) if tm == t and ev == 1)
        d2 = sum(1 for tm, ev in zip(tempos2, eventos2) if tm == t and ev == 1)
        n1_t = sum(1 for tm in tempos1 if tm >= t)
        n2_t = sum(1 for tm in tempos2 if tm >= t)
        n_t = n1_t + n2_t
        if n_t > 1:
            d_t = d1 + d2
            e1 = d_t * n1_t / n_t
            v = (n1_t * n2_t * d_t * (n_t - d_t)) / (n_t * n_t * (n_t - 1)) if n_t > 1 else 0
            O1 += d1
            E1 += e1
            V += v
    if V > 0:
        chi2 = (O1 - E1)**2 / V
        return chi2
    return 0

chi2 = logrank_test(
    df[df["sexo"]==1]["tempo"].values,
    df[df["sexo"]==1]["evento"].values,
    df[df["sexo"]==0]["tempo"].values,
    df[df["sexo"]==0]["evento"].values
)
print(f"  Log-rank test: χ² = {chi2:.2f}")
print(f"  Mediana sexo=1: {df[df['sexo']==1]['tempo'].median():.1f} meses")
print(f"  Mediana sexo=0: {df[df['sexo']==0]['tempo'].median():.1f} meses")

# ============================================================
# 3. Cox Proportional Hazards
# ============================================================
print("\n" + "=" * 70)
print("3. Modelo de Cox (proportional hazards)")
print("=" * 70)

# Implementação simplificada via log-likelihood
def cox_log_likelihood(params, X, tempos, eventos):
    """NLL do modelo de Cox."""
    n, p = X.shape
    beta = params
    linear_pred = X @ beta

    # Breslow estimator
    ordem = np.argsort(-tempos)
    tempos_s = tempos[ordem]
    eventos_s = eventos[ordem]
    X_s = X[ordem]
    lp_s = linear_pred[ordem]

    ll = 0
    for i in range(n):
        if eventos_s[i] == 1:
            risk_set = np.exp(lp_s[:i+1])
            ll += lp_s[i] - np.log(risk_set.sum())
    return -ll

from scipy.optimize import minimize

X = df[["sexo", "ses", "uso_ia", "baseline_fe"]].values
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)

try:
    result = minimize(
        cox_log_likelihood,
        np.zeros(X.shape[1]),
        args=(X_scaled, df["tempo"].values, df["evento"].values),
        method="BFGS",
        options={"maxiter": 100}
    )
    beta_est = result.x / X.std(axis=0)  # voltar para escala original

    print(f"  Convergência: {'OK' if result.success else 'FALHOU'}")
    print(f"\n  Coeficientes (HR = exp(β)):")
    vars_names = ["sexo", "ses", "uso_ia", "baseline_fe"]
    for var, b in zip(vars_names, beta_est):
        hr = np.exp(b)
        print(f"    {var:<15}: β = {b:+.3f}, HR = {hr:.3f}")
except Exception as e:
    print(f"  Erro: {e}")
    beta_est = None

# ============================================================
# 4. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("4. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel A: Curva KM
ax = axes[0, 0]
ax.step(t_km, s_km, where="post", linewidth=2.5, color="#667eea", label="Geral")
ax.step(t_m, s_m, where="post", linewidth=2, color="#3498db", label="Sexo=M", linestyle="--")
ax.step(t_f, s_f, where="post", linewidth=2, color="#e74c3c", label="Sexo=F", linestyle=":")
ax.fill_between(t_km, s_km - 0.05, s_km + 0.05, alpha=0.2, color="#667eea")
ax.set_xlabel("Meses desde T1")
ax.set_ylabel("Probabilidade de NÃO atingir critério")
ax.set_title("Curva de Kaplan-Meier", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)

# Painel B: Hazard ratios
ax = axes[0, 1]
if beta_est is not None:
    hrs = np.exp(beta_est)
    colors = ["#27ae60" if hr < 1 else "#e74c3c" for hr in hrs]
    bars = ax.barh(vars_names, hrs, color=colors, edgecolor="black")
    ax.axvline(1, color="black", linestyle="--", linewidth=1.5)
    ax.set_xlabel("Hazard Ratio")
    ax.set_title("Hazard Ratios (Cox)\n< 1 = protetor, > 1 = risco", fontweight="bold")
    for bar, hr in zip(bars, hrs):
        ax.text(hr + 0.02 if hr < 1 else hr + 0.02, bar.get_y() + bar.get_height()/2,
                f"{hr:.2f}", va="center", fontweight="bold")
    ax.grid(True, axis="x", alpha=0.3)
else:
    ax.text(0.5, 0.5, "Cox não convergiu", ha="center")

# Painel C: Eventos no tempo
ax = axes[1, 0]
df_sorted = df.sort_values("tempo")
event_times = df_sorted[df_sorted["evento"]==1]["tempo"]
ax.hist([df[df["evento"]==1]["tempo"], df[df["evento"]==0]["tempo"]],
        bins=20, label=["Evento", "Censurado"],
        color=["#e74c3c", "#95a5a6"], edgecolor="black")
ax.set_xlabel("Meses")
ax.set_ylabel("Frequência")
ax.set_title("Distribuição de tempos\n(evento vs censura)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel D: Predição por nível de uso de IA
ax = axes[1, 1]
for uso_label, color in [("Baixo", "#3498db"), ("Alto", "#e67e22")]:
    mask = (df["uso_ia"] > 0.5) if uso_label == "Alto" else (df["uso_ia"] < -0.5)
    sub = df[mask]
    t_sub, s_sub = kaplan_meier(sub["tempo"].values, sub["evento"].values)
    ax.step(t_sub, s_sub, where="post", linewidth=2, color=color, label=f"Uso IA {uso_label}")
ax.set_xlabel("Meses")
ax.set_ylabel("Sobrevida")
ax.set_title("KM por nível de uso de IA\n(alto vs baixo)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)

plt.suptitle("Análise de Sobrevivência — P05", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura18_sobrevivencia.png", dpi=200, bbox_inches="tight")
print("✅ Figura 18 salva: resultados/figura18_sobrevivencia.png")
plt.close()

print("\n" + "=" * 70)
print("CONCLUSÕES")
print("=" * 70)
print(f"""
Análise de Sobrevivência (P05):

População: N={n} crianças
Eventos: {df['evento'].sum()} atingiram critério de letramento
Censurados: {(df['evento']==0).sum()} (não atingiram em 5 anos OU dropout)
Tempo mediano: {df['tempo'].median():.1f} meses

Aplicações para P05:
  1. Análise de tempo até critério de letramento
  2. Análise de retenção na coorte (attrition)
  3. Identificação de preditores precoces de risco
  4. Plano de intervenções adaptativas
""")
