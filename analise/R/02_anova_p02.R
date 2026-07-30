# ============================================================
# 02_anova_p02.R
# ANCOVA + Post-hoc + Tamanho de Efeito — Projeto P02
#
# Design: ECR 2×2 fatorial + grupo controle
# - Fator 1: Tipo (ADAPTATIVA vs FIXA)
# - Fator 2: Duração (8 vs 16 semanas)
# - + Grupo controle (sem gamificação)
# - Total: 5 grupos
# - Covariável: pré-teste (T0)
# - Outcome: pós-teste (T1) em cada medida de FE
#
# Análise primária: ANCOVA 2×4 (5 grupos, alpha .05, Bonferroni)
# Análise secundária: Post-hoc (Tukey HSD) + Tamanho de efeito
# Análise terciária: ANCOVA separada por sexo (exploratória)
#
# Pré-requisitos: dados em formato long com colunas:
#   id, grupo, duracao, sexo, idade, ses, escola,
#   pre_stroop, post_stroop, pre_bds, post_bds, pre_dccs, post_dccs
#
# Uso: Rscript R/02_anova_p02.R
# ============================================================

# Setup
source(here::here("R", "00_setup.R"))

# --- 0. Packages específicos -----------------------------
pacotes_ancova <- c(
  "afex",      # ANCOVA fácil
  "emmeans",   # Estimated marginal means (post-hoc)
  "effectsize", # Cohen's d, eta²
  "car",       # Anova type III
  "multcomp",  # Multiple comparisons
  "broom",     # Tidier model outputs
  "flextable"  # Tabelas bonitas para publicação
)

for (pkg in pacotes_ancova) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
  library(pkg, character.only = TRUE)
}

# --- 1. Carregar dados -----------------------------------
PROJETO <- "P02"
INPUT_FILE <- here("dados", "processed", PROJETO, "p02_clean.csv")
OUTPUT_DIR <- here("resultados", PROJETO)

if (!dir.exists(OUTPUT_DIR)) dir.create(OUTPUT_DIR, recursive = TRUE)

log_msg(sprintf("Iniciando ANCOVA para o projeto %s", PROJETO))

if (!file.exists(INPUT_FILE)) {
  log_msg(sprintf("⚠️  Arquivo %s não encontrado. Criando dados de exemplo.", INPUT_FILE), level = "WARN")

  # Simular dados do P02 (5 grupos, com efeito esperado)
  set.seed(42)
  n_por_grupo <- 40
  n_total <- n_por_grupo * 5

  dados_exemplo <- expand.grid(
    id = 1:n_total,
    grupo = factor(
      rep(c("ADAP_8", "ADAP_16", "FIXA_8", "FIXA_16", "CTRL"),
          each = n_por_grupo),
      levels = c("CTRL", "FIXA_8", "FIXA_16", "ADAP_8", "ADAP_16")
    ),
    sexo = sample(c("F", "M"), n_total, replace = TRUE),
    escola = sample(c("A", "B", "C"), n_total, replace = TRUE)
  ) |>
    dplyr::mutate(
      idade = sample(7:9, n_total, replace = TRUE, prob = c(0.3, 0.5, 0.2)),
      ses = rnorm(n_total, 0, 1)
    )

  # Gerar pré e pós com efeito de grupo esperado
  for (i in 1:n_total) {
    # Pré-teste (sem efeito de grupo)
    dados_exemplo$pre_stroop[i] <- rnorm(1, 0, 1)
    dados_exemplo$pre_bds[i] <- rnorm(1, 0, 1)
    dados_exemplo$pre_dccs[i] <- rnorm(1, 0, 1)

    # Efeito esperado (Cohen's d):
    # ADAP_16: d = 0.50
    # ADAP_8:  d = 0.30
    # FIXA_16: d = 0.20
    # FIXA_8:  d = 0.10
    # CTRL:    d = 0.00
    efeitos <- c(
      "CTRL" = 0.00, "FIXA_8" = 0.10, "FIXA_16" = 0.20,
      "ADAP_8" = 0.30, "ADAP_16" = 0.50
    )
    efeito <- efeitos[as.character(dados_exemplo$grupo[i])]

    # Pós-teste = pré-teste + efeito de grupo + ruído
    dados_exemplo$post_stroop[i] <- dados_exemplo$pre_stroop[i] + efeito + rnorm(1, 0, 0.5)
    dados_exemplo$post_bds[i] <- dados_exemplo$pre_bds[i] + efeito + rnorm(1, 0, 0.5)
    dados_exemplo$post_dccs[i] <- dados_exemplo$pre_dccs[i] + efeito + rnorm(1, 0, 0.5)

    # Covariáveis adicionais
    dados_exemplo$engajamento[i] <- rnorm(1, as.numeric(as.character(dados_exemplo$grupo[i])) * 0.3, 1)
  }

  # Criar FE composto (média z-scored dos 3 pós)
  dados_exemplo <- dados_exemplo |>
    dplyr::mutate(
      pre_fe = rowMeans(dplyr::across(c(pre_stroop, pre_bds, pre_dccs))),
      post_fe = rowMeans(dplyr::across(c(post_stroop, post_bds, post_dccs)))
    )

  dir.create(dirname(INPUT_FILE), recursive = TRUE, showWarnings = FALSE)
  write.csv(dados_exemplo, INPUT_FILE, row.names = FALSE)
  log_msg("Dados de exemplo criados (N=200)")
}

