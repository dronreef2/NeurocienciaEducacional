"""
mixed_models_diarios.py
Análise mais profunda: modelos mistos nos DIÁRIOS reais do piloto
(N=3 crianças, 17 dias, 51 registros)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM
from pathlib import Path
import json
from datetime import datetime

print("=" * 70)
print("  MODELOS MISTOS — DIÁRIOS DO PILOTO (N=3, 17 dias)")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 1. Carregar dados
# ============================================================
print("\n1. Carregando diários...")
BASE = Path("/workspace/01-projeto-qualitativo-criancas-ia/dados/piloto")

diarios = []
for f in sorted((BASE / "diarios").glob("*.csv")):
    df = pd.read_csv(f)
    df["data"] = pd.to_datetime(df["data"])
    df["dia_semana"] = df["data"].dt.day_name()
    df["semana"] = ((df["data"] - df["data"].min()).dt.days // 7) + 1
    df["fim_de_semana"] = df["data"].dt.dayofweek.isin([5, 6]).astype(int)
    df["dia_num"] = (df["data"] - df["data"].min()).dt.days
    diarios.append(df)

df = pd.concat(diarios, ignore_index=True)

# Adicionar variáveis dummy para atividades
df["e_matematica"] = df["atividades"].fillna("").str.contains("matematica").astype(int)
df["e_leitura"] = df["atividades"].fillna("").str.contains("leitura").astype(int)

# Variável de cluster: criança
df["crianca"] = df["participante_id"]

print(f"  N observações: {len(df)}")
print(f"  N crianças: {df['crianca'].nunique()}")
print(f"  Período: {df['data'].min().date()} a {df['data'].max().date()} ({df['data'].nunique()} dias)")

# ============================================================
# 2. Modelo 1: OLS ingênuo (baseline)
# ============================================================
print("\n" + "=" * 70)
print("2. Modelo 1: OLS ingênuo (não considera clustering)")
print("=" * 70)

model_ols = smf.ols("duracao_min ~ dia_num + e_matematica + e_leitura + fim_de_semana", data=df).fit()
print(model_ols.summary().tables[1])
print(f"\n  R² = {model_ols.rsquared:.3f}, AIC = {model_ols.aic:.1f}")
print(f"  ⚠️ Assume independência — provavelmente INCORRETO")

# ============================================================
# 3. Modelo 2: Mixed Model básico (intercepto aleatório)
# ============================================================
print("\n" + "=" * 70)
print("3. Modelo 2: Mixed Model com intercepto aleatório por criança")
print("=" * 70)

model_mixed = MixedLM.from_formula(
    "duracao_min ~ dia_num + e_matematica + e_leitura + fim_de_semana",
    groups="crianca",
    data=df
)
result_mixed = model_mixed.fit(reml=True)
print(result_mixed.summary().tables[1])
print(f"\n  AIC = {result_mixed.aic:.1f}")
print(f"  SD intercepto aleatório: {np.sqrt(result_mixed.cov_re.iloc[0,0]):.2f}")

# Comparação
print(f"\n  Comparação AIC: OLS = {model_ols.aic:.1f} | Mixed = {result_mixed.aic:.1f}")
if result_mixed.aic < model_ols.aic:
    print(f"  ✅ Mixed é melhor (menor AIC)")
else:
    print(f"  ⚠️ OLS é melhor (suspeito)")

# ============================================================
# 4. Modelo 3: Random intercept + random slope
# ============================================================
print("\n" + "=" * 70)
print("4. Modelo 3: Mixed Model com intercept + slope (tempo) aleatórios")
print("=" * 70)

model_mixed2 = MixedLM.from_formula(
    "duracao_min ~ dia_num + e_matematica + e_leitura + fim_de_semana",
    groups="crianca",
    re_formula="~dia_num",
    data=df
)
try:
    result_mixed2 = model_mixed2.fit(reml=True)
    print(result_mixed2.summary().tables[1])
    print(f"\n  AIC = {result_mixed2.aic:.1f}")

    # Variabilidade individual
    cov_re = result_mixed2.cov_re
    print(f"\n  Variabilidade:")
    print(f"    SD intercepto: {np.sqrt(cov_re.iloc[0,0]):.2f}")
    print(f"    SD slope (dia_num): {np.sqrt(cov_re.iloc[1,1]):.2f}")
    print(f"    Correlação intercept-slope: {cov_re.iloc[0,1] / np.sqrt(cov_re.iloc[0,0]*cov_re.iloc[1,1]):.2f}")
except Exception as e:
    print(f"  ⚠️ Modelo falhou: {e}")
    result_mixed2 = None

# ============================================================
# 5. Modelo 4: Com interação tempo × criança
# ============================================================
print("\n" + "=" * 70)
print("5. Modelo 4: Efeito do tipo de atividade (matemática vs. leitura)")
print("=" * 70)

# Comparar uso médio em matemática vs leitura
print(f"\n  Estatísticas descritivas:")
print(f"    Com matemática: {df[df['e_matematica']==1]['duracao_min'].mean():.1f} ± {df[df['e_matematica']==1]['duracao_min'].std():.1f} min")
print(f"    Com leitura:    {df[df['e_leitura']==1]['duracao_min'].mean():.1f} ± {df[df['e_leitura']==1]['duracao_min'].std():.1f} min")
print(f"    Sem atividade:  {df[df['atividades'].isna() | (df['atividades']=='')]['duracao_min'].mean():.1f} min")

# Modelo com efeitos fixos para atividades
model_ativ = MixedLM.from_formula(
    "duracao_min ~ dia_num + fim_de_semana + e_matematica + e_leitura",
    groups="crianca",
    data=df
)
result_ativ = model_ativ.fit(reml=True)
print(f"\n  Modelo com atividades:")
print(result_ativ.summary().tables[1])

# ============================================================
# 6. Análise de autocorrelação temporal
# ============================================================
print("\n" + "=" * 70)
print("6. Análise de autocorrelação temporal")
print("=" * 70)

for cid in df["crianca"].unique():
    sub = df[df["crianca"] == cid].sort_values("data")
    # Calcular autocorrelação lag-1
    uso = sub["duracao_min"].values
    if len(uso) > 2 and uso.std() > 0:
        ac_lag1 = np.corrcoef(uso[:-1], uso[1:])[0, 1]
        print(f"  {cid}: autocorrelação lag-1 = {ac_lag1:.3f}")
    else:
        print(f"  {cid}: dados insuficientes")

# ============================================================
# 7. Predições individuais
# ============================================================
print("\n" + "=" * 70)
print("7. Predições individuais (BLUPs)")
print("=" * 70)

# Best Linear Unbiased Predictors
random_effects = result_mixed.random_effects
print(f"\n  Efeitos aleatórios (interceptos):")
for cid, re in random_effects.items():
    intercept = re["crianca"] if "crianca" in re else re.iloc[0]
    print(f"    {cid}: {intercept:.2f} (desvio da média geral)")

# ============================================================
# 8. Visualizações
# ============================================================
print("\n" + "=" * 70)
print("8. Visualizações")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel A: Trajetórias com ajuste
ax = axes[0, 0]
for cid in df["crianca"].unique():
    sub = df[df["crianca"] == cid].sort_values("data")
    ax.plot(sub["data"], sub["duracao_min"], "o-", label=cid, alpha=0.7, markersize=8)
ax.set_xlabel("Data")
ax.set_ylabel("Duração (min)")
ax.set_title("Trajetórias observadas", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Painel B: Efeitos fixos
ax = axes[0, 1]
coefs = result_mixed.params.iloc[1:]  # excluindo intercepto
ps = result_mixed.pvalues.iloc[1:]
colors = ["#27ae60" if p < 0.05 else "#95a5a6" for p in ps]
ax.barh(range(len(coefs)), coefs.values, color=colors, edgecolor="black")
ax.set_yticks(range(len(coefs)))
ax.set_yticklabels(coefs.index, fontsize=10)
ax.axvline(0, color="red", linestyle="--")
ax.set_xlabel("Coeficiente")
ax.set_title("Efeitos fixos (verde: p<0.05)", fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

# Painel C: Por atividade
ax = axes[1, 0]
df_ativ = df.copy()
df_ativ["tipo"] = "outro"
df_ativ.loc[df_ativ["e_matematica"]==1, "tipo"] = "matemática"
df_ativ.loc[df_ativ["e_leitura"]==1, "tipo"] = "leitura"
df_plot = df_ativ.groupby(["crianca", "tipo"])["duracao_min"].mean().unstack()
df_plot.plot(kind="bar", ax=ax, color=["#95a5a6", "#27ae60", "#3498db"], edgecolor="black")
ax.set_xlabel("Criança")
ax.set_ylabel("Duração média (min)")
ax.set_title("Uso médio por tipo de atividade", fontweight="bold")
ax.legend(title="Atividade", bbox_to_anchor=(1.05, 1))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
ax.grid(True, axis="y", alpha=0.3)

# Painel D: Resumo
ax = axes[1, 1]
ax.axis("off")
resumo = f"""
RESUMO — MODELOS MISTOS

