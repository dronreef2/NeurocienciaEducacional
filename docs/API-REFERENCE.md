# 📖 API Reference — neurociencia_edu

> **Documentação completa do pacote Python `neurociencia_edu`**
> **Versão:** 0.1.0
> **Para:** Desenvolvedores, contribuidores

---

## 📦 Instalação

```bash
pip install neurociencia-edu
# ou do repositório:
pip install git+https://github.com/dronreef2/NeurocienciaEducacional.git
```

## 🏗️ Estrutura do Pacote

```
neurociencia_edu/
├── __init__.py
├── eeg/
│   ├── preprocessing.py  # preprocess_eeg()
│   └── erp.py            # compute_erp(), grand_average()
├── stats/
│   ├── ancova.py         # run_ancova()
│   ├── mediation.py      # run_mediation()
│   ├── sem.py            # run_sem()
│   ├── irt.py            # fit_rasch()
│   ├── power.py          # power_analysis()
│   └── mixed.py          # fit_mixed_model()
├── io/
│   ├── bids.py           # load_transcripts()
│   ├── validators.py     # validate_csv()
│   └── transformers.py   # transform_data()
├── text/
│   ├── sentiment.py      # analyze_sentiment()
│   └── network.py        # co_occurrence_network()
└── visualization/
    ├── plots.py          # plot_forest(), plot_kaplan_meier()
    └── reports.py        # generate_html_report()
```

## 🔌 Módulos Principais

### `eeg.preprocessing`

#### `preprocess_eeg(raw, sfreq, l_freq=0.1, h_freq=40.0, notch=60.0)`
Aplica pré-processamento padrão a dados EEG brutos.

**Parâmetros:**
- `raw` (np.ndarray): array (n_channels, n_samples) com sinal EEG em volts
- `sfreq` (float): taxa de amostragem em Hz
- `l_freq` (float): corte passa-alta (default 0.1 Hz)
- `h_freq` (float): corte passa-baixa (default 40 Hz)
- `notch` (float): frequência para filtro notch (default 60 Hz, rede EUA)

**Retorna:**
- `np.ndarray`: sinal limpo (mesma forma)

**Exemplo:**
```python
import neurociencia_edu as ne
import numpy as np

# Dados simulados
eeg = np.random.randn(32, 5000) * 1e-6  # 32 canais, 10s a 500Hz

clean = ne.preprocess_eeg(eeg, sfreq=500)
print(clean.shape)  # (32, 5000)
```

#### `compute_erp(trials, times, baseline=(-0.2, 0.0))`
Calcula Event-Related Potential (ERP) médio.

**Parâmetros:**
- `trials` (np.ndarray): (n_trials, n_channels, n_times)
- `times` (np.ndarray): vetor de tempos em segundos
- `baseline` (tuple): janela de baseline (início, fim) em segundos

**Retorna:**
- `np.ndarray`: ERP médio (n_channels, n_times)

### `stats.ancova`

#### `run_ancova(data, outcome, predictor, covariates)`
Realiza ANCOVA.

**Exemplo:**
```python
import pandas as pd
import neurociencia_edu as ne

df = pd.DataFrame({
    "y": [10, 12, 15, 18, 20, 22, 25, 28],
    "group": ["A"]*4 + ["B"]*4,
    "baseline": [8, 10, 12, 14, 16, 18, 20, 22],
    "age": [7, 8, 7, 9, 8, 8, 9, 8]
})

result = ne.run_ancova(
    data=df, outcome="y", predictor="group",
    covariates=["baseline", "age"]
)
print(result.summary())
```

### `stats.mediation`

#### `run_mediation(data, x_var, m_var, y_var, n_bootstrap=5000)`
Testa modelo de mediação simples (X → M → Y) com bootstrap.

**Exemplo:**
```python
df = pd.DataFrame({
    "X": np.random.randn(200),
    "M": np.random.randn(200),
    "Y": np.random.randn(200)
})

result = ne.run_mediation(df, "X", "M", "Y")
print(f"Indireto: {result['indirect']:.3f}")
print(f"IC 95%: [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
```

### `stats.sem`

#### `run_sem(model_spec, data, estimator='MLM')`
Modelagem de Equações Estruturais.

**Exemplo:**
```python
model = """
  # Modelo de medida
  FE =~ fe1 + fe2 + fe3
  Eng =~ eng1 + eng2 + eng3

  # Modelo estrutural
  Eng ~ IA
  FE ~ Eng + IA
"""

result = ne.run_sem(model, data=df)
print(f"CFI: {result['cfi']:.3f}, RMSEA: {result['rmsea']:.3f}")
```

### `stats.irt`

#### `fit_rasch(responses)`
Calibra modelo de Rasch 1PL.

**Parâmetros:**
- `responses` (np.ndarray): matriz (n_subjects, n_items) de respostas binárias (0/1)

