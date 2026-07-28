# 📄 Projeto Detalhado — P02 (Gamificação e Autorregulação)

> **Status:** v0.1 — piloto
> **Projeto:** Gamificação e autorregulação em crianças do ensino fundamental
> **Pesquisadora:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN)
> **Linha:** Leitura + Neurociências (Neurociência Cognitiva e Educação Matemática)

---

## 1. RESUMO

Este projeto experimental fatorial (2×2) investiga como diferentes elementos de gamificação — **extrínsecos** (pontos, badges, rankings) vs. **intrínsecos** (narrativa, autonomia, mastery) — afetam a **autorregulação da aprendizagem** e o **desempenho matemático** de crianças de 7–10 anos. Com N=80–120, em 2 escolas, será desenvolvido um **app prototipado com 4 versões** do mesmo conteúdo matemático. A autorregulação será medida por escala (OSLIS-Brasil) e por logs comportamentais (tempo, persistência, pedidos de dica). Resultados esperados: contribuir com a literatura sobre gamificação em crianças, distinguindo efeitos de curto e longo prazo.

**Palavras-chave:** gamificação, autorregulação, matemática, educação infantil, experimento fatorial.

---

## 2. INTRODUÇÃO E JUSTIFICATIVA

A gamificação tem sido amplamente adotada em contextos educacionais, com **meta-análises** (Hamari et al., 2014; Sailer & Homner, 2020) mostrando efeitos positivos modestos. Porém, a maioria dos estudos foi conduzida com **adultos ou universitários**, e há pouca evidência em **crianças em idade escolar**. Além disso, os estudos geralmente não distinguem entre diferentes **elementos de gamificação** (pontos vs. narrativa, por exemplo) nem investigam efeitos sobre **processos cognitivos de ordem superior** como a autorregulação.

Este projeto preenche essa lacuna, focando em crianças de 7–10 anos — uma janela desenvolvimental em que a **autorregulação está se consolidando** (Diamond, 2013) e em que a matemática é uma das áreas de maior investimento pedagógico.

---

## 3. OBJETIVOS

### 3.1. Objetivo geral
Investigar os efeitos de diferentes elementos de gamificação (extrínsecos vs. intrínsecos) sobre a autorregulação e o desempenho matemático de crianças de 7–10 anos.

### 3.2. Objetivos específicos
1. Comparar os efeitos de gamificação extrínseca vs. intrínseca sobre **autorregulação percebida** (escala) e **comportamental** (logs).
2. Avaliar o **efeito de interação** entre tipo de gamificação e **características da criança** (idade, sexo, autorregulação basal).
3. Verificar se os efeitos **persistem em longo prazo** (follow-up de 1 mês).
4. Produzir **subsídios para o design** de apps educacionais com gamificação ética (não-manipulativa).

---

## 4. MÉTODO

### 4.1. Delineamento
**Experimento fatorial 2×2** com medidas repetidas (3 tempos: pré, pós, follow-up 1 mês).

| | **Sem gamificação** | **Com gamificação** |
|---|---|---|
| **Extrínseca** | Controle | Experimental 1 |
| **Intrínseca** | Experimental 2 | Experimental 3 |

Cada criança participa de **1 condição** (between-subjects, para evitar carry-over).

### 4.2. Participantes
- **N planejado:** 80–120 crianças (20–30 por condição)
- **Faixa etária:** 7–10 anos (2º ao 5º ano)
- **Critérios de inclusão:** matriculadas em escola parceira; sem experiência prévia com o app
- **Critérios de exclusão:** crianças com diagnóstico neuropsiquiátrico formal
- **Recrutamento:** 2 escolas (1 piloto + 1 experimento principal), em [município do Seridó/RN]

### 4.3. Materiais

#### App prototipado (4 versões)
- **Conteúdo:** problemas de matemática do 2º ao 5º ano (adição, subtração, multiplicação, divisão)
- **Duração da atividade:** 20–30 minutos por sessão
- **Plataforma:** tablet Android (PsychoPy ou Construct 3)
- **Versões:**
  - **Controle (sem gamificação):** apenas o conteúdo matemático
  - **Extrínseca:** + pontos, badges, leaderboard
  - **Intrínseca:** + narrativa (personagem em jornada), autonomia (escolha de temas), mastery (níveis de dificuldade adaptáveis)
  - **Combinada:** ambos os tipos (controle adicional)

#### Bateria de medidas
- **Pré-teste (T0):**
  - Questionário sociodemográfico
  - Escala de autorregulação (OSLIS-Brasil)
  - Pré-teste de matemática (livre de efeitos da gamificação)
  - Questionário de familiaridade com tecnologia
