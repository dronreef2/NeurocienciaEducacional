# Pré-Registro OSF — Projeto P03 (bandeira EEG)

> **Template:** OSF Standard Pre-Data Collection Registration
> **Projeto:** P03 — Marcadores neurais (EEG) do processamento de leitura com tutoria IA adaptativa vs. instrução tradicional
> **Versão:** 1.0
> **Data prevista:** Mês 12 (Dezembro 2026)

---

## 1. Título

**Marcadores eletrofisiológicos do processamento de palavras escritas em crianças do 2º ano do ensino fundamental após 4 meses de tutoria com IA adaptativa: estudo controlado com EEG**

---

## 2. Hipóteses

| ID | Hipótese | Predição |
|---|---|---|
| **H1** | Grupo IA-Adaptativa apresentará N170 mais negativo (maior especialização) que grupo controle | N170 amplitude: IA-ADAP < CTRL (p < .05) |
| **H2** | Grupo IA-Adaptativa apresentará N400 menor em leitura de pseudopalavras (menor conflito semântico) | N400 effect: IA-ADAP < CTRL (p < .05) |
| **H3** | Grupo IA-Adaptativa apresentará maior P300 em tarefas de atenção durante leitura | P300 amplitude: IA-ADAP > CTRL (p < .05) |
| **H4** | Efeito será mediado por horas de uso efetivo do tutor | Mediação: Uso → FE → N170 (β indireto significativo) |

---

## 3. Design

- **Tipo:** Estudo controlado quasi-experimental (2 grupos)
- **Grupos:**
  - **IA-Adaptativa:** Tutoria com Khanmigo + materiais de leitura
  - **Controle:** Instrução tradicional de leitura
- **N:** 60 crianças (30 por grupo) — pode aumentar para 80 se poder permitir
- **Duração:** 4 meses de intervenção + 1 dia de EEG pré e 1 dia pós

---

## 4. Medidas EEG

### Aquisição
- **Equipamento:** 32-channel actiCHamp (Brain Products) ou similar
- **Frequência de amostragem:** 500 Hz
- **Referência:** FCz online, re-referenciado para média offline
- **Impedância:** < 10 kΩ
- **Duração da gravação:** 30 min

### Paradigma
- **Tarefa de decisão lexical:** 240 trials
  - 60 palavras reais
  - 60 pseudopalavras
  - 60 falsas-fontes (scrambled)
  - 60 catch trials
  - Duração do estímulo: 300 ms
  - SOA: 1500-2000 ms
  - Resposta: botão (esquerda = palavra, direita = não-palavra)

### Componentes de interesse
- **N170** (130-210 ms, O1/O2/P7/P8): especialização visual
- **N400** (300-500 ms, Cz/CPz/Pz): integração semântica
- **P300** (250-450 ms, Pz/Cz): atenção

---

## 5. Análise

### Pré-processamento
- MNE-Python 1.5
- Filtro passa-banda 0.1-30 Hz
- Notch 60 Hz
- ICA para remoção de blinks/movimentos oculares
- Rejeição de trials: amplitude > 100 µV

### Análise estatística
- **GLM misto** (lme4 em R): condição (palavra/pseudopalavra/falsa-fonte) × grupo (IA/controle) × tempo × cluster
- **Cluster-based permutation test** (MNE-Python) para controle de múltiplas comparações
- **Correção FDR** (Benjamini-Hochberg) para componentes

---

## 6. Cronograma

| Mês | Atividade |
|---|---|
| 12 | Pré-registro + CEP |
| 13-14 | Recrutamento de escolas e famílias |
| 15 | EEG pré-teste (T0) |
| 16-19 | Intervenção (16 semanas) |
| 20 | EEG pós-teste (T1) |
| 21-23 | Análise |
| 24-27 | Manuscrito |

---

## 7. Recursos

- **Equipamento:** actiCHamp (empréstimo ICe/UFRN)
- **Análise:** MNE-Python 1.5, R
- **Espaço:** Lab EEG ICe/UFRN
- **Parceiros:** Ângela Naschold, Antonio Pereira (ICe), Sal Khan/Khan Academy (Khanmigo API)

---

## 8. Limitações pré-declaradas

1. **N pequeno** (60) → baixa potência para interações
2. **EEG em crianças:** artefatos motores são maiores
3. **Falta de randomização** (quasi-experimental)
4. **Não-cego:** crianças sabem que estão usando IA
5. **Generalizabilidade:** Khanmigo é plataforma específica

---

## 9. Aprovações

- [ ] Investigador principal
- [ ] Orientadora (Angela Naschold)
- [ ] Coorientador ICe (Antonio Pereira)
- [ ] CEP/UFRN

---

**Data de criação:** 2026-07-28
**OSF ID:** [a criar]
