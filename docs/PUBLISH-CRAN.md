# 📦 Como Publicar no CRAN

> **Guia passo a passo** para publicar o package R `neurocienciasedu` no CRAN.
> **Status:** Opcional — só faça quando estiver estável.
> **Aviso:** CRAN tem regras **bem estritas**; revise tudo com cuidado.

---

## 🎯 Visão geral

Publicar no CRAN permite que R users instalem com:

```r
install.packages("neurocienciasedu")
```

## 📋 Pré-requisitos

1. ✅ Conta no [CRAN](https://cran.r-project.org/) (após primeira submissão bem-sucedida)
2. ✅ R 4.4.x instalado
3. ✅ `devtools`, `roxygen2` instalados
4. ✅ DESCRIPTION com metadados corretos
5. ✅ Todos os testes passando
6. ✅ Documentação completa (`man/*.Rd`)

## 🔧 Passo 1: Configurar DESCRIPTION

Já temos `analise/R/DESCRIPTION`. Verificar:

```r
Package: neurocienciasedu
Type: Package
Title: Case Sensitive Title (max 65 chars)
Version: 0.1.0
Authors@R: person(...)
Description: Longer description (~150-200 chars, starts with capital, ends with period)
License: MIT + file LICENSE
Encoding: UTF-8
LazyData: true
URL: https://github.com/dronreef2/NeurocienciaEducacional
BugReports: https://github.com/dronreef2/NeurocienciaEducacional/issues
```

**⚠️ Regras CRAN importantes:**
- Title: ≤ 65 caracteres, em **Title Case**
- Description: começar maiúsculo, terminar com ponto
- Authors@R (não Author + Maintainer)
- License: SPDX válido (`MIT + file LICENSE`)

## 🔧 Passo 2: LICENSE

```bash
cd analise/R
cp /caminho/do/LICENSE .
```

Conteúdo de LICENSE:
```
YEAR: 2026
COPYRIGHT HOLDER: Programa de Pesquisa em Neurociência Educacional
```

## 🔧 Passo 3: Documentação roxygen2

```r
# Em analise/R/
roxygen2::roxygenise()
```

Gera `man/*.Rd` automaticamente das tags `#'` no código.

## 🔧 Passo 4: Testes testthat

```r
# Todos os testes devem passar
devtools::test()
```

## 🔧 Passo 5: Verificação CRAN

**Antes de submeter, RODE ESTES:**

```r
# 1. Verificar documentação
devtools::check_man()

# 2. Verificar com configuração CRAN
devtools::check(args = c("--as-cran"))

# Saída esperada:
# 0 errors ✓ | 0 warnings ✓ | 0 notes ✓
```

**CRAN é estrito:**
- ❌ 0 errors (obrigatório)
- ⚠️ 0 warnings (fortemente recomendado)
- 📝 0 notes (ideal, mas alguns são OK)

**Erros comuns:**
- `\donttest{}` faltando em exemplos que demoram
- `library()` em vez de `requireNamespace()`
- `print()` em funções sem `invisible()`
- URLs quebradas
- Encoding UTF-8 issues

## 🔧 Passo 6: Verificação multi-plataforma

CRAN roda em Linux, Windows, macOS. Você precisa testar em pelo menos 2:

```r
# macOS (R CMD check)
system("R CMD check --as-cran neurocienciasedu_0.1.0.tar.gz")

# Ou via devtools
devtools::check(document = FALSE, args = c("--as-cran", "--no-manual"))
```

## 🔧 Passo 7: Build do tarball

```r
# Em analise/R/
devtools::build()
# Saída: neurocienciasedu_0.1.0.tar.gz
```

## 🔧 Passo 8: Submissão ao CRAN

### Opção A: Via web (primeira vez)
1. Vá para https://cran.r-project.org/submit.html
2. Leia as instruções
3. Upload: `neurocienciasedu_0.1.0.tar.gz`
4. Preencha:
   - Name: seu nome
   - Email: email válido (CRAN vai te contatar)
5. Submit

### Opção B: Via terminal (com `devtools`)
```r
devtools::submit_cran()
# Pede confirmação, depois envia
```

## 🔧 Passo 9: Aguardar revisão

- ⏰ CRAN tem **fila** — pode levar dias ou semanas
- 📧 Você receberá email com decisões:
  - ✅ **Accepted** (publicado!)
  - ⚠️ **Needs changes** (corrija e re-submeta)
  - ❌ **Rejected** (raro, geralmente por problemas graves)

## 🔧 Passo 10: Após aceitação

Seu package aparece em https://cran.r-project.org/package=neurocienciasedu

Agora pode ser instalado por qualquer pessoa:
```r
install.packages("neurocienciasedu")
```

## 🤖 Passo 11: Automatizar com GitHub Actions

Já temos o workflow configurado. Ele:
1. Faz check com `--as-cran` em Linux + Windows + macOS
2. Verifica cobertura
3. Faz build

Para **submeter automaticamente** ao CRAN via CI, recomenda-se ferramenta
[`rhub`](https://github.com/r-hub/rhub) ou [`cran-comments`](https://github.com/ropensci/cran-comments).

## 📋 Checklist CRAN

- [ ] DESCRIPTION com metadados válidos
- [ ] LICENSE presente
- [ ] NAMESPACE exporta tudo
- [ ] man/*.Rd gerados (roxygen2)
- [ ] Testes passando (`devtools::test()`)
- [ ] `devtools::check()` sem errors
- [ ] `devtools::check(args = "--as-cran")` sem errors
- [ ] Exemplos em help pages rodando rápido
- [ ] `\donttest{}` em exemplos demorados (>5s)
- [ ] vignettes/ opcional mas recomendado
- [ ] NEWS.md com mudanças
- [ ] URL + BugReports preenchidos

## 🔄 Versionamento

| Versão | Quando |
|---|---|
| 0.0.x | Desenvolvimento inicial |
| 0.1.0 | Primeira versão "funcionando" |
| 0.x.y | Iterações antes de 1.0 |
| 1.0.0 | API estável |
| 1.x.y | Backward-compatible |
| x.0.0 | Breaking change |

Para CRAN, **não pode** ter `.9000` (dev versions).

## 🛠️ Comandos úteis

```r
# Atualizar version
usethis::use_version("patch")  # 0.1.0 → 0.1.1
usethis::use_version("minor")  # 0.1.0 → 0.2.0
usethis::use_version("major")  # 0.1.0 → 1.0.0

# Verificar tudo
devtools::check()

# Documentação
devtools::document()

# Testes
devtools::test()
```

## 🆘 Troubleshooting CRAN

### ❌ "Non-ASCII characters"
Adicione `Encoding: UTF-8` no DESCRIPTION e use apenas ASCII.

### ❌ "Examples too long"
Use `\donttest{}` ou `\dontrun{}` em exemplos demorados.

### ❌ "Undeclared dependencies"
Declare todos os pacotes em DESCRIPTION.

### ❌ "License not recognized"
Use formato SPDX: `MIT + file LICENSE` ou `GPL-3`.

### ❌ "Author field failed"
Use `Authors@R: person(...)` com `role = c("aut", "cre")`.

## 📚 Referências

- [R Packages (2e) by Hadley Wickham](https://r-pkgs.org/)
- [CRAN Repository Policy](https://cran.r-project.org/web/packages/policies.html)
- [Submitting to CRAN](https://r-pkgs.org/release.html)

---

**Última atualização:** 2026-07-31
**Mantenedor:** Programa de Pesquisa
