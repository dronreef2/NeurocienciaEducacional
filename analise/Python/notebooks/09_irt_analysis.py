"""
09_irt_analysis.py
Item Response Theory (IRT) — P05
Análise de itens de testes cognitivos com modelo de Rasch
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm

print("=" * 60)
print("  ITEM RESPONSE THEORY (IRT) — Modelo de Rasch 1PL")
print("=" * 60)

# ============================================================
# 1. Simular respostas a um teste de FE
# ============================================================
print("\n1. Simulando respostas a teste de 20 itens (N=300 crianças)...")

np.random.seed(42)
n_subjects = 300
n_items = 20

# Habilidade (theta) dos sujeitos: N(0, 1)
theta = np.random.normal(0, 1, n_subjects)

# Dificuldade (b) dos itens: ~N(0, 1.5)
b = np.random.normal(0, 1.5, n_items)

# Modelo de Rasch: P(X=1|theta, b) = 1 / (1 + exp(-(theta - b)))
prob_matrix = 1 / (1 + np.exp(-(theta[:, None] - b[None, :])))

# Simular respostas
responses = (np.random.rand(n_subjects, n_items) < prob_matrix).astype(int)

df = pd.DataFrame(responses, columns=[f"item_{i+1:02d}" for i in range(n_items)])
df.insert(0, "subject_id", [f"S{i+1:03d}" for i in range(n_subjects)])
df.insert(1, "theta_true", theta)

print(f"  N sujeitos: {n_subjects}")
print(f"  N itens: {n_items}")
print(f"  Total respostas: {n_subjects * n_items}")
print(f"  Proporção de acertos: {responses.mean():.3f}")

# ============================================================
# 2. Estatísticas por item
# ============================================================
print("\n2. Estatísticas por item:")
print(f"{'Item':<10} | {'Prop. acerto':<12} | {'Correlação item-total':<22} | {'b (verdadeiro)':<15}")
print("-" * 70)
for i in range(n_items):
    p_val = responses[:, i].mean()
    # Correlação bisserial pontual
    total = responses.sum(axis=1)
    rpb = np.corrcoef(responses[:, i], total)[0, 1]
    print(f"  item_{i+1:02d} | {p_val:<12.3f} | {rpb:<22.3f} | {b[i]:<15.3f}")

# ============================================================
# 3. Calibração dos itens (Joint Maximum Likelihood)
# ============================================================
print("\n3. Calibrando itens (estimando b e theta)...")

def neg_log_likelihood_rasch(params, X, n_iter=10):
    """NLL para modelo de Rasch, alternando entre b e theta. Vetorizado."""
    n_subj, n_item = X.shape
    theta_est = params[:n_subj]
    b_est = params[n_subj:]

    # Matriz de probabilidades (n_subj x n_item)
    z = theta_est[:, None] - b_est[None, :]
    p = 1 / (1 + np.exp(-z))
    p = np.clip(p, 1e-10, 1-1e-10)

    # NLL vetorizado
    nll = -np.sum(X * np.log(p) + (1 - X) * np.log(1 - p))
    return nll

# Inicialização
theta_init = (responses.mean(axis=1) - 0.5) * 2
b_init = -(responses.mean(axis=0) - 0.5) * 2

# Identificação: theta_médio = 0
params_init = np.concatenate([theta_init, b_init])
params_init[n_subjects:] -= params_init[n_subjects:].mean()

# Otimização (Joint MLE)
result = minimize(
    neg_log_likelihood_rasch,
    params_init,
    args=(responses,),
    method="L-BFGS-B",
    options={"maxiter": 100, "disp": False}
)

theta_est = result.x[:n_subjects]
b_est = result.x[n_subjects:]
b_est -= b_est.mean()  # Identificação

print(f"  Convergência: {'OK' if result.success else 'FALHOU'}")
print(f"  NLL final: {result.fun:.2f}")

# ============================================================
# 4. Avaliação do ajuste
# ============================================================
print("\n4. Avaliação do ajuste:")

# Correlação entre theta estimado e verdadeiro
r_theta = np.corrcoef(theta_est, theta)[0, 1]
print(f"  Correlação theta estimado vs verdadeiro: r = {r_theta:.3f}")

# Correlação entre b estimado e verdadeiro
r_b = np.corrcoef(b_est, b)[0, 1]
print(f"  Correlação b estimado vs verdadeiro: r = {r_b:.3f}")

# RMSE
rmse_theta = np.sqrt(((theta_est - theta) ** 2).mean())
rmse_b = np.sqrt(((b_est - b) ** 2).mean())
print(f"  RMSE theta: {rmse_theta:.3f}")
print(f"  RMSE b: {rmse_b:.3f}")

# Infit e Outfit (item fit statistics)
print("\n  Item fit (Outfit mean-square):")
print(f"  {'Item':<10} | {'b estimado':<12} | {'Outfit':<10}")
print("  " + "-" * 40)
for i in range(n_items):
    p_pred = 1 / (1 + np.exp(-(theta_est - b_est[i])))
    residuals = (responses[:, i] - p_pred) / np.sqrt(p_pred * (1 - p_pred))
    outfit = (residuals ** 2).mean()

    flag = " ⚠️" if outfit > 1.5 or outfit < 0.5 else ""
    print(f"  item_{i+1:02d}   | {b_est[i]:<12.3f} | {outfit:<10.3f}{flag}")

# ============================================================
# 5. Curva característica do item (ICC) para 4 itens
# ============================================================
print("\n5. Gerando Curva Característica do Item (ICC)...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Painel A: ICCs
ax = axes[0]
theta_grid = np.linspace(-3, 3, 100)
for i in [0, 4, 9, 14]:
    p_grid = 1 / (1 + np.exp(-(theta_grid - b_est[i])))
    ax.plot(theta_grid, p_grid, label=f"Item {i+1} (b={b_est[i]:.2f})", linewidth=2)

ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
ax.set_xlabel("Habilidade (θ)")
ax.set_ylabel("P(acerto)")
ax.set_title("Curva Característica do Item (ICC)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel B: Distribuição de theta e b
ax = axes[1]
ax.hist(theta_est, bins=30, alpha=0.6, label="θ estimado (sujeitos)", color="steelblue", edgecolor="black")
ax.hist(b_est, bins=15, alpha=0.6, label="b estimado (itens)", color="coral", edgecolor="black")
ax.set_xlabel("Valor estimado")
ax.set_ylabel("Frequência")
ax.set_title("Distribuição de θ e b", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/figura10_irt_rasch.png", dpi=200, bbox_inches="tight")
print("  Figura 10 salva: resultados/figura10_irt_rasch.png")
plt.close()

# ============================================================
# 6. Wright Map (mapa de itens-pessoas)
# ============================================================
print("\n6. Gerando Wright Map (item-person map)...")

fig, ax = plt.subplots(figsize=(10, 8))

# Eixo vertical: habilidade
all_values = np.concatenate([theta_est, b_est])
v_min, v_max = all_values.min() - 0.5, all_values.max() + 0.5

# Pessoas (lado esquerdo)
ax.scatter(np.random.normal(-0.3, 0.05, len(theta_est)), theta_est,
           s=30, alpha=0.5, color="steelblue", label="Pessoas")

# Itens (lado direito)
ax.scatter(np.random.normal(0.3, 0.02, len(b_est)), b_est,
           s=80, alpha=0.8, color="coral", marker="s", label="Itens")

# Adicionar nomes dos itens
for i in range(n_items):
    ax.text(0.5, b_est[i], f"  item {i+1}", va="center", fontsize=8)

# Eixo central
ax.axvline(0, color="black", linewidth=1)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(v_min, v_max)
ax.set_yticks(np.arange(-3, 4, 1))
ax.set_xticks([])
ax.set_ylabel("Habilidade (θ) | Dificuldade (b)")
ax.set_title("Wright Map (Item-Person Map)", fontweight="bold")
ax.legend(loc="upper right")

# Adicionar interpretação
ax.text(0.6, v_max - 0.3, "Itens MUITO difíceis\n(medem alta habilidade)",
        fontsize=8, ha="center", style="italic", color="coral")
ax.text(0.6, v_min + 0.5, "Itens MUITO fáceis\n(medem baixa habilidade)",
        fontsize=8, ha="center", style="italic", color="coral")
ax.text(-0.6, v_max - 0.3, "Sujeitos com\nalta habilidade",
        fontsize=8, ha="center", style="italic", color="steelblue")
ax.text(-0.6, v_min + 0.5, "Sujeitos com\nbaixa habilidade",
        fontsize=8, ha="center", style="italic", color="steelblue")

plt.tight_layout()
plt.savefig("resultados/figura11_wright_map.png", dpi=200, bbox_inches="tight")
print("  Figura 11 salva: resultados/figura11_wright_map.png")
plt.close()

# ============================================================
# 7. Conclusões
# ============================================================
print("\n" + "=" * 60)
print("CONCLUSÕES — IRT (Modelo de Rasch 1PL)")
print("=" * 60)
print(f"""
Resultados:
  - Correlação θ estimado vs verdadeiro: r = {r_theta:.3f}
  - Correlação b estimado vs verdadeiro: r = {r_b:.3f}
  - RMSE θ: {rmse_theta:.3f}, RMSE b: {rmse_b:.3f}

Aplicações para P05:
  1. Calibração de itens do BRIEF-2 para nossa amostra
  2. Comparação de DIF (Differential Item Functioning) por sexo/SES
  3. Construção de testes adaptativos computadorizados (CAT)
  4. Avaliação de equidade dos itens
  5. Detecção de itens enviesados ou mal calibrados

Próximos passos:
  - Modelo 2PL (discriminação variável por item)
  - Modelo de crédito parcial para itens Likert
  - Bayesian IRT com priors informativos
""")
