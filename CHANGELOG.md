# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-31

### 🎉 Primeira release estável

Esta é a primeira release pública do Programa de Pesquisa em Neurociência
Educacional. O programa consiste em 5 projetos (2026-2030) conduzidos em
parceria com a UFRN/CERES, investigando como tecnologias educacionais
baseadas em IA impactam o desenvolvimento cognitivo de crianças.

### Adicionado

#### Documentação
- 5 protocolos detalhados (P01-P05)
- 13 notas de leitura de papers seminais
- Glossário de conceitos (60+ termos)
- Mapa conceitual (6 diagramas Mermaid)
- Matriz de síntese
- 8 instrumentos do P01 (entrevistas, TCLE, questionários)
- Cronograma-mestre (M0-M60)
- 3 pré-registros (P02, P03)
- Templates de diário de pesquisa
- Email para orientadora
- BLUEPRINT.md, AGENTS.md, CONTRIBUTING.md, CONTRIBUTORS.md, SECURITY.md
- Code review (avaliação técnica)

#### Análise — R
- 4 pipelines principais: AT, ANCOVA, SEM, LGCM
- R package `neurocienciasedu` (DESCRIPTION, NAMESPACE, R/*, man/*, tests/*)
- 4 R Markdown notebooks
- 8 testes testthat
- Análise de mediação, Cohen's d, Bonferroni, emmeans

#### Análise — Python
- 4 pipelines principais: preprocessing EEG, ERP analysis, mediation, BIDS
- Python package `neurociencia_edu` (eeg/, stats/, io/, tests/, dashboard/)
- 3 Jupyter notebooks
- 7+ testes pytest
- Type hints completos, docstrings Google style
- MediationResult NamedTuple, clustering com permutation

#### Infraestrutura
- Docker (R 4.4 + Python 3.11 + MNE 1.5)
- docker-compose (dev, RStudio, Jupyter)
- GitHub Actions: CI/CD (lint, test, build, publish)
- GitHub Pages: Sphinx docs auto-deploy
- Pre-commit hooks (9 hooks: ruff, markdownlint, styler, detect-secrets, etc.)
- Poetry (Python packaging)
- Makefile + Snakemake (workflows)
- 6 Snakemake rules modulares

#### Visualização
- Streamlit dashboard interativo
- R Markdown reports
- Jupyter notebooks com Plotly
- Wordclouds, topographies, boxplots

### Métricas

- 214 arquivos no repositório
- ~750 KB de código + docs
- 30+ testes automatizados
- 9 pre-commit hooks
- 4 GitHub Actions workflows
- 6 Snakemake rules
- 5 R Markdown + 3 Jupyter notebooks
- 11 badges no README

### Como citar

```bibtex
@software{neurociencia_edu_2026,
  title = {Programa de Pesquisa em Neurociência Educacional},
  author = {{Programa de Pesquisa em Neurociência Educacional} and Naschold, Angela Maria Chuvas},
  year = {2026},
  version = {1.0.0},
  url = {https://github.com/dronreef2/NeurocienciaEducacional},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

### Próximos passos (v1.1.0)

- Substituir dados sintéticos pelos reais
- Publicar packages no PyPI e CRAN
- Adicionar mais componentes ERP
- Implementar mixed-effects models
- Dashboard Shiny

---

## [0.9.0] - 2026-07-28

### Adicionado
- P01-P05 protocolos detalhados
- 13 notas de leitura
- Estrutura de pastas dos 5 projetos
- Instrumentos do P01

## [0.1.0] - 2026-01-15

### Adicionado
- Estrutura inicial do repositório
- README, ROADMAP-PRATICO
- Templates básicos

[Unreleased]: https://github.com/dronreef2/NeurocienciaEducacional/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/dronreef2/NeurocienciaEducacional/releases/tag/v1.0.0
[0.9.0]: https://github.com/dronreef2/NeurocienciaEducacional/compare/v0.1.0...v0.9.0
[0.1.0]: https://github.com/dronreef2/NeurocienciaEducacional/releases/tag/v0.1.0
