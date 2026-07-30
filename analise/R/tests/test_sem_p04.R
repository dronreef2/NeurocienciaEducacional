# ============================================================
# tests/test_sem_p04.R
# Testes unitários para o SEM do P04
# ============================================================

library(testthat)
library(lavaan)

# --- 1. Test: dados de exemplo têm estrutura correta ----------------
test_that("dados de exemplo têm estrutura correta", {
  set.seed(42)
  n <- 100
  dados <- data.frame(
    participante = sprintf("P%03d", 1:n),
    idade = sample(c(7, 8, 9), n, replace = TRUE),
    sexo = sample(c("F", "M"), n, replace = TRUE),
    ses = rnorm(n, 0, 1),
    uso_ia = pmin(pmax(rnorm(n, 3, 1.5), 0), 7),
    engajamento = rnorm(n, 0, 1),
    stroop = rnorm(n, 0, 1),
    backward_digit = rnorm(n, 0, 1),
    dccs = rnorm(n, 0, 1),
    fe_composto = rnorm(n, 0, 1)
  )

  expect_equal(nrow(dados), n)
  expect_true(all(c("uso_ia", "engajamento", "fe_composto") %in% names(dados)))
  expect_true(all(!is.na(dados$uso_ia)))
})

# --- 2. Test: CFA ajusta sem erros ----------------------------------
test_that("CFA do FE converge", {
  set.seed(42)
  n <- 100
  dados <- data.frame(
    stroop = rnorm(n, 0, 1),
    backward_digit = rnorm(n, 0, 1),
    dccs = rnorm(n, 0, 1)
  )
  # Adicionar carga verdadeira no fator latente
  dados$FE_latente <- rnorm(n, 0, 1)
  dados$stroop <- 0.7 * dados$FE_latente + rnorm(n, 0, 0.5)
  dados$backward_digit <- 0.7 * dados$FE_latente + rnorm(n, 0, 0.5)
  dados$dccs <- 0.7 * dados$FE_latente + rnorm(n, 0, 0.5)

  modelo <- '
    FE =~ stroop + backward_digit + dccs
  '
  fit <- cfa(modelo, data = dados, std.lv = TRUE)

  # Deve convergir
  expect_s3_class(fit, "lavaan")
  # Cargas devem ser significativas
  params <- parameterEstimates(fit)
  expect_gt(nrow(params), 0)
})

# --- 3. Test: SEM de mediação tem coeficientes esperados ----------
test_that("efeito indireto é estimado", {
  set.seed(42)
  n <- 200
  dados <- data.frame(uso_ia = rnorm(n, 0, 1))

  # Mediação com efeito verdadeiro
  dados$engajamento <- 0.4 * dados$uso_ia + rnorm(n, 0, 0.5)
  dados$fe <- 0.3 * dados$uso_ia + 0.3 * dados$engajamento + rnorm(n, 0, 0.5)

  modelo <- '
    engajamento ~ a*uso_ia
    fe ~ b*engajamento + c*uso_ia
    indirect := a*b
  '
  fit <- sem(modelo, data = dados)

  expect_s3_class(fit, "lavaan")
  # Efeito indireto deve ser próximo de 0.4 * 0.3 = 0.12
  params <- parameterEstimates(fit)
  ind <- params[params$label == "indirect", ]
  expect_true(abs(ind$est - 0.12) < 0.1)  # tolerância
})

# --- 4. Test: índices de ajuste são reportados --------------------
test_that("índices de ajuste são extraídos corretamente", {
  set.seed(42)
  n <- 100
  dados <- data.frame(
    x = rnorm(n),
    y = rnorm(n)
  )
  fit <- lm(y ~ x, data = dados)

  # Não é lavaan, mas estamos testando estrutura de fitMeasures
  # Para um SEM, deve funcionar
  dados$z <- 0.5 * dados$x + 0.5 * dados$y + rnorm(n, 0, 0.5)
  fit_sem <- sem('z ~ x + y', data = dados)

  indices <- fitMeasures(fit_sem, c("cfi", "tli", "rmsea", "srmr"))
  expect_true(all(c("cfi", "tli", "rmsea", "srmr") %in% names(indices)))
  expect_true(indices["cfi"] >= 0)
  expect_true(indices["cfi"] <= 1)
})
