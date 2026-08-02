# Pré-Registro OSF — Projeto P05

> **Template:** OSF Standard Pre-Data Collection Registration
> **Projeto:** P05 — Coorte longitudinal: desenvolvimento de funções executivas, letramento e uso de tecnologia em crianças dos 7 aos 11 anos
> **Versão:** 1.0
> **Data prevista:** Mês 12 (Dezembro 2026)
> **Tipo:** Estudo longitudinal prospectivo (5 ondas)

---

## 1. Informações gerais

- **Título:** COORTE-INF: Desenvolvimento cognitivo e neural de crianças dos 7 aos 11 anos — estudo longitudinal com EEG e medidas neuropsicológicas
- **Tipo:** Coorte longitudinal prospectiva (5 ondas anuais)
- **Investigadora:** [Seu nome]
- **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN/CERES)
- **Co-investigador:** Prof. Dr. Antonio Pereira (ICe/UFRN) — EEG
- **Financiamento:** CAPES + possível FAPESP/CNPq
- **Período:** 2027-2031 (5 anos)

## 2. Pergunta de pesquisa

**RQ1:** Quais são as trajetórias de desenvolvimento de funções executivas (FE), letramento, e uso de tecnologia em crianças brasileiras dos 7 aos 11 anos, e como essas trajetórias se influenciam mutuamente?

**Sub-questões:**

- **RQ1a:** Existem **subgrupos** de crianças com trajetórias de FE distintas (LGMM)?
- **RQ1b:** O **uso de tecnologia** (em quantidade e qualidade) prediz **mudanças** na trajetória de FE?
- **RQ1c:** Marcadores neurais (EEG) **tempo 1** predizem **mudanças** em FE ao longo do tempo?
- **RQ1d:** Como **fatores contextuais** (escola, família, comunidade) modulam essas trajetórias?

## 3. Hipóteses

### 3.1. Hipóteses de crescimento (LGCM)

| ID | Hipótese | Predição |
|---|---|---|
| **H1a** | FE cresce linearmente dos 7 aos 11 anos | Slope médio > 0, p < .001 |
| **H1b** | Há **heterogeneidade** nas trajetórias | Variância do slope > 0, p < .001 |
| **H1c** | Existem **2-3 subgrupos** distintos (LGMM) | BIC menor para modelo de mistura |

### 3.2. Hipóteses preditivas

| ID | Hipótese | Predição |
|---|---|---|
| **H2a** | Uso excessivo de tecnologia (>3h/dia) prediz **declínio** em FE | β slope < 0, p < .05 |
| **H2b** | Uso educacional de tecnologia prediz **ganho** em letramento | β slope > 0, p < .05 |
| **H2c** | Marcadores neurais (N170, P300) em T1 predizem **ganho** em FE | β > 0, p < .05 |

## 4. Design

### 4.1. Tipo
- Coorte longitudinal prospectiva
- **5 ondas** anuais (T1=7 anos, T2=8, ..., T5=11)
- Acompanhamento de 5 anos

### 4.2. Participantes
- **N inicial:** 200 crianças (aos 7 anos, 2º ano)
- **Acompanhamento esperado:** ≥ 80% (N=160 ao final)
- **Critérios:**
  - Matriculadas no 2º ano em escola pública/privada de Natal/RN
  - Sem deficiência cognitiva ou neurológica
  - Consentimento parental + assentimento infantil

### 4.3. Medidas por onda

| Constructo | Instrumento | Tempo |
|---|---|---|
| **FE — Controle inibitório** | Stroop Digital | 8 min |
| **FE — Memória de trabalho** | Backward Digit Span | 10 min |
| **FE — Flexibilidade** | DCCS | 5 min |
| **Letramento — Leitura** | TLE (Seabra & Capovilla) | 15 min |
| **Letramento — Escrita** | TDE (desenho de palavras) | 15 min |
| **Letramento — Matemática** | TML | 15 min |
| **QI estimado** | Raven SPM colorido | 15 min |
| **TDAH (screening)** | SNAP-IV (pais) | 10 min |
| **Ansiedade** | MASC (criança) | 10 min |
| **Uso de tecnologia** | Questionário + diário | — |
| **Qualidade do uso** | Questionário de letramento digital | — |
| **EEG (subset)** | Paradigma de leitura (N170, P300) | 30 min |
| **Contexto familiar** | Questionário socioeconômico (ABEP) | 15 min |
| **Contexto escolar** | Questionário professor | 10 min |

