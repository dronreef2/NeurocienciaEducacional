"""
03_tutorial_irt.py
TUTORIAL 3: Item Response Theory (IRT) — P05

Objetivos:
- Entender o que é IRT e por que usar
- Implementar modelo de Rasch (1PL)
- Calibrar itens e estimar habilidades
- Visualizar Curva Característica do Item (ICC)
- Construir Wright Map

Pré-requisitos: numpy, scipy, matplotlib
Tempo estimado: 30 minutos

Aplicação em P05:
- Calibração dos itens do BRIEF-2
- Avaliação de equidade dos itens (DIF)
- Construção de testes adaptativos computadorizados
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm

print("=" * 70)
print("  TUTORIAL 3 — Item Response Theory (P05)")
print("=" * 70)

# ============================================================
# PASSO 1: O que é IRT?
# ============================================================
print("""
PASSO 1: O que é IRT (Item Response Theory)?

Diferente da Teoria Clássica dos Testes (TCT), que usa escores brutos,
IRT modela a probabilidade de ACERTO de cada item em função da
HABILIDADE (θ) do respondente.

MODELO DE RASCH (1PL — 1 Parâmetro Logístico):

  P(X=1 | θ, b) = 1 / (1 + exp(-(θ - b)))

Onde:
  θ = habilidade do respondente (latente, N(0,1) por convenção)
  b = dificuldade do item (1 parâmetro)

VANTAGENS sobre TCT:
  - Habilidade do respondente independente do conjunto de itens
  - Dificuldade do item independente da amostra
  - Permite Computerized Adaptive Testing (CAT)
  - Avalia DIF (Differential Item Functioning) — equidade
  - Maior precisão na medida de habilidades extremas

APLICAÇÕES EM P05:
  - Calibrar itens do BRIEF-2 (pais + professores)
  - Construir escala de letramento computadorizada
  - Triagem precoce de dificuldades (com IRT + EEG)
