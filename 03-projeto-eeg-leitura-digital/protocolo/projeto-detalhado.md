# 📄 Projeto Detalhado — P03 (EEG de Leitura Digital vs. Papel)

> **Status:** v0.1 — piloto
> **Projeto:** Marcadores eletrofisiológicos de atenção e integração semântica na leitura digital vs. papel em crianças
> **Pesquisadora:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN)
> **Parceiro:** Instituto do Cérebro da UFRN (ICe) — Prof. Antonio Pereira (vice-coordenador)
> **Linha:** Leitura + Neurociências (flagship do programa)

---

## 1. RESUMO

Este projeto experimental within-subjects investiga os **marcadores eletrofisiológicos de atenção e integração semântica** (P300, N400, theta frontal) durante a leitura de textos informativos em **papel**, **tela simples** e **tela com hipertexto** em crianças de 8–10 anos (N=30–40). O EEG é registrado simultaneamente à leitura, com 32 canais. Medidas comportamentais (compreensão, fluência, tempo de leitura) e auto-relato complementam. Resultados esperados: contribuir com o entendimento de como o cérebro em desenvolvimento responde à leitura digital, com implicações para políticas de digitalização escolar.

**Palavras-chave:** EEG, ERPs, leitura digital, crianças, N400, P300, hipertexto, desenvolvimento.

---

## 2. INTRODUÇÃO E JUSTIFICATIVA

A leitura digital é cada vez mais presente na vida de crianças brasileiras. O **PNED (Programa Nacional de Educação Digital)** e a **Estratégia Brasileira de Educação Digital (EBED)** preveem uso massivo de telas nas escolas nos próximos anos. Porém, há pouca evidência sobre **como o cérebro em desenvolvimento responde a essa mudança**. A maioria dos estudos sobre leitura digital é comportamental (Clinton, 2019; Delaney et al., 2022), e os poucos com EEG foram conduzidos com adultos (Stavanger et al., 2024 — única exceção em crianças que conhecemos).

Este projeto preenche essa lacuna, focando em crianças de 8–10 anos — uma **janela desenvolvimental única** em que o córtex pré-frontal e os sistemas atencionais estão amadurecendo. Investigar como o cérebro responde à leitura digital nesta fase tem implicações para o **planejamento educacional**, **design de plataformas**, e **políticas públicas**.

---

## 3. OBJETIVOS

### 3.1. Objetivo geral
Investigar como a leitura em diferentes meios (papel, tela simples, tela com hipertexto) modula os marcadores eletrofisiológicos de atenção e integração semântica em crianças de 8–10 anos.

### 3.2. Objetivos específicos
1. Comparar a **amplitude e latência de N170, P300, N400 e P600** entre as 3 condições (papel, tela simples, tela hipertexto)
2. Investigar se a **fluência de leitura** e o **tipo de texto** (narrativo vs. informativo) moderam esses efeitos
3. Verificar a relação entre os **marcadores EEG** e o **desempenho comportamental** (compreensão, fluência)
4. Explorar se a **razão theta/beta** em repouso (maturação) correlaciona-se com o desempenho em leitura

---

## 4. MÉTODO

### 4.1. Delineamento
**Experimento within-subjects** 3 (meio: papel / tela-simples / tela-hipertexto) × 2 (tipo de texto: narrativo / informativo), com **registro EEG contínuo**.

### 4.2. Participantes
- **N planejado:** 30–40 crianças (com poder para detectar efeitos médios de ERP, d=0.5)
- **Faixa etária:** 8–10 anos (3º ao 5º ano)
- **Critérios de inclusão:**
  - Fluência de leitura ≥ 50 palavras/min (medida por pré-teste)
  - Sem histórico de epilepsia ou fotossensibilidade
  - Sem uso de medicação psicoativa
  - Sem implantes metálicos
  - Consentimento dos pais + assentimento da criança
- **Critérios de exclusão:**
  - Excesso de artefatos EEG (> 30% dos trials)
  - Diagnóstico neuropsiquiátrico formal
  - Recusa em continuar durante a coleta

