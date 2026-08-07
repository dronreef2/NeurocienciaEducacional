# 📝 Manuscrito P05 — Rascunho v1 (Template)

> **Título provisório:** "COORTE-INF: Desenvolvimento de funções executivas e letramento dos 7 aos 11 anos — estudo longitudinal com 5 ondas e sub-estudo EEG"
> **Versão:** Rascunho v1 (2026-08-06) — Template
> **Autores:** [Seu nome]¹, Ângela M. C. Naschold², Antonio Pereira³, [Co-autores coorte]
> **Afiliação:** ¹PPGED/UFRN, ²CERES/UFRN, ³ICe/UFRN

---

## Abstract (250 palavras)

**Background:** O desenvolvimento das funções executivas (FE) durante a infância é crucial para o sucesso acadêmico, mas as trajetórias individuais e suas relações com letramento e tecnologia são pouco compreendidas.

**Objetivo:** Investigar trajetórias de FE e letramento dos 7 aos 11 anos, suas relações bidirecionais, e marcadores neurais (N170, P300) numa coorte longitudinal com 5 ondas anuais.

**Método:** Coorte prospectiva com 200 crianças recrutadas aos 7 anos (2º ano), acompanhadas anualmente por 5 anos (T1=7a, T5=11a). FE avaliada com BRIEF-2, Stroop, e Trail Making Test. Letramento com PROLETRAMENTO. Sub-estudo EEG (N=50) aos 9 e 11 anos com paradigma de leitura. Análise: Latent Growth Curve Models (LGCM), cross-lagged panel models (CLPM), e Random-Intercept CLPM para separar within/between.

**Resultados esperados:** Espera-se crescimento médio de 0.5-1.0 desvio-padrão em FE por ano, com variabilidade individual substancial. Relações bidirecionais FE ↔ Letramento (β ≈ 0.30-0.40). N170 diminui com idade (maior automaticidade).

**Conclusões:** [A ser preenchido]

**Palavras-chave:** longitudinal; desenvolvimento; funções executivas; letramento; EEG; LGCM; CLPM.

---

## 1. Introdução

### 1.1. Contexto
- Infância dos 7-11 anos: período crítico para FE (Diamond, 2013)
- BNCC: foco em alfabetização nos anos iniciais
- Crescimento de uso de tecnologia (telas, IA) durante esse período

### 1.2. Teoria
- **Modelo de investimento:** FE predizem letramento (Cartwright, 2012)
- **Modelo de letramento-maturacional:** letramento modifica FE (Skibbe et al., 2019)
- **Bidirecionalidade:** FE ↔ Letramento (Shaul & Schwartz, 2014)
- **Marcadores neurais:** N170 decresce em amplitude (negatividade) com expertise de leitura (Maurer et al., 2005)

### 1.3. Estado da arte
- Estudos longitudinais: poucos, americanos/europeus
- Brasil: raros com 5+ ondas
- Sub-estudo EEG em coorte: praticamente inexistente

### 1.4. Pergunta
> Como se desenvolvem as FE e o letramento dos 7 aos 11 anos, e qual a natureza das relações bidirecionais entre eles? Marcadores neurais acompanham esse desenvolvimento?

### 1.5. Hipóteses
- H1: FE crescem em média 0.5-1.0 DP/ano (mas com variabilidade)
- H2: FE(T) → Letramento(T+1) (efeito preditivo)
- H3: Letramento(T) → FE(T+1) (efeito reverso)
- H4: N170 torna-se mais negativo com idade (expertise)

---

## 2. Método

### 2.1. Design
- Coorte prospectiva longitudinal
- 5 ondas anuais (T1, T2, T3, T4, T5)
- Sub-estudo EEG em T3 (9 anos) e T5 (11 anos)

### 2.2. Participantes
- N inicial = 200 (250 com margem para attrition de 20%)
- Idade inicial: 7-8 anos (2º ano)
- 10 escolas de Natal/RN
- Critérios: sem condições neurológicas, consentimento

### 2.3. Instrumentos

**Por onda (todos os 5):**
- BRIEF-2 (pais + professores)
- Stroop Test (criança)
- Trail Making Test A e B
- PROLETRAMENTO
- Questionário de uso de tecnologia

**Ondas específicas:**
- T1: baseline completo + DNA (saliva) para polimorfismos
- T3: EEG sub-estudo (N=50) + questionário de IA
- T5: EEG sub-estudo (mesmas crianças) + ressonância (N=20, opcional)

### 2.4. Procedimento

1. **T1 (M0-M3):** baseline, recrutamento intensivo
2. **T2-T5 (cada 12 meses):** avaliações
3. **Estratégias de retenção:**
   - Presentes aniversário
   - Newsletter semestral
   - Devolutiva individual
   - Compensação por tempo (R$ 50/vale-presente)

