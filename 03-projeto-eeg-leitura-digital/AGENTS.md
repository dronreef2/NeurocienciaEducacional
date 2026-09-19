# AGENTS.md — Projeto P03 (EEG Leitura Tela vs Papel)

> Instruções para IAs trabalhando no **P03 — Processamento Neural da Leitura em Tela vs Papel**.
> **Versão:** 1.0 — 2026-09-19
> **Status:** protocolo + 5 instrumentos ERP + dados sintéticos EEG ok

---

## 🎯 Sobre o P03

**Título:** Processamento Neural da Leitura em Tela vs Papel em Crianças do 3º ao 5º ano: Estudo com EEG 32-canais

**Pergunta:** Quais diferenças neurofisiológicas na leitura em tela vs papel?

**Design:** Quase-experimental within-subjects + EEG 32-canais (BrainProducts / ActiCHamp)

**N:** 60 crianças (8-12 anos)

**Componentes ERP medidos:**

| Componente | Latência | Região | Função |
|---|---|---|---|
| N170 | 170ms | Occipito-temporal | Processamento visual de palavras |
| P200 | 200ms | Frontal-central | Atenção inicial |
| P300 | 300ms | Parietal | Atenção sustentada |
| N400 | 400ms | Centro-parietal | Integração semântica |
| P600 | 600ms | Parietal | Processamento sintático |

**Periódico-alvo:** *NeuroImage* (A1, Elsevier) ou *Developmental Cognitive Neuroscience*

**Cronograma:**
- 2027-Q1: CEP + acordo ICe (Prof. Antonio Pereira)
- 2027-Q2/Q3: coleta EEG
- 2027-Q4: análise
- 2028-Q1: manuscrito
- 2028-Q3: publicação

---

## 🚨 Regras ESPECÍFICAS

1. **EEG = equipamento caro + criança**: JAMAIS manipular equipamento sem técnico
2. **ICA para remoção de artefatos oculares** — sempre revisar visualmente
3. **Re-referência ao average** antes de qualquer análise
4. **Filtragem:** 0.1-40 Hz + notch 60 Hz
5. **Rejeição de épocas:** amplitude > 100 µV
6. **Análise primária:** ANOVA mista 2 (mídia) × 2 (tarefa)
7. **Análise secundária:** cluster-based permutation, time-frequency, sLORETA
8. **Power analysis:** Simulação Monte Carlo para detectar d=0.5 com power=0.80

---

## 📂 Estrutura

```
03-projeto-eeg-leitura-digital/
├── AGENTS.md                  ← este arquivo
├── README.md
├── protocolo/
├── instrumentos/
├── analise/
│   ├── 01_eeg_preprocessing.py
│   └── 02_eeg_erp_analysis.py
└── scripts/
```

**Dados sintéticos:**
- `dados_sinteticos/P03_eeg_papel.npy` — (30, 32, 500) — 30 sujeitos, 32 canais, 500 amostras
- `dados_sinteticos/P03_eeg_tela.npy` — idem

---

## 🎯 Hipóteses pré-registradas

| H | Componente | Predição |
|---|---|---|
| H3.1 | N170 | Tela ↑ amplitude |
| H3.2 | P300 | Tela ↓ amplitude |
| H3.3 | N400 | Tela ↑ amplitude |
| H3.4 | Idade | Interação significativa |
| H3.5 | Comportamental | Papel d=0.30 melhor |

---

## 🔗 Links

- `docs/osf-json/P03-osf.json` — pré-registro (rich metadata)
- `pages/4_🧠_P03_EEG.py` — visualização Streamlit
- `analise/Python/neurociencia_edu/eeg/` — pipeline EEG (`preprocess_eeg`, `compute_erp`)
- `analise/Python/tests/test_eeg_preprocess.py` e `test_eeg_erp.py`
- `analise/Python/notebooks/11_p03_eeg_realista.ipynb` — simulação

---

## 👥 Pessoas-chave

- **Prof. Antonio Pereira** (ICe/UFRN) — EEG access, co-orientação técnica

---

**Última atualização:** 2026-09-19
