# AGENTS.md — Instruções para IAs trabalhando no Neuro

> Este arquivo segue o padrão **AGENTS.md** reconhecido por Cursor, Claude Code, GitHub Copilot, Aider, Cline, Roo Code, Continue, Windsurf, e outros.
> **Versão:** 2.0 — atualizada em 2026-09-19
> **Status:** programa em M2 de 60, P01 CEP-ready + kit de reunião Ângela pronto

---

## 🎯 TL;DR (30 segundos)

Você está em um **programa de pesquisa científica sequencial de 5 projetos (2026–2030)** na interseção entre **tecnologia educacional, neurociência cognitiva e desenvolvimento infantil**.

- **Pesquisadora responsável:** pós-graduada em gestão de projetos, futura mestranda PPGED/UFRN
- **Orientadora proposta:** Profa. Dra. **Ângela Maria Chuvas Naschold** (UFRN/CERES, linha Leitura + Neurociências)
- **Linha-mãe:** como diferentes tecnologias educacionais (IA generativa, gamificação, leitura digital) moldam o desenvolvimento cognitivo de crianças brasileiras dos 6 aos 12 anos
- **Diferencial:** triangulação sequencial (quali → ECR → quase-exp EEG → SEM → LGCM), pré-registro aberto, dados anonimizados, código aberto
- **Repositório:** https://github.com/dronreef2/NeurocienciaEducacional (público, 94 commits, 871 arquivos)

---

## 📊 Estado atual (atualizado 2026-09-19)

### Programa
- **Mês 2 de 60** (M1 cumprido — plano estruturado)
- **5 projetos** com protocolo detalhado (P01–P05)
- **5 pré-registros OSF** validados e prontos para submissão
- **8 instrumentos do P01** completos (TCLE, TALE, diário, questionários, roteiros)
- **Kit de reunião com Ângela** completo (email + briefing + termo + agenda + ata + checklist)

### P01 (qualitativo, IA e MToM) — **MAIS MADURO**
- ✅ Protocolo detalhado (Análise Temática Reflexiva, Braun & Clarke 2022)
- ✅ 8 instrumentos (TCLE pais/mães, TALE criança, diário 17 dias, 2 questionários, 2 roteiros)
- ✅ Piloto com 3 crianças (Maria, Pedro, Júlia), 17 dias cada
- ✅ 5 temas emergentes identificados
- ✅ Manuscrito v1 (rascunho ~6k palavras)
- ✅ Pré-registro OSF validado
- ✅ Carta de anuência (template)
- ✅ Checklist CEP/Plataforma Brasil
- ⏳ Submissão CEP (autorização Ângela pendente)
- ⏳ Submissão *Computers & Education* (autorização Ângela pendente)

### P02–P05
- ✅ Protocolos detalhados
- ✅ Dados sintéticos (seed=42, reprodutíveis)
- ✅ Pré-registros OSF validados
- ✅ Análises estatísticas (mixed models, IRT, CLPM, SEM, LGCM, survival)

### Infraestrutura técnica
- ✅ **159 testes Python** passando (pytest)
- ✅ **23 testes stdlib** (unittest) para `osf_submit.py`
- ✅ **12 CI workflows** GitHub Actions (todos non-blocking com `continue-on-error`)
- ✅ **Pacote Python** `neurociencia_edu` (15+ módulos)
- ✅ **Pacote R** `neurocienciasedu`
- ✅ **Snakemake** pipeline
- ✅ **Dashboard Streamlit** multi-página (8 páginas)
- ✅ **PDF export** por projeto (reportlab)
- ✅ **Storytelling mode** (7 passos guiados)
- ✅ **CLI** `neuro` (catalog, validate, cache)
- ✅ **Data catalog** YAML (6 datasets)
- ✅ **DVC** instalado
- ✅ **Sphinx** docs deployadas em GitHub Pages
- ✅ **Quarto** P01 manuscript deploy

