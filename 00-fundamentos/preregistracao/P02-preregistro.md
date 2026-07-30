# Pré-Registro OSF — Projeto P02

> **Template:** OSF Standard Pre-Data Collection Registration
> **Projeto:** P02 — Gamificação adaptativa com IA na promoção de funções executivas em crianças do 2º ano do ensino fundamental
> **Versão do pré-registro:** 1.0
> **Data de submissão prevista:** Mês 6 (M0 = Jan 2026)
> **Investigador principal:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN/CERES)
> **Coorientador (potencial):** Prof. Dr. Antonio Pereira (ICe/UFRN) ou pesquisador de Educação Matemática/Games

---

## 1. Informações gerais

- **Título:** Efeitos da gamificação adaptativa com inteligência artificial sobre funções executivas e engajamento de crianças do 2º ano do ensino fundamental: ensaio controlado randomizado
- **Tipo de estudo:** Ensaio controlado randomizado (ECR) 2×2 fatorial
- **Área de conhecimento:** Educação (CNPq 7.08.00.00-6), Neurociência Cognitiva
- **Financiamento:** [CAPES/UFRN — a submeter]
- **Conflitos de interesse:** Nenhum declarado
- **Ética:** Submissão ao CEP/UFRN prevista para Mês 5 (Plataforma Brasil)

---

## 2. Pergunta de pesquisa

**RQ1:** Qual o efeito de um sistema de gamificação adaptativa com IA sobre (a) controle inibitório, (b) memória de trabalho, e (c) engajamento de crianças do 2º ano do EF, comparado a (i) gamificação fixa (não adaptativa) e (ii) instrução tradicional sem gamificação?

**Sub-questões:**

- **RQ1a:** O ganho em FE é mediado pelo nível de engajamento?
- **RQ1b:** O efeito é moderado por (a) nível socioeconômico, (b) sexo, (c) desempenho inicial em leitura/escrita?
- **RQ1c:** Os efeitos diferem entre crianças com e sem dificuldades atencionais pré-existentes?

---

## 3. Hipóteses (H₁)

| ID | Hipótese | Predição |
|---|---|---|
| **H1** | Gamificação adaptativa > gamificação fixa > controle em FE | Pós-teste: GAM-ADAP > GAM-FIX > CTRL (p < .05) |
| **H2** | Gamificação adaptativa > controle em engajamento | Engajamento medido por tempo de uso + questionário de fluxo (Flow State Scale) (p < .05) |
| **H3** | Mediação: engajamento medeia o efeito de tipo de gamificação sobre FE | Efeito indireto significativo (β indireto, IC 95% não inclui zero) |
| **H4** | Interação: gamificação adaptativa × alto SES → maior ganho em FE | Efeito de interação significativo (p < .05) |

> **Nota:** Toda hipótese é direcionada. Análise primária é ANCOVA (pós-teste covariado por pré-teste e idade). Análise secundária é SEM com mediação (lavaan).

---

## 4. Design

### 4.1 Tipo
- **Ensaio controlado randomizado** (ECR) 2×2 fatorial
- **Fator 1:** Tipo de gamificação (ADAPTATIVA vs FIXA)
- **Fator 2:** Duração da intervenção (8 vs 16 semanas)
- → **4 grupos:** ADAPTATIVA-8, ADAPTATIVA-16, FIXA-8, FIXA-16
- **+ 1 grupo controle** (instrução tradicional, sem gamificação) → **5 grupos totais**

> **Decisão de design (justificativa):** O fator 2 (duração) é incluído para responder à pergunta prática "8 semanas bastam?". Aumenta N mas também poder.

### 4.2 Randomização
- **Método:** Alocação 1:1:1:1:1 com bloco permutado (blocos de 10)
- **Quem randomiza:** Pesquisador externo (cego à lista de escolas) via `randomizr` em R
- **Cegamento:**
  - **Pais/crianças:** Não sabem que existe comparação entre tipos de gamificação (sabem só que estão numa pesquisa com jogo)
  - **Professores:** Não sabem a hipótese específica
  - **Aplicadores de teste:** Cegos ao grupo
  - **Analistas:** Cegos até pré-processamento concluído

### 4.3 Medidas