### 2.5. Análise

**LGCM (Latent Growth Curve Model):**
- Fator intercepto (nível inicial)
- Fator slope (crescimento linear)
- Variâncias para ambos
- Covariância intercept-slope

**CLPM (Cross-Lagged Panel Model):**
- 4 transições: T1→T2, T2→T3, T3→T4, T4→T5
- Efeitos autorregressivos (estabilidade)
- Efeitos cross-lagged (X→Y, Y→X)

**RI-CLPM (Hamaker et al., 2015):**
- Separa within-person de between-person
- Controla por traços estáveis

**Análise EEG (sub-estudo):**
- Comparação T3 vs. T5 (within-subject)
- Componentes N170, P300
- Análise por cluster temporal

---

## 3. Resultados (template)

### 3.1. Retenção

| Onda | N esperado | N real | % retenção |
|---|---|---|---|
| T1 | 200 | 200 | 100% |
| T2 | 200 | 188 | 94% |
| T3 | 200 | 178 | 89% |
| T4 | 200 | 165 | 83% |
| T5 | 200 | 152 | 76% |

### 3.2. LGCM — Trajetórias de FE

**Inibição (BRIEF-2):**
- Intercepto: M = 55.2, V = 80.4 (σ = 8.97)
- Slope: M = -3.5/ano, V = 12.0 (σ = 3.46)
- Correlação intercept-slope: r = -0.30
- **Interpretação:** FE melhoram em média 3.5 pontos/ano; crianças com FE inicial menor têm mais rápido crescimento (efeito de regressão)

**Letramento:**
- Intercepto: M = 50 palavras/min
- Slope: M = +15 palavras/ano

### 3.3. CLPM — Relações bidirecionais

**Caminhos médios (padronizados):**

| Efeito | T1→T2 | T2→T3 | T3→T4 | T4→T5 | Média |
|---|---|---|---|---|---|
| FE → Letramento | 0.32** | 0.28** | 0.25** | 0.22* | 0.27 |
| Letramento → FE | 0.18* | 0.20* | 0.22* | 0.19* | 0.20 |

**Conclusão:** Efeitos bidirecionais, com FE → Letramento mais forte.

### 3.4. RI-CLPM

Separa within-person (efeito de mudanças dentro do indivíduo) de between-person (efeito de traço):

- Within: FE↑ → Letramento↑ (β = 0.15)
- Between: nível de FE correlaciona com nível de letramento (r = 0.45)

### 3.5. Sub-estudo EEG

| Componente | T3 (9a) | T5 (11a) | t(49) | p | d |
|---|---|---|---|---|---|
| N170 amplitude | -2.8 μV | -3.7 μV | 3.2 | .002 | 0.45 |
| N170 latência | 195 ms | 178 ms | -2.8 | .007 | -0.40 |
| P300 amplitude | 4.9 μV | 5.8 μV | 2.1 | .04 | 0.30 |

**Conclusão:** N170 torna-se mais negativo e mais rápido com idade (expertise).

---

## 4. Discussão (template)

### 4.1. Trajetórias heterogêneas
- Subgrupos: crescimento rápido, típico, lento
- LGMM (Growth Mixture Modeling) pode identificar 2-3 classes

### 4.2. Bidirecionalidade
- Suporte para modelo bidirecional
- Mas: FE prediz letramento mais fortemente
- Implicação: intervir em FE pode melhorar letramento

### 4.3. Marcadores neurais
- N170 segue expertise hypothesis
- Pode ser biomarcador precoce de risco de dislexia

### 4.4. Implicações
- Triagem precoce baseada em FE + EEG
- Intervenções em 2º/3º ano (janela de plasticidade)
- Diferenciação por subgrupo

### 4.5. Limitações
- Attrition (24% em 5 anos)
- Amostra urbana
- EEG sub-estudo pequeno

---

## 5. Conclusões

[A ser preenchido]

---

## Timeline (5 anos)

- **Ano 1 (M0-M12):** CEP + recrutamento + T1
- **Ano 2 (M13-M24):** T2 + análises interim
- **Ano 3 (M25-M36):** T3 + EEG sub-estudo
- **Ano 4 (M37-M48):** T4
- **Ano 5 (M49-M60):** T5 + EEG + manuscritos

**Manuscritos planejados:**
- M1: artigo transversal baseline
- M2: artigo LGCM (após T3)
- M3: artigo CLPM (após T4)
- M4: artigo EEG (após T5)
- M5: artigo final integração

**Revistas-alvo:**
- M3, M4: *Developmental Cognitive Neuroscience* (A1)
- M5: *Child Development* (A1)
