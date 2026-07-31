# ============================================================
# R/lgcm.R
# Latent Growth Curve Models (P05) - versão modular
# ============================================================

#' LGCM do P05 (Coorte Longitudinal)
#'
#' Ajusta modelos de crescimento latente para trajetórias de FE.
#'
#' @param input_file Caminho do CSV em formato long
#' @param output_dir Diretório de saída
#' @param n_ondas Número de ondas (default 5)
#' @return Lista invisível com modelos
#' @export
lgcm_p05 <- function(input_file, output_dir, n_ondas = 5) {
  log_msg("Iniciando LGCM P05")

  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  if (!file.exists(input_file)) {
    log_msg("Arquivo não encontrado. Criando dados de exemplo...",
            level = "WARN")
    _criar_dados_exemplo_lgcm(input_file, n_ondas)
  }

  dados <- read.csv(input_file)
  dados_wide <- _preparar_dados_lgcm(dados, n_ondas)

  # Modelos
  fit_linear <- ajustar_lgcm_linear(dados_wide, n_ondas)
  fit_cond <- ajustar_lgcm_condicional(dados_wide, n_ondas)
  fit_quad <- ajustar_lgcm_quadratico(dados_wide, n_ondas)

  # Comparação
  comparacao <- _comparar_modelos_lgcm(fit_linear, fit_cond, fit_quad)
  write.csv(comparacao, file.path(output_dir, "comparacao_modelos.csv"))

  # Plot trajetórias
  plot_trajetorias(dados, output_dir)

  # Relatório
  _relatorio_lgcm(comparacao, output_dir)

  log_msg("LGCM P05 concluído", level = "SUCCESS")
  invisible(list(linear = fit_linear, condicional = fit_cond, quadratico = fit_quad))
}


