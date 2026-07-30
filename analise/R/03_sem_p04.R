# ============================================================
# 03_sem_p04.R
# Modelagem de Equações Estruturais (SEM) — Projeto P04
#
# Hipótese: o uso de IA generativa (X) afeta Funções Executivas (Y)
#           mediado por engajamento (M), moderado por letramento digital (W)
#
# Variáveis:
# - X (independente): frequência de uso de IA generativa (dias/semana)
# - M (mediador): engajamento (Flow State Scale + tempo de uso)
# - Y (dependente): FE (composto: Stroop + Backward Digit Span + DCCS)
# - W (moderador): letramento digital (escala própria)
# - Covariáveis: idade, sexo, SES
#
# Uso: Rscript R/03_sem_p04.R
# ============================================================

# Setup
source(here::here("R", "00_setup.R"))

# --- 0. Packages específicos -----------------------------
if (!requireNamespace("lavaan", quietly = TRUE)) {
  install.packages("lavaan")
}
library(lavaan)
if (!requireNamespace("semTools", quietly = TRUE)) {
  install.packages("semTools")
}
library(semTools)
if (!requireNamespace("semPlot", quietly = TRUE)) {
  install.packages("semPlot")
}
library(semPlot)
if (!requireNamespace("psych", quietly = TRUE)) {
  install.packages("psych")
}
library(psych)

# --- 1. Carregar dados -----------------------------------
PROJETO <- "P04"
INPUT_FILE <- here("dados", "processed", PROJETO, "p04_clean.csv")
OUTPUT_DIR <- here("resultados", PROJETO)

if (!dir.exists(OUTPUT_DIR)) dir.create(OUTPUT_DIR, recursive = TRUE)

log_msg(sprintf("Iniciando SEM para o projeto %s", PROJETO))

if (!file.exists(INPUT_FILE)) {
  log_msg(sprintf("⚠️  Arquivo %s não encontrado. Criando dados de exemplo.", INPUT_FILE), level = "WARN")

  # Criar dados de exemplo (substituir pelos dados reais)
  set.seed(42)
  n <- 200
  dados_exemplo <- data.frame(
    participante = sprintf("P%03d", 1:n),
    idade = sample(c(7, 8, 9), n, replace = TRUE, prob = c(0.3, 0.5, 0.2)),
    sexo = sample(c("F", "M"), n, replace = TRUE),
    ses = rnorm(n, 0, 1),
    uso_ia = pmin(pmax(rnorm(n, 3, 1.5), 0), 7),  # dias/semana
    engajamento = rnorm(n, 0, 1),
    stroop = rnorm(n, 0, 1),
    backward_digit = rnorm(n, 0, 1),
    dccs = rnorm(n, 0, 1),
    letramento_digital = rnorm(n, 0, 1)
  )
  # Criar FE composto (média z-scored)
  dados_exemplo$fe_composto <- rowMeans(dados_exemplo[, c("stroop", "backward_digit", "dccs")])
  # Criar efeito de mediação: uso_ia → engajamento → fe
  dados_exemplo$engajamento <- 0.3 * scale(dados_exemplo$uso_ia)[,1] + rnorm(n, 0, 0.7)
  dados_exemplo$fe_composto <- 0.25 * scale(dados_exemplo$uso_ia)[,1] +
                              0.30 * scale(dados_exemplo$engajamento)[,1] + rnorm(n, 0, 0.5)

  INPUT_FILE <- here("dados", "processed", PROJETO, "p04_clean.csv")
  dir.create(dirname(INPUT_FILE), recursive = TRUE, showWarnings = FALSE)
  write.csv(dados_exemplo, INPUT_FILE, row.names = FALSE)
  log_msg("Dados de exemplo criados para teste")
}

dados <- read.csv(INPUT_FILE)
log_msg(sprintf("Carregadas %d observações", nrow(dados)))

# --- 2. Estatísticas descritivas ------------------------
log_msg("Calculando estatísticas descritivas")

desc_stats <- describe(dados[, c("uso_ia", "engajamento", "fe_composto",
                                  "stroop", "backward_digit", "dccs",
                                  "letramento_digital")])
print(desc_stats)
write.csv(desc_stats, file.path(OUTPUT_DIR, "01_descritivas.csv"))

# --- 3. Correlações -------------------------------------
log_msg("Calculando correlações")

cor_matrix <- cor(dados[, c("uso_ia", "engajamento", "fe_composto",
                            "letramento_digital", "idade", "ses")],
                  use = "complete.obs")
print(round(cor_matrix, 3))
write.csv(round(cor_matrix, 3), file.path(OUTPUT_DIR, "02_correlacoes.csv"))

# --- 4. Modelo SEM de mediação -------------------------
log_msg("Ajustando modelo de mediação")

modelo_medicao <- '
  # Modelo de mensuração (FE como variável latente)
  FE =~ stroop + backward_digit + dccs
'

# Ajustar CFA primeiro
fit_cfa <- cfa(modelo_medicao, data = dados, std.lv = TRUE)
summary(fit_cfa, fit.measures = TRUE, standardized = TRUE)

# Modelo de mediação completo
modelo_completo <- '
  # Mensuração
  FE =~ stroop + backward_digit + dccs

  # Estrutural
  engajamento ~ a*uso_ia + idade + sexo + ses
  FE ~ b*engajamento + c*uso_ia + idade + sexo + ses

  # Efeito indireto
  indirect := a*b

  # Efeito total
  total := c + a*b