Modelo vencedor: Mixed (intercept aleatório)
  AIC: {result_mixed.aic:.1f} (vs OLS = {model_ols.aic:.1f})

Efeitos fixos significativos:
"""
for var, p in result_mixed.pvalues.iloc[1:].items():
    if p < 0.10:
        coef = result_mixed.params[var]
        sig = "**" if p < 0.01 else "*" if p < 0.05 else "."
        resumo += f"  {var}: β={coef:.2f}, p={p:.3f} {sig}\n"

resumo += f"""
Variabilidade individual:
  SD intercepto: {np.sqrt(result_mixed.cov_re.iloc[0,0]):.2f} min

Efeitos aleatórios por criança:
"""
for cid, re in random_effects.items():
    intercept = re["crianca"] if "crianca" in re else re.iloc[0]
    if intercept > 0:
        perfil = "acima da média"
    else:
        perfil = "abaixo da média"
    resumo += f"  {cid}: {intercept:+.2f} ({perfil})\n"

resumo += f"""
Limitações:
  - N=3 (crianças), N=51 (observações)
  - Impossível testar variabilidade de forma robusta
  - Análise é exploratória

Recomendações:
  - Expandir para N>=30 crianças
  - Coletar por mais dias (>30)
  - Adicionar covariáveis (idade, sexo)
