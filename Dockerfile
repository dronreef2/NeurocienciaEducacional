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
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    curl \
    make \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libsm6 \
    libxext6 \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# --- 2. Instalar pacotes Python -------------------------------------
COPY analise/requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# --- 3. Instalar pacotes R ------------------------------------------
RUN R -e "options(repos=c(CRAN='https://cran.r-project.org'))" \
       -e "install.packages(c('tidyverse', 'tidytext', 'lavaan', 'emmeans'))"

# --- 4. Copiar código do projeto ------------------------------------
WORKDIR /workspace
COPY . /workspace

# --- 5. Verificar instalação -----------------------------------------
RUN echo "=== Verificando instalação ===" && \
    R --version | head -1 && \
    python3 --version && \
    python3 -c "import mne; print('MNE:', mne.__version__)" && \
    echo "OK Instalacao verificada"

# --- 6. Comando padrão -----------------------------------------------
CMD ["bash"]
