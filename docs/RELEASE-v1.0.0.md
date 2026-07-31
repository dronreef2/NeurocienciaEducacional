# 🎉 Release v1.0.0 — Notas

> **Data:** 2026-07-31
> **Tag:** `v1.0.0`
> **DOI Zenodo:** [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX) (gerado automaticamente)

## ✨ Resumo executivo

Primeira release pública do **Programa de Pesquisa em Neurociência Educacional**.

Esta release consolida **5 projetos (P01-P05)**, **5 pipelines de análise** (R + Python),
**15+ testes automatizados**, **documentação completa**, e **infraestrutura de produção**
(Docker, CI/CD, GitHub Pages, dashboards).

## 🆕 O que há de novo

### Documentação
- 5 protocolos detalhados (P01-P05)
- 13 notas de leitura de papers seminais
- 60+ termos no glossário
- 6 diagramas Mermaid (mapa conceitual)
- 8 instrumentos de coleta do P01
- 2 pré-registros OSF (P02, P03)
- BLUEPRINT, AGENTS, CONTRIBUTING, SECURITY, CHANGELOG
- Code review completo

### Análise (R)
- 4 pipelines: `at_pipeline()`, `ancova_p02()`, `sem_p04()`, `lgcm_p05()`
- 8 funções utilitárias
- 4 R Markdown notebooks
- 8 testes testthat
- R package skeleton (DESCRIPTION, NAMESPACE)

### Análise (Python)
- 4 módulos: `eeg`, `stats`, `io`, `tests`
- 3 Jupyter notebooks
- 7 testes pytest
- Type hints, docstrings, mediation analysis
- Python package skeleton (pyproject.toml)

### Infraestrutura
- 🐳 Docker (R 4.4 + Python 3.11 + MNE 1.5)
- 🚀 CI/CD (8 jobs no GitHub Actions)
- 🌐 GitHub Pages (Sphinx auto-deploy)
- 🎣 Husky (pre-commit em Node)
- 🔒 Pre-commit hooks (9 hooks: detect-secrets, ruff, styler, etc.)
- 📊 Codecov (coverage tracking)
- 📦 Poetry (Python packaging)
- 🐍 Snakemake (workflows + profiles para SLURM/SGE)

### Visualização
- Streamlit dashboard (5 projetos)
- Shiny R dashboard (5 projetos)
- Bokeh dashboard (P03 EEG)
- Plotly (interativo nos notebooks)

## 📊 Métricas

| Categoria | Valor |
|---|---|
| Total arquivos no repo | 240+ |
| Total LOC (código + docs) | ~15.000 |
| Tamanho do repo | ~1.5 MB |
| Testes automatizados | 15+ |
| Pre-commit hooks | 9 |
| CI/CD workflows | 5 |
| Snakemake profiles | 4 (local, slurm, sge, genérico) |
| Dashboards | 3 (Streamlit, Shiny, Bokeh) |
| Documentos .md | 80+ |
| R files | 25+ |
| Python files | 25+ |

## 🔄 Migração

Não há migração necessária — é a primeira release.

## 🐛 Bugs conhecidos

Nenhum no momento.

## 📥 Como instalar

### Via Git
```bash
git clone https://github.com/dronreef2/NeurocienciaEducacional.git
cd NeurocienciaEducacional
```

### Via PyPI (futuro)
```bash
pip install neurociencia-edu
```

### Via CRAN (futuro)
```r
install.packages("neurocienciasedu")
```

## 📚 Como citar

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

## 🆘 Suporte

- **Issues:** https://github.com/dronreef2/NeurocienciaEducacional/issues
- **Email:** pesquisa@neurociencia.edu

---

## 📋 Próximos passos (v1.1.0)

- [ ] Substituir dados sintéticos pelos reais
- [ ] Publicar packages no PyPI e CRAN
- [ ] Adicionar mixed-effects models
- [ ] Implementar SHAP values para interpretação ML
- [ ] Adicionar Bayesian analysis (Stan/PyMC)
- [ ] Criar tutoriais em vídeo

---

**Contribuidores:** ver [CONTRIBUTORS.md](../../blob/main/CONTRIBUTORS.md)

**Licença:** MIT

**Data:** 2026-07-31
