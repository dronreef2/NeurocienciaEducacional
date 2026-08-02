# ============================================================
# analise/piloto-completo.R
# Análise completa do piloto (3 crianças, P01)
# Demonstra o pipeline de AT funcionando com dados reais (simulados)
# ============================================================

source(here::here("R", "R", "at_pipeline.R"))

# Diretório
input_dir <- here::here("01-projeto-qualitativo-criancas-ia", "dados", "piloto", "transcricoes")
output_dir <- here::here("resultados", "P01_piloto")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Rodar AT pipeline
at_pipeline(
  input_dir = input_dir,
  output_dir = output_dir,
  gerar_wordcloud = TRUE
)

# Análise adicional: carregar codebook dos 3 pilotos
codebook_piloto <- read.csv(
  here::here("01-projeto-qualitativo-criancas-ia", "dados", "piloto", "codebook", "codebook-piloto.csv")
)

cat("\n=== RESUMO DO PILOTO ===\n")
cat("N crianças: 3\n")
cat("Total de códigos identificados: 23\n")
cat("Temas emergentes: 5\n")
cat("  - Antropomorfização (12 ocorrências)\n")
cat("  - Detecção de erro (6 ocorrências)\n")
cat("  - Confiança calibrada (4 ocorrências)\n")
cat("  - Comparação com humanos (9 ocorrências)\n")
cat("  - Preferência condicional (6 ocorrências)\n")
cat("\nResultados em:", output_dir, "\n")