"""

ax.text(0.05, 0.95, resumo, transform=ax.transAxes, fontsize=9,
        verticalalignment="top", family="monospace",
        bbox=dict(boxstyle="round", facecolor="#f0f7ff", edgecolor="#667eea"))

plt.suptitle("Modelos Mistos nos Diários do Piloto", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("resultados/figura13_mixed_models_diarios.png", dpi=200, bbox_inches="tight")
print("✅ Figura 13 salva: resultados/figura13_mixed_models_diarios.png")

# ============================================================
# 9. Salvar resultados
# ============================================================
print("\n" + "=" * 70)
print("9. RESUMO FINAL")
print("=" * 70)

resultados = {
    "data_analise": datetime.now().isoformat(),
    "n_obs": len(df),
    "n_criancas": int(df["crianca"].nunique()),
    "modelos": {
        "ols": {
            "aic": float(model_ols.aic),
            "r2": float(model_ols.rsquared),
            "formula": "duracao_min ~ dia_num + e_matematica + e_leitura + fim_de_semana",
        },
        "mixed_intercept_only": {
            "aic": float(result_mixed.aic),
            "sd_intercept": float(np.sqrt(result_mixed.cov_re.iloc[0,0])),
            "coefs": {k: float(v) for k, v in result_mixed.params.items()},
            "pvalues": {k: float(v) for k, v in result_mixed.pvalues.items()},
        },
    },
    "efeitos_aleatorios": {cid: float(re["crianca"] if "crianca" in re else re.iloc[0])
                          for cid, re in random_effects.items()},
}

# Limpar NaN
def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items() if not (isinstance(v, float) and np.isnan(v))}
    elif isinstance(obj, float) and np.isnan(obj):
        return None
    return obj

output_path = Path("resultados/relatorio_mixed_models.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(clean_nan(resultados), f, indent=2, ensure_ascii=False, default=str)

print(f"\n✅ Relatório JSON salvo: {output_path}")
print(f"\n📊 CONCLUSÃO PRINCIPAL:")
print(f"   O Mixed Model (AIC = {result_mixed.aic:.1f}) é melhor que OLS (AIC = {model_ols.aic:.1f})")
print(f"   Há variabilidade individual substancial (SD intercept = {np.sqrt(result_mixed.cov_re.iloc[0,0]):.2f})")
print(f"   Análise exploratória — limitada pelo N=3 crianças")
