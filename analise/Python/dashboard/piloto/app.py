"""
app.py
Dashboard interativo do piloto P01 (Streamlit)
Visualiza dados de transcrições, diários, codebook e questionários.

Para rodar: streamlit run analise/Python/dashboard/piloto/app.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# ============================================================
# Configuração
# ============================================================

st.set_page_config(
    page_title="P01 Piloto — Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Diretórios
BASE = Path(__file__).resolve().parents[4] / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto"
TRANSCRICOES_DIR = BASE / "transcricoes"
DIARIOS_DIR = BASE / "diarios"
QUESTIONARIOS_DIR = BASE / "questionarios"
CODEBOOK_PATH = BASE / "codebook" / "codebook-piloto.csv"

# ============================================================
# Carregamento de dados (com cache)
# ============================================================

@st.cache_data
def load_transcripts():
    """Carrega todas as transcrições."""
    data = {}
    for f in TRANSCRICOES_DIR.glob("*.txt"):
        data[f.stem] = f.read_text()
    return data

@st.cache_data
def load_diaries():
    """Carrega todos os diários."""
    dfs = []
    for f in DIARIOS_DIR.glob("*.csv"):
        df = pd.read_csv(f)
        df["data"] = pd.to_datetime(df["data"])
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()

@st.cache_data
def load_questionnaires(tipo):
    """Carrega questionários por tipo."""
    if tipo == "pais":
        f = QUESTIONARIOS_DIR / "questionario_pais.csv"
    else:
        f = QUESTIONARIOS_DIR / "questionario_professores.csv"

    if f.exists():
        return pd.read_csv(f)
    return pd.DataFrame()

@st.cache_data
def load_codebook():
    """Carrega o codebook."""
    if CODEBOOK_PATH.exists():
        return pd.read_csv(CODEBOOK_PATH)
    return pd.DataFrame()

# Carregar
transcripts = load_transcripts()
diaries = load_diaries()
questionario_pais = load_questionnaires("pais")
questionario_prof = load_questionnaires("professores")
codebook = load_codebook()

# ============================================================
# Header
# ============================================================

st.title("🧠 Dashboard Piloto P01")
st.markdown("""
**Programa de Pesquisa em Neurociência Educacional — UFRN/CERES**

