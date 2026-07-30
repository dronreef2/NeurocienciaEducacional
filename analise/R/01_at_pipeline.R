# ============================================================
# 01_at_pipeline.R
# Pipeline de Análise Temática (AT) Reflexiva — Projeto P01
#
# OBJETIVO: pré-processar entrevistas transcritas, gerar códigos
# iniciais, calcular frequências, e exportar codebook para
# codificação manual no Taguette.
#
# PRÉ-REQUISITOS:
# - Dados brutos em dados/raw/P01/ (formato: .txt, um por criança)
# - Setup carregado
# - Taguette (https://www.taguette.org/) instalado para
#   codificação manual complementar
#
# Uso: Rscript R/01_at_pipeline.R
# ============================================================

# Setup
source(here::here("R", "00_setup.R"))

# --- 0. Parâmetros ------------------------------------------
PROJETO <- "P01"
INPUT_DIR <- here("dados", "raw", PROJETO)
OUTPUT_DIR <- here("dados", "processed", PROJETO)
RESULTADOS_DIR <- here("resultados", PROJETO)

# Criar diretórios
for (path in c(OUTPUT_DIR, RESULTADOS_DIR)) {
  if (!dir.exists(path)) dir.create(path, recursive = TRUE)
}

log_msg(sprintf("Iniciando pipeline de AT para o projeto %s", PROJETO))

# --- 1. Carregar transcrições -------------------------------
log_msg("Etapa 1: Carregando transcrições")

# Esperado: arquivos .txt em dados/raw/P01/, um por criança
# Formato do arquivo: cabeçalho opcional + texto da transcrição
arquivos <- list.files(INPUT_DIR, pattern = "\\.txt$", full.names = TRUE)

if (length(arquivos) == 0) {
  log_msg(sprintf("⚠️  Nenhum arquivo .txt encontrado em %s", INPUT_DIR), level = "WARN")
  log_msg("Crie os arquivos de transcrição (um por criança) e rode novamente.", level = "WARN")
  # Criar exemplo para teste
  exemplo <- "Criança: Então a Khanmigo me ajuda a fazer a lição. Às vezes ela explica, às vezes eu não entendo. Quando ela erra, eu falo pra professora."
  dir.create(INPUT_DIR, recursive = TRUE, showWarnings = FALSE)
  writeLines(exemplo, file.path(INPUT_DIR, "exemplo_C01.txt"))
  log_msg("Arquivo de exemplo criado em exemplo_C01.txt para teste", level = "INFO")
  arquivos <- list.files(INPUT_DIR, pattern = "\\.txt$", full.names = TRUE)
}

# Carregar todos em um data frame
transcricoes <- tibble::tibble(
  arquivo = basename(arquivos),
  participante = tools::file_path_sans_ext(basename(arquivos)),
  texto = sapply(arquivos, readLines, warn = FALSE, USE.NAMES = FALSE) %>% paste(collapse = " ")
)

log_msg(sprintf("Carregadas %d transcrições", nrow(transcricoes)))

# --- 2. Pré-processamento -----------------------------------
log_msg("Etapa 2: Pré-processamento de texto")

# Função de limpeza
limpar_texto <- function(texto) {
  texto |>
    stringr::str_to_lower() |>
    stringr::str_replace_all("[áàãâä]", "a") |>
    stringr::str_replace_all("[éèêë]", "e") |>
    stringr::str_replace_all("[íìîï]", "i") |>
    stringr::str_replace_all("[óòõôö]", "o") |>
    stringr::str_replace_all("[úùûü]", "u") |>
    stringr::str_replace_all("[ç]", "c") |>
    stringr::str_replace_all("[[:punct:]]", " ") |>
    stringr::str_replace_all("[[:digit:]]", " ") |>
    stringr::str_replace_all("\\s+", " ") |>
    stringr::str_trim()
}

transcricoes <- transcricoes |>
  dplyr::mutate(texto_limpo = limpar_texto(texto))

log_msg("Pré-processamento concluído")

# --- 3. Tokenização ----------------------------------------
log_msg("Etapa 3: Tokenização")

# Quebrar em palavras (tokens)
tokens <- transcricoes |>
  tidytext::unnest_tokens(palavra, texto_limpo) |>
  dplyr::anti_join(tidytext::stop_words, by = "palabra")

