"""
Streamlit Dashboard — Programa de Pesquisa em Neurociência Educacional

Visualização interativa de resultados dos 5 projetos.

Uso:
    poetry run streamlit run analise/Python/neurociencia_edu/dashboard/app.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path as P

# Configuração da página
st.set_page_config(
    page_title="Neurociencia Educacional",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paths
PROJETO_ROOT = P(__file__).resolve().parent.parent.parent.parent
RESULTADOS_DIR = PROJETO_ROOT / "resultados"
DADOS_DIR = PROJETO_ROOT / "dados" / "processed"

# ============================================================
# Header
# ============================================================
st.title("🧠 Programa de Pesquisa em Neurociência Educacional")
st.markdown("""
**Dashboard interativo** para visualização dos resultados dos 5 projetos
(2026-2030) conduzidos em parceria com a UFRN/CERES.

**Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold
""")

# Sidebar
st.sidebar.title("📊 Navegação")
projeto = st.sidebar.selectbox(
    "Selecione o projeto:",
    ["Visão geral", "P01 - AT Khanmigo", "P02 - ANCOVA",
     "P03 - EEG/ERP", "P04 - SEM", "P05 - LGCM"]
)

# ============================================================
# Visão geral
# ============================================================
if projeto == "Visão geral":
    st.header("Visão Geral do Programa")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("P01 — AT", "🟢 Em andamento", "6-9 meses")
    with col2:
        st.metric("P02 — ANCOVA", "🟡 Em andamento", "9-12 meses")
    with col3:
        st.metric("P03 — EEG", "🟠 Setup", "12-18 meses")
    with col4:
        st.metric("P04 — SEM", "🟠 Em andamento", "10-14 meses")
    with col5:
        st.metric("P05 — LGCM", "🔴 Planejado", "5+ anos")

    st.markdown("---")

    st.subheader("📁 Status dos Resultados")
    if RESULTADOS_DIR.exists():
        arquivos = sorted(RESULTADOS_DIR.rglob("*"))
        if arquivos:
            df = pd.DataFrame([
                {"Projeto": str(a.relative_to(RESULTADOS_DIR)).split("/")[0],
                 "Arquivo": str(a.relative_to(RESULTADOS_DIR)),
                 "Tamanho (KB)": round(a.stat().st_size / 1024, 1)}
                for a in arquivos if a.is_file()
            ])
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info("Nenhum resultado ainda. Rode as análises primeiro.")
    else:
        st.warning("Pasta `resultados/` não encontrada.")

# ============================================================
# P01 — Análise Temática
# ============================================================
elif projeto == "P01 - AT Khanmigo":
    st.header("P01 — Análise Temática (Khanmigo)")

    p01_dir = RESULTADOS_DIR / "P01"
    if not p01_dir.exists():
        st.warning("Resultados do P01 não encontrados. Rode `at_pipeline()` primeiro.")
        st.stop()

    # Carregar codebook
    codebook_path = p01_dir / "07_codebook_inicial.csv"
    if codebook_path.exists():
        codebook = pd.read_csv(codebook_path)

        st.subheader("Codebook Inicial")
        st.dataframe(codebook, use_container_width=True)

        # Gráfico de frequência dos códigos
        if "frequencia_sugerida" in codebook.columns:
            fig = px.bar(
                codebook.sort_values("frequencia_sugerida", ascending=True),
                x="frequencia_sugerida", y="codigo",
                orientation="h",
                title="Frequência sugerida dos códigos",
                labels={"frequencia_sugerida": "Nº participantes", "codigo": "Código"},
                color="frequencia_sugerida",
                color_continuous_scale="Blues",
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Codebook ainda não gerado.")

    # Frequência de palavras
    freq_path = p01_dir / "01_frequencia_palavras.csv"
    if freq_path.exists():
        freq = pd.read_csv(freq_path).head(20)

        st.subheader("Top 20 palavras mais frequentes")
        fig = px.bar(
            freq.sort_values("n"),
            x="n", y="palavra",
            orientation="h",
            title="Frequência de palavras",
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# P02 — ANCOVA
# ============================================================
elif projeto == "P02 - ANCOVA":
    st.header("P02 — ANCOVA (Gamificação)")

    p02_dir = RESULTADOS_DIR / "P02"
    if not p02_dir.exists():
        st.warning("Resultados do P02 não encontrados. Rode `ancova_p02()` primeiro.")
        st.stop()

    # Tabela de resultados
    tab_path = p02_dir / "13_tabela_resultados.csv"
    if tab_path.exists():
        tab = pd.read_csv(tab_path)
        st.subheader("Tabela de Resultados")
        st.dataframe(tab, use_container_width=True)

    # Cohen's d
    cd_path = p02_dir / "08_cohens_d_stroop.csv"
    if cd_path.exists():
        cd = pd.read_csv(cd_path)
        st.subheader("Cohen's d (vs. CTRL)")

        fig = go.Figure(go.Bar(
            x=cd["comparacao"],
            y=cd["d"],
            error_y=dict(
                type="data",
                array=[cd["ci_upper"] - cd["d"],
                       cd["d"] - cd["ci_lower"]],
                visible=True,
            ),
        ))
        fig.update_layout(
            title="Tamanho de efeito (Cohen's d) com IC 95%",
            xaxis_title="Comparação",
            yaxis_title="Cohen's d",
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# P03 — EEG/ERP
# ============================================================
elif projeto == "P03 - EEG/ERP":
    st.header("P03 — EEG / ERP (Bandeira)")

    p03_dir = RESULTADOS_DIR / "P03"
    if not p03_dir.exists():
        st.warning("Resultados do P03 não encontrados. Rode o pipeline EEG primeiro.")
        st.stop()

    # Métricas dos componentes
    metrics_path = p03_dir / "00_metricas_componentes.csv"
    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path)

        st.subheader("Métricas dos Componentes ERP")

        # Seletor
        componente = st.selectbox(
            "Selecione o componente:",
            metrics["componente"].unique(),
        )

        df_comp = metrics[metrics["componente"] == componente]

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                df_comp, x="condicao", y="amplitude_media",
                title=f"Amplitude média — {componente}",
                error_y=df_comp["amplitude_pico"] - df_comp["amplitude_media"],
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                df_comp, x="condicao", y="latencia_pico_ms",
                title=f"Latência de pico — {componente}",
            )
            st.plotly_chart(fig, use_container_width=True)

    # Verifica arquivos de imagem
    for img_name in ["02_erp_N170.png", "03_topografia_N170.png",
                     "05_erps_canais.png"]:
        img_path = p03_dir / img_name
        if img_path.exists():
            st.image(str(img_path), caption=img_name.replace(".png", "").replace("_", " "))

# ============================================================
# P04 — SEM
# ============================================================
elif projeto == "P04 - SEM":
    st.header("P04 — SEM (IA Generativa × FE)")

    p04_dir = RESULTADOS_DIR / "P04"
    if not p04_dir.exists():
        st.warning("Resultados do P04 não encontrados. Rode `sem_p04()` primeiro.")
        st.stop()

    # Diagrama
    img_path = p04_dir / "05_modelo_sem.png"
    if img_path.exists():
        st.image(str(img_path), caption="Diagrama do modelo SEM")

    # Parâmetros
    params_path = p04_dir / "03_parametros_sem.csv"
    if params_path.exists():
        params = pd.read_csv(params_path)
        st.subheader("Parâmetros do SEM")
        st.dataframe(params, use_container_width=True)

# ============================================================
# P05 — LGCM
# ============================================================
elif projeto == "P05 - LGCM":
    st.header("P05 — LGCM (Coorte Longitudinal)")

    p05_dir = RESULTADOS_DIR / "P05"
    if not p05_dir.exists():
        st.warning("Resultados do P05 não encontrados. Rode `lgcm_p05()` primeiro.")
        st.stop()

    # Comparação de modelos
    comp_path = p05_dir / "03_comparacao_modelos.csv"
    if comp_path.exists():
        comp = pd.read_csv(comp_path)
        st.subheader("Comparação de Modelos")
        st.dataframe(comp, use_container_width=True)

    # Trajetórias
    img_path = p05_dir / "05_trajetorias_preditas.png"
    if img_path.exists():
        st.image(str(img_path), caption="Trajetórias preditas por perfil")

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown("""
<small>
Programa de Pesquisa em Neurociência Educacional — UFRN/CERES<br>
Repositório: <a href="https://github.com/dronreef2/NeurocienciaEducacional">GitHub</a> |
Documentação: <a href="https://dronreef2.github.io/NeurocienciaEducacional">GitHub Pages</a>
</small>
""", unsafe_allow_html=True)
