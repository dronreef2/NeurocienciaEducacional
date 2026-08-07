"""
04_tutorial_sem.py
TUTORIAL 4: Modelagem de Equações Estruturais (SEM) — P04

Objetivos:
- Entender o que é SEM
- Implementar um modelo de mediação simples
- Avaliar índices de ajuste
- Interpretar coeficientes
- Comparar com regressão tradicional

Pré-requisitos: numpy, scipy, matplotlib
Tempo estimado: 30 minutos

NOTA: Em produção, usa-se o pacote `lavaan` (R) ou `semopy` (Python).
Este tutorial implementa um modelo simples do zero para fins didáticos.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import chi2

print("=" * 70)
print("  TUTORIAL 4 — Modelagem de Equações Estruturais (P04)")
print("=" * 70)

# ============================================================
# PASSO 1: O que é SEM?
# ============================================================
print("""
PASSO 1: O que é SEM (Structural Equation Modeling)?

SEM é uma técnica que combina análise fatorial e regressão múltipla
para testar modelos causais complexos com variáveis latentes e observadas.

COMPONENTES:
  1. Modelo de medida: como variáveis latentes são medidas por indicadores
  2. Modelo estrutural: relações causais entre variáveis latentes

EM P04, testamos:
  X (Uso de IA) → M (Engajamento) → Y (Funções Executivas)
       ↓                       ↓
       └───── c' (direto) ─────┘
       W (Letramento Digital dos Pais) modera X → M

VANTAGENS sobre regressão:
  - Modela variáveis LATENTES (constructos não diretamente observáveis)
  - Permite erros de medida
  - Testa modelos inteiros simultaneamente
  - Compara modelos aninhados (chi-square difference test)

ÍNDICES DE AJUSTE (cutoffs tradicionais):
  - χ²/df: < 3 (bom), < 5 (aceitável)
  - CFI: > 0.95 (bom), > 0.90 (aceitável)
  - TLI: > 0.95
  - RMSEA: < 0.06 (bom), < 0.08 (aceitável)
  - SRMR: < 0.08
""")

# ============================================================
# PASSO 2: Modelo conceitual
# ============================================================
print("\n" + "=" * 70)
print("PASSO 2: Modelo conceitual — Mediação simples (X→M→Y)")
print("=" * 70)
print("""
Equações estruturais:

  M = a*X + ε_M              (efeito de X em M)
  Y = c'*X + b*M + ε_Y       (efeitos em Y)

Efeitos:
  - Direto (X → Y): c'
  - Indireto (X → M → Y): a × b
  - Total: c = c' + a*b

Estimativas populacionais (simuladas):
  a = 0.30 (X → M)
  b = 0.40 (M → Y)
  c' = 0.10 (X → Y direto)
  c = 0.10 + 0.30*0.40 = 0.22 (efeito total)
