"""Página 5: P04 - SEM (IA e FE)"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="P04 - SEM (IA × FE)", page_icon="📈", layout="wide")

st.markdown("# 📈 P04 — IA Generativa e Funções Executivas")
st.markdown("### *Modelagem de Equações Estruturais (SEM) — N=300-500*")
st.markdown("---")

# Carregar dados
data_path = Path("/workspace/dados_sinteticos/P04_dados_sinteticos.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
else:
    np.random.seed(42)
    n = 400
    df = pd.DataFrame({
        "respondente_id": range(1, n + 1),
        "ia_uso": np.random.uniform(0, 10, n),
        "engajamento": np.random.uniform(0, 10, n),
        "fe_inibicao": np.random.uniform(0, 10, n),
        "fe_memoria": np.random.uniform(0, 10, n),
        "fe_flexibilidade": np.random.uniform(0, 10, n),
        "letramento_pais": np.random.uniform(0, 10, n),
        "sexo": np.random.choice(["M", "F"], n),
        "idade": np.random.choice([7, 8, 9, 10, 11], n),
    })

# Filtros
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    sexos = st.multiselect("Sexo:", df["sexo"].unique(), default=list(df["sexo"].unique()))
    idade_range = st.slider("Idade:", 7, 11, (7, 11))

df_f = df[(df["sexo"].isin(sexos)) & (df["idade"].between(*idade_range))]

# Modelo conceitual
st.markdown("## 🔗 Modelo Conceitual")
st.markdown("""
```
Uso de IA (X) ──a──> Engajamento (M) ──b──> FE (Y)
   │                                              ↑
   └─────────────c' (direto)──────────────────────┤
   │                                              │
   └──────W×X (moderação por letramento pais)────┘
```
""")

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("N filtrado", len(df_f))
with col2:
    st.metric("Uso IA médio", f"{df_f['ia_uso'].mean():.2f}")
with col3:
    st.metric("Engajamento médio", f"{df_f['engajamento'].mean():.2f}")
with col4:
    st.metric("FE inibição média", f"{df_f['fe_inibicao'].mean():.2f}")

# Correlações
st.markdown("## 📊 Matriz de Correlações")
corr_vars = ["ia_uso", "engajamento", "fe_inibicao", "fe_memoria", "fe_flexibilidade", "letramento_pais"]
corr = df_f[corr_vars].corr()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_vars)))
ax.set_yticks(range(len(corr_vars)))
ax.set_xticklabels(corr_vars, rotation=45, ha="right")
ax.set_yticklabels(corr_vars)
for i in range(len(corr_vars)):
    for j in range(len(corr_vars)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
plt.colorbar(im, ax=ax, label="Correlação de Pearson")
ax.set_title("Matriz de correlações", fontweight="bold")
plt.tight_layout()
st.pyplot(fig)

# Scatter plots
st.markdown("## 📈 Relações-chave")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# IA -> Engajamento
axes[0].scatter(df_f["ia_uso"], df_f["engajamento"], alpha=0.5, color="blue")
axes[0].set_xlabel("Uso de IA (X)")
axes[0].set_ylabel("Engajamento (M)")
axes[0].set_title("X → M (path a)", fontweight="bold")

# Engajamento -> FE
axes[1].scatter(df_f["engajamento"], df_f["fe_inibicao"], alpha=0.5, color="green")
axes[1].set_xlabel("Engajamento (M)")
axes[1].set_ylabel("FE Inibição (Y)")
axes[1].set_title("M → Y (path b)", fontweight="bold")

# IA -> FE
axes[2].scatter(df_f["ia_uso"], df_f["fe_inibicao"], alpha=0.5, color="red")
axes[2].set_xlabel("Uso de IA (X)")
axes[2].set_ylabel("FE Inibição (Y)")
axes[2].set_title("X → Y (path c')", fontweight="bold")

for ax in axes:
    ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

# Hipóteses SEM
st.markdown("## 🎯 Hipóteses SEM")
st.markdown("""
| H | Caminho | Coef. esperado | IC 95% |
|---|---|---|---|
| H4.1 | a (X→M) | 0.30 | [0.20, 0.40] |
| H4.2 | b (M→Y) | 0.40 | [0.30, 0.50] |
| H4.3 | c' (X→Y direto) | 0.15 | [0.00, 0.20] |
| H4.4 | Indireto (a×b) | 0.12 | [0.06, 0.18] |
| H4.5 | W×X (moderação) | 0.15 | [0.05, 0.25] |
""")

# Download
st.markdown("## 📥 Exportar")
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV (filtrado)",
    data=csv,
    file_name="P04_dados_filtrados.csv",
    mime="text/csv",
)
