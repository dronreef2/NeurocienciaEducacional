"""
dashboard_piloto.py (root version for Streamlit Cloud)
Aponta para o dashboard específico do piloto P01
"""

import sys
from pathlib import Path

# Adicionar o caminho do dashboard específico
sys.path.insert(0, str(Path(__file__).parent / "analise" / "Python" / "dashboard" / "piloto"))

# Importar e executar
import streamlit as st
st.set_page_config(page_title="Piloto P01", page_icon="🎯", layout="wide")

# Carregar o dashboard do piloto
dashboard_file = Path(__file__).parent / "analise" / "Python" / "dashboard" / "piloto" / "dashboard_piloto.py"
if dashboard_file.exists():
    with open(dashboard_file) as f:
        exec(f.read())
else:
    st.error(f"Dashboard não encontrado: {dashboard_file}")
