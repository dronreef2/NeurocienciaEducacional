"""
figura5-dag-p04.py
Gera Figura 5: DAG (Directed Acyclic Graph) para P04
Causal model for IA → FE via mediation/moderation
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np


def criar_dag_p04(output_path: str = "figura5_dag_p04.png"):
    """Cria o DAG causal do P04 (IA generativa → FE via mediação e moderação)."""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Cores
    cor_iv = "#3498db"   # azul (variável independente)
    cor_dv = "#e74c3c"   # vermelho (variável dependente)
    cor_med = "#f39c12"  # laranja (mediador)
    cor_mod = "#27ae60"  # verde (moderador)
    cor_ctrl = "#9b59b6" # roxo (controle)

    def add_node(x, y, w, h, text, color, text_color="white", fontsize=11):
        box = mpatches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.1",
            facecolor=color, edgecolor="black", linewidth=2
        )
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center",
                color=text_color, fontsize=fontsize, fontweight="bold")

    def add_arrow(x1, y1, x2, y2, label="", style="->", color="black", lw=2):
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=20,
            color=color, linewidth=lw
        )
        ax.add_patch(arrow)
        if label:
            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(mid_x + 0.1, mid_y + 0.1, label,
                    fontsize=8, color=color, fontweight="bold",
                    bbox=dict(boxstyle="round", facecolor="white", edgecolor=color, pad=2))

    # Título
    ax.text(7, 8.5, "Figura 5. DAG — Modelo Causal P04",
            ha="center", fontsize=14, fontweight="bold")
    ax.text(7, 8.1, "IA generativa → Funções Executivas (mediação e moderação)",
            ha="center", fontsize=11, style="italic", color="gray")

    # Variável independente
    add_node(2, 6.5, 2, 0.8, "X: Uso de IA\n(horas/semana)", cor_iv, fontsize=10)

    # Mediação
    add_node(7, 6.5, 2.5, 0.8, "M1: Engajamento\n(atenção, motivação)", cor_med, fontsize=10)
    add_node(7, 4.5, 2.5, 0.8, "M2: Metacognição\n(auto-regulação)", cor_med, fontsize=10)

    # Variável dependente
    add_node(12, 5.5, 2.5, 0.8, "Y: Funções\nExecutivas\n(inibição, flexibilidade)", cor_dv, fontsize=10)

    # Moderador
    add_node(7, 2, 2.5, 0.8, "W: Letramento\nDigital dos Pais", cor_mod, fontsize=10)

    # Controles
    add_node(2, 1.5, 2, 0.8, "C1: Idade, Sexo", cor_ctrl, fontsize=9)
    add_node(12, 1.5, 2, 0.8, "C2: SES, Escola", cor_ctrl, fontsize=9)

    # Setas principais (efeitos causais hipotetizados)
    add_arrow(3, 6.5, 5.8, 6.5, "a1", color=cor_iv)
    add_arrow(3, 6.5, 5.8, 4.5, "a2", color=cor_iv)

    add_arrow(8.2, 6.5, 10.8, 5.8, "b1", color=cor_med)
    add_arrow(8.2, 4.5, 10.8, 5.5, "b2", color=cor_med)
    add_arrow(7, 5.7, 7, 5.3, "", color=cor_med)  # M1 → M2

    # Efeito direto (X → Y)
    add_arrow(3.2, 6.3, 10.6, 5.7, "c'", color=cor_iv)

    # Moderação (W interage com X → M1)
    add_arrow(7, 2.8, 5, 6.0, "W×X", color=cor_mod, lw=1.5)
    add_arrow(7, 2.8, 9, 6.0, "", color=cor_mod, lw=1.5)

    # Controles → IV, DV
    add_arrow(2, 2.3, 2, 5.7, "", color=cor_ctrl, lw=1.5, style="-|>")
    add_arrow(12, 2.3, 12, 4.7, "", color=cor_ctrl, lw=1.5, style="-|>")

    # Legenda
    legend_y = 0.4
    items = [
        ("Independente (X)", cor_iv),
        ("Dependente (Y)", cor_dv),
        ("Mediador (M)", cor_med),
        ("Moderador (W)", cor_mod),
        ("Controle (C)", cor_ctrl),
    ]
    for i, (label, color) in enumerate(items):
        x_pos = 0.5 + i * 2.7
        rect = mpatches.Rectangle((x_pos, legend_y), 0.3, 0.2,
                                  facecolor=color, edgecolor="black")
        ax.add_patch(rect)
        ax.text(x_pos + 0.4, legend_y + 0.1, label, va="center", fontsize=9)

    # Notas
    ax.text(7, 0.1,
            "Efeito indireto: a1*b1 + a2*b2 (mediação serial) | Efeito total: c' + a1*b1 + a2*b2 | Moderação: interação W×X",
            ha="center", fontsize=8, style="italic", color="gray")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Figura salva: {output_path}")


if __name__ == "__main__":
    criar_dag_p04("docs/manuscritos/figuras/figura5_dag_p04.png")
