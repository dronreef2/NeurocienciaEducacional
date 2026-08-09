# 📋 P05 — Protocolo Detalhado

> **Título:** COORTE-INF: Desenvolvimento cognitivo, neural e educacional dos 7 aos 11 anos — coorte longitudinal com 5 ondas e sub-estudo EEG
> **Versão:** 2.0 (2026-08-08)
> **Pesquisador principal:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela M. C. Naschold
> **Co-orientador:** Prof. Dr. Antonio Pereira (ICe/UFRN)
> **Status:** Aguardando submissão CEP

---

## 1. Resumo

### 1.1. Pergunta de pesquisa
> Como se desenvolvem as funções executivas (FE) e o letramento dos 7 aos 11 anos, e qual a natureza das relações bidirecionais entre eles? Como os marcadores neurais (N170, P300) acompanham esse desenvolvimento?

### 1.2. Hipóteses
- **H1:** FE crescem em média 0.5-1.0 DP por ano, com variabilidade individual substancial
- **H2:** FE(T) prediz Letramento(T+1) (efeito preditivo)
- **H3:** Letramento(T) prediz FE(T+1) (efeito reverso, bidirecional)
- **H4:** N170 torna-se mais negativo e mais rápido com idade (expertise)

---

## 2. Background

### 2.1. Modelos teóricos

**Modelo de investimento (Cartwright, 2012):**
- FE predizem aquisição de letramento
- Crianças com FE melhores aprendem a ler mais rápido

**Modelo maturacional-letrado (Skibbe et al., 2019):**
- Exposição à leitura modifica FE
- Especialmente em ambientes letrados

**Modelo bidirecional (Shaul & Schwartz, 2014):**
- FE ↔ Letramento (relação recíproca)
- Importante distinguir within vs between

**Marcadores neurais (Maurer et al., 2005):**
- N170 emerge com a leitura
- Mais negativo com expertise
- Pode predizer dificuldade de leitura

### 2.2. Estado da arte

- **Estudos longitudinais com FE:** raros, N grande (>500), poucos no Brasil
- **Estudos EEG longitudinais:** virtualmente inexistentes
- **Bidirecionalidade FE-letramento:** ainda em debate
- **Brazilian context:** escassos estudos com 5+ ondas

---

## 3. Método

### 3.1. Design

**Coorte prospectiva longitudinal:**
- 5 ondas anuais (T1, T2, T3, T4, T5)
- Início: 2º ano (7-8 anos)
- Duração: 5 anos (até 5º/6º ano)

**Sub-estudo EEG:**
- 2 ondas: T3 (9 anos) e T5 (11 anos)
- N = 50 (sub-amostra)

### 3.2. Participantes

**N inicial = 200** (com margem de 20% para atrito, total 250)

- Idade inicial: 7-8 anos
- 2º ano de 10 escolas públicas
- 25 crianças por escola (5 por série)

**Critérios de inclusão:**
- Matriculados no 2º ano em 2026
- Sem condições neurológicas/genéticas
- Consentimento parental + assentimento infantil

**Critérios de exclusão:**
- Atraso no desenvolvimento
- Deficiência sensorial não corrigida
- Uso de medicação psicoativa contínua

### 3.3. Instrumentos

**Por onda (todos os 5):**
| Instrumento | Constructo | Tempo |
|---|---|---|
| BRIEF-2 (pais) | FE comportamental | 15 min |
| BRIEF-2 (professores) | FE comportamental | 15 min |
| Stroop Test | Inibição | 8 min |
| Trail Making Test A e B | Atenção/Flexibilidade | 10 min |
| Digit Span (WISC) | Memória de trabalho | 10 min |
| PROLETRAMENTO | Leitura | 20 min |
| Questionário tecnologia | Uso de telas/IA | 10 min |
| Questionário contexto | Família, SES | 15 min |

**T1 apenas:**
- DNA (saliva) para polimorfismos (opcional, com consentimento adicional)
- Avaliação cognitiva completa (WISC subtests)

**T3 e T5 (sub-estudo EEG, N=50):**
- EEG (32 canais)
- Paradigma de leitura (palavras vs. pseudopalavras)
- 1 sessão adicional de 45 min

### 3.4. Procedimento

**T1 (M0-M3, baseline):**
- Recrutamento intensivo
- Avaliação completa
- Randomização para sub-estudo EEG (50 selecionados)

**T2-T5 (cada 12 meses):**
- Re-avaliação
- Janela de 3 meses por onda

**Estratégias de retenção:**
- Presentes aniversário (R$ 30)
- Newsletter semestral
- Devolutiva individual anual
- Compensação por tempo (R$ 50 por onda)
- Flexibilidade de horário

### 3.5. Análise

**LGCM (Latent Growth Curve Model):**
- Intercept (nível inicial)
- Slope linear (crescimento médio)
- Slope quadrático (curvatura)
- Variâncias: permite heterogeneidade
- Covariância intercept-slope

**CLPM (Cross-Lagged Panel Model):**
- 4 transições: T1→T2, T2→T3, T3→T4, T4→T5
- Efeitos auto-regressivos (estabilidade)
- Efeitos cross-lagged (X→Y, Y→X)

