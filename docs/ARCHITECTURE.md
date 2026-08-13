# 🏗️ Arquitetura do Programa de Pesquisa

> **Documento técnico descrevendo a arquitetura, componentes e fluxo de dados**
> **Versão:** 1.0 (2026-08-13)

---

## 📐 Visão Geral

O Programa de Pesquisa em Neurociência Educacional é organizado como um
**monorepo** com camadas bem definidas, separando:

- **Documentação** (guias, protocolos, manuscritos)
- **Dados** (piloto anonimizado + sintéticos)
- **Análise** (Python + R + notebooks)
- **Pacotes** (bibliotecas reutilizáveis)
- **Dashboards** (Streamlit, Shiny, Bokeh)
- **Infraestrutura** (CI/CD, Docker, Make)

---

## 🗂️ Estrutura de Diretórios

```
NeurocienciaEducacional/
│
├── 📄 Documentação principal
│   ├── README.md                    # Apresentação principal
│   ├── CHANGELOG.md                 # Histórico de mudanças
│   ├── RESUMO-EXECUTIVO.md          # Visão executiva
│   ├── BLUEPRINT.md                 # Blueprint do programa
│   ├── AGENTS.md                    # Guia para AI IDEs
│   ├── CONTRIBUTING.md              # Como contribuir
│   ├── CODE_OF_CONDUCT.md           # Código de conduta
│   ├── USER-GUIDE.md                # Guia do usuário
│   ├── QUICKSTART.md                # Início rápido
│   ├── API-REFERENCE.md             # API do pacote
│   ├── docs/                        # Documentação adicional
│   │   ├── ARCHITECTURE.md          # Este arquivo
│   │   ├── hipoteses/               # Tabelas de hipóteses
│   │   ├── referencias/             # BibTeX + CSL
│   │   ├── manuscritos/             # Manuscritos
│   │   ├── divulgacao/              # Press release
│   │   ├── osf-json/                # Pré-registros OSF
│   │   └── sphinx/                  # Docs Sphinx
│   └── _quarto.yml                  # Config Quarto
│
├── 🔬 Dados
│   ├── dados_sinteticos/            # Dados gerados (synthetic)
│   │   ├── P01_diarios_sinteticos.csv
│   │   ├── P02_dados_sinteticos.csv
│   │   ├── P03_eeg_*.npy
│   │   ├── P04_dados_sinteticos.csv
│   │   └── P05_dados_longitudinais_sinteticos.csv
│   ├── 01-projeto-qualitativo-criancas-ia/dados/piloto/
│   │   ├── diarios/                 # 3 crianças × 17 dias
│   │   ├── transcricoes/            # Áudios transcritos
│   │   └── codebook/                # 27 códigos temáticos
│   └── .gitignore                   # Exclui dados sensíveis
│
├── 🧮 Análise
│   └── analise/
│       ├── Python/                  # Análise Python
│       │   ├── neurociencia_edu/    # Pacote Python
│       │   │   ├── config.py        # Config centralizado
│       │   │   ├── logging_config.py
│       │   │   ├── exceptions.py
│       │   │   ├── validators.py
│       │   │   ├── eeg/             # Pré-processamento EEG
│       │   │   ├── stats/           # Estatística
│       │   │   ├── io/              # I/O de dados
│       │   │   ├── text/            # Análise qualitativa
│       │   │   ├── visualization/   # Gráficos
│       │   │   └── tests/           # Testes do pacote
│       │   ├── notebooks/           # Jupyter notebooks (14)
│       │   ├── scripts/             # Scripts Python (8)
│       │   ├── dashboard/           # Dashboards
│       │   ├── tests/               # Testes integração
│       │   ├── pyproject.toml       # Config Poetry
│       │   ├── benchmarks/          # Performance tests
│       │   └── .vscode/             # VSCode config
│       └── R/                       # Análise R
│           ├── R/                   # Pacote R
│           ├── notebooks/           # R tutorial LGCM
│           └── tests/               # Testes R
│
├── 📊 Resultados
│   ├── figura1-21.png               # Figuras geradas
│   ├── validacao_dados.json
│   ├── relatorio_*.json
│   └── simulacao_piloto/            # Outputs do Notebook 15
│
├── 🐳 Infraestrutura
│   ├── Makefile                     # Comandos de build
│   ├── Snakefile                    # Pipeline Snakemake
│   ├── Dockerfile                   # Imagem principal
│   ├── Dockerfile.dashboard         # Imagem do dashboard
│   ├── docker-compose.yml
│   ├── .devcontainer/               # VSCode dev container
│   ├── .github/
│   │   ├── workflows/               # GitHub Actions (9+)
│   │   ├── ISSUE_TEMPLATE/
│   │   ├── PULL_REQUEST_TEMPLATE.md
│   │   └── SECURITY.md
│   ├── .pre-commit-config.yaml      # Pre-commit hooks
│   ├── .husky/                      # Git hooks
│   ├── .ruff.toml                   # Ruff config
│   ├── mypy.ini                     # Mypy config
│   ├── .markdownlint.json
│   ├── .secrets.baseline            # Detect-secrets
│   ├── .codecov.yml                 # Codecov config
│   └── .zenodo.json                 # Zenodo DOI
│
├── 📦 Publicação
│   ├── CITATION.cff                 # Citação automática
│   ├── LICENSE                      # MIT
│   ├── pyproject.toml               # PyPI metadata
│   ├── .zenodo.json                 # Zenodo metadata
│   └── docs/release-v1.0.0-docs.*   # Release archives
│
└── 🎯 Dashboards
    ├── streamlit_app.py             # Entry point Streamlit
    ├── dashboard_piloto.py          # Dashboard do piloto
    └── .streamlit/                  # Config Streamlit
```

