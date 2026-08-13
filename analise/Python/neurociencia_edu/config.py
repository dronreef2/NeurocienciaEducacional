"""
Config: Configuração centralizada do pacote neurociencia_edu.

Este módulo centraliza paths, constantes, settings e configurações usadas
em todo o pacote. Carrega valores de:
- Variáveis de ambiente (para secrets como OSF_TOKEN, PYPI_TOKEN)
- Arquivo .env (se existir)
- Defaults hardcoded (para tudo o mais)

Uso:
    >>> from neurociencia_edu.config import get_settings
    >>> settings = get_settings()
    >>> print(settings.dados_path)
    PosixPath('/workspace/01-projeto-qualitativo-criancas-ia/dados')
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ============================================================
# Paths do projeto
# ============================================================

def find_project_root() -> Path:
    """Encontra a raiz do projeto (onde está pyproject.toml).

    Returns:
        Path: diretório raiz do projeto (onde está pyproject.toml).

    Raises:
        FileNotFoundError: se não encontrar pyproject.toml.
    """
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    raise FileNotFoundError(
        "pyproject.toml não encontrado. "
        "Certifique-se de estar executando dentro do projeto."
    )


def find_workspace() -> Path:
    """Encontra o diretório workspace (raiz do monorepo).

    O workspace é o diretório que contém:
    - analise/ (com Python e R)
    - docs/
    - dados_sinteticos/
    - Makefile
    - README.md

    Returns:
        Path: diretório workspace.
    """
    pkg_root = find_project_root()
    # Se o pyproject.toml está em analise/Python/, subir dois níveis
    if pkg_root.name == "Python" and pkg_root.parent.name == "analise":
        return pkg_root.parent.parent
    # Se está na raiz, retornar ela mesma
    return pkg_root


PROJECT_ROOT: Path = find_project_root()
WORKSPACE: Path = find_workspace()


# ============================================================
# Estrutura de diretórios
# ============================================================

@dataclass(frozen=True)
class Paths:
    """Paths canônicos do projeto.

    Attributes:
        raiz: Diretório raiz do projeto.
        dados: Diretório de dados (P01 piloto).
        dados_sinteticos: Diretório de dados sintéticos.
        resultados: Diretório de resultados (figuras, JSONs).
        docs: Diretório de documentação.
        scripts: Diretório de scripts Python.
        notebooks: Diretório de notebooks.
        analise_python: Diretório de análise Python.
        analise_r: Diretório de análise R.
        osf_json: Diretório de pré-registros OSF.
        manuscritos: Diretório de manuscritos.
        recrutamento: Diretório de recrutamento.
        instrumentos: Diretório de instrumentos.
        codigo: Diretório de código-fonte.
    """

    raiz: Path = field(default_factory=lambda: PROJECT_ROOT)
    workspace: Path = field(default_factory=lambda: WORKSPACE)
    dados: Path = field(default_factory=lambda: WORKSPACE / "01-projeto-qualitativo-criancas-ia" / "dados")
    dados_sinteticos: Path = field(default_factory=lambda: WORKSPACE / "dados_sinteticos")
    resultados: Path = field(default_factory=lambda: WORKSPACE / "resultados")
    docs: Path = field(default_factory=lambda: WORKSPACE / "docs")
    scripts: Path = field(default_factory=lambda: WORKSPACE / "analise" / "Python" / "scripts")
    notebooks: Path = field(default_factory=lambda: WORKSPACE / "analise" / "Python" / "notebooks")
    analise_python: Path = field(default_factory=lambda: WORKSPACE / "analise" / "Python")
    analise_r: Path = field(default_factory=lambda: WORKSPACE / "analise" / "R")
    osf_json: Path = field(default_factory=lambda: WORKSPACE / "docs" / "osf-json")
    manuscritos: Path = field(default_factory=lambda: WORKSPACE / "docs" / "manuscritos")
    recrutamento: Path = field(default_factory=lambda: WORKSPACE / "01-projeto-qualitativo-criancas-ia" / "recrutamento")
    instrumentos: Path = field(default_factory=lambda: WORKSPACE / "01-projeto-qualitativo-criancas-ia" / "instrumentos")
    codigo: Path = field(default_factory=lambda: WORKSPACE / "analise" / "Python" / "neurociencia_edu")

    def criar_necessarios(self) -> None:
        """Cria diretórios que não existem."""
        for path in [
            self.dados_sinteticos,
            self.resultados,
            self.dados / "diarios" if self.dados.exists() else None,
        ]:
            if path is not None and not path.exists():
                path.mkdir(parents=True, exist_ok=True)

    def __post_init__(self) -> None:
        """Validação após inicialização."""
        if not self.raiz.exists():
            raise FileNotFoundError(f"Raiz não encontrada: {self.raiz}")


# ============================================================
# Constantes do programa
# ============================================================

@dataclass(frozen=True)
class Programa:
    """Constantes do programa de pesquisa.

    Attributes:
        nome: Nome do programa.
        instituicao: Instituição principal.
        orientadora: Nome da orientadora.
        pesquisador: Nome do pesquisador principal.
        email_contato: Email de contato.
        idioma_principal: Idioma padrão dos documentos.
        idiomas_suportados: Lista de idiomas suportados.
        ano_inicio: Ano de início do programa.
        ano_fim: Ano de fim do programa.
        projetos: Tupla de IDs dos projetos.
    """

    nome: str = "Programa de Pesquisa em Neurociência Educacional"
    instituicao: str = "UFRN / CERES / PPGED"
    orientadora: str = "Profa. Dra. Ângela Maria Chuvas Naschold"
    pesquisador: str = "[Seu nome]"
    email_contato: str = "neurociencia@ufrn.br"
    idioma_principal: str = "pt-BR"
    idiomas_suportados: tuple = ("pt-BR", "en", "es")
    ano_inicio: int = 2026
    ano_fim: int = 2030
    projetos: tuple = ("P01", "P02", "P03", "P04", "P05")


# ============================================================
# Parâmetros estatísticos padrão
# ============================================================

@dataclass(frozen=True)
class StatsConfig:
    """Configurações estatísticas padrão.

    Attributes:
        alpha: Nível de significância padrão.
        n_bootstrap: Número de amostras bootstrap.
        n_permutations: Número de permutações.
        random_state: Seed para reprodutibilidade.
        n_synthetic_default: N padrão em dados sintéticos.
    """

    alpha: float = 0.05
    n_bootstrap: int = 5000
    n_permutations: int = 1000
    random_state: int = 42
    n_synthetic_default: int = 100


# ============================================================
# Configuração de visualização
# ============================================================

@dataclass(frozen=True)
class VizConfig:
    """Configurações de visualização.

    Attributes:
        style: Estilo do matplotlib.
        palette: Paleta de cores padrão.
        dpi: DPI padrão para figuras.
        figsize_default: Tamanho padrão de figura.
        save_format: Formato padrão de salvamento.
    """

    style: str = "seaborn-v0_8-whitegrid"
    palette: str = "viridis"
    dpi: int = 200
    figsize_default: tuple = (12, 8)
    save_format: str = "png"


# ============================================================
# Tokens e credenciais (via env vars)
# ============================================================

@dataclass(frozen=True)
class Credentials:
    """Credenciais carregadas de variáveis de ambiente.

    Attributes:
        osf_token: Token do OSF (submissão de pré-registros).
        pypi_token: Token do PyPI.
        test_pypi_token: Token do TestPyPI.
        codecov_token: Token do Codecov.
        github_token: Token do GitHub.
    """

    osf_token: Optional[str] = field(default_factory=lambda: os.getenv("OSF_TOKEN"))
    pypi_token: Optional[str] = field(default_factory=lambda: os.getenv("PYPI_TOKEN"))
    test_pypi_token: Optional[str] = field(default_factory=lambda: os.getenv("TEST_PYPI_TOKEN"))
    codecov_token: Optional[str] = field(default_factory=lambda: os.getenv("CODECOV_TOKEN"))
    github_token: Optional[str] = field(default_factory=lambda: os.getenv("GITHUB_TOKEN"))

    def has_osf(self) -> bool:
        """Verifica se há token OSF configurado."""
        return bool(self.osf_token)

    def has_pypi(self) -> bool:
        """Verifica se há token PyPI configurado."""
        return bool(self.pypi_token)


# ============================================================
# Configuração unificada
# ============================================================

@dataclass(frozen=True)
class Settings:
    """Configuração unificada do projeto.

    Combina todas as configurações em um único objeto imutável.

    Attributes:
        paths: Paths do projeto.
        programa: Constantes do programa.
        stats: Configurações estatísticas.
        viz: Configurações de visualização.
        creds: Credenciais (via env vars).
    """

    paths: Paths = field(default_factory=Paths)
    programa: Programa = field(default_factory=Programa)
    stats: StatsConfig = field(default_factory=StatsConfig)
    viz: VizConfig = field(default_factory=VizConfig)
    creds: Credentials = field(default_factory=Credentials)

    def summary(self) -> str:
        """Retorna um resumo textual da configuração."""
        return f"""
{self.programa.nome}
{self.programa.instituicao}
Período: {self.programa.ano_inicio}-{self.programa.ano_fim}