- **Pós-teste (T1):** imediatamente após a atividade
  - Escala de autorregulação (OSLIS-Brasil) — pós
  - Questionário de motivação (adaptado de CAIMI)
  - Questionário de experiência com o app (engajamento, satisfação)
  - Logs comportamentais (tempo, acertos, pedidos de dica, abandonos)
- **Follow-up (T2):** 1 mês depois
  - Escala de autorregulação
  - Pós-teste de matemática (mesmo instrumento)

### 4.4. Procedimentos
1. **Mês 1–2:** Construção do app (parceria com curso de Design/CC)
2. **Mês 3:** Submissão ao CEP
3. **Mês 4:** Piloto (n=10 crianças) — ajustes do app
4. **Mês 5:** Coleta principal (T0 → atividade → T1)
5. **Mês 6:** Follow-up T2
6. **Mês 7–9:** Análise estatística (R + JASP)
7. **Mês 10–12:** Submissão do paper

### 4.5. Análise dos dados
- **ANOVA mista** (Tipo de gamificação × Tempo)
- **Modelos lineares generalizados (GLM)** para outcomes binários (completou, desistiu)
- **Análise de mediação:** gamificação → engajamento → autorregulação
- **Análise de moderação:** sexo, idade, autorregulação basal
- **Cluster analysis:** identificar perfis de crianças (respondedores, não-respondedores, etc.)

### 4.6. Aspectos éticos
- Aprovação CEP/UFRN (mesma do P01, com adaptações)
- TCLE dos pais
- TALE das crianças
- **Cuidado especial:** gamificação pode despertar **uso excessivo** ("vício") — debriefing pós-experimento sobre uso equilibrado
- **Devolutiva:** as crianças ganham acesso ao app após o estudo, se desejarem

---

## 5. ORÇAMENTO (estimativa)

| Item | Qtd | Unitário | Total |
|---|---|---|---|
| Tablets (10) | 10 | R$ 800 | R$ 8.000 |
| Designer (120h) | 1 | R$ 80/h | R$ 9.600 |
| Programador (80h) | 1 | R$ 100/h | R$ 8.000 |
| Material de escritório | 1 | R$ 200 | R$ 200 |
| Lanche para crianças | 120 × 2 | R$ 5 | R$ 1.200 |
| Transporte | 24 visitas | R$ 100 | R$ 2.400 |
| Inscrição congresso | 1 | R$ 250 | R$ 250 |
| **TOTAL** | | | **R$ 29.650** |

---

## 6. CRONOGRAMA (12 meses)

| Mês | Atividade |
|---|---|
| M1 | Revisão de literatura; parceria com Design/CC |
| M2 | Construção do app (versão 1 — controle) |
| M3 | Construção das versões 2, 3, 4; submissão ao CEP |
| M4 | Piloto (n=10); ajustes |
| M5 | Coleta principal (T0 + atividade + T1) |
| M6 | Follow-up T2 (1 mês depois) |
| M7 | Análise estatística |
| M8 | Escrita do paper |
| M9 | Pré-registro + submissão do paper (revista BR) |
| M10 | Resubmissão ou submissão intl |
| M11 | Apresentação em congresso |
| M12 | Devolutiva para escolas + ajustes pós-paper |

---

## 7. REFERÊNCIAS (preliminares)

- Diamond, A. (2013). Executive functions. *Annual Review of Psychology*, 64, 135–168.
- Hamari, J. et al. (2014). Does gamification work? *HICSS-47*.
- Howard-Jones, P. (2014). *Neurociência e Educação*. Artmed.
- Howard-Jones, P. A. et al. (2021). Neuroeducational research in the digital age. *Mind, Brain, and Education*, 15(1), 5–14.
- Mekler, E. D. et al. (2017). Towards understanding the effects of individual gamification elements. *CHI*.
- Sailer, M. & Homner, L. (2020). The gamification of teaching and learning. *Frontiers in Psychology*, 11, 901.
- Zimmerman, B. J. (2002). Becoming a self-regulated learner. *Theory Into Practice*, 41(2), 64–70.

---

## 8. PRÉ-REGISTRO

Será pré-registrado no OSF antes da coleta. Template em `00-fundamentos/preregistracao/template-osf.md`.

---

## 9. ANEXOS (a criar)

- [ ] Roteiro de teste piloto
- [ ] Questionário sociodemográfico
- [ ] OSLIS-Brasil (escala de autorregulação) — versão autorizada
- [ ] Teste de matemática padronizado
- [ ] Roteiro de debriefing

---

> **Próximo passo:** alinhar com a Angela sobre parceria com Design/CC; orçar tablets; submeter pré-registro.
