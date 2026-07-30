# 💻 Análise de Dados — Scripts do Programa

> **Stack analítico** para os 5 projetos do programa de pesquisa.
> **Princípios:** reprodutibilidade, clareza, modularidade.
> **Linguagens:** R (análise estatística, AT, SEM, LGMM) e Python (EEG/ERP).

---

## 📁 Estrutura

```
analise/
├── README.md                     ← este arquivo
├── R/                            ← scripts R
│   ├── 00_setup.R                ← carrega libraries, configura paths
│   ├── 01_at_pipeline.R          ← pipeline de Análise Temática (P01)
│   ├── 02_at_visualization.R     ← visualizações (wordcloud, frequência)
│   ├── 03_sem_p04.R              ← SEM do P04 (FE × IA)
│   ├── 04_lgcm_p05.R             ← LGCM/LGMM do P05 (coorte)
│   └── utils.R                   ← funções auxiliares
├── Python/                       ← scripts Python
│   ├── 00_setup.py               ← instala MNE, configura paths
│   ├── 01_eeg_preprocessing.py   ← pipeline de pré-processamento (P03, P05)
│   ├── 02_eeg_erp_analysis.py    ← análise de ERPs (P03)
│   ├── utils.py                  ← funções auxiliares
│   └── config.py                 ← configurações (canais, eventos, etc.)
├── dados/                        ← (NÃO VERSIONADO) dados brutos e processados
├── resultados/                   ← (NÃO VERSIONADO) outputs (figuras, tabelas)
└── requirements.txt              ← dependências Python
```

---

## 🎯 Princípios

### Reprodutibilidade
- **Set seed** em qualquer análise com aleatoriedade
- **Versões fixas** de packages (renv para R, requirements.txt para Python)
- **Documentar** cada passo em Markdown (não só em comentários)
- **Snake_case** (Python) e **snake_case** (R) consistentes
- **Commits atômicos** com Conventional Commits em PT-BR

### Clareza
- **Funções pequenas** com responsabilidade única
- **Docstrings** em todas as funções
- **Comentários** só quando necessário (código se autodocumenta)
- **Logs** estruturados (não `print` aleatório)
- **Mensagens de erro** claras

### Modularidade
- **Cada projeto** em uma subpasta ou arquivo dedicado
- **Funções reutilizáveis** em `utils.R` / `utils.py`
- **Configurações** centralizadas em `00_setup.R` / `00_setup.py`

---

## 📊 Por projeto

| Projeto | Linguagem | Script principal | Dependências principais |
|---|---|---|---|
| **P01** (AT) | R | `R/01_at_pipeline.R` | tidyverse, tidytext, quanteda, ggplot2 |
| **P02** (ANOVA) | R | `R/02_anova_p02.R` (a criar) | afex, emmeans, ggplot2 |
| **P03** (EEG) | Python | `Python/01_eeg_preprocessing.py` | mne, numpy, pandas, scipy |
| **P03** (ERP) | Python | `Python/02_eeg_erp_analysis.py` | mne, scipy.stats, matplotlib |
| **P04** (SEM) | R | `R/03_sem_p04.R` | lavaan, semTools, semPlot |
| **P05** (LGCM) | R | `R/04_lgcm_p05.R` | lavaan, OpenMx, tidySEM, ggplot2 |

---

## 🔧 Como rodar

### R
```bash
# Instalar renv para reprodutibilidade
R -e "install.packages('renv')"

# Inicializar projeto
R -e "renv::init()"
R -e "renv::restore()"  # instala packages do renv.lock

# Rodar pipeline do P01
Rscript R/01_at_pipeline.R
```

### Python
```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar pipeline de EEG
python Python/01_eeg_preprocessing.py --input dados/raw/P03/subj01.bdf --output dados/processed/P03/subj01/
```

---

## 📚 Boas práticas adotadas

1. **Documentação em YAML header** de cada script
2. **Argumentos via linha de comando** (não hardcoded)
3. **Paths relativos** (não absolutos)
4. **Logging** estruturado
5. **Versionamento de packages** (renv + requirements.txt)
6. **Testes** quando aplicável (a implementar)
7. **Snakemake / Makefile** para orquestrar pipelines (a implementar)

---

> **Próximo passo:** criar `requirements.txt` + `renv.lock` para reprodutibilidade total.
