# ============================================================
# R/utils.R
# Funções utilitárias compartilhadas por todos os pipelines
# ============================================================

#' Limpar texto para análise
#'
#' Remove acentos, pontuação, números, e normaliza espaços.
#'
#' @param texto Vetor de caracteres ou string única
#' @return Vetor de caracteres com texto limpo
#' @export
#' @examples
#' limpar_texto("Criança, 25 anos!")  # "crianca    anos "
limpar_texto <- function(texto) {
  if (!is.character(texto)) {
    stop("`texto` deve ser um vetor de caracteres")
  }

  texto |>
    stringr::str_to_lower() |>
    stringr::str_replace_all("[áàãâä]", "a") |>
    stringr::str_replace_all("[éèêë]", "e") |>
    stringr::str_replace_all("[íìîï]", "i") |>
    stringr::str_replace_all("[óòõôö]", "o") |>
    stringr::str_replace_all("[úùûü]", "u") |>
    stringr::str_replace_all("[ç]", "c") |>
    stringr::str_replace_all("[[:punct:]]", " ") |>
    stringr::str_replace_all("[[:digit:]]", " ") |>
    stringr::str_replace_all("\\s+", " ") |>
    stringr::str_trim()
}


#' Tokenizar texto
#'
#' @param tibble_doc Tibble com coluna `texto_limpo`
#' @param stop_words_pt Vetor de stop words em português
#' @return Tibble com colunas: participante, palavra
#' @export
tokenizar <- function(tibble_doc, stop_words_pt = NULL) {
  if (is.null(stop_words_pt)) {
    stop_words_pt <- obter_stop_words_pt()
  }

  tokens <- tibble_doc |>
    tidytext::unnest_tokens(palavra, texto_limpo) |>
    dplyr::anti_join(tidytext::stop_words, by = "palabra") |>
    dplyr::anti_join(stop_words_pt, by = "palavra")

  tokens
}


#' Obter lista de stop words em português
#'
#' @return Tibble com coluna `palabra`
#' @export
obter_stop_words_pt <- function() {
  tibble::tibble(
    palabra = c(
      "e", "ou", "mas", "que", "se", "porque", "como", "quando", "onde",
      "eu", "tu", "ele", "ela", "nos", "vos", "eles", "elas",
      "meu", "minha", "teu", "tua", "seu", "sua", "nosso", "nossa",
      "este", "esta", "isto", "aquilo", "esse", "essa", "isso",
      "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
      "em", "no", "na", "nos", "nas", "por", "pelo", "pela",
      "com", "sem", "para", "pra", "ate", "sob", "sobre",
      "e", "ou", "mas", "tambem", "mais", "menos", "muito", "pouco",
      "ja", "ainda", "sempre", "nunca", "talvez", "assim", "entao",
      "ai", "aqui", "ali", "la", "ca", "tipo", "coisa",
      "gente", "pessoa", "menino", "menina", "crianca"
    )
  )
}


#' Calcular frequência de palavras
#'
#' @param tokens Tibble com coluna `palavra`
#' @return Tibble com colunas: palabra, n, freq_relativa
#' @export
calcular_frequencia <- function(tokens) {
  tokens |>
    dplyr::count(palabra, sort = TRUE) |>
    dplyr::mutate(freq_relativa = n / sum(n) * 100)
}


#' Calcular TF-IDF
#'
#' @param tokens Tibble com colunas: participante, palabra
#' @return Tibble com TF-IDF calculado
#' @export
calcular_tfidf <- function(tokens) {
  tokens |>
    dplyr::count(participante, palabra) |>
    tidytext::bind_tf_idf(palavra, participante, n) |>
    dplyr::arrange(participante, dplyr::desc(tf_idf))
}


#' Calcular Cohen's d entre dois grupos
#'
#' @param x Numeric vector (grupo 1)
#' @param y Numeric vector (grupo 2)
#' @return Valor numérico de Cohen's d
#' @export
cohens_d <- function(x, y) {
  nx <- length(x)
  ny <- length(y)
  pooled_sd <- sqrt(((nx - 1) * var(x, na.rm = TRUE) +
                       (ny - 1) * var(y, na.rm = TRUE)) /
                      (nx + ny - 2))
  if (pooled_sd == 0) {
    return(0)
  }
  (mean(x, na.rm = TRUE) - mean(y, na.rm = TRUE)) / pooled_sd
}