**Retorna:**
- `dict` com:
  - `theta`: habilidades estimadas (n_subjects,)
  - `b`: dificuldades estimadas (n_items,)
  - `se_theta`: erro padrão de theta
  - `se_b`: erro padrão de b

**Exemplo:**
```python
import numpy as np
import neurociencia_edu as ne

# 300 sujeitos, 20 itens
responses = (np.random.rand(300, 20) < 0.5).astype(int)

result = ne.fit_rasch(responses)
print(f"θ médio: {result['theta'].mean():.2f}")
print(f"b médio: {result['b'].mean():.2f}")
```

### `stats.power`

#### `power_analysis(effect_size, n, alpha=0.05, test='t_test')`
Calcula poder estatístico.

**Exemplos:**
```python
# t-test pareado
power = ne.power_analysis(effect_size=0.5, n=30, test="t_test")

# Correlação
power = ne.power_analysis(effect_size=0.3, n=100, test="correlation")

# ANOVA
power = ne.power_analysis(effect_size=0.25, n=50, test="anova")
```

### `stats.mixed`

#### `fit_mixed_model(data, formula, groups, re_formula=None)`
Mixed-effects model.

**Exemplo:**
```python
import neurociencia_edu as ne

model = ne.fit_mixed_model(
    data=df,
    formula="score ~ time + group",
    groups="child_id",
    re_formula="~time"
)
print(model.summary())
```

### `text.sentiment`

#### `analyze_sentiment(texts, language='pt')`
Análise de sentimento em textos.

**Exemplo:**
```python
texts = ["Eu gosto do Khanmigo", "É muito difícil", "Aprendi fração!"]
results = ne.analyze_sentiment(texts, language="pt")
for t, r in zip(texts, results):
    print(f"{r['score']:+.2f}: {t}")
```

### `text.network`

#### `co_occurrence_network(documents, threshold=0.1)`
Constrói rede de co-ocorrência.

**Exemplo:**
```python
docs = ["código1 código2 código3", "código1 código4", ...]
G = ne.co_occurrence_network(docs)
print(f"Nós: {G.number_of_nodes()}, Arestas: {G.number_of_edges()}")
```

### `io.bids`

#### `load_transcripts(input_dir, anonymize=True)`
Carrega transcrições anonimizadas.

**Exemplo:**
```python
transcripts = ne.load_transcripts("dados/transcricoes/", anonymize=True)
for id, text in transcripts.items():
    print(f"{id}: {text[:100]}...")
```

### `io.validators`

#### `validate_csv(filepath, required_columns, range_checks=None)`
Valida um CSV.

**Exemplo:**
```python
result = ne.validate_csv(
    "dados/diario.csv",
    required_columns=["data", "participante_id", "duracao_min"],
    range_checks={"duracao_min": (0, 1440)}
)
print(result["valid"], result["issues"])
```

## 🎨 Visualização

### `visualization.plots`

```python
import neurociencia_edu as ne

# Forest plot (para meta-análise)
ne.plot_forest(effects, ci_lowers, ci_uppers, labels)

# Kaplan-Meier
ne.plot_kaplan_meier(times, events, group_col="sex")

# ERPs
ne.plot_erp(erp_data, times, channels)
```

## 🔗 Workflows Típicos

### Workflow 1: P01 (Análise Temática)
```python
import neurociencia_edu as ne

# 1. Carregar
transcripts = ne.load_transcripts("dados/transcricoes/")
codebook = ne.load_codebook("dados/codebook.csv")

# 2. Analisar
analysis = ne.run_thematic_analysis(
    transcripts, codebook,
    method="reflexive"
)

# 3. Visualizar
ne.plot_themes(analysis)
```

### Workflow 2: P03 (EEG)
```python
# 1. Carregar EEG (formato BIDS)
raw = ne.load_eeg_bids("dados/eeg/")

# 2. Pré-processar
clean = ne.preprocess_eeg(raw, sfreq=500)

# 3. Calcular ERPs
erps = ne.compute_erp(clean, events)

# 4. Análise estatística
results = ne.analyze_erps(erps, conditions=["papel", "tela"])
```

### Workflow 3: P05 (LGCM)
```python
# Rodar tutorial LGCM (R)
# (Veja analise/R/notebooks/05_tutorial_lgcm.R)
```

## 🐛 Tratamento de Erros

```python
from neurociencia_edu.exceptions import FitError, ValidationError

try:
    result = ne.fit_rasch(responses)
except FitError as e:
    print(f"Erro no ajuste: {e}")
except ValidationError as e:
    print(f"Dados inválidos: {e}")
```

## 📊 Versão

```python
import neurociencia_edu as ne
print(ne.__version__)  # 0.1.0
```

## 📚 Ver também

- [Tutoriais Jupyter](../analise/Python/notebooks/)
- [Notebooks de análise](../analise/Python/notebooks/)
- [Guias em R](../analise/R/)
- [CHANGELOG](../../CHANGELOG.md)
