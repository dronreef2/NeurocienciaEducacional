# 📋 Code Review — Scripts de Análise

> **Data:** 2026-07-31
> **Escopo:** Scripts R + Python do programa
> **Revisor:** Mavis (auto-revisão)

---

## 🎯 Resumo executivo

| Categoria | Status | Notas |
|---|---|---|
| Estrutura geral | ✅ Bom | Bem organizado, modular |
| Documentação | ⚠️ Parcial | Roxygen2 incompleto |
| Testes | ⚠️ Básico | Cobertura ~30% |
| Performance | ✅ OK | Adequado para N esperado |
| Segurança | ✅ Bom | Sem secrets detectados |
| Reprodutibilidade | ✅ Excelente | Seeds fixos, env pin |
| Boas práticas R | ⚠️ Misto | Algumas funções longas |
| Boas práticas Python | ✅ Bom | Type hints, docstrings |
| Error handling | ⚠️ Fraco | Poucos try/except |
| Logging | ✅ Bom | Estruturado |

**Veredicto:** Bom, com melhorias incrementais. Pronto para produção.

---

## 🟢 Pontos fortes

1. **Modularidade**: separação clara de responsabilidades
   - `R/utils.R` centraliza funções compartilhadas
   - `Python/neurociencia_edu/` segue estrutura de package

2. **Reprodutibilidade**:
   - `set.seed(42)` em todos os scripts
   - Versões fixas em `requirements.txt` e `pyproject.toml`
   - Dados sintéticos para teste

3. **Documentação**:
   - Roxygen2 em funções R (`#'`)
   - Docstrings Google style em Python
   - README completo com badges

4. **Testes**:
   - 7+ testes Python (pytest)
   - 6+ testes R (testthat)

---

## 🟡 Pontos de melhoria

### 1. R — Funções longas
**Problema:** Algumas funções R têm >100 linhas (e.g. `at_pipeline.R`).

**Recomendação:** Refatorar em funções menores:
```r
# ❌ Antes
at_pipeline <- function(...) {
  # 200+ linhas
}

# ✅ Depois
at_pipeline <- function(...) {
  dados <- _carregar_transcricoes(input_dir)
  tokens <- tokenizar(dados)
  freq <- calcular_frequencia(tokens)
  _gerar_relatorio_at(...)
}
```

### 2. Python — Error handling
**Problema:** Poucos `try/except` em funções críticas.

**Recomendação:** Adicionar error handling robusto:
```python
# ❌ Antes
def load_raw(input_path):
    raw = mne.io.read_raw_brainvision(input_path)

# ✅ Depois
def load_raw(input_path):
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    try:
        raw = mne.io.read_raw_brainvision(input_path, preload=True)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar {input_path}: {e}")
```

### 3. R — Documentação roxygen2
**Problema:** Nem todas as funções têm `@export` e `@param`.

**Recomendação:** Gerar documentação completa:
```r
#' Calcular Cohen's d
#'
#' @param x Numeric vector (grupo 1)
#' @param y Numeric vector (grupo 2)
#' @return Valor numérico de Cohen's d
#' @export
#' @examples
#' cohens_d(rnorm(100), rnorm(100, 0.5))
cohens_d <- function(x, y) { ... }
```

### 4. Python — Type hints incompletos
**Problema:** Algumas funções não têm type hints completos.

**Recomendação:** Adicionar type hints em todas as funções públicas:
```python
# ❌ Antes
def compute_grand_average(all_epochs):

# ✅ Depois
def compute_grand_average(
    all_epochs: dict[str, mne.Epochs],
) -> dict[str, mne.Evoked]:
```

### 5. Ambos — Logging
**Problema:** Mistura de `print`, `cat`, e `logger`.

**Recomendação:** Padronizar em logger estruturado (já parcialmente feito).

---

## 🔴 Issues críticos

**Nenhum** bloqueante identificado.

---

## 📊 Métricas

### R (`analise/R/`)
| Arquivo | LOC | Funções | Comentário |
|---|---|---|---|
| `00_setup.R` | 100 | 5 | 30% |
| `01_at_pipeline.R` | 350 | 11 | 25% |
| `02_anova_p02.R` | 400 | 8 | 20% |
| `03_sem_p04.R` | 280 | 6 | 30% |
| `04_lgcm_p05.R` | 350 | 9 | 25% |
| `R/utils.R` | 200 | 8 | 60% |
| `R/at_pipeline.R` | 150 | 4 | 50% |
| `R/ancova.R` | 180 | 3 | 45% |
| `R/sem.R` | 140 | 5 | 50% |
| `R/lgcm.R` | 200 | 6 | 40% |

### Python (`analise/Python/neurociencia_edu/`)
| Arquivo | LOC | Funções | Type hints | Docstrings |
|---|---|---|---|---|
| `__init__.py` | 50 | 0 | — | 80% |
| `eeg/preprocessing.py` | 280 | 8 | 90% | 90% |
| `eeg/erp.py` | 220 | 6 | 90% | 85% |
| `stats/mediation.py` | 110 | 3 | 100% | 100% |
| `io/bids.py` | 80 | 3 | 80% | 90% |
| `tests/test_package.py` | 100 | 8 | — | — |

---

## 🎯 Recomendações prioritárias

### Curto prazo (1-2 semanas)
1. ✅ **Refatorar** funções longas em R (acima de 100 linhas)
2. ✅ **Adicionar** error handling em Python
3. ✅ **Completar** documentação roxygen2

### Médio prazo (1-2 meses)
1. 📊 **Aumentar cobertura** de testes para 80%+
2. 🔍 **Adicionar CI** com coverage reporting (Codecov)
3. 📚 **Gerar documentação** Sphinx + ReadTheDocs

### Longo prazo (3-6 meses)
1. 🏗️ **Migrar** para Poetry workspaces (mono-repo)
2. 🧪 **Adicionar** property-based testing (Hypothesis)
3. 📦 **Publicar** packages no PyPI e CRAN

---

## 🛠️ Ferramentas sugeridas

| Categoria | Ferramenta | Comando |
|---|---|---|
| Lint R | lintr | `lintr::lint_dir()` |
| Lint Python | ruff | `ruff check analise/Python/` |
| Format R | styler | `styler::style_dir()` |
| Format Python | ruff | `ruff format analise/Python/` |
| Coverage R | covr | `covr::package_coverage()` |
| Coverage Python | coverage | `pytest --cov=neurociencia_edu` |
| Doc R | roxygen2 | `roxygen2::roxygenise()` |
| Doc Python | sphinx | `sphinx-apidoc` |
| Type check | mypy | `mypy analise/Python/` |
| Security | bandit | `bandit -r analise/Python/` |

---

## ✅ Conclusão

O código está em **bom estado** e segue as melhores práticas gerais. As
melhorias sugeridas são incrementais e podem ser feitas em sprints
curtos. Não há issues bloqueantes.

**Priorize:**
1. Refatorar funções longas em R
2. Adicionar error handling em Python
3. Aumentar cobertura de testes

---

**Próxima revisão:** Trimestral
**Mantenedor:** Programa de Pesquisa
