"""
Logging: Sistema de logging padronizado.

Este módulo fornece uma configuração centralizada de logging para todo o
pacote neurociencia_edu. Usa Rich para output colorido e formatado quando
disponível, com fallback para logging padrão.

Uso básico:
    >>> from neurociencia_edu.logging_config import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("Mensagem informativa")
    >>> logger.error("Erro encontrado")

Configuração customizada:
    >>> from neurociencia_edu.logging_config import configure_logging
    >>> configure_logging(level="DEBUG", log_file="app.log")
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Union


# ============================================================
# Constantes
# ============================================================

DEFAULT_FORMAT = "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

DEFAULT_LEVEL = "INFO"
LOG_FILE_ENV = "NEUROCIENCIA_LOG_FILE"
LOG_LEVEL_ENV = "NEUROCIENCIA_LOG_LEVEL"


# ============================================================
# Detecção de dependências opcionais
# ============================================================

try:
    from rich.logging import RichHandler
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


# ============================================================
# Funções públicas
# ============================================================

def configure_logging(
    level: Optional[Union[str, int]] = None,
    log_file: Optional[Union[str, Path]] = None,
    use_rich: Optional[bool] = None,
    quiet: bool = False,
) -> logging.Logger:
    """Configura o sistema de logging global.

    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
              Default: env var NEUROCIENCIA_LOG_LEVEL ou INFO.
        log_file: Path para arquivo de log (opcional).
        use_rich: Se True, usa Rich para output colorido.
                 Se None, detecta automaticamente.
        quiet: Se True, desabilita output no console.

    Returns:
        logging.Logger: logger raiz configurado.
    """
    # Resolver nível
    if level is None:
        level = os.getenv(LOG_LEVEL_ENV, DEFAULT_LEVEL)
    if isinstance(level, str):
        level = level.upper()

    # Resolver formato
    if use_rich is None:
        use_rich = HAS_RICH and not quiet

    # Logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Limpar handlers existentes (evitar duplicação)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    if not quiet:
        if use_rich:
            console_handler = RichHandler(
                rich_tracebacks=True,
                show_path=False,
                show_time=True,
                markup=True,
            )
            console_handler.setLevel(level)
            root_logger.addHandler(console_handler)
        else:
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(level)
            formatter = logging.Formatter(DEFAULT_FORMAT, datefmt=DEFAULT_DATEFMT)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

    # File handler
    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(DEFAULT_FORMAT, datefmt=DEFAULT_DATEFMT)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Configurar loggers de bibliotecas verbosas
    _configure_verbose_libraries(level)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Retorna um logger com nome padronizado.

    Args:
        name: nome do módulo (geralmente __name__).

    Returns:
        logging.Logger: logger configurado.
    """
    # Se ainda não foi configurado, configura com defaults
    if not logging.getLogger().handlers:
        configure_logging()

    # Padronizar nome
    if not name.startswith("neurociencia_edu"):
        if name == "__main__":
            name = "neurociencia_edu.main"
        else:
            name = f"neurociencia_edu.{name}"

    return logging.getLogger(name)


# ============================================================
# Funções auxiliares
# ============================================================

def _configure_verbose_libraries(level: Union[str, int]) -> None:
    """Reduz verbosidade de bibliotecas que logam demais."""
    numeric_level = logging.getLevelName(level) if isinstance(level, str) else level

    # Bibliotecas verbosas
    verbose_loggers = [
        "matplotlib",
        "PIL",
        "urllib3",
        "asyncio",
        "filelock",
        "h5py",
    ]

    for name in verbose_loggers:
        lib_logger = logging.getLogger(name)
        # Só reduzir se o nível do usuário for mais permissivo
        if numeric_level > logging.DEBUG:
            lib_logger.setLevel(logging.WARNING)
        lib_logger.propagate = True


def log_function_call(logger: logging.Logger) -> "callable":
    """Decorator para logar entrada/saída de funções.

    Args:
        logger: logger a ser usado.

    Returns:
        callable: decorator.
    """
    def decorator(func: "callable") -> "callable":
        def wrapper(*args, **kwargs):
            logger.debug(f"→ {func.__name__}()")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"← {func.__name__}() OK")
                return result
            except Exception as e:
                logger.error(f"× {func.__name__}() falhou: {e}")
                raise
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


def log_section(logger: logging.Logger, title: str) -> None:
    """Loga uma seção com separador visual.

    Args:
        logger: logger a ser usado.
        title: título da seção.
    """
    sep = "=" * 70
    logger.info(sep)
    logger.info(f"  {title}")
    logger.info(sep)


# ============================================================
# Inicialização automática
# ============================================================

# Configura logging ao importar o módulo (apenas uma vez)
if not logging.getLogger().handlers:
    log_file_env = os.getenv(LOG_FILE_ENV)
    configure_logging(log_file=log_file_env)