#' Gerar codebook inicial baseado em termos-chave
#'
#' @param transcricoes Tibble com coluna `texto_limpo`
#' @param termos_por_codigo Lista nomeada com termos por código
#' @return Tibble com codebook
#' @export
gerar_codebook <- function(transcricoes, termos_por_codigo = NULL) {
  if (is.null(termos_por_codigo)) {
    termos_por_codigo <- list(
      "metacognicao_explicita" = c("pensei", "achei", "sei", "lembro"),
      "confianca_alta" = c("confio", "sempre", "acredito"),
      "confianca_baixa" = c("erro", "errada", "nao sei", "confundi"),
      "deteccao_erro" = c("erro", "errada", "errou"),
      "comparacao_humano" = c("pessoa", "gente", "humano"),
      "comparacao_professor" = c("professora", "professor", "mestre"),
      "atribuicao_inteligencia" = c("inteligente", "sabe tudo", "esperta"),
      "atribuicao_amizade" = c("amiga", "amigo", "companhia"),
      "uso_estrategico" = c("quando", "para", "ajuda", "uso"),
      "uso_emocional" = c("triste", "feliz", "sente"),
      "resistencia" = c("nao gosto", "chato", "ruim"),
      "curiosidade" = c("quero", "mais", "aprende")
    )
  }

  codebook <- tibble::tibble(
    codigo = names(termos_por_codigo),
    descricao = sapply(names(termos_por_codigo), function(x) {
      switch(x,
        "metacognicao_explicita" = "Criança verbaliza explicitamente seu pensamento",
        "confianca_alta" = "Criança expressa alta confiança no tutor",
        "confianca_baixa" = "Criança expressa baixa confiança",
        "deteccao_erro" = "Criança identifica erros do tutor",
        "comparacao_humano" = "Compara tutor com humano",
        "comparacao_professor" = "Compara tutor com professora",
        "atribuicao_inteligencia" = "Atribui inteligência ao tutor",
        "atribuicao_amizade" = "Atribui qualidades de amizade",
        "uso_estrategico" = "Uso instrumental/estratégico",
        "uso_emocional" = "Uso para suporte emocional",
        "resistencia" = "Resiste ou se opõe ao uso",
        "curiosidade" = "Demonstra curiosidade e exploração"
      )
    }),
    termos = sapply(termos_por_codigo, function(x) paste(x, collapse = ", ")),
    frequencia_sugerida = NA_integer_
  )

  # Calcular frequência sugerida
  for (i in seq_len(nrow(codebook))) {
    termos <- unlist(strsplit(codebook$termos[i], ", "))
    n_mention <- sum(sapply(transcricoes$texto_limpo, function(texto) {
      any(sapply(termos, function(t) {
        stringr::str_detect(texto, stringr::regex(t, ignore_case = TRUE))
      }))
    }))
    codebook$frequencia_sugerida[i] <- n_mention
  }

  codebook
}


#' Log estruturado
#'
#' @param msg Mensagem
#' @param level Nível: "INFO", "WARN", "ERROR", "SUCCESS"
#' @return Invisível
#' @export
log_msg <- function(msg, level = "INFO") {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  cat(sprintf("[%s] %s: %s\n", timestamp, level, msg))
  invisible(NULL)
}


#' Verificar setup do projeto
#'
#' @return Invisível
#' @export
verificar_setup <- function() {
  log_msg("Verificando setup do projeto...")

  # Pacotes essenciais
  pacotes <- c("tidyverse", "tidytext", "lavaan", "emmeans", "here")
  for (pkg in pacotes) {
    if (requireNamespace(pkg, quietly = TRUE)) {
      log_msg(sprintf("  ✅ %s: disponível", pkg))
    } else {
      log_msg(sprintf("  ❌ %s: NÃO instalado", pkg), level = "WARN")
    }
  }

  invisible(NULL)
}
