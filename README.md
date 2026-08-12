# 🧠 Programa de Pesquisa: Tecnologia, Cérebro e Desenvolvimento Infantil

<!-- Badges -->
[![CI](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/ci.yml/badge.svg)](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/ci.yml)
[![Lint Markdown](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/lint-markdown.yml/badge.svg)](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/lint-markdown.yml)
[![Pages](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/pages.yml/badge.svg)](https://github.com/dronreef2/NeurocienciaEducacional/actions/workflows/pages.yml)
[![codecov](https://codecov.io/gh/dronreef2/NeurocienciaEducacional/graph/badge.svg)](https://codecov.io/gh/dronreef2/NeurocienciaEducacional)
[![codecov-python](https://codecov.io/gh/dronreef2/NeurocienciaEducacional/branch/main/graph/badge.svg?flag=python_package)](https://codecov.io/gh/dronreef2/NeurocienciaEducacional?flags[]=python_package)
[![codecov-r](https://codecov.io/gh/dronreef2/NeurocienciaEducacional/branch/main/graph/badge.svg?flag=r_package)](https://codecov.io/gh/dronreef2/NeurocienciaEducacional?flags[]=r_package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![R 4.4](https://img.shields.io/badge/R-4.4-blue.svg)](https://www.r-project.org/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![MNE 1.5](https://img.shields.io/badge/MNE-1.5-orange.svg)](https://mne.tools/)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Husky](https://img.shields.io/badge/Husky-enabled-pink?logo=husky)](https://typicode.github.io/husky/)
[![Open Science](https://img.shields.io/badge/Open%20Science-OSF-blue.svg)](https://osf.io/)
[![LGPD Compliant](https://img.shields.io/badge/LGPD-compliant-green.svg)](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)
[![UFRN](https://img.shields.io/badge/UFRN-CERES%2FICe-blue.svg)](https://www.ufrn.br/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![PyPI](https://img.shields.io/pypi/v/neurociencia-edu.svg)](https://pypi.org/project/neurociencia-edu/)
[![CRAN](https://img.shields.io/badge/CRAN-neurocienciasedu-blue.svg)](https://cran.r-project.org/package=neurocienciasedu)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://dronreef2.github.io/NeurocienciaEducacional/)

> Repositório-mestre do programa de pesquisa de 5 projetos (2026–2030) na interseção entre **Tecnologia Educacional**, **Neurociência Cognitiva** e **Desenvolvimento Infantil**, conduzido em parceria com a Profa. Dra. Ângela Chuvas Naschold (UFRN) e o Instituto do Cérebro da UFRN (ICe).

---

## 🎯 Visão do programa

Investigar, em uma série coordenada de 5 estudos, como diferentes tecnologias educacionais (tutores de IA generativa, gamificação, leitura digital, assistentes de escrita com IA) moldam o desenvolvimento cognitivo, atencional e metacognitivo de crianças entre 5 e 12 anos — e como o cérebro responde a essas tecnologias em janelas desenvolvimentais críticas.

**Linha de pesquisa ancorada em:** *Leitura + Neurociências* (RedLeitura / UFRN), sob coordenação da Profa. Ângela Naschold.

---

## 📦 Os 5 projetos (visão integrada)

| # | Projeto | Tipo | Período | Dificuldade | Paper-alvo principal |
|---|---|---|---|---|---|
| 01 | Vozes das crianças sobre tutores de IA | Qualitativo | 6–9 m | 🟢 | *Computers & Education* |
| 02 | Gamificação e autorregulação em matemática | Experimental | 9–12 m | 🟡 | *Learning and Instruction* |
| 03 | EEG de leitura digital vs. papel | Experimental + neuro | 12–18 m | 🟠 | *Developmental Cognitive Neuroscience* |
| 04 | IA generativa × funções executivas | Transversal correlacional | 10–14 m | 🟠 | *Computers in Human Behavior* |
| 05 | Coorte longitudinal com EEG | Longitudinal + neuro | 5+ anos | 🔴 | *Developmental Science* |

---

## 🗂️ Estrutura do repositório

```
.
├── 00-fundamentos/                  # Trilha formativa e bibliografia unificada
│   ├── bibliografia-seminais.md
│   ├── trilha-formacao.md
│   └── cronograma-mestre.md
├── 01-projeto-qualitativo-criancas-ia/   # ✅ CEP-ready (9 docs)
├── 02-projeto-gamificacao-autorregulacao/  # 🟡 planejado (README)
├── 03-projeto-eeg-leitura-digital/      # 🟡 planejado (README) — flagship
├── 04-projeto-ia-generativa-funcoes-executivas/  # 🟡 planejado (README)
├── 05-projeto-coorte-longitudinal/      # 🟡 planejado (README) — visão 5+ anos
├── docs/                            # Atas, modelos, referências cruzadas
└── .github/                         # Templates de issue, workflows
```

Cada pasta de projeto segue o padrão: `instrumentos/` (TCLE, TALE, escalas), `protocolo/` (submissão CEP), `analise/` (scripts R/Python, planilhas), `dados/` (NÃO versionado — ver `.gitignore`).

---

## 🚀 Como usar este repositório

1. **Kanban central** (GitHub Projects): `Backlog → Em curso → Aguardando revisão → Concluído`
2. **Issues por projeto** com labels: `projeto-01`, `projeto-02`, ..., `fundamentos`, `cep`, `paper`, `congresso`
3. **Branches por projeto**: `main`, `01-qualitativo/*`, `02-gamificacao/*`, etc.
4. **Tags para versões de manuscrito**: `v0.1-rascunho`, `v1.0-submissao-cep`, `v2.0-submissao-journal`
5. **Conventional Commits** em PT-BR: `docs:`, `analise:`, `protocolo:`, `dados:`

---

## 📚 Como citar

> [Seu nome]. (2026). *Programa de Pesquisa: Tecnologia, Cérebro e Desenvolvimento Infantil* (v0.1). GitHub. https://github.com/[seu-usuario]/[nome-repo]

---

## 📜 Licença

- **Código** (scripts, pipelines): MIT — ver `LICENSE`
- **Documentos e manuscritos** (`.md` e `.tex`): CC BY 4.0
- **Dados**: não versionados por padrão (privacidade e ética); ver política em `docs/POLITICA-DADOS.md` (a criar)

---

## 🤝 Contato

- Pesquisadora: [Seu nome]
- Orientadora: Profa. Dra. Ângela Maria Chuvas Naschold — `angela.naschold@ufrn.br`
- Linha de pesquisa: RedLeitura / Leitura + Neurociências (UFRN)
- Laboratório parceiro: Instituto do Cérebro da UFRN (ICe)
<!-- 2026-08-12T14:14:00 -->
