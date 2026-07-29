# 📄 Projeto Detalhado — P05 (Coorte Longitudinal com EEG)

> **Status:** v0.1 — piloto / visão de longo prazo
> **Projeto:** Coorte prospectiva de crianças de 5 a 12 anos: marcadores de maturação neural, FE e leitura
> **Pesquisadora:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN)
> **Parceiros:** Instituto do Cérebro da UFRN (ICe); Escolas parceiras do Projeto L+N
> **Linha:** Abre nova linha (potencial tese de doutorado + lifelong research)
> **Rede internacional:** ABCD Study (EUA), Saguenay Youth Study (Canadá), Family Life Project (EUA)

---

## 1. RESUMO

Esta **coorte prospectiva de 5 anos** acompanha **100–200 crianças** de **5 a 9 anos** (com possibilidade de extensão até 12 anos no doutorado), com **5 ondas anuais** de avaliação multimétodo: (1) **EEG em repouso e durante tarefa** (maturação neural, N170, N400), (2) **bateria neuropsicológica** (NEPSY-II ou CANTAB adaptado), (3) **bateria de leitura** (PROLEC, fluência, compreensão), (4) **questionários de exposição digital e contexto** (pais, criança, professor), (5) **observação em sala** (1x por onda). O objetivo é identificar **trajetórias distintas** de maturação neural e desenvolvimento cognitivo, associadas a diferentes perfis de **exposição a tecnologias educacionais** (Khanmigo, plataformas adaptativas, leitura digital, etc.). Análise por **modelagem de curva de crescimento** (latent growth curve models) e **LGMM** (latent growth mixture models). O estudo visa subsidiar políticas públicas de **educação digital** com base em **evidência neurocientífica longitudinal** — primeira coorte brasileira nesse escopo.

**Palavras-chave:** coorte longitudinal, EEG desenvolvimental, funções executivas, leitura, tecnologia educacional, latent growth curve, Brasil.

---

## 2. INTRODUÇÃO E JUSTIFICATIVA

A **primeira infância e o início da vida escolar** são janelas desenvolvimentais críticas para a maturação do cérebro, em que se formam trajetórias que se estendem por toda a vida. A exposição a **tecnologias educacionais** (plataformas digitais, IA generativa, leitura em tela) é cada vez mais precoce — e **quase não há dados longitudinais** sobre como essa exposição modula o desenvolvimento.

Coortes internacionais (ABCD Study, EUA; Saguenay Youth Study, Canadá) demonstraram a **viabilidade e o valor** de acompanhar 10.000+ crianças por 10+ anos, com multimétodo (neuroimagem, comportamento, contexto). No Brasil, **não há equivalente** com crianças dessa faixa etária. Essa lacuna é especialmente crítica em um momento em que o **PNED** (Programa Nacional de Educação Digital) e a **EBED** (Estratégia Brasileira de Educação Digital) estão implementando uso massivo de tecnologias em escolas.

Este projeto preenche essa lacuna, integrando a **rede de escolas parceiras do Projeto L+N** (Ipanguaçu, Currais Novos) com a **infraestrutura de EEG do ICe** e a **expertise em neurociência desenvolvimental** que a UFRN tem construído.

---

## 3. OBJETIVOS

### 3.1. Objetivo geral
Identificar trajetórias longitudinais de maturação neural, desenvolvimento de funções executivas, e aquisição de leitura em crianças brasileiras de 5 a 12 anos, associadas a diferentes perfis de exposição a tecnologias educacionais.

### 3.2. Objetivos específicos
1. Caracterizar **trajetórias de maturação neural** (theta/beta, conectividade em repouso, N170, N400) ao longo de 5 anos
2. Caracterizar **trajetórias de FE** (memória de trabalho, inibição, flexibilidade) ao longo de 5 anos
3. Caracterizar **trajetórias de leitura** (decoding, fluência, vocabulário, compreensão) ao longo de 5 anos
4. Identificar **subgrupos de trajetórias distintas** (latent growth mixture models)
5. Examinar **preditores** de trajetórias (exposição digital, SES, contexto familiar, escola, sono, exercício)
6. Construir **modelo preditivo** de desfechos (compreensão de leitura, FE) a partir de biomarcadores + contexto

---

## 4. MÉTODO

### 4.1. Delineamento
**Coorte prospectiva** com **5 ondas anuais** (T0: 5 anos, T1: 6 anos, T2: 7 anos, T3: 8 anos, T4: 9 anos), com possibilidade de extensão no doutorado (T5: 10 anos, T6: 11 anos, T7: 12 anos).

