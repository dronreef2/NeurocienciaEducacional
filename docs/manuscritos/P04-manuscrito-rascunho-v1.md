# 📝 Manuscrito P04 — Rascunho v1 (Template)

> **Título provisório:** "Uso de IA generativa e funções executivas em crianças do 2º ao 5º ano: mediação por engajamento e moderação por letramento digital"
> **Versão:** Rascunho v1 (2026-08-06) — Template
> **Autores:** [Seu nome]¹, Ângela M. C. Naschold²
> **Afiliação:** ¹PPGED/UFRN, ²CERES/UFRN

---

## Abstract (250 palavras)

**Background:** O uso de IA generativa por crianças cresce rapidamente, mas pouco se sabe sobre suas relações com funções executivas (FE) e os mecanismos envolvidos.

**Objetivo:** Testar um modelo de mediação-moderação em que o uso de IA generativa (X) afeta FE (Y) através do engajamento escolar (M), moderado pelo letramento digital dos pais (W).

**Método:** Estudo transversal com 300-500 crianças do 2º ao 5º ano de escolas públicas e privadas de Natal/RN. Instrumentos: questionário de uso de IA, BRIEF-2 (FE), Engagement vs. Disaffection Scale, questionário de letramento digital dos pais. Análise por Modelagem de Equações Estruturais (SEM) com lavaan (R).

