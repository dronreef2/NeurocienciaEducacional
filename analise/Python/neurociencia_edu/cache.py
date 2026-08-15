"""Cache inteligente de análises.

Cache baseado em SHA256 de (input file content + function source).
Permite re-rodar análises pesadas sem reprocessar inputs não modificados.
"""
from __future__ import annotations

import functools
import hashlib
import inspect
import json
import os
import pickle
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Optional

from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


DEFAULT_CACHE_DIR = ".neuro_cache"
DEFAULT_MAX_GB = 1.0


class AnalysisCache:
    """Cache persistente para resultados de análises."""

    def __init__(
        self,
        cache_dir: str | Path = DEFAULT_CACHE_DIR,
        max_size_gb: float = DEFAULT_MAX_GB,
    ) -> None:
        """Inicializa o cache.

        Args:
            cache_dir: Diretório do cache.
            max_size_gb: Tamanho máximo em GB (LRU eviction).
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = int(max_size_gb * 1024 * 1024 * 1024)
        self.meta_file = self.cache_dir / "metadata.json"
        self.metadata: dict[str, dict] = self._load_metadata()
        logger.info(f"Cache initialized at {self.cache_dir} (max {max_size_gb}GB)")

    def _load_metadata(self) -> dict[str, dict]:
        """Carrega metadata de entradas anteriores."""
        if self.meta_file.exists():
            with open(self.meta_file) as f:
                return json.load(f)
        return {}

    def _save_metadata(self) -> None:
        """Salva metadata."""
        with open(self.meta_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    @staticmethod
    def _hash_inputs(args: tuple, kwargs: dict) -> str:
        """Gera hash dos inputs."""
        h = hashlib.sha256()
        for a in args:
            if isinstance(a, (str, Path)) and Path(a).exists():
                # Hash do conteúdo do arquivo
                with open(a, "rb") as f:
                    h.update(f.read())
            else:
                h.update(repr(a).encode())
        for k, v in sorted(kwargs.items()):
            h.update(k.encode())
            if isinstance(v, (str, Path)) and Path(v).exists():
                with open(v, "rb") as f:
                    h.update(f.read())
            else:
                h.update(repr(v).encode())
        return h.hexdigest()

    @staticmethod
    def _hash_function(func: Callable) -> str:
        """Gera hash do código-fonte da função."""
        try:
            source = inspect.getsource(func)
        except (OSError, TypeError):
            source = func.__name__
        return hashlib.sha256(source.encode()).hexdigest()[:16]

    def get(self, key: str) -> Any | None:
        """Recupera item do cache.

        Args:
            key: Chave do cache.

        Returns:
            Valor armazenado ou None se não existir.
        """
        cache_file = self.cache_dir / f"{key}.pkl"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "rb") as f:
                value = pickle.load(f)
            # Update access time
            if key in self.metadata:
                self.metadata[key]["accessed"] = time.time()
                self._save_metadata()
            logger.debug(f"Cache hit: {key[:16]}")
            return value
        except (pickle.UnpicklingError, EOFError) as e:
            logger.warning(f"Cache file corrupted: {key} ({e})")
            cache_file.unlink(missing_ok=True)
            return None

    def set(self, key: str, value: Any) -> None:
        """Armazena item no cache.

        Args:
            key: Chave do cache.
            value: Valor a armazenar.
        """
        cache_file = self.cache_dir / f"{key}.pkl"
        with open(cache_file, "wb") as f:
            pickle.dump(value, f)

        size = cache_file.stat().st_size
        self.metadata[key] = {
            "size": size,
            "created": time.time(),
            "accessed": time.time(),
        }
        self._save_metadata()
        self._evict_if_needed()
        logger.debug(f"Cache stored: {key[:16]} ({size} bytes)")

    def _evict_if_needed(self) -> None:
        """Remove itens menos usados se cache > max_size."""
        total_size = sum(m["size"] for m in self.metadata.values())
        if total_size <= self.max_size_bytes:
            return

        # Ordenar por accessed time (LRU)
        sorted_keys = sorted(
            self.metadata.keys(),
            key=lambda k: self.metadata[k]["accessed"]
        )

        for key in sorted_keys:
            if total_size <= self.max_size_bytes:
                break
            cache_file = self.cache_dir / f"{key}.pkl"
            cache_file.unlink(missing_ok=True)
            total_size -= self.metadata[key]["size"]
            del self.metadata[key]
            logger.info(f"Cache evicted: {key[:16]}")

        self._save_metadata()

    def clear(self) -> int:
        """Limpa todo o cache.

        Returns:
            Número de itens removidos.
        """
        n = len(self.metadata)
        for key in list(self.metadata.keys()):
            cache_file = self.cache_dir / f"{key}.pkl"
            cache_file.unlink(missing_ok=True)
        self.metadata.clear()
        self._save_metadata()
        logger.info(f"Cache cleared: {n} items removed")
        return n

    def list(self) -> list[dict]:
        """Lista itens no cache.

        Returns:
            Lista de dicts com info de cada item.
        """
        items = []
        for key, meta in self.metadata.items():
            items.append({
                "key": key,
                "size_kb": meta["size"] / 1024,
                "created": meta["created"],
                "accessed": meta["accessed"],
            })
        return items

    def stats(self) -> dict:
        """Retorna estatísticas do cache.

        Returns:
            Dict com stats.
        """
        total_size = sum(m["size"] for m in self.metadata.values())
        return {
            "total_items": len(self.metadata),
            "total_size_kb": total_size / 1024,
            "total_size_mb": total_size / 1024 / 1024,
            "max_size_gb": self.max_size_bytes / 1024 / 1024 / 1024,
            "utilization": total_size / self.max_size_bytes if self.max_size_bytes > 0 else 0,
        }


# ============================================================
# Singleton
# ============================================================

_cache: Optional[AnalysisCache] = None


def get_cache() -> AnalysisCache:
    """Retorna a instância singleton do cache."""
    global _cache
    if _cache is None:
        _cache = AnalysisCache()
    return _cache


def cached_analysis(name: Optional[str] = None) -> Callable:
    """Decorator para cachear resultados de uma análise.

    Args:
        name: Nome opcional (default: nome da função).

    Returns:
        Decorator.

    Example:
        >>> @cached_analysis("mixed_models_p01")
        >>> def run_mixed(df_path):
        ...     return expensive_computation(df_path)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache()
            func_hash = AnalysisCache._hash_function(func)
            input_hash = AnalysisCache._hash_inputs(args, kwargs)
            cache_key = f"{(name or func.__name__)}_{func_hash}_{input_hash}"

            cached = cache.get(cache_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        return wrapper
    return decorator
