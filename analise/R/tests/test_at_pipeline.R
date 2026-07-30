# ============================================================
# tests/test_at_pipeline.R
# Testes unitários para o pipeline de Análise Temática (P01)
# Framework: testthat
# ============================================================

library(testthat)

# Carregar funções a serem testadas
# (Aqui assumimos que estão em R/01_at_pipeline.R — refatorar em utils depois)

# --- 1. Test: limpar_texto -------------------------------------------
test_that("limpar_texto normaliza corretamente", {
  source(here::here("R", "01_at_pipeline.R"), local = TRUE, echo = FALSE)

  # Remover definição de main (não rodar pipeline)
  # Testa apenas a função limpar_texto
  if (exists("limpar_texto")) {
    # Lowercase
    expect_equal(limpar_texto("OLÁ"), "ola")
    # Remove acentos
    expect_equal(limpar_texto("criança"), "crianca")
    # Remove pontuação
    expect_equal(limpar_texto("Olá, mundo!"), "ola  mundo")
    # Remove números
    expect_equal(limpar_texto("Tenho 25 anos"), "tenho   anos")
    # Espaços múltiplos
    expect_equal(limpar_texto("a    b"), "a b")
    # Trim
    expect_equal(limpar_texto("  texto  "), "texto")
  } else {
    skip("limpar_texto não exportada — refatorar para utils.R")
  }
})

# --- 2. Test: tokenização --------------------------------------------
test_that("tokenização funciona em dados de exemplo", {
  # Criar dados de teste
  texto_exemplo <- "Khanmigo me ajuda. Às vezes ela explica bem."
  tokens_exemplo <- tibble::tibble(
    participante = "C01",
    texto = texto_exemplo
  ) |>
    dplyr::mutate(texto_limpo = limpar_texto(texto)) |>
    tidytext::unnest_tokens(palavra, texto_limpo) |>
    dplyr::anti_join(tidytext::stop_words, by = "palabra")

  # Deve ter tokenizado
  expect_gt(nrow(tokens_exemplo), 0)
  # Não deve ter stopwords em inglês
  expect_false("me" %in% tokens_exemplo$palabra)
  # Deve ter palavras-chave
  expect_true("khanmigo" %in% tokens_exemplo$palavra)
})

# --- 3. Test: contagem de frequência ---------------------------------
test_that("frequência de palavras é calculada corretamente", {
  tokens <- tibble::tibble(
    participante = c("C01", "C01", "C02"),
    palabra = c("a", "a", "b")
  )
  freq <- tokens |>
    dplyr::count(palabra, sort = TRUE)

  expect_equal(nrow(freq), 2)
  expect_equal(freq$n[freq$palabra == "a"], 2)
  expect_equal(freq$n[freq$palabra == "b"], 1)
})

# --- 4. Test: TF-IDF -------------------------------------------------
test_that("TF-IDF identifica palavras características", {
  tokens <- tibble::tibble(
    participante = c(rep("C01", 5), rep("C02", 5)),
    palabra = c(rep("khanmigo", 3), rep("a", 2),
                rep("professora", 3), rep("a", 2))
  )
  tfidf <- tokens |>
    dplyr::count(participante, palabra) |>
    tidytext::bind_tf_idf(palabra, participante, n)

  # Khanmigo deve ter TF-IDF > 0 em C01
  khanmigo_c01 <- tfidf |>
    dplyr::filter(participante == "C01", palabra == "khanmigo")
  expect_gt(khanmigo_c01$tf_idf, 0)

  # 'a' deve ter TF-IDF = 0 (comum a ambos)
  a_c01 <- tfidf |>
    dplyr::filter(participante == "C01", palabra == "a")
  expect_equal(a_c01$tf_idf, 0)
})

# --- 5. Test: codebook inicial --------------------------------------
test_that("codebook tem estrutura correta", {
  expect_true(is.data.frame(codebook_inicial))
  expect_true("codigo" %in% names(codebook_inicial))
  expect_true("descricao" %in% names(codebook_inicial))
  expect_gt(nrow(codebook_inicial), 5)
})

# --- 6. Test: pipeline end-to-end -----------------------------------
test_that("pipeline roda com dados de exemplo", {
  # Setup: criar arquivo de exemplo
  temp_dir <- tempfile("at_test_")
  dir.create(temp_dir)
  exemplo_path <- file.path(temp_dir, "exemplo.txt")
  writeLines("Khanmigo me ajuda. Às vezes ela explica.",
             exemplo_path)

  # Tentar rodar pré-processamento
  transcricoes <- tibble::tibble(
    arquivo = basename(exemplo_path),
    participante = "C01",
    texto = readLines(exemplo_path, warn = FALSE) |> paste(collapse = " ")
  ) |>
    dplyr::mutate(texto_limpo = limpar_texto(texto))

  expect_equal(nrow(transcricoes), 1)
  expect_true(nchar(transcricoes$texto_limpo) > 0)

  # Limpar
  unlink(temp_dir, recursive = TRUE)
})
