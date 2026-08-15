"""Página 2: P01 - Qualitativo (IA e MToM)"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Adicionar pacote ao path (relativo ao arquivo, funciona em local + Streamlit Cloud)
_PKG_PATH = Path(__file__).resolve().parent.parent / "analise" / "Python"
if str(_PKG_PATH) not in sys.path:
    sys.path.insert(0, str(_PKG_PATH))
from neurociencia_edu.pdf_export import generate_project_pdf

st.set_page_config(page_title="P01 - Qualitativo", page_icon="📊", layout="wide")

st.markdown("# 📊 P01 — IA Generativa e Cognição de Teoria da Mente")
st.markdown("### *Estudo qualitativo com crianças do 2º ao 5º ano*")
st.markdown("---")

# Sidebar com filtros
with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    crianca = st.multiselect(
        "Criança:",
        ["Maria (C01)", "Pedro (C02)", "Júlia (C03)", "Todas"],
        default=["Todas"],
    )
    show_themes = st.checkbox("Mostrar 5 temas emergentes", value=True)

# Carregar dados sintéticos
_DATA_DIR = Path(__file__).resolve().parent.parent / "dados_sinteticos"
data_path = _DATA_DIR / "P01_diarios_sinteticos.csv"
if not data_path.exists():
    st.warning("⚠️ Dados sintéticos não encontrados. Gerando on-the-fly...")
    np.random.seed(42)
    n = 51
    df = pd.DataFrame({
        "crianca_id": ["C01"] * 17 + ["C02"] * 17 + ["C03"] * 17,
        "nome": ["Maria"] * 17 + ["Pedro"] * 17 + ["Júlia"] * 17,
        "dia": list(range(1, 18)) * 3,
        "mtom": [0] * 17 + [2 if d <= 8 else 1 if d <= 14 else 0 for d in range(1, 18)] + [2 if d <= 5 else 0 for d in range(1, 18)],
        "detecta_erro": [min(3, d // 4) for d in range(1, 18)] * 3,
        "confianca": [round(0.7 - d * 0.01, 2) for d in range(1, 18)] + [round(0.85 - d * 0.015, 2) for d in range(1, 18)] + [round(0.5 - d * 0.02, 2) for d in range(1, 18)],
    })
else:
    df = pd.read_csv(data_path)

# Filtrar
if "Todas" not in crianca:
    selected_ids = {"Maria (C01)": "C01", "Pedro (C02)": "C02", "Júlia (C03)": "C03"}
    ids = [selected_ids[c] for c in crianca]
    df = df[df["crianca_id"].isin(ids)]

# Métricas principais
st.markdown("## 📊 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Entradas", len(df))
with col2:
    st.metric("Crianças únicas", df["crianca_id"].nunique())
with col3:
    st.metric("Dias de observação", df["dia"].nunique())
with col4:
    st.metric("Detecção de erro média", f"{df['detecta_erro'].mean():.2f}")

# Gráficos
st.markdown("## 📈 Visualizações")

tab1, tab2, tab3, tab4 = st.tabs(["MToM × Dia", "Detecção de Erro", "Confiança", "Comparativo"])

with tab1:
    fig, ax = plt.subplots(figsize=(12, 5))
    if "nome" in df.columns:
        for nome in df["nome"].unique():
            sub = df[df["nome"] == nome]
            ax.plot(sub["dia"], sub["mtom"], "o-", label=nome, linewidth=2, markersize=8)
    else:
        for cid in df["crianca_id"].unique():
            sub = df[df["crianca_id"] == cid]
            ax.plot(sub["dia"], sub["mtom"], "o-", label=cid, linewidth=2, markersize=8)
    ax.set_xlabel("Dia")
    ax.set_ylabel("MToM (0-2)")
    ax.set_title("Teoria da Mente ao longo do tempo", fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(12, 5))
    if "nome" in df.columns:
        for nome in df["nome"].unique():
            sub = df[df["nome"] == nome]
            ax.bar(sub["dia"] + (list(df["nome"].unique()).index(nome) * 0.3) - 0.3, sub["detecta_erro"], width=0.3, label=nome)
    else:
        for i, cid in enumerate(df["crianca_id"].unique()):
            sub = df[df["crianca_id"] == cid]
            ax.bar(sub["dia"] + i * 0.3 - 0.3, sub["detecta_erro"], width=0.3, label=cid)
    ax.set_xlabel("Dia")
    ax.set_ylabel("Detecção de erro (0-3)")
    ax.set_title("Detecção de erro ao longo do tempo", fontweight="bold")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(12, 5))
    if "nome" in df.columns:
        for nome in df["nome"].unique():
            sub = df[df["nome"] == nome]
            ax.plot(sub["dia"], sub["confianca"], "s-", label=nome, linewidth=2, markersize=8)
    ax.set_xlabel("Dia")
    ax.set_ylabel("Confiança (0-1)")
    ax.set_title("Confiança na IA ao longo do tempo", fontweight="bold")
    ax.legend()
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with tab4:
    if "confianca" in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        if "nome" in df.columns:
            for nome in df["nome"].unique():
                sub = df[df["nome"] == nome]
                ax.scatter(sub["dia"], sub["confianca"], s=100, alpha=0.6, label=nome)
        ax.set_xlabel("Dia")
        ax.set_ylabel("Confiança")
        ax.set_title("Confiança vs Dia", fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# 5 Temas emergentes
if show_themes:
    st.markdown("## 🎨 5 Temas Emergentes")
    temas = [
        {"nome": "1. Antropomorfização Condicional", "desc": "Atribuição de agência à IA apenas quando ela responde corretamente."},
        {"nome": "2. Detecção Precoce de Erro", "desc": "A partir do 4º-5º dia, crianças detetam erros da IA."},
        {"nome": "3. Confiança Calibrada", "desc": "Confiança modulada por contexto (matemática vs interpretação)."},
        {"nome": "4. Comparação Sistemática", "desc": "IA como mais uma fonte, comparada a professores/pais."},
        {"nome": "5. Preferência Contextual", "desc": "Preferência por modalidade (texto/voz/imagem) depende da tarefa."},
    ]
    for tema in temas:
        with st.expander(tema["nome"]):
            st.markdown(tema["desc"])

# Dados brutos
st.markdown("## 📋 Dados Brutos")
st.dataframe(df.head(20), use_container_width=True)

# Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="P01_piloto_dados.csv",
    mime="text/csv",
)

# PDF Export
if st.button("📄 Gerar Relatório PDF (P01)"):
    with st.spinner("Gerando PDF..."):
        try:
            pdf_bytes = generate_project_pdf(
                project_id="P01",
                title="IA Generativa e Cognição de Teoria da Mente",
                data=df,
                metadata={
                    "N total": len(df),
                    "Crianças únicas": df["crianca_id"].nunique(),
                    "Dias": df["dia"].nunique() if "dia" in df.columns else 17,
                    "Período": "2026-2030",
                },
            )
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="P01_relatorio.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
