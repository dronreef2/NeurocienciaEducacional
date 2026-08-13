# P01 — Manuscrito Renderizado

> **Versões renderizadas do manuscrito P01 em múltiplos formatos**

## 📂 Arquivos

| Arquivo | Formato | Tamanho | Uso |
|---|---|---|---|
| `P01-manuscrito-quarto.html` | HTML | ~500KB | Web, GitHub Pages |
| `P01-manuscrito-quarto.pdf` | PDF (A4, two-column) | ~1MB | Submissão revista |
| `P01-manuscrito-quarto.docx` | DOCX (Word) | ~200KB | Revisão por co-autores |

## 🔄 Como regenerar

### Local
```bash
# Instalar Quarto: https://quarto.org/docs/get-started/
quarto render P01-manuscrito-quarto.qmd --to html
quarto render P01-manuscrito-quarto.qmd --to pdf
quarto render P01-manuscrito-quarto.qmd --to docx
```

### Automático (CI)
O workflow `.github/workflows/quarto-render.yml` regenera os arquivos
a cada push em main.

## 🌐 Visualizar online

GitHub Pages: https://dronreef2.github.io/NeurocienciaEducacional/P01-manuscrito-quarto.html

## 📝 Submissão

Para enviar para Computers & Education:
- Use o PDF: `P01-manuscrito-quarto.pdf`
- Submeta via Editorial Manager: https://www.editorialmanager.com/compedu/
- Inclua highlights (3-5 bullet points)
- Inclua cover letter personalizada

## 🔗 Arquivos fonte

- Fonte Quarto: `../P01-manuscrito-quarto.qmd`
- Bibliografia: `../../referencias/referencias.bib`
- Estilo CSL: `../../referencias/apa-7.csl`
- Config: `../../../_quarto.yml`
