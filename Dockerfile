# ============================================================
# Dockerfile — Programa de Pesquisa em Neurociência Educacional
# Imagem reproduzível com R + Python + MNE
# ============================================================

# Stage 1: Base com R + Python
FROM rocker/tidyverse:4.4.1 AS base

LABEL maintainer="Programa de Pesquisa em Neurociência Educacional <pesquisa@neurociencia.edu>"
LABEL description="Ambiente reproduzível: R 4.4 + Python 3.11 + MNE-Python 1.5"
LABEL version="1.0"

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# --- 1. Instalar Python 3.11 + dependências do sistema -------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    git \
    curl \
    wget \
    make \
    graphviz \
    # Para MNE
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libsm6 \
    libxext6 \
    # Para R compilation
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libxt-dev \
    # Limpar cache
    && rm -rf /var/lib/apt/lists/*

# --- 2. Configurar Python -------------------------------------------
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    python3 -m pip install --upgrade pip setuptools wheel

# --- 3. Instalar pacotes Python -------------------------------------
COPY analise/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# --- 4. Instalar pacotes R ------------------------------------------
RUN R -e "install.packages(c('renv', 'remotes', 'testthat', 'lintr', 'pkgdown', 'usethis'))"

# --- 5. Copiar código do projeto ------------------------------------
WORKDIR /workspace
COPY . /workspace

# --- 6. Instalar pacotes R do projeto (com renv) --------------------
# Se houver renv.lock, restaurar; senão, instalar manualmente
RUN if [ -f analise/renv.lock ]; then \
        R -e "renv::restore()"; \
    else \
        R -e "install.packages(c('tidyverse', 'tidytext', 'quanteda', 'readxl', 'janitor', 'patchwork', 'wordcloud', 'lavaan', 'semTools', 'semPlot', 'psych', 'afex', 'emmeans', 'effectsize', 'car', 'multcomp', 'broom', 'flextable', 'OpenMx', 'tidySEM'))"; \
    fi

# --- 7. Setup inicial -----------------------------------------------
RUN R -e "renv::init(bare = TRUE)" || true
RUN python3 analise/Python/00_setup.py

# --- 8. Verificar instalação -----------------------------------------
RUN echo "=== Verificando instalação ===" && \
    R --version | head -1 && \
    python3 --version && \
    R -e "cat('R packages:', length(rownames(installed.packages())), '\n')" && \
    python3 -c "import mne; print('MNE:', mne.__version__)" && \
    echo "✅ Instalação verificada"

# --- 9. Comando padrão -----------------------------------------------
CMD ["bash"]