**Resultados esperados:** Espera-se que o uso de IA tenha efeito positivo direto pequeno em FE (c' ≈ 0.10-0.20), mediado por engajamento (β_XM ≈ 0.30, β_MY ≈ 0.40), e que o letramento digital dos pais module a relação (efeito W×X significativo).

**Conclusões:** [A ser preenchido]

**Palavras-chave:** IA generativa; funções executivas; mediação; moderação; SEM; crianças.

---

## 1. Introdução

### 1.1. Contexto
- 50%+ das crianças usam alguma forma de IA (Common Sense Media, 2024)
- BNCC inclui pensamento computacional
- Funções executivas: preditores de sucesso acadêmico (Diamond, 2013)

### 1.2. Teoria
- **Modelo de mediação-moderação:** Baron & Kenny (1986); Hayes (2017)
- **Engajamento:** comportamental, emocional, cognitivo (Skinner et al., 2009)
- **Letramento digital:** capacidade de usar, entender e avaliar tecnologias digitais

### 1.3. Estado da arte
- Estudos com adultos: IA aumenta produtividade (Mollick, 2024)
- Estudos com crianças: escassos
- **Gap:** como IA se relaciona com FE? Engajamento medeia? Letramento digital modera?

### 1.4. Pergunta
> O uso de IA generativa afeta funções executivas de crianças, e essa relação é mediada por engajamento e moderada por letramento digital dos pais?

### 1.5. Hipóteses
- H1: Uso de IA → Engajamento (efeito positivo)
- H2: Engajamento → FE (efeito positivo)
- H3: Uso de IA → FE (efeito direto, menor)
- H4: Letramento digital dos pais modera a relação (W × X significativo)

---

## 2. Método

### 2.1. Design
- Transversal correlacional
- Modelo SEM: X (uso IA) → M (engajamento) → Y (FE), com moderador W (letramento digital dos pais)

### 2.2. Participantes
- N = 300-500 crianças (cálculo de poder: 80% para detectar r ≥ 0.20)
- 2º ao 5º ano, 7-11 anos
- Escolas públicas e privadas de Natal/RN
- Estratificação: tipo de escola, série

### 2.3. Instrumentos

| Constructo | Instrumento | Itens |
|---|---|---|
| Uso de IA (X) | Questionário de uso de IA (autorrelato + parental) | 10 |
| Engajamento (M) | Engagement vs. Disaffection Scale (EvsD) | 20 |
| FE (Y) | BRIEF-2 (pais + professores) | 86 |
| Letramento digital (W) | Digital Literacy Scale (DLS) — pais | 15 |
| Controles | Idade, sexo, SES, escola | — |

### 2.4. Procedimento
1. Recrutamento em 5-8 escolas
2. Coleta online (LimeSurvey/RedCap) para pais e professores
3. Coleta presencial (40 min) para crianças
4. Compensação: certificado + devolutiva

### 2.5. Análise
- **Análise fatorial confirmatória (CFA):** validar constructos
- **Modelagem de Equações Estruturais (SEM):** lavaan (R)
- **Moderação:** interação W × X no modelo
- **Índices de ajuste:** CFI > 0.95, RMSEA < 0.06, SRMR < 0.08
- **Análise de poder:** simulação Monte Carlo (n = 10000)

---

## 3. Resultados (template)

### 3.1. Estatísticas descritivas

| Variável | M | DP | Min | Max |
|---|---|---|---|---|
| Idade | 9.2 | 1.3 | 7 | 11 |
| Uso de IA (horas/sem) | 4.5 | 3.2 | 0 | 20 |
| Engajamento | 3.8 | 0.7 | 1.5 | 5.0 |
| FE (BRIEF-2 GEC) | 52.3 | 11.5 | 35 | 85 |
| Letramento digital pais | 3.2 | 0.8 | 1 | 5 |

### 3.2. Correlações

| | Uso IA | Engaj. | FE | Letram. |
|---|---|---|---|---|
| Uso IA | 1.00 | | | |
| Engajamento | 0.32** | 1.00 | | |
| FE | 0.15** | 0.45** | 1.00 | |
| Letramento | 0.40** | 0.18** | 0.10* | 1.00 |

### 3.3. Modelo SEM

```
   Uso_IA (X) ──a──> Engajamento (M) ──b──> FE (Y)
       │              │                       ↑
       │              │                       │
       c' (direto)────┴───────────────────────┤
       │                                      │
       └────── d (interação) ─────────────────┘
            (W: Letramento)
```

**Coeficientes padronizados:**

| Caminho | β | EP | IC 95% | p |
|---|---|---|---|---|
| a (X → M) | 0.32 | 0.04 | [0.24, 0.40] | <.001 |
| b (M → Y) | 0.43 | 0.04 | [0.35, 0.51] | <.001 |
| c' (X → Y direto) | 0.12 | 0.05 | [0.02, 0.22] | .019 |
| Efeito indireto (a*b) | 0.138 | — | [0.10, 0.18] | <.001 |
| Moderação (W × X) | 0.18 | 0.06 | [0.06, 0.30] | .003 |

**Índices de ajuste:**
- χ²/df = 2.34
- CFI = 0.962
- TLI = 0.955
- RMSEA = 0.048 [0.040, 0.056]
- SRMR = 0.045

### 3.4. Análise de subgrupos

- Tipo de escola (pública vs. privada): diferença significativa?
- Ano escolar: efeito maior em 2º/3º vs. 4º/5º?

---

## 4. Discussão (template)

### 4.1. Suporte para H1-H3
- Efeito direto pequeno, mas significativo
- Mediação substancial via engajamento
- Consistente com literatura (Hamari et al., 2014)

### 4.2. Moderação por letramento digital
- Pais com maior letramento digital: filhos têm maior benefício do uso de IA
- Pais com menor letramento: filhos podem usar IA de forma menos eficaz
- Implicações para equidade

### 4.3. Implicações teóricas
- Engajamento é mecanismo proximal
- Uso de IA não substitui mediação parental
- Modelo TEM que considerar contexto

### 4.4. Implicações práticas
- Escolas: treinar pais em letramento digital
- Plataformas: tornar erros visíveis (calibração de confiança)
- Políticas: equidade de acesso

### 4.5. Limitações
- Design transversal (sem causalidade)
- Autorrelato (viés de desejabilidade social)
- Amostra de conveniência

---

## 5. Conclusões

[A ser preenchido]

---

## Timeline

- M0-M2: CEP + adaptação de instrumentos
- M3-M5: Coleta
- M6-M9: Análise (CFA + SEM)
- M10-M12: Manuscrito
- M13: Submissão

**Revista-alvo:** *Computers in Human Behavior* (Qualis A1, IF ~9.0)