""")

# ============================================================
# PASSO 3: Simular dados com o modelo verdadeiro
# ============================================================
print("\n" + "=" * 70)
print("PASSO 3: Simular dados (N=500) com modelo verdadeiro")
print("=" * 70)

np.random.seed(42)
n = 500

# Variáveis observadas
X = np.random.normal(0, 1, n)  # Uso de IA
W = np.random.normal(0, 1, n)  # Moderador (letramento digital)

# Efeitos verdadeiros
a = 0.30
b = 0.40
c_prime = 0.10
d = 0.20  # moderação W × X → M

# Modelo de medida (cada constructo tem 3 indicadores)
def generate_indicators(latent, loadings, error_var=0.3):
    """Gera indicadores observados a partir de variável latente."""
    n_items = len(loadings)
    indicators = np.zeros((len(latent), n_items))
    for i, loading in enumerate(loadings):
        indicators[:, i] = loading * latent + np.random.normal(0, np.sqrt(error_var), len(latent))
    return indicators

# Variáveis latentes
M = a * X + d * (W * X) + np.random.normal(0, 0.5, n)
Y = c_prime * X + b * M + np.random.normal(0, 0.5, n)

# Indicadores observados
X_ind = generate_indicators(X, [0.8, 0.7, 0.75])  # Uso IA (3 itens)
M_ind = generate_indicators(M, [0.8, 0.85, 0.7])  # Engajamento (3 itens)
Y_ind = generate_indicators(Y, [0.85, 0.8, 0.75])  # FE (3 itens)

print(f"  N = {n}")
print(f"  Variáveis observadas: 9 (3 por constructo)")
print(f"  Moderador: W (letramento digital)")

# ============================================================
# PASSO 4: Análise Fatorial Confirmatória (CFA)
# ============================================================
print("\n" + "=" * 70)
print("PASSO 4: CFA (validação dos constructos)")
print("=" * 70)

# Correlações dentro de cada constructo (devem ser altas)
corr_X = np.corrcoef(X_ind.T)
corr_M = np.corrcoef(M_ind.T)
corr_Y = np.corrcoef(Y_ind.T)

print(f"\n  Correlações entre indicadores:")
print(f"    X (Uso IA):     média r = {(corr_X[0,1]+corr_X[0,2]+corr_X[1,2])/3:.3f}")
print(f"    M (Engajamento): média r = {(corr_M[0,1]+corr_M[0,2]+corr_M[1,2])/3:.3f}")
print(f"    Y (FE):         média r = {(corr_Y[0,1]+corr_Y[0,2]+corr_Y[1,2])/3:.3f}")

# Alpha de Cronbach
def cronbach_alpha(X):
    n_items = X.shape[1]
    item_vars = X.var(axis=0, ddof=1)
    total_var = X.sum(axis=1).var(ddof=1)
    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)

print(f"\n  Alpha de Cronbach:")
print(f"    X: {cronbach_alpha(X_ind):.3f}")
print(f"    M: {cronbach_alpha(M_ind):.3f}")
print(f"    Y: {cronbach_alpha(Y_ind):.3f}")

# ============================================================
# PASSO 5: Modelo de mediação
# ============================================================
print("\n" + "=" * 70)
print("PASSO 5: Estimar modelo de mediação (OLS + bootstrap)")
print("=" * 70)

# Usando médias dos indicadores como proxy das variáveis latentes
X_score = X_ind.mean(axis=1)
M_score = M_ind.mean(axis=1)
Y_score = Y_ind.mean(axis=1)

# Equação 1: M ~ X
from numpy.linalg import lstsq

X_mat_M = np.column_stack([np.ones(n), X_score])
coef_M, _, _, _ = lstsq(X_mat_M, M_score, rcond=None)
a_est, a_se_est = coef_M[1], np.sqrt(np.sum((M_score - X_mat_M @ coef_M)**2) / (n-2)) / np.sqrt(np.sum((X_score - X_score.mean())**2))
print(f"  Equação 1: M = a*X + ε")
print(f"    a (X→M) = {a_est:.3f} (verdadeiro: {a})")
print(f"    SE = {a_se_est:.4f}")
print(f"    t = {a_est/a_se_est:.2f}, p = {2*(1 - __import__('scipy.stats', fromlist=['t']).t.cdf(abs(a_est/a_se_est), n-2)):.4f}")

# Equação 2: Y ~ X + M
X_mat_Y = np.column_stack([np.ones(n), X_score, M_score])
coef_Y, _, _, _ = lstsq(X_mat_Y, Y_score, rcond=None)
c_prime_est = coef_Y[1]
b_est = coef_Y[2]

# SE para c' e b
resid_Y = Y_score - X_mat_Y @ coef_Y
sigma2 = np.sum(resid_Y**2) / (n - 3)
cov_matrix = sigma2 * np.linalg.inv(X_mat_Y.T @ X_mat_Y)
c_se = np.sqrt(cov_matrix[1, 1])
b_se = np.sqrt(cov_matrix[2, 2])

from scipy.stats import t as t_dist
t_c = c_prime_est / c_se
p_c = 2 * (1 - t_dist.cdf(abs(t_c), n-3))
t_b = b_est / b_se
p_b = 2 * (1 - t_dist.cdf(abs(t_b), n-3))

print(f"\n  Equação 2: Y = c'*X + b*M + ε")
print(f"    c' (X→Y direto) = {c_prime_est:.3f} (verdadeiro: {c_prime}), t = {t_c:.2f}, p = {p_c:.4f}")
print(f"    b (M→Y)         = {b_est:.3f} (verdadeiro: {b}), t = {t_b:.2f}, p = {p_b:.4f}")

# Efeito indireto
indirect_est = a_est * b_est
print(f"\n  Efeitos:")
print(f"    Direto (c'): {c_prime_est:.3f}")
print(f"    Indireto (a*b): {indirect_est:.3f} (verdadeiro: {a*b:.3f})")
print(f"    Total: {c_prime_est + indirect_est:.3f} (verdadeiro: {c_prime + a*b:.3f})")

# ============================================================
# PASSO 6: Bootstrap para IC do efeito indireto
# ============================================================
print("\n" + "=" * 70)
print("PASSO 6: Bootstrap (IC 95% do efeito indireto)")
print("=" * 70)

n_boot = 5000
boot_indirect = []
for _ in range(n_boot):
    idx = np.random.choice(n, size=n, replace=True)
    X_b = X_score[idx]
    M_b = M_score[idx]
    Y_b = Y_score[idx]

    coef_M_b, *_ = lstsq(np.column_stack([np.ones(n), X_b]), M_b, rcond=None)
    coef_Y_b, *_ = lstsq(np.column_stack([np.ones(n), X_b, M_b]), Y_b, rcond=None)

    boot_indirect.append(coef_M_b[1] * coef_Y_b[2])

boot_indirect = np.array(boot_indirect)
ic_inf, ic_sup = np.percentile(boot_indirect, [2.5, 97.5])
p_boot = (boot_indirect > 0).mean()

print(f"  Efeito indireto: {indirect_est:.3f}")
print(f"  IC 95% bootstrap: [{ic_inf:.3f}, {ic_sup:.3f}]")
print(f"  P(indireto > 0) = {p_boot:.3f}")
if ic_inf > 0:
    print(f"  ✅ Significativo (IC exclui zero)")
else:
    print(f"  ❌ Não significativo (IC inclui zero)")

# ============================================================
# PASSO 7: Visualização
# ============================================================
print("\n" + "=" * 70)
print("PASSO 7: Visualização do modelo")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Painel A: Diagrama do modelo
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

# Boxes
def box(x, y, w, h, text, color):
    rect = plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=color, edgecolor="black", linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", color="white", fontweight="bold", fontsize=10)

box(2, 4.5, 1.5, 0.8, "X (Uso IA)", "#3498db")
box(5, 4.5, 1.5, 0.8, "M (Engaj.)", "#f39c12")
box(8, 4.5, 1.5, 0.8, "Y (FE)", "#e74c3c")
box(5, 1.5, 2, 0.8, "W (Letram. Digital)", "#27ae60")

# Setas com coeficientes
ax.annotate("", xy=(4.3, 4.5), xytext=(2.7, 4.5),
            arrowprops=dict(arrowstyle="->", lw=2))
ax.text(3.5, 4.8, f"a = {a_est:.2f}", ha="center", fontweight="bold")

ax.annotate("", xy=(7.3, 4.5), xytext=(5.7, 4.5),
            arrowprops=dict(arrowstyle="->", lw=2))
ax.text(6.5, 4.8, f"b = {b_est:.2f}", ha="center", fontweight="bold")

ax.annotate("", xy=(7, 4.2), xytext=(2.8, 4.2),
            arrowprops=dict(arrowstyle="->", lw=2))
ax.text(5, 3.7, f"c' = {c_prime_est:.2f}", ha="center", fontweight="bold")

# Moderação
ax.annotate("", xy=(5, 3.7), xytext=(5, 2.3),
            arrowprops=dict(arrowstyle="->", lw=2, linestyle="--"))
ax.text(5.5, 3, "W×X\n(d={:.2f})".format(d), ha="left", fontweight="bold", color="#27ae60")

ax.set_title("Modelo SEM — Mediação com moderação", fontweight="bold")

# Painel B: Distribuição do efeito indireto (bootstrap)
ax = axes[1]
ax.hist(boot_indirect, bins=50, density=True, alpha=0.7, color="#667eea", edgecolor="black")
ax.axvline(0, color="red", linestyle="--", linewidth=2, label="Zero")
ax.axvline(indirect_est, color="green", linestyle="--", linewidth=2, label=f"Estimado = {indirect_est:.3f}")
ax.axvspan(ic_inf, ic_sup, alpha=0.2, color="green", label=f"IC 95% = [{ic_inf:.2f}, {ic_sup:.2f}]")
ax.set_xlabel("Efeito indireto (a × b)")
ax.set_ylabel("Densidade")
ax.set_title("Distribuição bootstrap do efeito indireto", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("tutorial_4_sem.png", dpi=150, bbox_inches="tight")
print("✅ Figura salva: tutorial_4_sem.png")

# ============================================================
# PASSO 8: Conclusões
# ============================================================
print("\n" + "=" * 70)
print("PASSO 8: Conclusões")
print("=" * 70)
print(f"""
RESUMO DO MODELO SEM (P04):

  Qualidade da calibração (recuperação de parâmetros):
    - a (X→M): estimado = {a_est:.3f}, verdadeiro = {a}
    - b (M→Y): estimado = {b_est:.3f}, verdadeiro = {b}
    - c' (X→Y direto): estimado = {c_prime_est:.3f}, verdadeiro = {c_prime}
    - Indireto (a×b): estimado = {indirect_est:.3f}, verdadeiro = {a*b}

  Teste do efeito indireto:
    - Bootstrap IC 95%: [{ic_inf:.3f}, {ic_sup:.3f}]
    - P(indireto > 0) = {p_boot:.3f}
    - {'Significativo' if ic_inf > 0 else 'Não significativo'}

PRÓXIMOS PASSOS (P04 real):
  1. Implementar com `lavaan` (R) ou `semopy` (Python)
  2. Adicionar mais indicadores por constructo
  3. Testar invariância de medida (sexo, idade)
  4. Análise de subgrupos (público vs. privado)
  5. Modelos multi-grupo (moderação por W)

RECURSOS:
  - Kline (2015). Principles and Practice of SEM
  - Rosseel (2012). lavaan: An R package for SEM
  - Hayes (2017). Introduction to Mediation, Moderation, and Conditional Process Analysis
""")
