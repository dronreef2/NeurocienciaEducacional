# 🚀 Guia de Deploy — Streamlit Community Cloud

> **Objetivo:** Publicar o dashboard do P01 em https://share.streamlit.io/
> **Tempo estimado:** 5-10 minutos
> **Custo:** Gratuito (Community Cloud)

---

## ✅ Pré-requisitos

- [x] Conta no GitHub (com o repositório `dronreef2/NeurocienciaEducacional`)
- [x] Conta no Streamlit Cloud (criar via SSO do GitHub: https://share.streamlit.io/)
- [x] Arquivo `streamlit_app.py` na raiz do repositório
- [x] Arquivo `requirements.txt` na raiz
- [x] Dados do piloto em `01-projeto-qualitativo-criancas-ia/dados/piloto/`

---

## 📋 Passo a Passo

### 1. Acessar o painel

Vá em: **https://share.streamlit.io/**

### 2. Criar novo app

Clique em **"Create app"** (canto superior direito) ou **"New app"**.

### 3. Preencher formulário

| Campo | Valor |
|---|---|
| **Repository** | `dronreef2/NeurocienciaEducacional` |
| **Branch** | `main` (ou `master` se preferir) |
| **Main file path** | `streamlit_app.py` |
| **App URL** (opcional) | `neurociencia-educacional-piloto` (gerará `https://neurociencia-educacional-piloto.streamlit.app`) |

### 4. Configurações avançadas (opcional)

Clique em **"Advanced settings"**:

- **Python version**: 3.11 (recomendado)
- **Secrets**: nenhum necessário (app é público, sem chaves)
- **Run command**: deixe em branco (usa padrão)

### 5. Deploy

Clique em **"Deploy!"**. O processo:
1. Clona o repositório
2. Instala dependências de `requirements.txt` (ou `pyproject.toml`)
3. Roda `streamlit run streamlit_app.py`
4. Gera URL pública

**Tempo de build:** 2-5 minutos na primeira vez.

---

## 🎯 Verificação Pós-Deploy

### Smoke test

1. Acesse a URL gerada
2. Verifique se a página inicial carrega
3. Navegue pelas 6 abas:
   - 🏠 Visão Geral
   - 📅 Uso de Khanmigo
   - 📋 Codebook
   - 🎙️ Transcrições
   - ❓ Questionários
   - 📊 Análise Cruzada

### Logs

Se houver erro:
- Vá em `https://share.streamlit.io/` → seu app → **"Manage app"** → **"Logs"**
- Verifique se `requirements.txt` foi lido corretamente
- Verifique se os caminhos de dados estão corretos

---

## 🔄 Atualização

O deploy é **automático** ao fazer push no branch configurado:

```bash
git add -A
git commit -m "feat: atualizar dashboard"
git push origin main
```

O Streamlit Cloud detecta o push e re-deploya em ~1-2 minutos.

---

## 💡 Considerações Importantes

### Recursos gratuitos (Community Cloud)

| Recurso | Limite |
|---|---|
| Apps por conta | 5 |
| Memória por app | 1 GB |
| CPU | Compartilhada |
| Storage | Sem persistent storage (não escreva no app) |
| Banda | Ilimitada (razoável) |
| Cold start | ~30s após inatividade |
| Sleep após inatividade | 7 dias sem访问 |

### Limitações deste app

1. **Dados são lidos do repositório** (sem DB). Se precisar atualizar dados, faça commit + push.
2. **Memória limitada** (1 GB) — se o dashboard crescer muito, considere mover para um servidor pago.
3. **Cold start** — primeira visita após inatividade pode demorar ~30s.
4. **Público** — qualquer pessoa com a URL pode acessar. **NÃO inclua dados sensíveis**.

### Privacidade e LGPD

⚠️ **ATENÇÃO:** O app é **público**. Certifique-se de que:

- [x] Dados do piloto são **sintéticos/fictícios** (sim, são)
- [x] Nomes são fictícios (Maria, Pedro, Júlia)
- [x] Não há CPFs, telefones, endereços reais
- [x] Não há dados de escolas identificáveis
- [x] Não há fotos de crianças

Para dados reais (após coleta), **NÃO** use o Community Cloud público.
Use deploy privado (Streamlit for Teams) ou auto-hospedagem.

### Alternativas de deploy

| Plataforma | Custo | Complexidade | URL pública |
|---|---|---|---|
| **Streamlit Community Cloud** | Grátis | Baixa | Sim, mas pública |
| **Streamlit for Teams** | $250/mês | Baixa | Sim, com auth |
| **Heroku** | $5-7/mês | Média | Sim |
| **Railway** | $5/mês | Média | Sim |
| **Render** | Grátis (sleep) | Baixa | Sim |
| **Servidor próprio (UFRN)** | Grátis (se houver) | Alta | Sim (interno) |

---

## 🔧 Customização

### Mudar tema

Edite `.streamlit/config.toml` e faça push.

### Adicionar nova página

Edite `analise/Python/dashboard/piloto/app.py` na função de página correspondente.

### Conectar a banco de dados

```python
# Adicione ao requirements.txt
# sqlalchemy>=2.0
# psycopg2-binary>=2.9  # PostgreSQL

# Em streamlit_app.py:
import os
DATABASE_URL = st.secrets["DATABASE_URL"]
```

Configure a secret no painel do Streamlit Cloud.

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"

→ Verifique se o módulo está em `requirements.txt`.

### Erro: "FileNotFoundError: dados"

→ Os dados do piloto não estão no repositório. Verifique `.gitignore`.

### App reiniciando constantemente

→ Provavelmente falta de memória. Otimize carregamento (use `@st.cache_data`).

### URL não funciona

→ Aguarde 1-2 minutos após o build. Verifique os logs.

---

## 📞 Suporte

- [Documentação oficial](https://docs.streamlit.io/streamlit-community-cloud)
- [Fórum Streamlit](https://discuss.streamlit.io/)
- [Status](https://status.streamlit.io/)

---

**Última atualização:** 2026-08-06
**Status:** ✅ Pronto para deploy
