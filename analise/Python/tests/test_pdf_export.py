"""Testes para neurociencia_edu.pdf_export."""
import io

import pandas as pd
import pytest

from neurociencia_edu.pdf_export import (
    generate_project_pdf,
    generate_summary_pdf,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "x": [1, 2, 3, 4, 5] * 10,
        "y": [2, 4, 5, 4, 5] * 10,
        "group": ["A", "B"] * 25,
    })


class TestGenerateProjectPDF:
    """Testes do gerador de PDF por projeto."""

    def test_returns_bytes(self, sample_df: pd.DataFrame) -> None:
        """Deve retornar bytes (PDF)."""
        pdf = generate_project_pdf(
            project_id="P01",
            title="IA e MToM",
            data=sample_df,
        )
        assert isinstance(pdf, bytes)
        assert len(pdf) > 1000  # PDF não-trivial

    def test_starts_with_pdf_magic(self, sample_df: pd.DataFrame) -> None:
        """PDF deve começar com %PDF."""
        pdf = generate_project_pdf("P01", "Test", sample_df)
        assert pdf.startswith(b"%PDF")

    def test_with_metadata(self, sample_df: pd.DataFrame) -> None:
        """Com metadata não deve quebrar."""
        pdf = generate_project_pdf(
            project_id="P02",
            title="Gamificação",
            data=sample_df,
            metadata={"N": 200, "Período": "2026-2028"},
        )
        assert pdf.startswith(b"%PDF")

    def test_with_figures(self, sample_df: pd.DataFrame, tmp_path) -> None:
        """Com figuras não deve quebrar."""
        # Criar PNG fake
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig_path = tmp_path / "test.png"
        plt.plot([1, 2, 3])
        plt.savefig(fig_path, dpi=100)
        plt.close()

        pdf = generate_project_pdf(
            project_id="P03",
            title="EEG",
            data=sample_df,
            figures=[str(fig_path)],
        )
        assert pdf.startswith(b"%PDF")

    def test_a4_format(self, sample_df: pd.DataFrame) -> None:
        """Formato A4 deve funcionar."""
        pdf = generate_project_pdf(
            project_id="P04",
            title="SEM",
            data=sample_df,
            format="A4",
        )
        assert pdf.startswith(b"%PDF")


class TestGenerateSummaryPDF:
    """Testes do PDF sumário."""

    def test_summary_returns_bytes(self) -> None:
        """Sumário deve retornar bytes."""
        projects = {
            "P01": {
                "title": "IA e MToM",
                "description": "Estudo qualitativo",
                "metadata": {"N": 15},
            },
            "P02": {
                "title": "Gamificação",
                "description": "ECR 2x4",
                "metadata": {"N": 200},
            },
        }
        pdf = generate_summary_pdf(projects)
        assert isinstance(pdf, bytes)
        assert pdf.startswith(b"%PDF")
