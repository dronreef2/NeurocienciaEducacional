"""Testes para neurociencia_edu.cli."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


WORKSPACE = Path("/workspace")
CATALOG_PATH = WORKSPACE / "dados_sinteticos" / "catalog.yaml"


# Testes do módulo Catalog (que é usado pelo CLI)


class TestCatalog:
    """Testes do data catalog."""

    def test_catalog_load(self) -> None:
        """Catalog deve carregar YAML válido."""
        from neurociencia_edu.cli import Catalog
        cat = Catalog(str(CATALOG_PATH))
        assert "datasets" in cat.data
        assert len(cat.data["datasets"]) >= 5

    def test_catalog_list(self) -> None:
        """list_datasets deve retornar nomes."""
        from neurociencia_edu.cli import Catalog
        cat = Catalog(str(CATALOG_PATH))
        names = cat.list_datasets()
        assert "P01_diarios_sinteticos" in names
        assert "P05_dados_longitudinais_sinteticos" in names

    def test_catalog_show(self) -> None:
        """show deve retornar metadata de um dataset."""
        from neurociencia_edu.cli import Catalog
        cat = Catalog(str(CATALOG_PATH))
        info = cat.show("P01_diarios_sinteticos")
        assert info["projeto"] == "P01"
        assert info["tipo"] == "csv"
        assert info["n_rows"] == 255

    def test_catalog_show_nonexistent_raises(self) -> None:
        """show de dataset inexistente deve levantar KeyError."""
        from neurociencia_edu.cli import Catalog
        cat = Catalog(str(CATALOG_PATH))
        with pytest.raises(KeyError, match="não encontrado"):
            cat.show("DATASET_INEXISTENTE")

    def test_catalog_by_projeto(self) -> None:
        """by_projeto deve filtrar por projeto."""
        from neurociencia_edu.cli import Catalog
        cat = Catalog(str(CATALOG_PATH))
        p03 = cat.by_projeto("P03")
        assert "P03_eeg_papel" in p03
        assert "P03_eeg_tela" in p03
        assert "P01_diarios_sinteticos" not in p03


class TestCLI:
    """Testes do CLI executado via subprocess."""

    def test_cli_help(self) -> None:
        """CLI --help deve funcionar."""
        result = subprocess.run(
            [sys.executable, "-m", "neurociencia_edu", "--help"],
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE / "analise" / "Python"),
            timeout=10,
        )
        assert result.returncode == 0, f"STDERR: {result.stderr}"
        assert "catalog" in result.stdout or "validate" in result.stdout

    def test_cli_catalog_list(self) -> None:
        """CLI catalog list deve listar datasets."""
        result = subprocess.run(
            [sys.executable, "-m", "neurociencia_edu", "catalog", "list"],
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE / "analise" / "Python"),
            timeout=10,
        )
        assert result.returncode == 0, f"STDERR: {result.stderr}"
        assert "P01" in result.stdout or "P05" in result.stdout