Workspace: {self.paths.workspace}
Pacote Python: {self.paths.raiz}
Resultados: {self.paths.resultados}
Notebooks: {self.paths.notebooks}

Idioma padrão: {self.programa.idioma_principal}
Idiomas: {', '.join(self.programa.idiomas_suportados)}
Projetos: {', '.join(self.programa.projetos)}

Stats: α={self.stats.alpha}, n_bootstrap={self.stats.n_bootstrap}
Viz: style={self.viz.style}, dpi={self.viz.dpi}

Credenciais:
  OSF: {'✓' if self.creds.has_osf() else '✗'}
  PyPI: {'✓' if self.creds.has_pypi() else '✗'}
"""


# ============================================================
# Singleton instance
# ============================================================

_cached_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Retorna a configuração singleton (cached).

    Returns:
        Settings: configuração completa.
    """
    global _cached_settings
    if _cached_settings is None:
        _cached_settings = Settings()
    return _cached_settings


def reset_settings() -> None:
    """Reseta o cache de settings (útil para testes)."""
    global _cached_settings
    _cached_settings = None


# ============================================================
# Funções utilitárias
# ============================================================

def ensure_dir(path: Path) -> Path:
    """Garante que um diretório existe, criando-o se necessário.

    Args:
        path: Path do diretório.

    Returns:
        Path: o mesmo path, agora garantido como existente.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_logger_name(name: str) -> str:
    """Gera nome padronizado para logger.

    Args:
        name: nome base do logger.

    Returns:
        str: nome padronizado 'neurociencia_edu.<name>'.
    """
    if not name.startswith("neurociencia_edu"):
        if name == "__main__":
            return "neurociencia_edu.main"
        return f"neurociencia_edu.{name}"
    return name
