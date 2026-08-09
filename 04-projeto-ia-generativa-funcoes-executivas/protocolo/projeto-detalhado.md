# 📋 P04 — Protocolo Detalhado

> **Título:** Uso de IA generativa e funções executivas em crianças do 2º ao 5º ano: estudo transversal correlacional com Modelagem de Equações Estruturais (SEM)
> **Versão:** 2.0 (2026-08-09)
> **Pesquisador principal:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela M. C. Naschold
> **Status:** Aguardando submissão CEP

---

## 1. Resumo

### 1.1. Pergunta de pesquisa
> O uso de IA generativa (X) afeta funções executivas (Y) em crianças do 2º ao 5º ano, mediado por engajamento escolar (M) e moderado pelo letramento digital dos pais (W)?

### 1.2. Hipóteses

- **H1:** Uso de IA → Engajamento (efeito direto positivo, β ≈ 0.30)
- **H2:** Engajamento → FE (efeito direto positivo, β ≈ 0.40)
- **H3:** Uso de IA → FE (efeito direto positivo, menor, β ≈ 0.10-0.20)
- **H4:** Efeito indireto significativo (β × b), IC 95% exclui zero
- **H5:** Letramento digital dos pais modera X → Y (W × X significativo)

### 1.3. Modelo conceitual

```
   Uso_IA (X) ──a1──> Engajamento (M1) ──b1──> FE (Y)
       │              │                          ↑
       │              │                          │
       c' (direto)────┴──────────────────────────┤
       │                                         │
       └──d (W×X)──> Engajamento (moderação)
```

---

## 2. Background

### 2.1. Estado da arte

- **Hamari et al. (2014):** gamificação → engajamento, r ≈ 0.40
- **Mollick (2024):** IA generativa aumenta produtividade em adultos
- **Howard-Jones (2014):** tecnologia em educação tem efeitos complexos
- **Diamond (2013):** FE são preditores de sucesso acadêmico
- **Skinner et al. (2009):** engajamento tripartite (comportamental, emocional, cognitivo)

**Gap:** Como IA se relaciona com FE em crianças? Mecanismos? Moderadores?

### 2.2. Teoria

**Modelo de mediação-moderação (Baron & Kenny, 1986; Hayes, 2017):**
- Mediação: M explica parte da relação X → Y
- Moderação: W muda a força/direção de X → Y

**Engajamento (Skinner et al., 2009):**
- Comportamental: frequência, intensidade
- Emocional: interesse, entusiasmo
- Cognitivo: estratégia, auto-regulação

**Letramento digital:**
- Capacidade de usar, entender e avaliar tecnologias
- Inclui aspectos técnicos, cognitivos, críticos

---

## 3. Método

### 3.1. Design

**Transversal correlacional com modelagem SEM.**

- Variável independente (X): uso de IA generativa
- Mediador (M): engajamento escolar
- Variável dependente (Y): funções executivas
- Moderador (W): letramento digital dos pais
- Controles: idade, sexo, SES, escola

### 3.2. Participantes

**N = 300-500** crianças

**Cálculo de poder (Notebook 08):**
- Detectar r ≥ 0.20 com power = 0.80
- 200 + para análise robusta
- 300-500 com margem para subgrupos

**Critérios:**
- 2º ao 5º ano, 7-11 anos
- Escolas públicas e privadas de Natal/RN
- Estratificação: tipo de escola (pública/privada), série (2º-5º)

**Recrutamento:**
- 5-8 escolas (3 públicas + 2-5 privadas)
- Amostra por conveniência + estratificação
- Compensação: certificado + devolutiva

### 3.3. Instrumentos

| Constructo | Instrumento | Respondente | Itens | Tempo |
|---|---|---|---|---|
| **Uso de IA (X)** | Questionário de uso (autorrelato) | Criança | 10 | 10 min |
| **Uso de IA (X)** | Questionário parental | Pais | 12 | 10 min |
| **Engajamento (M)** | Engagement vs. Disaffection Scale (EvsD) | Criança | 20 | 15 min |
| **FE (Y)** | BRIEF-2 (comportamental) | Pais | 86 | 15 min |
| **FE (Y)** | BRIEF-2 (comportamental) | Professores | 86 | 15 min |
| **FE (Y)** | Stroop Test (inibição) | Criança | — | 8 min |
| **FE (Y)** | Trail Making Test B | Criança | — | 5 min |
| **FE (Y)** | Digit Span (memória) | Criança | — | 10 min |
| **Letramento digital (W)** | Digital Literacy Scale | Pais | 15 | 10 min |
| **Controles** | Questionário demográfico | Pais | 10 | 10 min |

**Total por criança:** ~40 min (online + presencial)
**Total por família:** ~50 min (online)

### 3.4. Procedimento

