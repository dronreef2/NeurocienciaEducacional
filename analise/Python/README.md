# neurociencia-edu

> **Pacote Python para o Programa de Pesquisa em Neurociência Educacional (UFRN/CERES)**

[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/dronreef2/NeurocienciaEducacional)

Pacote de análise estatística e neurociência computacional para os
5 projetos de pesquisa (P01-P05) do programa.

## 📦 Instalação

```bash
pip install neurociencia-edu
# ou do repositório
pip install git+https://github.com/dronreef2/NeurocienciaEducacional.git
```

## 🚀 Uso Rápido

```python
import neurociencia_edu as ne
import pandas as pd
import numpy as np

# Análise Temática (P01)
transcripts = ne.load_transcripts("dados/transcricoes/", anonymize=True)

# IRT - Modelo de Rasch (P05)
responses = pd.read_csv("dados/P05_respostas.csv")
result = ne.fit_rasch(responses.values)
print(f"θ: {result['theta'].mean():.2f} ± {result['theta'].std():.2f}")

# Mixed Models (P01)
df = pd.read_csv("dados/P01_diarios.csv")
model = ne.fit_mixed_model(
    data=df, formula="score ~ tempo + (tempo | crianca)", groups="crianca_id"
)
print(model.summary())
```

## 📚 Módulos

| Módulo | Função | Projeto |
|---|---|---|
| `eeg.preprocessing` | `preprocess_eeg`, `compute_erp` | P03 |
| `stats.ancova` | `run_ancova` | P02 |
| `stats.mediation` | `run_mediation` | P04 |
| `stats.sem` | `run_sem` | P04 |
| `stats.irt` | `fit_rasch` | P05 |
| `stats.power` | `power_analysis` | Geral |
| `stats.mixed` | `fit_mixed_model` | P01, P05 |
| `io.bids` | `load_transcripts` | P01 |
| `io.validators` | `validate_csv` | Geral |
| `text.sentiment` | `analyze_sentiment` | P01 |
| `text.network` | `co_occurrence_network` | P01 |

## 🔗 Links

- **Repositório:** https://github.com/dronreef2/NeurocienciaEducacional
- **Documentação:** https://dronreef2.github.io/NeurocienciaEducacional/
- **Documentação API:** [docs/API-REFERENCE.md](../../docs/API-REFERENCE.md)
- **Tutoriais:** [notebooks/](../notebooks/)
- **Quick Start:** [docs/QUICKSTART.md](../../docs/QUICKSTART.md)

## 📄 Licença

MIT — veja [LICENSE](../../LICENSE) para detalhes.

## ✨ Citação

```bibtex
@software{neurociencia_edu,
  title  = {neurociencia-edu: Educational Neuroscience Research Toolkit},
  author = {[Seu Nome] and Naschold, Angela},
  year   = {2026},
  url    = {https://github.com/dronreef2/NeurocienciaEducacional}
}
```
