"""Página 6: P05 - Coorte Longitudinal (LGCM)"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="P05 - Longitudinal (LGCM)", page_icon="📅", layout="wide")

st.markdown("# 📅 P05 — Coorte Longitudinal de Funções Executivas")
st.markdown("### *Latent Growth Curve Models (LGCM) — 5 ondas, 200 crianças*")
st.markdown("---")

# Carregar dados
data_path = Path("/workspace/dados_sinteticos/P05_dados_longitudinais_sinteticos.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
else:
    np.random.seed(42)
    rows = []
    for cid in range(1, 201):
        intercept = np.random.normal(0, 1)
        slope = np.random.normal(0.5, 0.2)
        for onda in range(5):
            fe = intercept + slope * onda + np.random.normal(0, 0.5)
            rows.append({
                "crianca_id": cid,
                "onda": onda + 1,
                "fe_inibicao": fe,
                "fe_memoria": fe + np.random.normal(0, 0.3),
                "fe_flexibilidade": fe + np.random.normal(0, 0.3),
                "idade": 7 + onda,
                "sexo": np.random.choice(["M", "F"]),
            })
    df = pd.DataFrame(rows)

# Filtros
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    onda_sel = st.multiselect("Onda:", [1, 2, 3, 4, 5], default=[1, 2, 3, 4, 5])
    sexos = st.multiselect("Sexo:", df["sexo"].unique(), default=list(df["sexo"].unique()))

df_f = df[(df["onda"].isin(onda_sel)) & (df["sexo"].isin(sexos))]

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("N crianças", df_f["crianca_id"].nunique())
with col2:
    st.metric("N observações", len(df_f))
with col3:
    st.metric("Ondas", df_f["onda"].nunique())
with col4:
    st.metric("Sexos", df_f["sexo"].nunique())

# Trajetórias
st.markdown("## 📈 Trajetórias de Desenvolvimento")

fig, ax = plt.subplots(figsize=(14, 6))
for cid in df_f["crianca_id"].unique()[:50]:  # 50 primeiras crianças
    sub = df_f[df_f["crianca_id"] == cid].sort_values("onda")
    ax.plot(sub["onda"], sub["fe_inibicao"], alpha=0.2, color="gray")

# Média por onda
mean_by_onda = df_f.groupby("onda")["fe_inibicao"].mean()
ax.plot(mean_by_onda.index, mean_by_onda.values, "o-", color="red", linewidth=3, markersize=10, label="Média")

ax.set_xlabel("Onda")
ax.set_ylabel("FE Inibição")
ax.set_title("Trajetórias individuais + média populacional", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# LGCM estimado
st.markdown("## 📐 Modelo de Crescimento (LGCM)")

# Estimar intercepto e slope médios
intercept_mean = df_f[df_f["onda"] == 1]["fe_inibicao"].mean()
onda_max = df_f["onda"].max()
fe_max = df_f[df_f["onda"] == onda_max]["fe_inibicao"].mean()
slope_est = (fe_max - intercept_mean) / (onda_max - 1)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Intercepto (média)", f"{intercept_mean:.2f}")
with col2:
    st.metric("Slope (crescimento/ano)", f"{slope_est:.2f}")
with col3:
    st.metric("Variação no intercepto", f"{df_f.groupby('crianca_id')['fe_inibicao'].first().std():.2f}")

# Hipóteses
st.markdown("## 🎯 Hipóteses do LGCM")
st.markdown("""
| H | Parâmetro | Esperado |
|---|---|---|
| H5.1 | Slope (β1) | +0.5 DP/ano |
| H5.2 | Var(Intercept) | > 0 |
| H5.3 | Var(Slope) | > 0 |
| H5.4 | Cov(Intercept,Slope) | < 0 (catch-up) |
""")

# Análise de sobrevivência simulada
st.markdown("## ⏱️ Análise de Sobrevivência (tempo até atingir critério)")

# Simular: 30% dos que não atingem critério por ano
np.random.seed(42)
event_times = np.random.exponential(scale=2, size=200)
event_times = np.minimum(event_times, 5)
event_observed = np.random.binomial(1, 0.7, size=200)

fig, ax = plt.subplots(figsize=(12, 5))
from neurociencia_edu.stats import kaplan_meier
km = kaplan_meier(event_times, event_observed)

ax.step(km["times"], km["survival_function"], where="post", linewidth=2)
ax.fill_between(km["times"], km["survival_function"], alpha=0.3)
ax.set_xlabel("Onda")
ax.set_ylabel("S(t) — Probabilidade de não atingir critério")
ax.set_title("Curva de Kaplan-Meier (tempo até atingir critério FE)", fontweight="bold")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.metric("Eventos", int(event_observed.sum()))
with col2:
    st.metric("Mediana", f"{km['median']:.2f} ondas" if km['median'] else "N/A")

# Download
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="P05_dados_longitudinais.csv",
    mime="text/csv",
)