# Custom stop words em português (você pode expandir)
stop_words_pt <- tibble::palabra = c(
  "é", "foi", "sao", "as", "os", "um", "uma", "de", "do", "da",
  "em", "no", "na", "para", "pra", "com", "que", "se", "nao",
  "mais", "menos", "muito", "pouco", "ai", "aí", "entao", "então",
  "tipo", "assim", "aqui", "ali", "la", "lá", "cá", "ja", "já"
)

tokens <- tokens |>
  dplyr::anti_join(stop_words_pt, by = "palavra")

log_msg(sprintf("Tokens gerados: %d (após remover stop words)", nrow(tokens)))

# --- 4. Frequência de palavras -----------------------------
log_msg("Etapa 4: Análise de frequência")

freq_palavras <- tokens |>
  dplyr::count(palavra, sort = TRUE) |>
  dplyr::mutate(
    freq_relativa = n / sum(n) * 100
  )

# Top 50 palavras
top_50 <- freq_palavras |> head(50)

# Salvar
readr::write_csv(freq_palavras,
  file.path(RESULTADOS_DIR, "01_frequencia_palavras.csv"))
readr::write_csv(top_50,
  file.path(RESULTADOS_DIR, "02_top_50_palavras.csv"))

log_msg("Frequências salvas em resultados/P01/")

# --- 5. Bigramas (pares de palavras) -----------------------
log_msg("Etapa 5: Análise de bigramas")

bigramas <- transcricoes |>
  tidytext::unnest_tokens(bigrama, texto_limpo, token = "ngrams", n = 2) |>
  tidyr::separate(bigrama, c("palavra1", "palavra2"), sep = " ") |>
  dplyr::filter(!palavra1 %in% stop_words_pt$palabra) |>
  dplyr::filter(!palavra2 %in% stop_words_pt$palabra) |>
  dplyr::count(palavra1, palavra2, sort = TRUE)

readr::write_csv(bigramas,
  file.path(RESULTADOS_DIR, "03_bigramas.csv"))

log_msg(sprintf("Bigramas gerados: %d", nrow(bigramas)))

# --- 6. TF-IDF por participante -----------------------------
log_msg("Etapa 6: TF-IDF por participante")

# Identifica palavras características de cada criança
tfidf <- tokens |>
  dplyr::count(participante, palavra) |>
  tidytext::bind_tf_idf(palavra, participante, n) |>
  dplyr::arrange(participante, dplyr::desc(tf_idf))

readr::write_csv(tfidf,
  file.path(RESULTADOS_DIR, "04_tfidf_por_participante.csv"))

log_msg("TF-IDF calculado")

# --- 7. Wordcloud ------------------------------------------
log_msg("Etapa 7: Gerando wordcloud")

if (requireNamespace("wordcloud2", quietly = TRUE) ||
    requireNamespace("wordcloud", quietly = TRUE)) {
  # PNG estático (preferível para publicação)
  png(file.path(RESULTADOS_DIR, "05_wordcloud.png"),
      width = 1200, height = 800, res = 100)
  if (requireNamespace("wordcloud", quietly = TRUE)) {
    wordcloud::wordcloud(
      words = freq_palavras$palavra,
      freq = freq_palavras$n,
      min.freq = 2,
      max.words = 100,
      random.order = FALSE,
      rot.per = 0.35,
      colors = RColorBrewer::brewer.pal(8, "Dark2")
    )
  } else {
    # Fallback: barplot das top 30 palavras
    top_30 <- freq_palavras |> head(30)
    barplot(top_30$n, names.arg = top_30$palavra, las = 2, cex.names = 0.8,
            main = "Top 30 palavras mais frequentes", ylab = "Frequência")
  }
  dev.off()
  log_msg("Wordcloud salvo em resultados/P01/05_wordcloud.png")
} else {
  log_msg("⚠️  Package 'wordcloud' não instalado. Instale com install.packages('wordcloud')", level = "WARN")
}

# --- 8. Coocorrência de termos-chave -----------------------
log_msg("Etapa 8: Coocorrência de termos-chave")

