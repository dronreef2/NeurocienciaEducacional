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
#' - [at.pipeline_internal()] para Análise Temática
#' - [ancova.\1_internal\22()] para ANCOVA
#' - [sem.\1_internal\24()] para SEM
#' - [lgcm.\1_internal\25()] para LGCM
#'
#' @section Funções utilitárias:
#' - [limpar.texto_internal()] normalização de texto
#' - [tokenizar()] tokenização
#' - [calcular.frequencia_internal()] frequência de palavras
#' - [calcular.tfidf_internal()] TF-IDF
#' - [gerar.codebook_internal()] codebook inicial
#' - [cohens.d_internal()] tamanho de efeito
#' - [log.msg_internal()] log estruturado
#'
#' @docType package
#' @name neurocienciasedu-package
#' @aliases neurocienciasedu
#' @keywords internal
".\1_internal\2

# Suppress R CMD check NOTEs
utils::globalVariables(c(
  "palabra", "participante", "n", "freq.\1_internal\2,
  "tf", "idf", "tf.\1_internal\2, "p1", "p2", "grupo", "sexo",
  "idade", "ses", "stroop", "backward.\1_internal\2, "dccs",
  "pre.\1_internal\2, "pre.\1_internal\2, "pre.\1_internal\2,
  "post.\1_internal\2, "post.\1_internal\2, "post.\1_internal\2,
  "onda", "fe.\1_internal\2, "id", "tempo"
))
