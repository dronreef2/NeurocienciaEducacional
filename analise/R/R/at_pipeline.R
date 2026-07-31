# ============================================================
# R/at_pipeline.R
# Pipeline de Análise Temática (P01) - versão modular
# ============================================================

#' Análise Temática Reflexiva (Braun & Clarke 2022)
#'
#' Pipeline completo para análise qualitativa de transcrições.
#'
#' @param input_dir Diretório com arquivos .txt (um por participante)
#' @param output_dir Diretório de saída
#' @param gerar_wordcloud Lógico: gerar wordcloud?
#' @return Invisível
#' @export
#' @examples
#' \dontrun{
#' at_pipeline(
#'   input_dir = "dados/raw/P01",
#'   output_dir = "resultados/P01"
#' )
#' }
at_pipeline <- function(input_dir,
                        output_dir,
                        gerar_wordcloud = TRUE) {
  log_msg(sprintf("Iniciando Análise Temática (P01)"))

  # Criar diretórios
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  # 1. Carregar transcrições
  arquivos <- list.files(input_dir, pattern = "\\.txt$", full.names = TRUE)

  if (length(arquivos) == 0) {
    log_msg("Nenhum arquivo encontrado. Criando dados de exemplo...",
            level = "WARN")
    _criar_dados_exemplo_at(input_dir)
    arquivos <- list.files(input_dir, pattern = "\\.txt$", full.names = TRUE)
  }

  transcricoes <- tibble::tibble(
    arquivo = basename(arquivos),
    participante = tools::file_path_sans_ext(basename(arquivos)),
    texto = sapply(arquivos, function(f) {
      paste(readLines(f, warn = FALSE), collapse = " ")
    })
  ) |>
    dplyr::mutate(texto_limpo = limpar_texto(texto))

  log_msg(sprintf("Carregadas %d transcrições", nrow(transcricoes)))

  # 2. Tokenização
  tokens <- tokenizar(transcricoes)
  log_msg(sprintf("Tokens gerados: %d", nrow(tokens)))

  # 3. Frequência
  freq <- calcular_frequencia(tokens)
  readr::write_csv(freq, file.path(output_dir, "01_frequencia_palavras.csv"))

  # 4. Bigramas
  bigramas <- tokens |>
    tidytext::unnest_tokens(bigrama, paste(participante, palavra),
                            token = "ngrams", n = 2) |>
    tidyr::separate(bigrama, c("p1", "p2"), sep = " ", remove = FALSE) |>
    dplyr::filter(!p1 %in% obter_stop_words_pt()$palabra,
                  !p2 %in% obter_stop_words_pt()$palabra) |>
    dplyr::count(p1, p2, sort = TRUE)
  readr::write_csv(bigramas, file.path(output_dir, "02_bigramas.csv"))

  # 5. TF-IDF
  tfidf <- calcular_tfidf(tokens)
  readr::write_csv(tfidf, file.path(output_dir, "03_tfidf_por_participante.csv"))

  # 6. Codebook
  codebook <- gerar_codebook(transcricoes)
  readr::write_csv(codebook, file.path(output_dir, "04_codebook_inicial.csv"))

  # 7. Wordcloud
  if (gerar_wordcloud) {
    _plot_wordcloud(freq, output_dir)
  }

  # 8. Relatório
  _relatorio_at(transcricoes, freq, output_dir)

  log_msg("Análise Temática concluída", level = "SUCCESS")
  invisible(NULL)
}


#' @keywords internal
_criar_dados_exemplo_at <- function(input_dir) {
  dir.create(input_dir, recursive = TRUE, showWarnings = FALSE)
  exemplos <- c(
    "Khanmigo me ajuda a fazer a lição. Às vezes ela explica bem, às vezes erra.",
    "Ela é inteligente mas demora pra responder. Eu prefiro a professora.",
    "Quando ela erra eu falo pra professora. A Khanmigo é minha amiga.",
    "Não gosto quando ela demora. Mas ela me ajuda a aprender.",
    "A Khanmigo sabe tudo sobre animais. Eu confio nela."
  )
  for (i in seq_along(exemplos)) {
    writeLines(exemplos[i],
               file.path(input_dir, sprintf("exemplo_C%02d.txt", i)))
  }
}


#' @keywords internal
_plot_wordcloud <- function(freq, output_dir) {
  if (!requireNamespace("wordcloud", quietly = TRUE)) {
    log_msg("Pacote 'wordcloud' não instalado. Pulando.", level = "WARN")
    return(invisible(NULL))
  }

  png(file.path(output_dir, "05_wordcloud.png"),
      width = 1200, height = 800, res = 100)
  wordcloud::wordcloud(
    words = freq$palavra,
    freq = freq$n,
    min.freq = 1,
    max.words = 100,
    random.order = FALSE,
    rot.per = 0.35,
    colors = RColorBrewer::brewer.pal(8, "Dark2")
  )
  dev.off()
}


#' @keywords internal
_relatorio_at <- function(transcricoes, freq, output_dir) {
  relatorio <- paste0(
    "===========================================\n",
    "  RELATÓRIO - Análise Temática (P01)\n",
    "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
    "===========================================\n\n",
    "Participantes: ", nrow(transcricoes), "\n",
    "Palavras totais: ", sum(freq$n), "\n",
    "Vocabulário único: ", nrow(freq), "\n",
    "Média de palavras/participante: ",
    round(sum(freq$n) / nrow(transcricoes), 0), "\n\n",
    "Top 10 palavras:\n"
  )

  for (i in seq_len(min(10, nrow(freq)))) {
    relatorio <- paste0(relatorio,
      sprintf("  %d. %s (%d ocorrências)\n",
              i, freq$palabra[i], freq$n[i]))
  }

  relatorio <- paste0(relatorio, "\nArquivos gerados em: ", output_dir, "\n")
  writeLines(relatorio, file.path(output_dir, "relatorio.txt"))
}