#### Pré-teste (T0, semana 0)
| Constructo | Instrumento | Tempo |
|---|---|---|
| Controle inibitório | **Stroop Digital** (crianças) | 8 min |
| Memória de trabalho | **Backward Digit Span** (WISC-V adaptado) | 10 min |
| Flexibilidade cognitiva | **Dimensional Change Card Sort** (Zelazo 2003) | 5 min |
| Engajamento (linha de base) | **Questionário de motivação escolar** (adaptado de Pintrich) | 10 min |
| Habilidades de leitura | **TLE — Teste de Leitura de Palavras** (Seabra & Capovilla) | 15 min |
| Controle de confundidores | Questionário sociodemográfico (pais) | 20 min |
| **Total** | | **~68 min por criança** (divididos em 2 sessões) |

#### Pós-teste (T1, semana 8 ou 16 conforme grupo)
- Repetição dos instrumentos de T0
- **+ Questionário de fluxo** (Flow State Scale — Jackson & Marsh)
- **+ Entrevista breve** (5 min) sobre experiência com jogo

#### Follow-up (T2, 3 meses pós-intervenção)
- Repetição dos instrumentos de FE (para avaliar retenção)

### 4.4 Intervenção

**Plataforma:** Sistema de gamificação **adaptativa** a ser desenvolvido em Unity + LLM para personalização de desafios. (Alternativa: adaptar plataforma existente como Khanmigo — mas isso muda o projeto para P04.)

**Mecânica da gamificação adaptativa (grupo ADAPTATIVA):**
- 5 elementos (Koivisto & Hamari 2019): pontos, badges, leaderboard, narrativa, avatar
- **IA adapta:** dificuldade dos desafios em tempo real (algoritmo ZPD — Zone of Proximal Development) baseado no desempenho da criança
- **Feedback adaptativo:** explicação contextualizada após erros

**Mecânica da gamificação fixa (grupo FIXA):**
- Mesma interface, mesmos 5 elementos
- Dificuldade **fixa** (mesma para todas as crianças)
- Feedback genérico ("Tente novamente")

**Grupo controle (instrução tradicional):**
- Aulas regulares de matemática/português sem gamificação adicional
- Aplicação dos mesmos pré e pós-testes

**Duração:**
- 8 ou 16 semanas (entre grupos)
- 30 min/dia, 3×/semana
- Total: 36 ou 72 horas de exposição

---

## 5. Amostra

### 5.1 Tamanho
- **N total:** 200 crianças (40 por grupo × 5 grupos)
- **Justificativa do poder:**
  - Para ANCOVA com 4 grupos (sem contar o controle extra), α = .05, poder = .80, detectar efeito médio (f = 0.25)
  - G*Power: N mínimo = 180. Adicionando 10% de perda, N = 200.

### 5.2 Recrutamento
- **Local:** 5 escolas públicas de Natal/RN (Caicó se for parceria CERES)
- **Série:** 2º ano do Ensino Fundamental (crianças 7-8 anos)
- **Critérios de inclusão:**
  - Matriculadas no 2º ano em 2026
  - Sem diagnóstico de deficiência cognitiva
  - Consentimento dos pais + assentimento da criança
  - Frequência mínima de 80% esperada
- **Critérios de exclusão:**
  - Uso de medicação psicoativa
  - Histórico de epilepsia (contraindicação EEG se P02 incluir sub-estudo)
  - Transferência de escola durante o estudo

---

## 6. Plano de análise

### 6.1 Análise primária
- **ANCOVA 2×4 (Tipo de gamificação × Duração)** com pré-teste como covariável
- Variável dependente: pós-teste em cada medida de FE
- α = .05, correção de Bonferroni para múltiplas comparações (3 medidas de FE)

### 6.2 Análise secundária — mediação
- **SEM** (lavaan) testando:
  - Tipo de gamificação (X) → Engajamento (M) → FE (Y)
  - Covariáveis: idade, sexo, SES
  - Reportar efeito indireto com IC 95% (bootstrap, 5000 iterações)

### 6.3 Análise exploratória
- Modelos de aprendizado de máquina (random forest) para identificar perfis de crianças que mais se beneficiam
- Análise de subgrupos por SES, sexo, dificuldade pré-existente

### 6.4 Tratamento de dados faltantes
- **Missing at random (MAR):** Múltipla imputação (mice em R, m = 20)
- **Missing not at random (MNAR):** Análise de sensibilidade (pattern mixture model)

