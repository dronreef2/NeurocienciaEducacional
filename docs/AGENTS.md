# AGENTS.md — Diretório `docs/`

> Instruções para IAs trabalhando na pasta `docs/` (documentação).
> **Versão:** 1.0 — 2026-09-19

---

## 📂 Estrutura

```
docs/
├── AGENTS.md                  ← este arquivo
│
├── *.md                       ← docs raiz (~18 arquivos)
│   ├── API-REFERENCE.md       ← referência do pacote Python
│   ├── ARCHITECTURE.md        ← arquitetura do sistema
│   ├── ATALHOS-UTEIS.md       ← links críticos
│   ├── CHECKLIST-PRE-REUNIAO-ANGELA.md  ← kit reunião
│   ├── CODE_REVIEW.md
│   ├── DEPLOY-STREAMLIT.md
│   ├── POLITICA-AUTORIA.md    ← CRediT (NÃO modificar sem Ângela)
│   ├── POLITICA-DADOS.md      ← LGPD (NÃO modificar)
│   ├── PUBLISH-CRAN.md / PUBLISH-PYPI.md
│   ├── QUICKSTART.md
│   ├── RELEASE-v1.0.0.md
│   ├── ROADMAP-PRATICO.md / ROADMAP-GANTT.md
│   ├── SETUP-*.md
│   ├── USER-GUIDE.md
│   └── ZENODO-SETUP.md
│
├── apresentacao/              ← slides (Quarto + RevealJS)
├── atas/                      ← atas de reunião + kit Ângela
├── diario-pesquisa/           ← reflexões pessoais
├── divulgacao/                ← press releases
├── hipoteses/                 ← hipóteses detalhadas por projeto
├── manuscritos/               ← 5 manuscritos (rascunhos)
├── modelos/                   ← templates (ata, etc.)
├── osf-json/                  ← 5 JSONs para OSF + README
├── recrutamento/              ← páginas i18n PT/EN/ES
├── referencias/
├── source/                    ← Sphinx source
├── sphinx/                    ← Sphinx config
└── superpowers/               ← design + plan docs (SDD)
```

---

## 🚨 Regras ESPECÍFICAS de `docs/`

1. **POLITICA-AUTORIA.md** e **POLITICA-DADOS.md**: NÃO modificar sem aprovação da Ângela
2. **Atas em `atas/`** podem conter info sensível — NUNCA commitar TCLEs assinados, áudios, dados financeiros
3. **Manuscritos** já submetidos a journals: NÃO modificar após submission
4. **Pré-registros OSF** submetidos: NÃO modificar após submission
5. **LGPD**: todos os documentos públicos devem ser anonimizados
6. **Convenção atas:** `AAAA-MM-DD-[participantes]-[tipo].md` (ver `atas/README.md`)

---

## 🎯 Tipos de documento

| Tipo | Localização | Status | Editar livremente? |
|---|---|---|---|
| Protocolo | `0X-.../protocolo/` | v0.X | Sim (com supervisão) |
| Instrumento | `0X-.../instrumentos/` | v0.X | Sim |
| Manuscrito | `docs/manuscritos/` | rascunho | Só com revisão Ângela |
| Pré-registro | `docs/osf-json/` | validado | NÃO após submeter |
| Ata | `docs/atas/` | viva | Sim (anonimizar) |
| Política | raiz | v1.0 | NÃO sem aprovação |
| Apresentação | `docs/apresentacao/` | viva | Sim |
| Roadmap | `docs/ROADMAP-PRATICO.md` | vivo | Sim |

---

## 📚 Idiomas

- **Padrão:** português brasileiro
- **i18n:** PT/EN/ES apenas em `recrutamento/` + `apresentacao/`
- **Manuscritos:** em inglês (journals A1 são em inglês)

---

## 🔗 Links

- `AGENTS.md` raiz → visão geral
- `atas/README.md` → convenção de atas

---

**Última atualização:** 2026-09-19
