# 📊 Como Configurar Codecov (Python + R)

> **Guia específico** para configurar Codecov neste repositório, que tem
> **dois tipos de testes** (Python pytest + R testthat).

---

## 🎯 TL;DR (você já fez a maior parte!)

1. ✅ **Já feito:** Token salvo como `CODECOV_TOKEN` no GitHub Secrets
2. ⏭️ **Próximo:** O workflow vai triggar automaticamente
3. ⏭️ **Depois:** Configurar o `.codecov.yml` (já está configurado!)
4. ⏭️ **Ver:** Dashboard em https://codecov.io/gh/dronreef2/NeurocienciaEducacional

---

## 🔧 O que está configurado

### 1. Token (seu passo)
```
GitHub → Settings → Secrets and variables → Actions
Secret: CODECOV_TOKEN
```

### 2. Workflow Codecov (commit anterior + este)
- `.github/workflows/codecov.yml` — workflow dedicado
- `.github/workflows/ci.yml` — também tem upload inline
- Ambos usam `codecov/codecov-action@v5` com o token

### 3. Config Codecov (commit anterior)
- `.codecov.yml` — define targets, components, flags

---

## 🚀 Como funciona

Quando você fizer **push** para `main`:

1. **GitHub Actions** trigga `CI` workflow
2. CI roda:
   - `test-python` job → gera `coverage-python.xml`
   - `test-r` job → gera `coverage-r.xml`
3. **Codecov** workflow trigga (via `workflow_run` ou push direto)
4. Upload de ambos XMLs para Codecov
5. Dashboard atualizado em segundos

---

## 📋 Verificação rápida

Após o próximo push, você deve ver:

### 1. Em GitHub Actions
```
✅ CI / Test Python
✅ CI / Test R
✅ Codecov / Upload coverage to Codecov
```

### 2. Em codecov.io
- Acesse https://codecov.io/gh/dronreef2/NeurocienciaEducacional
- Deve mostrar: Python ~50%, R ~40% (valores iniciais)

### 3. No PR (futuro)
- Comentário automático com diff de coverage
- Check ✅ no merge se coverage não cair

---

## 🔍 Especificações do nosso setup

### Python
- **Ferramenta:** `pytest-cov`
- **Comando:** `pytest --cov=neurociencia_edu --cov-report=xml`
- **Output:** `analise/Python/coverage-python.xml`
- **Flag:** `python_package`
- **Source:** `analise/Python/neurociencia_edu/`

### R
- **Ferramenta:** `covr`
- **Comando:** `covr::to_cobertura(coverage, 'coverage-r.xml')`
- **Output:** `analise/R/coverage-r.xml`
- **Flag:** `r_package`
- **Source:** `analise/R/R/`

### Components
Definidos em `.codecov.yml`:
- `python_package` (path: `analise/Python/neurociencia_edu/**`)
- `r_package` (path: `analise/R/R/**`)
- `notebooks` (path: `**/notebooks/**`)

---

## 🛠️ Comandos locais (para debug)

### Python
```bash
cd analise/Python
pytest --cov=neurociencia_edu --cov-report=html
# Abre htmlcov/index.html
```

### R
```r
# Em R
devtools::test()  # Roda testes
covr::package_coverage()  # Gera cobertura
covr::report()  # Relatório HTML
```

---

## ❌ Troubleshooting

### "coverage file not found"
Causa: teste falhou antes de gerar o XML.

**Solução:** Verifique os logs do job `test-python` ou `test-r`.

### "Token invalid"
Causa: token expirou ou foi revogado.

**Solução:** Gere novo token em codecov.io e atualize `CODECOV_TOKEN` no GitHub.

### "Coverage report upload failed"
Causa: formato XML incorreto.

**Solução:** O Codecov aceita XML (Cobertura, JaCoCo) e JSON. Veja `.codecov.yml`.

### "Project coverage is 0%"
Causa: paths errados no `.codecov.yml`.

**Solução:** Verifique se os `paths` em `individual_components` batem com seus diretórios.

### Como ver os logs detalhados do upload
```yaml
# Em codecov-action
with:
  verbose: true  # ← já está configurado assim
```

---

## 📚 Referências

- [Codecov Docs](https://docs.codecov.com/)
- [GitHub Action v5](https://github.com/codecov/codecov-action)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [covr](https://covr.r-lib.org/)

---

**Última atualização:** 2026-07-31
**Mantenedor:** Programa de Pesquisa
