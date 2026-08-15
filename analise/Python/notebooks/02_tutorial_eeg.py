"""
from neurociencia_edu.eeg import preprocess_eeg, compute_erp
02_tutorial_eeg.py
TUTORIAL 2: Análise EEG / ERP — P03

Objetivos:
- Entender o pipeline de processamento EEG
- Simular dados de N170 (leitura) e P300 (atenção)
- Calcular ERPs
- Comparar condições (papel vs. tela)
- Fazer testes estatísticos

Pré-requisitos: numpy, scipy, matplotlib, pandas
Tempo estimado: 25 minutos

NOTA: P03 ainda não tem dados coletados (setup planejado para 2026).
Este tutorial usa dados sintéticos para demonstrar o pipeline.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
from pathlib import Path

print("=" * 70)
print("  TUTORIAL 2 — Análise EEG/ERP (P03)")
print("=" * 70)

# ============================================================
# PASSO 1: O que é EEG/ERP?
# ============================================================
print("""
PASSO 1: O que é EEG/ERP?

EEG (Eletroencefalografia) mede atividade elétrica do cérebro
via eletrodos no couro cabeludo. Sinal contínuo com frequência
de amostragem tipicamente 250-1000 Hz.

ERP (Event-Related Potential) é o sinal EEG "média" alinhado a um evento
(ex: apresentação de uma palavra). Componentes ERP são picos/vales
característicos em janelas temporais específicas:

  N170 (~170 ms, occipital-temporal):
    - Sensível a faces e palavras escritas
    - Mais negativo (maior amplitude) para palavras do que símbolos
    - Emerge com a alfabetização (Maurer et al., 2005)

  P300 (~300 ms, parietal):
    - Atenção alocada, memória de trabalho
    - Mais positivo em tarefas de decisão

