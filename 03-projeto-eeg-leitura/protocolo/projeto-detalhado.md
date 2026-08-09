# 📋 P03 — Protocolo Detalhado

> **Título:** Marcadores neurais (N170, P300) da leitura em tela versus papel em crianças do 2º ao 4º ano: estudo quasi-experimental com EEG
> **Versão:** 2.0 (2026-08-08)
> **Pesquisador principal:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela M. C. Naschold
> **Co-orientador:** Prof. Dr. Antonio Pereira (ICe/UFRN)
> **Status:** Aguardando submissão CEP

---

## 1. Resumo

### 1.1. Pergunta de pesquisa
> Como a leitura em tela vs. papel modula os componentes ERP N170 (~170ms) e P300 (~350ms) em crianças do 2º ao 4º ano do ensino fundamental?

### 1.2. Hipóteses
- **H1:** A amplitude de N170 será atenuada (menos negativa) para palavras em tela vs. papel (efeito d ≈ 0.4-0.6).
- **H2:** A amplitude de P300 será maior (mais positiva) para palavras em tela (esforço atencional).
- **H3:** Os efeitos serão modulados pelo ano escolar (2º < 4º), refletindo expertise.

---

## 2. Background

### 2.1. Modelo de dupla-rota da leitura (Coltheart, 2001)

- **Rota lexical:** reconhecimento direto de palavras familiares
- **Rota fonológica:** decodificação letra-som
- **N170** emerge conforme rota lexical se automatiza (Maurer et al., 2005)

### 2.2. Componentes ERP

**N170 (150-200 ms, occipital-temporal):**
- Sensível a faces E palavras escritas
- Mais negativo com expertise de leitura
- Latência mais cedo em leitores proficientes

**P300 (300-500 ms, parietal):**
- Atenção alocada, memória de trabalho
- Maior amplitude = maior engajamento atencional
- Modulado por carga cognitiva (Sweller, 1988)

### 2.3. Estado da arte

- **Mangen et al. (2013):** P300 modulado por tela vs. papel em adultos
- **Delgado et al. (2018):** leitura em tela prejudica compreensão
- **Common Sense Media (2024):** 8h/dia de tela em crianças
- **Gap:** EEG comparando tela vs. papel em crianças em alfabetização

---

## 3. Método

### 3.1. Design

**Quasi-experimental contrabalanceado (within-subjects):**
- Variável independente: meio (tela vs. papel)
- Variáveis dependentes: amplitude e latência de N170, P300
- 2 sessões × 30 min

### 3.2. Participantes

**N = 60** crianças (20 por ano escolar)

- 2º ano: 20 (7-8 anos)
- 3º ano: 20 (8-9 anos)
- 4º ano: 20 (9-10 anos)
- Critérios: sem epilepsia, sem medicação psicoativa, sem deficiência visual não corrigida

### 3.3. Equipamento

- **EEG:** actiCHamp (Brain Products), 32 canais
- **Eletrodos:** 10-20 system + EOG
- **Acelerômetro ocular:** EyeLink 1000
- **Apresentação:** E-Prime 3.0 ou PsychoPy
- **Tela:** 24" 1920×1080, 60Hz

### 3.4. Estímulos

- **80 palavras** (frequência controlada)
- **80 pseudopalavras** (mesma estrutura silábica)
- **Fontes:** Arial, 80pt (papel) ou tamanho equivalente (tela)
- **Duração:** 300 ms apresentação, 1500-2000 ms ISI

### 3.5. Procedimento

```
Sessão 1 (30 min, papel):
  1. Adaptação à sala EEG (10 min)
  2. Calibração EOG (2 min)
  3. Prática (10 trials)
  4. Bloco experimental (160 trials, ~10 min)
  5. Washout (5 min)

Sessão 2 (30 min, tela):
  - Idêntico, mas com tela
  - Contrabalanceamento: 50% começa com tela
```

### 3.6. Análise EEG

**Pré-processamento (MNE-Python):**
1. Filtro passa-banda: 0.1-30 Hz
2. Re-referência: mastoides
3. ICA para remoção de artefatos oculares
4. Épocas: -200 a 800 ms
5. Baseline correction: -200 a 0 ms
6. Rejeição de artefatos: ±150 μV

**Análise estatística:**
- ROI N170: PO7, PO8, O1, O2 (occipital-temporal)
- ROI P300: P3, Pz, P4 (parietal)
- **Análise de cluster temporal** (Pernet et al., 2010)
- Paired t-test por cluster
- Correção FDR (Benjamini-Hochberg)

### 3.7. Análise secundária

- Comportamental: precisão, tempo de reação
- Correlação EEG-comportamento
- Análise por ano escolar (2º < 3º < 4º)

---

## 4. Aspectos Éticos

- **CEP/UFRN** (CAAE pendente)
- **TCLE pais + TALE criança** (linguagem acessível + pictogramas)
- **Cuidado especial:** EEG em crianças (pais presentes, pausas)
- **Devolutiva:** relatório individual + sessão explicativa

---

## 5. Análise de Poder

**Baseado em Mangen et al. (2013):**
- Efeito esperado d = 0.5 (N170)
- Para paired t-test, N = 34 para power = 0.80
- **N = 60** (margem para subgrupos e atrito)

---

## 6. Limitações

- Tarefa experimental artificial (não leitura natural)
- Possível viés de novidade (crianças + EEG)
- Attrition (10-15% esperado)
- Variabilidade alta em crianças

---

## 7. Timeline

| Mês | Atividade |
|---|---|
| M0-M2 | Submissão CEP + setup EEG |
| M3-M4 | Recrutamento |
| M5-M10 | Coleta (60 crianças) |
| M11-M13 | Pré-processamento |
| M14-M15 | Análise |
| M16-M18 | Manuscrito |
| M19 | Submissão Dev Cognitive Neuroscience |

---

## 8. Orçamento

| Item | Custo (R$) |
|---|---|
| Manutenção actiCHamp | 3.000 |
| Eletrodos (gasto) | 5.000 |
| Espaço ICe (custo operacional) | 2.000 |
| Bolsista (12 meses) | 18.000 |
| Material participantes | 3.000 |
| Análise + estatística | 2.000 |
| Congresso | 5.000 |
| **Total** | **38.000** |

---

## 9. Resultados Esperados

**Baseado em simulação (Notebook 11):**
- N170: papel (-4.5 μV) < tela (-3.2 μV), d ≈ 0.5
- P300: tela (6.8 μV) > papel (5.0 μV), d ≈ 0.4
- Interação com ano: 4º ano menos afetado

**Implicações:**
- Tela pode prejudicar automaticidade de leitura em crianças pequenas
- Esforço atencional maior em tela (compensação?)
- Implicações educacionais (não usar tela precocemente)

---

## 10. Disseminação

- **Manuscrito:** Developmental Cognitive Neuroscience (A1)
- **Conferência:** ECVP (European Conference on Visual Perception)
- **Devolutiva:** Escolas + famílias
- **Dados:** OpenNeuro (EEG) + GitHub

---

**Próxima revisão:** Após piloto N=5
**Status:** Aguardando CEP + setup