### 4.3. Local
- **Coleta:** Instituto do Cérebro da UFRN (ICe) — sala de EEG dedicada
- **Recrutamento:** escola parceira (Ipanguaçu ou Currais Novos) — transporte fornecido

### 4.4. Equipamentos
- **EEG:** 32 ou 64 canais (verificar disponibilidade no ICe)
- **Touca:** com gel seco (mais fácil com crianças que gel úmido)
- **Estimulação:** tela calibrada (≥ 22", resolução Full HD, distância fixa de 60 cm)
- **Software de apresentação:** E-Prime 3.0 ou PsychoPy 3
- **Software de análise:** EEGLAB + ERPLAB (MATLAB) ou MNE-Python

### 4.5. Estímulos
- **12 textos** (6 narrativos, 6 informativos), paralelos em:
  - Comprimento (~150 palavras cada)
  - Complexidade sintática
  - Vocabulário (controlado por frequência lexical)
  - Idade-alvo (8–10 anos)
- **3 versões de cada texto:**
  - **Papel:** texto impresso em papel A4
  - **Tela simples:** texto em PDF, sem links
  - **Tela hipertexto:** texto com 3–4 links por texto (sub-páginas com definições, ilustrações)
- **Design contrabalanceado:** cada criança lê os 12 textos em ordem randomizada Latin Square

### 4.6. Procedimentos
1. **Adaptação (10 min):** criança visita o lab, vê o equipamento, faz um teste de leitura
2. **Setup do EEG (20 min):** touca, gel, verificação de impedâncias
3. **Baseline EEG (5 min):** olhos abertos/fechados, em repouso
4. **Bloco de leitura 1 (15 min):** 2 textos (1 papel, 1 tela, ou 1 hipertexto)
5. **Questionários pós-teste (5 min):** compreensão, auto-relato
6. **Pausa (5 min):** lanche, brincadeira
7. **Bloco de leitura 2 (15 min):** 2 textos
8. **Pausa (5 min)**
9. **Bloco de leitura 3 (15 min):** 2 textos
10. **Finalização (10 min):** debriefing, agradecimento, devolutiva
- **Duração total:** ~90 minutos por criança

### 4.7. Medidas

#### EEG
- **ERP components:** N170, P300, N400, P600
- **Power spectrum:** theta (4–7 Hz), beta (13–30 Hz), razão theta/beta
- **Conectividade:** coerência inter-hemisférica em repouso

#### Comportamental
- **Compreensão:** 4 perguntas por texto (múltipla escolha + aberta)
- **Fluência:** palavras/min (medida na leitura em voz alta de 1 texto)
- **Tempo de leitura:** medido pelo software

#### Auto-relato
- Engajamento (escala 0–10)
- Esforço percebido (escala 0–10)
- Preferência (qual meio preferiu)

### 4.8. Análise dos dados

#### Pré-processamento EEG
- Filtragem 0.1–30 Hz + notch 60 Hz
- Re-amostragem para 250 Hz
- Correção de artefatos por ICA (componentes de olho e movimento)
- Rejeição de trials com amplitude > 100 μV
- Baseline: 200 ms pré-stimulus
- Re-referência: average reference

#### Análise ERP
- **Mass-univariate cluster-permutation test** (1.000 permutações)
- Janela: -200 a 1000 ms pós-stimulus
- Clusters definidos por t-test pareado (p < 0.05)
- Correção para múltiplas comparações (cluster-level)

#### Análise de conectividade
- Coerência inter-hemisférica em bandas (theta, alpha, beta)
- Cálculo por par de eletrodos homólogos (F3-F4, C3-C4, P3-P4, O1-O2)

#### Análise estatística
- GLM misto (Meio × Tipo de texto) para componentes ERP
- Correlação Pearson entre marcadores EEG e comportamento
- Modelos de regressão para preditores de compreensão

### 4.9. Aspectos éticos
- CEP/UFRN com protocolo específico para EEG em crianças
- TCLE específico mencionando EEG (com explicação acessível)
- TALE mencionando a touca e o procedimento
- **Cuidado especial:** presença de **psicólogo** durante a coleta (para acolher se a criança se sentir desconfortável)
- **Biossegurança:** touca e gel limpos, sem risco de infecção
- **Transporte:** van com cintos de segurança, seguro de passageiros
- **Debriefing:** explicar o que foi medido, mostrar a forma de onda, deixar a criança brincar com a touca

---

## 5. ORÇAMENTO (estimativa)

| Item | Qtd | Unitário | Total |
|---|---|---|---|
| Uso do EEG (ICe — pode ser gratuito) | 35 h | R$ 0 | R$ 0 |
| Psicóloga (20h) | 1 | R$ 100/h | R$ 2.000 |
| Assistente de pesquisa (100h) | 1 | R$ 50/h | R$ 5.000 |
| Transporte van (10 viagens) | 10 | R$ 600 | R$ 6.000 |
| Material para textos (papel, impressão) | 1 | R$ 500 | R$ 500 |
| Lanche e brincadeiras para crianças | 40 | R$ 30 | R$ 1.200 |
| Licença E-Prime (se necessário) | 1 | R$ 1.500 | R$ 1.500 |
| Inscrição congresso (SRCD, ICOMVE) | 2 | R$ 800 | R$ 1.600 |
| Material de escritório | 1 | R$ 200 | R$ 200 |
| **TOTAL** | | | **R$ 18.000** |

---

## 6. CRONOGRAMA (18 meses)

| Mês | Atividade |
|---|---|
| M1 | Revisão de literatura; alinhamento com ICe |
| M2 | Construção dos textos (12 textos, 3 versões); piloto de EEG (n=2) |
| M3 | Submissão ao CEP; ajustes pós-piloto |
| M4 | Aprovação CEP esperada; piloto ampliado (n=5) |
| M5–M7 | Coleta principal (n=30–40, ao longo de 3 meses) |
| M8 | Pré-processamento EEG (EEGLAB/ERPLAB) |
| M9 | Análise ERP e conectividade |
| M10 | Análise estatística completa |
| M11 | Escrita do paper |
| M12 | Submissão (1ª tentativa) — Developmental Cognitive Neuroscience |
| M13–M14 | Resposta aos revisores ou submissão alternativa |
| M15 | Apresentação ICOMVE / SRCD |
| M16–M18 | Paper final, devolutiva, próximos passos |

---

## 7. REFERÊNCIAS (preliminares)

- Cohen, M. X. (2014). *Analyzing Neural Time Series Data*. MIT Press.
- Dehaene, S. (2010). *Reading in the Brain*. Viking.
- Luck, S. J. (2014). *An Introduction to the Event-Related Potential Technique* (2nd ed.). MIT Press.
- Stavanger, C. J. et al. (2024). Screen reading and the brain in children. *npj Science of Learning*, 9, 12.
- Wolf, M. (2018). *Reader, Come Home*. Harper.
- Snowling, M. J. & Hulme, C. (eds.) (2020). *The Science of Reading: A Handbook*. Wiley-Blackwell.

---

## 8. PRÉ-REGISTRO

Será pré-registrado no OSF antes da coleta. Template em `00-fundamentos/preregistracao/template-osf.md`.

---

## 9. RISCOS E LIMITAÇÕES

### Riscos
- **Fadiga da criança** (protocolo longo) — mitigação: pausas, brincadeira, debriefing
- **Estresse do EEG** (criança pode ter medo) — mitigação: psicóloga presente, explicação acessível
- **Movimentos durante a leitura** — esperado, controlado por ICA e rejeição
- **Artefatos de piscar** — esperado, controlado por ICA

### Limitações
- N moderado (30–40) — efeitos pequenos podem não ser detectados
- Apenas uma faixa etária (8–10) — generalização limitada
- Contexto específico (escola pública do interior do RN) — generalização limitada
- Não mede uso real em longo prazo — apenas tarefa experimental

---

## 10. ANEXOS (a criar)

- [ ] TCLE específico para EEG
- [ ] TALE específico para EEG
- [ ] 12 textos com 3 versões
- [ ] Questionário de compreensão
- [ ] Protocolo de piloto
- [ ] Pipeline EEG documentado
- [ ] Dicionário de variáveis

---

> **Próximo passo:** agendar reunião com a Angela + Prof. Antonio Pereira (ICe) para alinhamento; verificar disponibilidade de EEG e sala.
