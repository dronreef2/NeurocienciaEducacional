"""
figura1-framework-teorico.py
Gera Figura 1: Framework teórico do P01
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def criar_framework_teorico(output_path: str = "figura1_framework_teorico.png"):
    """Cria o framework teórico conceitual do P01."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Cores
    cor_input = "#3498db"
    cor_output = "#e74c3c"
    cor_mediador = "#f39c12"
    cor_moderador = "#27ae60"
    cor_experiencia = "#9b59b6"

    def add_box(x, y, w, h, text, color, text_color="white", fontsize=11):
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.1",
            facecolor=color, edgecolor="black", linewidth=1.5
        )
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center",
                color=text_color, fontsize=fontsize, fontweight="bold")

    # Título
    ax.text(6, 7.5, "Figura 1. Framework Teórico do P01",
            ha="center", fontsize=14, fontweight="bold")
    ax.text(6, 7.1, "Vozes das Crianças sobre Tutores de IA",
            ha="center", fontsize=11, style="italic", color="gray")

    # Input
    add_box(2, 5.5, 2, 0.8, "Uso do Khanmigo\n(8 semanas)", cor_input, fontsize=10)

    # Experiências
    add_box(6, 5.5, 2.5, 0.8, "Experiências com IA\n(afetiva, cognitiva)", cor_experiencia, fontsize=10)

    # Mediadores
    add_box(6, 3.5, 2.5, 0.8, "Mediação:\nMetacognição + Confiança Calibrada", cor_mediador, fontsize=10)

    # Outputs
    add_box(10, 5.5, 2, 0.8, "Compreensão infantil\nda IA", cor_output, fontsize=10)

    # Moderadores
    add_box(2, 1.5, 2.5, 0.8, "Moderadores:\nIdade, SES, Letramento Digital", cor_moderador, fontsize=10)

    # Setas
    arrow_props = dict(arrowstyle="->", color="black", lw=2, mutation_scale=20)

    ax.annotate("", xy=(4.8, 5.5), xytext=(3, 5.5), arrowprops=arrow_props)
    ax.annotate("", xy=(9, 5.5), xytext=(7.2, 5.5), arrowprops=arrow_props)
    ax.annotate("", xy=(6, 4.3), xytext=(6, 5.1), arrowprops=arrow_props)
    ax.annotate("", xy=(9.5, 5.2), xytext=(7, 4), arrowprops=arrow_props)
    ax.annotate("", xy=(4, 3.2), xytext=(3, 1.9), arrowprops=arrow_props)
    ax.annotate("", xy=(2, 4.9), xytext=(2, 2.3), arrowprops=arrow_props)

    # Legenda
    legend_y = 0.3
    items = [
        ("Variável independente", cor_input),
        ("Variável mediadora", cor_mediador),
        ("Variável moderadora", cor_moderador),
        ("Variável dependente", cor_output),
    ]
    for i, (label, color) in enumerate(items):
        x_pos = 1 + i * 3
        rect = plt.Rectangle((x_pos, legend_y), 0.3, 0.2,
                             facecolor=color, edgecolor="black")
        ax.add_patch(rect)
        ax.text(x_pos + 0.4, legend_y + 0.1, label, va="center", fontsize=9)

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Figura salva: {output_path}")


if __name__ == "__main__":
    criar_framework_teorico("docs/manuscritos/figuras/figura1_framework_teorico.png")