### 6.5 Critérios de exclusão de dados
- Pré-especificado: crianças com < 50% de aderência (frequência < 18 das 36 sessões para grupo 8-semanas)
- Análise de intenção de tratar (ITT) **e** per-protocol (PP)

### 6.6 Software
- R versão 4.4.x com `tidyverse`, `lavaan`, `mice`, `randomizr`
- Análise cega (analista não sabe a que grupo cada ID corresponde)
- Script de análise arquivado no OSF antes de unblinding

---

## 7. Controle de qualidade

### 7.1 Fidelidade da implementação
- **Checklist de implementação** preenchido por observadores em 20% das sessões
- **Logs da plataforma** registrando tempo de uso, missões completadas, etc.
- Entrevistas com professores

### 7.2 Validade interna
- Verificação de cegarização dos aplicadores (perguntar ao final se sabem o grupo)
- Comparação de grupos na baseline (T0) para confirmar randomização
- Análise de dropouts (características dos que saem vs ficam)

### 7.3 Validade externa
- Documentar contexto (escola, bairro, professor, currículo) para avaliar generalizabilidade
- Replicação futura em outras regiões

---

## 8. Questões éticas

- **CEP/UFRN:** Submissão antes de T0
- **TCLE** para pais (2 versões: completo + resumido)
- **TALE** para crianças (linguagem acessível)
- **Anonimização:** ID numérico, dados separados de identificadores
- **Devolutiva:** Resultados agregados para escolas e famílias após publicação
- **Compartilhamento de dados:** Dados **não-pessoais** (Tabela 4 do pré-registro) depositados no OSF após publicação
- **Suspensão:** Se efeitos adversos (estresse, frustração) → parar intervenção

---

## 9. Cronograma

| Mês | Atividade |
|---|---|
| 5 | Submissão CEP |
| 6 | Aprovação CEP + Pré-registro OSF |
| 7 | Recrutamento de escolas |
| 8 | Pré-teste (T0) — 1ª onda de escolas |
| 9-16 | Intervenção (8 semanas) — grupo 8-sem |
| 13-20 | Intervenção (16 semanas) — grupo 16-sem |
| 17 | Pós-teste (T1) — grupo 8-sem |
| 21 | Pós-teste (T1) — grupo 16-sem |
| 24 | Follow-up (T2) — ambos grupos |
| 25-27 | Análise de dados |
| 28-30 | Manuscrito + submissão |

---

## 10. Financiamento e recursos

- **Bolsa CAPES** (a solicitar): R$ XX.XXX
- **Equipamentos:** tablets/Chromebooks (empréstimo escola ou compra)
- **Plataforma de gamificação:** desenvolvimento próprio em Unity
- **Análise estatística:** R + lavaan (open source)

---

## 11. Limitações pré-declaradas

1. **Generalizabilidade:** Uma região (Natal/RN) — limitada
2. **Tempo:** Follow-up de 3 meses não capta efeitos de longo prazo
3. **Cegamento:** Professores não podem ser cegados (implementam a intervenção)
4. **Diferenças entre escolas:** Turmas, professores diferentes → variância extra
5. **Adesão:** Plataformas digitais têm taxa de drop-out alta

---

## 12. Plano de divulgação

- **Artigo 1:** Efeito principal (RCT) → submissão a *Computers & Education* (Qualis A1)
- **Artigo 2:** Mediação (SEM) → *Learning and Instruction* (Qualis A1)
- **Artigo 3:** Subgrupos (ML) → *Journal of Learning Sciences*
- **Conferências:** SBIE, CIAED, ESERA, EARLI
- **Disseminação:** Blog, vídeo YouTube, escola (devolutiva)

---

## 13. Mudanças do pré-registro

> **Compromisso:** Qualquer mudança após o início da coleta de dados será documentada no OSF com justificativa + análise de sensibilidade.

---

## 14. Aprovações

- [ ] Investigador principal
- [ ] Orientadora (Angela Naschold)
- [ ] CEP/UFRN (em andamento)
- [ ] Comitê de ética do ICe (se sub-estudo EEG)

---

**Data de criação:** 2026-07-28
**Última atualização:** 2026-07-28
**OSF ID:** [a criar após submissão]