**RI-CLPM (Hamaker et al., 2015):**
- Separa within-person (variação dentro do indivíduo)
- De between-person (traço estável)
- Controla por fatores genéticos não-medidos

**LGMM (Latent Growth Mixture Model):**
- Identifica subgrupos de trajetórias
- 2-4 classes esperadas

**Análise EEG:**
- Comparação T3 vs. T5 (within-subject)
- Componentes N170, P300
- Análise por cluster temporal

**Software:**
- R: lavaan, OpenMx, tidySEM
- Python: MNE-Python, statsmodels

---

## 4. Aspectos Éticos

- **CEP/UFRN** (submissão M0)
- **TCLE + TALE** anuais (re-consentimento em cada onda)
- **Sigilo de DNA:** armazenamento codificado, sem identificação pessoal
- **Devolutiva anual:** individual + coletiva
- **Comitê independente:** monitorar bem-estar
- **Critérios de interrupção:** se atrito > 30% ou problema ético

---

## 5. Análise de Poder

**LGCM (N=200):**
- Detectar slope médio com power = 0.80
- Variância do slope: detectável com r = 0.30

**CLPM (N=200, 4 transições):**
- Detectar β = 0.20 com power = 0.80
- Efeitos pequenos a médios

**Sub-estudo EEG (N=50):**
- Detectar d = 0.40 com power = 0.80
- Comparação T3 vs T5 (within)

---

## 6. Limitações

- **Atrito:** 20-30% em 5 anos (realista)
- **Amostra urbana:** generalização limitada
- **Custo:** alto (5 anos, EEG, sub-estudo)
- **Avaliação de EEG:** apenas 2 ondas (limitado)
- **Viés de história:** pandemia, políticas educacionais

---

## 7. Timeline (5 anos)

```
2026 (M0-M12):
  M0: Submissão CEP
  M1-M3: Recrutamento (N=200)
  M4-M9: Onda T1 (baseline completo)
  M10-M12: Análise T1 + planejamento EEG

2027 (M13-M24):
  M13-M18: Onda T2
  M19-M24: Análise T1-T2 (manuscrito 1)

2028 (M25-M36):
  M25-M30: Onda T3
  M31-M33: Sub-estudo EEG T3
  M34-M36: Análise T1-T3 (manuscrito 2)

2029 (M37-M48):
  M37-M42: Onda T4
  M43-M48: Análise intermediária

2030 (M49-M60):
  M49-M54: Onda T5
  M55-M57: Sub-estudo EEG T5
  M58-M60: Análise final + manuscritos
```

---

## 8. Orçamento (5 anos)

| Item | Custo (R$) |
|---|---|
| Bolsistas (2 × 60 meses) | 168.000 |
| Material participantes (200 × 5 ondas) | 30.000 |
| EEG (manutenção + periféricos) | 25.000 |
| Análises estatísticas (consultores) | 15.000 |
| Congressos (3 × R$ 8.000) | 24.000 |
| Publicação Open Access (5 artigos) | 25.000 |
| Equipe de campo (5 anos) | 60.000 |
| Software (licenças) | 10.000 |
| Infraestrutura (sala, internet) | 12.000 |
| **Total** | **~370.000** |

**Fontes potenciais:** CAPES, FAPERN, CNPq, UFRN, ICe

---

## 9. Manuscritos Planejados (5+)

1. **Baseline (M12):** Prevalência de FE e letramento aos 7 anos
2. **LGCM (M24):** Trajetórias de crescimento (2 ondas)
3. **CLPM (M36):** Bidirecionalidade FE ↔ Letramento (3 ondas)
4. **RI-CLPM (M48):** Separação within/between
5. **EEG (M54):** Marcadores neurais em 2 ondas
6. **Final (M60):** Integração, 5 ondas, EEG

**Revistas-alvo:**
- Child Development (A1, IF ~5.0)
- Developmental Cognitive Neuroscience (A1, IF ~4.5)
- Journal of Educational Psychology (A1, IF ~5.0)
- Scientific Studies of Reading (A1, IF ~3.0)

---

## 10. Disseminação e Impacto

- **Acadêmica:** 5+ manuscritos em revistas A1
- **Conferências:** SBP, ICIS, SRCD
- **Política pública:** subsídios para BNCC, política de alfabetização
- **Escolas:** relatórios + treinamentos
- **Comunidade:** eventos abertos, podcasts
- **Dados:** OpenNeuro + OSF (aberto)

---

## 11. Equipe

- **Coordenação:** Profa. Ângela Naschold (UFRN/CERES)
- **Co-orientação:** Prof. Antonio Pereira (ICe)
- **Pesquisador principal:** [Seu nome] (mestrando PPGED)
- **Bolsistas IC:** 2-3 alunos
- **Estatístico:** consultor (R + Python)
- **Neuropsicólogo:** avaliação infantil
- **Tecnólogos EEG:** 1-2

---

**Próxima revisão:** Após aprovação CEP
**Status:** Aguardando CEP
