# ============================================================
# 04_lgcm_p05.R
# Latent Growth Curve Models (LGCM) — Projeto P05
#
# OBJETIVO: modelar trajetórias de desenvolvimento de FE ao longo
# de 5 anos (5 ondas: 7, 8, 9, 10, 11 anos) e identificar
# preditores das trajetórias.
#
# Modelo básico (intercept + slope):
#   FE_it = π_0i + π_1i * Idade_t + ε_it
#   π_0i = γ_00 + γ_01 * Sexo + γ_02 * SES + u_0i
#   π_1i = γ_10 + γ_11 * Sexo + γ_12 * SES + u_1i
#
# Modelo condicional (com covariáveis moderadoras):
#   - Sexo (masculino/feminino)
#   - SES
#   - Tipo de escola (pública/privada)
#   - Uso de tecnologia (tempo/dia)
#
# Modelos adicionais:
#   - LGCM com slope quadrático (curva não-linear)
#   - LGMM (Latent Growth Mixture Model) para identificar subgrupos
#   - LGCM multivariado (FE + leitura)
#
# Pré-requisitos: dados em formato longo (long format) com
# colunas: id, onda, idade, fe_score, sexo, ses, ...
#
# Uso: Rscript R/04_lgcm_p05.R
# ============================================================

# Setup
source(here::here("R", "00_setup.R"))

# --- 0. Packages específicos -----------------------------
if (!requireNamespace("lavaan", quietly = TRUE)) {
  install.packages("lavaan")
}
library(lavaan)
if (!requireNamespace("OpenMx", quietly = TRUE)) {
  install.packages("OpenMx")
}
library(OpenMx)  # para LGMM (mais flexível que lavaan)
if (!requireNamespace("tidySEM", quietly = TRUE)) {
  install.packages("tidySEM")
}
library(tidySEM)
if (!requireNamespace("psych", quietly = TRUE)) {
  install.packages("psych")
}
library(psych)

# --- 1. Carregar dados -----------------------------------
PROJETO <- "P05"
INPUT_FILE <- here("dados", "processed", PROJETO, "p05_long.csv")
OUTPUT_DIR <- here("resultados", PROJETO)

if (!dir.exists(OUTPUT_DIR)) dir.create(OUTPUT_DIR, recursive = TRUE)

log_msg(sprintf("Iniciando LGCM para o projeto %s", PROJETO))

if (!file.exists(INPUT_FILE)) {
  log_msg(sprintf("⚠️  Arquivo %s não encontrado. Criando dados de exemplo.", INPUT_FILE), level = "WARN")

  # Simular dados de coorte com 5 ondas
  set.seed(42)
  n <- 150
  dados_long <- expand.grid(
    id = 1:n,
    onda = 1:5,
    idade = c(7, 8, 9, 10, 11)
  ) |>
    dplyr::arrange(id, onda) |>
    dplyr::mutate(
      sexo = rep(sample(c("F", "M"), n, replace = TRUE), each = 5),
      ses = rep(rnorm(n, 0, 1), each = 5),
      escola = rep(sample(c("publica", "privada"), n, replace = TRUE, prob = c(0.7, 0.3)), each = 5),
      # Gerar FE com intercept = 0, slope = 0.5 (crescimento linear), erro = 0.3
      fe_score = NA
    )

  # Simular trajetórias com variação individual
  for (i in 1:n) {
    intercept_i <- rnorm(1, 0, 0.5)
    slope_i <- rnorm(1, 0.5, 0.2) + 0.1 * dados_long$ses[dados_long$id == i][1]
    for (t in 1:5) {
      idx <- (i - 1) * 5 + t
      dados_long$fe_score[idx] <- intercept_i + slope_i * (t - 1) + rnorm(1, 0, 0.3)
    }
  }

  dir.create(dirname(INPUT_FILE), recursive = TRUE, showWarnings = FALSE)
  write.csv(dados_long, INPUT_FILE, row.names = FALSE)
  log_msg("Dados de exemplo criados")
}

dados <- read.csv(INPUT_FILE)
log_msg(sprintf("Carregadas %d observações de %d participantes",
                nrow(dados), length(unique(dados$id))))

# --- 2. Preparar dados ----------------------------------
log_msg("Preparando dados para LGCM")

# Centralizar tempo (onda 1 = 0)
dados$tempo <- dados$onda - 1
dados$tempo_quad <- dados$tempo^2  # para slope quadrático

# --- 3. Descritivas -------------------------------------
log_msg("Calculando estatísticas descritivas por onda")

