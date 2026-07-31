# ============================================================
# dashboard/app.R
# Shiny Dashboard - Programa de Pesquisa em Neurociencia Educacional
#
# Como rodar:
#   R -e "shiny::runApp('analise/R/dashboard/')"
# Ou deploy:
#   R -e "rsconnect::deployApp('analise/R/dashboard/')"
# ============================================================

library(shiny)
library(shinydashboard)
library(ggplot2)
library(dplyr)
library(readr)
library(DT)

# Paths
PROJETO_ROOT <- here::here()
RESULTADOS_DIR <- file.path(PROJETO_ROOT, "resultados")

# UI
ui <- dashboardPage(
  skin = "blue",

  dashboardHeader(title = "Neurociencia Educacional"),

  dashboardSidebar(
    sidebarMenu(
      menuItem("Visao geral", tabName = "overview", icon = icon("home")),
      menuItem("P01 - AT", tabName = "p01", icon = icon("comments")),
      menuItem("P02 - ANCOVA", tabName = "p02", icon = icon("calculator")),
      menuItem("P03 - EEG/ERP", tabName = "p03", icon = icon("brain")),
      menuItem("P04 - SEM", tabName = "p04", icon = icon("project-diagram")),
      menuItem("P05 - LGCM", tabName = "p05", icon = icon("chart-line"))
    )
  ),

  dashboardBody(
    tabItems(
      # ===================================================
      # Visao geral
      # ===================================================
      tabItem(tabName = "overview",
        h2("Visao Geral do Programa"),

        fluidRow(
          valueBoxOutput("box_p01"),
          valueBoxOutput("box_p02"),
          valueBoxOutput("box_p03"),
          valueBoxOutput("box_p04"),
          valueBoxOutput("box_p05")
        ),

        fluidRow(
          box(title = "Status dos Resultados", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("tabela_resultados")
          )
        )
      ),

      # ===================================================
      # P01
      # ===================================================
      tabItem(tabName = "p01",
        h2("P01 - Analise Temetica (Khanmigo)"),

        fluidRow(
          box(title = "Codebook Inicial", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("codebook_p01")
          )
        ),

        fluidRow(
          box(title = "Frequencia dos Codigos", status = "info", solidHeader = TRUE,
              width = 12,
              plotOutput("plot_codebook_p01", height = 400)
          )
        )
      ),

      # ===================================================
      # P02
      # ===================================================
      tabItem(tabName = "p02",
        h2("P02 - ANCOVA (Gamificacao)"),

        fluidRow(
          box(title = "Tabela de Resultados", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("tabela_p02")
          )
        ),

        fluidRow(
          box(title = "Cohen's d (vs CTRL)", status = "info", solidHeader = TRUE,
              width = 12,
              plotOutput("plot_cohens_p02", height = 400)
          )
        )
      ),

      # ===================================================
      # P03
      # ===================================================
      tabItem(tabName = "p03",
        h2("P03 - EEG / ERP (Bandeira)"),

        fluidRow(
          box(title = "Metricas dos Componentes", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("metricas_p03")
          )
        ),

        fluidRow(
          box(title = "Imagem ERP N170", status = "info", solidHeader = TRUE,
              width = 12,
              imageOutput("img_erp_p03")
          )
        )
      ),

      # ===================================================
      # P04
      # ===================================================
      tabItem(tabName = "p04",
        h2("P04 - SEM (IA Generativa x FE)"),

        fluidRow(
          box(title = "Parametros do SEM", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("params_p04")
          )
        ),

        fluidRow(
          box(title = "Diagrama do Modelo", status = "info", solidHeader = TRUE,
              width = 12,
              imageOutput("img_sem_p04")
          )
        )
      ),

      # ===================================================
      # P05
      # ===================================================
      tabItem(tabName = "p05",
        h2("P05 - LGCM (Coorte Longitudinal)"),

        fluidRow(
          box(title = "Comparacao de Modelos", status = "primary", solidHeader = TRUE,
              width = 12,
              DTOutput("comp_p05")
          )
        ),

        fluidRow(
          box(title = "Trajetorias Preditas", status = "info", solidHeader = TRUE,
              width = 12,
              imageOutput("img_lgcm_p05")
          )
        )
      )
    )
  )
)