dados <- read.csv(INPUT_FILE)
dados$grupo <- factor(dados$grupo)
dados$sexo <- factor(dados$sexo)
log_msg(sprintf("Carregadas %d observações de %d grupos",
                nrow(dados), length(unique(dados$grupo))))

# --- 2. Descritivas -------------------------------------
log_msg("Calculando estatísticas descritivas por grupo")

desc_grupo <- dados |>
  dplyr::group_by(grupo) |>
  dplyr::summarise(
    n = dplyr::n(),
    idade_media = mean(idade, na.rm = TRUE),
    idade_dp = sd(idade, na.rm = TRUE),
    pct_feminino = mean(sexo == "F") * 100,
    pre_stroop_media = mean(pre_stroop, na.rm = TRUE),
    pre_stroop_dp = sd(pre_stroop, na.rm = TRUE),
    post_stroop_media = mean(post_stroop, na.rm = TRUE),
    post_stroop_dp = sd(post_stroop, na.rm = TRUE),
    pre_bds_media = mean(pre_bds, na.rm = TRUE),
    pre_bds_dp = sd(pre_bds, na.rm = TRUE),
    post_bds_media = mean(post_bds, na.rm = TRUE),
    post_bds_dp = sd(post_bds, na.rm = TRUE),
    pre_dccs_media = mean(pre_dccs, na.rm = TRUE),
    pre_dccs_dp = sd(pre_dccs, na.rm = TRUE),
    post_dccs_media = mean(post_dccs, na.rm = TRUE),
    post_dccs_dp = sd(post_dccs, na.rm = TRUE),
    .groups = "drop"
  )
print(desc_grupo)
write.csv(desc_grupo, file.path(OUTPUT_DIR, "01_descritivas_por_grupo.csv"))

# --- 3. Verificar pressupostos da ANCOVA ---------------
log_msg("Verificando pressupostos da ANCOVA")

# Função para verificar pressupostos
verificar_pressupostos <- function(modelo, dados, outcome, pretesto) {
  # 1. Normalidade dos resíduos (Shapiro-Wilk)
  residuos <- residuals(modelo)
  shapiro <- shapiro.test(residuos)
  cat(sprintf("\n=== Pressupostos: %s ===\n", outcome))
  cat(sprintf("Shapiro-Wilk W: %.3f, p = %.4f\n",
              shapiro$statistic, shapiro$p.value))
  cat(sprintf("  %s\n", ifelse(shapiro$p.value > 0.05,
                                "✓ Normalidade OK",
                                "✗ Normalidade VIOLADA")))

  # 2. Homogeneidade de variâncias (Levene)
  library(car)
  levene <- car::leveneTest(as.formula(paste(outcome, "~ grupo")), data = dados)
  cat(sprintf("Levene: F = %.3f, p = %.4f\n",
              levene$`F value`[1], levene$`Pr(>F)`[1]))
  cat(sprintf("  %s\n", ifelse(levene$`Pr(>F)`[1] > 0.05,
                                "✓ Homogeneidade OK",
                                "✗ Homogeneidade VIOLADA (usar Welch ANOVA)")))

  # 3. Homogeneidade das slopes de regressão
  # Interação grupo:pretesto não deve ser significativa
  formula_interacao <- as.formula(paste(outcome, "~ grupo *", pretesto))
  modelo_interacao <- lm(formula_interacao, data = dados)
  anova_interacao <- car::Anova(modelo_interacao, type = "III")
  p_interacao <- anova_interacao$`Pr(>F)`[3]  # interação
  cat(sprintf("Interação grupo:%s: p = %.4f\n", pretesto, p_interacao))
  cat(sprintf("  %s\n", ifelse(p_interacao > 0.05,
                                "✓ Slopes homogêneos (ANCOVA válida)",
                                "✗ Slopes heterogêneos (não usar ANCOVA simples)")))

  invisible(list(
    shapiro = shapiro,
    levene = levene,
    interacao_p = p_interacao
  ))
}

