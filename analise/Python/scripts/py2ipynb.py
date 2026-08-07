"""Converte .py de análise em .ipynb (células markdown + code)."""
import nbformat as nbf
from pathlib import Path

def py_to_ipynb(py_path, ipynb_path, title):
    content = Path(py_path).read_text()
    lines = content.split("\n")
    cells = []
    current_code = []
    in_docstring = False
    docstring_lines = []

    def flush_code():
        if current_code:
            cells.append(nbf.v4.new_code_cell(source="\n".join(current_code)))
            current_code.clear()

    for line in lines:
        if '"""' in line:
            count = line.count('"""')
            if count == 1 and not in_docstring:
                in_docstring = True
                docstring_lines.append(line.replace('"""', '').strip())
                continue
            elif count == 1 and in_docstring:
                in_docstring = False
                docstring_lines.append(line.replace('"""', '').strip())
                if docstring_lines:
                    cells.append(nbf.v4.new_markdown_cell(source="\n".join(docstring_lines).strip()))
                    docstring_lines.clear()
                continue
            elif count == 2:
                text = line.replace('"""', '').strip()
                if text:
                    cells.append(nbf.v4.new_markdown_cell(source=text))
                continue
        if in_docstring:
            docstring_lines.append(line)
            continue
        if line.strip().startswith("# ===") or line.strip().startswith("## "):
            flush_code()
            cells.append(nbf.v4.new_markdown_cell(source=line.replace("#", "").strip()))
            continue
        if line.strip().startswith("#"):
            flush_code()
            cells.append(nbf.v4.new_markdown_cell(source=line.replace("#", "").strip()))
            continue
        current_code.append(line)
    flush_code()
    title_cell = nbf.v4.new_markdown_cell(source=f"# {title}\n\nAnálise executável gerada a partir de script Python.")
    cells.insert(0, title_cell)
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"}
    }
    with open(ipynb_path, 'w') as f:
        nbf.write(nb, f)
    print(f"OK {ipynb_path}")

if __name__ == "__main__":
    py_to_ipynb(
        "/workspace/analise/Python/notebooks/09_irt_analysis.py",
        "/workspace/analise/Python/notebooks/09_irt_analysis.ipynb",
        "09. Item Response Theory - Modelo de Rasch (P05)"
    )
