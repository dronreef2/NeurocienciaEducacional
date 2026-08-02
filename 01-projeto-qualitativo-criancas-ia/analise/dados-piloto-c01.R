# ============================================================
# analise/dados-piloto-c01.R
# Análise piloto com transcrição fictícia (P01)
# Demonstra o pipeline de AT funcionando
# ============================================================

source(here::here("R", "R", "at_pipeline.R"))

# Diretório de saída
output_dir <- here::here("resultados", "P01_piloto")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Dados piloto (1 criança, 1 entrevista simulada)
input_dir <- file.path(output_dir, "transcricoes_piloto")
dir.create(input_dir, recursive = TRUE, showWarnings = FALSE)

entrevista_piloto <- "
Entrevistador: E aí, [nome inventado], como foi usar o Khanmigo essa semana?
Criança: Ah, foi legal! Ela me ajudou a fazer a lição de matemática.
Entrevistador: E o que você achou dela?
Criança: Ela é inteligente, mas às vezes demora pra responder. Eu prefiro a professora às vezes porque a professora entende melhor.
Entrevistador: Entende melhor o quê?
Criança: Quando eu não sei, eu falo pra ela e ela sabe o que eu tô pensando. O Khanmigo faz perguntas difíceis.
Entrevistador: Que tipo de perguntas?
Criança: Tipo, ele pergunta 'o que você acha?' e eu não sei. Mas também já vi ele errar uma vez.
Entrevistador: Errar? Como assim?
Criança: Ele falou que 2 mais 2 era 5. Eu falei: tá errado! Aí eu contei nos dedos e mostrei pra ele.
Entrevistador: E o que você sentiu quando ele errou?
Criança: Achei engraçado, porque ele é grande e sabe tudo, mas errou. Falei pra minha mãe e ela riu também.
Entrevistador: Você confia nele?
Criança: Confio um pouco. Pra somar eu uso, mas pra ler eu prefiro minha avó.
Entrevistador: Por quê?
Criança: Porque minha avó conta histórias. O Khanmigo só explica.
Entrevistador: Você acha que ele é seu amigo?
Criança: Ele é legal, mas amigo é o Pedro da escola.
"

# Salvar
writeLines(entrevista_piloto, file.path(input_dir, "C01_piloto.txt"))

# Rodar análise
at_pipeline(
  input_dir = input_dir,
  output_dir = output_dir,
  gerar_wordcloud = TRUE
)

cat("\n✅ Análise piloto concluída!\n")
cat("Resultados em:", output_dir, "\n")