# --- 4. ANCOVA: Stroop ----------------------------------
log_msg("ANCOVA 1/3: Stroop (controle inibitório)")

# Modelo
m_stroop <- lm(post_stroop ~ grupo + pre_stroop + idade + sexo, data = dados)

# Pressupostos
press_stroop <- verificar_pressupostos(m_stroop, dados, "post_stroop", "pre_stroop")

# ANOVA tipo III
anova_stroop <- car::Anova(m_stroop, type = "III")
print(anova_stroop)
write.csv(as.data.frame(anova_stroop),
          file.path(OUTPUT_DIR, "02_ancova_stroop.csv"))

# Efeitos parciais (eta²)
eta2_stroop <- effectsize::eta_squared(m_stroop, partial = TRUE)
print(eta2_stroop)
write.csv(as.data.frame(eta2_stroop),
          file.path(OUTPUT_DIR, "02_eta2_stroop.csv"))

# --- 5. ANCOVA: Backward Digit Span --------------------
log_msg("ANCOVA 2/3: Backward Digit Span (memória de trabalho)")

m_bds <- lm(post_bds ~ grupo + pre_bds + idade + sexo, data = dados)
press_bds <- verificar_pressupostos(m_bds, dados, "post_bds", "pre_bds")

anova_bds <- car::Anova(m_bds, type = "III")
print(anova_bds)
write.csv(as.data.frame(anova_bds),
          file.path(OUTPUT_DIR, "03_ancova_bds.csv"))

eta2_bds <- effectsize::eta_squared(m_bds, partial = TRUE)
write.csv(as.data.frame(eta2_bds),
          file.path(OUTPUT_DIR, "03_eta2_bds.csv"))

# --- 6. ANCOVA: DCCS -----------------------------------
log_msg("ANCOVA 3/3: DCCS (flexibilidade cognitiva)")

m_dccs <- lm(post_dccs ~ grupo + pre_dccs + idade + sexo, data = dados)
press_dccs <- verificar_pressupostos(m_dccs, dados, "post_dccs", "pre_dccs")

anova_dccs <- car::Anova(m_dccs, type = "III")
print(anova_dccs)
write.csv(as.data.frame(anova_dccs),
          file.path(OUTPUT_DIR, "04_ancova_dccs.csv"))

eta2_dccs <- effectsize::eta_squared(m_dccs, partial = TRUE)
write.csv(as.data.frame(eta2_dccs),
          file.path(OUTPUT_DIR, "04_eta2_dccs.csv"))

# --- 7. Correção de Bonferroni -------------------------
log_msg("Aplicando correção de Bonferroni para múltiplas comparações")

# Coletar p-valores de "grupo" das 3 ANCOVAs
p_grupos <- c(
  stroop = anova_stroop$`Pr(>F)`[1],
  bds = anova_bds$`Pr(>F)`[1],
  dccs = anova_dccs$`Pr(>F)`[1]
)
p_corrigido <- p.adjust(p_grupos, method = "bonferroni")

correcao <- data.frame(
  outcome = names(p_grupos),
  p_bruto = p_grupos,
  p_bonferroni = p_corrigido,
  significativo_bruto = p_grupos < 0.05,
  significativo_bonferroni = p_corrigido < 0.05
)
print(correcao)
write.csv(correcao,
          file.path(OUTPUT_DIR, "05_correcao_bonferroni.csv"))

# --- 8. Post-hoc: emmeans -----------------------------
log_msg("Calculando post-hoc (emmeans com ajuste de Tukey)")

# Para Stroop
emm_stroop <- emmeans(m_stroop, ~ grupo)
emm_stroop_summary <- summary(emm_stroop)
print(emm_stroop_summary)
write.csv(as.data.frame(emm_stroop_summary),
          file.path(OUTPUT_DIR, "06_emm_stroop.csv"))