#' Ajustar LGCM Linear
#'
#' @param dados_wide Wide format data
#' @param n_ondas Número de ondas
#' @return Objeto lavaan
#' @export
ajustar_lgcm_linear <- function(dados_wide, n_ondas = 5) {
  fe_vars <- paste0("fe_onda", 1:n_ondas)
  loading_times <- paste(sprintf("%d*%s", 0:(n_ondas - 1), fe_vars), collapse = " + ")

  formula <- sprintf("intercept =~ %s; slope =~ %s", paste(rep(1, n_ondas), fe_vars, sep = "*", collapse = " + "), loading_times)

  # Construir modelo
  intercept_part <- paste0("1*", fe_vars, collapse = " + ")
  slope_part <- paste0(seq(0, n_ondas - 1), "*", fe_vars, collapse = " + ")

  modelo <- paste0("
    intercept =~ ", intercept_part, "
    slope =~ ", slope_part, "
    intercept ~ 1
    slope ~ 1
    intercept ~~ intercept
    slope ~~ slope
    intercept ~~ slope
  ")

  lavaan::growth(modelo, data = dados_wide, missing = "ml")
}


#' Ajustar LGCM Condicional
#'
#' @param dados_wide Wide format data com covariáveis
#' @param n_ondas Número de ondas
#' @return Objeto lavaan
#' @export
ajustar_lgcm_condicional <- function(dados_wide, n_ondas = 5) {
  fe_vars <- paste0("fe_onda", 1:n_ondas)
  intercept_part <- paste0("1*", fe_vars, collapse = " + ")
  slope_part <- paste0(seq(0, n_ondas - 1), "*", fe_vars, collapse = " + ")

  modelo <- paste0("
    intercept =~ ", intercept_part, "
    slope =~ ", slope_part, "
    intercept ~ sexo_num + ses + escola_num
    slope ~ sexo_num + ses + escola_num
    intercept ~~ intercept
    slope ~~ slope
    intercept ~~ slope
  ")

  lavaan::growth(modelo, data = dados_wide, missing = "ml",
                 meanstructure = TRUE)
}


#' Ajustar LGCM Quadrático
#'
#' @param dados_wide Wide format data
#' @param n_ondas Número de ondas
#' @return Objeto lavaan
#' @export
ajustar_lgcm_quadratico <- function(dados_wide, n_ondas = 5) {
  fe_vars <- paste0("fe_onda", 1:n_ondas)
  intercept_part <- paste0("1*", fe_vars, collapse = " + ")
  slope_part <- paste0(seq(0, n_ondas - 1), "*", fe_vars, collapse = " + ")
  quad_part <- paste0(seq(0, n_ondas - 1)^2, "*", fe_vars, collapse = " + ")

  modelo <- paste0("
    intercept =~ ", intercept_part, "
    slope =~ ", slope_part, "
    quadratic =~ ", quad_part, "
    intercept ~ 1
    slope ~ 1
    quadratic ~ 1
  ")

  lavaan::growth(modelo, data = dados_wide, missing = "ml")
}


#' Plotar trajetórias
#'
#' @param dados Data frame long
#' @param output_dir Diretório de saída
#' @return Invisível
#' @export
plot_trajetorias <- function(dados, output_dir) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    return(invisible(NULL))
  }

  p <- ggplot2::ggplot(dados, ggplot2::aes(x = idade, y = fe_score,
                                          group = id, color = sexo)) +
    ggplot2::geom_line(alpha = 0.3) +
    ggplot2::geom_smooth(ggplot2::aes(group = sexo), method = "lm",
                         se = TRUE, linewidth = 1.5) +
    ggplot2::labs(title = "Trajetórias de desenvolvimento de FE",
                  x = "Idade (anos)", y = "Escore FE (z)",
                  color = "Sexo") +
    ggplot2::scale_color_manual(values = c("F" = "#d62728", "M" = "#1f77b4")) +
    ggplot2::theme_minimal()

  ggplot2::ggsave(file.path(output_dir, "trajetorias.png"),
                  p, width = 10, height = 6, dpi = 100)
  invisible(NULL)
}


#' @keywords internal
_criar_dados_exemplo_lgcm <- function(input_file, n_ondas) {
  dir.create(dirname(input_file), recursive = TRUE, showWarnings = FALSE)
  set.seed(42)
  n <- 150

  dados <- expand.grid(
    id = 1:n,
    onda = 1:n_ondas,
    idade = seq(7, length.out = n_ondas, by = 1)[1:n_ondas]
  )[1:(n * n_ondas), ] |>
    dplyr::arrange(id, onda) |>
    dplyr::mutate(
      sexo = rep(sample(c("F", "M"), n, replace = TRUE), each = n_ondas),
      ses = rep(rnorm(n, 0, 1), each = n_ondas),
      escola = rep(sample(c("publica", "privada"), n,
                          replace = TRUE, prob = c(0.7, 0.3)),
                   each = n_ondas),
      tempo = onda - 1
    )

  dados$fe_score <- NA
  for (i in 1:n) {
    intercept_i <- rnorm(1, 0, 0.5)
    slope_i <- rnorm(1, 0.5, 0.2) + 0.1 * dados$ses[dados$id == i][1]
    for (t in 1:n_ondas) {
      idx <- (i - 1) * n_ondas + t
      dados$fe_score[idx] <- intercept_i + slope_i * (t - 1) + rnorm(1, 0, 0.3)
    }
  }

  write.csv(dados, input_file, row.names = FALSE)
}


#' @keywords internal
_preparar_dados_lgcm <- function(dados, n_ondas) {
  dados_wide <- dados |>
    dplyr::select(id, onda, fe_score) |>
    tidyr::pivot_wider(names_from = onda, values_from = fe_score,
                       names_prefix = "fe_onda") |>
    dplyr::left_join(
      dados |>
        dplyr::filter(onda == 1) |>
        dplyr::select(id, sexo, ses, escola),
      by = "id"
    ) |>
    dplyr::mutate(
      sexo_num = ifelse(sexo == "M", 1, 0),
      escola_num = ifelse(escola == "privada", 1, 0),
      ses = scale(ses)[, 1]
    )

  dados_wide
}


#' @keywords internal
_comparar_modelos_lgcm <- function(fit_linear, fit_cond, fit_quad) {
  data.frame(
    Modelo = c("Linear", "Condicional", "Quadrático"),
    chisq = c(lavaan::fitMeasures(fit_linear, "chisq"),
              lavaan::fitMeasures(fit_cond, "chisq"),
              lavaan::fitMeasures(fit_quad, "chisq")),
    df = c(lavaan::fitMeasures(fit_linear, "df"),
           lavaan::fitMeasures(fit_cond, "df"),
           lavaan::fitMeasures(fit_quad, "df")),
    CFI = c(lavaan::fitMeasures(fit_linear, "cfi"),
            lavaan::fitMeasures(fit_cond, "cfi"),
            lavaan::fitMeasures(fit_quad, "cfi")),
    RMSEA = c(lavaan::fitMeasures(fit_linear, "rmsea"),
              lavaan::fitMeasures(fit_cond, "rmsea"),
              lavaan::fitMeasures(fit_quad, "rmsea"))
  )
}


#' @keywords internal
_relatorio_lgcm <- function(comparacao, output_dir) {
  relatorio <- paste0(
    "===========================================\n",
    "  RELATÓRIO - LGCM P05\n",
    "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
    "===========================================\n\n",
    "Comparação de modelos:\n",
    paste(capture.output(print(comparacao)), collapse = "\n")
  )
  writeLines(relatorio, file.path(output_dir, "relatorio.txt"))
}
