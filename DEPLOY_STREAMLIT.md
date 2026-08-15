# 🚀 Deploy no Streamlit Cloud

## Passo a passo

1. **Acesse** [share.streamlit.io](https://share.streamlit.io)
2. **Conecte** seu GitHub (droneef2/NeurocienciaEducacional)
3. **Crie um novo app**:
   - **Repository**: `dronreef2/NeurocienciaEducacional`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `https://<seu-app>.streamlit.app`
4. **Aguarde o build** (3-5 min na primeira vez)
5. **Compartilhe** com orientadora e colaboradores

## Configurações

- **Python version**: 3.11
- **Auto-deploy**: ativado (push to main → redeploy)
- **Secrets**: nenhum necessário (dados sintéticos)

## Verificação

Acesse `https://<seu-app>.streamlit.app` e verifique:
- 🏠 Página inicial carrega
- 📊 P01, P02, P03, P04, P05 funcionam
- 🎬 Storytelling (7 passos) navegável
- 📚 Sobre carrega
- 📥 Downloads CSV funcionam
- 📄 Downloads PDF funcionam

## Troubleshooting

### Erro "ModuleNotFoundError: No module named 'neurociencia_edu'"
- Solução: já é resolvido em `streamlit_app.py` com `sys.path.insert`
- Se persistir, adicione `analise/Python` ao `PYTHONPATH` nas config

### Erro "FileNotFoundError: catalog.yaml"
- Solução: o catalog é relativo a `/workspace/dados_sinteticos/`
- Em Streamlit Cloud, ajuste o `cat_path` para `Path(__file__).parent / "dados_sinteticos" / "catalog.yaml"`

### Dados sintéticos não carregam
- Os arquivos `.csv` e `.npy` são gerados pelo `gerar_dados_sinteticos.py`
- Verifique se estão commitados em `dados_sinteticos/`
- Se ausentes, cada página gera dados on-the-fly

### Build lento (>10 min)
- Reduza dependências em `requirements.txt`
- Use `@st.cache_data` nas funções de carga

## Estrutura de arquivos para o deploy

```
NeurocienciaEducacional/
├── streamlit_app.py        # Entry point (Main file path)
├── pages/                  # Páginas adicionais
│   ├── 1_🏠_Visao_Geral.py
│   ├── 2_📊_P01_Qualitativo.py
│   ├── 3_🎮_P02_Gamificacao.py
│   ├── 4_🧠_P03_EEG.py
│   ├── 5_📈_P04_SEM.py
│   ├── 6_📅_P05_Longitudinal.py
│   ├── 7_🎬_Storytelling.py
│   └── 8_📚_Sobre.py
├── analise/Python/         # Módulos do programa
│   └── neurociencia_edu/
│       ├── pdf_export.py
│       ├── cli.py
│       ├── cache.py
│       └── stats/
├── dados_sinteticos/       # Dados para visualização
│   ├── P01_diarios_sinteticos.csv
│   ├── P02_dados_sinteticos.csv
│   ├── P03_eeg_papel.npy
│   ├── P03_eeg_tela.npy
│   ├── P04_dados_sinteticos.csv
│   ├── P05_dados_longitudinais_sinteticos.csv
│   └── catalog.yaml
├── .streamlit/
│   └── config.toml         # Theme + server config
├── requirements.txt        # Python deps
└── DEPLOY_STREAMLIT.md     # Este arquivo
```

## URLs importantes

- **Streamlit Cloud**: https://share.streamlit.io
- **Repositório**: https://github.com/dronreef2/NeurocienciaEducacional
- **Documentação Streamlit**: https://docs.streamlit.io
