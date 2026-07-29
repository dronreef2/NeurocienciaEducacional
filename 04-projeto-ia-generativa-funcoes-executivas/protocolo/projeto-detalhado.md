# 📄 Projeto Detalhado — P04 (IA Generativa × Funções Executivas)

> **Status:** v0.1 — piloto
> **Projeto:** Uso de IA generativa (ChatGPT, Claude, Gemini) e suas relações com funções executivas em adolescentes
> **Pesquisadora:** [Seu nome]
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold (UFRN)
> **Linha:** Cognição + tecnologia (transversal ao Leitura + Neurociências)

---

## 1. RESUMO

Este estudo transversal correlacional investiga a relação entre o **padrão de uso de IA generativa** (frequência, tipo de tarefa, tempo de uso) e o **desempenho em funções executivas (FE)** — memória de trabalho, controle inibitório, flexibilidade cognitiva — em **adolescentes de 12–16 anos** (N=150–300). As FE são avaliadas por **bateria computadorizada** (N-back, Stroop, WCST, Keeping Track). A qualidade de escrita é avaliada por **comparação de redações com e sem IA**. Análise por **equações estruturais (SEM)** com o modelo de 3 FE de Miyake. Resultados esperados: contribuir com a literatura sobre **cognitive offloading** (Risko & Gilbert, 2016) e informar políticas de letramento digital em escolas.

**Palavras-chave:** IA generativa, funções executivas, adolescentes, offloading cognitivo, equações estruturais, letramento digital.

---

## 2. INTRODUÇÃO E JUSTIFICATIVA

A **IA generativa** (ChatGPT, Claude, Gemini) está profundamente presente na vida de adolescentes brasileiros. Pesquisa do **TIC Kids Online Brasil 2024** indica que **70% dos adolescentes de 12–17 anos** usam IA generativa para tarefas escolares. Porém, **quase não há evidência** sobre os efeitos cognitivos desse uso.

A literatura internacional começa a abordar o tema. Trabalhos recentes (Anthropic, OpenAI) documentam o fenômeno de **"cognitive offloading"** (Risko & Gilbert, 2016) — o uso de ferramentas externas para reduzir demanda cognitiva. O impacto de longo prazo sobre **funções executivas** (memória de trabalho, inibição, flexibilidade) é uma **preocupação teórica central**, mas há **poucos dados empíricos com adolescentes**.

Este projeto preenche essa lacuna, com foco em:
- **Padrões de uso** (frequência, tipo de tarefa, contexto)
- **FE específicas** (não FE global) — distinguindo os 3 fatores de Miyake
- **Análise SEM** para modelar relações complexas
- **Contexto brasileiro** — com adolescentes de escola pública

---

## 3. OBJETIVOS

### 3.1. Objetivo geral
Investigar a relação entre padrões de uso de IA generativa e o desempenho em funções executivas em adolescentes de 12–16 anos.

### 3.2. Objetivos específicos
1. Caracterizar o **uso de IA generativa** na amostra (frequência, tipo de tarefa, contexto)
2. Medir o **desempenho em FE** (memória de trabalho, inibição, flexibilidade) com bateria computadorizada
3. Testar o **modelo de 3 FE de Miyake** (shifting, updating, inhibition) com análise fatorial confirmatória
4. Examinar a **relação** entre uso de IA e FE (correlações, regressões, SEM)
5. Investigar **moderação** por sexo, idade, SES, AI literacy
6. Comparar **redações com e sem IA** (qualidade textual, esforço percebido)

---

## 4. MÉTODO

### 4.1. Delineamento
**Estudo transversal correlacional** com componente qualitativo (análise de redações).

### 4.2. Participantes
- **N planejado:** 150–300 adolescentes (poder estatístico para SEM com 3 fatores)
- **Faixa etária:** 12–16 anos (6º ao 9º ano do Ensino Fundamental)
- **Critérios de inclusão:** matriculados em escola parceira; com consentimento dos pais + assentimento
- **Critérios de exclusão:** diagnóstico neuropsiquiátrico formal; uso de medicação psicoativa
- **Recrutamento:** 3–5 escolas (presenciais ou amostragem online com verificação parental)

### 4.3. Instrumentos

#### 4.3.1. Bateria computadorizada de FE
Aplicada individualmente ou em pequenos grupos (≤ 10), em sessão de ~45 min.

| FE | Tarefa | Variável dependente |
|---|---|---|
| **Memória de trabalho (updating)** | N-back (1, 2, 3-back) | Acurácia por nível, d' |
| **Controle inibitório** | Stroop computadorizado (palavra-cor) | Tempo de reação incompatível, taxa de erro |
| **Controle inibitório** | Stop-Signal Task | Stop Signal Reaction Time (SSRT) |
| **Flexibilidade cognitiva (shifting)** | Wisconsin Card Sorting Test (WCST) computadorizado | % de erros perseverativos, % de acertos |
| **Flexibilidade cognitiva (shifting)** | Trail Making B (versão digital) | Tempo, erros |
| **Memória de trabalho (updating)** | Keeping Track | Acurácia |

**Software:** PsychoPy 3 (open source) ou Inquisit (licença paga).

#### 4.3.2. Tarefa de escrita (com e sem IA)
- **Tema da redação:** definido a partir de temas de ENEM (ex: "O impacto da inteligência artificial na educação")
- **Condição 1:** escrever SEM IA, 30 min
- **Condição 2:** escrever COM ChatGPT disponível, 30 min
- **Ordem contrabalanceada**
- **Variáveis dependentes:** qualidade textual (rubrica ENEM), originalidade (TTCT), esforço percebido (escala Likert), número de prompts usados

