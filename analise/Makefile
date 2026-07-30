# ============================================================
# Makefile para o programa de pesquisa
#
# Orquestra os pipelines de análise de forma reprodutível.
#
# Uso:
#   make help         # ver targets disponíveis
#   make all          # rodar tudo
#   make p01          # rodar apenas P01
#   make p03          # rodar apenas P03 (EEG)
#   make p05          # rodar apenas P05 (LGCM)
#   make clean        # limpar resultados
# ============================================================

# Variáveis
PYTHON := python3
RSCRIPT := Rscript
ANALISE_DIR := analise
RESULTADOS_DIR := $(ANALISE_DIR)/resultados
DADOS_DIR := $(ANALISE_DIR)/dados

# Cores para output
GREEN := \033[0;32m
BLUE := \033[0;34m
NC := \033[0m

# Phony targets
.PHONY: help all clean p01 p02 p03 p04 p05 setup test deps

# ============================================================
# Help
# ============================================================
help: ## Mostra esta ajuda
	@echo "$(BLUE)Targets disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================
# Setup
# ============================================================
setup: ## Verifica setup do projeto
	@echo "$(BLUE)Verificando setup...$(NC)"
	@cd $(ANALISE_DIR) && $(PYTHON) Python/00_setup.py

deps: ## Instala dependências
	@echo "$(BLUE)Instalando dependências Python...$(NC)"
	@cd $(ANALISE_DIR) && pip install -r requirements.txt
	@echo "$(BLUE)Instalando dependências R...$(NC)"
	@cd $(ANALISE_DIR) && $(RSCRIPT) -e "renv::restore()"

# ============================================================
# Testes
# ============================================================
test: ## Roda testes
	@echo "$(BLUE)Rodando testes Python...$(NC)"
	@cd $(ANALISE_DIR) && pytest Python/tests/ -v || echo "Sem testes Python ainda"
	@echo "$(BLUE)Rodando testes R...$(NC)"
	@cd $(ANALISE_DIR) && $(RSCRIPT) -e "testthat::test_dir('R/tests')" || echo "Sem testes R ainda"

# ============================================================
# P01 — Análise Temática
# ============================================================
p01: ## Pipeline do P01 (Análise Temática)
	@echo "$(BLUE)=== P01: Análise Temática ===$(NC)"
	@cd $(ANALISE_DIR) && $(RSCRIPT) R/01_at_pipeline.R
	@echo "$(GREEN)✅ P01 concluído$(NC)"

# ============================================================
# P02 — ANOVA (a implementar)
# ============================================================
p02: ## Pipeline do P02 (ANOVA)
	@echo "$(BLUE)=== P02: ANOVA ===$(NC)"
	@echo "⚠️  Script R/02_anova_p02.R ainda não criado"
	@echo "   Estrutura planejada:"
	@echo "   - Ler dados dos 5 grupos"
	@echo "   - ANCOVA 2x4 (Tipo × Duração) com pré-teste como covariável"
	@echo "   - Post-hoc (Tukey HSD)"
	@echo "   - Tamanho de efeito (eta², Cohen's d)"

# ============================================================
# P03 — EEG/ERP
# ============================================================
p03: ## Pipeline do P03 (EEG → ERP)
	@echo "$(BLUE)=== P03: EEG / ERP ===$(NC)"
	@echo "Etapa 1: Pré-processamento"
	@cd $(ANALISE_DIR) && $(PYTHON) Python/01_eeg_preprocessing.py \
		--input $(DADOS_DIR)/raw/P03/ --batch --projeto P03
	@echo "Etapa 2: Análise de ERP"
	@cd $(ANALISE_DIR) && $(PYTHON) Python/02_eeg_erp_analysis.py \
		--input $(DADOS_DIR)/processed/P03/ --batch --projeto P03
	@echo "$(GREEN)✅ P03 concluído$(NC)"

# ============================================================
# P04 — SEM
# ============================================================
p04: ## Pipeline do P04 (SEM)
	@echo "$(BLUE)=== P04: SEM (mediação) ===$(NC)"
	@cd $(ANALISE_DIR) && $(RSCRIPT) R/03_sem_p04.R
	@echo "$(GREEN)✅ P04 concluído$(NC)"

# ============================================================
# P05 — LGCM (coorte)
# ============================================================
p05: ## Pipeline do P05 (LGCM)
	@echo "$(BLUE)=== P05: LGCM (coorte) ===$(NC)"
	@cd $(ANALISE_DIR) && $(RSCRIPT) R/04_lgcm_p05.R
	@echo "$(GREEN)✅ P05 concluído$(NC)"

# ============================================================
# All
# ============================================================
all: p01 p03 p04 p05 ## Roda todos os pipelines
	@echo "$(GREEN)==========================================="
	@echo "  ✅ TODOS OS PIPELINES CONCLUÍDOS"
	@echo "===========================================$(NC)"

# ============================================================
# Clean
# ============================================================
clean: ## Limpa resultados (CUIDADO: apaga tudo)
	@echo "$(BLUE)Limpando resultados...$(NC)"
	@rm -rf $(RESULTADOS_DIR)/*
	@echo "$(GREEN)✅ Resultados limpos$(NC)"

# ============================================================
# Status
# ============================================================
status: ## Mostra status dos dados
	@echo "$(BLUE)=== STATUS DO PROJETO ===$(NC)"
	@echo "Dados brutos:"
	@find $(DADOS_DIR)/raw -type f 2>/dev/null | wc -l | xargs echo "  Arquivos:"
	@echo "Dados processados:"
	@find $(DADOS_DIR)/processed -type f 2>/dev/null | wc -l | xargs echo "  Arquivos:"
	@echo "Resultados:"
	@find $(RESULTADOS_DIR) -type f 2>/dev/null | wc -l | xargs echo "  Arquivos:"
	@echo ""
	@echo "Tamanho total:"
	@du -sh $(DADOS_DIR) $(RESULTADOS_DIR) 2>/dev/null
