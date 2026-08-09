"""
gerar_dados_sinteticos.py
Gerador de dados sintéticos para TODOS os 5 projetos
Útil para testar pipelines antes da coleta real
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import sys

print("=" * 70)
print("  GERADOR DE DADOS SINTÉTICOS — PROGRAMA COMPLETO")
print("=" * 70)

OUTPUT_DIR = Path("/workspace/dados_sinteticos")
OUTPUT_DIR.mkdir(exist_ok=True)

np.random.seed(42)


# ============================================================
# P01 — Qualitativo (entrevistas + diários)
# ============================================================
def gen_p01(n_children=15, n_days=17):
    print(f"\n[P01] Gerando dados qualitativos ({n_children} crianças, {n_days} dias)...")

    diarios = []
    for cid in range(1, n_children+1):
        n_active = np.random.randint(8, n_days+1)
        active_days = sorted(np.random.choice(n_days, n_active, replace=False))
        for d in active_days:
            data = pd.Timestamp("2026-07-15") + pd.Timedelta(days=d)
            duracao = int(np.random.gamma(2, 10))
            atividades = np.random.choice(
                ["matematica", "leitura", "escrita", "matematica+leitura"],
                p=[0.55, 0.25, 0.10, 0.10]
            )
            dificuldade = np.random.choice(
                ["fracao", "divisao", "multiplicacao", "palavras", "compreensao", ""],
                p=[0.20, 0.15, 0.15, 0.20, 0.15, 0.15]
            )
            diarios.append({
                "data": data.strftime("%Y-%m-%d"),
                "participante_id": f"C{cid:02d}",
                "duracao_min": duracao,
                "atividades": atividades,
                "dificuldades": dificuldade,
                "observacoes": "" if np.random.rand() < 0.5 else "Observação dos pais",
            })

    df_diarios = pd.DataFrame(diarios)
    df_diarios.to_csv(OUTPUT_DIR / "P01_diarios_sinteticos.csv", index=False)
    print(f"  ✓ Diários: {len(df_diarios)} registros")
    return df_diarios

# ============================================================
# P02 — ECR 2x4
# ============================================================
def gen_p02(n_per_cell=50):
    print(f"\n[P02] Gerando ECR 2×4 ({5*n_per_cell} crianças)...")

    data = []
    for cond in ["TRAD", "PONT", "BADG", "NARR", "AVAT"]:
        # Efeitos verdadeiros
        efeito = {"TRAD": 0.0, "PONT": 0.30, "BADG": 0.25, "NARR": 0.55, "AVAT": 0.50}[cond]

        for i in range(n_per_cell):
            baseline = np.random.normal(50, 10)
            change = np.random.normal(efeito, 0.8)
            followup = baseline - change

            data.append({
                "id": f"S_{cond}_{i+1:03d}",
                "condicao": cond,
                "plataforma": "TRAD" if cond == "TRAD" else "GAME",
                "elemento": "NENHUM" if cond == "TRAD" else cond,
                "idade": np.random.randint(7, 12),
                "sexo": np.random.choice(["M", "F"]),
                "ses": round(np.random.normal(0, 1), 2),
                "brief2_baseline": round(baseline, 2),
                "brief2_followup": round(followup, 2),
                "mudanca": round(change, 2),
            })

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "P02_dados_sinteticos.csv", index=False)
    print(f"  ✓ ECR: {len(df)} crianças")
    return df

# ============================================================
# P03 — EEG (sintético com 32 canais)
# ============================================================
def gen_p03(n_subjects=60, n_channels=32, n_samples=500):
    print(f"\n[P03] Gerando EEG ({n_subjects} sujeitos, {n_channels} canais)...")

    channel_names = ["Fp1","Fp2","F3","Fz","F4","C3","Cz","C4","P3","Pz","P4","P7","P8",
                     "PO7","PO8","O1","Oz","O2","T7","T8","TP9","TP10","FT9","FT10",
                     "Fpz","AF7","AF8","F1","F2","P1","P2","POz"][:n_channels]

    for cond in ["papel", "tela"]:
        data_3d = np.random.randn(n_subjects, n_channels, n_samples) * 1e-6
        # Adicionar N170 e P300
        times = np.linspace(-0.2, 0.8, n_samples)
        for s in range(n_subjects):
            for ch in range(n_channels):
                if ch in [13, 14, 15, 17]:  # ROI occipito-temporal
                    if cond == "papel":
                        n170 = -4.0 * np.exp(-((times - 0.17) ** 2) / (2 * 0.025 ** 2))
                    else:
                        n170 = -2.8 * np.exp(-((times - 0.19) ** 2) / (2 * 0.025 ** 2))
                else:
                    n170 = -1.0 * np.exp(-((times - 0.17) ** 2) / (2 * 0.025 ** 2))
                if ch in [8, 9, 10]:  # ROI parietal
                    if cond == "tela":
                        p300 = 6.0 * np.exp(-((times - 0.35) ** 2) / (2 * 0.060 ** 2))
                    else:
                        p300 = 4.5 * np.exp(-((times - 0.35) ** 2) / (2 * 0.060 ** 2))
                else:
                    p300 = 1.5 * np.exp(-((times - 0.35) ** 2) / (2 * 0.060 ** 2))
                data_3d[s, ch] += (n170 + p300) * 1e-6

        # Salvar em formato BIDS-like
        np.save(OUTPUT_DIR / f"P03_eeg_{cond}.npy", data_3d)

    # Salvar metadados
    meta = {
        "n_subjects": n_subjects,
        "n_channels": n_channels,
        "n_samples": n_samples,
        "sfreq": int(n_samples / 1.0),  # 500 Hz em 1 segundo
        "channel_names": channel_names,
        "conditions": ["papel", "tela"],
        "ROIs": {
            "N170": ["PO7", "PO8", "O1", "O2"],
            "P300": ["P3", "Pz", "P4"]
        }
    }
    with open(OUTPUT_DIR / "P03_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  ✓ EEG: {n_subjects} sujeitos × 2 condições")

# ============================================================
# P04 — SEM transversal
# ============================================================
def gen_p04(n=400):
    print(f"\n[P04] Gerando dados SEM transversal (N={n})...")

    # Covariáveis
    idade = np.random.randint(7, 12, n)
    sexo = np.random.choice([0, 1], n)
    ses = np.random.normal(0, 1, n)
    escola = np.random.choice(range(1, 9), n)  # 8 escolas
    letramento_pais = np.random.normal(3, 1, n).clip(1, 5)
    uso_ia = np.random.gamma(2, 2, n).clip(0, 15)  # horas/semana
    engajamento = 0.3 * uso_ia + 0.2 * letramento_pais + 0.1 * ses + np.random.normal(0, 0.7, n)
    fe = 0.10 * uso_ia + 0.45 * engajamento - 0.15 * letramento_pais + 0.3 * ses + np.random.normal(0, 0.5, n)

    # Indicadores
    data = []
    for i in range(n):
        data.append({
            "id": f"S{i+1:04d}",
            "idade": int(idade[i]),
            "sexo": "M" if sexo[i] else "F",
            "ses": round(ses[i], 2),
            "escola": int(escola[i]),
            "letramento_pais": round(letramento_pais[i], 2),
            "uso_ia": round(uso_ia[i], 2),
            "engaj_1": round(engajamento[i] + np.random.normal(0, 0.3), 2),
            "engaj_2": round(engajamento[i] + np.random.normal(0, 0.3), 2),
            "engaj_3": round(engajamento[i] + np.random.normal(0, 0.3), 2),
            "fe_inib_1": round(fe[i] + np.random.normal(0, 0.4), 2),
            "fe_inib_2": round(fe[i] + np.random.normal(0, 0.4), 2),
            "fe_flex_1": round(fe[i] + np.random.normal(0, 0.4), 2),
            "fe_flex_2": round(fe[i] + np.random.normal(0, 0.4), 2),
            "fe_mt_1": round(fe[i] + np.random.normal(0, 0.4), 2),
            "fe_mt_2": round(fe[i] + np.random.normal(0, 0.4), 2),
        })

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "P04_dados_sinteticos.csv", index=False)
    print(f"  ✓ SEM: {len(df)} respondentes")
    return df

# ============================================================
# P05 — Coorte longitudinal
# ============================================================
def gen_p05(n=200, n_waves=5):
    print(f"\n[P05] Gerando dados longitudinais (N={n}, {n_waves} ondas)...")

    data = []
    for cid in range(1, n+1):
        # Variabilidade individual
        intercept = np.random.normal(50, 8)
        slope = np.random.normal(2.5, 1.0)
        cov = np.random.normal(0, 0.3)

        baseline_fe = intercept + np.random.normal(0, 2)

        for t in range(n_waves):
            idade = 7 + t
            fe = intercept + slope * t + np.random.normal(0, 2.5)
            leitura = (50 + 15 * t) + cov * 10 + np.random.normal(0, 5)
            ia_uso = 1 + 0.5 * t + np.random.normal(0, 1)

            data.append({
                "child_id": f"C{cid:04d}",
                "wave": t + 1,
                "idade": idade,
                "brief2_total": round(fe, 2),
                "letramento_palavras_min": max(0, round(leitura, 1)),
                "ia_uso_horas_sem": max(0, round(ia_uso, 2)),
                "sexo": np.random.choice(["M", "F"]),
                "ses": round(np.random.normal(0, 1), 2),
            })

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / "P05_dados_longitudinais_sinteticos.csv", index=False)
    print(f"  ✓ Coorte: {len(df)} observações ({n} crianças × {n_waves} ondas)")
    return df

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print(f"\nGerando dados sintéticos em: {OUTPUT_DIR}\n")

    p01 = gen_p01()
    p02 = gen_p02()
    gen_p03()
    p04 = gen_p04()
    p05 = gen_p05()

    # Sumário
    print("\n" + "=" * 70)
    print("RESUMO DOS DADOS GERADOS")
    print("=" * 70)

    files = [
        ("P01", "P01_diarios_sinteticos.csv", p01),
        ("P02", "P02_dados_sinteticos.csv", p02),
        ("P04", "P04_dados_sinteticos.csv", p04),
        ("P05", "P05_dados_longitudinais_sinteticos.csv", p05),
    ]

    for proj, fname, df in files:
        path = OUTPUT_DIR / fname
        size_kb = path.stat().st_size / 1024
        print(f"  {proj}: {len(df)} linhas, {size_kb:.1f} KB → {path.name}")

    print(f"  P03: EEG numpy arrays (papel + tela) + metadata.json")
    print()
    print("✅ Todos os dados sintéticos gerados com sucesso!")
    print(f"\nPara usar: df = pd.read_csv('{OUTPUT_DIR}/P01_diarios_sinteticos.csv')")