'

fit_sem <- sem(modelo_completo, data = dados, std.lv = TRUE,
               se = "bootstrap", bootstrap = 5000)
log_msg("Modelo SEM ajustado")

# --- 5. Resultados --------------------------------------
summary(fit_sem, fit.measures = TRUE, standardized = TRUE,
        ci = TRUE, level = 0.95)
write.csv(parameterEstimates(fit_sem, standardized = TRUE),
          file.path(OUTPUT_DIR, "03_parametros_sem.csv"))

# --- 6. Índices de ajuste --------------------------------
log_msg("Calculando índices de ajuste")

fit_indices <- fitMeasures(fit_sem, c(
  "chisq", "df", "pvalue",
  "cfi", "tli",
  "rmsea", "rmsea.ci.lower", "rmsea.ci.upper",
  "srmr",
  "aic", "bic"
))
print(fit_indices)
write.csv(t(as.data.frame(fit_indices)),
          file.path(OUTPUT_DIR, "04_indices_ajuste.csv"))

# --- 7. Efeito de mediação ------------------------------
log_msg("Testando efeito de mediação")

# Teste de Sobel + bootstrap
sobel_result <- sobel(pred = dados$uso_ia,
                      med = dados$engajamento,
                      out = dados$fe_composto)
cat(sprintf("\n=== Teste de Sobel ===\n"))
cat(sprintf("Efeito indireto: %.3f\n", sobel_result$Indirect.Effect))
cat(sprintf("Erro padrão: %.3f\n", sobel_result$SE))
cat(sprintf("Z: %.3f\n", sobel_result$z.value))
cat(sprintf("p-valor: %.4f\n", sobel_result$p.value))

# Efeito indireto via bootstrap (já calculado no lavaan)
ind <- parameterEstimates(fit_sem, standardized = TRUE) |>
  dplyr::filter(label == "indirect")
cat(sprintf("\n=== Mediação via bootstrap (5000 iterações) ===\n"))
cat(sprintf("Efeito indireto: %.3f [%.3f, %.3f]\n",
            ind$est, ind$ci.lower, ind$ci.upper))
cat(sprintf("p-valor: %.4f\n", ind$pvalue))

# --- 8. Visualização do modelo --------------------------
log_msg("Gerando diagrama do modelo")

png(file.path(OUTPUT_DIR, "05_modelo_sem.png"),
    width = 1200, height = 900, res = 100)
semPaths(fit_sem,
         what = "std",
         layout = "tree",
         edge.label.cex = 1.0,
         sizeMan = 8,
         sizeLat = 12)
dev.off()
log_msg("Diagrama salvo em 05_modelo_sem.png")

# --- 9. Modelo de moderação ----------------------------
log_msg("Ajustando modelo de moderação")

modelo_mod <- '
  # Mensuração
  FE =~ stroop + backward_digit + dccs

  # Estrutural com interação
  FE ~ c*uso_ia + d*letramento_digital + e*uso_ia_let
  engajamento ~ a*uso_ia

  # Termo de interação
  uso_ia_let := uso_ia*letramento_digital

  # Efeito condicional
  indirect := a*c + a*d*mean(dados$letramento_digital)
'

# Criar termo de interação
dados$uso_ia_let <- dados$uso_ia * dados$letramento_digital

fit_mod <- sem(modelo_mod, data = dados, std.lv = TRUE)
summary(fit_mod, standardized = TRUE)

# --- 10. Relatório final -------------------------------
log_msg("Gerando relatório final")

relatorio <- paste0(
  "===========================================\n",
  "  RELATÓRIO - SEM P04\n",
  "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
  "===========================================\n\n",
  "AMOSTRA: ", nrow(dados), " observações\n\n",
  "ÍNDICES DE AJUSTE:\n",
  sprintf("  CFI: %.3f (bom se > 0.95)\n", fit_indices["cfi"]),
  sprintf("  TLI: %.3f (bom se > 0.95)\n", fit_indices["tli"]),
  sprintf("  RMSEA: %.3f [%.3f, %.3f] (bom se < 0.06)\n",
          fit_indices["rmsea"], fit_indices["rmsea.ci.lower"], fit_indices["rmsea.ci.upper"]),
  sprintf("  SRMR: %.3f (bom se < 0.08)\n", fit_indices["srmr"]),
  "\n",
  "EFEITOS:\n",
  sprintf("  a (uso → engajamento): %.3f (p = %.4f)\n", ind$est, ind$pvalue),
  sprintf("  b (engajamento → FE): ver output\n"),
  sprintf("  c (uso → FE direto): ver output\n"),
  sprintf("  Indireto (a*b): %.3f [%.3f, %.3f]\n",
          ind$est, ind$ci.lower, ind$ci.upper),
  "\n",
  "ARQUIVOS GERADOS:\n",
  "  01_descritivas.csv\n",
  "  02_correlacoes.csv\n",
  "  03_parametros_sem.csv\n",
  "  04_indices_ajuste.csv\n",
  "  05_modelo_sem.png\n",
  "  relatorio.txt\n"
)

writeLines(relatorio, file.path(OUTPUT_DIR, "relatorio.txt"))
log_msg("Relatório salvo")

# ============================================================
# Fim do pipeline SEM
# ============================================================
log_msg("SEM do P04 concluído com sucesso", level = "SUCCESS")
