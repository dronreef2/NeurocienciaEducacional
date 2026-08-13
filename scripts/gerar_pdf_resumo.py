"""
gerar_pdf_resumo.py
Gera PDF do Resumo Executivo usando reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image as RLImage, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from pathlib import Path
from datetime import datetime
import os

# ============================================================
# Configuração
# ============================================================
OUTPUT = Path("/workspace/docs/RESUMO-EXECUTIVO.pdf")
INPUT_MD = Path("/workspace/RESUMO-EXECUTIVO.md")
LOGO = "/workspace/resultados/simulacao_piloto/simulacao_piloto_p01.png"

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=2*cm,
    rightMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title="Resumo Executivo — Programa de Pesquisa em Neurociência Educacional",
    author="Programa de Pesquisa (UFRN/CERES)",
    subject="5 projetos (2026-2030)",
    creator="reportlab",
    keywords="neurociência educacional, IA generativa, crianças, funções executivas"
)

# ============================================================
# Estilos
# ============================================================
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=22,
    textColor=colors.HexColor("#1a3a52"),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold"
)

style_subtitle = ParagraphStyle(
    "CustomSubtitle",
    parent=styles["Heading2"],
    fontSize=14,
    textColor=colors.HexColor("#2c3e50"),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName="Helvetica-Oblique"
)

style_h1 = ParagraphStyle(
    "CustomH1",
    parent=styles["Heading1"],
    fontSize=18,
    textColor=colors.HexColor("#2c3e50"),
    spaceBefore=20,
    spaceAfter=10,
    fontName="Helvetica-Bold",
    borderPadding=8,
    borderColor=colors.HexColor("#667eea"),
    borderWidth=2,
    leftIndent=0,
    borderRadius=4,
)

style_h2 = ParagraphStyle(
    "CustomH2",
    parent=styles["Heading2"],
    fontSize=14,
    textColor=colors.HexColor("#1a3a52"),
    spaceBefore=15,
    spaceAfter=8,
    fontName="Helvetica-Bold",
)

style_h3 = ParagraphStyle(
    "CustomH3",
    parent=styles["Heading3"],
    fontSize=12,
    textColor=colors.HexColor("#34495e"),
    spaceBefore=10,
    spaceAfter=5,
    fontName="Helvetica-Bold"
)

style_body = ParagraphStyle(
    "CustomBody",
    parent=styles["BodyText"],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    fontName="Helvetica"
)

style_code = ParagraphStyle(
    "CustomCode",
    parent=styles["Code"],
    fontSize=8,
    leading=10,
    fontName="Courier",
    backColor=colors.HexColor("#f4f4f4"),
    leftIndent=15,
    rightIndent=15,
    spaceBefore=5,
    spaceAfter=10,
    borderColor=colors.HexColor("#ddd"),
    borderWidth=0.5,
    borderPadding=5,
)

style_quote = ParagraphStyle(
    "CustomQuote",
    parent=styles["BodyText"],
    fontSize=10,
    leading=14,
    fontName="Helvetica-Oblique",
    textColor=colors.HexColor("#555"),
    leftIndent=30,
    rightIndent=30,
    spaceBefore=8,
    spaceAfter=8,
    borderColor=colors.HexColor("#667eea"),
    borderWidth=0,
    leftBorderWidth=3,
    borderPadding=8,
)

# ============================================================
# Construir conteúdo
# ============================================================
story = []

# Capa
story.append(Paragraph("Programa de Pesquisa em", style_title))
story.append(Paragraph("Neurociência Educacional", style_title))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Resumo Executivo", style_subtitle))
story.append(Paragraph("5 projetos, 5 anos (2026-2030), 1 orientadora, 1 repositório", style_subtitle))
story.append(Spacer(1, 1.5*cm))

# Capa info
capa_info = [
    ["Pesquisador principal:", "[Seu nome]"],
    ["Orientadora:", "Profa. Dra. Ângela M. C. Naschold"],
    ["Instituição:", "UFRN / CERES / PPGED"],
    ["Período:", "2026-2030 (60 meses)"],
    ["Local:", "Natal e Caicó, RN, Brasil"],
    ["Versão:", "1.0 — " + datetime.now().strftime("%Y-%m-%d")],
    ["Repositório:", "github.com/dronreef2/NeurocienciaEducacional"],
]
t = Table(capa_info, colWidths=[5*cm, 11*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ecf0f1")),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3a52")),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#667eea")),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#bdc3c7")),
]))
story.append(t)
story.append(Spacer(1, 1.5*cm))

# Imagem
if os.path.exists(LOGO):
    img = RLImage(LOGO, width=14*cm, height=10*cm)
    story.append(img)
    story.append(Paragraph("<i>Figura 21 — Simulação completa do piloto P01 (N=30, T=14)</i>",
                           ParagraphStyle("img_caption", parent=style_body, alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#777"))))

story.append(PageBreak())

# Visão Geral
story.append(Paragraph("🎯 Visão Geral", style_h1))
story.append(Paragraph(
    "Este programa de pesquisa investiga como <b>Inteligências Artificiais generativas</b> "
    "(IA/GenAI) impactam o desenvolvimento cognitivo, emocional e acadêmico de crianças "
    "do 2º ao 5º ano do Ensino Fundamental, com foco em <b>funções executivas</b> (FE), "
    "<b>leitura</b> e <b>engajamento escolar</b>.",
    style_body))
story.append(Paragraph(
    "A abordagem combina métodos <b>qualitativos</b>, <b>quantitativos</b> e <b>neurocientíficos</b> "
    "para gerar evidências robustas e aplicáveis ao contexto educacional brasileiro.",
    style_body))

# Os 5 Projetos
story.append(Paragraph("📚 Os 5 Projetos", style_h1))

projetos = [
    ("P01", "IA Generativa e Cognição de Teoria da Mente (Qualitativo)",
     "Computers & Education", "N=12-15 crianças, 18 meses",
     "Análise Temática Reflexiva + 5 testes estatísticos",
     "Manuscrito v1 escrito ✅, piloto n=3 concluído ✅"),
    ("P02", "Gamificação e Funções Executivas (ECR 2×4)",
     "Computers in Human Behavior", "N=200 (4 grupos × 50), 14 meses",
     "ANCOVA + modelos mistos + simulação",
     "Protocolo ✅, simulação ✅"),
    ("P03", "IA Generativa e Leitura (EEG 32-canais)",
     "NeuroImage", "N=60 crianças, 18 meses",
     "ERP + ANOVA + cluster-based permutation",
     "Protocolo ✅, simulação ✅"),
    ("P04", "IA Generativa e FE (SEM Transversal)",
     "Computers in Human Behavior", "N=300-500, 15 meses",
     "CFA + SEM + Mediação + Moderação",
     "Protocolo ✅"),
    ("P05", "Coorte Longitudinal de FE (LGCM)",
     "Child Development", "N=200 crianças × 5 ondas, 30 meses",
     "LGCM + IRT + Sobrevivência + CTT + Mixed Models",
     "Protocolo ✅, simulação ✅"),
]

for pid, titulo, revista, amostra, analise, status in projetos:
    story.append(Paragraph(f"<b>{pid} — {titulo}</b>", style_h3))
    info_proj = [
        ["Revista-alvo:", revista],
        ["Amostra:", amostra],
        ["Análise:", analise],
        ["Status:", status],
    ]
    t = Table(info_proj, colWidths=[3*cm, 13*cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3a52")),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

story.append(PageBreak())

# Cronograma
story.append(Paragraph("📊 Cronograma Consolidado (2026-2030)", style_h1))

cronograma_data = [
    ["Ano", "P01", "P02", "P03", "P04", "P05"],
    ["2026", "Coleta", "Setup", "Setup", "—", "—"],
    ["2027", "Análise", "Coleta", "Coleta", "Coleta", "Setup"],
    ["2028", "Manuscrito", "Manuscrito", "Manuscrito", "Manuscrito", "Coleta"],
    ["2029-30", "Replicação", "Replicação", "Replicação", "Análise final", "Análise final"],
]

t = Table(cronograma_data, colWidths=[2*cm, 2.7*cm, 2.7*cm, 2.7*cm, 2.7*cm, 2.7*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a52")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# Contribuições
story.append(Paragraph("🎓 Contribuições Esperadas", style_h1))

contrib_data = [
    ["Tipo", "Item", "Quantidade"],
    ["Científica", "Manuscritos A1 (IF > 6)", "5"],
    ["Científica", "Pré-registros OSF", "5"],
    ["Científica", "Conjuntos de dados (LGPD)", "5"],
    ["Científica", "Tese de doutorado (parcial)", "1"],
    ["Social", "Política educacional", "1 doc"],
    ["Social", "Programa de letramento digital", "1"],
    ["Educacional", "Design de IA educacional", "1"],
    ["Educacional", "Currículo escolar (BNCC + IA)", "1"],
]

t = Table(contrib_data, colWidths=[3*cm, 9*cm, 3*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#667eea")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

story.append(PageBreak())

# Orçamento
story.append(Paragraph("💰 Orçamento Consolidado", style_h1))

orcamento_data = [
    ["Categoria", "Valor (R$)"],
    ["Bolsistas (60 meses)", "90.000"],
    ["Material e equipamentos (EEG, tablets)", "35.000"],
    ["Plataformas e licenças", "8.000"],
    ["Tradução e revisão", "6.000"],
    ["Análise estatística (consultores)", "10.000"],
    ["Congressos (5)", "25.000"],
    ["Publicações (5 Open Access)", "30.000"],
    ["<b>TOTAL</b>", "<b>204.000</b>"],
]

t = Table(orcamento_data, colWidths=[10*cm, 5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a52")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#667eea")),
    ("TEXTCOLOR", (0, -1), (-1, -1), colors.whitesmoke),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "<b>Fontes de financiamento:</b> CAPES (bolsas), CNPq (Universal), "
    "FAPERN (RN), UFRN (edital interno).",
    style_body))

# Métricas
story.append(Paragraph("📈 Métricas do Programa", style_h1))

metricas_data = [
    ["Métrica", "Valor"],
    ["Projetos", "5"],
    ["Duração", "5 anos (60 meses)"],
    ["Pré-registros OSF", "5 ✅"],
    ["Métodos estatísticos", "10+"],
    ["Idiomas", "3 (PT/EN/ES)"],
    ["Artigos esperados", "5 (A1, IF > 6)"],
    ["Financiamento", "R$ 204k"],
    ["Equipe", "5+ pesquisadores"],
    ["Escolas parceiras", "6"],
    ["Participantes totais", "~800"],
]

t = Table(metricas_data, colWidths=[10*cm, 5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a52")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
]))
story.append(t)

story.append(PageBreak())

# Próximos passos
story.append(Paragraph("📅 Próximos Passos Imediatos", style_h1))

proximos = [
    ("1", "Reunião com Angela", "agendar", "Apresentar protocolo completo"),
    ("2", "Submissão CEP (P01)", "imediato", "Documentos prontos ✅"),
    ("3", "Recrutamento P01", "M1-M2", "N=12-15 crianças"),
    ("4", "Coleta de dados P01", "M3-M4", "2 meses de diários"),
    ("5", "Análise P01", "M5-M7", "Análise Temática + 5 testes"),
    ("6", "Manuscrito P01", "M8-M10", "Computers & Education"),
    ("7", "Iniciar P02-P05", "M6+", "Em paralelo"),
]

t = Table(
    [["#", "Atividade", "Quando", "Observação"]] +
    [[n, a, q, o] for n, a, q, o in proximos],
    colWidths=[1*cm, 4.5*cm, 3*cm, 6.5*cm]
)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a52")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("ALIGN", (1, 0), (1, -1), "LEFT"),
    ("ALIGN", (2, 0), (2, -1), "CENTER"),
    ("ALIGN", (3, 0), (3, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
]))
story.append(t)

# Links úteis
story.append(Spacer(1, 1*cm))
story.append(Paragraph("🔗 Links Úteis", style_h2))
links = [
    "Repositório: github.com/dronreef2/NeurocienciaEducacional",
    "Dashboard: neurociencia-educacional.streamlit.app",
    "Documentação: dronreef2.github.io/NeurocienciaEducacional",
    "UFRN: ufrn.br | CERES: ufrn.br/ceres | PPGED: ufrn.br/ppged",
]
for link in links:
    story.append(Paragraph(f"• {link}", style_body))

# Rodapé
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "<i>Programa completo, documentado, pré-registrado, pronto para execução.</i>",
    ParagraphStyle("footer", parent=style_body, alignment=TA_CENTER, fontSize=11, textColor=colors.HexColor("#667eea"), fontName="Helvetica-Oblique")
))
story.append(Paragraph(
    f"Gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')} via reportlab",
    ParagraphStyle("footer2", parent=style_body, alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#999"))
))

# ============================================================
# Gerar PDF
# ============================================================
doc.build(story)
print(f"✓ PDF gerado: {OUTPUT}")
print(f"  Tamanho: {OUTPUT.stat().st_size / 1024:.1f} KB")
