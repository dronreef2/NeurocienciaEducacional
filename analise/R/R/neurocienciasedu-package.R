# ============================================================
# R/neurocienciasedu-package.R
# Documentação do package (gerada por roxygen2)
# ============================================================

#' neurocienciasedu: Pipeline de Análise para o Programa de Pesquisa em Neurociência Educacional
#'
#' Pipeline R para análise de dados do programa de pesquisa de 5 projetos
#' (2026-2030) em neurociência educacional, conduzido em parceria com a
#' UFRN/CERES. Inclui:
#' - Análise Temática (P01)
#' - ANCOVA 2x4 fatorial (P02)
#' - SEM com mediação (P04)
#' - LGCM/LGMM longitudinal (P05)
#'
#' @section Funções principais:
#' - [at_pipeline()] para Análise Temática
#' - [ancova_p02()] para ANCOVA
#' - [sem_p04()] para SEM
#' - [lgcm_p05()] para LGCM
#'
#' @section Funções utilitárias:
#' - [limpar_texto()] normalização de texto
#' - [tokenizar()] tokenização
#' - [calcular_frequencia()] frequência de palavras
#' - [calcular_tfidf()] TF-IDF
#' - [gerar_codebook()] codebook inicial
#' - [cohens_d()] tamanho de efeito
#' - [log_msg()] log estruturado
#'
#' @docType package
#' @name neurocienciasedu-package
#' @aliases neurocienciasedu
#' @keywords internal
"_PACKAGE"

# Suppress R CMD check NOTEs
utils::globalVariables(c(
  "palabra", "participante", "n", "freq_relativa",
  "tf", "idf", "tf_idf", "p1", "p2", "grupo", "sexo",
  "idade", "ses", "stroop", "backward_digit", "dccs",
  "pre_stroop", "pre_bds", "pre_dccs",
  "post_stroop", "post_bds", "post_dccs",
  "onda", "fe_score", "id", "tempo"
))