```
Fase 1: Recrutamento (M1-M2)
  - Contato com escolas
  - Consentimento dos pais

Fase 2: Coleta Online (M3-M4)
  - Questionários pais (LimeSurvey/RedCap)
  - Questionários professores (LimeSurvey)
  - Link enviado por e-mail

Fase 3: Coleta Presencial (M5-M7)
  - Aplicação individual (40 min)
  - Aplicação coletiva (escola, para engajamento)

Fase 4: Análise (M8-M10)
  - Limpeza de dados
  - CFA → SEM
  - Sub-análises
```

### 3.5. Análise

**Etapa 1: Análise Fatorial Confirmatória (CFA)**
- Validar constructos latentes
- 3 indicadores por constructo
- Ajustar modelo (modificações justificadas)

**Etapa 2: Modelagem de Equações Estruturais (SEM)**
- Software: lavaan (R) ou semopy (Python)
- Estimador: ML robusto (MLM)
- Índices de ajuste: CFI > 0.95, TLI > 0.95, RMSEA < 0.06, SRMR < 0.08

**Etapa 3: Análise de Mediação**
- Indirect effect = a × b
- Bootstrap (5000 amostras) para IC 95%
- Teste de Sobel (complementar)

**Etapa 4: Análise de Moderação**
- Interação W × X
- Simple slopes (Hayes PROCESS Model 1)
- Visualização (Johnson-Neyman)

**Etapa 5: Análise de Subgrupos**
- Tipo de escola (pública vs privada)
- Série (2º/3º vs 4º/5º)
- Sexo

**Etapa 6: Análise de Robustez**
- Modelos com diferentes estimadores
- Análise de dados faltantes (FIML)
- Sensitivity analysis (outliers)

### 3.6. Análise de poder (simulação Monte Carlo)

- N = 500, 5000 replicações
- Detectar r = 0.20 com power = 0.95
- Detectar β = 0.15 com power = 0.80

---

## 4. Aspectos Éticos

- **CEP/UFRN** (submissão M0)
- **TCLE pais + TALE criança** (com pictogramas)
- **Sigilo:** códigos C001-C500
- **Direito de retirada** sem prejuízo
- **Devolutiva:** individual (relatório) + coletiva (palestra)
- **Comitê independente:** monitorar uso ético de dados de crianças

---

## 5. Limitações e Considerações

**Limitações:**
- **Transversal:** não permite inferência causal
- **Autorrelato:** viés de desejabilidade social
- **Amostra de conveniência:** limita generalização
- **Variabilidade no uso de IA:** medido por autorrelato

**Mitigações:**
- Múltiplos respondentes (pais + criança)
- Incluir medidas comportamentais (além de questionário)
- Análise estratificada por tipo de escola
- Triangulação de dados

---

## 6. Timeline

| Mês | Atividade |
|---|---|
| M0 | Submissão CEP |
| M1-M2 | Adaptação de instrumentos + tradução |
| M3-M5 | Coleta online (pais + professores) |
| M6-M7 | Coleta presencial (criança) |
| M8 | Limpeza + codificação |
| M9-M10 | CFA + SEM |
| M11 | Análise de subgrupos |
| M12-M14 | Manuscrito |
| M15 | Submissão Computers in Human Behavior |

---

## 7. Orçamento

| Item | Custo (R$) |
|---|---|
| Bolsista (15 meses) | 22.500 |
| Material participantes | 5.000 |
| Plataformas online (LimeSurvey Pro) | 2.000 |
| Tablets/cronômetros (testes) | 4.000 |
| Análise estatística (consultor SEM) | 5.000 |
| Tradução de instrumentos | 2.000 |
| Congresso | 5.000 |
| **Total** | **45.500** |

---

## 8. Resultados Esperados

**Baseado em simulação (Notebook 04):**

| Caminho | Estimativa | IC 95% |
|---|---|---|
| a (X→M) | 0.30 | [0.20, 0.40] |
| b (M→Y) | 0.40 | [0.30, 0.50] |
| c' (X→Y direto) | 0.10 | [0.00, 0.20] |
| Indireto (a×b) | 0.12 | [0.06, 0.18] |
| Total | 0.22 | [0.10, 0.34] |
| W×X | 0.15 | [0.05, 0.25] |

**Hipotetizados:**
- Mediação significativa
- Moderação por letramento digital dos pais
- Efeitos mais fortes em crianças mais velhas (4º/5º)

---

## 9. Plano de Disseminação

- **Manuscrito principal:** Computers in Human Behavior (A1, IF ~9.0)
- **Conferência:** SBP, ICIS
- **Devolutiva:** escolas + famílias
- **Dados:** OSF (CC0) + GitHub
- **Policy brief:** para Secretaria de Educação

---

## 10. Análise de Impacto

**Científico:**
- Primeiro estudo brasileiro com SEM + IA + FE em crianças
- Avanço no MToM (Machine Theory of Mind)
- Base para P05 (longitudinal)

**Social:**
- Subsídio para políticas educacionais
- Orientação para pais e professores
- Letramento digital crítico

**Educacional:**
- Design de plataformas de IA para crianças
- Treinamento de professores
- Currículo escolar

---

**Próxima revisão:** Após piloto N=20
**Status:** Aguardando CEP
