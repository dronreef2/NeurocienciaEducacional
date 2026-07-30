# ============================================================
# 00_setup.R
# Setup global do projeto — carrega libraries, configura paths,
# define constantes usadas em todos os scripts.
#
# Uso: source("R/00_setup.R") no início de cada script
# ============================================================

# --- Reprodutibilidade -------------------------------------
# Sempre definir seed no início de qualquer análise
set.seed(42)

# --- Paths -------------------------------------------------
# Usar here::here() para paths relativos (funciona com RStudio,
# CLI, Rscript, etc.)
if (!requireNamespace("here", quietly = TRUE)) {
  install.packages("here")
}
library(here)

# Definir paths do projeto
PATHS <- list(
  dados_brutos      = here("dados", "raw"),
  dados_processados = here("dados", "processed"),
  resultados        = here("resultados"),
  scripts_R         = here("R"),
  scripts_python    = here("Python"),
  refs              = here("..", "00-fundamentos", "notas-leitura")
)

# Criar diretórios se não existirem
for (path in PATHS) {
  if (!dir.exists(path)) dir.create(path, recursive = TRUE)
}

# --- Versões ------------------------------------------------
# Documentar versões para reprodutibilidade
if (requireNamespace("renv", quietly = TRUE)) {
  cat("📦 Versões dos packages:\n")
  print(renv::project())
} else {
  cat("⚠️  renv não instalado. Recomendado: renv::init()\n")
}

# --- Logging ------------------------------------------------
# Função de log simples (substitui print)
log_msg <- function(msg, level = "INFO") {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  cat(sprintf("[%s] %s: %s\n", timestamp, level, msg))
}

# --- Tidyverse e packages centrais --------------------------
# Tidyverse: collection de packages para data science
if (!requireNamespace("tidyverse", quietly = TRUE)) {
  install.packages("tidyverse")
}
library(tidyverse)  # ggplot2, dplyr, tidyr, readr, purrr, tibble, stringr

# Tidytext: análise de texto (para P01 AT)
if (!requireNamespace("tidytext", quietly = TRUE)) {
  install.packages("tidytext")
}
library(tidytext)

# Quanteda: análise quantitativa de texto (para P01 AT)
if (!requireNamespace("quanteda", quietly = TRUE)) {
  install.packages("quanteda")
}
library(quanteda)

# Readxl: ler Excel (para questionários)
if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl")
}
library(readxl)

# Janitor: limpeza de dados
if (!requireNamespace("janitor", quietly = TRUE)) {
  install.packages("janitor")
}
library(janitor)

# patchwork: combinar gráficos ggplot
if (!requireNamespace("patchwork", quietly = TRUE)) {
  install.packages("patchwork")
}
library(patchwork)

# --- Configurações de visualização --------------------------
# Tema padrão para ggplot (limpo, publicável)
theme_set(
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0),
    plot.subtitle = element_text(hjust = 0, color = "grey40"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )
)

# Paleta de cores consistente (colorblind-friendly)
CORES_PROGRAMA <- c(
  primario   = "#1f77b4",  # azul
  secundario = "#ff7f0e",  # laranja
  sucesso    = "#2ca02c",  # verde
  atencao    = "#d62728",  # vermelho
  neutro     = "#7f7f7f"   # cinza
)

# Escala padrão
scale_colour_discrete <- function(...) {
  scale_colour_manual(values = unname(CORES_PROGRAMA), ...)
}

# --- Mensagem de confirmação --------------------------------
log_msg("Setup carregado com sucesso")
log_msg(sprintf("Diretório de trabalho: %s", here()))

# ============================================================
# Fim do setup
# Próximo: source("R/01_at_pipeline.R") para P01
# ============================================================