---

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────────┐
│                         COLETA DE DADOS                              │
│  (diários, EEG, questionários, gamificação)                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ANONIMIZAÇÃO (LGPD)                               │
│  scripts/ingest_data.py → SHA256 hash                               │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VALIDAÇÃO                                        │
│  scripts/validar_dados_piloto.py                                     │
│  • Colunas obrigatórias                                              │
│  • Tipos de dados                                                    │
│  • Ranges válidos                                                    │
│  • PII não presente                                                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ANÁLISE                                           │
│  ┌──────────┬──────────┬──────────┬──────────┐                     │
│  │ Temática │  LMM     │  IRT     │  SEM     │                     │
│  │ (Braun)  │ (LME4)   │ (Rasch)  │ (lavaan) │                     │
│  └──────────┴──────────┴──────────┴──────────┘                     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   RELATÓRIOS / FIGURAS                               │
│  21 figuras PNG + JSONs                                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PUBLICAÇÃO                                         │
│  • Manuscritos (5)                                                   │
│  • Pré-registros OSF (5)                                             │
│  • Dashboards                                                        │
│  • Press release                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🐍 Arquitetura do Pacote Python

```
neurociencia_edu/
│
├── config.py              # ← Config centralizada (singleton)
│   ├── find_project_root()
│   ├── Paths              # dataclass frozen
│   ├── Programa           # constantes
│   ├── StatsConfig
│   ├── VizConfig
│   ├── Credentials        # env vars
│   └── Settings           # ← get_settings() singleton
│
├── logging_config.py      # ← Logging padronizado
│   ├── configure_logging()
│   ├── get_logger()
│   ├── log_section()
│   └── log_function_call()
│
├── exceptions.py          # ← Hierarquia de exceções
│   └── NeurocienciaEduError
│       ├── ConfigurationError
│       ├── DataError
│       │   ├── DataNotFoundError
│       │   ├── DataValidationError
│       │   └── DataAnonymizationError
│       ├── ProcessingError
│       │   ├── FitError
│       │   ├── ConvergenceError
│       │   └── InsufficientDataError
│       └── AnalysisError
│
├── validators.py          # ← Validadores + LGPD
│   ├── validar_colunas_obrigatorias()
│   ├── validar_range()
│   ├── detectar_pii()
│   ├── anonimizar_texto()
│   ├── anonimizar_dataframe()
│   ├── sanitizar_nome()
│   └── caminho_existe()
│
├── eeg/                   # Módulo EEG (P03)
│   ├── preprocessing.py
│   └── erp.py
│
├── stats/                 # Módulo Estatística
│   ├── ancova.py
│   ├── mediation.py
│   ├── sem.py
│   ├── irt.py
│   ├── power.py
│   └── mixed.py
│
├── io/                    # I/O de dados
│   ├── bids.py
│   ├── validators.py
│   └── transformers.py
│
├── text/                  # Análise qualitativa
│   ├── sentiment.py
│   └── network.py
│
└── visualization/         # Plots
    ├── plots.py
    └── reports.py
```

### Princípios

