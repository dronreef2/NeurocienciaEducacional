# 📊 Tabela de Hipóteses — 5 Projetos

> **Tabela consolidada de todas as hipóteses dos 5 projetos do programa**
> **Atualizado em:** 2026-08-12
> **Total:** 27 hipóteses (H1, H2, H3... com sub-hipóteses)

---

## 🎯 Visão Geral

| Projeto | Método | N | Hipóteses | Pré-registro |
|---|---|---|---|---|
| **P01** | Qualitativo (ATR) | 12-15 | 5 (exploratórias) | [OSF](../osf-json/P01-osf.json) |
| **P02** | ECR 2×4 | 200 | 4 | [OSF](../osf-json/P02-osf.json) |
| **P03** | EEG (32-ch) | 60 | 5 | [OSF](../osf-json/P03-osf.json) |
| **P04** | SEM transversal | 300-500 | 5 | [OSF](../osf-json/P04-osf.json) |
| **P05** | LGCM longitudinal | 200 | 4 | [OSF](../osf-json/P05-osf.json) |

---

## 📋 P01 — IA Generativa e Cognição de Teoria da Mente (Qualitativo)

**Pergunta:** Que MToM crianças de 7-11 anos constroem em relação a GenAIs?

| ID | Hipótese | Variáveis | Método | Resultado esperado | Status |
|---|---|---|---|---|---|
| H1.1 | A MToM varia com a idade | MToM × Idade | Análise Temática | Crianças mais velhas = MToM mais baixa | ⏳ A testar |
| H1.2 | A MToM decai com a experiência | MToM × Dia | Análise Temática Longitudinal | Decay significativo (piloto: ρ=-0.85) | ⏳ A confirmar |
| H1.3 | Existem 5+ temas principais | — | ATR (Braun-Clarke 2022) | 5 temas: Antrop., Detecção, Confiança, Comparação, Preferência | ✅ Piloto: 5 temas |
| H1.4 | Há variabilidade individual | MToM × Criança | Mixed Models | Efeito aleatório significativo | ✅ Piloto: Pedro +4.84 |
| H1.5 | Padrões emergem de interações | Código × Código | Análise de Rede | Clusters temáticos | ✅ Piloto: 2 comunidades |

**Análise estatística:**
- Teste binomial (MToM ≠ 0.5)
- Spearman (dia × MToM)
- Mann-Kendall (tendência)
- Qui² (idade × MToM)
- Mixed models (efeitos aleatórios)

---

## 📋 P02 — Gamificação e FE (ECR 2×4)

**Pergunta:** A gamificação (pontos + narrativa) melhora FE em crianças?

**Design:** ECR fatorial 2 (Pontos: sim/não) × 2 (Narrativa: sim/não)

| ID | Hipótese | Variável Dependente | Efeito | Tamanho | Status |
|---|---|---|---|---|---|
| H2.1 | Pontos melhoram atenção sustentada | Stroop (inibição) | β ≈ 0.20 | d = 0.20 | ⏳ A testar |
| H2.2 | Narrativa melhora memória de trabalho | Digit Span | β ≈ 0.25 | d = 0.25 | ⏳ A testar |
| H2.3 | Combinação (P×N) tem efeito aditivo | TMT-B (flexibilidade) | β ≈ 0.35 | d = 0.35 | ⏳ A testar |
| H2.4 | Efeitos mediados por engajamento | M (engajamento) | a×b ≠ 0 | — | ⏳ A testar |

**Análise estatística:**
- ANCOVA (2×4 com pré-teste)
- Modelos mistos
- Análise de mediação (Hayes PROCESS)
- Simulação Monte Carlo (poder)

**Grupos:**
1. Controle (sem gamificação)
2. Pontos apenas
3. Narrativa apenas
4. Pontos + Narrativa

---

## 📋 P03 — IA Generativa e Leitura (EEG)

**Pergunta:** Como a leitura em tela vs papel modula o processamento neural?

| ID | Hipótese | Componente ERP | Região | Efeito | Status |
|---|---|---|---|---|---|
| H3.1 | Tela aumenta N170 (processamento visual) | N170 (170ms) | Occipito-temporal | Amplitude ↑ | ⏳ A testar |
| H3.2 | Tela reduz P300 (atenção) | P300 (300ms) | Parietal | Amplitude ↓ | ⏳ A testar |
| H3.3 | Tela aumenta N400 (integração) | N400 (400ms) | Centro-parietal | Amplitude ↑ | ⏳ A testar |
| H3.4 | Idade modula efeito da tela | Idade × Tela | — | Interação | ⏳ A testar |
| H3.5 | Compreensão melhor em papel | Comportamental | — | d = 0.30 | ⏳ A testar |

**Análise estatística:**
- ANOVA mista 2 (mídia) × 2 (tarefa)
- Cluster-based permutation (1000 permutações)
- Time-frequency analysis (wavelet)
- Mixed models