### Documentação
- ✅ **13 notas de leitura** (papers seminais com notas de aplicação)
- ✅ **Glossário** (110+ termos)
- ✅ **Mapa conceitual** (Mermaid)
- ✅ **Matriz síntese**
- ✅ **ROADMAP** prático + Gantt
- ✅ **Política de dados** LGPD-compliant
- ✅ **Política de autoria** (CRediT)
- ✅ **20+ figuras** 300 dpi
- ✅ **Recrutamento i18n** (PT/EN/ES)

---

## 📂 Estrutura do monorepo

```
NeurocienciaEducacional/
├── AGENTS.md                  ← este arquivo
├── BLUEPRINT.md               ← contexto completo para IAs
├── README.md                  ← landing page
├── CHANGELOG.md               ← histórico de versões
├── CITATION.cff               ← como citar
├── LICENSE                    ← MIT (código) + CC-BY-4.0 (dados)
│
├── 00-fundamentos/            ← base teórica e gestão
│   ├── bibliografia-seminais.md
│   ├── cronograma-mestre.md   ← 2026–2030
│   ├── glossario-conceitos.md (110+ termos)
│   ├── mapa-conceitual.md
│   ├── matriz-sintese.md
│   ├── trilha-formacao.md
│   ├── notas-leitura/         ← 13 papers com notas
│   └── preregistracao/        ← 5 templates OSF
│
├── 01-projeto-qualitativo-criancas-ia/   ← P01 (MAIS MADURO)
├── 02-projeto-gamificacao-funcoes-executivas/  ← P02
├── 03-projeto-eeg-leitura-digital/       ← P03
├── 04-projeto-ia-generativa-funcoes-executivas/  ← P04
├── 05-projeto-coorte-longitudinal/       ← P05
│
├── docs/                      ← documentação geral
│   ├── API-REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── ATALHOS-UTEIS.md
│   ├── CHECKLIST-PRE-REUNIAO-ANGELA.md  ← kit reunião
│   ├── CODE_REVIEW.md
│   ├── DEPLOY-STREAMLIT.md
│   ├── POLITICA-AUTORIA.md    ← CRediT
│   ├── POLITICA-DADOS.md      ← LGPD
│   ├── PUBLISH-CRAN.md / PUBLISH-PYPI.md
│   ├── QUICKSTART.md
│   ├── RELEASE-v1.0.0.md
│   ├── ROADMAP-PRATICO.md / ROADMAP-GANTT.md
│   ├── SETUP-*.md
│   ├── USER-GUIDE.md
│   ├── ZENODO-SETUP.md
│   ├── apresentacao/          ← slides
│   ├── atas/                  ← atas + kit reunião
│   ├── diario-pesquisa/
│   ├── divulgacao/            ← press releases
│   ├── hipoteses/
│   ├── manuscritos/           ← 5 manuscritos (rascunhos)
│   ├── modelos/               ← templates
│   ├── osf-json/              ← 5 JSONs para OSF
│   ├── recrutamento/          ← i18n PT/EN/ES
│   ├── referencias/
│   ├── source/                ← Sphinx source
│   ├── sphinx/
│   └── superpowers/           ← design + plan docs
│
├── analise/
│   ├── Python/                ← código principal
│   │   ├── pyproject.toml     ← Poetry, PyPI-ready
│   │   ├── pytest.ini
│   │   ├── neurociencia_edu/  ← pacote principal (15+ módulos)
│   │   ├── notebooks/         ← 12 notebooks
│   │   ├── tests/             ← 159+23 testes
│   │   ├── dashboard/
│   │   ├── scripts/           ← osf_submit.py, etc.
│   │   ├── benchmarks/
│   │   └── resultados/
│   ├── R/                     ← pacote R `neurocienciasedu`
│   ├── Snakemake/             ← pipeline
│   ├── config/                ← configurações
│   ├── dados/
│   ├── resultados/
│   └── rules/
│
├── dados_sinteticos/          ← 6 datasets + catalog.yaml
├── resultados/                ← figuras, tabelas
│
├── pages/                     ← Streamlit multi-page app (8 páginas)
│   ├── 1_🏠_Visao_Geral.py
│   ├── 2_📊_P01_Qualitativo.py
│   ├── 3_🎮_P02_Gamificacao.py
│   ├── 4_🧠_P03_EEG.py
│   ├── 5_📈_P04_SEM.py
│   ├── 6_📅_P05_Longitudinal.py
│   ├── 7_🎬_Storytelling.py
│   └── 8_📚_Sobre.py
│
├── streamlit_app.py           ← entry point Streamlit
├── requirements.txt           ← deps Streamlit Cloud
├── DEPLOY_STREAMLIT.md        ← guia de deploy
│
├── .streamlit/config.toml     ← theme + server config
├── .github/workflows/         ← 12 CI workflows
├── .devcontainer/             ← devcontainer config
├── .husky/                    ← git hooks
├── .pre-commit-config.yaml    ← pre-commit
├── Dockerfile + docker-compose.yml
├── Makefile + Snakefile
└── attachments/               ← arquivos enviados pelo usuário
```

