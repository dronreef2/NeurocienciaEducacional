"""
figura4-timeline.py
Gera Figura 4: Timeline do estudo piloto
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def criar_timeline(output_path: str = "figura4_timeline.png"):
    """Timeline visual do estudo piloto P01."""
    fig, ax = plt.subplots(figsize=(14, 5))

    meses = ["M1\n(Jan)", "M2\n(Fev)", "M3\n(Mar)", "M4\n(Abr)", "M5\n(Mai)",
            "M6\n(Jun)", "M7\n(Jul)", "M8\n(Ago)", "M9\n(Set)"]
    x = list(range(len(meses)))

    atividades = [
        ("Submissão CEP", 0, 1, "#3498db"),
        ("Aprovação + recrutamento", 1, 2, "#3498db"),
        ("Coleta T0 (baseline)", 2, 3, "#27ae60"),
        ("Período de uso (8 sem)", 3, 5, "#f39c12"),
        ("Coleta T1 (entrevistas)", 5, 6, "#27ae60"),
        ("Transcrição + codificação", 6, 7, "#9b59b6"),
        ("Análise Temática", 7, 8, "#9b59b6"),
        ("Manuscrito + submissão", 8, 9, "#e74c3c"),
    ]

    for i, (nome, start, end, color) in enumerate(atividades):
        ax.barh(i, end - start, left=start, height=0.6,
                color=color, alpha=0.8, edgecolor="black", linewidth=1)
        ax.text((start + end) / 2, i, nome, ha="center", va="center",
                color="white", fontweight="bold", fontsize=9)

    ax.set_yticks(range(len(atividades)))
    ax.set_yticklabels([a[0] for a in atividades], fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(meses, fontsize=10)
    ax.set_xlim(-0.3, len(meses) - 0.7)
    ax.set_ylim(-0.5, len(atividades) - 0.5)
    ax.invert_yaxis()
    ax.set_xlabel("Meses do Programa", fontsize=11)
    ax.set_title("Figura 4. Timeline do Estudo Piloto (P01)\nM0-M9 (2026)",
                fontsize=13, fontweight="bold", pad=15)
    ax.grid(True, axis="x", alpha=0.3)

    legend_items = [
        mpatches.Patch(color="#3498db", label="Ética"),
        mpatches.Patch(color="#27ae60", label="Coleta de dados"),
        mpatches.Patch(color="#f39c12", label="Intervenção"),
        mpatches.Patch(color="#9b59b6", label="Análise"),
        mpatches.Patch(color="#e74c3c", label="Manuscrito"),
    ]
    ax.legend(handles=legend_items, loc="upper center",
              bbox_to_anchor=(0.5, -0.15), ncol=5, fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Figura salva: {output_path}")


if __name__ == "__main__":
    criar_timeline("docs/manuscritos/figuras/figura4_timeline.png")