# Termos-chave definidos manualmente (ajustar conforme o tema emerge)
termos_chave <- c(
  "khanmigo", "tutor", "robô", "maquina", "ajuda", "explica",
  "confunde", "erro", "errada", "certa", "amigo", "professora",
  "escola", "lição", "tarefa", "matematica", "leitura",
  "inteligente", "burro", "confia", "acredita", "entende"
)

# Calcular frequência de cada termo-chave
freq_termos <- purrr::map_dfr(termos_chave, function(termo) {
  n_docs <- sum(stringr::str_detect(transcricoes$texto_limpo,
                                     stringr::regex(termo, ignore_case = TRUE)))
  tibble::tibble(
    termo = termo,
    n_participantes = n_docs,
    pct_participantes = n_docs / nrow(transcricoes) * 100
  )
}) |>
  dplyr::arrange(dplyr::desc(n_participantes))

readr::write_csv(freq_termos,
  file.path(RESULTADOS_DIR, "06_freq_termos_chave.csv"))

log_msg("Coocorrência calculada")

# --- 9. Codebook inicial (sugestões para Taguette) --------
log_msg("Etapa 9: Gerando codebook inicial")

# Sugestões de códigos baseados em análise exploratória
codebook_inicial <- tibble::tibble(
  codigo = c(
    "metacognicao_explicita",
    "metacognicao_implicita",
    "confianca_alta",
    "confianca_baixa",
    "deteccao_erro",
    "comparacao_humano",
    "comparacao_professor",
    "atribuicao_inteligencia",
    "atribuicao_amizade",
    "uso_estrategico",
    "uso_emocional",
    "resistencia",
    "curiosidade"
  ),
  descricao = c(
    "Criança verbaliza explicitamente seu pensamento (ex: 'eu acho que...', 'eu pensei...')",
    "Indícios implícitos de monitoramento cognitivo (pausas, correções)",
    "Criança expressa alta confiança no tutor (ex: 'sempre acerta', 'confio')",
    "Criança expressa baixa confiança (ex: 'às vezes erra', 'não sei se posso confiar')",
    "Criança identifica e reage a erros do tutor",
    "Criança compara tutor com humano (geral, não específico)",
    "Criança compara tutor com professora ou pais",
    "Criança atribui inteligência ao tutor",
    "Criança atribui qualidades de amizade/sociais ao tutor",
    "Criança usa o tutor de forma instrumental/estratégica",
    "Criança usa o tutor para suporte emocional/afetivo",
    "Criança resiste ou se opõe ao uso do tutor",
    "Criança demonstra curiosidade e exploração ativa"
  ),
  exemplo = c(
    "\"Eu pensei que talvez...\"",
    "(pausa longa antes de responder)",
    "\"Ela sempre sabe o que fazer\"",
    "\"Às vezes ela erra, não sei\"",
    "\"Ela errou! Vou falar pra professora\"",
    "\"É como uma pessoa que sabe tudo\"",
    "\"Diferente da professora porque...\"",
    "\"Ela é inteligente\"",
    "\"Ela é minha amiga\"",
    "\"Uso quando não sei\"",
    "\"Quando tô triste, pergunto pra ela\"",
    "\"Não gosto de usar\"",
    "\"Quero aprender mais coisas\""
  ),
  frequencia_sugerida = NA_integer_,
  notas = ""
)

# Calcular frequência sugerida baseada nos termos-chave
for (i in 1:nrow(codebook_inicial)) {
  codigo <- codebook_inicial$codigo[i]
  # Heurística simples: número de participantes que mencionam termos relacionados
  termos_relacionados <- list(
    "metacognicao_explicita"     = c("pensei", "achei", "sei", "lembro"),
    "metacognicao_implicita"     = c(),
    "confianca_alta"             = c("confio", "sempre", "acredito"),
    "confianca_baixa"            = c("erro", "errada", "nao sei", "confundi"),
    "deteccao_erro"              = c("erro", "errada", "errou"),
    "comparacao_humano"          = c("pessoa", "gente", "humano"),
    "comparacao_professor"       = c("professora", "professor", "mestre"),
    "atribuicao_inteligencia"    = c("inteligente", "sabe tudo", "esperta"),
    "atribuicao_amizade"         = c("amiga", "amigo", "companhia"),
    "uso_estrategico"            = c("quando", "para", "ajuda", "uso"),
    "uso_emocional"              = c("triste", "feliz", "sente"),
    "resistencia"                = c("nao gosto", "chato", "ruim"),
    "curiosidade"                = c("quero", "mais", "aprende")
  )
  if (length(termos_relacionados[[codigo]]) > 0) {
    n_mention <- sum(sapply(transcricoes$texto_limpo, function(texto) {
      any(sapply(termos_relacionados[[codigo]], function(t) {
        stringr::str_detect(texto, stringr::regex(t, ignore_case = TRUE))
      }))
    }))
    codebook_inicial$frequencia_sugerida[i] <- n_mention
  }
}

