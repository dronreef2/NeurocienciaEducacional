"""
figura2-heatmap-codigos.py
Gera Figura 2: Heatmap de frequências de códigos
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def criar_heatmap_codigos(output_path: str = "figura2_heatmap_codigos.png"):
    """Heatmap de frequências de códigos por participante (dados do piloto)."""

    codebook = pd.read_csv(
        "/workspace/01-projeto-qualitativo-criancas-ia/dados/piloto/codebook/codebook-piloto.csv"
    )

    codigos = codebook["codigo"].tolist()
    participantes = ["C01 (Maria)", "C02 (Pedro)", "C03 (Júlia)"]

    # Matriz de presença (codificada a partir do codebook)
    matriz = np.array([
        [1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [0, 1, 0],
        [1, 0, 1], [1, 0, 0], [1, 0, 1], [1, 0, 0], [1, 1, 1],
        [1, 1, 1], [1, 1, 0], [1, 1, 1], [0, 1, 0], [1, 0, 0],
        [1, 1, 1], [0, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1],
        [1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 0, 1],
        [1, 0, 0], [1, 1, 0],
    ])

    fig, ax = plt.subplots(figsize=(8, 12))

    im = ax.imshow(matriz, cmap="YlOrRd", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(participantes)))
    ax.set_xticklabels(participantes, rotation=0, fontsize=11)
    ax.set_yticks(range(len(codigos)))
    ax.set_yticklabels(codigos, fontsize=8)

    for i in range(len(codigos)):
        for j in range(len(participantes)):
            text = "✓" if matriz[i, j] == 1 else ""
            ax.text(j, i, text, ha="center", va="center",
                   color="black" if matriz[i, j] == 0 else "white",
                   fontsize=10, fontweight="bold")

    ax.set_title("Figura 2. Heatmap de Códigos por Participante\n(Presença do código na entrevista, N=3, P01 piloto)",
                fontsize=12, fontweight="bold", pad=20)

    cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Presença", rotation=270, labelpad=15)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Figura salva: {output_path}")


if __name__ == "__main__":
    criar_heatmap_codigos("docs/manuscritos/figuras/figura2_heatmap_codigos.png")