Visualização interativa dos dados do estudo piloto com 3 crianças
do 2º ano do ensino fundamental que usaram o tutor de IA Khanmigo
por 15-17 dias.
""")

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("📂 Navegação")
page = st.sidebar.radio("Ir para:", [
    "🏠 Visão Geral",
    "📅 Uso de Khanmigo",
    "📋 Codebook",
    "🎙️ Transcrições",
    "❓ Questionários",
    "📊 Análise Cruzada",
])

# ============================================================
# Página: Visão Geral
# ============================================================

if page == "🏠 Visão Geral":
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Participantes", len(transcripts))

    with col2:
        if not diaries.empty:
            total_min = diaries["duracao_min"].sum()
            st.metric("Total de uso", f"{total_min} min")
        else:
            st.metric("Total de uso", "N/A")

    with col3:
        if not codebook.empty:
            st.metric("Códigos", len(codebook))
        else:
            st.metric("Códigos", "N/A")

    with col4:
        if not codebook.empty:
            st.metric("Ocorrências", codebook["frequencia"].sum())
        else:
            st.metric("Ocorrências", "N/A")

    st.subheader("📖 Sobre o Estudo")
    st.markdown("""
    Este dashboard apresenta os dados do estudo piloto do **P01**, que investigou
    como crianças do 2º ano interpretam, vivenciam e confiam no tutor de IA
    **Khanmigo** (Khan Academy).

    ### Pergunta de pesquisa
    > Como crianças do 2º ano do ensino fundamental interpretam, vivenciam e
    > confiam no tutor de IA Khanmigo após 8 semanas de uso?

    ### Temas identificados (5)

    1. **Antropomorfização Condicional** — uso de pronomes humanos + reconhecimento de limites
    2. **Detecção Precoce de Erro** — capacidade de identificar e corrigir o tutor
    3. **Confiança Calibrada** — verificação ativa, "confio mas confiro"
    4. **Comparação Sistemática** — avaliação contra humanos (professora, família)
    5. **Preferência Contextual** — escolha situacional IA vs humanos
    """)

# ============================================================
# Página: Uso de Khanmigo
# ============================================================

elif page == "📅 Uso de Khanmigo":
    st.header("📅 Padrão de Uso do Khanmigo")

    if diaries.empty:
        st.warning("Sem dados de diário disponíveis.")
    else:
        # Filtro por participante
        participantes = sorted(diaries["participante_id"].unique())
        selected = st.sidebar.multiselect(
            "Filtrar por participante:",
            participantes,
            default=participantes,
        )

        df = diaries[diaries["participante_id"].isin(selected)]

        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dias registrados", len(df))
        with col2:
            st.metric("Total de minutos", f"{df['duracao_min'].sum()}")
        with col3:
            st.metric("Média por dia", f"{df['duracao_min'].mean():.1f} min")

        # Série temporal
        st.subheader("📈 Evolução do uso diário")
        fig = px.line(
            df, x="data", y="duracao_min", color="participante_id",
            title="Duração de uso do Khanmigo (em minutos)",
            labels={"duracao_min": "Minutos", "data": "Data"},
            markers=True,
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Atividades
        st.subheader("🎯 Tipos de atividade")
        if "atividades" in df.columns:
            ativ_contagem = df["atividades"].value_counts().reset_index()
            ativ_contagem.columns = ["Atividade", "Frequência"]
            fig = px.bar(
                ativ_contagem, x="Atividade", y="Frequência",
                color="Frequência", color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap dia da semana
        st.subheader("🗓️ Padrão semanal")
        df["dia_semana"] = pd.to_datetime(df["data"]).dt.day_name()
        heatmap_data = df.groupby(["participante_id", "dia_semana"])["duracao_min"].sum().reset_index()
        fig = px.density_heatmap(
            heatmap_data, x="dia_semana", y="participante_id",
            z="duracao_min", title="Uso total por dia da semana",
            labels={"duracao_min": "Minutos totais"},
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Página: Codebook
# ============================================================

elif page == "📋 Codebook":
    st.header("📋 Codebook — Códigos Identificados")

    if codebook.empty:
        st.warning("Codebook não disponível.")
    else:
        st.markdown(f"**Total:** {len(codebook)} códigos | **{codebook['frequencia'].sum()}** ocorrências")

        # Tabela completa
        st.subheader("Tabela completa")
        st.dataframe(
            codebook[["codigo", "frequencia", "participantes", "descricao"]],
            use_container_width=True,
            height=400,
        )

        # Top 10 códigos
        st.subheader("🔝 Top 10 códigos por frequência")
        top10 = codebook.nlargest(10, "frequencia")
        fig = px.bar(
            top10, x="frequencia", y="codigo", orientation="h",
            color="frequencia", color_continuous_scale="Reds",
            labels={"frequencia": "Ocorrências", "codigo": "Código"},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Cobertura por participante
        st.subheader("👥 Cobertura por participante")
        all_participants = set()
        for p_list in codebook["participantes"].dropna():
            for p in p_list.split(";"):
                all_participants.add(p.strip())

        coverage_data = []
        for p in sorted(all_participants):
            count = codebook["participantes"].str.contains(p, na=False).sum()
            coverage_data.append({"Participante": p, "Códigos presentes": count})

        cov_df = pd.DataFrame(coverage_data)
        fig = px.bar(
            cov_df, x="Participante", y="Códigos presentes",
            color="Códigos presentes", color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Página: Transcrições
# ============================================================

elif page == "🎙️ Transcrições":
    st.header("🎙️ Transcrições")

    if not transcripts:
        st.warning("Sem transcrições disponíveis.")
    else:
        participante = st.sidebar.selectbox(
            "Selecione o participante:",
            list(transcripts.keys()),
        )

        st.subheader(f"Transcrição: {participante}")

        content = transcripts[participante]
        st.text_area("Conteúdo:", content, height=400)

        # Análise simples de palavras
        st.subheader("📝 Análise de texto")
        col1, col2, col3 = st.columns(3)

        words = re.findall(r"\w+", content.lower())
        with col1:
            st.metric("Total de palavras", len(words))
        with col2:
            st.metric("Palavras únicas", len(set(words)))
        with col3:
            st.metric("Densidade lexical", f"{len(set(words))/len(words)*100:.1f}%")

        # Palavras mais frequentes
        stop_words = {"o", "a", "e", "de", "que", "do", "da", "em", "um", "uma",
                      "para", "com", "não", "os", "as", "dos", "das", "é", "foi",
                      "eu", "ele", "ela", "pra", "por", "se", "mas", "mais", "muito"}

        words_clean = [w for w in words if w not in stop_words and len(w) > 2]
        counter = Counter(words_clean)
        top_words = counter.most_common(20)

        df_words = pd.DataFrame(top_words, columns=["Palavra", "Frequência"])
        fig = px.bar(
            df_words, x="Frequência", y="Palavra", orientation="h",
            color="Frequência", color_continuous_scale="Teal",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Página: Questionários
# ============================================================

elif page == "❓ Questionários":
    st.header("❓ Questionários")

    tab1, tab2 = st.tabs(["👨‍👩‍👧 Pais", "👨‍🏫 Professores"])

    with tab1:
        if not questionario_pais.empty:
            st.subheader("Questionário de Pais (N=3)")
            st.dataframe(questionario_pais, use_container_width=True)

            # Conhecimento vs preocupação
            fig = px.scatter(
                questionario_pais,
                x="conhecimento_ia", y="preocupacao_ia",
                size="pai_idade", hover_data=["participante_id"],
                labels={
                    "conhecimento_ia": "Conhecimento sobre IA (1-5)",
                    "preocupacao_ia": "Preocupação com IA (1-5)",
                },
                title="Conhecimento vs Preocupação com IA (pais)",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dados de pais não disponíveis.")

    with tab2:
        if not questionario_prof.empty:
            st.subheader("Questionário de Professores (N=3)")
            st.dataframe(questionario_prof, use_container_width=True)
        else:
            st.warning("Dados de professores não disponíveis.")

# ============================================================
# Página: Análise Cruzada
# ============================================================

elif page == "📊 Análise Cruzada":
    st.header("📊 Análise Cruzada — Uso × Temas × Confiança")

    if codebook.empty or diaries.empty:
        st.warning("Dados insuficientes para análise cruzada.")
    else:
        # Calcular scores por participante
        scores = []
        for p in sorted(set(p for plist in codebook["participantes"].dropna()
                          for p in plist.split(";"))):
            p = p.strip()

            # Confiança calibrada: códigos de confiança
            confianca_alta = codebook[codebook["codigo"] == "confianca_alta"]["frequencia"].sum()
            confianca_baixa = codebook[codebook["codigo"] == "confianca_baixa"]["frequencia"].sum()
            calibrada = codebook[codebook["codigo"] == "confianca_calibrada"]["frequencia"].sum()

            # Detecção de erro
            deteccao = codebook[codebook["codigo"].str.contains("deteccao|correcao", na=False)]["frequencia"].sum()

            # Comparação humana
            comparacao = codebook[codebook["codigo"] == "compara_humano"]["frequencia"].sum()

            # Uso total
            if not diaries.empty:
                uso = diaries[diaries["participante_id"] == p]["duracao_min"].sum()
            else:
                uso = 0

            scores.append({
                "Participante": p,
                "Uso total (min)": uso,
                "Detecção de erro": deteccao,
                "Comparação humana": comparacao,
                "Confiança calibrada": calibrada,
            })

        df_scores = pd.DataFrame(scores)
        st.subheader("Perfil por participante")
        st.dataframe(df_scores, use_container_width=True)

        # Radar chart
        st.subheader("🎯 Perfil multidimensional")
        categorias = ["Detecção de erro", "Comparação humana", "Confiança calibrada"]

        fig = go.Figure()
        for _, row in df_scores.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[c] for c in categorias],
                theta=categorias,
                fill="toself",
                name=row["Participante"],
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            height=500,
            title="Perfil de cada participante (radar)",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Correlação uso x detecção
        if not diaries.empty:
            st.subheader("📈 Correlação: uso × detecção de erro")
            fig = px.scatter(
                df_scores, x="Uso total (min)", y="Detecção de erro",
                text="Participante", size_max=20,
                labels={"Uso total (min)": "Total de uso (minutos)"},
            )
            fig.update_traces(textposition="top center")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Footer
# ============================================================

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Versão:** 1.0 (Piloto)
**Dados:** 2026-08
**Programa:** Neurociência Educacional UFRN
""")

st.markdown("---")
st.markdown("""
<sub>Dashboard desenvolvido para visualização interativa dos dados piloto
do P01. Para feedback, abra issue no GitHub.</sub>
""")
