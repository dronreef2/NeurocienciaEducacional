# AGENTS.md — Diretório `pages/` (Streamlit multi-page)

> Instruções para IAs trabalhando no dashboard Streamlit.
> **Versão:** 1.0 — 2026-09-19

---

## 📂 Estrutura

```
pages/
├── AGENTS.md                  ← este arquivo
├── 1_🏠_Visao_Geral.py        ← overview
├── 2_📊_P01_Qualitativo.py    ← P01 com PDF download
├── 3_🎮_P02_Gamificacao.py    ← ECR 2x4
├── 4_🧠_P03_EEG.py            ← ERP
├── 5_📈_P04_SEM.py            ← mediação + moderação
├── 6_📅_P05_Longitudinal.py   ← LGCM + Kaplan-Meier
├── 7_🎬_Storytelling.py       ← 6 atos + epílogo
└── 8_📚_Sobre.py              ← referências
```

**Entry point:** `streamlit_app.py` (raiz)
**Deploy:** https://<app>.streamlit.app (após configurar Streamlit Cloud)

---

## 🚨 Regras ESPECÍFICAS

1. **Path resolution**: SEMPRE use `Path(__file__).resolve().parent.parent / "..."`
   - Funciona em `/workspace` (sandbox) e `/mount/src/...` (Streamlit Cloud)
   - NUNCA use `Path("/workspace/...")` (quebra no deploy)
2. **Imports do pacote**:
   ```python
   import sys
   _PKG_PATH = Path(__file__).resolve().parent.parent / "analise" / "Python"
   if str(_PKG_PATH) not in sys.path:
       sys.path.insert(0, str(_PKG_PATH))
   from neurociencia_edu.pdf_export import generate_project_pdf
   ```
3. **Matplotlib colorbar**: usar `fig.colorbar(im, ax=axes, ...)` (compartilhado, evita warning)
4. **Páginas numeradas**: prefixo `N_` onde N é a ordem no menu
5. **Ícones**: usar emoji no nome do arquivo para ícone na sidebar
6. **Dados sintéticos fallback**: cada página deve funcionar mesmo sem dados (gerar on-the-fly)

---

## 🎯 Comandos

```bash
# Local
streamlit run streamlit_app.py

# Deploy
# Streamlit Cloud → share.streamlit.io
# Main file path: streamlit_app.py
```

---

## 🔗 Links

- `AGENTS.md` raiz → visão geral
- `streamlit_app.py` → entry point
- `DEPLOY_STREAMLIT.md` → guia de deploy
- `.streamlit/config.toml` → theme

---

**Última atualização:** 2026-09-19
