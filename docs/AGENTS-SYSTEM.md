# 🤖 Sistema de AGENTS.md do Neuro

> **Como o sistema multi-AGENTS.md funciona neste repositório.**
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Conceito

**AGENTS.md** é um padrão reconhecido por **Cursor, Claude Code, Aider, Cline, Roo Code, Continue, Windsurf, GitHub Copilot** e outros assistentes de IA.

**Hierarquia** (IAs leem de cima para baixo, fundem contexto):

```
AGENTS.md (raiz)                     ← visão geral + regras globais
├── 01-.../AGENTS.md                 ← regras do P01
├── 02-.../AGENTS.md                 ← regras do P02
├── 03-.../AGENTS.md                 ← regras do P03
├── 04-.../AGENTS.md                 ← regras do P04
├── 05-.../AGENTS.md                 ← regras do P05
├── analise/AGENTS.md                ← regras do diretório de análise
│   └── Python/AGENTS.md             ← regras específicas do Python
├── docs/AGENTS.md                   ← regras da documentação
├── pages/AGENTS.md                  ← regras do Streamlit
└── dados_sinteticos/AGENTS.md       ← regras dos dados sintéticos
```

**Quando uma IA abre um arquivo**, ela deve:
1. Ler o AGENTS.md **da raiz**
2. Ler o AGENTS.md **do diretório mais próximo** do arquivo
3. Aplicar regras mais específicas quando houver conflito

---

## 📂 Mapeamento completo

| Nível | Arquivo | Função | Tamanho |
|---|---|---|---|
| 0 | `AGENTS.md` | Visão geral + regras globais | 13.9k |
| 1 | `01-.../AGENTS.md` | P01 (IA e MToM) | 3.7k |
| 1 | `02-.../AGENTS.md` | P02 (Gamificação ECR) | 2.7k |
| 1 | `03-.../AGENTS.md` | P03 (EEG) | 3.1k |
| 1 | `04-.../AGENTS.md` | P04 (SEM) | 2.4k |
| 1 | `05-.../AGENTS.md` | P05 (LGCM) | 2.7k |
| 1 | `analise/AGENTS.md` | Análise de dados | 2.5k |
| 1 | `docs/AGENTS.md` | Documentação | 3.3k |
| 1 | `pages/AGENTS.md` | Streamlit | 2.1k |
| 1 | `dados_sinteticos/AGENTS.md` | Dados sintéticos | 1.8k |
| 2 | `analise/Python/AGENTS.md` | Python specifics | 4.4k |

**Total:** 11 arquivos AGENTS.md, ~43k chars

---

## 🚨 Regras GLOBAIS (em todos os níveis)

1. **Nunca inventar dados** de escolas, pessoas, crianças
2. **Nunca versionar** TCLEs assinados, áudios, dados com PII
3. **Sempre pré-registrar** análises antes da coleta (OSF)
4. **Sempre LGPD-compliant** (anonimização, consentimento)
5. **Português brasileiro** como idioma padrão
6. **Conventional Commits PT-BR**

---

## 🔄 Como atualizar

Quando você criar/modificar algo que afeta IAs:

1. **Adicionar nova pasta** → criar `AGENTS.md` na pasta
2. **Mudar convenção** → atualizar AGENTS.md relevante + raiz
3. **Mudar dependência** → atualizar pyproject + AGENTS.md Python
4. **Novo pré-registro submetido** → marcar como "NÃO modificar" no AGENTS

---

## 📋 Quando NÃO criar AGENTS.md

- Pastas com < 5 arquivos (a raiz cobre)
- Pastas de output/cache (não editáveis)
- Pastas auto-geradas (`__pycache__`, `.git`, `node_modules`)

---

## 🔗 Referências externas

- [agents.md](https://agents.md/) — especificação do padrão
- [Cursor docs](https://docs.cursor.com/)
- [Claude Code AGENTS.md support](https://docs.anthropic.com/en/docs/claude-code/agents-md)

---

**Última atualização:** 2026-09-19