# Comparações pareadas (todos os pares)
post_hoc_stroop <- pairs(emm_stroop, adjust = "tukey")
print(post_hoc_stroop)
write.csv(as.data.frame(post_hoc_stroop),
          file.path(OUTPUT_DIR, "07_posthoc_stroop.csv"))

# Para BDS
emm_bds <- emmeans(m_bds, ~ grupo)
post_hoc_bds <- pairs(emm_bds, adjust = "tukey")
write.csv(as.data.frame(post_hoc_bds),
          file.path(OUTPUT_DIR, "07_posthoc_bds.csv"))

# Para DCCS
emm_dccs <- emmeans(m_dccs, ~ grupo)
post_hoc_dccs <- pairs(emm_dccs, adjust = "tukey")
write.csv(as.data.frame(post_hoc_dccs),
          file.path(OUTPUT_DIR, "07_posthoc_dccs.csv"))

# --- 9. Tamanhos de efeito (Cohen's d) ----------------
log_msg("Calculando Cohen's d entre grupos")

# Função para calcular Cohen's d entre 2 grupos
cohens_d <- function(x, y) {
  nx <- length(x)
  ny <- length(y)
  pooled_sd <- sqrt(((nx - 1) * var(x) + (ny - 1) * var(y)) / (nx + ny - 2))
  (mean(x) - mean(y)) / pooled_sd
}

# Cohen's d: cada grupo vs. controle
cohens_d_stroop <- data.frame(comparacao = character(), d = numeric(), ci_lower = numeric(), ci_upper = numeric())

for (g in levels(dados$grupo)) {
  if (g == "CTRL") next
  ctrl <- dados$post_stroop[dados$grupo == "CTRL"]
  g_data <- dados$post_stroop[dados$grupo == g]
  d <- cohens_d(g_data, ctrl)
  n <- length(g_data)
  se <- sqrt((n + n) / (n * n) + d^2 / (2 * n))
  ci_lower <- d - 1.96 * se
  ci_upper <- d + 1.96 * se
  cohens_d_stroop <- rbind(cohens_d_stroop, data.frame(
    comparacao = paste(g, "vs CTRL"),
    d = d,
    ci_lower = ci_lower,
    ci_upper = ci_upper
  ))
}
print(cohens_d_stroop)
write.csv(cohens_d_stroop,
          file.path(OUTPUT_DIR, "08_cohens_d_stroop.csv"))

# --- 10. Visualizações --------------------------------
log_msg("Gerando visualizações")