Em P03, comparamos leitura em TELA vs. PAPEL.
""")

# ============================================================
# PASSO 2: Simular dados EEG
# ============================================================
print("\n" + "=" * 70)
print("PASSO 2: Simular dados EEG (N=20 crianças, 2 condições)")
print("=" * 70)

np.random.seed(42)
n_children = 20
n_channels = 32
sfreq = 500  # Hz
n_samples_per_trial = 500  # 1 segundo
n_trials_per_condition = 80
time = np.arange(n_samples_per_trial) / sfreq - 0.2  # -200ms a 800ms

print(f"  Parâmetros:")
print(f"    Crianças: {n_children}")
print(f"    Canais: {n_channels}")
print(f"    Taxa de amostragem: {sfreq} Hz")
print(f"    Trials por condição: {n_trials_per_condition}")

# Função para gerar ERP
def generate_erp(channels, time, condition):
    """Gera ERP sintético com N170 e P300."""
    erp = np.zeros((channels, len(time)))

    for ch in range(channels):
        # N170: pico negativo em ~170ms, mais occipital-temporal
        if ch in [25, 26, 27, 28, 29, 30, 31]:  # canais occipito-temporais
            n170_amp = -4.0 if condition == "papel" else -2.8  # tela menor
            n170_lat = 0.18 if condition == "papel" else 0.20   # tela mais tarde
        else:
            n170_amp = -1.0
            n170_lat = 0.18

        # P300: pico positivo em ~350ms, mais parietal
        if ch in [0, 1, 2, 3, 4]:  # canais parietais
            p300_amp = 6.0 if condition == "tela" else 4.5  # tela maior
            p300_lat = 0.35
        else:
            p300_amp = 2.0
            p300_lat = 0.35

        # Soma de Gaussianas
        n170 = n170_amp * np.exp(-((time - n170_lat) ** 2) / (2 * 0.025 ** 2))
        p300 = p300_amp * np.exp(-((time - p300_lat) ** 2) / (2 * 0.060 ** 2))
        erp[ch] = n170 + p300

    return erp

# Gerar dados por criança
data = {}
for cond in ["papel", "tela"]:
    data[cond] = {}
    for child in range(n_children):
        # ERP verdadeiro (varia por criança)
        erp_true = generate_erp(n_channels, time, cond)
        # Adicionar ruído
        noise = np.random.normal(0, 2.0, (n_channels, n_samples_per_trial))
        # Trials individuais
        trials = erp_true[:, None, :] + noise[:, None, :]
        # Variação por trial (jitter)
        trials += np.random.normal(0, 0.5, trials.shape)
        data[cond][child] = trials

print("✅ Dados simulados")
print(f"  Shape por trial: {data['papel'][0].shape} (canais × samples)")

# ============================================================
# PASSO 3: Pré-processamento
# ============================================================
print("\n" + "=" * 70)
print("PASSO 3: Pré-processamento (filtro 0.1-30 Hz)")
print("=" * 70)

def bandpass_filter(data, sfreq, l_freq=0.1, h_freq=30):
    """Aplica filtro passa-banda."""
    nyq = sfreq / 2
    low = l_freq / nyq
    high = h_freq / nyq
    b, a = signal.butter(4, [low, high], btype="band")
    return signal.filtfilt(b, a, data, axis=-1)

# Filtrar
for cond in ["papel", "tela"]:
    for child in range(n_children):
        data[cond][child] = bandpass_filter(data[cond][child], sfreq)

print("✅ Filtro passa-banda aplicado (0.1-30 Hz)")

# ============================================================
# PASSO 4: Calcular ERPs (média por condição)
# ============================================================
print("\n" + "=" * 70)
print("PASSO 4: Calcular ERPs (média por criança e condição)")
print("=" * 70)

# Média por criança (depois por condição)
erp_per_child = {"papel": [], "tela": []}
for cond in ["papel", "tela"]:
    for child in range(n_children):
        erp = data[cond][child].mean(axis=1)  # média dos trials → (channels, time)
        erp_per_child[cond].append(erp)

# ROI occipital-temporal (canais 25-31)
roi_channels = list(range(25, 32))
roi_labels = ["PO7", "PO8", "O1", "Oz", "O2", "PO9", "PO10"]

# ERP médio da ROI
roi_papel = np.array([erp[roi_channels, :].mean(axis=0) for erp in erp_per_child["papel"]])
roi_tela = np.array([erp[roi_channels, :].mean(axis=0) for erp in erp_per_child["tela"]])

print(f"  ROI: {roi_labels}")
print(f"  N170 esperado: mais negativo em papel ({roi_papel.mean(axis=1).min():.2f}) vs tela ({roi_tela.mean(axis=1).min():.2f})")

# ============================================================
# PASSO 5: Visualizar ERPs
# ============================================================
print("\n" + "=" * 70)
print("PASSO 5: Visualizar ERPs")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Painel A: ERPs de todas as crianças (butterfly plot)
ax = axes[0, 0]
for i in range(n_children):
    # Média da ROI para cada criança (1D)
    ax.plot(time * 1000, roi_papel[i], color="blue", alpha=0.2, linewidth=0.5)
    ax.plot(time * 1000, roi_tela[i], color="red", alpha=0.2, linewidth=0.5)
ax.axvline(170, color="green", linestyle="--", alpha=0.5, label="N170")
ax.axvline(350, color="purple", linestyle="--", alpha=0.5, label="P300")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Amplitude (μV)")
ax.set_title("ERPs por criança (butterfly)", fontweight="bold")
ax.legend()

# Painel B: ERPs médios com IC 95%
ax = axes[0, 1]
mean_papel = roi_papel.mean(axis=0)
mean_tela = roi_tela.mean(axis=0)
se_papel = roi_papel.std(axis=0) / np.sqrt(n_children)
se_tela = roi_tela.std(axis=0) / np.sqrt(n_children)

ax.plot(time * 1000, mean_papel, color="blue", linewidth=2, label="Papel")
ax.fill_between(time * 1000, mean_papel - 1.96*se_papel, mean_papel + 1.96*se_papel,
                color="blue", alpha=0.2)
ax.plot(time * 1000, mean_tela, color="red", linewidth=2, label="Tela")
ax.fill_between(time * 1000, mean_tela - 1.96*se_tela, mean_tela + 1.96*se_tela,
                color="red", alpha=0.2)
ax.axvline(170, color="green", linestyle="--", alpha=0.5, label="N170")
ax.axvline(350, color="purple", linestyle="--", alpha=0.5, label="P300")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Amplitude (μV)")
ax.set_title("ERPs médios (IC 95%)", fontweight="bold")
ax.legend()

# Painel C: Topografia (N170)
ax = axes[1, 0]
window_n170 = (time >= 0.15) & (time <= 0.20)
topo_papel = mean_papel[window_n170].mean()
topo_tela = mean_tela[window_n170].mean()
bars = ax.bar(["Papel", "Tela"], [topo_papel, topo_tela],
              color=["#3498db", "#e74c3c"], edgecolor="black")
ax.set_ylabel("Amplitude N170 (μV)")
ax.set_title("Amplitude N170 (150-200ms)", fontweight="bold")
ax.axhline(0, color="black", linewidth=0.5)
for bar, val in zip(bars, [topo_papel, topo_tela]):
    ax.text(bar.get_x() + bar.get_width()/2, val - 0.3,
            f"{val:.2f}", ha="center", fontweight="bold")

# Painel D: Topografia (P300)
ax = axes[1, 1]
window_p300 = (time >= 0.30) & (time <= 0.40)
topo_papel_p = mean_papel[window_p300].mean()
topo_tela_p = mean_tela[window_p300].mean()
bars = ax.bar(["Papel", "Tela"], [topo_papel_p, topo_tela_p],
              color=["#3498db", "#e74c3c"], edgecolor="black")
ax.set_ylabel("Amplitude P300 (μV)")
ax.set_title("Amplitude P300 (300-400ms)", fontweight="bold")
ax.axhline(0, color="black", linewidth=0.5)
for bar, val in zip(bars, [topo_papel_p, topo_tela_p]):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.1,
            f"{val:.2f}", ha="center", fontweight="bold")

plt.suptitle("Análise EEG/ERP — P03 (dados sintéticos)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("tutorial_2_eeg.png", dpi=150, bbox_inches="tight")
print("✅ Figura salva: tutorial_2_eeg.png")

# ============================================================
# PASSO 6: Testes estatísticos
# ============================================================
print("\n" + "=" * 70)
print("PASSO 6: Testes estatísticos (paired t-test)")
print("=" * 70)

# Amplitude N170 média por criança
n170_papel = roi_papel[:, window_n170].mean(axis=1)
n170_tela = roi_tela[:, window_n170].mean(axis=1)
t_n170, p_n170 = stats.ttest_rel(n170_papel, n170_tela)
d_n170 = (n170_papel - n170_tela).mean() / (n170_papel - n170_tela).std()

print(f"\n  N170:")
print(f"    Papel: {n170_papel.mean():.2f} ± {n170_papel.std():.2f} μV")
print(f"    Tela:  {n170_tela.mean():.2f} ± {n170_tela.std():.2f} μV")
print(f"    t({n_children-1}) = {t_n170:.2f}, p = {p_n170:.4f}, d = {d_n170:.2f}")
print(f"    {'Significativo' if p_n170 < 0.05 else 'Não significativo'} (α=0.05)")

# Amplitude P300 média por criança
p300_papel = roi_papel[:, window_p300].mean(axis=1)
p300_tela = roi_tela[:, window_p300].mean(axis=1)
t_p300, p_p300 = stats.ttest_rel(p300_papel, p300_tela)
d_p300 = (p300_tela - p300_papel).mean() / (p300_tela - p300_papel).std()

print(f"\n  P300:")
print(f"    Papel: {p300_papel.mean():.2f} ± {p300_papel.std():.2f} μV")
print(f"    Tela:  {p300_tela.mean():.2f} ± {p300_tela.std():.2f} μV")
print(f"    t({n_children-1}) = {t_p300:.2f}, p = {p_p300:.4f}, d = {d_p300:.2f}")
print(f"    {'Significativo' if p_p300 < 0.05 else 'Não significativo'} (α=0.05)")

# ============================================================
# PASSO 7: Conclusões
# ============================================================
print("\n" + "=" * 70)
print("PASSO 7: Conclusões e Próximos Passos")
print("=" * 70)
print(f"""
RESUMO DOS ACHADOS (dados sintéticos):

  N170: papel ({n170_papel.mean():.2f} μV) < tela ({n170_tela.mean():.2f} μV)
  → N170 MAIS NEGATIVO em papel (consistente com expertise hypothesis)
  → t = {t_n170:.2f}, p = {p_n170:.4f}, d = {d_n170:.2f}

  P300: tela ({p300_tela.mean():.2f} μV) > papel ({p300_papel.mean():.2f} μV)
  → P300 MAIOR em tela (consistente com maior esforço atencional)
  → t = {t_p300:.2f}, p = {p_p300:.4f}, d = {d_p300:.2f}

PRÓXIMOS PASSOS (P03 real):

  1. Submeter ao CEP (3 meses)
  2. Recrutar 60 crianças (3 meses)
  3. Coletar EEG com actiCHamp (32 canais, 6 meses)
  4. Pré-processamento com MNE-Python
  5. Análise de cluster temporal (Pernet et al., 2010)
  6. Submissão do manuscrito (5 meses)
""")