### 4.4. Análise

#### 4.4.1. Modelagem de crescimento
- **LGCM (Latent Growth Curve Model)** com `lavaan`:
  - Linear, quadrático, condicional
  - Covariáveis: sexo, SES, tipo de escola
- **LGMM (Latent Growth Mixture Model)** com `OpenMx`:
  - 1-5 classes
  - Seleção via BIC, entropy, LRT
- **Tratamento de dados faltantes:**
  - MAR (Missing at Random): ML sob `lavaan`
  - MNAR (Missing Not at Random): pattern mixture models (análise de sensibilidade)

#### 4.4.2. Análise preditiva (cross-lagged)
- **Cross-lagged panel model** (CLPM):
  - FE_t → Letramento_t+1
  - Letramento_t → FE_t+1
  - Uso_tec_t → FE_t+1
  - Uso_tec_t → Letramento_t+1
- **Random-Intercept CLPM (RI-CLPM)** para separar within-person e between-person

#### 4.4.3. Análise neural (subset com EEG)
- **LGCM multivariado** com FE + marcadores neurais
- **Predictive models:** EEG_t1 → slope FE (regressão)

#### 4.4.4. Softwares
- `lavaan` + `OpenMx` (R)
- `MNE-Python` para EEG
- `semTools`, `psych` (R)

## 5. Cronograma

| Mês | Atividade |
|---|---|
| 12 | Submissão CEP + setup EEG |
| 13 | Recrutamento + parceria com ICe |
| 14 | Onda 1 (T1) — N=200 |
| 15-17 | Análise T1 |
| 18 | Onda 2 (T2) — N esperado 190 |
| 24 | Onda 3 (T3) — N esperado 180 |
| 30 | Onda 4 (T4) — N esperado 170 |
| 36 | Onda 5 (T5) — N esperado 160 |
| 37-42 | Análise longitudinal final |
| 42-48 | Manuscritos |

## 6. Tamanho amostral

- **N = 200** (inicial)
- **Poder para LGCM:** detecta slope médio com 80% de poder (Cohen's d = 0.30)
- **Poder para LGMM:** identifica classes com 80% de poder se N ≥ 150 por classe
- **Poder para CLPM:** detecta β cross-lagged ≥ .20 com poder ≥ .80

## 7. Retenção e atrito

- **Estratégias:**
  - Compensação financeira modesta por onda
  - Lembretes por WhatsApp/SMS
  - Atualização de contato a cada 6 meses
  - Eventos com famílias (a cada ano)
- **Análise de atrito:** comparar T1 vs T5 nas variáveis demográficas
- **Imputação:** ML sob MAR + análise de sensibilidade MNAR

## 8. Aspectos éticos

- **Re-consentimento** a cada onda (crianças agora com 8, 9, 10, 11 anos)
- **Comunicação** dos resultados parciais às famílias (a cada ano)
- **LGPD** compliance
- **Armazenamento** de EEG em servidor seguro (ICe/UFRN)
- **Devolutiva** dos resultados individuais sob pedido

## 9. Limitações pré-declaradas

1. **N grande mas pode perder poder** em subgrupos
2. **Atrito** longitudinal — análises de sensibilidade
3. **Custo** — EEG é caro; subset menor
4. **Generalizabilidade** — uma coorte, uma região
5. **Efeito de coorte** — pode não generalizar para outras gerações

## 10. Plano de divulgação

- **Artigos:**
  - *Developmental Science* (Qualis A1) — artigo metodológico (protocolo)
  - *Developmental Cognitive Neuroscience* (Qualis A1) — EEG + FE
  - *Child Development* (Qualis A1) — trajetórias longitudinais
- **Conferências:** SRCD, ICIS, AERA
- **Devolutiva:** escolas e famílias anualmente

## 11. Pré-registro das análises

> Compromisso: **análises principais pré-registradas** após onda 1 (T1).

## 12. Aprovações

- [ ] Investigadora
- [ ] Orientadora (Angela Naschold)
- [ ] Co-investigador EEG (Antonio Pereira)
- [ ] CEP/UFRN
- [ ] Comitê de ética ICe

---

**Data:** 2026-07-28
**OSF ID:** [a criar]
**Versão:** 1.0
