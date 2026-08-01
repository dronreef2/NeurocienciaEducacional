# ============================================================
# R/sem.R
# Modelagem de Equações Estruturais (P04) - versão modular
# ============================================================

# Funcoes internas (helper)
helper_criar_dados_exemplo_sem <- function(input_file) {
  dir.create(dirname(input_file), recursive = TRUE, showWarnings = FALSE)
  set.seed(42)
  n <- 200
  dados <- data.frame(
    participante = sprintf("P%03d", 1:n),
    idade = sample(c(7, 8, 9), n, replace = TRUE),
    sexo = sample(c("F", "M"), n, replace = TRUE),
    ses = rnorm(n, 0, 1),
    uso_ia = pmin(pmax(rnorm(n, 3, 1.5), 0), 7),
    letramento_digital = rnorm(n, 0, 1)
  )
  dados$engajamento <- 0.3 * scale(dados$uso_ia)[, 1] + rnorm(n, 0, 0.7)
  dados$stroop <- 0.2 * scale(dados$uso_ia)[, 1] + rnorm(n, 0, 0.5)
  dados$backward_digit <- 0.2 * scale(dados$uso_ia)[, 1] + rnorm(n, 0, 0.5)
  dados$dccs <- 0.2 * scale(dados$uso_ia)[, 1] + rnorm(n, 0, 0.5)
  write.csv(dados, input_file, row.names = FALSE)
}


helper_relatorio_sem <- function(params, fit_indices, output_dir) {
  ind <- params[params$label == "indirect", ]
  relatorio <- paste0(
    "===========================================\n",
    "  RELATORIO - SEM P04\n",
    "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
    "===========================================\n\n",
    "Indices de ajuste:\n",
    sprintf("  CFI: %.3f\n", fit_indices["cfi"]),
    sprintf("  TLI: %.3f\n", fit_indices["tli"]),
    sprintf("  RMSEA: %.3f\n", fit_indices["rmsea"]),
    sprintf("  SRMR: %.3f\n", fit_indices["srmr"]),
    "\nEfeito indireto:\n",
    sprintf("  %.3f [%.3f, %.3f]\n", ind$est, ind$ci.lower, ind$ci.upper)
  )
  writeLines(relatorio, file.path(output_dir, "relatorio.txt"))
}


#' SEM do P04 (IA Generativa x FE)
#'
#' Ajusta modelo de mediação com IA -> Engajamento -> FE.
#'
#' @param input_file Caminho do CSV
#' @param output_dir Diretorio de saida
#' @return Lista invisivel com modelos ajustados
#' @export
sem_p04 <- function(input_file, output_dir) {
  log_msg("Iniciando SEM P04")

  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  if (!file.exists(input_file)) {
    log_msg("Arquivo nao encontrado. Criando dados de exemplo...",
            level = "WARN")
    helper_criar_dados_exemplo_sem(input_file)
  }

  dados <- read.csv(input_file)

  # CFA
  fit_cfa <- criar_cfa(dados)
  log_msg("CFA ajustado")

  # SEM completo (mediacao)
  fit_sem <- ajustar_sem_completo(dados)
  log_msg("SEM completo ajustado")

  # Sumarios
  summary(fit_sem, fit.measures = TRUE, standardized = TRUE)
  params <- lavaan::parameterEstimates(fit_sem, standardized = TRUE)
  write.csv(params, file.path(output_dir, "parametros_sem.csv"))

  # Indices de ajuste
  fit_indices <- lavaan::fitMeasures(fit_sem,
    c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr", "aic", "bic"))
  write.csv(t(as.data.frame(fit_indices)),
            file.path(output_dir, "indices_ajuste.csv"))

  # Plot
  plot_sem_diagrama(fit_sem, output_dir)

  # Relatorio
  helper_relatorio_sem(params, fit_indices, output_dir)

  log_msg("SEM P04 concluido", level = "SUCCESS")
  invisible(list(cfa = fit_cfa, sem = fit_sem))
}


#' Criar modelo de mensuracao (CFA)
#'
#' @param dados Data frame com colunas stroop, backward_digit, dccs
#' @return Objeto lavaan
#' @export
criar_cfa <- function(dados) {
  modelo <- '
    FE =~ stroop + backward_digit + dccs
  '
  lavaan::cfa(modelo, data = dados, std.lv = TRUE)
}


#' Ajustar SEM completo (mediacao)
#'
#' @param dados Data frame
#' @return Objeto lavaan
#' @export
ajustar_sem_completo <- function(dados) {
  modelo <- '
    FE =~ stroop + backward_digit + dccs
    engajamento ~ a*uso_ia + idade + sexo + ses
    FE ~ b*engajamento + c*uso_ia + idade + sexo + ses
    indirect := a*b
    total := c + a*b
  '
  lavaan::sem(modelo, data = dados, std.lv = TRUE,
              se = "bootstrap", bootstrap = 5000)
}


#' Plotar diagrama do SEM
#'
#' @param fit_sem Objeto lavaan
#' @param output_dir Diretorio de saida
#' @return Invisivel
#' @export
plot_sem_diagrama <- function(fit_sem, output_dir) {
  if (!requireNamespace("semPlot", quietly = TRUE)) {
    log_msg("semPlot nao instalado, pulando plot", level = "WARN")
    return(invisible(NULL))
  }

  png(file.path(output_dir, "modelo_sem.png"),
      width = 1200, height = 900, res = 100)
  semPlot::semPaths(fit_sem,
                    what = "std",
                    layout = "tree",
                    edge.label.cex = 1.0,
                    sizeMan = 8,
                    sizeLat = 12)
  dev.off()
}
