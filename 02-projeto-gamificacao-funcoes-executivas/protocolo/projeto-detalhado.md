# 📋 P02 — Protocolo Detalhado

> **Título:** Efeitos de elementos de gamificação adaptativa sobre funções executivas em crianças do 2º ao 5º ano: ensaio controlado randomizado 2×4
> **Versão:** 2.0 (2026-08-08)
> **Pesquisador principal:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela M. C. Naschold
> **Status:** Aguardando submissão CEP

---

## 1. Resumo

### 1.1. Pergunta de pesquisa
> Como diferentes elementos de gamificação (pontos, badges, narrativas, avatares) afetam as funções executivas (inibição, flexibilidade cognitiva, memória de trabalho) em crianças do 2º ao 5º ano?

### 1.2. Hipóteses
- **H1:** Crianças no grupo gamificado apresentarão maior ganho em inibição (BRIEF-2 Inibição) que o grupo controle (d = 0.35-0.50).
- **H2:** Narrativas + avatares produzem efeito aditivo sobre pontos + badges (interação 2×4 significativa).
- **H3:** Efeitos serão mediados por engajamento escolar (Hayes PROCESS Model 4).
- **H4 (exploratória):** Efeitos serão modulados por idade (crianças mais velhas se beneficiam mais de elementos narrativos).

---

## 2. Background e Justificativa

### 2.1. Estado da arte

**Meta-análise de Hamari et al. (2014):**
- Gamificação → engajamento: r ≈ 0.40
- Maior efeito em elementos de imersão narrativa
- Variabilidade significativa entre tipos de elemento

**Estudos recentes em crianças:**
- Mekler et al. (2017): badges têm efeito limitado
- Koivisto & Hamari (2019): narrativas > pontos para engajamento profundo
- Toda et al. (2019): efeitos diferenciais por idade

**Gap:** Poucos estudos com crianças pequenas em contexto brasileiro; nenhum comparando 4 elementos em ECR.

### 2.2. Teoria

**Teoria da Autodeterminação (Deci & Ryan, 2000):**
- Motivação intrínseca: autonomia, competência, pertencimento
- Narrativas atendem a "pertencimento" (storytelling)
- Avatares atendem a "autonomia" (identidade)
- Pontos/badges atendem a "competência" (reconhecimento)

**Modelo de Diamond (2013) sobre FE:**
- Inibição: controlada por atenção
- Flexibilidade: switching entre tarefas
- Memória de trabalho: capacidade limitada

---

## 3. Método

### 3.1. Design

**Ensaio controlado randomizado (ECR) com design fatorial 2 × 4:**

|  | Elemento 1 | Elemento 2 | Elemento 3 | Elemento 4 |
|---|---|---|---|---|
| **Plataforma 1 (Tradicional)** | Controle (sem elemento) | — | — | — |
| **Plataforma 2 (Gamificada)** | Pontos | Badges | Narrativas | Avatares |

Total: 5 condições × 40 crianças = **200 crianças**

### 3.2. Randomização

- **Estratificação:** escola (4 escolas) e série (2º-5º)
- **Blocos permutados** dentro de cada estrato
- **Alocação oculta:** pesquisador cego ao processo de randomização

### 3.3. Participantes

**N = 200**, divididos em:
- 50 crianças: **Controle** (plataforma tradicional)
- 150 crianças: **Gamificado** (4 elementos × 37-38)

**Critérios de inclusão:**
- 2º ao 5º ano, 7-11 anos
- Sem diagnóstico neurológico/psiquiátrico
- Consentimento parental + assentimento infantil

**Critérios de exclusão:**
- Uso atual de medicação psicoativa
- Repetência de 2+ séries
- Atraso no desenvolvimento conhecido

### 3.4. Instrumentos

| Constructo | Instrumento | Avalia | Tempo |
|---|---|---|---|
| **Inibição** | BRIEF-2 (Inibição) | FE comportamental (pais) | 10 min |
| **Inibição** | Stroop Test | FE atencional (criança) | 8 min |
| **Flexibilidade** | Trail Making Test B | FE (criança) | 5 min |
| **Memória de trabalho** | Digit Span (WISC) | FE (criança) | 10 min |
| **Engajamento** | EvsD Scale | Engajamento escolar | 8 min |
| **Controle** | Questionário pais | Idade, sexo, SES | 10 min |

**Total:** ~50 min por criança, dividido em 2 sessões

### 3.5. Procedimento

```
T0 (Baseline, M0):
  - Questionários pais (online)
  - Testes FE (individual, ~30 min)
  - Randomização
  ↓
Intervenção (M1-M8, 8 semanas):
  - 3 sessões/semana × 30 min
  - Plataforma: tradicional vs gamificada
  - Monitoramento de engajamento
  ↓
T1 (Pós-intervenção, M9):
  - Re-teste FE (todos instrumentos)
  - Questionário engajamento
  ↓
T2 (Follow-up 3 meses, M12):
  - Re-teste FE
  - Questionário pais
```

### 3.6. Análise

**Análise primária:** ANOVA mista 2 (plataforma) × 4 (elemento) × 2 (tempo)

**Análise secundária:** ANCOVA com pré-teste como covariável

**Análise de mediação:** Hayes PROCESS Model 4 (engajamento como mediador)

**Tamanho de efeito:** η² parcial, Cohen's d para comparações

**Software:** R (afex + emmeans), Python (statsmodels)

---

## 4. Aspectos Éticos

- Submissão CEP/UFRN (M0)
- TCLE pais + TALE criança (com pictogramas)
- Anonimização: códigos C01-C200
- Direito de retirada sem prejuízo
- Devolutiva individual + coletiva
- Cuidado especial: não expor grupo controle à condição gamificada

---

## 5. Limitações e Considerações

- **Saliência de Hawthorne:** crianças em pesquisa se comportam diferente
- **Efeito de novidade:** primeiras semanas podem ter viés
- **Diferenças culturais:** elementos podem ter efeito diferente por região
- **Sazonalidade:** evitar coletas em férias

---

## 6. Timeline

| Mês | Atividade |
|---|---|
| M0 | Submissão CEP |
| M1-M2 | Recrutamento + T0 |
| M3-M10 | Intervenção (8 semanas) |
| M11 | T1 (pós-teste) |
| M12 | T2 (follow-up) |
| M13-M14 | Análise |
| M15-M17 | Manuscrito |
| M18 | Submissão J Educational Psychology |

---

## 7. Orçamento

| Item | Custo (R$) |
|---|---|
| Bolsista (8 meses) | 12.000 |
| Material para escolas | 3.000 |
| Plataformas (licenças) | 2.000 |
| Análise estatística | 1.000 |
| Tradução de manuscrito | 2.000 |
| Congresso (apresentação) | 5.000 |
| **Total** | **25.000** |

---

## 8. Resultados Esperados

**Baseado em meta-análise (Hamari 2014):**
- Efeito médio: d ≈ 0.35
- Variabilidade: depende do elemento
- Interação narrativa × idade: r ≈ 0.20

**Poder estatístico (N=200):**
- Detectar d = 0.35 com power = 0.80 (α = 0.05)
- Efeito pequeno a médio detectável

---

## 9. Plano de Disseminação

- **Manuscrito:** Journal of Educational Psychology (A1)
- **Conferência:** SBP (Sociedade Brasileira de Psicologia)
- **Devolutiva:** Escolas participantes (relatório + palestra)
- **Dados:** OSF + GitHub (aberto)
- **Materiais:** Guia para pais sobre gamificação saudável

---

**Próxima revisão:** Após coleta piloto (N=10)
**Status:** Aguardando CEP