---

## 🚨 Regras de ouro (NÃO QUEBRAR)

1. **NUNCA inventar** dados de escolas, pessoas, crianças, ou procedimentos que não existem.
2. **NUNCA versionar** dados sensíveis (TCLEs assinados, áudios, dados brutos com PII). `.gitignore` já trata a maior parte; respeitar.
3. **SEMPRE ler contexto** antes de criar/modificar algo: `BLUEPRINT.md`, `00-fundamentos/cronograma-mestre.md`, `AGENTS.md` da subpasta (se houver), README do projeto.
4. **SEMPRE manter coerência** com a linha da orientadora (Leitura + Neurociências, UFRN/CERES).
5. **EM CASO DE DÚVIDA METODOLÓGICA**: perguntar à pesquisadora. Não decidir sozinho.
6. **NUNCA publicar** dados de crianças sem TCLE/TALE assinado. LGPD é lei (Art. 7º, IV).
7. **SEMPRE pré-registrar** análises antes da coleta (OSF) — não é opcional, é regra do programa.

---

## 📐 Convenções obrigatórias

### Idioma e commits
- **Idioma principal:** português brasileiro
- **Commits:** Conventional Commits em PT-BR
  - `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `perf:`, `ci:`, `build:`
  - Exemplos: `feat(p01): adicionar questionário parental`, `fix(streamlit): corrigir path do catálogo`

### Estrutura de arquivos
- **Documentos:** começar com `> **Status:** v0.X — [estado]` quando aplicável
- **Nomes:** `[NN]-[tipo]-[descrição-curta].md` (ex: `01-protocolo-p01.md`, `08-tcle-pais.md`)
- **Tipos de documento:** `protocolo`, `instrumento`, `tcle`, `tale`, `analise`, `rascunho`, `final`, `ata`
- **Pastas numeradas:** `00-fundamentos/`, `01-...`, `02-...`, ..., `05-...` (estrutura sequencial)

### Python
- **Estilo:** PEP 8, type hints, docstrings (Google style)
- **Lint:** ruff (permissivo: `select=["F","E"]`)
- **Tests:** pytest (159 passando) + unittest stdlib (23 para osf_submit)
- **TDD:** Red → Green → Refactor (não escrever código sem teste)
- **Pacote:** `neurociencia_edu/` com submódulos `stats/`, `eeg/`, `io/`, `text/`, `cli.py`, `cache.py`, `pdf_export.py`

### R
- **Estilo:** tidyverse, snake_case
- **Indentificadores:** **NUNCA** começar com underscore (R 4.4 não permite)
- **Pacote:** `neurocienciasedu/`

### Streamlit
- **PAGES_DIR:** `pages/` na raiz (não dentro de `analise/`)
- **Path resolution:** SEMPRE usar `Path(__file__).resolve().parent.parent` (relativo, funciona local + Streamlit Cloud)
- **Cores matplotlib:** `RdBu_r` para divergentes, viridis para sequenciais
- **Colorbar:** usar `fig.colorbar(im, ax=axes, ...)` (compartilhado, evita warning)

---

## 🎯 Próximas tarefas prioritárias (em ordem)

1. **Reunião com Ângela** (kit pronto, falta disparar email e marcar data)
2. **Submissão do P01 ao CEP/UFRN** (após autorização Ângela)
3. **Submissão do P01 a *Computers & Education*** (após autorização Ângela)
4. **Submissão dos 5 pré-registros ao OSF** (`export OSF_TOKEN=...; python3 osf_submit.py --all`)
5. **Upload dos `*.metadata.json` companion** no OSF (P02, P03) como supplementary files
6. **Coleta de campo P01** (após aprovação CEP) — piloto expandido para 12-15 crianças
7. **Aplicação para mestrado PPGED/UFRN** (após aceite formal Ângela)
8. **Manuscrito P01 v2** (incorporar revisões da Ângela)
9. **Iniciar P02** (submissão FAPERN Demanda Espontânea Q2/2026)
10. **Iniciar P03** (acordo com ICe para EEG)

---

## 🤖 Comandos rápidos para IAs

### Sub-agentes disponíveis
- `explore` — exploração read-only (grep, glob, read)
- `general` — tarefas delegadas bounded
- `scout` — reconhecimento rápido externo

### Skills carregáveis
- `senior-fullstack-developer:engineering-workflow` (este workflow)
- `senior-fullstack-developer:frontend-dev` (UI/visual)
- `senior-fullstack-developer:fullstack-dev` (cross-layer)
- `superpowers:brainstorming` (criatividade)
- `superpowers:writing-plans` (planos)
- `superpowers:test-driven-development` (TDD)
- `superpowers:verification-before-completion` (validar antes de declarar pronto)

### Onde olhar primeiro
| Se você quer... | Olhe em... |
|---|---|
| Entender o programa todo | `BLUEPRINT.md` |
| Ver cronograma | `00-fundamentos/cronograma-mestre.md` |
| Saber o que é o P01 | `01-projeto-qualitativo-criancas-ia/README.md` |
| Entender LGPD | `docs/POLITICA-DADOS.md` |
| Ver o dashboard | `streamlit_app.py` + `pages/` |
| Rodar os testes | `analise/Python/tests/` |
| Submeter OSF | `analise/Python/scripts/osf_submit.py` |
| Preparar reunião Ângela | `docs/CHECKLIST-PRE-REUNIAO-ANGELA.md` + `docs/atas/` |
| Publicar no PyPI | `docs/PUBLISH-PYPI.md` |
| Publicar no CRAN | `docs/PUBLISH-CRAN.md` |
| Deploy Streamlit | `DEPLOY_STREAMLIT.md` |

---

## 🔗 Referências externas

- **Repositório:** https://github.com/dronreef2/NeurocienciaEducacional
- **Streamlit Cloud:** https://<app>.streamlit.app (após deploy)
- **GitHub Pages:** https://dronreef2.github.io/NeurocienciaEducacional
- **Orientadora:** `angela.naschold@ufrn.br`
- **PPGED/UFRN:** https://www.ufrn.br
- **CERES/UFRN:** https://ceres.ufrn.br
- **ICe (Instituto do Cérebro):** https://ice.ufrn.br
- **OSF:** https://osf.io (para pré-registros)

---

## ⚠️ Áreas que NÃO tocar sem consultar

- **LGPD/PII** — qualquer coisa com dados de crianças
- **Submissão ao CEP** — afeta ética da pesquisa
- **Pré-registros OSF já submetidos** — não modificar após submission
- **Manuscritos já submetidos a journals** — não modificar após submission
- **POLITICA-AUTORIA.md** — só com acordo da Ângela
- **Cronograma-mestre** — atualizar status, mas não mudar datas sem aprovação

---

## 📝 Histórico de versões deste arquivo

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 2026-07-27 | Versão inicial |
| 2.0 | 2026-09-19 | Atualização completa: +85 commits, OSF, dashboard, kit reunião, estrutura expandida |

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após reunião com Ângela (atualizar com decisões dela)
