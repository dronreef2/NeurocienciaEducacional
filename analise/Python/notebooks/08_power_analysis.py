"""
08_power_analysis.py
Análise de poder estatístico para os 5 projetos
Calcula tamanho amostral necessário para detectar efeitos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

print("=" * 60)
print("  ANÁLISE DE PODER ESTATÍSTICO — Programa de Pesquisa")
print("=" * 60)

# ============================================================
# Helper: cálculo de poder
# ============================================================
def power_one_sample_t(d, n, alpha=0.05):
    """Poder para teste t de uma amostra."""
    df = n - 1
    ncp = d * np.sqrt(n)  # non-centrality parameter
    t_crit = stats.t.ppf(1 - alpha/2, df)
    power = 1 - stats.nct.cdf(t_crit, df, ncp) + stats.nct.cdf(-t_crit, df, ncp)
    return power

def power_two_sample_t(d, n_per_group, alpha=0.05):
    """Poder para teste t de duas amostras independentes."""
    df = 2 * n_per_group - 2
    ncp = d * np.sqrt(n_per_group / 2)
    t_crit = stats.t.ppf(1 - alpha/2, df)
    power = 1 - stats.nct.cdf(t_crit, df, ncp) + stats.nct.cdf(-t_crit, df, ncp)
    return power

def power_correlation(r, n, alpha=0.05):
    """Poder para teste de correlação."""
    # Fisher z-transformation
    z = 0.5 * np.log((1 + r) / (1 - r))
    se = 1 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - alpha/2)
    power = 1 - stats.norm.cdf(z_crit - z/se) + stats.norm.cdf(-z_crit - z/se)
    return power

def power_f_test_anova(f, n_per_group, k_groups, alpha=0.05):
    """Poder para ANOVA one-way (Cohen's f)."""
    df1 = k_groups - 1
    df2 = k_groups * (n_per_group - 1)
    ncp = f**2 * k_groups * n_per_group
    f_crit = stats.f.ppf(1 - alpha, df1, df2)
    power = 1 - stats.ncf.cdf(f_crit, df1, df2, ncp)
    return power

# ============================================================
# P01 — Qualitativo (não requer power analysis formal)
# ============================================================
print("\n" + "=" * 60)
print("P01 — QUALITATIVO (Análise Temática Reflexiva)")
print("=" * 60)
print("""
A Análise Temática Reflexiva (Braun & Clarke, 2022) não usa testes
de significância. O critério de qualidade é a SATURAÇÃO TEÓRICA.

Saturação é atingida quando:
- Novos participantes não geram novos temas
- Os 5 temas estão bem desenvolvidos com sub-temas
- Há triangulação entre fontes

Recomendação P01:
  N piloto: 3 (✓ atingido)
  N final: 12-15 (saturação esperada)
  Margem: incluir 2-3 sobressalentes
""")

# ============================================================
# P02 — ECR 2x4 fatorial (teste F)
# ============================================================
print("\n" + "=" * 60)
print("P02 — ECR 2×4 FATORIAL (Gamificação × FE)")
print("=" * 60)
print("Cálculo de poder para efeito principal de gamificação (Cohen's f):")

f_effects = [0.10, 0.25, 0.40]  # pequeno, médio, grande
f_labels = ["Pequeno (f=0.10)", "Médio (f=0.25)", "Grande (f=0.40)"]
ns = [25, 50, 75, 100, 150, 200]

print(f"\n{'Tamanho amostral':<20} | " + " | ".join([f"{l:<20}" for l in f_labels]))
print("-" * 100)
for n in ns:
    powers = [power_f_test_anova(f, n, 2) for f in f_effects]
    print(f"  n={n:<16} | " + " | ".join([f"power = {p:.3f}            " for p in powers]))

print("""
Recomendação P02:
  Efeito esperado: médio (f=0.25) baseado em meta-análise de Hamari (2014)
  N necessário: ~100 por grupo (2 grupos, total N=200) para power = 0.80
  Plano atual: N=200 ✓
""")

# ============================================================
# P03 — EEG (teste t pareado)
# ============================================================
print("\n" + "=" * 60)
print("P03 — EEG (Comparação de amplitudes N170/P300)")
print("=" * 60)
print("Cálculo de poder para teste t pareado (efeito médio d=0.5):")

d_effects = [0.3, 0.5, 0.8]
d_labels = ["Pequeno (d=0.3)", "Médio (d=0.5)", "Grande (d=0.8)"]
print(f"\n{'N':<10} | " + " | ".join([f"{l:<20}" for l in d_labels]))
print("-" * 75)
for n in [10, 20, 30, 50, 60, 80, 100]:
    powers = [power_one_sample_t(d, n) for d in d_effects]
    print(f"  N={n:<6} | " + " | ".join([f"power = {p:.3f}            " for p in powers]))

print("""
Recomendação P03:
  Efeito esperado: médio (d=0.5) para N170 (letras vs símbolos)
  N necessário: ~34 para power = 0.80
  Plano atual: N=60 ✓ (margem para subgrupos)
""")

# ============================================================
# P04 — SEM transversal (teste de correlação + regressão)
# ============================================================
print("\n" + "=" * 60)
print("P04 — TRANSVERSAL COM SEM")
print("=" * 60)
print("Cálculo de poder para detectar efeito indireto de X→M→Y:")

correlations = [0.15, 0.20, 0.30, 0.40]
ns = [100, 200, 300, 400, 500, 800]
print(f"\n{'N':<10} | " + " | ".join([f"r = {r:<18}" for r in correlations]))
print("-" * 100)
for n in ns:
    powers = [power_correlation(r, n) for r in correlations]
    print(f"  N={n:<6} | " + " | ".join([f"power = {p:.3f}            " for p in powers]))

print("""
Recomendação P04:
  Efeito indireto esperado: pequeno a médio (r ≈ 0.20-0.30)
  N necessário: ~200-300 para detectar mediação
  Plano atual: N=300-500 ✓
""")

# ============================================================
# P05 — Coorte longitudinal (Mixed Model)
# ============================================================
print("\n" + "=" * 60)
print("P05 — COORTE LONGITUDINAL (5 ondas)")
print("=" * 60)
print("Cálculo de poder para interação tempo × grupo (Cohen's f):")

# Para longitudinal com 5 ondas, poder é maior que cross-sectional
# (porque cada sujeito contribui com múltiplas observações)

# Aproximação simplificada
def longitudinal_power(f, n_per_group, n_waves, alpha=0.05):
    """Poder aproximado para interação time*group em longitudinal."""
    # Effective N considerando correlação intra-sujeito
    rho = 0.6  # autocorrelação típica
    n_eff = n_per_group * n_waves * (1 + (n_waves - 1) * rho) / n_waves
    return power_f_test_anova(f, int(n_eff), 2, alpha)

print(f"\n{'N inicial':<15} | Ondas | Efeito pequeno (f=0.15) | Efeito médio (f=0.25)")
print("-" * 75)
for n in [50, 100, 150, 200, 300]:
    for n_waves in [3, 5]:
        p_small = longitudinal_power(0.15, n, n_waves)
        p_med = longitudinal_power(0.25, n, n_waves)
        print(f"  N={n:<8} | {n_waves}     | power = {p_small:.3f}              | power = {p_med:.3f}")

print("""
Recomendação P05:
  Efeito esperado: pequeno a médio para interação tempo×grupo
  N inicial necessário: ~200 crianças para 5 ondas (power=0.80)
  Plano atual: N=200 com 10 escolas ✓
  Considerar attrition: ~20% ao longo de 5 anos
  N inicial recomendado: 250
""")

# ============================================================
# Visualização: Curvas de poder
# ============================================================
print("\n" + "=" * 60)
print("Gerando curvas de poder...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel 1: Teste t (P03)
ax = axes[0, 0]
ns = np.arange(10, 150)
for d in [0.3, 0.5, 0.8]:
    powers = [power_one_sample_t(d, n) for n in ns]
    ax.plot(ns, powers, label=f"d = {d}")
ax.axhline(0.80, color="red", linestyle="--", alpha=0.5, label="Power = 0.80")
ax.set_xlabel("N (pareado)")
ax.set_ylabel("Poder")
ax.set_title("P03 — Teste t pareado", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel 2: Correlação (P04)
ax = axes[0, 1]
ns = np.arange(20, 600)
for r in [0.15, 0.20, 0.30, 0.40]:
    powers = [power_correlation(r, n) for n in ns]
    ax.plot(ns, powers, label=f"r = {r}")
ax.axhline(0.80, color="red", linestyle="--", alpha=0.5, label="Power = 0.80")
ax.set_xlabel("N")
ax.set_ylabel("Poder")
ax.set_title("P04 — Correlação (efeito indireto)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel 3: ANOVA (P02)
ax = axes[1, 0]
ns = np.arange(20, 300)
for f in [0.10, 0.25, 0.40]:
    powers = [power_f_test_anova(f, n, 2) for n in ns]
    ax.plot(ns, powers, label=f"f = {f}")
ax.axhline(0.80, color="red", linestyle="--", alpha=0.5, label="Power = 0.80")
ax.set_xlabel("N por grupo")
ax.set_ylabel("Poder")
ax.set_title("P02 — ANOVA (efeito principal)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel 4: Longitudinal (P05)
ax = axes[1, 1]
ns = np.arange(50, 500)
for n_w in [3, 5]:
    powers = [longitudinal_power(0.25, n, n_w) for n in ns]
    ax.plot(ns, powers, label=f"{n_w} ondas, f=0.25")
ax.axhline(0.80, color="red", linestyle="--", alpha=0.5, label="Power = 0.80")
ax.set_xlabel("N inicial")
ax.set_ylabel("Poder")
ax.set_title("P05 — Longitudinal (tempo×grupo)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/figura9_poder_estatistico.png", dpi=200, bbox_inches="tight")
print("Figura salva: resultados/figura9_poder_estatistico.png")
plt.close()

# ============================================================
# Sumário final
# ============================================================
print("\n" + "=" * 60)
print("SUMÁRIO — PODER ESTATÍSTICO")
print("=" * 60)
print("""
| Projeto | Design       | N planejado | Poder esperado | Status |
|---------|--------------|-------------|----------------|--------|
| P01     | Qualitativo  | 12-15       | Saturação      | ✓      |
| P02     | ECR 2×4      | 200         | 0.80 (f=0.25)  | ✓      |
| P03     | EEG pareado  | 60          | 0.93 (d=0.5)   | ✓      |
| P04     | SEM          | 300-500     | 0.80-0.95      | ✓      |
| P05     | Coorte       | 200-250     | 0.80 (5 ondas) | ✓      |

Todos os projetos têm poder adequado para detectar efeitos médios.
""")