readr::write_csv(codebook_inicial,
  file.path(RESULTADOS_DIR, "07_codebook_inicial.csv"))

log_msg("Codebook inicial salvo")

# --- 10. Estatísticas resumidas ----------------------------
log_msg("Etapa 10: Estatísticas resumidas")

estatisticas <- tibble::tibble(
  metrica = c(
    "n_participantes",
    "n_palavras_total",
    "n_palavras_unicas",
    "media_palavras_por_participante",
    "termo_mais_frequente",
    "freq_termo_mais_frequente"
  ),
  valor = c(
    nrow(transcricoes),
    nrow(tokens),
    nrow(freq_palavras),
    round(nrow(tokens) / nrow(transcricoes), 0),
    freq_palavras$palavra[1],
    freq_palavras$n[1]
  )
)

readr::write_csv(estatisticas,
  file.path(RESULTADOS_DIR, "08_estatisticas_resumidas.csv"))

log_msg("Estatísticas salvas")
print(estatisticas)

# --- 11. Relatório final -----------------------------------
log_msg("Etapa 11: Gerando relatório")

relatorio <- paste0(
  "===========================================\n",
  "  RELATÓRIO - Análise Temática (P01)\n",
  "  Gerado em: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n",
  "===========================================\n\n",
  "PARTICIPANTES: ", nrow(transcricoes), "\n",
  "PALAVRAS TOTAIS: ", nrow(tokens), "\n",
  "VOCABULÁRIO ÚNICO: ", nrow(freq_palavras), "\n",
  "MÉDIA DE PALAVRAS/PARTICIPANTE: ",
  round(nrow(tokens) / nrow(transcricoes), 0), "\n\n",
  "TOP 10 PALAVRAS:\n"
)

for (i in 1:min(10, nrow(freq_palavras))) {
  relatorio <- paste0(relatorio,
    sprintf("  %d. %s (%d ocorrências)\n", i,
            freq_palavras$palavra[i], freq_palavras$n[i]))
}

relatorio <- paste0(relatorio, "\n",
  "ARQUIVOS GERADOS:\n",
  "  - 01_frequencia_palavras.csv\n",
  "  - 02_top_50_palavras.csv\n",
  "  - 03_bigramas.csv\n",
  "  - 04_tfidf_por_participante.csv\n",
  "  - 05_wordcloud.png\n",
  "  - 06_freq_termos_chave.csv\n",
  "  - 07_codebook_inicial.csv\n",
  "  - 08_estatisticas_resumidas.csv\n",
  "  - relatorio.txt (este arquivo)\n\n",
  "PRÓXIMOS PASSOS:\n",
  "  1. Importar 07_codebook_inicial.csv no Taguette\n",
  "  2. Codificar manualmente as transcrições (refinar códigos)\n",
  "  3. Voltar para R para análise final após codificação\n"
)

writeLines(relatorio, file.path(RESULTADOS_DIR, "relatorio.txt"))
log_msg("Relatório salvo em resultados/P01/relatorio.txt")

# ============================================================
# Fim do pipeline
#
# Outputs:
# - dados/processed/P01/ : (vazio por enquanto, dados brutos ficam em raw)
# - resultados/P01/ : 8 arquivos CSV + 1 PNG + 1 TXT
#
# Próximo: usar Taguette para codificação manual com o codebook,
# depois rodar a parte qualitativa com mais profundidade.
# ============================================================

log_msg("Pipeline de AT concluído com sucesso", level = "SUCCESS")
