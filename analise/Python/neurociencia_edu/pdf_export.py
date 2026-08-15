"""Geração de relatórios PDF para o dashboard Streamlit."""
from __future__ import annotations

import io
from datetime import datetime
from typing import Optional

import pandas as pd

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_project_pdf(
    project_id: str,
    title: str,
    data: pd.DataFrame,
    metadata: Optional[dict] = None,
    figures: Optional[list] = None,
    format: str = "letter",
) -> bytes:
    """Gera PDF de um projeto.

    Args:
        project_id: ID do projeto (P01, P02, etc.)
        title: Título do relatório
        data: DataFrame com os dados
        metadata: Dict com info adicional (n_rows, periodo, etc.)
        figures: Lista de paths para figuras PNG (opcional)
        format: Tamanho da página (letter ou A4)

    Returns:
        Bytes do PDF gerado.
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab não está instalado")

    buffer = io.BytesIO()
    pagesize = letter if format == "letter" else A4
    doc = SimpleDocTemplate(buffer, pagesize=pagesize)
    elements = []
    styles = getSampleStyleSheet()

    # Estilo customizado
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], fontSize=18, spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading2"], fontSize=14, spaceAfter=8,
    )
    body_style = styles["BodyText"]

    # Cabeçalho
    elements.append(Paragraph(f"{project_id} — {title}", title_style))
    elements.append(Paragraph(
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        body_style,
    ))
    elements.append(Spacer(1, 0.2 * inch))

    # Metadata
    if metadata:
        elements.append(Paragraph("Metadados", heading_style))
        meta_data = []
        for k, v in metadata.items():
            meta_data.append([str(k), str(v)])
        meta_table = Table(meta_data, colWidths=[2 * inch, 4 * inch])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.2 * inch))

    # Resumo estatístico
    elements.append(Paragraph("Resumo Estatístico", heading_style))

    numeric_cols = data.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        summary = data[numeric_cols].describe().T.reset_index()
        summary_data = [["Variável", "N", "Média", "DP", "Min", "Max"]]
        for _, row in summary.iterrows():
            summary_data.append([
                str(row["index"]),
                f"{int(row['count'])}",
                f"{row['mean']:.2f}",
                f"{row['std']:.2f}",
                f"{row['min']:.2f}",
                f"{row['max']:.2f}",
            ])
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))
        elements.append(summary_table)

    elements.append(PageBreak())

    # Dados brutos (primeiras 20 linhas)
    elements.append(Paragraph("Dados Brutos (primeiras 20 linhas)", heading_style))
    table_data = [data.columns.tolist()] + data.head(20).astype(str).values.tolist()
    raw_table = Table(table_data, repeatRows=1)
    raw_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
    ]))
    elements.append(raw_table)

    # Figuras
    if figures:
        elements.append(PageBreak())
        elements.append(Paragraph("Figuras", heading_style))
        for fig_path in figures:
            try:
                from reportlab.platypus import Image as RLImage
                elements.append(RLImage(fig_path, width=6 * inch, height=4 * inch))
                elements.append(Spacer(1, 0.2 * inch))
            except Exception:
                pass

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_summary_pdf(
    projects: dict[str, dict],
) -> bytes:
    """Gera PDF sumário com todos os 5 projetos.

    Args:
        projects: Dict {P01: {title, data, metadata}, ...}

    Returns:
        Bytes do PDF.
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab não está instalado")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Capa
    elements.append(Paragraph("Programa de Pesquisa em Neurociência Educacional", styles["Title"]))
    elements.append(Paragraph("Sumário Executivo · 5 Projetos", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["BodyText"],
    ))
    elements.append(Paragraph("UFRN · CERES · PPGED", styles["BodyText"]))
    elements.append(Paragraph("Orientadora: Profa. Dra. Ângela M. C. Naschold", styles["BodyText"]))
    elements.append(PageBreak())

    # Sumário por projeto
    for pid, info in projects.items():
        elements.append(Paragraph(f"{pid} — {info.get('title', '?')}", styles["Heading1"]))
        if "description" in info:
            elements.append(Paragraph(info["description"], styles["BodyText"]))
            elements.append(Spacer(1, 0.1 * inch))
        if "metadata" in info:
            meta_data = []
            for k, v in info["metadata"].items():
                meta_data.append([str(k), str(v)])
            meta_table = Table(meta_data, colWidths=[2 * inch, 4 * inch])
            meta_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(meta_table)
        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