# Server
server <- function(input, output, session) {

  # Carregar dados com caching
  carregar_arquivo <- function(path) {
    if (file.exists(path)) {
      tryCatch(read_csv(path, show_col_types = FALSE),
               error = function(e) NULL)
    } else {
      NULL
    }
  }

  # P01
  codebook_p01_data <- reactive({
    carregar_arquivo(file.path(RESULTADOS_DIR, "P01", "07_codebook_inicial.csv"))
  })

  output$codebook_p01 <- renderDT({
    df <- codebook_p01_data()
    if (is.null(df)) {
      data.frame(Mensagem = "Resultados do P01 nao encontrados")
    } else {
      df
    }
  })

  output$plot_codebook_p01 <- renderPlot({
    df <- codebook_p01_data()
    if (is.null(df) || !"frequencia_sugerida" %in% names(df)) {
      ggplot() + annotate("text", x = 0, y = 0, label = "Sem dados") + theme_void()
    } else {
      df |>
        arrange(frequencia_sugerida) |>
        ggplot(aes(x = reorder(codigo, frequencia_sugerida),
                   y = frequencia_sugerida)) +
        geom_col(fill = "#1f77b4") +
        coord_flip() +
        labs(x = NULL, y = "Frequencia",
             title = "Frequencia dos codigos (sugerida)") +
        theme_minimal()
    }
  })

  # P02
  output$tabela_p02 <- renderDT({
    carregar_arquivo(file.path(RESULTADOS_DIR, "P02", "13_tabela_resultados.csv")) |>
      (\(.) if (is.null(.)) data.frame(Mensagem = "Resultados do P02 nao encontrados") else .)()
  })

  output$plot_cohens_p02 <- renderPlot({
    df <- carregar_arquivo(file.path(RESULTADOS_DIR, "P02", "08_cohens_d_stroop.csv"))
    if (is.null(df)) {
      ggplot() + annotate("text", x = 0, y = 0, label = "Sem dados") + theme_void()
    } else {
      ggplot(df, aes(x = comparacao, y = d)) +
        geom_col(fill = "#ff7f0e") +
        labs(x = NULL, y = "Cohen's d",
             title = "Tamanho de efeito (Cohen's d) vs CTRL") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
    }
  })

  # P03
  output$metricas_p03 <- renderDT({
    carregar_arquivo(file.path(RESULTADOS_DIR, "P03", "00_metricas_componentes.csv")) |>
      (\(.) if (is.null(.)) data.frame(Mensagem = "Resultados do P03 nao encontrados") else .)()
  })

  output$img_erp_p03 <- renderImage({
    list(
      src = file.path(RESULTADOS_DIR, "P03", "02_erp_N170.png"),
      contentType = "image/png",
      width = "100%"
    )
  }, deleteFile = FALSE)

  # P04
  output$params_p04 <- renderDT({
    carregar_arquivo(file.path(RESULTADOS_DIR, "P04", "03_parametros_sem.csv")) |>
      (\(.) if (is.null(.)) data.frame(Mensagem = "Resultados do P04 nao encontrados") else .)()
  })

  output$img_sem_p04 <- renderImage({
    list(
      src = file.path(RESULTADOS_DIR, "P04", "05_modelo_sem.png"),
      contentType = "image/png",
      width = "100%"
    )
  }, deleteFile = FALSE)

  # P05
  output$comp_p05 <- renderDT({
    carregar_arquivo(file.path(RESULTADOS_DIR, "P05", "03_comparacao_modelos.csv")) |>
      (\(.) if (is.null(.)) data.frame(Mensagem = "Resultados do P05 nao encontrados") else .)()
  })

  output$img_lgcm_p05 <- renderImage({
    list(
      src = file.path(RESULTADOS_DIR, "P05", "05_trajetorias_preditas.png"),
      contentType = "image/png",
      width = "100%"
    )
  }, deleteFile = FALSE)

  # Boxes
  output$box_p01 <- renderValueBox({
    valueBox("Em andamento", "P01 - AT", icon = icon("comments"), color = "green")
  })
  output$box_p02 <- renderValueBox({
    valueBox("Em andamento", "P02 - ANCOVA", icon = icon("calculator"), color = "yellow")
  })
  output$box_p03 <- renderValueBox({
    valueBox("Setup", "P03 - EEG", icon = icon("brain"), color = "orange")
  })
  output$box_p04 <- renderValueBox({
    valueBox("Em andamento", "P04 - SEM", icon = icon("project-diagram"), color = "orange")
  })
  output$box_p05 <- renderValueBox({
    valueBox("Planejado", "P05 - LGCM", icon = icon("chart-line"), color = "red")
  })
}

# Run
shinyApp(ui = ui, server = server)
