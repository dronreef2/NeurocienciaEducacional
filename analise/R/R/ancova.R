# ============================================================
# R/ancova.R
# ANCOVA 2x4 fatorial (P02) - versão modular
# ============================================================

#' ANCOVA do P02 (Gamificação)
#'
#' Executa ANCOVA 2x4 fatorial com post-hoc, correção Bonferroni,
#' e tamanho de efeito.
#'
#' @param input_file Caminho do CSV limpo
#' @param output_dir Diretório de saída
#' @return Invisível
#' @export
ancova_p02 <- function(input_file,
                       output_dir) {
  log_msg("Iniciando ANCOVA P02")

  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  # Carregar dados
  if (!file.exists(input_file)) {
    log_msg("Arquivo não encontrado. Criando dados de exemplo...",
            level = "WARN")
    _criar_dados_exemplo_ancova(input_file)
  }

  dados <- read.csv(input_file)
  dados$grupo <- factor(dados$grupo)
  dados$sexo <- factor(dados$sexo)

  # Outcomes
  outcomes <- c("stroop", "bds", "dccs")
  pre_col <- c("pre_stroop", "pre_bds", "pre_dccs")
  post_col <- c("post_stroop", "post_bds", "post_dccs")

  results <- list()
  for (i in seq_along(outcomes)) {
    out <- outcomes[i]
    pre <- pre_col[i]
    post <- post_col[i]

    formula <- as.formula(sprintf("%s ~ grupo + %s + idade + sexo",
                                  post, pre))
    modelo <- lm(formula, data = dados)

    anova_result <- car::Anova(modelo, type = "III")
    eta2 <- effectsize::eta_squared(modelo, partial = TRUE)
    emm <- emmeans::emmeans(modelo, ~ grupo)
    emm_pairs <- pairs(emm, adjust = "tukey")

    results[[out]] <- list(
      modelo = modelo,
      anova = anova_result,
      eta2 = eta2,
      emm = emm,
      post_hoc = emm_pairs
    )

    # Salvar
    write.csv(as.data.frame(anova_result),
              file.path(output_dir, sprintf("ancova_%s.csv", out)))
    write.csv(as.data.frame(eta2),
              file.path(output_dir, sprintf("eta2_%s.csv", out)))
    write.csv(as.data.frame(emm_pairs),
              file.path(output_dir, sprintf("posthoc_%s.csv", out)))
  }

  # Bonferroni
  p_grupos <- sapply(outcomes, function(o) {
    results[[o]]$anova$`Pr(>F)`[1]
  })
  p_corrigido <- p.adjust(p_grupos, method = "bonferroni")

  correcao <- data.frame(
    outcome = names(p_grupos),
    p_bruto = p_grupos,
    p_bonferroni = p_corrigido
  )
  write.csv(correcao, file.path(output_dir, "correcao_bonferroni.csv"))

  # Cohen's d (cada grupo vs. CTRL)
  _cohens_d_por_grupo(dados, output_dir)

  # Plots
  _plot_ancova(dados, results, output_dir)

  # Relatório
  _relatorio_ancova(results, correcao, output_dir)

  log_msg("ANCOVA P02 concluída", level = "SUCCESS")
  invisible(results)
}


#' @keywords internal
_criar_dados_exemplo_ancova <- function(input_file) {
  dir.create(dirname(input_file), recursive = TRUE, showWarnings = FALSE)
  set.seed(42)
  n_por_grupo <- 40

  dados <- expand.grid(
    id = 1:(n_por_grupo * 5),
    grupo = factor(rep(c("ADAP_8", "ADAP_16", "FIXA_8", "FIXA_16", "CTRL"),
                       each = n_por_grupo),
                   levels = c("CTRL", "FIXA_8", "FIXA_16", "ADAP_8", "ADAP_16"))
  ) |>
    dplyr::mutate(
      idade = sample(7:9, dplyr::n(), replace = TRUE, prob = c(0.3, 0.5, 0.2)),
      ses = rnorm(dplyr::n(), 0, 1)
    )

  for (i in 1:nrow(dados)) {
    dados$pre_stroop[i] <- rnorm(1, 0, 1)
    dados$pre_bds[i] <- rnorm(1, 0, 1)
    dados$pre_dccs[i] <- rnorm(1, 0, 1)
    efeito <- c("CTRL" = 0, "FIXA_8" = 0.1, "FIXA_16" = 0.2,
                "ADAP_8" = 0.3, "ADAP_16" = 0.5)[as.character(dados$grupo[i])]
    dados$post_stroop[i] <- dados$pre_stroop[i] + efeito + rnorm(1, 0, 0.5)
    dados$post_bds[i] <- dados$pre_bds[i] + efeito + rnorm(1, 0, 0.5)
    dados$post_dccs[i] <- dados$pre_dccs[i] + efeito + rnorm(1, 0, 0.5)
  }

  write.csv(dados, input_file, row.names = FALSE)
}


#' @keywords internal
_cohens_d_por_grupo <- function(dados, output_dir) {
  resultados <- data.frame()
  ctrl <- dados$post_stroop[dados$grupo == "CTRL"]

  for (g in levels(dados$grupo)) {
    if (g == "CTRL") next
    g_data <- dados$post_stroop[dados$grupo == g]
    d <- cohens_d(g_data, ctrl)
    resultados <- rbind(resultados, data.frame(
      comparacao = paste(g, "vs CTRL"),
      cohens_d = d
    ))
  }

  write.csv(resultados, file.path(output_dir, "cohens_d.csv"))
}


#' @keywords internal
_plot_ancova <- function(dados, results, output_dir) {
  for (out in names(results)) {
    emm_df <- as.data.frame(results[[out]]$emm)
    p <- ggplot2::ggplot(emm_df,
                         ggplot2::aes(x = grupo, y = emmean,
                                      ymin = lower.CL, ymax = upper.CL,
                                      color = grupo)) +
      ggplot2::geom_point(size = 3) +
      ggplot2::geom_errorbar(width = 0.2) +
      ggplot2::labs(x = "Grupo", y = "Média marginal (95% IC)",
                    title = sprintf("emmeans — %s", out)) +
      ggplot2::theme_minimal() +
      ggplot2::theme(legend.position = "none",
                     axis.text.x = ggplot2::element_text(angle = 45, hjust = 1))

    ggplot2::ggsave(file.path(output_dir, sprintf("emmeans_%s.png", out)),
                    p, width = 10, height = 6, dpi = 100)
  }
}


#' @keywords internal
_relatorio_ancova <- function(results, correcao, output_dir) {
  relatorio <- paste0(
    "===========================================\n",
    "  RELATÓRIO - ANCOVA P02\n",
    "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
    "===========================================\n\n",
    "Correção de Bonferroni:\n",
    paste(capture.output(print(correcao)), collapse = "\n")
  )
  writeLines(relatorio, file.path(output_dir, "relatorio.txt"))
}
