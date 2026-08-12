# Makefile para o Programa de Pesquisa em Neurociência Educacional
# Comandos comuns de desenvolvimento, análise e deploy
#
# Uso: make help

# ============================================================
# Variáveis
# ============================================================
PYTHON ?= python3
PIP ?= pip
NOTEBOOKS_DIR := analise/Python/notebooks
SCRIPTS_DIR := analise/Python/scripts
RESULTS_DIR := resultados
PYPROJECT := analise/Python/pyproject.toml

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

# ============================================================
# Help
# ============================================================
.PHONY: help
help: ## Mostrar este help
	@echo "$(GREEN)Programa de Pesquisa em Neurociência Educacional$(NC)"
	@echo ""
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "Exemplos:"
	@echo "  make install         # Instalar dependências"
	@echo "  make test            # Rodar testes"
	@echo "  make validate        # Validar dados"
	@echo "  make analyze-pilot   # Análise do piloto"
	@echo "  make all             # Tudo"

# ============================================================
# Instalação
# ============================================================
.PHONY: install
install: ## Instalar dependências Python
	@echo "$(YELLOW)Instalando dependências...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install -q pytest pandas numpy matplotlib scipy statsmodels networkx scikit-learn
	@echo "$(GREEN)✓ Dependências instaladas$(NC)"

.PHONY: install-dev
install-dev: ## Instalar com dependências de desenvolvimento
	$(PIP) install -r requirements.txt
	$(PIP) install -q pytest pytest-cov ruff mypy pre-commit jupyter nbformat

.PHONY: install-extras
install-extras: ## Instalar extras (EEG, Bayesian, Dashboard)
	$(PIP) install -q mne pymc streamlit plotly lifelines

# ============================================================
# Dados
# ============================================================
.PHONY: synthetic-data
synthetic-data: ## Gerar dados sintéticos para todos os 5 projetos
	@echo "$(YELLOW)Gerando dados sintéticos...$(NC)"
	$(PYTHON) $(SCRIPTS_DIR)/gerar_dados_sinteticos.py
	@echo "$(GREEN)✓ Dados em dados_sinteticos/$(NC)"

.PHONY: validate
validate: ## Validar dados do piloto
	@echo "$(YELLOW)Validando dados...$(NC)"
	$(PYTHON) $(SCRIPTS_DIR)/validar_dados_piloto.py

.PHONY: ingest
ingest: ## Ingerir dados (com anonimização)
	@echo "$(YELLOW)Para usar:$(NC)"
	@echo "  $(PYTHON) $(SCRIPTS_DIR)/ingest_data.py --input <dir> --output <dir> --type <transcripts|diary|questionnaire> --anonymize"

# ============================================================
# Análise
# ============================================================
.PHONY: analyze-pilot
analyze-pilot: ## Análise estatística do piloto
	@echo "$(YELLOW)Analisando piloto P01...$(NC)"
	$(PYTHON) $(SCRIPTS_DIR)/analise_piloto_real.py

.PHONY: mixed-models
mixed-models: ## Mixed models nos diários
	$(PYTHON) $(SCRIPTS_DIR)/mixed_models_diarios.py

.PHONY: sentiment
sentiment: ## Análise de sentimento + rede
	$(PYTHON) $(SCRIPTS_DIR)/sentiment_network_analysis.py

.PHONY: osf-dry
osf-dry: ## Simular submissão OSF (dry-run)
	@echo "$(YELLOW)Dry-run OSF submission:$(NC)"
	OSF_TOKEN=dummy $(PYTHON) $(SCRIPTS_DIR)/osf_submit.py --all --dry-run

.PHONY: osf-submit
osf-submit: ## Submeter pré-registros ao OSF (requer OSF_TOKEN)
	@echo "$(YELLOW)Submetendo ao OSF...$(NC)"
	@echo "Configure OSF_TOKEN antes: export OSF_TOKEN=..."
	$(PYTHON) $(SCRIPTS_DIR)/osf_submit.py --all

