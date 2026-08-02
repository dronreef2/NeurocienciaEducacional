# Pré-Registro OSF — Projeto P04

> **Template:** OSF Standard Pre-Data Collection Registration
> **Projeto:** P04 — O papel da inteligência artificial generativa nas funções executivas de crianças: estudo transversal correlacional
> **Versão:** 1.0
> **Data prevista:** Mês 10 (Outubro 2026)

---

## 1. Informações gerais

- **Título:** Uso de IA generativa e funções executivas em crianças do 2º ao 5º ano: um estudo transversal correlacional com modelagem de equações estruturais
- **Tipo:** Estudo transversal correlacional com SEM (Structural Equation Modeling)
- **Área:** Educação + Neurociência Cognitiva
- **Investigadora:** [Seu nome]
- **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN/CERES)

## 2. Pergunta de pesquisa

**RQ1:** Qual a relação entre o uso de IA generativa (frequência, tipo de tarefa, tipo de conteúdo) e o desempenho em funções executivas (controle inibitório, memória de trabalho, flexibilidade cognitiva) em crianças do 2º ao 5º ano?

**Sub-questões:**

- **RQ1a:** O **engajamento** com a IA medeia a relação entre frequência de uso e FE?
- **RQ1b:** O **letramento digital** dos pais modera essa relação?
- **RQ1c:** A relação é **linear** ou **curvilínea** (uso ótimo)?
- **RQ1d:** Qual a contribuição relativa de **uso de IA** vs. **variáveis demográficas** (idade, sexo, SES)?

## 3. Hipóteses

| ID | Hipótese | Predição |
|---|---|---|
| **H1** | Maior uso de IA → melhor FE | β > 0, p < .05 |
| **H2** | Engajamento medeia relação uso_ia → FE | Efeito indireto significativo (β ≠ 0, IC 95% não inclui 0) |
| **H3** | Letramento digital modera (uso_ia × letramento → FE) | Interação significativa, p < .05 |
| **H4** | Relação curvilínea: muito uso (>3h/dia) é prejudicial | β quadrático < 0 |
| **H5** | Idade modera (crianças mais velhas se beneficiam mais) | Interação significativa |

## 4. Design

### 4.1. Tipo
- Estudo transversal correlacional
- 1 coleta de dados (T0)
- SEM com variável latente FE

### 4.2. Participantes
- **N:** 300-500 crianças (2º ao 5º ano)
- **Idade:** 7-11 anos
- **Recrutamento:** 3-5 escolas públicas + 1-2 privadas de Natal/RN
- **Critérios:**
  - Matriculadas em 2026
  - Acesso a dispositivo com internet
  - Consentimento dos pais + assentimento da criança

### 4.3. Medidas

#### Variáveis independentes (X)
| Constructo | Instrumento | Tipo |
|---|---|---|
| Uso de IA generativa | Questionário de uso (desenvolvido para o estudo) | Frequência, tipo, contexto |
| Tipo de IA | ChatGPT, Khanmigo, Gemini, Copilot, etc. | Categórico |
| Tempo de uso | Diário de uso (1 semana) + autorrelato | Contínuo (min/dia) |
| Letramento digital dos pais | Questionário adaptado (Hargittai 2009) | Contínuo |

#### Mediador (M)
| Constructo | Instrumento | Tipo |
|---|---|---|
| Engajamento | Escala de Flow (Jackson & Marsh) | Contínuo |
| Autonomia percebida | Questionário de motivação (Pintrich) | Contínuo |

#### Variáveis dependentes (Y)
| Constructo | Instrumento | Tempo |
|---|---|---|
| Controle inibitório | **Stroop Digital** (crianças) | 8 min |
| Memória de trabalho | **Backward Digit Span** (WISC-V adaptado) | 10 min |
| Flexibilidade cognitiva | **Dimensional Change Card Sort** (DCCS, Zelazo 2003) | 5 min |
| FE Composto | Latente (CFA) | — |

#### Covariáveis
- Idade, sexo, SES (escala ABEP), tipo de escola, QI estimado (Raven colorido), ansiedade (escala), TDAH (escala)

### 4.4. Análise

#### Análise primária
- **CFA:** confirmar estrutura unidimensional de FE
- **SEM com mediação:** `uso_ia → engajamento → FE`
- **Software:** `lavaan` (R) + `semTools`
- **Estimação:** ML robusto (MLR) para lidar com não-normalidade
- **Correção de Bonferroni** para 3 medidas de FE (α = .017)

#### Análise secundária
- **Moderação:** interação uso_ia × letramento_digital
- **Curvilinearidade:** incluir termo quadrático
- **Multigrupo:** por idade e sexo
- **Invariância:** testar equivalência do constructo FE entre grupos

#### Análise de robustez
- **Validação cruzada** (k-fold = 5)
- **Bootstrap** (5000 iterações) para ICs
- **Análise de sensibilidade** com diferentes modelos

### 4.5. Tamanho amostral
- **N mínimo:** 300 (power = .80, α = .05, efeito médio f² = .10)
- **N ótimo:** 500 (para análise de subgrupos)
- **Justificativa:** G*Power + regras de Kline (2016) para SEM

## 5. Resultados esperados

- **Modelo 1 (mediação):** uso_ia → engajamento → FE
- **Modelo 2 (moderação):** interação uso_ia × letramento_digital
- **Tamanho de efeito:** r² = 0.10-0.20 (efeito pequeno a médio)
- **Variância explicada:** 20-30% do FE

## 6. Questões éticas

- **CEP/UFRN:** submissão antes de T0
- **TCLE** dos pais
- **TALE** da criança
- **Anonimização:** IDs alfanuméricos
- **Dados sensíveis:** não incluir (apenas comportamento, não neuroimagem)
- **LGPD:** cumprimento integral

## 7. Cronograma

| Mês | Atividade |
|---|---|
| 9 | Submissão CEP |
| 10 | Aprovação + recrutamento |
| 11-12 | Coleta de dados (1ª onda de escolas) |
| 13-14 | Análise de dados |
| 15-16 | Manuscrito + submissão |

## 8. Limitações pré-declaradas

1. **Corte transversal** — não permite inferência causal
2. **Autoreporte** de uso de IA (pais e crianças) — possível viés
3. **Variáveis omitidas** — pode haver confundidores não medidos
4. **Generalizabilidade** — uma região
5. **Efeito de seleção** — quem usa IA pode ser diferente dos não-usuários

## 9. Plano de divulgação

- **Artigo:** *Computers in Human Behavior* (Qualis A1) ou *Learning and Instruction*
- **Conferências:** AERA, EARLI, SBIE
- **Preprint:** PsyArXiv

## 10. Mudanças do pré-registro

> **Compromisso:** qualquer mudança documentada no OSF.

## 11. Aprovações

- [ ] Investigadora
- [ ] Orientadora (Angela Naschold)
- [ ] CEP/UFRN

---

**Data:** 2026-07-28
**OSF ID:** [a criar]