#### 4.3.3. Questionários
- **Questionário de uso de IA** (a validar): frequência, tipo de tarefa, contexto, percepção de dependência
- **AI literacy scale** (a adaptar de Ng et al. 2024 ou similar)
- **Escala de autoeficácia acadêmica** (adaptação de Bandura)
- **Questionário sociodemográfico**

### 4.4. Procedimentos
1. **Mês 1–2:** Adaptação de instrumentos + desenvolvimento da bateria
2. **Mês 3:** Submissão ao CEP
3. **Mês 4:** Piloto (n=20) — ajustes
4. **Mês 5–7:** Coleta principal (em sala, com tablets)
5. **Mês 8:** Análise quantitativa (R + lavaan)
6. **Mês 9:** Análise qualitativa das redações
7. **Mês 10–12:** Escrita e submissão do paper

### 4.5. Análise dos dados

#### Análise primária
- **Análise fatorial confirmatória** do modelo de 3 FE (lavaan, R)
- **Índices de ajuste:** CFI, TLI, RMSEA, χ²/df
- **Correlações** entre uso de IA e FE
- **Regressão múltipla** com controles (sexo, idade, SES, AI literacy)
- **Modelos de equações estruturais (SEM):** uso de IA → offloading → FE

#### Análise secundária
- **Análise de mediação:** offloading como mediador entre uso e FE
- **Análise de moderação:** sexo, idade, SES
- **Análise qualitativa** das redações: comparação de qualidade entre condições

### 4.6. Aspectos éticos
- CEP/UFRN
- TCLE dos pais
- TALE dos adolescentes (linguagem acessível)
- **Cuidado especial:** tópico sensível — adolescentes podem revelar uso problemático
- **Plano de encaminhamento:** se algum adolescente reportar uso problemático, oferecer encaminhamento para apoio psicológico escolar
- **Debriefing** sobre uso equilibrado de IA
- **Anonimização rigorosa** (adolescentes podem ter receio de ser identificados)

---

## 5. ORÇAMENTO

| Item | Qtd | Unitário | Total |
|---|---|---|---|
| Tablets (15) | 15 | R$ 800 | R$ 12.000 |
| Licença Inquisit (alternativa) | 1 | R$ 3.000 | R$ 3.000 |
| Psicóloga (40h) | 1 | R$ 100/h | R$ 4.000 |
| Assistente de pesquisa (200h) | 1 | R$ 50/h | R$ 10.000 |
| Transporte | 30 visitas | R$ 80 | R$ 2.400 |
| Material de escritório | 1 | R$ 300 | R$ 300 |
| Lanche | 200 × 2 | R$ 5 | R$ 2.000 |
| Inscrição congresso (SRCD, ICOMVE) | 2 | R$ 800 | R$ 1.600 |
| **TOTAL** | | | **R$ 35.300** |

---

## 6. CRONOGRAMA (12 meses)

| Mês | Atividade |
|---|---|
| M1 | Adaptação de instrumentos; adaptação de AI literacy scale |
| M2 | Desenvolvimento da bateria computadorizada (PsychoPy) |
| M3 | Submissão ao CEP; pilotagem da bateria (n=5) |
| M4 | Piloto ampliado (n=20); ajustes |
| M5 | Coleta — bateria FE (escola 1) |
| M6 | Coleta — bateria FE (escolas 2 e 3) |
| M7 | Coleta — tarefa de escrita + questionários |
| M8 | Análise quantitativa (R + lavaan) |
| M9 | Análise qualitativa das redações |
| M10 | Submissão do paper (Computers in Human Behavior) |
| M11 | Resposta a revisores (se houver) |
| M12 | Apresentação (SRCD ou EARLI) |

---

## 7. REFERÊNCIAS (preliminares)

- Bender, E. M. et al. (2021). On the dangers of stochastic parrots. *FAccT '21*.
- Diamond, A. (2013). Executive functions. *Annual Review of Psychology*, 64, 135–168.
- Howard-Jones, P. (2014). *Neurociência e Educação*. Artmed.
- Miyake, A. et al. (2000). The unity and diversity of executive functions. *Cognitive Psychology*, 41, 49–100.
- Mollick, E. (2024). *Co-Intelligence*. Portfolio.
- Risko, E. F. & Gilbert, S. J. (2016). Cognitive offloading. *Trends in Cognitive Sciences*, 20(9), 676–688.
- Zelazo, P. D. (2020). Executive function and psychopathology. *Annual Review of Clinical Psychology*, 16, 139–164.

---

## 8. PRÉ-REGISTRO

Será pré-registrado no OSF antes da coleta. Template em `00-fundamentos/preregistracao/template-osf.md`.

---

## 9. RISCOS E LIMITAÇÕES

### Riscos
- **Tópico sensível:** adolescentes podem ter receio de ser identificados como "usuários" ou "não usuários"
- **Causalidade reversa:** não dá para saber se uso de IA causa mudança em FE, ou se adolescentes com FE mais baixas usam IA mais
- **Viés de auto-relato:** adolescentes podem subnotificar uso
- **Variação da tecnologia:** a IA de 2028 será diferente da IA de 2024 — generalização temporal limitada

### Limitações
- Transversal → não permite inferência causal
- Amostra específica (escolas do Seridó/RN) → generalização limitada
- Bateria de FE em português — poucos estudos normativos
- Idade restrita (12–16) — não cobre início da exposição

---

## 10. ANEXOS (a criar)

- [ ] Adaptação da AI literacy scale
- [ ] Tarefa de escrita (rubrica ENEM)
- [ ] TCLE específico para adolescentes
- [ ] TALE específico para adolescentes
- [ ] Roteiro de coleta
- [ ] Dicionário de variáveis
- [ ] Script R de análise SEM

---

> **Próximo passo:** revisar com a Angela; alinhar com a rede de escolas parceiras; submeter pré-registro.
