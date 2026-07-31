# 📦 Como Publicar no PyPI

> **Guia passo a passo** para publicar o package `neurociencia_edu` no PyPI (Python Package Index).
> **Status:** Opcional — só faça quando estiver estável.

---

## 🎯 Visão geral

Publicar no PyPI permite que outros pesquisadores instalem o package com:

```bash
pip install neurociencia-edu
```

## 📋 Pré-requisitos

1. ✅ Conta no [PyPI](https://pypi.org/account/register/)
2. ✅ Conta no [TestPyPI](https://test.pypi.org/account/register/) (para testes)
3. ✅ `pyproject.toml` configurado (já temos!)
4. ✅ `build` e `twine` instalados

## 🔧 Passo 1: Instalar ferramentas de build

```bash
pip install --upgrade build twine
```

## 🔧 Passo 2: Configurar credenciais

### Opção A: Token API (recomendado)

```
1. PyPI → Account settings → API tokens → "Add API token"
2. Scope: "Entire account" (primeira vez) ou "Project: neurociencia-edu" (depois)
3. Copie o token (pyt-...)
4. Configure:
   - Linux/Mac: criar ~/.pypirc
   - Windows: criar %USERPROFILE%\.pypirc
```

**~/.pypirc** (NÃO commite!):
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pyt-XXXXXXXXXXXXXXXX

[testpypi]
username = __token__
password = pyt-XXXXXXXXXXXXXXXX
```

### Opção B: Variáveis de ambiente (alternativa)

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pyt-XXXXXXXXXXXXXXXX
```

## 🔧 Passo 3: Testar localmente

```bash
# Construir
cd analise/Python
poetry build
# ou
python -m build

# Saída esperada em dist/:
# - neurociencia_edu-0.1.0-py3-none-any.whl
# - neurociencia_edu-0.1.0.tar.gz
```

## 🔧 Passo 4: Validar com `twine check`

```bash
twine check dist/*
# Saída esperada: PASSED
```

## 🔧 Passo 5: Publicar no TestPyPI (sempre!)

```bash
twine upload --repository testpypi dist/*
```

Depois teste a instalação:
```bash
pip install --index-url https://test.pypi.org/simple/ neurociencia-edu
```

## 🔧 Passo 6: Publicar no PyPI (produção)

```bash
twine upload dist/*
```

Saída esperada:
```
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: __token__
Enter your password: pyt-...
Uploading neurociencia_edu-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━ 30/30 kB
Uploading neurociencia_edu-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━ 40/40 kB

View at:
https://pypi.org/project/neurociencia-edu/0.1.0/
```

## 🔧 Passo 7: Verificar

🌐 https://pypi.org/project/neurociencia-edu/

```bash
# Em qualquer máquina
pip install neurociencia-edu
python -c "import neurociencia_edu; print(neurociencia_edu.__version__)"
```

## 🤖 Passo 8: Automatizar com GitHub Actions

Já temos `.github/workflows/pypi-publish.yml` (configurado neste commit).
Ele publica automaticamente quando você cria uma **Release** no GitHub.

### Como funciona:
1. Você cria uma tag: `git tag v0.1.0`
2. Push: `git push --tags`
3. Vai em GitHub → Releases → "Create release from tag"
4. Workflow trigga e publica automaticamente

### Configurar token no GitHub:
1. GitHub repo → Settings → Secrets and variables → Actions
2. New repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: seu token `pyt-...`
3. Save

## 📋 Checklist antes de publicar

- [ ] `pyproject.toml` tem `name`, `version`, `description`, `authors`, `license`, `readme`
- [ ] `LICENSE` está presente
- [ ] `README.md` está renderizando bem no PyPI
- [ ] Versão bumped em `__init__.py` e `pyproject.toml`
- [ ] `CHANGELOG.md` atualizado
- [ ] Testes passando (`pytest`)
- [ ] Lint passando (`ruff check`)
- [ ] Type check passando (`mypy`)
- [ ] Git tag criada
- [ ] Token PyPI configurado (se usando CI)

## 🔄 Versionamento semântico

| Versão | Quando |
|---|---|
| 0.x.y | Desenvolvimento (instável) |
| 1.0.0 | Primeira release estável |
| 1.1.0 | Nova funcionalidade (backward-compatible) |
| 1.1.1 | Bug fix |
| 2.0.0 | Breaking change |

## 🛠️ Comandos úteis

```bash
# Ver versão atual
poetry version

# Bump version
poetry version patch  # 0.1.0 → 0.1.1
poetry version minor  # 0.1.0 → 0.2.0
poetry version major  # 0.1.0 → 1.0.0

# Verificar tudo
poetry check
poetry lock

# Testar build
poetry build
```

## 🆘 Troubleshooting

### ❌ "File already exists"
Versão já foi publicada. Bump a versão.

### ❌ "Invalid distribution"
Rode `twine check dist/*` para identificar.

### ❌ "Authentication required"
Token inválido ou expirado. Gere novo.

### ❌ "Package name taken"
Escolha outro nome (e.g. `neurociencia-edu-ufrn`).

### ❌ "Long description not found"
Adicione `readme = "README.md"` no `pyproject.toml`.

## 📚 Referências

- [PyPI Official Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Poetry Publish](https://python-poetry.org/docs/cli/#publish)
- [GitHub Actions PyPI](https://github.com/marketplace/actions/pypi-publish)

---

**Última atualização:** 2026-07-31
**Mantenedor:** Programa de Pesquisa
