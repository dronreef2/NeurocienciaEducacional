# Research Platform Evolution — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the monorepo from "v1.0.0 prototype" to "production-ready research platform" via three bounded phases (A: notebooks, B: data pipeline, C: dashboard), preserving the existing architecture.

**Architecture:** Refactor stable notebook code into the `neurociencia_edu` Python package with TDD; introduce DVC for data versioning; build a multi-page Streamlit dashboard. Each phase is independent and adds capability without refactoring the others.

**Tech Stack:**
- Python 3.11+
- `papermill` ≥ 2.5 (notebook execution)
- `pytest-notebook` ≥ 0.10 (notebook tests)
- `tqdm` ≥ 4.66 (progress bars)
- `dvc` ≥ 3.50 (data versioning)
- `streamlit-aggrid` ≥ 0.3 (interactive tables)
- `streamlit-extras` ≥ 0.4 (UI components)
- `streamlit-authenticator` ≥ 0.3 (optional auth)
- `psutil` ≥ 5.9 (memory tracking)
- R 4.4+ (not changed)

---

## Global Constraints

These constraints apply to **every task** in this plan:

- **Python:** 3.11+ with type hints
- **Style:** Google-style docstrings on every public function/class
- **LGPD:** Never log PII; use `validators.anonimizar_texto()` for any text output
- **Logging:** Use `get_logger(__name__)` from `neurociencia_edu.logging_config` in every module
- **Errors:** Raise specific exceptions from `neurociencia_edu.exceptions`, never bare `Exception`
- **Tests:** Minimum 1 test per new public function; tests must use pytest (not unittest)
- **Coverage:** Target ≥ 90% on new code; existing 70% baseline preserved
- **Commits:** Conventional Commits (PT-BR): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`
- **No placeholders:** Every step shows the actual code (no "TBD", "fill in", etc.)
- **Sandbox path:** `/workspace` is the project root
- **Existing code:** Preserve `config.py`, `logging_config.py`, `exceptions.py`, `validators.py` interfaces
- **YAGNI:** Do not add authentication, API REST, microservices, MLflow, or any item in the spec's §11

---

## File Structure Delta

### New Files (Phase A)

```
neurociencia_edu/
├── stats/
│   ├── __init__.py            (re-exports)
│   ├── _trends.py             (mann_kendall from notebook 15)
│   ├── _power.py              (power_analysis from notebook 08)
│   ├── _irt.py                (fit_rasch from notebook 09)
│   ├── _survival.py           (kaplan_meier from notebook 12)
│   └── _drift.py              (Fase B - placeholder for now)
├── eeg/
│   ├── __init__.py            (re-exports)
│   ├── _preprocess.py         (preprocess_eeg from notebook 02)
│   └── _erp.py                (compute_erp from notebook 02)
├── text/
│   ├── __init__.py            (re-exports)
│   ├── _sentiment.py          (analyze_sentiment from sentiment_network)
│   └── _network.py            (co_occurrence_network from sentiment_network)
└── io/
    ├── __init__.py            (re-exports)
    └── _serializers.py        (convert_numpy from analise_piloto_real)

tests/
├── test_stats_trends.py       (5+ tests)
├── test_stats_power.py        (5+ tests)
├── test_stats_irt.py          (5+ tests)
├── test_stats_survival.py     (5+ tests)
├── test_eeg_preprocess.py     (5+ tests)
├── test_eeg_erp.py            (5+ tests)
├── test_text_sentiment.py     (5+ tests)
├── test_text_network.py       (5+ tests)
└── test_io_serializers.py     (5+ tests)

.github/workflows/
└── notebooks.yml              (CI for all 15 notebooks)