### 4.2. Participantes
- **N inicial:** 100–200 crianças (poder para detectar trajetórias latentes)
- **Critérios de inclusão:** 5 anos no T0; matriculadas em escolas parceiras do L+N; consentimento dos pais + assentimento
- **Critérios de exclusão:** diagnóstico neuropsiquiátrico formal; síndromes genéticas
- **Estratificação inicial:** SES (baixa, média, alta), sexo, zona (urbana/rural)
- **Recrutamento:** escolas parceiras (Ipanguaçu, Currais Novos, Caicó)

### 4.3. Ondas de avaliação

| Onda | Idade | Medidas principais | Duração | Local |
|---|---|---|---|---|
| **T0 (baseline)** | 5 anos | EEG repouso + neuropsi + leitura + questionários pais | ~2h | ICe + escola |
| **T1** | 6 anos | Idem | ~2h | ICe + escola |
| **T2** | 7 anos | Idem | ~2h | ICe + escola |
| **T3** | 8 anos | Idem + N170/N400 (tarefa de leitura) | ~2.5h | ICe + escola |
| **T4** | 9 anos | Idem | ~2.5h | ICe + escola |
| (T5–T7) | 10–12 anos | Extensão (no doutorado) | — | — |

### 4.4. Instrumentos

#### 4.4.1. EEG (no ICe)
- **Repouso (5 min):** olhos abertos/fechados alternados
- **Tarefa de atenção (oddball, 10 min):** tons auditivos raros vs. frequentes (P300)
- **Tarefa de leitura (T3–T4, 15 min):** leitura de palavras vs. pseudopalavras (N170), leitura de frases (N400)
- **Touca com gel seco (32 canais)** para minimizar tempo de setup com crianças
- **Pipeline:** EEGLAB + ERPLAB no ICe

#### 4.4.2. Bateria neuropsicológica
- **NEPSY-II** (subtestes selecionados por idade): Atenção, Funções Executivas, Linguagem, Memória
- **Testes específicos de FE:**
  - Stroop infantil (dia/noite)
  - N-back infantil
  - Torre de Londres (TOL)
  - Teste de Classificação de Cartas (WCST infantil)
- **Bateria de leitura:**
  - **PROLEC** (Prova de Avaliação dos Processos de Leitura) — adaptado para PT-BR
  - **TDE** (Teste de Desempenho Escolar)
  - Fluência de leitura oral (palavras/min)
  - **Compreensão:** Cloze + questões abertas

#### 4.4.3. Questionários (pais, criança, professor)
- **Exposição digital:** tempo, tipo, contexto, mediação parental (a desenvolver)
- **Contexto familiar:** SES, escolaridade dos pais, estrutura familiar
- **Saúde:** sono, atividade física, alimentação
- **Desenvolvimento:** WHO-5 wellbeing, SDQ (Strengths and Difficulties Questionnaire)

#### 4.4.4. Observação em sala
- 1 visita por onda, 1h, com protocolo estruturado
- Avalia: tecnologia usada, interação professor-aluno, qualidade do ensino

### 4.5. Procedimentos
- **Reuniões com escolas** (2x por ano): apresentação dos resultados parciais, alinhamento
- **Capacitação de professores:** 1x por ano, 4h, sobre letramento digital
- **Acolhimento das famílias:** encontro semestral para devolutiva
- **Compensação:** R$ 200 em material escolar por ano para cada família
- **Transporte:** van fornecida para as coletas no ICe

### 4.6. Análise dos dados

#### Análise primária
- **Latent Growth Curve Models (LGCM):** modelar trajetórias de cada variável (EEG, FE, leitura)
- **Latent Growth Mixture Models (LGMM):** identificar subgrupos de trajetórias distintas
- **Equações estruturais longitudinais:** modelos de mediação/moderação temporal
- **Análise multinível:** medidas aninhadas em crianças, aninhadas em escolas

#### Análise secundária
- **Machine learning supervisionado:** prever desfechos a partir de biomarcadores
- **Análise de redes:** mapear conexões entre variáveis (network analysis)

#### Software
- R (lavaan, lme4, OpenMx)
- Python (scikit-learn, networkx)
- MNE-Python (EEG)

### 4.7. Aspectos éticos
- CEP/UFRN (re-submissão a cada onda ou emenda anual)
- TCLE dos pais atualizado a cada onda
- TALE da criança atualizado
- **Comitê de monitoramento:** anual, com revisores externos
- **Plano de biossegurança** para EEG com crianças
- **Plano de compartilhamento de dados** (depositar no Zenodo)

