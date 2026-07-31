# Testes para funções utilitárias
library(testthat)
library(neurocienciasedu)

test_that("limpar_texto normaliza corretamente", {
  expect_equal(limpar_texto("OLÁ"), "ola")
  expect_equal(limpar_texto("criança"), "crianca")
  expect_equal(limpar_texto("Olá, mundo!"), "ola  mundo")
  expect_equal(limpar_texto("Tenho 25 anos"), "tenho   anos")
  expect_equal(limpar_texto("  texto  "), "texto")
})

test_that("limpar_texto rejeita input inválido", {
  expect_error(limpar_texto(123))
  expect_error(limpar_texto(NA))
})

test_that("obter_stop_words_pt retorna tibble válido", {
  sw <- obter_stop_words_pt()
  expect_s3_class(sw, "tbl_df")
  expect_true("palabra" %in% names(sw))
  expect_gt(nrow(sw), 10)
})

test_that("cohens_d calcula corretamente", {
  set.seed(42)
  x <- rnorm(100, 0, 1)
  y <- rnorm(100, 0.5, 1)
  d <- cohens_d(x, y)
  expect_true(is.numeric(d))
  expect_true(d < 0)  # x menor que y
  expect_true(abs(d + 0.5) < 0.3)  # próximo de -0.5
})

test_that("cohens_d retorna 0 quando pooled_sd é 0", {
  x <- rep(1, 10)
  y <- rep(2, 10)
  d <- cohens_d(x, y)
  expect_equal(d, 0)
})

test_that("log_msg imprime mensagem formatada", {
  expect_output(log_msg("teste"), "\\[.*\\] INFO: teste")
  expect_output(log_msg("erro", level = "ERROR"), "ERROR")
})

test_that("calcular_frequencia retorna tibble ordenado", {
  tokens <- tibble::tibble(
    participante = c("C01", "C01", "C02", "C02", "C02"),
    palabra = c("a", "a", "b", "b", "c")
  )
  freq <- calcular_frequencia(tokens)
  expect_s3_class(freq, "tbl_df")
  expect_equal(freq$n[1], 2)  # "b" ou "a" tem 2
  expect_true(all(freq$n >= freq$n[2:length(freq$n)]))  # ordenado
})

test_that("calcular_tfidf identifica palavras características", {
  tokens <- tibble::tibble(
    participante = c(rep("C01", 5), rep("C02", 5)),
    palabra = c(rep("khanmigo", 3), rep("a", 2),
                rep("professora", 3), rep("a", 2))
  )
  tfidf <- calcular_tfidf(tokens)
  expect_s3_class(tfidf, "tbl_df")
  expect_true("tf_idf" %in% names(tfidf))
})