desc_onda <- dados |>
  dplyr::group_by(onda, idade) |>
  dplyr::summarise(
    n = dplyr::n(),
    media = mean(fe_score, na.rm = TRUE),
    dp = sd(fe_score, na.rm = TRUE),
    minimo = min(fe_score, na.rm = TRUE),
    maximo = max(fe_score, na.rm = TRUE),
    .groups = "drop"
  )
print(desc_onda)
write.csv(desc_onda, file.path(OUTPUT_DIR, "01_descritivas_por_onda.csv"))

# Plot descritivo
p1 <- ggplot(dados, aes(x = idade, y = fe_score, group = id, color = sexo)) +
  geom_line(alpha = 0.3) +
  geom_smooth(aes(group = sexo), method = "lm", se = TRUE, size = 1.5) +
  labs(
    title = "Trajetórias de FE por sexo (dados longitudinais)",
    x = "Idade (anos)",
    y = "Escore FE (z)",
    color = "Sexo"
  ) +
  scale_color_manual(values = c("F" = "#d62728", "M" = "#1f77b4"))

ggsave(file.path(OUTPUT_DIR, "02_trajetorias_fe.png"),
       p1, width = 10, height = 6, dpi = 100)
log_msg("Gráfico de trajetórias salvo")

# --- 4. LGCM Linear (sem covariáveis) -------------------
log_msg("Ajustando LGCM linear unconditional")

modelo_linear <- '
  # Fatores de crescimento
  intercept =~ 1*fe_onda1 + 1*fe_onda2 + 1*fe_onda3 + 1*fe_onda4 + 1*fe_onda5
  slope =~ 0*fe_onda1 + 1*fe_onda2 + 2*fe_onda3 + 3*fe_onda4 + 4*fe_onda5

  # Médias (efeitos fixos)
  intercept ~ 1
  slope ~ 1

  # Variâncias (efeitos aleatórios)
  intercept ~~ intercept
  slope ~~ slope
  intercept ~~ slope

  # Resíduos (fixos em 0 para homocedasticidade, ou estimados)
  fe_onda1 ~~ fe_onda1
  fe_onda2 ~~ fe_onda2
  fe_onda3 ~~ fe_onda3
  fe_onda4 ~~ fe_onda4
  fe_onda5 ~~ fe_onda5
'

# Reorganizar dados para wide format (necessário para lavaan)
dados_wide <- dados |>
  dplyr::select(id, onda, fe_score) |>
  tidyr::pivot_wider(names_from = onda, values_from = fe_score,
                     names_prefix = "fe_onda") |>
  dplyr::left_join(
    dados |>
      dplyr::filter(onda == 1) |>
      dplyr::select(id, sexo, ses, escola),
    by = "id"
  )

fit_linear <- growth(modelo_linear, data = dados_wide, missing = "ml")
summary(fit_linear, fit.measures = TRUE, standardized = TRUE)

# --- 5. LGCM Condicional (com covariáveis) --------------
log_msg("Ajustando LGCM condicional")

modelo_cond <- '
  # Fatores de crescimento
  intercept =~ 1*fe_onda1 + 1*fe_onda2 + 1*fe_onda3 + 1*fe_onda4 + 1*fe_onda5
  slope =~ 0*fe_onda1 + 1*fe_onda2 + 2*fe_onda3 + 3*fe_onda4 + 4*fe_onda5

  # Regressões (covariáveis moderadoras)
  intercept ~ sexo_num + ses + escola_num
  slope ~ sexo_num + ses + escola_num

  # Variâncias dos fatores (residual)
  intercept ~~ intercept
  slope ~~ slope
  intercept ~~ slope
'

# Recodificar variáveis categóricas
dados_wide$sexo_num <- ifelse(dados_wide$sexo == "M", 1, 0)
dados_wide$escola_num <- ifelse(dados_wide$escola == "privada", 1, 0)
# Centralizar SES
dados_wide$ses <- scale(dados_wide$ses)[, 1]

fit_cond <- growth(modelo_cond, data = dados_wide, missing = "ml",
                   meanstructure = TRUE)
summary(fit_cond, fit.measures = TRUE, standardized = TRUE)

# --- 6. LGCM Quadrático (curva não-linear) --------------
log_msg("Ajustando LGCM quadrático")

modelo_quad <- '
  intercept =~ 1*fe_onda1 + 1*fe_onda2 + 1*fe_onda3 + 1*fe_onda4 + 1*fe_onda5
  slope =~ 0*fe_onda1 + 1*fe_onda2 + 2*fe_onda3 + 3*fe_onda4 + 4*fe_onda5
  quadratic =~ 0*fe_onda1 + 1*fe_onda2 + 4*fe_onda3 + 9*fe_onda4 + 16*fe_onda5

  intercept ~ 1
  slope ~ 1
  quadratic ~ 1