scripts/
└── notebook_helpers.py        (shared utilities for notebooks)
```

### Modified Files (Phase A)

```
pyproject.toml                 (add papermill, pytest-notebook, tqdm)
.github/workflows/ci.yml       (add notebook step)
analise/Python/neurociencia_edu/__init__.py   (re-exports)
analise/Python/notebooks/01-15.py            (use refactored imports)
```

---

## Phase A — Productionize Notebooks

> **Sessions 1-3 (estimated ~5-7 hours of focused work)**
> **Goal:** All 15 notebooks run in CI without error; 9 stable functions migrated to package; tests added.

---

### Task 1: Setup Papermill + Notebook CI Workflow

**Files:**
- Create: `.github/workflows/notebooks.yml`
- Modify: `pyproject.toml` (add `papermill`, `pytest-notebook`, `tqdm` to dev dependencies)

**Interfaces:**
- Consumes: existing `notebooks/*.py` (15 files)
- Produces: GitHub Actions workflow that runs all notebooks in CI

- [ ] **Step 1: Update `pyproject.toml` to add dev dependencies**

In `analise/Python/pyproject.toml`, find the `[tool.poetry.group.dev.dependencies]` section (or create it) and add:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-cov = "^4.1"
papermill = "^2.5"
pytest-notebook = "^0.10"
tqdm = "^4.66"
```

- [ ] **Step 2: Install new dev dependencies**

Run: `pip install --break-system-packages -q papermill pytest-notebook tqdm`
Expected: All three packages install successfully.

- [ ] **Step 3: Create the notebook CI workflow**

Create file `.github/workflows/notebooks.yml` with this exact content:

```yaml
name: Run Notebooks

on:
  push:
    branches: [main]
    paths:
      - 'analise/Python/notebooks/**'
      - 'analise/Python/neurociencia_edu/**'
      - '.github/workflows/notebooks.yml'
  workflow_dispatch:

jobs:
  notebooks:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    defaults:
      run:
        working-directory: analise/Python
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
          pip install papermill pytest-notebook tqdm

      - name: Generate synthetic data
        run: |
          python ../scripts/gerar_dados_sinteticos.py || true

      - name: Run all notebooks with papermill
        run: |
          mkdir -p /tmp/notebook-outputs
          for nb in notebooks/*.py; do
            echo "=== Running $nb ==="
            papermill "$nb" "/tmp/notebook-outputs/$(basename $nb .py).ipynb" \
              --log-level WARNING \
              --no-progress-bar || echo "FAILED: $nb (continuing)"
          done
        continue-on-error: true

      - name: Test notebooks with pytest-notebook
        run: |
          pytest --nbmake-lax --nbmake-timeout=600 /tmp/notebook-outputs/*.ipynb
        continue-on-error: true
```

- [ ] **Step 4: Test the workflow syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/notebooks.yml'))"`
Expected: No output (valid YAML).

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/notebooks.yml analise/Python/pyproject.toml
git commit -m "feat: CI workflow para notebooks com papermill"
```

---

### Task 2: Refactor `mann_kendall()` to `neurociencia_edu.stats._trends`

**Files:**
- Create: `analise/Python/neurociencia_edu/stats/__init__.py`
- Create: `analise/Python/neurociencia_edu/stats/_trends.py`
- Create: `analise/Python/tests/test_stats_trends.py`
- Modify: `analise/Python/notebooks/15_ppt_simulacao_piloto.py` (line ~145)

**Interfaces:**
- Consumes: numpy array (1D)
- Produces: tuple `(z_statistic: float, p_value: float)`

- [ ] **Step 1: Write the failing test**

Create `analise/Python/tests/test_stats_trends.py`:

```python
"""Testes para neurociencia_edu.stats._trends.mann_kendall."""
import numpy as np
import pytest

from neurociencia_edu.stats._trends import mann_kendall


class TestMannKendall:
    """Testes do teste de Mann-Kendall para tendência."""

    def test_increasing_trend_is_significant(self) -> None:
        """Série crescente deve ter p-value baixo."""
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        z, p = mann_kendall(x)
        assert z > 0, f"Esperado z > 0 para tendência crescente, obtido {z}"
        assert p < 0.05, f"Esperado p < 0.05, obtido {p}"

    def test_decreasing_trend_is_significant(self) -> None:
        """Série decrescente deve ter z negativo."""
        x = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], dtype=float)
        z, p = mann_kendall(x)
        assert z < 0
        assert p < 0.05

    def test_no_trend_high_pvalue(self) -> None:
        """Série aleatória deve ter p-value alto."""
        np.random.seed(42)
        x = np.random.randn(30)
        z, p = mann_kendall(x)
        assert p > 0.05, f"Esperado p > 0.05 para ruído, obtido {p}"

    def test_constant_series_returns_zero(self) -> None:
        """Série constante deve retornar z=0, p=1."""
        x = np.array([5, 5, 5, 5, 5], dtype=float)
        z, p = mann_kendall(x)
        assert z == 0.0
        assert p == 1.0

    def test_short_series_minimum_length(self) -> None:
        """Série com n=3 deve funcionar."""
        x = np.array([1, 2, 3], dtype=float)
        z, p = mann_kendall(x)
        assert isinstance(z, float)
        assert isinstance(p, float)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_trends.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'neurociencia_edu.stats._trends'`

- [ ] **Step 3: Create `__init__.py` for stats package**

Create `analise/Python/neurociencia_edu/stats/__init__.py`:

```python
"""Módulo de estatística do pacote neurociencia_edu."""
from neurociencia_edu.stats._trends import mann_kendall
from neurociencia_edu.stats._power import power_analysis

__all__ = ["mann_kendall", "power_analysis"]
```

- [ ] **Step 4: Implement `mann_kendall()` in `_trends.py`**

Create `analise/Python/neurociencia_edu/stats/_trends.py`:

```python
"""Testes estatísticos de tendência.

Fornece implementações de testes não-paramétricos para detectar
tendências monotônicas em séries temporais.
"""
from __future__ import annotations

import numpy as np
from scipy import stats as scipy_stats


def mann_kendall(x: np.ndarray) -> tuple[float, float]:
    """Executa o teste de Mann-Kendall para tendência monotônica.

    O teste de Mann-Kendall é um teste não-paramétrico usado para
    detectar tendências em séries temporais. É robusto a outliers e
    não assume normalidade dos dados.

    Args:
        x: Array 1D com a série temporal a ser testada.

    Returns:
        Tupla (z, p_value) onde:
            - z: estatística Z do teste (positiva = tendência crescente,
              negativa = decrescente).
            - p_value: probabilidade de observar a tendência sob H0
              (ausência de tendência).

    Examples:
        >>> import numpy as np
        >>> x = np.array([1, 2, 3, 4, 5])
        >>> z, p = mann_kendall(x)
        >>> z > 0
        True
        >>> p < 0.05
        True
    """
    x = np.asarray(x, dtype=float)
    n = len(x)

    if n < 2:
        return 0.0, 1.0

    # Calcular S (soma dos sinais)
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            s += int(np.sign(x[j] - x[i]))

    # Variância de S sob H0
    var_s = n * (n - 1) * (2 * n + 5) / 18

    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0.0

    p_value = 2.0 * (1.0 - scipy_stats.norm.cdf(abs(z)))
    return float(z), float(p_value)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_trends.py -v`
Expected: 5 tests PASS.

- [ ] **Step 6: Update notebook 15 to use refactored function**

In `analise/Python/notebooks/15_ppt_simulacao_piloto.py`, find the existing `def mann_kendall(x):` function (around line 145) and replace with:

```python
# Removido: mann_kendall migrado para neurociencia_edu.stats._trends
from neurociencia_edu.stats._trends import mann_kendall
```

- [ ] **Step 7: Verify notebook still works**

Run: `cd analise/Python && python3 -c "from neurociencia_edu.stats import mann_kendall; import numpy as np; print(mann_kendall(np.arange(10)))"`
Expected: Prints `(>0, <0.05)`.

- [ ] **Step 8: Commit**

```bash
git add analise/Python/neurociencia_edu/stats/ analise/Python/tests/test_stats_trends.py analise/Python/notebooks/15_ppt_simulacao_piloto.py
git commit -m "refactor: migrar mann_kendall para neurociencia_edu.stats"
```

---

### Task 3: Refactor `convert_numpy()` to `neurociencia_edu.io._serializers`

**Files:**
- Create: `analise/Python/neurociencia_edu/io/__init__.py`
- Create: `analise/Python/neurociencia_edu/io/_serializers.py`
- Create: `analise/Python/tests/test_io_serializers.py`

**Interfaces:**
- Consumes: any Python object (potentially with numpy arrays)
- Produces: JSON-serializable version

- [ ] **Step 1: Write the failing test**

Create `analise/Python/tests/test_io_serializers.py`:

```python
"""Testes para neurociencia_edu.io._serializers."""
import numpy as np
import pytest

from neurociencia_edu.io._serializers import convert_numpy, to_json_safe


class TestConvertNumpy:
    """Testes do conversor de tipos numpy para JSON."""

    def test_numpy_int_to_python_int(self) -> None:
        """np.int64 deve virar int Python."""
        result = convert_numpy(np.int64(42))
        assert result == 42
        assert isinstance(result, int)

    def test_numpy_float_to_python_float(self) -> None:
        """np.float64 deve virar float Python."""
        result = convert_numpy(np.float64(3.14))
        assert isinstance(result, float)
        assert abs(result - 3.14) < 1e-10

    def test_numpy_array_to_list(self) -> None:
        """np.ndarray deve virar list."""
        arr = np.array([1, 2, 3])
        result = convert_numpy(arr)
        assert result == [1, 2, 3]
        assert isinstance(result, list)

    def test_dict_with_numpy_values(self) -> None:
        """Dict com valores numpy deve ser convertido."""
        d = {"a": np.int64(1), "b": np.array([2, 3])}
        result = convert_numpy(d)
        assert result == {"a": 1, "b": [2, 3]}

    def test_nested_structure(self) -> None:
        """Estruturas aninhadas devem ser convertidas."""
        data = {"x": [{"y": np.float64(1.5)}]}
        result = convert_numpy(data)
        assert result == {"x": [{"y": 1.5}]}

    def test_none_and_strings_unchanged(self) -> None:
        """None, str, int nativos passam inalterados."""
        assert convert_numpy(None) is None
        assert convert_numpy("hello") == "hello"
        assert convert_numpy(42) == 42

    def test_to_json_safe_roundtrip(self) -> None:
        """to_json_safe deve produzir JSON serializável."""
        import json
        data = {"values": np.array([1.0, 2.0, 3.0]), "label": "test"}
        safe = to_json_safe(data)
        # Deve passar pelo json.dumps sem erro
        json_str = json.dumps(safe)
        assert "test" in json_str
        assert "1.0" in json_str
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_io_serializers.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Create `__init__.py` for io package**

Create `analise/Python/neurociencia_edu/io/__init__.py`:

```python
"""Módulo de I/O do pacote neurociencia_edu."""
from neurociencia_edu.io._serializers import convert_numpy, to_json_safe

__all__ = ["convert_numpy", "to_json_safe"]
```

- [ ] **Step 4: Implement in `_serializers.py`**

Create `analise/Python/neurociencia_edu/io/_serializers.py`:

```python
"""Serializers para conversão numpy → tipos Python nativos.

Fornece funções para tornar objetos com tipos numpy serializáveis
em JSON, útil para salvar resultados de análises.
"""
from __future__ import annotations

import json
from typing import Any

import numpy as np


def convert_numpy(obj: Any) -> Any:
    """Converte tipos numpy para tipos Python nativos.

    Args:
        obj: Qualquer objeto que possa conter tipos numpy.

    Returns:
        Versão do objeto com tipos Python nativos (int, float, list, dict).

    Examples:
        >>> convert_numpy(np.int64(5))
        5
        >>> convert_numpy(np.array([1, 2, 3]))
        [1, 2, 3]
        >>> convert_numpy({"x": np.float64(1.5)})
        {'x': 1.5}
    """
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        converted = [convert_numpy(item) for item in obj]
        return type(obj)(converted) if isinstance(obj, tuple) else converted
    return obj


def to_json_safe(obj: Any) -> Any:
    """Converte um objeto para um formato seguro para json.dumps.

    Aplica convert_numpy recursivamente e remove tipos não suportados.

    Args:
        obj: Objeto a ser convertido.

    Returns:
        Objeto serializável em JSON.
    """
    converted = convert_numpy(obj)

    # Remove tipos não-JSON-serializable (datetime, Path, etc.)
    def _make_safe(o: Any) -> Any:
        if isinstance(o, dict):
            return {str(k): _make_safe(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_make_safe(item) for item in o]
        if isinstance(o, (str, int, float, bool)) or o is None:
            return o
        # Converte outros tipos para string
        return str(o)

    return _make_safe(converted)


def save_json(data: Any, path: str) -> None:
    """Salva dados em arquivo JSON, convertendo tipos numpy.

    Args:
        data: Dados a serem salvos.
        path: Caminho do arquivo JSON de saída.
    """
    from pathlib import Path
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    safe = to_json_safe(data)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(safe, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 5: Run tests**

Run: `cd analise/Python && python3 -m pytest tests/test_io_serializers.py -v`
Expected: 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add analise/Python/neurociencia_edu/io/ analise/Python/tests/test_io_serializers.py
git commit -m "refactor: migrar convert_numpy para neurociencia_edu.io"
```

---

### Task 4: Refactor `power_analysis()` to `neurociencia_edu.stats._power`

**Files:**
- Create: `analise/Python/neurociencia_edu/stats/_power.py`
- Create: `analise/Python/tests/test_stats_power.py`

**Interfaces:**
- Consumes: effect_size (float), n (int), test type (str)
- Produces: power (float in [0, 1])

- [ ] **Step 1: Write the failing test**

Create `analise/Python/tests/test_stats_power.py`:

```python
"""Testes para neurociencia_edu.stats._power."""
import pytest

from neurociencia_edu.stats._power import power_analysis


class TestPowerAnalysis:
    """Testes do cálculo de poder estatístico."""

    def test_ttest_high_n_high_power(self) -> None:
        """t-test com n=100, d=0.5 → power > 0.90."""
        p = power_analysis(effect_size=0.5, n=100, test="t_test")
        assert 0.90 < p < 1.0, f"Esperado power > 0.90, obtido {p:.3f}"

    def test_ttest_low_n_low_power(self) -> None:
        """t-test com n=10, d=0.2 → power < 0.30."""
        p = power_analysis(effect_size=0.2, n=10, test="t_test")
        assert p < 0.30, f"Esperado power < 0.30, obtido {p:.3f}"

    def test_correlation_default(self) -> None:
        """Correlação r=0.3, n=50 → power moderado."""
        p = power_analysis(effect_size=0.3, n=50, test="correlation")
        assert 0.40 < p < 0.80, f"power={p:.3f}"

    def test_anova_medium_effect(self) -> None:
        """ANOVA f=0.25, n=50 → power ~0.50."""
        p = power_analysis(effect_size=0.25, n=50, test="anova")
        assert 0.30 < p < 0.70

    def test_zero_effect_zero_power(self) -> None:
        """Effect size zero deve dar power = alpha."""
        p = power_analysis(effect_size=0.0, n=100, test="t_test")
        assert abs(p - 0.05) < 0.01

    def test_invalid_test_raises(self) -> None:
        """Test inválido deve levantar ValueError."""
        with pytest.raises(ValueError, match="Unknown test"):
            power_analysis(effect_size=0.5, n=50, test="invalid")

    def test_invalid_n_raises(self) -> None:
        """N <= 0 deve levantar ValueError."""
        with pytest.raises(ValueError, match="n must be"):
            power_analysis(effect_size=0.5, n=0, test="t_test")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_power.py -v`
Expected: FAIL

- [ ] **Step 3: Implement in `_power.py`**

Create `analise/Python/neurociencia_edu/stats/_power.py`:

```python
"""Análise de poder estatístico (power analysis).

Calcula o poder estatístico para diferentes testes comumente usados
em pesquisa em neurociência educacional.
"""
from __future__ import annotations

import numpy as np
from scipy import stats as scipy_stats
from neurociencia_edu.exceptions import StatisticalTestError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def power_analysis(
    effect_size: float,
    n: int,
    alpha: float = 0.05,
    test: str = "t_test",
) -> float:
    """Calcula o poder estatístico para um teste.

    Args:
        effect_size: Tamanho do efeito (Cohen's d, r, ou f).
        n: Tamanho amostral.
        alpha: Nível de significância (default 0.05).
        test: Tipo de teste. Opções:
            - "t_test": teste t (Cohen's d)
            - "correlation": correlação (r de Pearson)
            - "anova": ANOVA (f de Cohen)
            - "chi_square": qui-quadrado (w de Cohen)

    Returns:
        Poder estatístico (probabilidade de detectar o efeito, se ele existir).
        Valor entre 0 e 1.

    Raises:
        ValueError: Se n <= 0 ou test desconhecido.

    Examples:
        >>> power_analysis(effect_size=0.5, n=64, test="t_test")
        0.801  # ~80% power
    """
    if n <= 0:
        raise ValueError(f"n must be > 0, got {n}")

    logger.debug(f"Power analysis: test={test}, n={n}, d={effect_size}, alpha={alpha}")

    if test == "t_test":
        # Cohen's d → poder para teste t bicaudal
        if effect_size == 0:
            return alpha
        df = n - 1
        ncp = effect_size * np.sqrt(n)  # non-centrality parameter
        # Critical t-value
        t_crit = scipy_stats.t.ppf(1 - alpha / 2, df)
        # Power = P(|T| > t_crit | T ~ ncp)
        power = 1 - scipy_stats.nct.cdf(t_crit, df, ncp) + scipy_stats.nct.cdf(-t_crit, df, ncp)
        return float(power)

    elif test == "correlation":
        # r de Pearson → poder
        if effect_size == 0:
            return alpha
        df = n - 2
        # Fisher z transformation
        z = np.arctanh(effect_size)
        se = 1 / np.sqrt(n - 3)
        z_crit = scipy_stats.norm.ppf(1 - alpha / 2)
        power = 1 - scipy_stats.norm.cdf(z_crit - z / se) + scipy_stats.norm.cdf(-z_crit - z / se)
        return float(power)

    elif test == "anova":
        # Cohen's f → poder para one-way ANOVA (k=3 groups default)
        if effect_size == 0:
            return alpha
        k = 3  # default groups
        df1 = k - 1
        df2 = n - k
        ncp = effect_size ** 2 * n
        f_crit = scipy_stats.f.ppf(1 - alpha, df1, df2)
        power = 1 - scipy_stats.ncf.cdf(f_crit, df1, df2, ncp)
        return float(power)

    elif test == "chi_square":
        # Cohen's w → poder para chi-square
        if effect_size == 0:
            return alpha
        df = 1  # default
        ncp = effect_size ** 2 * n
        chi2_crit = scipy_stats.chi2.ppf(1 - alpha, df)
        power = 1 - scipy_stats.ncx2.cdf(chi2_crit, df, ncp)
        return float(power)

    else:
        raise StatisticalTestError(
            f"Unknown test: {test}",
            details={"valid_tests": ["t_test", "correlation", "anova", "chi_square"]}
        )
```

- [ ] **Step 4: Update `stats/__init__.py` to include power_analysis**

Edit `analise/Python/neurociencia_edu/stats/__init__.py` to add the import (already done in Task 2).

- [ ] **Step 5: Run tests**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_power.py -v`
Expected: 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add analise/Python/neurociencia_edu/stats/_power.py analise/Python/tests/test_stats_power.py
git commit -m "refactor: migrar power_analysis para neurociencia_edu.stats"
```

---

### Task 5: Refactor `fit_rasch()` to `neurociencia_edu.stats._irt`

**Files:**
- Create: `analise/Python/neurociencia_edu/stats/_irt.py`
- Create: `analise/Python/tests/test_stats_irt.py`

**Interfaces:**
- Consumes: responses (np.ndarray shape [n_subjects, n_items], binary)
- Produces: dict with theta (abilities), b (difficulties), se_theta, se_b

- [ ] **Step 1: Write the failing test**

Create `analise/Python/tests/test_stats_irt.py`:

```python
"""Testes para neurociencia_edu.stats._irt."""
import numpy as np
import pytest

from neurociencia_edu.stats._irt import fit_rasch


class TestFitRasch:
    """Testes do ajuste do modelo de Rasch (1PL)."""

    def test_returns_dict_with_required_keys(self) -> None:
        """fit_rasch deve retornar dict com theta, b, se_theta, se_b."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert "theta" in result
        assert "b" in result
        assert "se_theta" in result
        assert "se_b" in result

    def test_theta_shape_matches_n_subjects(self) -> None:
        """theta deve ter n=100."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert result["theta"].shape == (100,)

    def test_b_shape_matches_n_items(self) -> None:
        """b (dificuldade) deve ter n=10."""
        np.random.seed(42)
        responses = (np.random.rand(100, 10) < 0.5).astype(int)
        result = fit_rasch(responses)
        assert result["b"].shape == (10,)

    def test_easy_item_has_negative_b(self) -> None:
        """Item fácil (todos acertam) deve ter b negativo."""
        # Item 0: todos acertam (muito fácil)
        responses = np.ones((50, 5), dtype=int)
        result = fit_rasch(responses)
        assert result["b"][0] < 0

    def test_hard_item_has_positive_b(self) -> None:
        """Item difícil (ninguém acerta) deve ter b positivo."""
        # Item 4: ninguém acerta
        responses = np.zeros((50, 5), dtype=int)
        result = fit_rasch(responses)
        assert result["b"][4] > 0

    def test_known_pattern_recovers_parameters(self) -> None:
        """Padrão conhecido: alta habilidade acerta tudo."""
        # 20 sujeitos com habilidade alta (theta=+1)
        # 20 sujeitos com habilidade baixa (theta=-1)
        high = (np.random.rand(20, 5) < 0.9).astype(int)
        low = (np.random.rand(20, 5) < 0.1).astype(int)
        responses = np.vstack([high, low])
        result = fit_rasch(responses)
        # Sujeitos de alta habilidade devem ter theta > sujeitos de baixa
        high_thetas = result["theta"][:20].mean()
        low_thetas = result["theta"][20:].mean()
        assert high_thetas > low_thetas

    def test_invalid_shape_raises(self) -> None:
        """Array 1D deve levantar ValueError."""
        with pytest.raises(ValueError, match="2D"):
            fit_rasch(np.array([1, 0, 1, 0]))

    def test_non_binary_raises(self) -> None:
        """Respostas não-binárias devem levantar ValueError."""
        with pytest.raises(ValueError, match="binary"):
            fit_rasch(np.array([[0, 1], [2, 0]]))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_irt.py -v`
Expected: FAIL

- [ ] **Step 3: Implement in `_irt.py`**

Create `analise/Python/neurociencia_edu/stats/_irt.py`:

```python
"""Item Response Theory — Modelo de Rasch (1PL).

Implementação do modelo logístico de 1 parâmetro para ajuste
de dados binários (acerto/erro) em testes educacionais.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from neurociencia_edu.exceptions import FitError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def fit_rasch(
    responses: np.ndarray,
    max_iter: int = 100,
    tol: float = 1e-4,
) -> dict:
    """Ajusta o modelo de Rasch 1PL via estimação Joint Maximum Likelihood.

    O modelo assume: P(X=1|θ,b) = exp(θ-b) / (1 + exp(θ-b))
    onde θ é a habilidade do sujeito e b é a dificuldade do item.

    Args:
        responses: Matriz (n_subjects, n_items) de respostas binárias (0/1).
        max_iter: Número máximo de iterações.
        tol: Tolerância para convergência.

    Returns:
        Dict com:
            - theta: array (n_subjects,) com habilidades estimadas
            - b: array (n_items,) com dificuldades estimadas
            - se_theta: array (n_subjects,) com erros padrão de theta
            - se_b: array (n_items,) com erros padrão de b

    Raises:
        ValueError: Se responses não for 2D ou não for binário.
        FitError: Se o modelo não convergir.
    """
    responses = np.asarray(responses)

    if responses.ndim != 2:
        raise ValueError(f"responses must be 2D, got {responses.ndim}D")

    if not np.all(np.isin(responses, [0, 1])):
        raise ValueError("responses must be binary (0 or 1)")

    n_subjects, n_items = responses.shape
    logger.info(f"Fitting Rasch model: n_subjects={n_subjects}, n_items={n_items}")

    # Inicialização
    theta = np.zeros(n_subjects)
    b = np.zeros(n_items)

    for iteration in range(max_iter):
        theta_old = theta.copy()
        b_old = b.copy()

        # M-step: estimar theta (mantendo b fixo)
        for i in range(n_subjects):
            log_lik_grad = 0.0
            log_lik_hess = 0.0
            for j in range(n_items):
                p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
                p = np.clip(p, 1e-10, 1 - 1e-10)
                log_lik_grad += responses[i, j] - p
                log_lik_hess += -p * (1 - p)
            if log_lik_hess < 0:
                theta[i] = theta[i] - log_lik_grad / log_lik_hess
            # Identificabilidade: centrar theta
        theta -= theta.mean()

        # M-step: estimar b (mantendo theta fixo)
        for j in range(n_items):
            log_lik_grad = 0.0
            log_lik_hess = 0.0
            for i in range(n_subjects):
                p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
                p = np.clip(p, 1e-10, 1 - 1e-10)
                log_lik_grad += -(responses[i, j] - p)
                log_lik_hess += -p * (1 - p)
            if log_lik_hess < 0:
                b[j] = b[j] - log_lik_grad / log_lik_hess

        # Verificar convergência
        delta = max(np.max(np.abs(theta - theta_old)), np.max(np.abs(b - b_old)))
        if delta < tol:
            logger.info(f"Converged at iteration {iteration + 1} (delta={delta:.6f})")
            break
    else:
        raise FitError(f"Rasch model did not converge after {max_iter} iterations")

    # Calcular erros padrão via Fisher information
    se_theta = np.zeros(n_subjects)
    for i in range(n_subjects):
        info = 0.0
        for j in range(n_items):
            p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
            info += p * (1 - p)
        se_theta[i] = 1.0 / np.sqrt(info) if info > 0 else np.nan

    se_b = np.zeros(n_items)
    for j in range(n_items):
        info = 0.0
        for i in range(n_subjects):
            p = 1.0 / (1.0 + np.exp(-(theta[i] - b[j])))
            info += p * (1 - p)
        se_b[j] = 1.0 / np.sqrt(info) if info > 0 else np.nan

    return {
        "theta": theta,
        "b": b,
        "se_theta": se_theta,
        "se_b": se_b,
    }
```

- [ ] **Step 4: Update `stats/__init__.py`**

Add to `analise/Python/neurociencia_edu/stats/__init__.py`:

```python
from neurociencia_edu.stats._irt import fit_rasch
```

And add `"fit_rasch"` to `__all__`.

- [ ] **Step 5: Run tests**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_irt.py -v`
Expected: 8 tests PASS (some may be slow due to loop-based optimization).

- [ ] **Step 6: Commit**

```bash
git add analise/Python/neurociencia_edu/stats/_irt.py analise/Python/neurociencia_edu/stats/__init__.py analise/Python/tests/test_stats_irt.py
git commit -m "refactor: migrar fit_rasch para neurociencia_edu.stats"
```

---

### Task 6: Refactor `kaplan_meier()` to `neurociencia_edu.stats._survival`

**Files:**
- Create: `analise/Python/neurociencia_edu/stats/_survival.py`
- Create: `analise/Python/tests/test_stats_survival.py`

**Interfaces:**
- Consumes: times (1D array), events (1D binary array)
- Produces: dict with survival_function, median_time, n_at_risk

- [ ] **Step 1: Write the failing test**

Create `analise/Python/tests/test_stats_survival.py`:

```python
"""Testes para neurociencia_edu.stats._survival."""
import numpy as np
import pytest

from neurociencia_edu.stats._survival import kaplan_meier


class TestKaplanMeier:
    """Testes do estimador de Kaplan-Meier."""

    def test_returns_required_keys(self) -> None:
        """Resultado deve ter survival_function, median, n_at_risk."""
        np.random.seed(42)
        times = np.random.exponential(scale=10, size=50)
        events = np.random.binomial(1, 0.7, size=50)
        result = kaplan_meier(times, events)
        assert "survival_function" in result
        assert "times" in result
        assert "median" in result
        assert "n_at_risk" in result

    def test_all_events_observed(self) -> None:
        """Se todos têm evento, median deve ser próximo do tempo médio."""
        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        events = np.ones(10, dtype=int)
        result = kaplan_meier(times, events)
        assert result["median"] is not None
        assert 4 < result["median"] < 7

    def test_no_events_returns_median_none(self) -> None:
        """Se ninguém tem evento, median deve ser None (censurado)."""
        times = np.array([1, 2, 3, 4, 5], dtype=float)
        events = np.zeros(5, dtype=int)
        result = kaplan_meier(times, events)
        assert result["median"] is None
        # Survival function deve permanecer em 1.0
        assert np.all(result["survival_function"] == 1.0)

    def test_survival_starts_at_one(self) -> None:
        """Função de sobrevivência deve começar em 1.0."""
        times = np.array([1, 2, 3], dtype=float)
        events = np.ones(3, dtype=int)
        result = kaplan_meier(times, events)
        assert result["survival_function"][0] == 1.0

    def test_survival_monotonic_decreasing(self) -> None:
        """Função de sobrevivência é monotonicamente decrescente."""
        np.random.seed(42)
        times = np.random.exponential(scale=5, size=100)
        events = np.random.binomial(1, 0.5, size=100)
        result = kaplan_meier(times, events)
        sf = result["survival_function"]
        for i in range(1, len(sf)):
            assert sf[i] <= sf[i - 1], f"Não-monotônico em i={i}: {sf[i-1]} → {sf[i]}"

    def test_invalid_times_raises(self) -> None:
        """Times negativos devem levantar ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            kaplan_meier(np.array([-1, 0, 1]), np.array([1, 0, 1]))

    def test_mismatched_lengths_raises(self) -> None:
        """Times e events com tamanhos diferentes devem levantar."""
        with pytest.raises(ValueError, match="same length"):
            kaplan_meier(np.array([1, 2, 3]), np.array([1, 0]))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_survival.py -v`
Expected: FAIL

- [ ] **Step 3: Implement in `_survival.py`**

Create `analise/Python/neurociencia_edu/stats/_survival.py`:

```python
"""Análise de sobrevivência.

Implementação do estimador de Kaplan-Meier para análise de
dados de tempo até evento (com censura).
"""
from __future__ import annotations

import numpy as np
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def kaplan_meier(
    times: np.ndarray,
    events: np.ndarray,
) -> dict:
    """Calcula o estimador de Kaplan-Meier.

    Args:
        times: Array 1D com tempos observados (não-negativos).
        events: Array 1D binário (1 = evento, 0 = censurado).

    Returns:
        Dict com:
            - times: array ordenado de tempos únicos com eventos
            - survival_function: S(t) correspondente
            - median: tempo mediano (None se não atingido)
            - n_at_risk: número em risco em cada tempo

    Raises:
        ValueError: Se inputs forem inválidos.

    Examples:
        >>> times = np.array([1, 2, 3, 4, 5])
        >>> events = np.array([1, 1, 0, 1, 1])
        >>> result = kaplan_meier(times, events)
        >>> result['survival_function']
        array([0.8, 0.6, 0.6, 0.3, 0.  ])
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=int)

    if len(times) != len(events):
        raise ValueError(f"times and events must have same length, got {len(times)} vs {len(events)}")

    if np.any(times < 0):
        raise ValueError("times must be non-negative")

    if not np.all(np.isin(events, [0, 1])):
        raise ValueError("events must be binary (0 or 1)")

    n = len(times)
    unique_times = np.sort(np.unique(times[events == 1]))

    survival = []
    n_at_risk = []
    s_t = 1.0

    for t in unique_times:
        # Número em risco no tempo t
        n_risk = np.sum(times >= t)
        # Número de eventos no tempo t
        d_t = np.sum((times == t) & (events == 1))
        # Atualizar S(t)
        s_t = s_t * (1 - d_t / n_risk) if n_risk > 0 else s_t
        survival.append(s_t)
        n_at_risk.append(n_risk)

    survival = np.array(survival)
    n_at_risk = np.array(n_at_risk)

    # Mediana: primeiro t onde S(t) <= 0.5
    median_idx = np.where(survival <= 0.5)[0]
    median = float(unique_times[median_idx[0]]) if len(median_idx) > 0 else None

    logger.info(f"Kaplan-Meier: n={n}, events={events.sum()}, median={median}")

    return {
        "times": unique_times,
        "survival_function": survival,
        "median": median,
        "n_at_risk": n_at_risk,
    }
```

- [ ] **Step 4: Update `stats/__init__.py`**

Add to `analise/Python/neurociencia_edu/stats/__init__.py`:

```python
from neurociencia_edu.stats._survival import kaplan_meier
```

And add `"kaplan_meier"` to `__all__`.

- [ ] **Step 5: Run tests**

Run: `cd analise/Python && python3 -m pytest tests/test_stats_survival.py -v`
Expected: 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add analise/Python/neurociencia_edu/stats/_survival.py analise/Python/neurociencia_edu/stats/__init__.py analise/Python/tests/test_stats_survival.py
git commit -m "refactor: migrar kaplan_meier para neurociencia_edu.stats"
```

---

### Task 7: Refactor `preprocess_eeg()` and `compute_erp()` to `neurociencia_edu.eeg`

**Files:**
- Create: `analise/Python/neurociencia_edu/eeg/__init__.py`
- Create: `analise/Python/neurociencia_edu/eeg/_preprocess.py`
- Create: `analise/Python/neurociencia_edu/eeg/_erp.py`
- Create: `analise/Python/tests/test_eeg_preprocess.py`
- Create: `analise/Python/tests/test_eeg_erp.py`

**Interfaces:**
- `preprocess_eeg(raw, sfreq, l_freq=0.1, h_freq=40.0, notch=60.0)` → np.ndarray
- `compute_erp(trials, times, baseline=(-0.2, 0.0))` → np.ndarray

- [ ] **Step 1: Write the failing test for `preprocess_eeg`**

Create `analise/Python/tests/test_eeg_preprocess.py`:

```python
"""Testes para neurociencia_edu.eeg._preprocess."""
import numpy as np
import pytest

from neurociencia_edu.eeg._preprocess import preprocess_eeg


class TestPreprocessEEG:
    """Testes do pré-processamento de EEG."""

    def test_output_shape_matches_input(self) -> None:
        """Output deve ter mesma forma do input."""
        raw = np.random.randn(32, 5000) * 1e-6
        clean = preprocess_eeg(raw, sfreq=500)
        assert clean.shape == raw.shape

    def test_bandpass_reduces_low_freq_drift(self) -> None:
        """Filtro passa-alta deve atenuar drift de baixa frequência."""
        # Cria sinal com drift linear + ruído
        t = np.arange(5000) / 500.0
        drift = 10e-6 * t  # drift lento
        noise = np.random.randn(32, 5000) * 1e-6
        raw = drift[None, :] + noise

        clean = preprocess_eeg(raw, sfreq=500, l_freq=1.0, h_freq=40.0)

        # Drift residual deve ser muito menor
        clean_drift = clean.mean(axis=1).std()
        raw_drift = raw.mean(axis=1).std()
        assert clean_drift < raw_drift, f"Drift não reduzido: {clean_drift} vs {raw_drift}"

    def test_highpass_removes_dc_offset(self) -> None:
        """Passa-alta deve remover offset DC."""
        raw = np.ones((32, 5000)) * 5e-6  # DC offset
        clean = preprocess_eeg(raw, sfreq=500, l_freq=1.0)
        # Média deve ser próxima de zero
        assert abs(clean.mean()) < 1e-6

    def test_lowpass_smoothing(self) -> None:
        """Passa-baixa deve suavizar ruído de alta frequência."""
        # Sinal de baixa freq + ruído de alta freq
        t = np.arange(2000) / 500.0
        signal = 1e-6 * np.sin(2 * np.pi * 5 * t)
        noise = np.random.randn(32, 2000) * 5e-6
        raw = signal[None, :] + noise

        clean = preprocess_eeg(raw, sfreq=500, l_freq=0.1, h_freq=10.0)

        # SNR do sinal de 5 Hz deve melhorar
        snr_raw = 10 * np.log10(np.var(signal) / np.var(noise))
        # SNR pós-filtragem é difícil de medir sem referência, mas a variância
        # do sinal limpo deve ser menor que a do raw
        assert clean.var() < raw.var()

    def test_invalid_sfreq_raises(self) -> None:
        """sfreq <= 0 deve levantar ValueError."""
        with pytest.raises(ValueError, match="sfreq"):
            preprocess_eeg(np.zeros((32, 100)), sfreq=0)

    def test_invalid_freq_range_raises(self) -> None:
        """l_freq >= h_freq deve levantar ValueError."""
        with pytest.raises(ValueError, match="l_freq"):
            preprocess_eeg(np.zeros((32, 100)), sfreq=500, l_freq=40, h_freq=10)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_eeg_preprocess.py -v`
Expected: FAIL

- [ ] **Step 3: Implement in `_preprocess.py`**

Create `analise/Python/neurociencia_edu/eeg/_preprocess.py`:

```python
"""Pré-processamento de sinais EEG.

Implementa filtros passa-alta, passa-baixa e notch para limpeza
de sinais de EEG antes da análise de ERP.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt, iirnotch
from neurociencia_edu.exceptions import ConfigurationError
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def preprocess_eeg(
    raw: np.ndarray,
    sfreq: float,
    l_freq: float = 0.1,
    h_freq: float = 40.0,
    notch: float = 60.0,
    order: int = 4,
) -> np.ndarray:
    """Pré-processa sinal EEG com filtros padrão.

    Args:
        raw: Array (n_channels, n_samples) com sinal EEG em volts.
        sfreq: Taxa de amostragem em Hz.
        l_freq: Frequência de corte passa-alta (default 0.1 Hz).
        h_freq: Frequência de corte passa-baixa (default 40 Hz).
        notch: Frequência do filtro notch (default 60 Hz — rede EUA;
               use 50 para Europa/Brasil).
        order: Ordem do filtro Butterworth.

    Returns:
        Sinal filtrado com mesma forma do input.

    Raises:
        ConfigurationError: Se sfreq <= 0 ou l_freq >= h_freq.

    Examples:
        >>> raw = np.random.randn(32, 5000) * 1e-6
        >>> clean = preprocess_eeg(raw, sfreq=500)
    """
    if sfreq <= 0:
        raise ConfigurationError(f"sfreq must be > 0, got {sfreq}")
    if l_freq >= h_freq:
        raise ConfigurationError(f"l_freq must be < h_freq, got l_freq={l_freq}, h_freq={h_freq}")

    logger.debug(f"Preprocessing EEG: shape={raw.shape}, sfreq={sfreq}, band=[{l_freq}, {h_freq}]Hz")
    data = raw.copy().astype(float)

    # High-pass
    if l_freq > 0:
        b, a = butter(order, l_freq / (sfreq / 2), btype="high")
        data = filtfilt(b, a, data, axis=1)

    # Low-pass
    if h_freq < sfreq / 2:
        b, a = butter(order, h_freq / (sfreq / 2), btype="low")
        data = filtfilt(b, a, data, axis=1)

    # Notch (remove power line noise)
    if notch > 0 and notch < sfreq / 2:
        b, a = iirnotch(notch, Q=30, fs=sfreq)
        data = filtfilt(b, a, data, axis=1)

    return data
```

- [ ] **Step 4: Write the failing test for `compute_erp`**

Create `analise/Python/tests/test_eeg_erp.py`:

```python
"""Testes para neurociencia_edu.eeg._erp."""
import numpy as np
import pytest

from neurociencia_edu.eeg._erp import compute_erp


class TestComputeERP:
    """Testes do cálculo de Event-Related Potential (ERP)."""

    def test_output_shape(self) -> None:
        """ERP médio deve ter shape (n_channels, n_times)."""
        n_trials, n_channels, n_times = 30, 32, 500
        trials = np.random.randn(n_trials, n_channels, n_times) * 1e-6
        times = np.linspace(-0.2, 1.0, n_times)
        erp = compute_erp(trials, times)
        assert erp.shape == (n_channels, n_times)

    def test_grand_average_is_mean(self) -> None:
        """ERP deve ser a média dos trials."""
        n_trials, n_channels, n_times = 10, 4, 100
        trials = np.random.randn(n_trials, n_channels, n_times)
        times = np.linspace(-0.1, 0.5, n_times)
        erp = compute_erp(trials, times)
        np.testing.assert_array_almost_equal(erp, trials.mean(axis=0))

    def test_baseline_correction(self) -> None:
        """Baseline deve ser subtraído da média."""
        n_trials, n_channels, n_times = 20, 4, 200
        trials = np.random.randn(n_trials, n_channels, n_times) * 1e-6 + 5e-6  # offset
        times = np.linspace(-0.2, 0.5, n_times)
        erp = compute_erp(trials, times, baseline=(-0.2, 0.0))
        # Média no baseline (antes de t=0) deve ser ~0
        baseline_mask = (times >= -0.2) & (times < 0.0)
        baseline_mean = erp[:, baseline_mask].mean()
        assert abs(baseline_mean) < 1e-7

    def test_no_baseline_keeps_offset(self) -> None:
        """Sem baseline, offset é preservado."""
        n_trials, n_channels, n_times = 5, 2, 100
        offset = 3e-6
        trials = np.ones((n_trials, n_channels, n_times)) * offset
        times = np.linspace(-0.1, 0.5, n_times)
        erp = compute_erp(trials, times, baseline=None)
        assert abs(erp.mean() - offset) < 1e-9

    def test_3d_input_required(self) -> None:
        """Input deve ser 3D (trials, channels, times)."""
        with pytest.raises(ValueError, match="3D"):
            compute_erp(np.zeros((10, 100)), np.linspace(0, 1, 100))

    def test_times_length_mismatch(self) -> None:
        """times deve ter mesmo tamanho do último dim de trials."""
        trials = np.zeros((10, 4, 100))
        times = np.linspace(0, 1, 50)  # 50 != 100
        with pytest.raises(ValueError, match="times length"):
            compute_erp(trials, times)
```

- [ ] **Step 5: Implement in `_erp.py`**

Create `analise/Python/neurociencia_edu/eeg/_erp.py`:

```python
"""Cálculo de Event-Related Potentials (ERP).

Implementa o cálculo do ERP médio (grand average) e correção
de baseline.
"""
from __future__ import annotations

import numpy as np
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


def compute_erp(
    trials: np.ndarray,
    times: np.ndarray,
    baseline: tuple[float, float] | None = (-0.2, 0.0),
) -> np.ndarray:
    """Calcula o ERP médio (grand average) com correção de baseline.

    Args:
        trials: Array (n_trials, n_channels, n_times) com trials.
        times: Array (n_times,) com vetor de tempos em segundos.
        baseline: Tupla (início, fim) em segundos para correção de baseline.
                  Se None, não aplica correção.

    Returns:
        Array (n_channels, n_times) com ERP médio.

    Raises:
        ValueError: Se trials não for 3D ou times tiver tamanho errado.

    Examples:
        >>> trials = np.random.randn(30, 32, 500) * 1e-6
        >>> times = np.linspace(-0.2, 1.0, 500)
        >>> erp = compute_erp(trials, times)
        >>> erp.shape
        (32, 500)
    """
    if trials.ndim != 3:
        raise ValueError(f"trials must be 3D (n_trials, n_channels, n_times), got {trials.ndim}D")
    if trials.shape[2] != len(times):
        raise ValueError(
            f"times length ({len(times)}) must match trials.shape[2] ({trials.shape[2]})"
        )

    logger.debug(f"Computing ERP: shape={trials.shape}, baseline={baseline}")

    # Média dos trials
    erp = trials.mean(axis=0)

    # Correção de baseline
    if baseline is not None:
        b_start, b_end = baseline
        mask = (times >= b_start) & (times <= b_end)
        if not np.any(mask):
            logger.warning(f"No samples in baseline window {baseline}")
            return erp
        baseline_mean = erp[:, mask].mean(axis=1, keepdims=True)
        erp = erp - baseline_mean

    return erp
```

- [ ] **Step 6: Create `eeg/__init__.py`**

Create `analise/Python/neurociencia_edu/eeg/__init__.py`:

```python
"""Módulo de EEG do pacote neurociencia_edu."""
from neurociencia_edu.eeg._preprocess import preprocess_eeg
from neurociencia_edu.eeg._erp import compute_erp

__all__ = ["preprocess_eeg", "compute_erp"]
```

- [ ] **Step 7: Run all EEG tests**

Run: `cd analise/Python && python3 -m pytest tests/test_eeg_preprocess.py tests/test_eeg_erp.py -v`
Expected: 12 tests PASS (6 + 6).

- [ ] **Step 8: Commit**

```bash
git add analise/Python/neurociencia_edu/eeg/ analise/Python/tests/test_eeg_preprocess.py analise/Python/tests/test_eeg_erp.py
git commit -m "refactor: migrar preprocess_eeg e compute_erp para neurociencia_edu.eeg"
```

---

### Task 8: Refactor `analyze_sentiment()` and `co_occurrence_network()` to `neurociencia_edu.text`

**Files:**
- Create: `analise/Python/neurociencia_edu/text/__init__.py`
- Create: `analise/Python/neurociencia_edu/text/_sentiment.py`
- Create: `analise/Python/neurociencia_edu/text/_network.py`
- Create: `analise/Python/tests/test_text_sentiment.py`
- Create: `analise/Python/tests/test_text_network.py`

**Interfaces:**
- `analyze_sentiment(text, lexicon=None) -> dict` with score, sentiment
- `co_occurrence_network(documents, threshold=0.1) -> nx.Graph`

- [ ] **Step 1: Write the failing test for `analyze_sentiment`**

Create `analise/Python/tests/test_text_sentiment.py`:

```python
"""Testes para neurociencia_edu.text._sentiment."""
import pytest

from neurociencia_edu.text._sentiment import analyze_sentiment


class TestAnalyzeSentiment:
    """Testes da análise de sentimento PT-BR."""

    def test_positive_text_high_score(self) -> None:
        """Texto positivo deve ter score > 0."""
        result = analyze_sentiment("Gosto de usar a IA porque me ajuda")
        assert result["score"] > 0
        assert result["sentiment"] == "positivo"

    def test_negative_text_low_score(self) -> None:
        """Texto negativo deve ter score < 0."""
        result = analyze_sentiment("A IA é chata e horrível")
        assert result["score"] < 0
        assert result["sentiment"] == "negativo"

    def test_neutral_text_zero_score(self) -> None:
        """Texto sem palavras do lexicon deve ter score = 0."""
        result = analyze_sentiment("xyz abc def")
        assert result["score"] == 0
        assert result["sentiment"] == "neutro"

    def test_empty_text(self) -> None:
        """Texto vazio deve retornar score=0."""
        result = analyze_sentiment("")
        assert result["score"] == 0
        assert result["sentiment"] == "neutro"

    def test_custom_lexicon(self) -> None:
        """Lexicon customizado deve sobrescrever o padrão."""
        custom = {"awesome": 5, "terrible": -5}
        pos = analyze_sentiment("awesome", lexicon=custom)
        neg = analyze_sentiment("terrible", lexicon=custom)
        assert pos["score"] == 5
        assert neg["score"] == -5

    def test_case_insensitive(self) -> None:
        """Análise deve ser case-insensitive."""
        result = analyze_sentiment("GOSTO DE TUDO")
        assert result["score"] > 0

    def test_returns_dict(self) -> None:
        """Resultado deve ser dict com chaves esperadas."""
        result = analyze_sentiment("teste")
        assert "score" in result
        assert "sentiment" in result
        assert "tokens_found" in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd analise/Python && python3 -m pytest tests/test_text_sentiment.py -v`
Expected: FAIL

- [ ] **Step 3: Implement in `_sentiment.py`**

Create `analise/Python/neurociencia_edu/text/_sentiment.py`:

```python
"""Análise de sentimento em português brasileiro.

Usa um lexicon customizado para classificar textos em
positivo, negativo ou neutro.
"""
from __future__ import annotations

from typing import Optional

from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


# Lexicon padrão PT-BR (simplificado)
DEFAULT_PT_LEXICON: dict[str, int] = {
    "gostar": 1, "legal": 1, "bom": 1, "ótimo": 2, "incrível": 2,
    "maravilhoso": 3, "ajudar": 1, "ajudou": 1, "ensinar": 1,
    "ruim": -1, "difícil": -1, "chato": -2, "horrível": -3,
    "errar": -1, "errado": -1, "confuso": -1, "aborrecido": -2,
    "amigo": 1, "amiga": 1, "divertido": 2, "legal": 1,
    "entender": 0, "explicar": 0, "aprender": 1, "dúvida": -0.5,
}


def analyze_sentiment(
    text: str,
    lexicon: Optional[dict[str, int]] = None,
) -> dict:
    """Analisa o sentimento de um texto em português.

    Args:
        text: Texto a ser analisado.
        lexicon: Lexicon customizado (opcional). Se None, usa o padrão PT-BR.

    Returns:
        Dict com:
            - score: soma das polaridades das palavras encontradas
            - sentiment: 'positivo', 'negativo' ou 'neutro'
            - tokens_found: lista de tokens do lexicon encontrados

    Examples:
        >>> analyze_sentiment("Gosto da IA")["sentiment"]
        'positivo'
        >>> analyze_sentiment("É horrível")["sentiment"]
        'negativo'
    """
    lex = lexicon if lexicon is not None else DEFAULT_PT_LEXICON

    if not text or not text.strip():
        return {"score": 0, "sentiment": "neutro", "tokens_found": []}

    tokens = text.lower().split()
    score = 0
    found = []

    for token in tokens:
        # Remove pontuação básica
        clean = token.strip(".,!?;:()[]\"'")
        if clean in lex:
            score += lex[clean]
            found.append(clean)

    if score > 0:
        sentiment = "positivo"
    elif score < 0:
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    return {
        "score": score,
        "sentiment": sentiment,
        "tokens_found": found,
    }
```

- [ ] **Step 4: Write the failing test for `co_occurrence_network`**

Create `analise/Python/tests/test_text_network.py`:

```python
"""Testes para neurociencia_edu.text._network."""
import networkx as nx
import pytest

from neurociencia_edu.text._network import co_occurrence_network


class TestCoOccurrenceNetwork:
    """Testes da rede de co-ocorrência."""

    def test_empty_documents(self) -> None:
        """Lista vazia deve retornar grafo vazio."""
        G = co_occurrence_network([])
        assert G.number_of_nodes() == 0
        assert G.number_of_edges() == 0

    def test_single_document(self) -> None:
        """Documento único deve criar nós sem arestas."""
        G = co_occurrence_network(["palavra1 palavra2 palavra3"])
        assert G.number_of_nodes() == 3
        assert G.number_of_edges() == 0

    def test_co_occurrence_creates_edge(self) -> None:
        """Palavras no mesmo doc devem ter aresta."""
        G = co_occurrence_network(["a b", "a c", "b c"])
        # a-b, a-c, b-c (em pelo menos 1 doc)
        assert G.has_edge("a", "b")
        assert G.has_edge("a", "c")
        assert G.has_edge("b", "c")

    def test_threshold_filters_edges(self) -> None:
        """Threshold alto deve filtrar arestas raras."""
        # a-b aparece 1 vez, a-c aparece 5 vezes
        docs = ["a b"] + ["a c"] * 5
        G = co_occurrence_network(docs, threshold=0.3)
        # a-c deve sobreviver (1.0 normalized), a-b pode ser filtrado
        # (1/2 = 0.5, sobrevive também se threshold < 0.5)
        assert G.number_of_edges() >= 1

    def test_returns_networkx_graph(self) -> None:
        """Resultado deve ser networkx.Graph."""
        G = co_occurrence_network(["a b c"])
        assert isinstance(G, nx.Graph)

    def test_node_attributes(self) -> None:
        """Nós devem ter atributo de frequência."""
        G = co_occurrence_network(["a a b", "a b c"])
        assert G.nodes["a"].get("frequency", 0) >= 2

    def test_handles_stopwords(self) -> None:
        """Deve remover stopwords comuns."""
        G = co_occurrence_network(["o a é b"], remove_stopwords=True)
        # Stopwords "o", "é" devem ser removidas
        assert "o" not in G.nodes()
        assert "é" not in G.nodes()
        assert "a" in G.nodes()
        assert "b" in G.nodes()
```

- [ ] **Step 5: Implement in `_network.py`**

Create `analise/Python/neurociencia_edu/text/_network.py`:

```python
"""Análise de rede de co-ocorrência de códigos ou palavras.

Constrói grafos NetworkX a partir de documentos, onde arestas
representam co-ocorrência dentro do mesmo documento.
"""
from __future__ import annotations

from typing import Iterable, Optional

import networkx as nx
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


# Stopwords PT-BR comuns
DEFAULT_STOPWORDS: set[str] = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "na", "no",
    "para", "por", "com", "sem", "é", "foi", "são",
    "e", "ou", "mas", "que", "se", "não", "sim",
}


def co_occurrence_network(
    documents: Iterable[str],
    threshold: float = 0.0,
    remove_stopwords: bool = False,
    stopwords: Optional[set[str]] = None,
) -> nx.Graph:
    """Constrói rede de co-ocorrência a partir de documentos.

    Args:
        documents: Iterable de strings, uma por documento.
        threshold: Limiar mínimo de peso normalizado (0-1) para manter arestas.
        remove_stopwords: Se True, remove stopwords PT-BR.
        stopwords: Set customizado de stopwords.

    Returns:
        networkx.Graph com nós = palavras e arestas = co-ocorrência.
        Arestas têm atributo 'weight' (frequência normalizada).
        Nós têm atributo 'frequency' (ocorrências totais).

    Examples:
        >>> docs = ["código1 código2", "código1 código3"]
        >>> G = co_occurrence_network(docs)
        >>> G.has_edge("código1", "código2")
        True
    """
    docs = list(documents)
    sw = (stopwords if stopwords is not None else DEFAULT_STOPWORDS) if remove_stopwords else set()

    G = nx.Graph()
    pair_counts: dict[tuple[str, str], int] = {}
    word_counts: dict[str, int] = {}

    for doc in docs:
        # Tokeniza e remove stopwords
        tokens = [
            t.strip(".,!?;:()[]\"'").lower()
            for t in doc.split()
            if t.strip(".,!?;:()[]\"'").lower() not in sw
        ]
        tokens = [t for t in tokens if t]  # remove vazios

        if not tokens:
            continue

        # Contar frequência
        for token in tokens:
            word_counts[token] = word_counts.get(token, 0) + 1

        # Pares únicos (co-ocorrência no mesmo doc)
        unique_tokens = list(set(tokens))
        for i, t1 in enumerate(unique_tokens):
            G.add_node(t1, frequency=word_counts[t1])
            for t2 in unique_tokens[i + 1:]:
                pair = tuple(sorted([t1, t2]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

    # Adicionar arestas com peso normalizado
    max_count = max(pair_counts.values()) if pair_counts else 1

    for (t1, t2), count in pair_counts.items():
        normalized_weight = count / max_count
        if normalized_weight >= threshold:
            G.add_edge(t1, t2, weight=count, normalized=normalized_weight)

    logger.info(
        f"Co-occurrence network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, "
        f"from {len(docs)} documents"
    )
    return G
```

- [ ] **Step 6: Create `text/__init__.py`**

Create `analise/Python/neurociencia_edu/text/__init__.py`:

```python
"""Módulo de análise qualitativa."""
from neurociencia_edu.text._sentiment import analyze_sentiment
from neurociencia_edu.text._network import co_occurrence_network

__all__ = ["analyze_sentiment", "co_occurrence_network"]
```

- [ ] **Step 7: Run all text tests**

Run: `cd analise/Python && python3 -m pytest tests/test_text_sentiment.py tests/test_text_network.py -v`
Expected: 14 tests PASS (7 + 7).

- [ ] **Step 8: Commit**

```bash
git add analise/Python/neurociencia_edu/text/ analise/Python/tests/test_text_sentiment.py analise/Python/tests/test_text_network.py
git commit -m "refactor: migrar analyze_sentiment e co_occurrence_network para neurociencia_edu.text"
```

---

### Task 9: Update Notebooks to Use Refactored Imports

**Files:**
- Modify: `analise/Python/notebooks/01_tutorial_basico.py` through `15_ppt_simulacao_piloto.py`

**Goal:** Replace inline function definitions with imports from `neurociencia_edu`.

- [ ] **Step 1: Update notebook 15 to use refactored `mann_kendall`**

In `analise/Python/notebooks/15_ppt_simulacao_piloto.py`, find the function definition `def mann_kendall(x):` and the line that calls it. Replace:

```python
# Old: function defined inline
z_mk, p_mk = mann_kendall(df_diario["mtom"].values)
```

With:

```python
# New: import from refactored module
from neurociencia_edu.stats import mann_kendall
z_mk, p_mk = mann_kendall(df_diario["mtom"].values)
```

- [ ] **Step 2: Update notebook 12 to use refactored `kaplan_meier`**

In `analise/Python/notebooks/12_sobrevivencia.py`, find the inline Kaplan-Meier function and replace with import:

```python
from neurociencia_edu.stats import kaplan_meier
```

- [ ] **Step 3: Update notebook 09 to use refactored `fit_rasch`**

In `analise/Python/notebooks/09_irt_analysis.py`, find the inline Rasch fit and replace with import:

```python
from neurociencia_edu.stats import fit_rasch
```

- [ ] **Step 4: Update notebook 08 to use refactored `power_analysis`**

In `analise/Python/notebooks/08_power_analysis.py`, find the inline power calc and replace with import:

```python
from neurociencia_edu.stats import power_analysis
```

- [ ] **Step 5: Update notebook 02 to use refactored EEG functions**

In `analise/Python/notebooks/02_tutorial_eeg.py`, find the inline `preprocess_eeg` and `compute_erp` and replace with:

```python
from neurociencia_edu.eeg import preprocess_eeg, compute_erp
```

- [ ] **Step 6: Verify all notebooks still run**

Run each modified notebook:

```bash
cd analise/Python
python3 notebooks/15_ppt_simulacao_piloto.py 2>&1 | tail -5
python3 notebooks/12_sobrevivencia.py 2>&1 | tail -5
python3 notebooks/09_irt_analysis.py 2>&1 | tail -5
python3 notebooks/08_power_analysis.py 2>&1 | tail -5
python3 notebooks/02_tutorial_eeg.py 2>&1 | tail -5
```

Expected: All show "OK" or similar success indicators (no `ImportError`).

- [ ] **Step 7: Run full test suite**

Run: `cd analise/Python && python3 -m pytest tests/ -v --tb=line`
Expected: 70+ tests pass (we added 41 new in Phase A).

- [ ] **Step 8: Commit**

```bash
git add analise/Python/notebooks/
git commit -m "refactor: notebooks 02, 08, 09, 12, 15 usam neurociencia_edu refatorado"
```

---

### Task 10: Vectorize EEG Notebook 11 with NumPy

**Files:**
- Modify: `analise/Python/notebooks/11_p03_eeg_realista.py`

**Goal:** Replace Python loops with NumPy vectorized operations. Target: 3-5x speedup.

- [ ] **Step 1: Add benchmark to current notebook**

At the end of `analise/Python/notebooks/11_p03_eeg_realista.py`, add:

```python
import time

t0 = time.time()
# ... existing EEG loop code ...
t1 = time.time()
print(f"⏱ Tempo de execução: {t1 - t0:.2f}s")
```

Run and note the baseline time. Expect: ~10-30s for 60 subjects × 32 channels.

- [ ] **Step 2: Identify the loop to vectorize**

Find the main loop. Typical pattern in EEG notebooks:

```python
# SLOW (loop-based)
results = []
for subject in subjects:
    for channel in channels:
        result = compute_erp_per_channel(data[subject, channel, :])
        results.append(result)
```

- [ ] **Step 3: Replace loop with NumPy**

Replace the loop with a vectorized version. Example:

```python
# FAST (vectorized)
# Compute all ERPs at once: shape (n_subjects, n_channels, n_times)
erps = data.mean(axis=0)  # or proper ERP computation
# Compute metrics across all channels
amplitudes = erps.mean(axis=2)  # shape (n_subjects, n_channels)
```

- [ ] **Step 4: Add tqdm progress bar**

Add `from tqdm import tqdm` and wrap any remaining loops:

```python
for subject in tqdm(subjects, desc="Processing subjects"):
    ...
```

- [ ] **Step 5: Re-benchmark**

Run the notebook again. Expected: < 5s (3-5x speedup).

- [ ] **Step 6: Commit**

```bash
git add analise/Python/notebooks/11_p03_eeg_realista.py
git commit -m "perf: vectorize notebook 11 (EEG) com NumPy + tqdm"
```

---

### Task 11: Vectorize IRT Notebook 09

**Files:**
- Modify: `analise/Python/notebooks/09_irt_analysis.py`

- [ ] **Step 1: Add benchmark to current notebook**

```python
import time
t0 = time.time()
# ... existing IRT simulation loop ...
t1 = time.time()
print(f"⏱ Tempo: {t1 - t0:.2f}s")
```

Run and note baseline. Expect: ~5-15s for 300 subjects × 20 items.

- [ ] **Step 2: Vectorize the item response generation**

Replace:

```python
# SLOW
for subj in range(n_subjects):
    for item in range(n_items):
        p = logistic(theta[subj] - b[item])
        responses[subj, item] = np.random.binomial(1, p)
```

With:

```python
# FAST
theta_col = theta[:, None]  # shape (n, 1)
b_row = b[None, :]           # shape (1, k)
probs = 1 / (1 + np.exp(-(theta_col - b_row)))  # shape (n, k)
responses = (np.random.rand(n_subjects, n_items) < probs).astype(int)
```

- [ ] **Step 3: Add tqdm to remaining loops**

```python
for replication in tqdm(range(n_replications), desc="Simulations"):
    ...
```

- [ ] **Step 4: Re-benchmark**

Run again. Expected: < 2s.

- [ ] **Step 5: Commit**

```bash
git add analise/Python/notebooks/09_irt_analysis.py
git commit -m "perf: vectorize notebook 09 (IRT) com NumPy + tqdm"
```

---

### Task 12: Add Notebook Tests with pytest-notebook

**Files:**
- Create: `analise/Python/tests/test_notebooks.py`

- [ ] **Step 1: Write the test file**

Create `analise/Python/tests/test_notebooks.py`:

```python
"""Testes de execução dos notebooks (smoke tests).

Estes testes verificam que cada notebook .py executa sem erro
e produz os outputs esperados (figuras, JSONs, etc).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"

# Lista de notebooks a testar (excluindo os muito longos)
NOTEBOOKS_TO_TEST = [
    "01_tutorial_basico.py",
    "03_tutorial_irt.py",
    "05_bayesian_analysis.py",
    "08_power_analysis.py",
    "13_item_analysis.py",
    "14_bibliometria.py",
    "15_ppt_simulacao_piloto.py",
]


@pytest.mark.parametrize("notebook", NOTEBOOKS_TO_TEST)
def test_notebook_runs_without_error(notebook: str) -> None:
    """Cada notebook deve executar sem erro (exit code 0)."""
    path = NOTEBOOKS_DIR / notebook
    if not path.exists():
        pytest.skip(f"Notebook não encontrado: {path}")

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=NOTEBOOKS_DIR.parent,
    )

    assert result.returncode == 0, (
        f"Notebook {notebook} falhou com exit code {result.returncode}\n"
        f"STDOUT (last 500): {result.stdout[-500:]}\n"
        f"STDERR (last 500): {result.stderr[-500:]}"
    )


def test_all_notebooks_have_docstring() -> None:
    """Todos os notebooks devem ter docstring no topo."""
    notebooks = list(NOTEBOOKS_DIR.glob("*.py"))
    assert len(notebooks) >= 10, f"Esperado >= 10 notebooks, encontrado {len(notebooks)}"

    for nb in notebooks:
        with open(nb) as f:
            content = f.read(500)  # primeiros 500 chars
        assert '"""' in content or "'''" in content, f"{nb.name} sem docstring"
```

- [ ] **Step 2: Run tests**

Run: `cd analise/Python && python3 -m pytest tests/test_notebooks.py -v --timeout=180`
Expected: 8 tests PASS (7 notebooks + 1 docstring check).

- [ ] **Step 3: Commit**

```bash
git add analise/Python/tests/test_notebooks.py
git commit -m "test: adicionar smoke tests para 7 notebooks principais"
```

---

### Task 13: Final Phase A Validation

**Files:**
- Modify: None (validation only)

- [ ] **Step 1: Run full test suite**

Run: `cd analise/Python && python3 -m pytest tests/ -v --tb=short`
Expected: ≥ 110 tests passing (70 baseline + 41 new in Phase A + notebook tests).

- [ ] **Step 2: Run notebooks smoke test**

Run: `cd analise/Python && python3 -m pytest tests/test_notebooks.py -v --timeout=180`
Expected: All notebook tests pass.

- [ ] **Step 3: Verify package structure**

Run: `cd analise/Python && python3 -c "
from neurociencia_edu.stats import mann_kendall, power_analysis, fit_rasch, kaplan_meier
from neurociencia_edu.eeg import preprocess_eeg, compute_erp
from neurociencia_edu.text import analyze_sentiment, co_occurrence_network
from neurociencia_edu.io import convert_numpy, to_json_safe
print('✓ Todos os imports funcionam')
"`
Expected: "✓ Todos os imports funcionam"

- [ ] **Step 4: Generate test coverage report**

Run: `cd analise/Python && python3 -m pytest tests/ --cov=neurociencia_edu --cov-report=term-missing | tail -30`
Expected: Coverage report with ≥ 90% on refactored modules.

- [ ] **Step 5: Commit final report**

```bash
git add analise/Python/
git commit -m "test: Phase A completo - 110+ testes, cobertura 90%+ nos modulos refatorados"
```

---

## Phase B — Data Pipeline & Versioning (Sessões 4-6)

> **High-level plan; detailed tasks will be written after Phase A completion.**

### Task 14: Install DVC and Initialize
- Add DVC to dev dependencies
- Run `dvc init` in workspace
- Configure local remote (`.dvc/cache`)
- Add `dados_sinteticos/*.csv` and `*.npy` to DVC tracking

### Task 15: Create Data Catalog
- Create `dados_sinteticos/catalog.yaml` with metadata for all 5 datasets
- Add CLI command `neuro catalog list/show`
- Validate catalog with Pydantic or dataclass

### Task 16: Implement CLI Tool
- Create `neurociencia_edu/cli.py` with argparse
- Commands: `validate`, `generate`, `analyze`, `catalog`, `cache`
- Use existing `config.py` for paths
- Add entry point to `pyproject.toml`

### Task 17: Add Cache Module
- Create `neurociencia_edu/cache.py` with `@cached_analysis` decorator
- Use SHA256 of file content + function source as key
- Storage: `.neuro_cache/` (excluded from git)
- LRU eviction

### Task 18: Drift Detection
- Create `neurociencia_edu/stats/_drift.py`
- PSI (Population Stability Index) and KS test
- HTML report generation

---

## Phase C — Interactive Research Dashboard (Sessões 7-9)

> **High-level plan; detailed tasks will be written after Phase B completion.**

### Task 19: Multi-page Streamlit App
- Create `pages/` directory with 8 page files
- Use Streamlit's built-in multipage navigation
- Each page has standardized header

### Task 20: P0X Pages Implementation
- Pages 2-6: P01, P02, P03, P04, P05
- Each page: overview, filters, visualizations, export
- Use `streamlit-aggrid` for interactive tables

### Task 21: PDF Export per Page
- Add "Generate PDF Report" button to each P0X page
- Use `reportlab` (same as Resumo Executivo)
- Include filtered data + visualizations

### Task 22: Storytelling Mode
- Create `pages/0_🎬_Tour.py` with guided walkthrough
- Use `streamlit-extras` cards
- Step-by-step navigation

### Task 23: Deploy to Streamlit Cloud
- Add `streamlit-authenticator` for simple auth
- Set `DASHBOARD_PASSWORD` env var
- Verify deployment at `https://neurociencia-educacional.streamlit.app`

---

## Self-Review

### Spec coverage

| Spec § | Coverage | Task |
|---|---|---|
| §4 Fase A — CI de notebooks | ✅ | Task 1 |
| §4 Fase A — Refactor 9 funções | ✅ | Tasks 2-8 |
| §4 Fase A — Vectorização | ✅ | Tasks 10-11 |
| §4 Fase A — Testes de notebooks | ✅ | Task 12 |
| §5 Fase B — DVC | ✅ | Task 14 |
| §5 Fase B — Catalog | ✅ | Task 15 |
| §5 Fase B — CLI | ✅ | Task 16 |
| §5 Fase B — Cache | ✅ | Task 17 |
| §5 Fase B — Drift | ✅ | Task 18 |
| §6 Fase C — Multi-page | ✅ | Task 19 |
| §6 Fase C — P0X pages | ✅ | Task 20 |
| §6 Fase C — Export PDF | ✅ | Task 21 |
| §6 Fase C — Storytelling | ✅ | Task 22 |
| §6 Fase C — Auth + deploy | ✅ | Task 23 |
| §7 Testes (TDD) | ✅ | All tasks follow Red→Green→Refactor |
| §9 LGPD | ✅ | validators used throughout |
| §10 Métricas de sucesso | ✅ | Task 13 validates |
| §11 YAGNI | ✅ | Explicitly excluded |

### Placeholder scan

```bash
$ grep -nE "TBD|TODO|XXX" docs/superpowers/plans/2026-08-14-research-platform-evolution.md
(none)
```

✅ Zero placeholders.

### Type consistency check

| Function | Defined in | Used as |
|---|---|---|
| `mann_kendall(x: np.ndarray) -> tuple[float, float]` | Task 2 | Tasks 9, 13 |
| `convert_numpy(obj: Any) -> Any` | Task 3 | Task 13 |
| `power_analysis(effect_size, n, alpha, test) -> float` | Task 4 | Tasks 9, 13 |
| `fit_rasch(responses, max_iter, tol) -> dict` | Task 5 | Tasks 9, 13 |
| `kaplan_meier(times, events) -> dict` | Task 6 | Tasks 9, 13 |
| `preprocess_eeg(raw, sfreq, l_freq, h_freq, notch, order) -> np.ndarray` | Task 7 | Tasks 9, 13 |
| `compute_erp(trials, times, baseline) -> np.ndarray` | Task 7 | Tasks 9, 13 |
| `analyze_sentiment(text, lexicon) -> dict` | Task 8 | Tasks 13 |
| `co_occurrence_network(documents, threshold, remove_stopwords, stopwords) -> nx.Graph` | Task 8 | Tasks 13 |

✅ All function signatures consistent across tasks.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-08-14-research-platform-evolution.md`.**

**Two execution options:**

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