---

## 5. ORÇAMENTO (5 anos)

| Item | Qtd | Unitário | Total |
|---|---|---|---|
| EEG (5 anos × 100 crianças × 2h) | 1.000h | R$ 0 (ICe) | R$ 0 |
| Bolsista de pós-doutorado (apoio) | 5 anos | R$ 80k/ano | R$ 400.000 |
| Bolsista de doutorado (apoio) | 5 anos | R$ 50k/ano | R$ 250.000 |
| IC júnior (2 × 5 anos) | 10 | R$ 12k/ano | R$ 120.000 |
| Transporte van (5 anos) | 50 | R$ 800 | R$ 40.000 |
| Compensação para famílias (5 anos × 100 crianças) | 500 | R$ 200 | R$ 100.000 |
| Capacitação de professores | 10 | R$ 1.500 | R$ 15.000 |
| Material de escritório | 5 | R$ 500 | R$ 2.500 |
| Reuniões com famílias (5 anos × 2) | 10 | R$ 2.000 | R$ 20.000 |
| Inscrição congressos | 10 | R$ 1.000 | R$ 10.000 |
| **TOTAL** | | | **R$ 957.500** |

> **Financiamento:** necessário edital grande (FAPESP, CNPq Universal, ou internacional). **Indispensável** para viabilizar. **A Onda 1 pode ser feita como IC**, com orçamento menor (~R$ 30k).

---

## 6. CRONOGRAMA (5+ anos)

| Ano | Onda | Atividades principais |
|---|---|---|
| **2028 (preparação)** | — | Edital de fomento, parcerias internacionais, CEP, equipe |
| **2029** | T0 (5 anos) | Recrutamento, baseline (N=100–200), EEG, neuropsi |
| **2030** | T1 (6 anos) | Reavaliação; publicações da T0 |
| **2031** | T2 (7 anos) | Reavaliação; mestrado concluído |
| **2032** | T3 (8 anos) | Reavaliação; doutorado em andamento; EEG com N170 |
| **2033** | T4 (9 anos) | Reavaliação final; paper global |
| **2034+ (extensão)** | T5–T7 (10–12 anos) | Acompanhamento opcional; desdobramentos |

---

## 7. REFERÊNCIAS (preliminares)

- Casey, B. J. et al. (2008). The adolescent brain. *Developmental Review*, 28(1), 62–77.
- Luciana, M. & Nelson, C. A. (eds.) (2012). *Handbook of Developmental Cognitive Neuroscience* (3rd ed.). MIT Press.
- Raudenbush, S. W. & Bryk, A. S. (2002). *Hierarchical Linear Models* (2nd ed.). SAGE.
- Singer, J. D. & Willett, J. B. (2003). *Applied Longitudinal Data Analysis*. Oxford.
- Volkow, N. D. et al. (2018). The conception of the ABCD study. *Developmental Cognitive Neuroscience*, 32, 4–7.

---

## 8. PRÉ-REGISTRO

Será pré-registrado no OSF antes do início (T0). Template em `00-fundamentos/preregistracao/template-osf.md`.

---

## 9. RISCOS E LIMITAÇÕES

### Riscos
- **Atrito elevado com famílias** (adesão por 5+ anos) — mitigação: compensação anual, encontros semestrais
- **Custo alto** — depende de financiamento grande
- **Estabilidade da equipe** — perda de pesquisadores no meio da coorte é comum
- **Mudança de contexto** (escola, política, tecnologia) — pode invalidar comparações

### Limitações
- Coorte específica (interior do RN) — generalização limitada
- EEG seriado em crianças pequenas é difícil (artefatos)
- Bateria de FE padronizada em PT-BR é limitada
- Não cobre o período pré-escolar completo (0–5 anos)

---

## 10. ESTRATÉGIA DE ENTRADA (PLANTAR A FLORESTA AOS POUCOS)

Como é inviável financiar 5 anos de uma vez, a estratégia é:
1. **T0 (Onda 1) como IC** — projeto de iniciação científica da pesquisadora
2. **Análise da T0 como mestrado** — defesa
3. **Manutenção da coorte como doutorado** — defesa parcial e depois tese
4. **Análise completa como pós-doutorado** — lifelong research program

Cada fase tem deliverables claros e financiamento próprio.

---

> **Próximo passo:** submeter pré-registro no OSF; iniciar Onda 1 como IC; buscar financiamento para anos subsequentes.