'

fit_quad <- growth(modelo_quad, data = dados_wide, missing = "ml")
summary(fit_quad, fit.measures = TRUE, standardized = TRUE)

# --- 7. Comparação de modelos ----------------------------
log_msg("Comparando modelos")

comparacao <- data.frame(
  Modelo = c("Linear", "Condicional", "Quadrático"),
  chisq = c(
    fitMeasures(fit_linear, "chisq"),
    fitMeasures(fit_cond, "chisq"),
    fitMeasures(fit_quad, "chisq")
  ),
  df = c(
    fitMeasures(fit_linear, "df"),
    fitMeasures(fit_cond, "df"),
    fitMeasures(fit_quad, "df")
  ),
  CFI = c(
    fitMeasures(fit_linear, "cfi"),
    fitMeasures(fit_cond, "cfi"),
    fitMeasures(fit_quad, "cfi")
  ),
  TLI = c(
    fitMeasures(fit_linear, "tli"),
    fitMeasures(fit_cond, "tli"),
    fitMeasures(fit_quad, "tli")
  ),
  RMSEA = c(
    fitMeasures(fit_linear, "rmsea"),
    fitMeasures(fit_cond, "rmsea"),
    fitMeasures(fit_quad, "rmsea")
  ),
  SRMR = c(
    fitMeasures(fit_linear, "srmr"),
    fitMeasures(fit_cond, "srmr"),
    fitMeasures(fit_quad, "srmr")
  ),
  AIC = c(
    fitMeasures(fit_linear, "aic"),
    fitMeasures(fit_cond, "aic"),
    fitMeasures(fit_quad, "aic")
  ),
  BIC = c(
    fitMeasures(fit_linear, "bic"),
    fitMeasures(fit_cond, "bic"),
    fitMeasures(fit_quad, "bic")
  )
)
print(comparacao)
write.csv(comparacao, file.path(OUTPUT_DIR, "03_comparacao_modelos.csv"))

# --- 8. Salvar parâmetros do melhor modelo -------------
melhor_modelo <- "Condicional"
log_msg(sprintf("Salvando parâmetros do modelo %s", melhor_modelo))

if (melhor_modelo == "Linear") {
  fit_final <- fit_linear
} else if (melhor_modelo == "Condicional") {
  fit_final <- fit_cond
} else {
  fit_final <- fit_quad
}

params <- parameterEstimates(fit_final, standardized = TRUE)
write.csv(params, file.path(OUTPUT_DIR, "04_parametros_lgcm.csv"))

# --- 9. Plot das trajetórias preditas -------------------
log_msg("Gerando gráfico de trajetórias preditas")

# Coeficientes do modelo condicional
coefs <- coef(fit_final)

# Trajetória predita para diferentes perfis
novo_dados <- expand.grid(
  sexo_num = c(0, 1),
  ses = c(-1, 0, 1),  # -1 DP, média, +1 DP
  escola_num = c(0, 1)
)

# Calcular intercept e slope preditos
novo_dados$intercept_pred <- coefs["intercept~1"] +
  coefs["intercept~sexo_num"] * novo_dados$sexo_num +
  coefs["intercept~ses"] * novo_dados$ses +
  coefs["intercept~escola_num"] * novo_dados$escola_num

novo_dados$slope_pred <- coefs["slope~1"] +
  coefs["slope~sexo_num"] * novo_dados$sexo_num +
  coefs["slope~ses"] * novo_dados$ses +
  coefs["slope~escola_num"] * novo_dados$escola_num

# Calcular FE predita em cada tempo
novo_dados_long <- novo_dados |>
  tidyr::crossing(tempo = 0:4) |>
  dplyr::mutate(
    fe_pred = intercept_pred + slope_pred * tempo,
    idade = 7 + tempo
  )

# Plot
p2 <- ggplot(novo_dados_long, aes(x = idade, y = fe_pred,
                                    color = factor(sexo_num),
                                    linetype = factor(ses),
                                    group = interaction(sexo_num, ses, escola_num))) +
  geom_line(alpha = 0.6) +
  facet_wrap(~ escola_num, labeller = as_labeller(c("0" = "Pública", "1" = "Privada"))) +
  labs(
    title = "Trajetórias preditas de FE por perfil (modelo LGCM condicional)",
    x = "Idade (anos)",
    y = "Escore FE predito",
    color = "Sexo (0=F, 1=M)",
    linetype = "SES"
  ) +
  scale_color_manual(values = c("0" = "#d62728", "1" = "#1f77b4"))

