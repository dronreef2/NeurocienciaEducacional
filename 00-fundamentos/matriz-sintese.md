# 🧩 Matriz de Síntese — Papers × Projetos

> **Cross-tabulation** que mostra como cada paper seminal se conecta com cada projeto.
> **Uso:** identificar gaps (células vazias) e prioridades (células "forte" sem leitura).
> **Atualizar** à medida que novos papers são lidos.

---

## Legenda

| Símbolo | Significado |
|---|---|
| 🟢 **forte** | Paper é referência central para o projeto (citar extensamente) |
| 🟡 **média** | Paper é complementar (citar seletivamente) |
| 🔵 **fraca** | Paper é periférico (citação opcional) |
| ⚪ — | Sem relação |
| 📖 | Nota de leitura já feita |

---

## Matriz: Papers × Projetos

| Paper | P01 | P02 | P03 | P04 | P05 |
|---|---|---|---|---|---|
| **Dehaene (2010).** *Reading in the Brain* | 🟢📖 | ⚪ | 🟢📖 | ⚪ | 🟡📖 |
| **Diamond (2013).** *Executive Functions* | 🟢📖 | 🔵 | ⚪ | 🟢📖 | 🟡📖 |
| **Miyake et al. (2000).** *Unity of EF* | ⚪ | ⚪ | ⚪ | 🟢📖 | 🟡📖 |
| **Hamari et al. (2014).** *Gamification* | ⚪ | 🟢📖 | ⚪ | ⚪ | ⚪ |
| **Luck (2014).** *ERP Technique* | ⚪ | ⚪ | 🟢📖 | ⚪ | 🟢📖 |
| **Naschold (2017).** *Projeto L+N* | 🟢📖 | 🟢📖 | 🟡 | 🔵 | 🟡📖 |
| **Braun & Clarke (2022).** *Thematic Analysis* | 🟢📖 | ⚪ | ⚪ | 🟡 | ⚪ |
| **Mollick (2024).** *Co-Intelligence* | 🟢📖 | 🟡 | ⚪ | 🟢📖 | ⚪ |
| **Howard-Jones (2014).** *Neuro + Ed* | 🟡📖 | 🟡📖 | 🟡📖 | 🟡📖 | 🟡📖 |
| **Snowling & Hulme (2020).** *Science of Reading* | 🟢📖 | ⚪ | 🟡📖 | ⚪ | 🟡📖 |

---

## Gaps identificados (células 🟢 sem nota)

| Onde | Gap | Sugestão |
|---|---|---|
| P01 × Hamari | (não relevante) | — |
| P02 × Miyake | EF no P02 | Considerar Miyake como complemento (já tem Hamari como central) |
| P03 × Diamond | FE no P03 | (não prioritário — Luck + Dehaene cobrem) |
| P05 × Miyake | EF no P05 | OK, já tem nota |

**Veredicto:** a matriz está bem coberta. Priorizar agora **papers novos** (não nas linhas) para preencher colunas de P04 e P05.

---

## Matriz: Projetos × Tipos de contribuição

| Projeto | Referencial teórico | Método | Medida específica | Análise |
|---|---|---|---|---|
| **P01** | Dehaene, Naschold, Mollick, Howard-Jones, Snowling | Análise Temática (Braun & Clarke) | Entrevista + think-aloud + diário | AT reflexiva |
| **P02** | Hamari, Naschold, Howard-Jones | Experimento fatorial 2×2 | OSLIS-Brasil + logs comportamentais | ANOVA mista + GLM |
| **P03** | Dehaene, Snowling, Luck, Howard-Jones | EEG within-subjects | N170, N400, P300 | Mass-univariate cluster |
| **P04** | Miyake, Diamond, Mollick, Howard-Jones | Transversal correlacional | Bateria FE computadorizada | SEM com lavaan |
| **P05** | Naschold, Luck, Howard-Jones, Snowling | Coorte longitudinal | EEG + NEPSY-II + leitura | LGCM + LGMM |

---

## Matriz: Tipos de análise × Software

| Tipo de análise | Software | Status | Projeto |
|---|---|---|---|
| Análise Temática Reflexiva | Taguette (open source) | ✅ em uso | P01 |
| ANOVA mista + GLM | R + JASP ou R + afex | 🔄 a aprender | P02 |
| Modelos mistos longitudinais | R + lme4 | 🔄 a aprender | P02, P05 |
| SEM (modelos de equações estruturais) | R + lavaan | 🔄 a aprender | P04, P05 |
| Mass-univariate cluster (ERP) | MNE-Python ou EEGLAB/ERPLAB | 🔄 a aprender | P03, P05 |
| Latent Growth Curve Models | R + lavaan ou OpenMx | 🔄 a aprender | P05 |
| Latent Growth Mixture Models | R + tidySEM ou Mplus | 🔄 a aprender | P05 |
| Pré-processamento EEG | EEGLAB + ERPLAB ou MNE-Python | 🔄 a aprender | P03, P05 |
| Network analysis | R + qgraph ou igraph | 🔄 opcional | P05 |

---

## Matriz: Habilidades × Cronograma de aprendizado

| Habilidade | Quando aprender | Onde | Duração estimada |
|---|---|---|---|
| Taguette (AT) | M1–M2 | YouTube + manual | 2 dias |
| R básico | M2–M4 | Coursera / R4DS | 2 meses |
| JASP | M2 | Documentação | 1 semana |
| lme4 | M5 | Curso "Mixed Effects Models" (Bates) | 2 semanas |
| lavaan (SEM) | M8 | Rosseel (2012) + tutoriais | 1 mês |
| EEGLAB/ERPLAB | M9–M11 | Mike Cohen tutorials | 2 meses |
| MNE-Python | M10–M12 | Documentação + cursos | 2 meses |
| OpenMx (LGCM) | Mês 18+ | Documentação | 2 semanas |
| tidySEM (LGMM) | Mês 18+ | Documentation | 1 semana |

---

## Próximos passos baseados na matriz

1. **Curto prazo (M1–M3):** dominar Taguette + R básico + JASP
2. **Médio prazo (M5–M9):** SEM (lavaan) + EEG (EEGLAB/ERPLAB ou MNE-Python)
3. **Longo prazo (M18+):** LGCM + LGMM para o P05

---

> **Como usar essa matriz:**
> - Antes de iniciar análise de um projeto, revise a coluna correspondente
> - Identifique gaps (células 🟢 sem nota) — esses são prioridade de leitura
> - Use para justificar a escolha de ferramentas em papers
> - Atualize mensalmente à medida que evolui
