# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-09

### 🎉 PRIMEIRA RELEASE ESTÁVEL

Programa de Pesquisa em Neurociência Educacional — 5 projetos (2026-2030) em
parceria com a UFRN/CERES.

### Adicionado

#### Documentação
- 5 protocolos detalhados (P01-P05)
- 13 notas de leitura
- Glossário expandido (110+ termos)
- 5 rascunhos de manuscritos
- 5 pré-registros OSF
- E-mail para orientadora
- BLUEPRINT.md + AGENTS.md para AI IDE
- CONTRIBUTING.md + CONTRIBUTORS.md + .github/SECURITY.md
- **USER-GUIDE.md** (guia do usuário)
- **ROADMAP-GANTT.md** (timeline visual Mermaid)
- **CITATION.cff** (citação automática)
- **ROADMAP-PRATICO** (timeline M0-M60)

#### Análise — Python (13 notebooks)
1. `01_tutorial_basico.py` — Introdução ao programa
2. `02_tutorial_eeg.py` — EEG/ERP (P03)
3. `03_tutorial_irt.py` — IRT Rasch (P05)
4. `04_tutorial_sem.py` — SEM (P04)
5. `05_bayesian_analysis.py` — Análise Bayesiana
6. `06_mixed_effects_models.py` — Mixed-Effects
7. `07_cross_lagged.py` — CLPM
8. `08_power_analysis.py` — Análise de poder
9. `09_irt_analysis.py` — IRT completo
10. `10_p02_ecr_simulacao.py` — Simulação P02
11. `11_p03_eeg_realista.py` — Simulação P03
12. `12_sobrevivencia.py` — Kaplan-Meier + Cox
13. `13_item_analysis.py` — Análise Clássica de Itens
14. `14_bibliometria.py` — Análise bibliométrica

#### Análise — R
- `05_tutorial_lgcm.R` — LGCM com lavaan + tidyverse
- R package `neurocienciasedu` com at_pipeline.R, ancova.R, sem.R, lgcm.R

#### Scripts
- `validar_dados_piloto.py` — Validação completa
- `ingest_data.py` — Ingestão com anonimização
- `analise_piloto_real.py` — 5 testes estatísticos reais
- `mixed_models_diarios.py` — Mixed models nos diários
- `sentiment_network_analysis.py` — Sentimento + rede
- `gerar_dados_sinteticos.py` — **Gerador de dados para TODOS os 5 projetos**
- `osf_submit.py` — **Submissão automatizada ao OSF**
- `py2ipynb.py` — Conversor .py → .ipynb

#### Pacote Python
- `pyproject.toml` completo (PyPI-ready)
- `neurociencia_edu` package
- Workflow de publicação PyPI

#### Testes
- 22 testes de integração (test_pipeline_integration.py)
- 11 testes sobrev/item (test_sobrevivencia_item.py)
- CI workflow: validate-data.yml

#### Dados sintéticos
- P01: 15 crianças × 17 dias
- P02: 250 participantes ECR
- P03: EEG 60 sujeitos × 32 canais
- P04: 400 respondentes SEM
- P05: 200 crianças × 5 ondas

#### Visualizações (20 figuras PNG 300dpi)
1-4: Manuscripto P01 (framework, heatmap, mapa, timeline)
5: DAG P04
6-11: Resultados notebooks
12-15: Análises piloto/P02/P03
16: LGCM
17: Sentimento + rede
18-19: Sobrevivência + item analysis
20: Bibliometria

#### Internacionalização
- 3 idiomas: PT, EN, ES
- Páginas de recrutamento multi-idioma
- Slides em 3 idiomas
- README em PT e EN

#### Infraestrutura
- 7 workflows GitHub Actions
- Docker + Docker Compose
- Streamlit Cloud (auto-deploy)
- Codecov integration
- Codecov + PyPI secrets support

### Métricas

- **270+ arquivos** no repositório
- **~20 MB** de código + docs
- **33+ testes** automatizados
- **5 pré-registros** OSF
- **13 reading notes**
- **20 figuras** de alta resolução
- **14 notebooks** (todos em .py + .ipynb)
- **7 workflows** CI/CD
- **3 idiomas**

---

## [0.9.0] - 2026-07-28

### Adicionado
- P01-P05 protocolos detalhados
- 13 notas de leitura
- Estrutura de pastas dos 5 projetos
- Instrumentos do P01
- Pré-registro template OSF

## [0.1.0] - 2026-01-15

### Adicionado
- Estrutura inicial do repositório
- README, ROADMAP-PRATICO
- Templates básicos

---

[Unreleased]: https://github.com/dronreef2/NeurocienciaEducacional/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/dronreef2/NeurocienciaEducacional/releases/tag/v1.0.0
[0.9.0]: https://github.com/dronreef2/NeurocienciaEducacional/compare/v0.1.0...v0.9.0
[0.1.0]: https://github.com/dronreef2/NeurocienciaEducacional/releases/tag/v0.1.0
