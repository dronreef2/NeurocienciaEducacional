# 📖 Guia do Usuário — Programa de Pesquisa em Neurociência Educacional

> **Versão:** 1.0 (Agosto 2026)
> **Para:** Pesquisadores, alunos, colaboradores
> **Idioma:** PT-BR (EN em breve)

## 🎯 O que é este programa?

Programa de pesquisa de 5 anos (2026-2030) investigando como a IA generativa
impacta o desenvolvimento cognitivo de crianças. Inclui 5 estudos complementares
(P01-P05), ferramentas de análise, e dados abertos.

## 🚀 Como começar

### 1. Instalação local

```bash
# Clone
git clone https://github.com/dronreef2/NeurocienciaEducacional.git
cd NeurocienciaEducacional

# Python (recomendado: Poetry)
poetry install --all-extras

# R (opcional, para P05 LGCM)
R -e "install.packages(c('lavaan', 'tidyverse', 'broom'))"
```

### 2. Estrutura do projeto

```
NeurocienciaEducacional/
├── 00-fundamentos/          # Teoria, leitura, glossário
├── 01-projeto-.../          # P01 (qualitativo)
├── 02-projeto-.../          # P02 (ECR)
├── 03-projeto-.../          # P03 (EEG)
├── 04-projeto-.../          # P04 (SEM)
├── 05-projeto-.../          # P05 (coorte)
├── docs/                    # Documentação
├── analise/                 # Análise (Python + R)
├── resultados/              # Outputs gerados
└── streamlit_app.py         # Dashboard entry
```

### 3. Rodar uma análise

```bash
# Validar dados
python3 analise/Python/scripts/validar_dados_piloto.py

# Análise estatística completa
python3 analise/Python/scripts/analise_piloto_real.py

# Mixed models
python3 analise/Python/scripts/mixed_models_diarios.py

# Sentimento + rede
python3 analise/Python/scripts/sentiment_network_analysis.py

# Dashboard interativo
streamlit run streamlit_app.py
```

## 📊 Análises disponíveis

### Python (analise/Python/)

| Script | Descrição | Projeto |
|---|---|---|
| `scripts/validar_dados_piloto.py` | Valida schema, PII, ranges | Geral |
| `scripts/ingest_data.py` | Ingere CSVs com anonimização | Geral |
| `scripts/analise_piloto_real.py` | 5 testes estatísticos | P01 |
| `scripts/mixed_models_diarios.py` | Mixed models nos diários | P01 |
| `scripts/sentiment_network_analysis.py` | Sentimento + rede | P01 |
| `notebooks/01-04_*.py` | Tutoriais (básico, EEG, IRT, SEM) | Geral |
| `notebooks/05-09_*.py` | Análises avançadas | P02-P05 |
| `notebooks/10-13_*.py` | Simulações P02, P03, sobrev, item | P02-P05 |

### R (analise/R/)

| Script | Descrição | Projeto |
|---|---|---|
| `notebooks/05_tutorial_lgcm.R` | LGCM com lavaan | P05 |
| `R/at_pipeline.R` | Análise Temática (texto) | P01 |
| `R/utils.R` | Funções utilitárias | Geral |

## 🎓 Tutoriais Jupyter

Execute localmente com:
```bash
jupyter lab analise/Python/notebooks/
```

Ou online com Binder/Google Colab (em breve).

## 📦 Como usar como pacote Python

```python
import neurociencia_edu as ne

# EEG preprocessing
cleaned_eeg = ne.preprocess_eeg(raw_data, sfreq=500, l_freq=0.1, h_freq=40)

# ANCOVA
result = ne.run_ancova(data, outcome="y", predictor="group", covariates=["age"])

# Mediation
result = ne.run_mediation(data, "X", "M", "Y")
```

## 🌐 Dashboard Online

Acesse: **https://neurociencia-educacional.streamlit.app**

Mostra:
- 6 páginas interativas
- Visualizações dos 5 temas
- Análise cruzada dos participantes
- Codebook completo

## 🤝 Como contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

Resumo rápido:
1. Fork + branch (`git checkout -b feature/X`)
2. Commits em PT-BR com Conventional Commits
3. Testes + docs
4. Pull Request

## 📚 Documentação adicional

- [CONTRIBUTING.md](CONTRIBUTING.md) — Guia de contribuição
- [BLUEPRINT.md](BLUEPRINT.md) — Visão técnica do programa
- [AGENTS.md](AGENTS.md) — Instruções para AI IDE
- [ROADMAP-PRATICO](../00-fundamentos/ROADMAP-PRATICO.md) — Timeline
- [DEPLOY-STREAMLIT.md](DEPLOY-STREAMLIT.md) — Deploy
- [CITATION.cff](../CITATION.cff) — Citação

## 🐛 Problemas?

Abra uma [issue](https://github.com/dronreef2/NeurocienciaEducacional/issues/new/choose).

## 📞 Contato

- **Pesquisadora principal:** [Seu nome] — PPGED/UFRN
- **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold — UFRN/CERES
- **Email:** [seu-email]@ufrn.br

## 📜 Licença

MIT — veja [LICENSE](../LICENSE).

---

**Última atualização:** 2026-08-08
