"""
figura3-mapa-temas.py
Gera Figura 3: Mapa de temas e sub-temas
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


def criar_mapa_temas(output_path: str = "figura3_mapa_temas.png"):
    """Mapa de temas (network diagram) do piloto P01."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-5, 5)
    ax.axis("off")

    cores = {
        "Antropomorfização": "#e74c3c",
        "Detecção de Erro": "#3498db",
        "Confiança Calibrada": "#27ae60",
        "Comparação Humana": "#9b59b6",
        "Preferência Contextual": "#f39c12"
    }

    temas_pos = {
        "Antropomorfização": (0, 3.5),
        "Detecção de Erro": (-3.5, 0),
        "Confiança Calibrada": (3.5, 0),
        "Comparação Humana": (-2.5, -3),
        "Preferência Contextual": (2.5, -3),
    }

    sub_temas = {
        "Antropomorfização": ["Usa pronomes humanos", "Atribui inteligência", "Reconhece como robô"],
        "Detecção de Erro": ["Erro imediato", "Erro diferido", "Corrige o tutor", "Reporta a humano"],
        "Confiança Calibrada": ["Alta confiança", "Baixa confiança", "Verifica resposta"],
        "Comparação Humana": ["Compara com professor", "Compara com família", "Atribui amizade"],
        "Preferência Contextual": ["Prefere professor em cansaço", "Prefere humano em leitura", "Combina IA + humano"]
    }

    for tema, (x, y) in temas_pos.items():
        circle = Circle((x, y), 0.9, facecolor=cores[tema], edgecolor="black",
                       linewidth=2, alpha=0.85)
        ax.add_patch(circle)
        ax.text(x, y, tema, ha="center", va="center", fontsize=11,
                fontweight="bold", color="white", wrap=True)

        subs = sub_temas[tema]
        for i, sub in enumerate(subs):
            angle = 2 * np.pi * i / len(subs)
            r = 1.8
            sub_x = x + r * np.cos(angle + np.pi/4 + (i * 0.3))
            sub_y = y + r * np.sin(angle + np.pi/4 + (i * 0.3))

            sub_circle = Circle((sub_x, sub_y), 0.35, facecolor=cores[tema],
                              edgecolor="gray", linewidth=1, alpha=0.4)
            ax.add_patch(sub_circle)
            ax.text(sub_x, sub_y, sub, ha="center", va="center",
                    fontsize=7, wrap=True)

            ax.plot([x, sub_x], [y, sub_y], color="gray", alpha=0.4, linewidth=1, zorder=0)

    ax.text(0, 4.5, "Figura 3. Mapa de Temas e Sub-Temas Emergentes\n(Análise Temática Reflexiva, P01 piloto, N=3)",
            ha="center", fontsize=13, fontweight="bold")

    ax.text(-5.5, -4.5, "Cada tema (círculo grande) agrupa sub-temas (círculos pequenos) identificados nas 3 entrevistas.\nTamanho e cor não codificam frequência (apenas agrupamento temático).",
            ha="left", fontsize=8, style="italic", color="gray")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Figura salva: {output_path}")


if __name__ == "__main__":
    criar_mapa_temas("docs/manuscritos/figuras/figura3_mapa_temas.png")