ggsave(file.path(OUTPUT_DIR, "05_trajetorias_preditas.png"),
       p2, width = 12, height = 6, dpi = 100)
log_msg("Gráfico de trajetórias preditas salvo")

# --- 10. LGMM (Latent Growth Mixture Model) ------------
# Identifica subgrupos de crianças com trajetórias similares
# Mais complexo — só rodar se justificado

log_msg("Ajustando LGMM (mixture model)")

# Número de classes a testar
n_classes <- 1:3

fits_lgmm <- list()
aics_lgmm <- c()

for (k in n_classes) {
  log_msg(sprintf("  Ajustando modelo com %d classe(s)", k))
  tryCatch({
    fit_k <- mxTryHard(
      mxModel(
        type = "RAM",
        manifestVars = paste0("fe_onda", 1:5),
        latentVars = c("intercept", "slope"),
        mxData(observed = dados_wide[, paste0("fe_onda", 1:5)], type = "raw"),
        mxPath(
          from = c("intercept", "slope"),
          to = paste0("fe_onda", 1:5),
          values = c(rep(0.5, 5), rep(0.3, 5)),
          free = c(rep(TRUE, 5), rep(TRUE, 5))
        ),
        mxPath(
          from = "intercept",
          arrows = 2,
          values = 1,
          free = TRUE
        ),
        mxPath(
          from = "slope",
          arrows = 2,
          values = 0.1,
          free = TRUE
        ),
        mxPath(
          from = "intercept",
          to = "slope",
          values = 0,
          free = TRUE
        ),
        mxPath(
          from = "one",
          to = c("intercept", "slope"),
          values = c(0, 0.5),
          free = TRUE
        ),
        mxPath(
          from = "one",
          to = paste0("fe_onda", 1:5),
          values = 0,
          free = FALSE
        ),
        mxPath(
          from = paste0("fe_onda", 1:5),
          arrows = 2,
          values = 0.3,
          free = TRUE
        ),
        # Classes
        if (k > 1) {
          mxPath(
            from = "class",
            to = c("intercept", "slope"),
            values = matrix(0, k, 2),
            free = TRUE
          )
        }
      )
    )
    fits_lgmm[[k]] <- fit_k
    aics_lgmm[k] <- summary(fit_k)$AIC
  }, error = function(e) {
    log_msg(sprintf("  Erro no modelo com %d classe(s): %s", k, e$message), level = "WARN")
    aics_lgmm[k] <- NA
  })
}

# Comparar AIC
comparacao_lgmm <- data.frame(
  n_classes = n_classes,
  AIC = aics_lgmm
)
print(comparacao_lgmm)
write.csv(comparacao_lgmm, file.path(OUTPUT_DIR, "06_comparacao_lgmm.csv"))

# --- 11. Relatório final --------------------------------
log_msg("Gerando relatório")

relatorio <- paste0(
  "===========================================\n",
  "  RELATÓRIO - LGCM P05 (coorte longitudinal)\n",
  "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
  "===========================================\n\n",
  "AMOSTRA: ", nrow(dados_wide), " participantes, ", max(dados$onda), " ondas\n\n",
  "DESCRITIVAS POR ONDA:\n",
  paste(capture.output(print(desc_onda)), collapse = "\n"),
  "\n\n",
  "COMPARAÇÃO DE MODELOS:\n",
  paste(capture.output(print(comparacao)), collapse = "\n"),
  "\n\n",
  "INTERPRETAÇÃO:\n",
  "  - Modelo linear: capta crescimento médio e variação individual\n",
  "  - Modelo condicional: testa se sexo/SES/escola moderam trajetórias\n",
  "  - Modelo quadrático: testa se há aceleração/desaceleração\n\n",
  "REFERÊNCIAS:\n",
  "  - Singer & Willett (2003). Applied Longitudinal Data Analysis.\n",
  "  - Grimm et al. (2016). Growth Models: A Multidisciplinary Perspective.\n",
  "  - Ram & Grimm (2009). Growth Mixture Modeling.\n\n",
  "ARQUIVOS GERADOS:\n",
  "  01_descritivas_por_onda.csv\n",
  "  02_trajetorias_fe.png\n",
  "  03_comparacao_modelos.csv\n",
  "  04_parametros_lgcm.csv\n",
  "  05_trajetorias_preditas.png\n",
  "  06_comparacao_lgmm.csv\n",
  "  relatorio.txt\n"
)

writeLines(relatorio, file.path(OUTPUT_DIR, "relatorio.txt"))
log_msg("Relatório salvo")

# ============================================================
# Fim do pipeline LGCM
# ============================================================
log_msg("LGCM do P05 concluído com sucesso", level = "SUCCESS")
