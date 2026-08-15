"""Página 1: Visão Geral dos 5 projetos."""
import streamlit as st
import pandas as pd
import yaml
from pathlib import Path

st.set_page_config(page_title="Visão Geral | P01-P05", page_icon="🏠", layout="wide")

st.markdown("# 🏠 Visão Geral dos 5 Projetos")
st.markdown("---")

# Carregar catalog
cat_path = Path("/workspace/dados_sinteticos/catalog.yaml")
if not cat_path.exists():
    st.error(f"❌ Catalog não encontrado: {cat_path}")
    st.stop()

with open(cat_path) as f:
    catalog = yaml.safe_load(f)

# Tabela de datasets
st.markdown("## 📊 Datasets Disponíveis")
datasets = catalog.get("datasets", {})

df_data = []
for name, info in datasets.items():
    df_data.append({
        "Dataset": name,
        "Projeto": info.get("projeto", "?"),
        "Tipo": info.get("tipo", "?").upper(),
        "Tamanho": str(info.get("n_rows", info.get("shape", "?"))),
        "Descrição": info.get("descricao", "?")[:60] + "...",
    })

df = pd.DataFrame(df_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# Métricas por projeto
st.markdown("## 📈 Métricas por Projeto")

projetos = {
    "P01": {"nome": "IA e MToM", "metodo": "Qualitativo (ATR)", "n": "12-15", "revista": "Computers & Education"},
    "P02": {"nome": "Gamificação e FE", "metodo": "ECR 2x4", "n": "200", "revista": "Computers in Human Behavior"},
    "P03": {"nome": "Leitura Tela vs Papel", "metodo": "Quase-exp. EEG", "n": "60", "revista": "NeuroImage"},
    "P04": {"nome": "IA e FE (SEM)", "metodo": "Transversal", "n": "300-500", "revista": "Computers in Human Behavior"},
    "P05": {"nome": "Coorte Longitudinal", "metodo": "LGCM", "n": "200", "revista": "Child Development"},
}

cols = st.columns(5)
for i, (pid, info) in enumerate(projetos.items()):
    with cols[i]:
        st.markdown(f"### {pid}")
        st.markdown(f"**{info['nome']}**")
        st.markdown(f"📊 {info['metodo']}")
        st.markdown(f"👥 N = {info['n']}")
        st.markdown(f"📖 {info['revista']}")

# Status badges
st.markdown("## ✅ Status dos Pré-registros")
st.success("5/5 pré-registros OSF prontos (P01, P02, P03, P04, P05)")

# Links
st.markdown("## 🔗 Links Rápidos")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    ### 📦 Repositório
    [github.com/dronreef2/NeurocienciaEducacional](https://github.com/dronreef2/NeurocienciaEducacional)
    """)
with col2:
    st.markdown("""
    ### 📚 Documentação
    - [QuickStart](https://github.com/dronreef2/NeurocienciaEducacional/blob/main/docs/QUICKSTART.md)
    - [API Reference](https://github.com/dronreef2/NeurocienciaEducacional/blob/main/docs/API-REFERENCE.md)
    - [Architecture](https://github.com/dronreef2/NeurocienciaEducacional/blob/main/docs/ARCHITECTURE.md)
    """)
with col3:
    st.markdown("""
    ### 📊 OSF Pré-registros
    - [P01](https://osf.io)
    - [P02](https://osf.io)
    - [P03](https://osf.io)
    - [P04](https://osf.io)
    - [P05](https://osf.io)
    """)
