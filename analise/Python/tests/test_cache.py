"""Testes para neurociencia_edu.cache."""
import tempfile
from pathlib import Path

import pytest

from neurociencia_edu.cache import AnalysisCache, cached_analysis, get_cache


class TestAnalysisCache:
    """Testes do cache de análises."""

    def test_init_creates_cache_dir(self, tmp_path) -> None:
        """Deve criar diretório de cache."""
        cache_dir = tmp_path / "test_cache"
        AnalysisCache(cache_dir=cache_dir, max_size_gb=0.1)
        assert cache_dir.exists()

    def test_set_and_get(self, tmp_path) -> None:
        """Set + Get deve retornar mesmo valor."""
        cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)
        cache.set("key1", {"data": [1, 2, 3]})
        result = cache.get("key1")
        assert result == {"data": [1, 2, 3]}

    def test_get_nonexistent_returns_none(self, tmp_path) -> None:
        """Get de chave inexistente deve retornar None."""
        cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)
        assert cache.get("nonexistent") is None

    def test_clear(self, tmp_path) -> None:
        """Clear deve remover todos os itens."""
        cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)
        cache.set("k1", 1)
        cache.set("k2", 2)
        n = cache.clear()
        assert n == 2
        assert cache.get("k1") is None

    def test_list(self, tmp_path) -> None:
        """List deve retornar todos os itens."""
        cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)
        cache.set("k1", 1)
        cache.set("k2", 2)
        items = cache.list()
        assert len(items) == 2
        assert any(item["key"] == "k1" for item in items)

    def test_stats(self, tmp_path) -> None:
        """Stats deve retornar info de uso."""
        cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)
        cache.set("k1", "x" * 1000)
        stats = cache.stats()
        assert stats["total_items"] == 1
        assert stats["total_size_kb"] > 0


class TestCachedAnalysisDecorator:
    """Testes do decorator @cached_analysis."""

    def test_caches_function_result(self, tmp_path) -> None:
        """Resultado deve ser cacheado."""
        import neurociencia_edu.cache as cache_mod
        cache_mod._cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)

        call_count = [0]

        @cached_analysis("test_fn")
        def expensive_fn(x: int) -> int:
            call_count[0] += 1
            return x * 2

        result1 = expensive_fn(5)
        result2 = expensive_fn(5)
        assert result1 == 10
        assert result2 == 10
        assert call_count[0] == 1  # só chamado uma vez

    def test_different_args_different_cache(self, tmp_path) -> None:
        """Args diferentes devem gerar cache keys diferentes."""
        import neurociencia_edu.cache as cache_mod
        cache_mod._cache = AnalysisCache(cache_dir=tmp_path / "c", max_size_gb=0.1)

        call_count = [0]

        @cached_analysis("diff_args")
        def fn(x: int) -> int:
            call_count[0] += 1
            return x

        fn(1)
        fn(2)
        fn(1)  # cache hit
        assert call_count[0] == 2
