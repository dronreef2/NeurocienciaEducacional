# AGENTS.md — `analise/Python/`

> Instruções para IAs trabalhando no pacote Python.
> **Versão:** 1.0 — 2026-09-19
> **Stack:** Python 3.11+, Poetry, pytest 7+, ruff

---

## 📂 Estrutura

```
analise/Python/
├── AGENTS.md                  ← este arquivo
├── pyproject.toml             ← Poetry config (PyPI-ready)
├── pytest.ini                 ← pytest config
├── README.md
│
├── neurociencia_edu/          ← pacote principal (15+ módulos)
│   ├── __init__.py
│   ├── config.py
│   ├── logging_config.py
│   ├── exceptions.py
│   ├── validators.py
│   ├── cli.py                 ← CLI `neuro`
│   ├── __main__.py            ← python -m neurociencia_edu
│   ├── cache.py               ← AnalysisCache + @cached_analysis
│   ├── pdf_export.py          ← PDF reports
│   │
│   ├── stats/                 ← estatísticas
│   │   ├── __init__.py
│   │   ├── _trends.py         ← mann_kendall
│   │   ├── _power.py          ← power_analysis
│   │   ├── _irt.py            ← fit_rasch (JMLE)
│   │   ├── _survival.py       ← kaplan_meier
│   │   └── _drift.py          ← PSI + KS
│   │
│   ├── eeg/                   ← EEG/ERP
│   │   ├── _preprocess.py     ← preprocess_eeg
│   │   └── _erp.py            ← compute_erp
│   │
│   ├── io/                    ← I/O
│   │   └── _serializers.py    ← convert_numpy, save_json
│   │
│   └── text/                  ← NLP
│       ├── _sentiment.py      ← analyze_sentiment (PT-BR)
│       └── _network.py        ← co_occurrence_network
│
├── notebooks/                 ← 12 Jupyter notebooks
│   ├── 01_eeg_exploration.ipynb
│   ├── 01_tutorial_basico.ipynb
│   ├── 02_erp_statistics.ipynb
│   ├── 02_tutorial_eeg.ipynb
│   ├── 03_complete_workflow.ipynb
│   ├── 03_tutorial_irt.ipynb
│   ├── 04_tutorial_sem.ipynb
│   ├── 05_bayesian_analysis.ipynb
│   ├── 06_mixed_effects_models.ipynb
│   ├── 07_cross_lagged.ipynb
│   ├── 08_power_analysis.ipynb
│   ├── 09_irt_analysis.ipynb
│   ├── 10_p02_ecr_simulacao.ipynb
│   ├── 11_p03_eeg_realista.ipynb
│   └── 12_sobrevivencia.ipynb
│
├── tests/                     ← 159 pytest + 23 unittest
│   ├── test_*.py
│   └── test_osf_submit_stdlib.py
│
├── scripts/                   ← standalone scripts
│   └── osf_submit.py          ← OSF submission
│
├── dashboard/
├── benchmarks/
└── resultados/
```

---

## 🚨 Regras ESPECÍFICAS Python

1. **TDD obrigatório**: Red → Green → Refactor
2. **Imports refatorados**: SEMPRE `from neurociencia_edu.stats import X` (não de utils antigos)
3. **Type hints** obrigatórios em funções públicas
4. **Docstrings** Google style
5. **Linting:** `ruff check analise/Python/` (select F+E)
6. **Pytest:** `pytest tests/ --ignore=tests/test_notebooks.py --ignore=tests/test_eeg_pipeline.py`
7. **Pyproject extras:**
   - `pip install -e .[eeg]` (MNE)
   - `pip install -e .[bayesian]` (PyMC)
   - `pip install -e .[dashboard]` (Streamlit + reportlab)
   - `pip install -e .[docs]` (Sphinx)
   - `pip install -e .[all]` (tudo)
8. **Submodule `_xxx.py`** (underscore prefix) = módulo interno, não API pública

---

## 🎯 Comandos rápidos

```bash
# Ambiente virtual
python3 -m venv .venv && source .venv/bin/activate

# Instalar pacote + deps
pip install -e ".[all]"

# Rodar testes
python3 -m pytest tests/ -v

# Lint
ruff check neurociencia_edu/

# CLI
python3 -m neurociencia_edu catalog list
python3 -m neurociencia_edu validate P01_diarios_sinteticos
python3 -m neurociencia_edu cache list

# OSF
python3 scripts/osf_submit.py --validate
python3 scripts/osf_submit.py --all
```

---

## 📦 Publicação

- **PyPI:** `poetry build && poetry publish` (ver `docs/PUBLISH-PYPI.md`)
- **Versão atual:** ver `pyproject.toml` (`[tool.poetry].version`)

---

## 🔗 Links

- `AGENTS.md` raiz → visão geral
- `analise/AGENTS.md` → diretório pai
- `analise/Python/pyproject.toml` → deps + metadata

---

**Última atualização:** 2026-09-19
