=============================
Análise em R — Introdução
=============================

Pipeline R do programa.

Setup
=====

Instalação dos pacotes:

.. code-block:: r

   install.packages(c(
     "tidyverse", "tidytext", "lavaan", "emmeans",
     "afex", "psych", "OpenMx", "tidySEM", "here"
   ))

Estrutura
=========

.. code-block:: text

   analise/R/
   ├── R/                       # Package source
   │   ├── utils.R
   │   ├── at_pipeline.R
   │   ├── ancova.R
   │   ├── sem.R
   │   └── lgcm.R
   ├── notebooks/               # R Markdown
   │   ├── 01_at_exploratory.Rmd
   │   ├── 02_ancova_report.Rmd
   │   ├── 03_lgcm_visualization.Rmd
   │   └── 04_sem_visualization.Rmd
   ├── tests/                   # testthat
   │   └── testthat/
   │       └── test-utils.R
   ├── DESCRIPTION
   └── NAMESPACE

Funções principais
==================

- ``at_pipeline()`` — Análise Temática (P01)
- ``ancova_p02()`` — ANCOVA 2x4 (P02)
- ``sem_p04()`` — SEM com mediação (P04)
- ``lgcm_p05()`` — LGCM longitudinal (P05)

Como usar
=========

.. code-block:: r

   # Carregar package
   devtools::load_all("analise/R")

   # Rodar Análise Temática
   at_pipeline(
     input_dir = "dados/raw/P01",
     output_dir = "resultados/P01"
   )

   # Rodar ANCOVA
   ancova_p02(
     input_file = "dados/processed/P02/p02_clean.csv",
     output_dir = "resultados/P02"
   )
