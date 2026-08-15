"""Testes de execução dos notebooks (smoke tests)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"

NOTEBOOKS_TO_TEST = [
    "01_tutorial_basico.py",
    "03_tutorial_irt.py",
    "05_bayesian_analysis.py",
    "08_power_analysis.py",
    "13_item_analysis.py",
    "14_bibliometria.py",
    "15_ppt_simulacao_piloto.py",
]


@pytest.mark.parametrize("notebook", NOTEBOOKS_TO_TEST)
def test_notebook_runs_without_error(notebook: str) -> None:
    """Cada notebook deve executar sem erro."""
    path = NOTEBOOKS_DIR / notebook
    if not path.exists():
        pytest.skip(f"Notebook não encontrado: {path}")

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=NOTEBOOKS_DIR.parent,
    )

    assert result.returncode == 0, (
        f"Notebook {notebook} falhou (exit {result.returncode})\n"
        f"STDOUT: {result.stdout[-300:]}\n"
        f"STDERR: {result.stderr[-300:]}"
    )


def test_all_notebooks_have_docstring() -> None:
    """Todos os notebooks devem ter docstring no topo."""
    notebooks = list(NOTEBOOKS_DIR.glob("*.py"))
    assert len(notebooks) >= 10

    for nb in notebooks:
        with open(nb) as f:
            content = f.read(500)
        assert '"""' in content or "'''" in content, f"{nb.name} sem docstring"
