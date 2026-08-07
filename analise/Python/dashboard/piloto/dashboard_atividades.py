"""
dashboard_atividades.py
Dashboard alternativo focado em análise de atividades
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard de Atividades — P01",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# Carregar dados
# ============================================================

@st.cache_data
def load_data():
    BASE = Path(__file__).resolve().parents[4] / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto"

    # Diários
    diarios = []
    for f in (BASE / "diarios").glob("*.csv"):
        df = pd.read_csv(f)
        df["data"] = pd.to_datetime(df["data"])
        diarios.append(df)
    diarios = pd.concat(diarios, ignore_index=True) if diarios else pd.DataFrame()

    # Codebook
    codebook = pd.read_csv(BASE / "codebook" / "codebook-piloto.csv") if (BASE / "codebook" / "codebook-piloto.csv").exists() else pd.DataFrame()

    return diarios, codebook

diarios, codebook = load_data()

# ============================================================
# Header
# ============================================================

st.title("📊 Dashboard de Atividades — Análise de Uso")
st.markdown("""
Visualização detalhada do **padrão de atividades** realizadas pelas crianças
com o tutor de IA Khanmigo durante o estudo piloto.
""")

if diarios.empty:
    st.warning("Sem dados disponíveis")
    st.stop()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("🎯 Filtros")
participantes = sorted(diarios["participante_id"].unique())
selected = st.sidebar.multiselect("Participantes:", participantes, default=participantes)

# Período
data_min = diarios["data"].min()
data_max = diarios["data"].max()
date_range = st.sidebar.date_input(
    "Período:",
    [data_min, data_max],
    min_value=data_min,
    max_value=data_max,
)

# Tipo de atividade
atividades_all = sorted([a for a in diarios["atividades"].dropna().unique() if a])
selected_atividades = st.sidebar.multiselect("Atividades:", atividades_all, default=atividades_all)

# ============================================================
# Filtrar dados
# ============================================================

df = diarios[
    (diarios["participante_id"].isin(selected))
    & (diarios["data"] >= pd.Timestamp(date_range[0]))
    & (diarios["data"] <= pd.Timestamp(date_range[1]))
]
if selected_atividades:
    df = df[df["atividades"].isin(selected_atividades)]

# ============================================================
# Métricas
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Sessões totais", len(df))
with col2:
    st.metric("Minutos totais", f"{df['duracao_min'].sum():.0f}")
with col3:
    st.metric("Média por sessão", f"{df['duracao_min'].mean():.1f} min")
with col4:
    st.metric("Atividades únicas", df["atividades"].nunique())

# ============================================================
# Visualização 1: Calendário de uso (heatmap)
# ============================================================

st.subheader("📅 Calendário de uso")

df_cal = df.copy()
df_cal["dia"] = df_cal["data"].dt.date
df_cal["semana"] = df_cal["data"].dt.isocalendar().week
df_cal["dia_semana"] = df_cal["data"].dt.day_name()

# Pivot
pivot = df_cal.pivot_table(
    index="dia_semana",
    columns=df_cal["data"].dt.date,
    values="duracao_min",
    aggfunc="sum",
    fill_value=0,
)

# Reordenar dias
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = pivot.reindex([d for d in day_order if d in pivot.index])

fig = px.imshow(
    pivot.values,
    x=[str(c) for c in pivot.columns],
    y=pivot.index,
    color_continuous_scale="Viridis",
    labels=dict(color="Min"),
    aspect="auto",
)
fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Visualização 2: Distribuição de duração por atividade
# ============================================================

st.subheader("⏱️ Duração por atividade")

fig = px.box(
    df,
    x="atividades",
    y="duracao_min",
    color="participante_id",
    title="Distribuição de duração por atividade e participante",
    labels={"duracao_min": "Duração (min)", "atividades": "Atividade"},
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Visualização 3: Sunburst — Atividade × Participante
# ============================================================

st.subheader("☀️ Sunburst — Hierarquia de uso")

df_sun = df.groupby(["participante_id", "atividades"])["duracao_min"].sum().reset_index()

fig = px.sunburst(
    df_sun,
    path=["participante_id", "atividades"],
    values="duracao_min",
    color="duracao_min",
    color_continuous_scale="RdBu",
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Visualização 4: Dificuldades reportadas
# ============================================================

st.subheader("⚠️ Dificuldades reportadas")

if "dificuldades" in df.columns:
    dificuldades = df["dificuldades"].fillna("").value_counts()
    dificuldades = dificuldades[dificuldades.index != ""]

    if len(dificuldades) > 0:
        fig = px.bar(
            x=dificuldades.values,
            y=dificuldades.index,
            orientation="h",
            color=dificuldades.values,
            color_continuous_scale="Reds",
            labels={"x": "Frequência", "y": "Dificuldade"},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Visualização 5: Observações livres
# ============================================================

st.subheader("📝 Observações dos pais")

if "observacoes" in df.columns:
    obs = df[df["observacoes"].notna() & (df["observacoes"] != "")]
    if len(obs) > 0:
        with st.expander(f"Ver {len(obs)} observações"):
            for _, row in obs.iterrows():
                st.markdown(f"**{row['data'].strftime('%d/%m')} ({row['participante_id']}):** {row['observacoes']}")
    else:
        st.info("Nenhuma observação registrada")

# ============================================================
# Análise de correlações
# ============================================================

st.subheader("🔗 Correlações entre variáveis")

# Codificar atividades
df_corr = df.copy()
df_corr["atividade_mat"] = (df_corr["atividades"] == "matematica").astype(int)
df_corr["atividade_leit"] = (df_corr["atividades"] == "leitura").astype(int)
df_corr["duracao_cat"] = pd.cut(
    df_corr["duracao_min"],
    bins=[-1, 5, 15, 30, 1000],
    labels=["Muito curto", "Curto", "Médio", "Longo"],
)

corr_vars = ["duracao_min", "atividade_mat", "atividade_leit"]
corr_matrix = df_corr[corr_vars].corr()

fig = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Matriz de correlação",
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Footer
# ============================================================

st.markdown("---")
st.markdown(f"""
<sub>Dashboard gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')}.
Dados: {len(df)} sessões de {len(selected)} crianças.
Programa de Pesquisa em Neurociência Educacional — UFRN/CERES.</sub>
""")