""")

# ============================================================
# PASSO 2: Simular dados
# ============================================================
print("\n" + "=" * 70)
print("PASSO 2: Simular respostas a um teste (300 pessoas, 20 itens)")
print("=" * 70)

np.random.seed(42)
n_subjects = 300
n_items = 20

# Habilidade real (latente)
theta_true = np.random.normal(0, 1, n_subjects)

# Dificuldade dos itens (variando de fácil a difícil)
b_true = np.linspace(-2, 2, n_items) + np.random.normal(0, 0.2, n_items)

# Modelo de Rasch
prob_matrix = 1 / (1 + np.exp(-(theta_true[:, None] - b_true[None, :])))
responses = (np.random.rand(n_subjects, n_items) < prob_matrix).astype(int)

print(f"  N sujeitos: {n_subjects}")
print(f"  N itens: {n_items}")
print(f"  Proporção média de acertos: {responses.mean():.3f}")
print(f"  Range de b (verdadeiro): [{b_true.min():.2f}, {b_true.max():.2f}]")

# ============================================================
# PASSO 3: Estatísticas clássicas por item (baseline)
# ============================================================
print("\n" + "=" * 70)
print("PASSO 3: Estatísticas clássicas por item")
print("=" * 70)

print(f"\n{'Item':<8} | {'P':<6} | {'rpb':<8} | {'b IRT':<8} | {'classif'}")
print("-" * 60)

total_score = responses.sum(axis=1)
for i in range(n_items):
    p = responses[:, i].mean()
    rpb = np.corrcoef(responses[:, i], total_score)[0, 1]

    if p > 0.85:
        classif = "muito fácil"
    elif p > 0.65:
        classif = "fácil"
    elif p > 0.35:
        classif = "médio"
    elif p > 0.15:
        classif = "difícil"
    else:
        classif = "muito difícil"

    print(f"  {i+1:02d}   | {p:.2f}  | {rpb:.2f}   | {b_true[i]:.2f}   | {classif}")

# ============================================================
# PASSO 4: Calibração IRT (Rasch 1PL)
# ============================================================
print("\n" + "=" * 70)
print("PASSO 4: Calibração IRT (Joint MLE)")
print("=" * 70)

def neg_log_likelihood_rasch(params, X):
    """NLL vetorizado para Rasch 1PL."""
    n_subj, n_item = X.shape
    theta_est = params[:n_subj]
    b_est = params[n_subj:]

    z = theta_est[:, None] - b_est[None, :]
    p = 1 / (1 + np.exp(-z))
    p = np.clip(p, 1e-10, 1-1e-10)

    nll = -np.sum(X * np.log(p) + (1 - X) * np.log(1 - p))
    return nll

# Inicialização
theta_init = (responses.mean(axis=1) - 0.5) * 2
b_init = -(responses.mean(axis=0) - 0.5) * 2
params_init = np.concatenate([theta_init, b_init])
params_init[n_subjects:] -= params_init[n_subjects:].mean()  # identificação

# Otimização
result = minimize(
    neg_log_likelihood_rasch,
    params_init,
    args=(responses,),
    method="L-BFGS-B",
    options={"maxiter": 100, "disp": False}
)

theta_est = result.x[:n_subjects]
b_est = result.x[n_subjects:]
b_est -= b_est.mean()  # identificação

print(f"  Convergência: {'OK' if result.success else 'FALHOU'}")
print(f"  NLL final: {result.fun:.2f}")

# Avaliação
r_theta = np.corrcoef(theta_est, theta_true)[0, 1]
r_b = np.corrcoef(b_est, b_true)[0, 1]
rmse_theta = np.sqrt(((theta_est - theta_true) ** 2).mean())
rmse_b = np.sqrt(((b_est - b_true) ** 2).mean())

print(f"\n  Qualidade da calibração:")
print(f"    Correlação θ estimado vs verdadeiro: r = {r_theta:.3f}")
print(f"    Correlação b estimado vs verdadeiro: r = {r_b:.3f}")
print(f"    RMSE θ: {rmse_theta:.3f}")
print(f"    RMSE b: {rmse_b:.3f}")

# ============================================================
# PASSO 5: Item fit statistics
# ============================================================
print("\n" + "=" * 70)
print("PASSO 5: Item fit (Infit e Outfit)")
print("=" * 70)

print(f"\n{'Item':<6} | {'b est':<8} | {'Infit':<8} | {'Outfit':<8} | {'Interpretação'}")
print("-" * 70)

n_problemas = 0
for i in range(n_items):
    p_pred = 1 / (1 + np.exp(-(theta_est - b_est[i])))
    residuals = (responses[:, i] - p_pred) / np.sqrt(p_pred * (1 - p_pred))

    # Infit (informado)
    infit = (residuals ** 2).mean()
    # Outfit (não-informado, sensível a outliers)
    outfit = ((residuals ** 2) * (residuals ** 2)).mean() ** 0.5  # approx

    flag = ""
    if infit > 1.5 or infit < 0.5:
        flag = " ⚠️ misfit"
        n_problemas += 1
    elif outfit > 2.0:
        flag = " ⚠️ outlier"
        n_problemas += 1

    print(f"  {i+1:02d}   | {b_est[i]:.2f}    | {infit:.2f}     | {outfit:.2f}     | {flag or 'OK'}")

print(f"\n  Itens com problema: {n_problemas}/{n_items}")

# ============================================================
# PASSO 6: Visualizar ICCs e Wright Map
# ============================================================
print("\n" + "=" * 70)
print("PASSO 6: Visualizações (ICC + Wright Map)")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Painel A: ICCs de 5 itens representativos
ax = axes[0]
theta_grid = np.linspace(-3, 3, 100)
for i in [0, 5, 9, 14, 19]:
    p_grid = 1 / (1 + np.exp(-(theta_grid - b_est[i])))
    label = f"Item {i+1} (b={b_est[i]:.2f})"
    ax.plot(theta_grid, p_grid, linewidth=2, label=label)

ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_xlabel("Habilidade (θ)", fontsize=11)
ax.set_ylabel("P(acerto)", fontsize=11)
ax.set_title("Curva Característica do Item (ICC)\n5 itens representativos",
             fontweight="bold")
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

# Painel B: Wright Map (item-person map)
ax = axes[1]
all_values = np.concatenate([theta_est, b_est])
v_min, v_max = all_values.min() - 0.5, all_values.max() + 0.5

# Pessoas (esquerda)
ax.scatter(np.random.normal(-0.4, 0.08, len(theta_est)), theta_est,
           s=15, alpha=0.4, color="steelblue", label="Pessoas")
# Itens (direita)
ax.scatter(np.random.normal(0.4, 0.03, len(b_est)), b_est,
           s=80, alpha=0.9, color="coral", marker="s", label="Itens")

# Nomes dos itens
for i in range(n_items):
    if i % 3 == 0:  # mostrar 1 a cada 3 para não poluir
        ax.text(0.55, b_est[i], f"i{i+1}", va="center", fontsize=7, color="coral")

ax.axvline(0, color="black", linewidth=1)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(v_min, v_max)
ax.set_yticks(np.arange(-3, 4, 1))
ax.set_xticks([])
ax.set_ylabel("Habilidade (θ) e Dificuldade (b)", fontsize=11)
ax.set_title("Wright Map (Item-Person Map)", fontweight="bold")
ax.legend(loc="upper right")

# Interpretação
ax.text(0.7, v_max - 0.5, "Itens MUITO difíceis\n(medem alta habilidade)",
        fontsize=8, ha="center", style="italic", color="coral")
ax.text(0.7, v_min + 0.5, "Itens MUITO fáceis\n(medem baixa habilidade)",
        fontsize=8, ha="center", style="italic", color="coral")
ax.text(-0.7, v_max - 0.5, "Pessoas com\nalta habilidade",
        fontsize=8, ha="center", style="italic", color="steelblue")
ax.text(-0.7, v_min + 0.5, "Pessoas com\nbaixa habilidade",
        fontsize=8, ha="center", style="italic", color="steelblue")

plt.tight_layout()
plt.savefig("tutorial_3_irt.png", dpi=150, bbox_inches="tight")
print("✅ Figura salva: tutorial_3_irt.png")

# ============================================================
# PASSO 7: Reliability (Person Separation Index)
# ============================================================
print("\n" + "=" * 70)
print("PASSO 7: Confiabilidade (Person Separation Index)")
print("=" * 70)

# Variância de theta ajustado
theta_adjusted = theta_est - b_est.mean()
sd_theta = theta_est.std()
se_theta = 1.0  # erro padrão aproximado

# Person Separation Index (similar to KR-20)
psi = sd_theta / np.sqrt(sd_theta**2 + se_theta**2)
reliability = (sd_theta**2 - se_theta**2) / sd_theta**2
n_strata = (4 * psi + 1) / 3

print(f"  Desvio-padrão de θ: {sd_theta:.2f}")
print(f"  Erro padrão médio: {se_theta:.2f}")
print(f"  Person Separation Index: {psi:.2f}")
print(f"  Confiabilidade: {reliability:.2f}")
print(f"  Níveis distinguíveis: ~{n_strata:.0f}")

# ============================================================
# PASSO 8: Conclusões
# ============================================================
print("\n" + "=" * 70)
print("PASSO 8: Conclusões")
print("=" * 70)
print(f"""
RESUMO DA CALIBRAÇÃO IRT:

  Qualidade da calibração:
    - Correlação θ: r = {r_theta:.3f}
    - Correlação b: r = {r_b:.3f}
    - {n_problemas} de {n_items} itens com misfit

  Aplicações para P05:
    1. Calibração dos itens do BRIEF-2
    2. Avaliação de DIF por sexo e SES
    3. Construção de CAT (Computerized Adaptive Test)
    4. Triagem precoce de crianças em risco

  Próximos passos:
    - Modelo 2PL (discriminação variável)
    - Bayesian IRT com priors informativos
    - Credit partial model para itens Likert
""")
