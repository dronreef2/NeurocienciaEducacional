# 🧠 Educational Neuroscience Research Program

> **Research program 2026-2030** investigating how different AI-based educational technologies impact cognitive development of children.
> **Partnership:** UFRN/CERES (Caicó/RN) + ICe (Natal/RN) | **Advisor:** Profa. Dra. Ângela Maria Chuvas Naschold
> **English version of [README.md](README.md)**

## 🎯 Mission

To understand, through mixed methods, how children from 2nd to 5th grade interpret, experience, and trust AI tutors (specifically Khanmigo), and what effects this interaction has on executive functions and literacy development.

## 📚 The 5 Studies

| ID | Theme | Design | N | Status |
|---|---|---|---|---|
| **P01** | Voices of children on AI tutors | Qualitative (Reflexive Thematic Analysis) | 3 (pilot) | ✅ Pilot done |
| **P02** | Gamification & EF | RCT 2×4 factorial | 200 | 🟡 Setup |
| **P03** | Reading EEG | Quasi-experimental (N170, P300) | 60 | 🟠 Setup |
| **P04** | Generative AI × EF | Cross-sectional (SEM) | 300-500 | 🟣 Data collection |
| **P05** | Cohort COORTE-INF | Longitudinal (5 annual waves) | 200 | 🔴 Planned |

## 🔬 Methodology

### Theoretical foundation

- **Machine Theory of Mind (MToM)** — how children conceptualize AI
- **Executive Functions** (Diamond, 2013) — inhibition, flexibility, working memory
- **Calibrated trust** (Muis et al., 2018) — alignment between confidence and accuracy
- **Reflexive Thematic Analysis** (Braun & Clarke, 2022)
- **Latent Growth Curve Models** (LGCM, LGMM)

### Quantitative methods

- Structural Equation Modeling (SEM, lavaan)
- Mixed-effects models (statsmodels, MixedLM)
- Cross-lagged panel models (CLPM)
- Bayesian analysis (PyMC)
- Item Response Theory (IRT, Rasch)
- EEG/ERP analysis (MNE-Python)

## 🛠️ Tech Stack

- **Python** 3.11+ (Poetry, Ruff, MNE-Python, scikit-learn, statsmodels)
- **R** 4.4+ (tidyverse, lavaan, OpenMx, testthat)
- **Snakemake** (workflow management)
- **Docker** + Docker Compose
- **Streamlit** + Shiny + Bokeh (dashboards)
- **Sphinx** + GitHub Pages (documentation)

## 📊 Pilot Results (P01, N=3)

5 emergent themes from Reflexive Thematic Analysis:

1. **Conditional Anthropomorphization** — 100% of children
2. **Early Error Detection** — 100% of children
3. **Calibrated Trust** — 67% (Pedro, Júlia)
4. **Systematic Comparison** (with humans) — 100%
5. **Contextual Preference** (situational choice) — 100%

**Statistical validation:** all 5 themes supported quantitatively. See [docs/manuscritos/P01-manuscrito-rascunho-v1.md](docs/manuscritos/P01-manuscrito-rascunho-v1.md).

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/dronreef2/NeurocienciaEducacional.git
cd NeurocienciaEducacional

# Install Python dependencies
poetry install

# Install R dependencies
R -e "devtools::install_deps()"

# Run validation
python3 analise/Python/scripts/validar_dados_piloto.py

# Run analysis
poetry run neurociencia-eeg-erp --input dados/processed/P03/ --batch
```

## 📁 Project Structure

```
NeurocienciaEducacional/
├── 00-fundamentos/          # Theoretical foundation
│   ├── 01-revisao-literatura/   # 13 reading notes
│   ├── 02-glossario-conceitos.md
│   └── 03-mapa-conceitual.md
├── 01-projeto-qualitativo-criancas-ia/  # P01
├── 02-projeto-gamificacao-funcoes-executivas/  # P02
├── 03-projeto-eeg-leitura/  # P03
├── 04-projeto-ia-generativa-funcoes-executivas/  # P04
├── 05-projeto-coorte-longitudinal/  # P05
├── docs/                    # Documentation
│   ├── manuscritos/            # Manuscript drafts
│   ├── recrutamento/           # Recruitment page
│   ├── osf-json/              # OSF pre-registrations
│   └── sphinx/                # Sphinx documentation
├── analise/                 # Analysis
│   ├── Python/                 # Python package + notebooks
│   ├── R/                      # R package + notebooks
│   └── rules/                  # Snakemake rules
├── resultados/              # Generated outputs
├── streamlit_app.py         # Streamlit Cloud entry point
├── requirements.txt
└── pyproject.toml
```

## 🤝 How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Quick summary:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/analysis-X`)
3. Make your changes (with tests!)
4. Run pre-commit: `poetry run pre-commit run --all-files`
5. Open a Pull Request

## 📜 License

MIT — see [LICENSE](LICENSE).

## 📞 Contact

- **Principal investigator:** [Your name] (PPGED/UFRN)
- **Advisor:** Profa. Dra. Ângela M. C. Naschold (angela.naschold@ufrn.br)
- **Repository:** [github.com/dronreef2/NeurocienciaEducacional](https://github.com/dronreef2/NeurocienciaEducacional)

## 📚 Citation

```bibtex
@software{neurociencia_educacional_2026,
  title = {Educational Neuroscience Research Program},
  author = {{Your Name} and Naschold, Ângela M. C.},
  year = {2026},
  version = {1.0.8},
  url = {https://github.com/dronreef2/NeurocienciaEducacional}
}
```

## 🌍 Other languages

- [Português (Brasil)](README.md) — primary
- [English](README.en.md) — this file

---

**Last updated:** 2026-08-07
**Status:** Active development
**Open science:** 5 OSF pre-registrations, all data and code public
