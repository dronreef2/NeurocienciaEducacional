"""Página 3: P02 - Gamificação e FE (ECR)"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="P02 - Gamificação (ECR)", page_icon="🎮", layout="wide")

st.markdown("# 🎮 P02 — Gamificação e Funções Executivas")
st.markdown("### *Experimento Controlado Randomizado (2×4) — N=200*")
st.markdown("---")

# Carregar dados
data_path = Path("/workspace/dados_sinteticos/P02_dados_sinteticos.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
else:
    np.random.seed(42)
    df = pd.DataFrame({
        "participante_id": range(1, 201),
        "grupo": np.random.choice(["Controle", "Pontos", "Narrativa", "Pontos+Narrativa"], 200),
        "stroop_pre": np.random.normal(50, 10, 200),
        "stroop_pos": np.random.normal(45, 10, 200),
        "tmt_pre": np.random.normal(60, 15, 200),
        "tmt_pos": np.random.normal(55, 15, 200),
        "digit_span_pre": np.random.normal(7, 2, 200),
        "digit_span_pos": np.random.normal(8, 2, 200),
        "engajamento": np.random.uniform(0.4, 0.95, 200),
    })
    df["stroop_delta"] = df["stroop_pos"] - df["stroop_pre"]
    df["tmt_delta"] = df["tmt_pos"] - df["tmt_pre"]
    df["digit_span_delta"] = df["digit_span_pos"] - df["digit_span_pre"]

# Filtros
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    grupos = st.multiselect("Grupos:", df["grupo"].unique(), default=list(df["grupo"].unique()))

df_f = df[df["grupo"].isin(grupos)]

# KPIs
st.markdown("## 📊 Visão Geral do ECR")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("N total", len(df_f))
with col2:
    st.metric("Grupos", df_f["grupo"].nunique())
with col3:
    if "stroop_delta" in df_f.columns:
        st.metric("Δ Stroop médio", f"{df_f['stroop_delta'].mean():.2f}")
with col4:
    if "engajamento" in df_f.columns:
        st.metric("Engajamento médio", f"{df_f['engajamento'].mean():.2f}")

# Design do ECR
st.markdown("## 🧪 Design do Experimento")
st.markdown("""
**Fatorial 2×4:**
- Fator 1: **Pontos** (sim/não)
- Fator 2: **Narrativa** (sim/não)

**4 Grupos:**
1. Controle (sem gamificação)
2. Pontos apenas
3. Narrativa apenas
4. Pontos + Narrativa
""")

# Gráficos
st.markdown("## 📈 Resultados por Grupo")

tab1, tab2, tab3 = st.tabs(["Pré/Pos", "Comparação", "Engajamento"])

with tab1:
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    metrics = [("stroop", "Stroop (inibição)"), ("tmt", "TMT-B (flexibilidade)"), ("digit_span", "Digit Span (memória)")]

    for i, (metric, title) in enumerate(metrics):
        pre_col = f"{metric}_pre"
        pos_col = f"{metric}_pos"

        if pre_col in df_f.columns and pos_col in df_f.columns:
            pre_means = df_f.groupby("grupo")[pre_col].mean()
            pos_means = df_f.groupby("grupo")[pos_col].mean()

            x = np.arange(len(pre_means))
            w = 0.35
            axes[i].bar(x - w/2, pre_means, w, label="Pré", alpha=0.6)
            axes[i].bar(x + w/2, pos_means, w, label="Pós", alpha=0.6)
            axes[i].set_xticks(x)
            axes[i].set_xticklabels(pre_means.index, rotation=15)
            axes[i].set_title(title, fontweight="bold")
            axes[i].legend()
            axes[i].grid(True, axis="y", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    if "stroop_delta" in df_f.columns:
        fig, ax = plt.subplots(figsize=(12, 5))
        deltas = df_f.groupby("grupo")[["stroop_delta", "tmt_delta", "digit_span_delta"]].mean()
        deltas.plot(kind="bar", ax=ax)
        ax.set_title("Mudança (pós - pré) por grupo", fontweight="bold")
        ax.set_ylabel("Δ Score")
        ax.axhline(0, color="red", linestyle="--", alpha=0.5)
        ax.grid(True, axis="y", alpha=0.3)
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig)

with tab3:
    if "engajamento" in df_f.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        df_f.boxplot(column="engajamento", by="grupo", ax=ax)
        ax.set_title("Engajamento por grupo", fontweight="bold")
        ax.set_ylabel("Engajamento (0-1)")
        plt.suptitle("")
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig)

# Hipóteses
st.markdown("## 🎯 Hipóteses do ECR")
st.markdown("""
| H | Descrição | Predição |
|---|---|---|
| H2.1 | Pontos melhoram atenção (Stroop) | β ≈ 0.20, d = 0.20 |
| H2.2 | Narrativa melhora memória (Digit Span) | β ≈ 0.25, d = 0.25 |
| H2.3 | Pontos × Narrativa (TMT-B) | β ≈ 0.35, d = 0.35 |
| H2.4 | Engajamento medeia efeitos | Efeito indireto ≠ 0 |
""")

# Download
st.markdown("## 📥 Exportar")
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV (filtrado)",
    data=csv,
    file_name="P02_dados_filtrados.csv",
    mime="text/csv",
)
