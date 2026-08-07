# ============================================================
# 05_tutorial_lgcm.R
# TUTORIAL 5: Latent Growth Curve Models (LGCM) com tidyverse + lavaan
# Para P05 (coorte longitudinal)
# ============================================================

# Verificar/instalar pacotes
if (!require(lavaan)) install.packages("lavaan")
if (!require(tidyverse)) install.packages("tidyverse")
if (!require(broom)) install.packages("broom")

library(lavaan)
library(tidyverse)
library(broom)

cat("========================================\n")
cat("  TUTORIAL 5 — LGCM (P05 Coorte)\n")
cat("========================================\n\n")

# ============================================================
# PASSO 1: O que é LGCM?
# ============================================================
cat("
PASSO 1: O que é Latent Growth Curve Model?

LGCM é um tipo de modelo SEM que descreve trajetórias de mudança
ao longo do tempo usando dois fatores latentes:

  - INTERCEPT: nível inicial (T1)
  - SLOPE: taxa de mudança por unidade de tempo

Em P05, usamos LGCM para modelar:
  - Inibição (BRIEF-2) ao longo de 5 ondas anuais
  - Letramento (PROLETRAMENTO) ao longo de 5 ondas
  - Possível crescimento curvilíneo (não-linear)

VANTAGENS sobre análise de variância (ANOVA):
  - Modela trajetórias individuais (não médias)
  - Permite variabilidade nos interceptos e slopes
  - Inclui preditores do crescimento
  - Modela formas funcionais (linear, quadrática, etc.)
\n")

# ============================================================
# PASSO 2: Simular dados longitudinais
# ============================================================
cat("PASSO 2: Simulando coorte (200 crianças, 5 ondas)\n")

set.seed(42)
n_criancas <- 200
n_ondas <- 5
wave_ids <- rep(1:n_ondas, times = n_criancas)
child_ids <- rep(1:n_criancas, each = n_ondas)

# Parâmetros verdadeiros do LGCM
mu_intercept <- 50
mu_slope <- 2.5  # crescimento de 2.5 pontos/ano
sigma_intercept <- 8
sigma_slope <- 1.5
cov_intercept_slope <- -0.3  # crianças com FE inicial menor crescem mais
sigma_residual <- 3

# Gerar efeitos aleatórios por criança
child_intercept <- rnorm(n_criancas, mu_intercept, sigma_intercept)
child_slope <- mu_slope + (cov_intercept_slope * (child_intercept - mu_intercept) / sigma_intercept^2) +
  rnorm(n_criancas, 0, sqrt(sigma_slope^2 - cov_intercept_slope^2/sigma_intercept^2))

# Compor série
fe_score <- child_intercept[child_ids] + child_slope[child_ids] * (wave_ids - 1) +
  rnorm(n_criancas * n_ondas, 0, sigma_residual)

# Criar data frame long format
dados_long <- data.frame(
  child_id = child_ids,
  wave = wave_ids,
  idade = 7 + (wave_ids - 1),
  fe_score = fe_score
)

# Converter para wide format (necessário para lavaan)
dados_wide <- dados_long %>%
  pivot_wider(
    names_from = wave,
    values_from = fe_score,
    names_prefix = "T"
  )

cat(sprintf("  N crianças: %d\n", n_criancas))
cat(sprintf("  N ondas: %d\n", n_ondas))
cat(sprintf("  N total de observações: %d\n", n_criancas * n_ondas))
cat("\nPrimeiras linhas (wide):\n")
print(head(dados_wide, 3))

# ============================================================
# PASSO 3: LGCM Linear
# ============================================================
cat("\n========================================\n")
cat("PASSO 3: LGCM Linear\n")
cat("========================================\n")

# Especificar o modelo
# i =~ T1 + T2 + T3 + T4 + T5  (intercept = média em todas as ondas)
# s =~ 0*T1 + 1*T2 + 2*T3 + 3*T4 + 4*T5  (slope linear)
modelo_linear <- '
  # Fator latente: Intercept
  i =~ 1*T1 + 1*T2 + 1*T3 + 1*T4 + 1*T5

  # Fator latente: Slope (linear)
  s =~ 0*T1 + 1*T2 + 2*T3 + 3*T4 + 4*T5

  # Covariância livre entre i e s
  i ~~ s
'

# Estimar com lavaan
fit_linear <- growth(modelo_linear, data = dados_wide)
cat("\nResumo do modelo:\n")
summary(fit_linear, fit.measures = TRUE, standardized = TRUE)

# Extrair parâmetros de interesse
params_linear <- parameterEstimates(fit_linear, standardized = TRUE)
cat("\nParâmetros de crescimento:\n")
print(params_linear[params_linear$lhs %in% c("i", "s") & params_linear$op == "~1", ])

# Índices de ajuste
fit_indices <- fitMeasures(fit_linear, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr"))
cat("\nÍndices de ajuste:\n")
print(round(fit_indices, 3))

# ============================================================
# PASSO 4: Comparação com modelo não-linear (quadrático)
# ============================================================
cat("\n========================================\n")
cat("PASSO 4: LGCM Quadrático (não-linear)\n")
cat("========================================\n")

modelo_quadratico <- '
  i =~ 1*T1 + 1*T2 + 1*T3 + 1*T4 + 1*T5
  s =~ 0*T1 + 1*T2 + 2*T3 + 3*T4 + 4*T5
  q =~ 0*T1 + 1*T2 + 4*T3 + 9*T4 + 16*T5  # termo quadrático

  i ~~ s + q
  s ~~ q
'

fit_quad <- growth(modelo_quadratico, data = dados_wide)
cat("\nResumo:\n")
summary(fit_quad, fit.measures = TRUE, standardized = TRUE)

# Comparação de modelos
cat("\n========================================\n")
cat("PASSO 5: Comparação de modelos (anova)\n")
cat("========================================\n")

anova_result <- anova(fit_linear, fit_quad)
print(anova_result)

# AIC e BIC
cat(sprintf("\nAIC linear: %.2f\n", AIC(fit_linear)))
cat(sprintf("AIC quadrático: %.2f\n", AIC(fit_quad)))
cat(sprintf("BIC linear: %.2f\n", BIC(fit_linear)))
cat(sprintf("BIC quadrático: %.2f\n", BIC(fit_quad)))

if (AIC(fit_linear) < AIC(fit_quad)) {
  cat("\n✓ Linear tem menor AIC — modelo linear é suficiente\n")
} else {
  cat("\n✓ Quadrático tem menor AIC — crescimento é não-linear\n")
}

# ============================================================
# PASSO 6: Adicionar preditores do crescimento
# ============================================================
cat("\n========================================\n")
cat("PASSO 6: LGCM com preditores (sexo, SES)\n")
cat("========================================\n")

# Adicionar covariáveis
set.seed(42)
dados_wide$sexo <- sample(c(0, 1), n_criancas, replace = TRUE)
dados_wide$ses <- rnorm(n_criancas, 0, 1)

modelo_com_covs <- '
  # Modelo de crescimento
  i =~ 1*T1 + 1*T2 + 1*T3 + 1*T4 + 1*T5
  s =~ 0*T1 + 1*T2 + 2*T3 + 3*T4 + 4*T5

  # Covariáveis preditoras
  i ~ sexo + ses
  s ~ sexo + ses
'

fit_covs <- growth(modelo_com_covs, data = dados_wide)
cat("\nEfeito das covariáveis:\n")
summary(fit_covs)$pe %>% filter(op == "~") %>% print()

# ============================================================
# PASSO 7: Visualização das trajetórias
# ============================================================
cat("\n========================================\n")
cat("PASSO 7: Visualização das trajetórias\n")
cat("========================================\n")

# Calcular trajetórias previstas
pred_linear <- predict(fit_linear)
trajectories <- data.frame(
  child_id = 1:n_criancas,
  intercept = pred_linear[, "i"],
  slope = pred_linear[, "s"]
)

# Média das trajetórias previstas
wave_seq <- 0:4
mean_traj <- trajectories$intercept + trajectories$slope * wave_seq
mean_traj <- colMeans(matrix(mean_traj, nrow = n_criancas))

# Plot
png("resultados/figura16_lgcm.png", width = 1200, height = 800, res = 150)
par(mfrow = c(2, 2))

# Painel 1: Trajetórias individuais
plot(0, 0, type = "n", xlim = c(0, 4), ylim = c(20, 80),
     xlab = "Onda", ylab = "FE Score",
     main = "Trajetórias individuais + média")

# Plotar 30 trajetórias
for (i in sample(1:n_criancas, 30)) {
  traj <- trajectories$intercept[i] + trajectories$slope[i] * wave_seq
  lines(wave_seq, traj, col = rgb(0.5, 0.5, 0.5, 0.5))
}
lines(wave_seq, mean_traj, col = "red", lwd = 3)
legend("topleft", c("30 crianças aleatórias", "Média prevista"),
       col = c("gray", "red"), lty = 1, lwd = c(1, 3))

# Painel 2: Distribuição de interceptos
hist(trajectories$intercept, breaks = 30, col = "steelblue",
     main = "Distribuição dos interceptos", xlab = "Intercept")

# Painel 3: Distribuição de slopes
hist(trajectories$slope, breaks = 30, col = "coral",
     main = "Distribuição dos slopes", xlab = "Slope (crescimento/ano)")

# Painel 4: Intercept vs Slope
plot(trajectories$intercept, trajectories$slope,
     pch = 19, col = rgb(0.4, 0.4, 0.4, 0.5),
     main = "Intercept vs Slope",
     xlab = "Intercept", ylab = "Slope")
abline(h = 0, col = "red", lty = 2)

dev.off()
cat("✅ Figura 16 salva: resultados/figura16_lgcm.png\n")

# ============================================================
# PASSO 8: Conclusões
# ============================================================
cat("\n========================================\n")
cat("PASSO 8: CONCLUSÕES — LGCM\n")
cat("========================================\n")

cat(sprintf("
RESUMO DO LGCM (P05):

Parâmetros estimados:
  Intercepto médio: %.2f (verdadeiro: %.0f)
  Slope médio:      %.2f (verdadeiro: %.1f)
  SD intercepto:    %.2f (verdadeiro: %.0f)
  SD slope:         %.2f (verdadeiro: %.1f)
  Cov(i,s):         %.2f (verdadeiro: %.1f)

Índices de ajuste:
  CFI:  %.3f
  TLI:  %.3f
  RMSEA: %.3f
  SRMR: %.3f

Modelo vencedor: %s

PRÓXIMOS PASSOS (P05 real):
  1. LGCM com 5 ondas reais (após T5)
  2. Adicionar covariáveis biológicas (DNA polimorfismos)
  3. LGMM (Latent Growth Mixture Modeling) para identificar subgrupos
  4. CLPM para relações bidirecionais FE ↔ letramento
  5. Cross-lagged com EEG (N170 mudança ao longo do tempo)
\n", fit_indices["cfi"], fit_indices["tli"], fit_indices["rmsea"], fit_indices["srmr"],
   ifelse(AIC(fit_linear) < AIC(fit_quad), "Linear", "Quadrático")))
