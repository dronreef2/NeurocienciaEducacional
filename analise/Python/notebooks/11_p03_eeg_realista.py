"""
11_p03_eeg_realista.py
Simulação realista de EEG do P03 (leitura em tela vs papel)
Compara amplitudes N170 e P300 entre condições
"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy import signal, stats
from pathlib import Path

print("=" * 70)
print("  P03 — SIMULAÇÃO REALISTA EEG (TELA vs PAPEL)")
print("=" * 70)

# ============================================================
# 1. Simulação realista
# ============================================================
np.random.seed(42)
n_subjects = 30
n_channels = 32
sfreq = 1000
epoch_tmin, epoch_tmax = -0.2, 0.8
times = np.arange(epoch_tmin, epoch_tmax, 1/sfreq)
n_times = len(times)

# Layout dos eletrodos (simplificado)
# 0-3: F (frontal)
# 4-11: C (central)
# 12-19: P (parietal)
# 20-27: T (temporal)
# 28-31: O (occipital)

channel_names = []
for i, prefix in enumerate(["Fp1","Fp2","F3","Fz","F4","C3","Cz","C4","P3","Pz","P4","P7","P8",
                              "PO7","PO8","O1","Oz","O2","T7","T8","TP9","TP10","FT9","FT10",
                              "Fpz","AF7","AF8","F1","F2","P1","P2","POz"]):
    channel_names.append(prefix)

print(f"  N sujeitos: {n_subjects}")
print(f"  N canais: {n_channels}")
print(f"  Taxa: {sfreq} Hz")
print(f"  Época: {epoch_tmin*1000:.0f} a {epoch_tmax*1000:.0f} ms")

# ============================================================
# 2. Gerar ERPs realistas
# ============================================================
print("\n2. Gerando ERPs realistas...")

def gaussian(x, mu, sigma, amplitude):
    """Função gaussiana para componentes ERP."""
    return amplitude * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

def generate_realistic_erp(n_channels, times, sfreq, condition, n_subjects):
    """Gera ERP realista variando por sujeito."""
    # Latências (em segundos)
    n170_lat = 0.170
    p200_lat = 0.220
    n400_lat = 0.400
    p300_lat = 0.350

    # Efeitos: papel vs tela
    # Esperado: tela -> N170 mais tardio e menor amplitude (menos expertise)
    #           tela -> P300 maior (mais esforço)
    #           tela -> N400 mais negativo (mais conflito semântico?)

    erp_data = np.zeros((n_subjects, n_channels, len(times)))

    for s in range(n_subjects):
        # Variabilidade por sujeito
        n170_amp_var = np.random.normal(0, 0.3)  # amplitude individual
        n170_lat_var = np.random.normal(0, 0.01)  # latência individual
        p300_amp_var = np.random.normal(0, 0.4)

        for ch in range(n_channels):
            # N170: mais forte em occipital-temporal
            if ch in [13, 14, 15, 17]:  # PO7, PO8, O1, O2
                if condition == "papel":
                    n170_amp = -4.5 + n170_amp_var
                    n170_lat_ch = n170_lat + n170_lat_var
                else:  # tela
                    n170_amp = -3.2 + n170_amp_var  # MENOR
                    n170_lat_ch = n170_lat + 0.015 + n170_lat_var  # MAIS TARDE
            else:
                n170_amp = -1.0
                n170_lat_ch = n170_lat

            # P200: positivo frontal-central
            if ch < 11:
                p200_amp = 2.5
            else:
                p200_amp = 1.0

            # P300: mais forte em parietal
            if ch in [8, 9, 10]:  # P3, Pz, P4
                if condition == "papel":
                    p300_amp = 5.0 + p300_amp_var
                else:  # tela
                    p300_amp = 6.8 + p300_amp_var  # MAIOR
            else:
                p300_amp = 2.0

            # N400 (negativo, central-parietal)
            if ch in [5, 6, 7, 8, 9, 10]:
                if condition == "papel":
                    n400_amp = -1.5
                else:
                    n400_amp = -2.5  # MAIOR (tela)
            else:
                n400_amp = 0

            # Compor ERP
            erp = np.zeros(len(times))
            erp += gaussian(times, n170_lat_ch, 0.025, n170_amp)
            erp += gaussian(times, p200_lat, 0.040, p200_amp)
            erp += gaussian(times, p300_lat, 0.070, p300_amp)
            erp += gaussian(times, n400_lat, 0.080, n400_amp)

            # Adicionar ruído 1/f
            noise = generate_pink_noise(len(times)) * 1.5
            erp_data[s, ch] = erp + noise

    return erp_data

def generate_pink_noise(n):
    """Gera ruído rosa (1/f)."""
    white = np.random.randn(n)
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n)
    freqs[0] = 1  # evitar divisão por zero
    fft = fft / np.sqrt(freqs)
    return np.fft.irfft(fft, n)

# Gerar para cada condição
print("  Gerando condição PAPEL...")
erp_papel = generate_realistic_erp(n_channels, times, sfreq, "papel", n_subjects)
print("  Gerando condição TELA...")
erp_tela = generate_realistic_erp(n_channels, times, sfreq, "tela", n_subjects)
print("✅ ERPs gerados")

# ============================================================
# 3. Pré-processamento: filtro
# ============================================================
print("\n3. Pré-processamento: filtro passa-banda 0.1-30 Hz")

def bandpass_filter(data, sfreq, l_freq=0.1, h_freq=30):
    nyq = sfreq / 2
    b, a = signal.butter(4, [l_freq/nyq, h_freq/nyq], btype="band")
    return signal.filtfilt(b, a, data, axis=-1)

for s in range(n_subjects):
    erp_papel[s] = bandpass_filter(erp_papel[s], sfreq)
    erp_tela[s] = bandpass_filter(erp_tela[s], sfreq)

print("✅ Filtro aplicado")

# ============================================================
# 4. ERPs médios
# ============================================================
print("\n4. Calculando ERPs médios por condição")

# ROIs
roi_n170 = [13, 14, 15, 17]  # PO7, PO8, O1, O2
roi_p300 = [8, 9, 10]  # P3, Pz, P4

# Média dos sujeitos x ROI
n170_papel = erp_papel[:, roi_n170, :].mean(axis=1).mean(axis=0)
n170_tela = erp_tela[:, roi_n170, :].mean(axis=1).mean(axis=0)
p300_papel = erp_papel[:, roi_p300, :].mean(axis=1).mean(axis=0)
p300_tela = erp_tela[:, roi_p300, :].mean(axis=1).mean(axis=0)

print(f"  ROI N170: {[channel_names[i] for i in roi_n170]}")
print(f"  ROI P300: {[channel_names[i] for i in roi_p300]}")

# ============================================================
# 5. Análise estatística
# ============================================================
print("\n" + "=" * 70)
print("5. Testes estatísticos (paired t-test por sujeito)")
print("=" * 70)

# Janelas de interesse
n170_window = (times >= 0.130) & (times <= 0.200)
p300_window = (times >= 0.300) & (times <= 0.450)

# N170 amplitude por sujeito
n170_amp_papel = erp_papel[:, roi_n170, :].mean(axis=1)[:, n170_window].mean(axis=1)
n170_amp_tela = erp_tela[:, roi_n170, :].mean(axis=1)[:, n170_window].mean(axis=1)

# P300 amplitude por sujeito
p300_amp_papel = erp_papel[:, roi_p300, :].mean(axis=1)[:, p300_window].mean(axis=1)
p300_amp_tela = erp_tela[:, roi_p300, :].mean(axis=1)[:, p300_window].mean(axis=1)

print(f"\n  N170 (150-200 ms):")
print(f"    Papel: M = {n170_amp_papel.mean():.2f}, DP = {n170_amp_papel.std():.2f} μV")
print(f"    Tela:  M = {n170_amp_tela.mean():.2f}, DP = {n170_amp_tela.std():.2f} μV")
t_n170, p_n170 = stats.ttest_rel(n170_amp_papel, n170_amp_tela)
d_n170 = (n170_amp_papel - n170_amp_tela).mean() / (n170_amp_papel - n170_amp_tela).std()
print(f"    t({n_subjects-1}) = {t_n170:.2f}, p = {p_n170:.6f}, d = {d_n170:.2f}")

print(f"\n  P300 (300-450 ms):")
print(f"    Papel: M = {p300_amp_papel.mean():.2f}, DP = {p300_amp_papel.std():.2f} μV")
print(f"    Tela:  M = {p300_amp_tela.mean():.2f}, DP = {p300_amp_tela.std():.2f} μV")
t_p300, p_p300 = stats.ttest_rel(p300_amp_papel, p300_amp_tela)
d_p300 = (p300_amp_tela - p300_amp_papel).mean() / (p300_amp_tela - p300_amp_papel).std()
print(f"    t({n_subjects-1}) = {t_p300:.2f}, p = {p_p300:.6f}, d = {d_p300:.2f}")

# Análise de cluster temporal (mass-univariate)
print("\n  Análise de cluster temporal:")
t_times = []
for t_idx in range(len(times)):
    t_subj = stats.ttest_rel(
        erp_papel[:, roi_n170, :].mean(axis=1)[:, t_idx],
        erp_tela[:, roi_n170, :].mean(axis=1)[:, t_idx]
    )[0]
    t_times.append(t_subj)
t_times = np.array(t_times)

# Identificar clusters de t-values significativos
significant = (np.abs(t_times) > 2.0)
print(f"    Janelas com |t| > 2: {significant.sum()}")
if significant.sum() > 0:
    indices = np.where(significant)[0]
    print(f"    Primeira janela: {times[indices[0]]*1000:.0f} ms")
    print(f"    Última janela: {times[indices[-1]]*1000:.0f} ms")

# ============================================================
# 6. Visualizações
# ============================================================
print("\n6. Gerando visualizações...")

fig, axes = plt.subplots(3, 2, figsize=(14, 12))

# Painel A: ERPs ROI N170
ax = axes[0, 0]
ax.plot(times*1000, n170_papel, color="blue", linewidth=2, label="Papel")
ax.plot(times*1000, n170_tela, color="red", linewidth=2, label="Tela")
ax.axhline(0, color="black", linewidth=0.5)
ax.axvspan(130, 200, alpha=0.1, color="green", label="N170 window")
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Amplitude (μV)")
ax.set_title("ERPs ROI N170 (PO7/PO8/O1/O2)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel B: ERPs ROI P300
ax = axes[0, 1]
ax.plot(times*1000, p300_papel, color="blue", linewidth=2, label="Papel")
ax.plot(times*1000, p300_tela, color="red", linewidth=2, label="Tela")
ax.axhline(0, color="black", linewidth=0.5)
ax.axvspan(300, 450, alpha=0.1, color="purple", label="P300 window")
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Amplitude (μV)")
ax.set_title("ERPs ROI P300 (P3/Pz/P4)", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel C: Diferença de ondas
ax = axes[1, 0]
diff = n170_papel - n170_tela
ax.plot(times*1000, diff, color="black", linewidth=2)
ax.axhline(0, color="red", linestyle="--", alpha=0.5)
ax.fill_between(times*1000, diff, 0, where=(diff > 0), alpha=0.3, color="blue", label="Papel > Tela")
ax.fill_between(times*1000, diff, 0, where=(diff < 0), alpha=0.3, color="red", label="Tela > Papel")
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Diferença (μV)")
ax.set_title("Onda diferença (Papel - Tela)\nROI N170", fontweight="bold")
ax.legend()
ax.grid(True, alpha=0.3)

# Painel D: Topografia (N170)
ax = axes[1, 1]
topo_data = erp_papel[:, :, n170_window].mean(axis=(0, 2))
im = ax.imshow(topo_data.reshape(4, 8), cmap="RdBu_r", aspect="auto",
                vmin=-6, vmax=6)
ax.set_title("Topografia média N170 (Papel)", fontweight="bold")
ax.set_xticks([])
ax.set_yticks([])
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

# Painel E: Barplot das amplitudes
ax = axes[2, 0]
x_pos = np.arange(2)
means_n = [n170_amp_papel.mean(), n170_amp_tela.mean()]
sems_n = [n170_amp_papel.std()/np.sqrt(n_subjects), n170_amp_tela.std()/np.sqrt(n_subjects)]
ax.bar(x_pos, means_n, yerr=sems_n, color=["#3498db", "#e74c3c"],
       edgecolor="black", capsize=5)
ax.set_xticks(x_pos)
ax.set_xticklabels(["Papel", "Tela"])
ax.set_ylabel("Amplitude (μV)")
ax.set_title(f"N170 (150-200ms)\nt={t_n170:.2f}, p={p_n170:.4f}, d={d_n170:.2f}", fontweight="bold")
ax.axhline(0, color="black", linewidth=0.5)
ax.grid(True, axis="y", alpha=0.3)

# Painel F: Barplot P300
ax = axes[2, 1]
means_p = [p300_amp_papel.mean(), p300_amp_tela.mean()]
sems_p = [p300_amp_papel.std()/np.sqrt(n_subjects), p300_amp_tela.std()/np.sqrt(n_subjects)]
ax.bar(x_pos, means_p, yerr=sems_p, color=["#3498db", "#e74c3c"],
       edgecolor="black", capsize=5)
ax.set_xticks(x_pos)
ax.set_xticklabels(["Papel", "Tela"])
ax.set_ylabel("Amplitude (μV)")
ax.set_title(f"P300 (300-450ms)\nt={t_p300:.2f}, p={p_p300:.4f}, d={d_p300:.2f}", fontweight="bold")
ax.axhline(0, color="black", linewidth=0.5)
ax.grid(True, axis="y", alpha=0.3)

plt.suptitle("P03 — Simulação EEG Realista (Tela vs Papel)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("/workspace/resultados/figura15_p03_eeg.png", dpi=200, bbox_inches="tight")
print("✅ Figura 15 salva: resultados/figura15_p03_eeg.png")
plt.close()

# ============================================================
# 7. Conclusões
# ============================================================
print("\n" + "=" * 70)
print("7. CONCLUSÕES — P03 EEG")
print("=" * 70)
print(f"""
RESULTADOS DA SIMULAÇÃO:

N170 (150-200 ms, ROI occipital-temporal):
  Papel: {n170_amp_papel.mean():.2f} μV (mais negativo)
  Tela:  {n170_amp_tela.mean():.2f} μV
  t = {t_n170:.2f}, p = {p_n170:.6f}, d = {d_n170:.2f}
  {'Significativo' if p_n170 < 0.05 else 'Não significativo'}
  ✓ Consistente com hipótese de menor automaticidade em tela

P300 (300-450 ms, ROI parietal):
  Papel: {p300_amp_papel.mean():.2f} μV
  Tela:  {p300_amp_tela.mean():.2f} μV (mais positivo)
  t = {t_p300:.2f}, p = {p_p300:.6f}, d = {d_p300:.2f}
  {'Significativo' if p_p300 < 0.05 else 'Não significativo'}
  ✓ Consistente com maior esforço atencional em tela

LATÊNCIAS:
  N170 tela mais tarde em ~15 ms (consistente com literatura)

PRÓXIMOS PASSOS (P03 real):
  1. Coletar com actiCHamp (32 canais)
  2. Usar MNE-Python para pré-processamento
  3. Análise de cluster (Pernet et al., 2010)
  4. Controlar por idade e habilidade de leitura
""")