# Gráfico 1: Boxplot pós-teste por grupo (Stroop)
p1 <- ggplot(dados, aes(x = grupo, y = post_stroop, fill = grupo)) +
  geom_boxplot(alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.3) +
  labs(
    title = "Pós-teste Stroop por grupo",
    x = "Grupo",
    y = "Escore Stroop (pós-teste)"
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(file.path(OUTPUT_DIR, "09_boxplot_stroop.png"),
       p1, width = 10, height = 6, dpi = 100)

# Gráfico 2: Means plot (emmeans)
p2 <- ggplot(as.data.frame(emm_stroop_summary),
             aes(x = grupo, y = emmean, ymin = lower.CL, ymax = upper.CL)) +
  geom_point(size = 3) +
  geom_errorbar(width = 0.2) +
  labs(
    title = "Médias marginais estimadas (emmeans) — Stroop",
    subtitle = "ANCOVA ajustada por pré-teste, idade e sexo",
    x = "Grupo",
    y = "Média marginal (95% IC)"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(file.path(OUTPUT_DIR, "10_emmeans_stroop.png"),
       p2, width = 10, height = 6, dpi = 100)

# Gráfico 3: Pré-pós por grupo
dados_long <- dados |>
  dplyr::select(id, grupo, pre_stroop, post_stroop) |>
  tidyr::pivot_longer(cols = c(pre_stroop, post_stroop),
                      names_to = "tempo", values_to = "escore") |>
  dplyr::mutate(tempo = factor(tempo, levels = c("pre_stroop", "post_stroop"),
                                labels = c("Pré-teste", "Pós-teste")))

p3 <- ggplot(dados_long, aes(x = tempo, y = escore, color = grupo, group = grupo)) +
  stat_summary(fun = mean, geom = "point", size = 3) +
  stat_summary(fun = mean, geom = "line") +
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2) +
  labs(
    title = "Evolução pré-pós por grupo (Stroop)",
    x = "Momento",
    y = "Escore Stroop (média ± EP)",
    color = "Grupo"
  )

ggsave(file.path(OUTPUT_DIR, "11_pre_pos_stroop.png"),
       p3, width = 10, height = 6, dpi = 100)

log_msg("Gráficos salvos")

# --- 11. Análise estratificada por sexo ---------------
log_msg("ANCOVA estratificada por sexo (exploratória)")

resultados_sexo <- list()
for (s in levels(dados$sexo)) {
  dados_s <- dados |> dplyr::filter(sexo == s)
  m_s <- lm(post_stroop ~ grupo + pre_stroop + idade, data = dados_s)
  anova_s <- car::Anova(m_s, type = "III")
  resultados_sexo[[s]] <- anova_s
  cat(sprintf("\n=== Sexo: %s ===\n", s))
  print(anova_s)
}
saveRDS(resultados_sexo, file.path(OUTPUT_DIR, "12_ancova_por_sexo.rds"))

# --- 12. Tabela publicável ----------------------------
log_msg("Gerando tabela publicável")

# Tabela de resultados
tabela_resultados <- data.frame(
  Outcome = c("Stroop (Controle Inibitório)",
              "BDS (Memória de Trabalho)",
              "DCCS (Flexibilidade)"),
  F_grupo = c(anova_stroop$`F value`[1],
              anova_bds$`F value`[1],
              anova_dccs$`F value`[1]),
  p_bruto = c(anova_stroop$`Pr(>F)`[1],
              anova_bds$`Pr(>F)`[1],
              anova_dccs$`Pr(>F)`[1]),
  p_bonferroni = p_corrigido,
  eta2_parcial = c(eta2_stroop$Eta2_partial[1],
                   eta2_bds$Eta2_partial[1],
                   eta2_dccs$Eta2_partial[1])
) |>
  dplyr::mutate(
    significativo = ifelse(p_bonferroni < 0.001, "***",
                            ifelse(p_bonferroni < 0.01, "**",
                                   ifelse(p_bonferroni < 0.05, "*", "ns")))
  )

print(tabela_resultados)
write.csv(tabela_resultados,
          file.path(OUTPUT_DIR, "13_tabela_resultados.csv"))

# --- 13. Relatório final ----------------------------
log_msg("Gerando relatório final")

relatorio <- paste0(
  "===========================================\n",
  "  RELATÓRIO - ANCOVA P02 (Gamificação)\n",
  "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
  "===========================================\n\n",
  "AMOSTRA: ", nrow(dados), " crianças, ",
  length(unique(dados$grupo)), " grupos\n",
  "Grupos: ", paste(levels(dados$grupo), collapse = ", "), "\n\n",
  "DESCRITIVAS:\n",
  paste(capture.output(print(desc_grupo)), collapse = "\n"),
  "\n\nRESULTADOS PRINCIPAIS:\n",
  paste(capture.output(print(tabela_resultados)), collapse = "\n"),
  "\n\nPRESSUPOSTOS:\n",
  "  Stroop: Shapiro p = ", round(press_stroop$shapiro$p.value, 4),
  ", Levene p = ", round(press_stroop$levene$`Pr(>F)`[1], 4),
  ", Slopes interação p = ", round(press_stroop$interacao_p, 4), "\n",
  "  BDS:    Shapiro p = ", round(press_bds$shapiro$p.value, 4),
  ", Levene p = ", round(press_bds$levene$`Pr(>F)`[1], 4),
  ", Slopes interação p = ", round(press_bds$interacao_p, 4), "\n",
  "  DCCS:   Shapiro p = ", round(press_dccs$shapiro$p.value, 4),
  ", Levene p = ", round(press_dccs$levene$`Pr(>F)`[1], 4),
  ", Slopes interação p = ", round(press_dccs$interacao_p, 4), "\n\n",
  "ARQUIVOS GERADOS:\n",
  "  01_descritivas_por_grupo.csv\n",
  "  02-04_ancova_[outcome].csv\n",
  "  02-04_eta2_[outcome].csv\n",
  "  05_correcao_bonferroni.csv\n",
  "  06-08_emm + post-hoc + Cohen's d\n",
  "  09-11_*.png (gráficos)\n",
  "  12_ancova_por_sexo.rds\n",
  "  13_tabela_resultados.csv\n",
  "  relatorio.txt\n"
)

writeLines(relatorio, file.path(OUTPUT_DIR, "relatorio.txt"))
log_msg("Relatório salvo")

# ============================================================
# Fim do pipeline ANCOVA
# ============================================================
log_msg("ANCOVA do P02 concluída com sucesso", level = "SUCCESS")