**Componentes analisados:**
- N170, P200, N400, P600
- Alpha (8-12 Hz), Beta (13-30 Hz)

---

## 📋 P04 — IA Generativa e FE (SEM Transversal)

**Pergunta:** Como o uso de IA afeta FE, mediado por engajamento e moderado por letramento digital dos pais?

**Modelo:** X (IA) → M (Engajamento) → Y (FE), W (Letramento digital) modera X→Y

| ID | Hipótese | Caminho | Coef. Esperado | IC 95% | Status |
|---|---|---|---|---|---|
| H4.1 | Uso de IA → Engajamento | a | β ≈ 0.30 | [0.20, 0.40] | ⏳ A testar |
| H4.2 | Engajamento → FE | b | β ≈ 0.40 | [0.30, 0.50] | ⏳ A testar |
| H4.3 | Uso de IA → FE (direto) | c' | β ≈ 0.10-0.20 | [0.00, 0.20] | ⏳ A testar |
| H4.4 | Efeito indireto significativo | a×b | β ≈ 0.12 | [0.06, 0.18] | ⏳ A testar |
| H4.5 | W (letramento pais) modera X→Y | W×X | β ≈ 0.15 | [0.05, 0.25] | ⏳ A testar |

**Análise estatística:**
- CFA (validação de constructos)
- SEM (lavaan, estimador MLM)
- Mediação (bootstrap 5000)
- Moderação (Hayes PROCESS Model 1)
- Simple slopes / Johnson-Neyman

**Índices de ajuste:**
- CFI > 0.95, TLI > 0.95
- RMSEA < 0.06, SRMR < 0.08

---

## 📋 P05 — Coorte Longitudinal de FE (LGCM)

**Pergunta:** Como as FE se desenvolvem ao longo do Ensino Fundamental?

**Ondas:** 5 (2º, 3º, 4º, 5º, 6º ano)

| ID | Hipótese | Parâmetro | Valor | IC 95% | Status |
|---|---|---|---|---|---|
| H5.1 | Crescimento linear das FE | Slope (β1) | +0.5 DP/ano | [+0.3, +0.7] | ⏳ A testar |
| H5.2 | Variabilidade no intercepto | Var(Intercept) | > 0 | — | ⏳ A testar |
| H5.3 | Variabilidade no slope | Var(Slope) | > 0 | — | ⏳ A testar |
| H5.4 | Covariância intercept-slope | Cov | < 0 (catch-up) | — | ⏳ A testar |

**Análise estatística:**
- LGCM (Latent Growth Curve Models)
- IRT Rasch 1PL (parâmetros de itens)
- Análise de Sobrevivência (Kaplan-Meier + Cox)
- Análise Clássica de Itens (CTT)
- Mixed Models longitudinais

**Modelos testados:**
- Linear, Quadrático, Logarítmico
- Com covariáveis (sexo, SES)
- Com fatores latentes (FE múltiplas)

---

## 🔬 Resumo das Análises

| Análise | Projetos | Total |
|---|---|---|
| Análise Temática | P01 | 1 |
| Teste binomial | P01 | 1 |
| Correlação Spearman | P01 | 1 |
| Mann-Kendall | P01 | 1 |
| Qui-quadrado | P01 | 1 |
| Mixed Models | P01, P05 | 2 |
| ANCOVA | P02 | 1 |
| ANOVA mista | P03 | 1 |
| Cluster permutation | P03 | 1 |
| CFA + SEM | P04 | 2 |
| Mediação | P04 | 1 |
| Moderação | P04 | 1 |
| LGCM | P05 | 1 |
| IRT Rasch | P05 | 1 |
| Sobrevivência | P05 | 2 |
| Análise de Itens (CTT) | P05 | 1 |
| Análise de Rede | P01 | 1 |
| Análise de Sentimento | P01 | 1 |
| **Total** | — | **20+** |

---

## 📈 Status Geral

| Status | Quantidade | % |
|---|---|---|
| ✅ Confirmado (piloto) | 5 | 18% |
| ⏳ A testar | 22 | 82% |
| **Total** | **27** | **100%** |

---

## 🎯 Próximos Passos

1. **P01:** Submeter manuscrito (n=3 piloto) — prelo
2. **P02:** Recrutar 200 crianças (5 escolas)
3. **P03:** Recrutar 60 crianças (1 escola)
4. **P04:** Coletar 300-500 respondentes (5-8 escolas)
5. **P05:** Iniciar coorte 2º ano (40 crianças)

---

## 📚 Referências

- Hayes, A. F. (2017). *Introduction to Mediation, Moderation, and Conditional Process Analysis*.
- Rosseel, Y. (2012). lavaan: An R package for structural equation modeling.
- Singer, J. D., & Willett, J. B. (2003). *Applied Longitudinal Data Analysis*.
- Braun, V., & Clarke, V. (2022). *Thematic Analysis: A Practical Guide*.

---

**Última atualização:** 2026-08-12
**Versão:** 1.0
