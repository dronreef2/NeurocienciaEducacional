"""
streamlit_app.py
Entry point para deploy no Streamlit Community Cloud
(https://share.streamlit.io/)

Para deploy:
1. Vá em https://share.streamlit.io/
2. Conecte sua conta GitHub
3. Selecione: dronreef2/NeurocienciaEducacional
4. Branch: main
5. Main file path: streamlit_app.py
6. App URL: neurociencia-educacional-piloto (ou personalizado)

Este arquivo é um wrapper que importa e executa o dashboard
principal localizado em analise/Python/dashboard/piloto/app.py
"""

import sys
from pathlib import Path

# Adicionar o diretório do dashboard ao path
DASHBOARD_DIR = Path(__file__).parent / "analise" / "Python" / "dashboard" / "piloto"
sys.path.insert(0, str(DASHBOARD_DIR))

# Importar o dashboard principal
# O Streamlit Cloud executa este arquivo como __main__, então o app.py
# precisa estar no mesmo namespace
import importlib.util
spec = importlib.util.spec_from_file_location("dashboard_piloto", DASHBOARD_DIR / "app.py")
dashboard = importlib.util.module_from_spec(spec)

# Re-executar o código do dashboard no escopo deste módulo
# para que o Streamlit detecte os elementos de UI
try:
    spec.loader.exec_module(dashboard)
except FileNotFoundError:
    # Fallback se os dados não existirem no ambiente deploy
    import streamlit as st

    st.set_page_config(
        page_title="P01 Piloto — Dashboard",
        page_icon="🧠",
        layout="wide",
    )

    st.title("🧠 Dashboard Piloto P01")
    st.error("""
    ❌ Dados do piloto não encontrados.

    Este dashboard espera os dados em:
    `01-projeto-qualitativo-criancas-ia/dados/piloto/`

    Verifique se o repositório foi clonado completo.
    """)

    st.markdown("""
    ### Como resolver:
    1. Verifique se o repositório inclui a pasta `01-projeto-qualitativo-criancas-ia/`
    2. Os dados piloto devem estar em `dados/piloto/transcricoes/`, `diarios/`, `questionarios/`, `codebook/`
    3. Caso estejam gitignored, faça commit e push primeiro
    """)

# Exibir informações do deploy
if hasattr(dashboard, 'st'):
    pass  # dashboard já configurou tudo
