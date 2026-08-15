"""Página 4: P03 - EEG (Leitura Tela vs Papel)"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="P03 - EEG", page_icon="🧠", layout="wide")

st.markdown("# 🧠 P03 — Leitura em Tela vs Papel")
st.markdown("### *Estudo quase-experimental com EEG 32-canais — N=60*")
st.markdown("---")

# Carregar dados
papeis_path = Path("/workspace/dados_sinteticos/P03_eeg_papel.npy")
tela_path = Path("/workspace/dados_sinteticos/P03_eeg_tela.npy")

with st.sidebar:
    st.markdown("## 🎛️ Filtros")
    n_subjects = st.slider("Número de sujeitos:", 1, 60, 30)
    component = st.selectbox("Componente ERP:", ["N170", "P300", "N400", "P600"])

if papeis_path.exists() and tela_path.exists():
    papel = np.load(papeis_path)
    tela = np.load(tela_path)
    papel = papel[:n_subjects]
    tela = tela[:n_subjects]
else:
    np.random.seed(42)
    n_samples = 500
    papel = np.random.randn(n_subjects, 32, n_samples) * 1e-6
    tela = np.random.randn(n_subjects, 32, n_samples) * 1e-6

# Componentes: latência e janela
components = {
    "N170": {"latency": 0.17, "window": (0.13, 0.21), "region": "Occipito-temporal"},
    "P300": {"latency": 0.30, "window": (0.28, 0.45), "region": "Parietal"},
    "N400": {"latency": 0.40, "window": (0.35, 0.55), "region": "Centro-parietal"},
    "P600": {"latency": 0.60, "window": (0.50, 0.80), "region": "Parietal"},
}
comp = components[component]

# Métricas
st.markdown(f"## 🧠 Análise: {component} ({comp['latency']*1000:.0f}ms, {comp['region']})")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Sujeitos", n_subjects)
with col2:
    st.metric("Canais", 32)
with col3:
    st.metric("Taxa amostragem", "250 Hz")

# ERP médio
times = np.linspace(-0.2, 1.0, papel.shape[2])
sfreq = 250

erp_papel = papel.mean(axis=(0, 1))  # grand average
erp_tela = tela.mean(axis=(0, 1))

# Plot
st.markdown("### 📈 ERP Comparativo (grand average)")
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(times, erp_papel * 1e6, label="Papel", color="blue", linewidth=2)
ax.plot(times, erp_tela * 1e6, label="Tela", color="red", linewidth=2)
ax.axhline(0, color="black", linestyle="--", alpha=0.3)
ax.axvline(0, color="black", linestyle="--", alpha=0.3, label="Estímulo")
ax.axvspan(comp["window"][0], comp["window"][1], alpha=0.2, color="yellow", label=f"Janela {component}")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Amplitude (µV)")
ax.set_title(f"ERP: {component}", fontweight="bold")
ax.legend(loc="upper right")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Amplitude na janela
mask = (times >= comp["window"][0]) & (times <= comp["window"][1])
amp_papel = erp_papel[mask].mean() * 1e6
amp_tela = erp_tela[mask].mean() * 1e6

st.markdown("### 📊 Amplitude Média por Condição")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Papel", f"{amp_papel:.3f} µV")
with col2:
    st.metric("Tela", f"{amp_tela:.3f} µV")
with col3:
    diff = amp_tela - amp_papel
    st.metric("Diferença", f"{diff:+.3f} µV")

# Topografia
st.markdown("### 🗺️ Topografia (32 canais)")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for i, (data, title) in enumerate([(papel, "Papel"), (tela, "Tela")]):
    topo = data.mean(axis=(0, 2)) * 1e6
    # Visualizar como grid 8x4
    topo_grid = topo.reshape(8, 4)
    im = axes[i].imshow(topo_grid, cmap="RdBu_r", aspect="auto", vmin=-3, vmax=3)
    axes[i].set_title(f"{title}", fontweight="bold")
    axes[i].set_xlabel("Canal X")
    axes[i].set_ylabel("Canal Y")
    plt.colorbar(im, ax=axes[i], label="µV")

plt.tight_layout()
st.pyplot(fig)

# Hipóteses
st.markdown("## 🎯 Hipóteses")
st.markdown(f"""
| H | Componente | Predição |
|---|---|---|
| H3.1 | N170 | Tela ↑ amplitude |
| H3.2 | P300 | Tela ↓ amplitude |
| H3.3 | N400 | Tela ↑ amplitude |
| H3.4 | Idade modula | Interação |
| H3.5 | Comportamental | Papel d=0.30 melhor |
""")