1. **Config centralizada** — paths, constantes, settings
2. **Logging padronizado** — formato consistente, configurável
3. **Validação rigorosa** — entrada validada antes de processar
4. **Exceções tipadas** — erros específicos para debugging
5. **Imutabilidade** — dataclasses frozen para configs
6. **Singleton** — get_settings() cacheado

---

## 🔀 Camadas de Processamento

```
┌─────────────────────────────────────────┐
│  CAMADA 1: Coleta (instrumentos)        │
│  • Diários de bordo                     │
│  • Questionários (LimeSurvey)            │
│  • EEG (32-ch)                          │
│  • Tarefas comportamentais              │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  CAMADA 2: Ingestão (scripts/)          │
│  • Anonimização (SHA256)                │
│  • Validação de schema                  │
│  • Geração de manifest                  │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  CAMADA 3: Armazenamento (dados/)       │
│  • CSVs (P01)                           │
│  • BIDS (P03)                           │
│  • JSONs (relatórios)                   │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  CAMADA 4: Análise (notebooks/scripts)  │
│  • Estatística (5 tipos)                │
│  • Qualitativa (ATR)                    │
│  • Rede (NetworkX)                      │
│  • IRT (Rasch)                          │
│  • SEM (lavaan)                         │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  CAMADA 5: Visualização (figuras/)      │
│  • 21 figuras PNG                       │
│  • 2 PDFs                               │
│  • Dashboards interativos               │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  CAMADA 6: Disseminação                 │
│  • Manuscritos                          │
│  • OSF pré-registros                    │
│  • Streamlit Cloud                      │
│  • Press release                        │
└─────────────────────────────────────────┘
```

---

## 🔁 Pipeline de Execução

```bash
# Desenvolvimento local
make install
make validate
make test
make analyze-pilot
make dashboard

# CI/CD
git push
  → CI (pytest + lint)
  → Codecov
  → Pages build
  → Quarto render (P01)
  → Streamlit Cloud auto-deploy

# Publicação
python osf_submit.py --all          # OSF
poetry build && poetry publish      # PyPI
git tag v1.0.0 && git push --tags  # GitHub release
```

---

## 🛠️ Stack Tecnológica

### Python
- **Core:** 3.11+, dataclasses, type hints
- **Data:** pandas, numpy, scipy
- **Stats:** statsmodels, scikit-learn
- **EEG:** mne, mne-bids
- **Viz:** matplotlib, seaborn, plotly, bokeh
- **Dashboard:** streamlit
- **Tests:** pytest, pytest-cov
- **Lint:** ruff, mypy
- **Build:** poetry

### R
- **Core:** 4.4+
- **Tidyverse:** dplyr, ggplot2
- **SEM:** lavaan
- **Longitudinal:** nlme
- **Tests:** testthat

### Infraestrutura
- **CI/CD:** GitHub Actions
- **Coverage:** Codecov
- **Pages:** GitHub Pages
- **Dashboard:** Streamlit Cloud
- **Container:** Docker
- **Dev:** VSCode + DevContainer

---

## 📊 Métricas

| Componente | Métrica | Valor |
|---|---|---|
| Código | Linhas Python | 12.3k |
| Código | Linhas R | 3.9k |
| Código | Linhas Markdown | 22.7k |
| Testes | Total | 70+ (43 novos) |
| Cobertura | Porcentagem | >80% (core) |
| Commits | Total | 80+ |
| Documentos | Total | 30+ |
| Workflows | CI/CD | 9+ |

---

## 🔐 Compliance

- **LGPD:** Anonimização via SHA256
- **CEP/CONEP:** Submissão aprovada
- **ICMJE:** Política de autoria
- **OSF:** 5 pré-registros
- **Open Science:** Dados abertos (anonimizados)

---

## 🚀 Roadmap de Desenvolvimento

### Próximas features
- [ ] Adicionar WebSocket para dashboard tempo real
- [ ] API REST com FastAPI
- [ ] Frontend React para visualizações avançadas
- [ ] Banco PostgreSQL para metadados
- [ ] Orquestração com Apache Airflow
- [ ] Cache Redis para análises pesadas

### Médio prazo
- [ ] Integração com plataformas educacionais
- [ ] App mobile (React Native)
- [ ] Análise em tempo real durante coleta

---

**Mantido por:** Programa de Pesquisa em Neurociência Educacional
**Última atualização:** 2026-08-13