# ============================================================
# Notebooks
# ============================================================
.PHONY: list-notebooks
list-notebooks: ## Listar notebooks disponíveis
	@echo "$(GREEN)Notebooks disponíveis:$(NC)"
	@ls -1 $(NOTEBOOKS_DIR)/*.py | xargs -n1 basename

.PHONY: run-notebook
run-notebook: ## Rodar notebook (uso: make run-notebook N=05)
	@echo "$(YELLOW)Rodando notebook $(N)...$(NC)"
	$(PYTHON) $(NOTEBOOKS_DIR)/$(N)_*.py

.PHONY: convert-notebooks
convert-notebooks: ## Converter todos os .py para .ipynb
	$(PYTHON) $(SCRIPTS_DIR)/py2ipynb.py

# ============================================================
# Testes
# ============================================================
.PHONY: test
test: ## Rodar todos os testes
	@echo "$(YELLOW)Rodando testes...$(NC)"
	cd analise/Python && $(PYTHON) -m pytest tests/ -v --tb=short

.PHONY: test-quick
test-quick: ## Testes rápidos (sem verbose)
	cd analise/Python && $(PYTHON) -m pytest tests/ -q 2>&1 | tail -10

.PHONY: test-coverage
test-coverage: ## Testes com cobertura
	cd analise/Python && $(PYTHON) -m pytest tests/ --cov=neurociencia_edu --cov-report=term-missing

# ============================================================
# Qualidade de código
# ============================================================
.PHONY: lint
lint: ## Rodar linter (ruff)
	@echo "$(YELLOW)Verificando lint...$(NC)"
	cd analise/Python && $(PYTHON) -m ruff check neurociencia_edu/ scripts/ notebooks/ || true

.PHONY: format
format: ## Formatar código com ruff
	cd analise/Python && $(PYTHON) -m ruff format neurociencia_edu/ scripts/ notebooks/

.PHONY: pre-commit
pre-commit: ## Rodar pre-commit hooks
	@echo "$(YELLOW)Pre-commit hooks...$(NC)"
	pre-commit run --all-files || true

# ============================================================
# Dashboard
# ============================================================
.PHONY: dashboard
dashboard: ## Rodar dashboard Streamlit localmente
	@echo "$(GREEN)Abrindo dashboard em http://localhost:8501$(NC)"
	streamlit run streamlit_app.py

.PHONY: dashboard-docker
dashboard-docker: ## Rodar dashboard em Docker
	docker build -f Dockerfile.dashboard -t neurociencia-dashboard .
	docker run -p 8501:8501 neurociencia-dashboard

# ============================================================
# Pacote Python
# ============================================================
.PHONY: build
build: ## Build do pacote Python
	@echo "$(YELLOW)Building package...$(NC)"
	cd analise/Python && poetry build
	@echo "$(GREEN)✓ Pacote em analise/Python/dist/$(NC)"

.PHONY: publish-test
publish-test: ## Publicar em TestPyPI
	cd analise/Python && poetry publish -r testpypi

.PHONY: publish
publish: ## Publicar em PyPI (PRODUÇÃO!)
	@echo "$(RED)ATENÇÃO: vai publicar no PyPI real!$(NC)"
	@read -p "Tem certeza? [y/N] " r && [ "$$r" = "y" ]
	cd analise/Python && poetry publish

# ============================================================
# Git
# ============================================================
.PHONY: status
status: ## Status do git
	git status

.PHONY: log
log: ## Log resumido
	git log --oneline -20

.PHONY: tag-release
tag-release: ## Criar tag v1.0.0 e push
	@echo "$(YELLOW)Criando tag v1.0.0...$(NC)"
	git tag -a v1.0.0 -m "Release 1.0.0 - Programa completo"
	git push origin v1.0.0
	@echo "$(GREEN)✓ Tag v1.0.0 criada!$(NC)"

# ============================================================
# CI/CD
# ============================================================
.PHONY: ci
ci: test lint ## Rodar tudo que CI faz
	@echo "$(GREEN)✓ CI local passou!$(NC)"

.PHONY: ci-quick
ci-quick: test-quick lint ## CI rápido

# ============================================================
# Utilitários
# ============================================================
.PHONY: clean
clean: ## Limpar arquivos temporários
	@echo "$(YELLOW)Limpando...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Limpo$(NC)"

.PHONY: stats
stats: ## Estatísticas do projeto
	@echo "$(GREEN)Estatísticas do projeto:$(NC)"
	@echo "  Arquivos: $$(find . -type f -not -path './.git/*' -not -path '*/.venv/*' | wc -l)"
	@echo "  Tamanho: $$(du -sh . 2>/dev/null | cut -f1)"
	@echo "  Commits: $$(git log --oneline | wc -l)"
	@echo "  Notebooks: $$(ls $(NOTEBOOKS_DIR)/*.py 2>/dev/null | wc -l)"
	@echo "  Scripts: $$(ls $(SCRIPTS_DIR)/*.py 2>/dev/null | wc -l)"
	@echo "  Testes: $$(cd analise/Python && find tests -name 'test_*.py' | wc -l)"

.PHONY: all
all: install validate test lint synthetic-data analyze-pilot ## Rodar tudo (exceto publish)
	@echo "$(GREEN)✓ Tudo concluído!$(NC)"

# ============================================================
# Ajuda
# ============================================================
.DEFAULT_GOAL := help
