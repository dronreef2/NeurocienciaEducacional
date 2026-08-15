"""
streamlit_app.py — Entry point do dashboard multi-página
Programa de Pesquisa em Neurociência Educacional (UFRN/CERES)

Estrutura:
- Pages/1_🏠_Visao_Geral.py
- Pages/2_📊_P01_Qualitativo.py
- Pages/3_🎮_P02_Gamificacao.py
- Pages/4_🧠_P03_EEG.py
- Pages/5_📈_P04_SEM.py
- Pages/6_📅_P05_Longitudinal.py
- Pages/7_🎬_Storytelling.py
- Pages/8_📚_Sobre.py
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar pacote ao path (relativo ao arquivo — funciona local + Streamlit Cloud)
_PKG_PATH = Path(__file__).resolve().parent / "analise" / "Python"
if str(_PKG_PATH) not in sys.path:
    sys.path.insert(0, str(_PKG_PATH))

# Config da página principal (só funciona na página principal)
st.set_page_config(
    page_title="Neurociência Educacional | UFRN",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Programa de Pesquisa em Neurociência Educacional - UFRN/CERES/PPGED\n\n5 projetos de pesquisa (2026-2030)\n\nOrientadora: Profa. Dra. Ângela M. C. Naschold",
        "Get Help": "https://github.com/dronreef2/NeurocienciaEducacional/issues",
        "Report a bug": "https://github.com/dronreef2/NeurocienciaEducacional/issues/new",
    },
)

# Banner principal
st.markdown(
    """
    # 🧠 Programa de Pesquisa em Neurociência Educacional

    ### UFRN · CERES · PPGED (2026–2030)

    ---
    """
)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navegação")
    st.markdown("""
    Use o menu lateral para acessar cada projeto:

    - 🏠 **Visão Geral** — status dos 5 projetos
    - 📊 **P01 Qualitativo** — IA e MToM
    - 🎮 **P02 Gamificação** — ECR
    - 🧠 **P03 EEG** — Leitura tela vs papel
    - 📈 **P04 SEM** — IA e FE
    - 📅 **P05 Longitudinal** — LGCM
    - 🎬 **Storytelling** — tour guiado
    - 📚 **Sobre** — referências

    ---

    ### 📊 Métricas Globais
    """)

# Cards de overview
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Projetos", "5", "P01-P05")
with col2:
    st.metric("Período", "60 meses", "2026-2030")
with col3:
    st.metric("Datasets", "6", "sintéticos")
with col4:
    st.metric("Pré-registros", "5/5", "OSF")

st.markdown("---")

# Seção: Status dos Projetos
st.markdown("## 📊 Status dos 5 Projetos")

import pandas as pd
from pathlib import Path

try:
    cat_path = Path(__file__).resolve().parent / "dados_sinteticos" / "catalog.yaml"
    if cat_path.exists():
        import yaml
        with open(cat_path) as f:
            catalog = yaml.safe_load(f)

        # Monta tabela de status
        status_data = []
        for name, info in catalog.get("datasets", {}).items():
            status_data.append({
                "Dataset": name,
                "Projeto": info.get("projeto", "?"),
                "Tipo": info.get("tipo", "?"),
                "Linhas/Shape": str(info.get("n_rows", info.get("shape", "?"))),
                "Anonimizado": "✅" if info.get("anonimizado") else "❌",
            })

        df_status = pd.DataFrame(status_data)
        st.dataframe(df_status, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Erro ao carregar catalog: {e}")

# Seção: Como usar
st.markdown("## 🚀 Como usar este dashboard")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Para colaboradores
    1. **Explore** cada projeto via menu lateral
    2. **Filtre** dados por escola, idade, sexo
    3. **Visualize** resultados em gráficos interativos
    4. **Exporte** relatórios PDF por projeto

    ### Para orientadora
    1. Acompanhe o progresso dos 5 projetos
    2. Revise pré-registros OSF
    3. Aprove manuscritos
    4. Planeje próximas etapas
    """)

with col2:
    st.markdown("""
    ### Para a Secretaria de Educação
    1. **Visão geral** do programa
    2. **Indicadores** por projeto
    3. **Devolutivas** para escolas parceiras
    4. **Política educacional** baseada em evidências

    ### Para a comunidade científica
    1. **Manuscritos** em 5 revistas A1
    2. **Dados anonimizados** no OSF
    3. **Código aberto** no GitHub
    4. **Reprodutibilidade** completa
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    Programa de Pesquisa em Neurociência Educacional · UFRN/CERES/PPGED<br>
    Orientadora: Profa. Dra. Ângela M. C. Naschold<br>
    <a href="https://github.com/dronreef2/NeurocienciaEducacional">github.com/dronreef2/NeurocienciaEducacional</a>
</div>
""", unsafe_allow_html=True)
