# Submission Readiness Report — P01

> **Executado pelo playbook:** `.agent/playbooks/submeter-p01.md` (v1.0)
> **Gerado por:** Conductor (Mavis) + Research + Methodology + Compliance + Review Agents
> **Data:** 2026-09-19
> **Versão:** 1.0 (1ª execução — primeiro integration test do Research OS)
> **Target:** CEP/UFRN + *Computers & Education* (Computers & Education Open)

---

## ⚠️ DISTINÇÃO CRÍTICA (ler antes)

```
DOCUMENTALMENTE COMPLETO    ≠    CIENTIFICAMENTE VALIDADO    ≠    ETICAMENTE APROVADO
        (arquivos existem)            (Ângela revisou)            (CEP concedeu parecer)
```

Este relatório distingue **explicitamente** entre esses três estados. **Conclusão final:** P01 está **DOCUMENTALMENTE COMPLETO** mas **CIENTIFICAMENTE NÃO VALIDADO** e **ETICAMENTE NÃO APROVADO**.

---

## Resumo executivo

| Dimensão | Status |
|---|---|
| **Documentação** | ✅ 14/15 documentos obrigatórios prontos (93%) |
| **Validação científica (Ângela)** | ❌ Pendente — reunião ainda não realizada |
| **Aprovação ética (CEP)** | ❌ Não submetido |
| **Submissão OSF** | ⏳ JSON validado, falta `--all` com token |
| **Submissão journal** | ❌ Manuscrito v1 (rascunho, sem revisão da Ângela) |

**Status global:** 🟡 **NEEDS WORK — bloqueado por revisão humana (HUMAN GATE)**

**Gargalo real:** Reunião com Ângela (autorização + revisão + carta anuência).

---

## 1. Objetivo

**Objetivo geral (verificado em `protocolo/projeto-detalhado.md` v0.1):**
> Compreender como crianças de 8 a 11 anos, matriculadas em escola pública parceira do Projeto Leitura + Neurociências (UFRN), percebem, interpretam e (re)negociam sua relação de aprendizagem com tutores de IA generativa em atividades escolares.

**Objetivos específicos (6):**
1. Identificar representações das crianças sobre o tutor de IA
2. Descrever estratégias metacognitivas emergentes
3. Analisar fatores contextuais mediadores
4. Investigar como a criança distingue a IA do professor humano
5. Produzir subsídios para desenho de IAs eticamente responsáveis
6. Gerar insumos para políticas públicas

**Observação metodológica:** Projeto-detalhado cita "crianças de 8-11 anos" mas manuscrito v1 foca em "2º ano (7-8 anos)" — **inconsistência** a resolver.

---

## 2. Hipóteses

**Em formato qualitativo, o projeto-detalhado NÃO formula hipóteses formais** (apropriado para pesquisa qualitativa exploratória).

**Hipóteses implícitas (reconstruídas pela IA, NÃO verificadas):**
- H-impl-1: Crianças constroem uma "Teoria da Mente de Máquina" funcional mas em desenvolvimento
- H-impl-2: O método socrático do Khanmigo favorece detecção precoce de erro
- H-impl-3: Confiança é calibrada por contexto (matemática vs interpretação)
- H-impl-4: Crianças distinguem IA de humanos funcionalmente, mas antropomorfizam parcialmente

**Status:** ⚠️ Hipóteses implícitas — devem ser explicitadas no manuscrito (Braun & Clarke 2022 não exige hipóteses pré-definidas, mas exige clareza sobre posicionamento epistemológico).

**Manuscrito v1:** Identificou 5 temas no piloto que **sugerem** essas hipóteses, mas são resultados, não hipóteses.

---

## 3. Pergunta de pesquisa

**Verificada no manuscrito v1:**
> "Como crianças do 2º ano do ensino fundamental interpretam, vivenciam e confiam no tutor de IA Khanmigo após 8 semanas de uso?"

**Inconsistência:**
- Manuscrito v1: **"2º ano, 7-8 anos, 8 semanas"**
- Projeto-detalhado: **"3º ao 5º ano, 8-11 anos"**

**Decisão necessária:** qual é a pergunta correta? Sugestão: focar **2º ano** (mais conservador, dados piloto já são com 7-8 anos).

---

## 4. Fundamentação teórica

**Status:** ✅ Documentado de forma abrangente.

**Pilares teóricos identificados:**

| Pilar | Referência | Nota de leitura? |
|---|---|---|
| Análise Temática Reflexiva | Braun & Clarke 2006, 2022 | ✅ Sim |
| Teoria da Mente | Premack & Woodruff 1978 | ❌ Não |
| MToM (Machine Theory of Mind) | Kahn et al. 2012, Liu et al. 2023 | ❌ Não |
| Funções executivas | Diamond 2013 | ✅ Sim |
| Metacognição | Flavell 1979, Veenman 2011, Zimmerman 2002 | ❌ Não |
| Leitura + Neurociências | Naschold 2017 | ✅ Sim |
| Reading in the Brain | Dehaene 2010 | ✅ Sim |

**Lacunas teóricas:**
- Não há nota de leitura específica sobre **MToM em crianças** (Liu et al. 2023 é citado mas não lido)
- Não há nota sobre **crianças e Alexa/Siri** (McReynolds et al. 2017 citado mas não lido)
- Não há nota sobre **privacidade infantil + IA**

**Recomendação técnica (R01):** ler pelo menos 3 papers adicionais antes de submeter (MToM, privacidade infantil, chatbots educacionais).

---

## 5. Metodologia

**Status:** ✅ Documentação sólida.

**Decisões metodológicas verificadas:**

| Decisão | Valor | Fonte |
|---|---|---|
| Tipo | Qualitativa exploratória-descritiva | projeto-detalhado §5.1 |
| Abordagem | Análise Temática Reflexiva (6 fases) | projeto-detalhado §5.6, braun-clarke-2022-aplicacao |
| Triangulação | Métodos múltiplos + fontes | projeto-detalhado §5.1 |
| Software análise | Taguette (grátis, open source) | projeto-detalhado §5.6 |
| Codificação | 2 pesquisadores independentes + consenso | projeto-detalhado §5.6 |

**Inconsistências metodológicas:**

1. **N de participantes:**
   - projeto-detalhado: 20-30 crianças
   - manuscrito v1: 3 crianças (piloto)
   - pré-registro OSF: "12-15 crianças (saturação)"
   - STATE.yaml: 12-15

   → **3 valores diferentes para o mesmo parâmetro.**

2. **Escolaridade:**
   - projeto-detalhado: 3º ao 5º ano (8-11 anos)
   - manuscrito v1: 2º ano (7-8 anos)
   - manuscrito cita "≥8 semanas de uso" mas piloto teve 17 dias

3. **Duração da coleta:**
   - projeto-detalhado: 2 semanas de diário + 8 semanas de uso
   - manuscrito v1: 17 dias (piloto)

4. **Cenário:**
   - projeto-detalhado: Ipanguaçu OU Currais Novos
   - carta-anuência: "município de [Ipanguaçu ou Currais Novos]"
   - manuscrito v1: Natal/RN

   → **3 municípios diferentes.**

---

## 6. Participantes

**Status:** ⚠️ Critérios documentados, mas N inconsistente.

**Critérios verificados:**

**Inclusão (projeto-detalhado §5.3):**
- 8-11 anos
- Matriculados na escola parceira
- ≥1 mês de uso do tutor
- TCLE + TALE assinados

**Exclusão (projeto-detalhado §5.3):**
- Diagnóstico neuropsiquiátrico formal
- Não ter usado o tutor no mês anterior

**Amostra documentada:**
- projeto-detalhado: 20-30 crianças (justificativa: Guest et al. 2006)
- pré-registro OSF: 12-15
- manuscrito v1: 3 crianças (piloto)

**Piloto atual (3 crianças):**
- C01 Maria (7 anos, F, 17 dias)
- C02 Pedro (8 anos, M, 17 dias)
- C03 Júlia (8 anos, F, 16 dias)

**Lacunas:**
- Não há critérios explícitos para **composição por sexo** (projeto-detalhado diz "equitativamente entre sexos" mas não operacionaliza)
- Não há critérios para **escolaridade específica** (projeto-detalhado diz 3º-5º mas manuscrito v1 diz 2º)

**Recomendação técnica (R02):** harmonizar N (sugestão: 12-15 crianças do 2º ano, alinhado com pré-registro e piloto).

---

## 7. Instrumentos

**Status:** ✅ 7/8 documentos prontos (88%).

**Inventário verificado:**

| Instrumento | Arquivo | Versão | Status |
|---|---|---|---|
| Roteiro de entrevista | `01-roteiro-entrevista.md` | v0.1 | ✅ |
| Protocolo think-aloud | `02-protocolo-thinkaloud.md` | v0.1 | ✅ |
| ~~Prompt do desenho projetivo~~ | `03-prompt-desenho.md` | — | ❌ NÃO EXISTE (opcional, usar do roteiro) |
| Template diário | `04-diario-uso.md` | v0.1 | ✅ |
| Questionário pais | `05-questionario-pais.md` | v0.1 | ✅ |
| Questionário professores | `06-questionario-professores.md` | v0.1 | ✅ |
| TCLE pais | `07-tcle-pais.md` | v0.1 | ✅ |
| TALE criança | `08-tale-crianca.md` | v0.1 | ✅ |

**Lacunas:**
- ❌ Falta `03-prompt-desenho.md` (checklist-cep.md lista como pendente — mas não é bloqueante se o prompt estiver embutido no roteiro de entrevista)

**Qualidade dos instrumentos:**
- TCLE/TALE: ✅ Linguagem acessível, atende CNS 466/2012 + 510/2016
- Roteiro de entrevista: ✅ Semiestruturado, permite flexibilidade
- Diário: ✅ Espaço para escrita/desenho, com instruções claras
- Questionários: ✅ Breves (10-15 min)

**Pontos fortes:**
- Triangulação de métodos (entrevista + think-aloud + diário + desenhos + questionários)
- Inclui perspectiva de pais e professores (não só da criança)
- TALE com linguagem apropriada para 8-11 anos

---

## 8. Procedimentos

**Status:** ✅ Documentados em 5 etapas.

**Procedimentos verificados (projeto-detalhado §5.5):**

1. Contato com escola (semana 1)
2. Reunião com pais (semana 2)
3. Piloto com 3 crianças (semanas 3-4)
4. Coleta formal (semanas 5-10)
5. Acompanhamento do diário (semanas 6-8)

**Pontos fortes:**
- Plano de coleta estruturado em 5 etapas
- Inclui piloto antes da coleta formal (validação de instrumentos)
- Acompanhamento longitudinal do diário

**Lacunas:**
- Não há **procedimento de interrupção** se houver desconforto (projeto-detalhado §5.7 menciona "plano de interrupção" mas não detalha)
- Não há **protocolo de encaminhamento** psicológico se necessário (checklist-cep.md lista como pendente)
- Não há **procedimento de devolutiva** detalhado (projeto-detalhado menciona mas não operacionaliza)

**Recomendação técnica (R03):** detalhar protocolo de interrupção e encaminhamento (CNS 510/2016 exige).

---

## 9. Análise

**Status:** ✅ Método bem definido.

**Análise verificada (projeto-detalhado §5.6):**

| Fase | Atividade | Ferramenta | Quem |
|---|---|---|---|
| 1 | Familiarização (transcrição + leitura repetida) | Manual + áudio | Pesquisadora |
| 2 | Geração de códigos iniciais | Taguette | 2 codificadores independentes |
| 3 | Busca por temas | Taguette | Pesquisadora |
| 4 | Revisão dos temas | Discussão | Equipe |
| 5 | Definição e nomeação | Discussão | Equipe |
| 6 | Produção do relatório | Markdown + Word | Pesquisadora |

**Software:** Taguette (open source, grátis)

**Pontos fortes:**
- 6 fases Braun & Clarke 2022 (versão atualizada)
- Codificação independente por 2 pesquisadores (aumenta confiabilidade)
- Discussão de consensos explícita

**Lacunas:**
- Não há **critério de saturação** operacionalizado (apenas "20-30 crianças" no projeto-detalhado)
- Não há **estratégia para discordâncias** entre codificadores (apenas "discussão de consensos")
- Não há **plano para apresentar resultados negativos**

**Pilotagem da análise (verificada em `analise/piloto-completo.R`):**
- Pipeline R com `at_pipeline.R`
- Suporta wordcloud
- Output: `resultados/P01_piloto/`

---

## 10. Ética

**Status:** ⏳ Documentação ética completa, mas SEM aprovação CEP.

**Itens éticos documentados (projeto-detalhado §5.7):**

- ✅ TCLE assinado pelos pais (modelo pronto)
- ✅ TALE assinado pelas crianças (modelo pronto)
- ✅ Anonimização (códigos C1, C2...)
- ✅ Direito de desistência
- ✅ Devolutiva para escola/famílias/crianças
- ✅ Plano de interrupção se desconforto
- ✅ Uso de tutor de IA homologado
- ✅ Armazenamento criptografado, destruição em 5 anos

**Conformidade legal verificada:**
- ✅ Resolução CNS 466/2012 (pesquisa com seres humanos)
- ✅ Resolução CNS 510/2016 (pesquisa em ciências humanas e sociais, com crianças)
- ✅ Lei 13.257/2016 (Marco Legal da Primeira Infância)
- ✅ LGPD (Art. 7º, IV — consentimento específico)

**Pendências:**
- ❌ Submissão à Plataforma Brasil NÃO FEITA
- ❌ CAAE (Comitê de Ética) não obtido
- ❌ Parecer CEP não concedido

**HUMAN GATE:** Submissão ao CEP é decisão humana (não automatizar). Antes de submeter, a Ângela precisa ter revisado o projeto.

---

## 11. LGPD

**Status:** ✅ LGPD compliance documentado, ⚠️ não auditado.

**Itens LGPD verificados:**

| Requisito LGPD | Status |
|---|---|
| Base legal para tratamento (consentimento específico) | ✅ TCLE + TALE |
| Finalidade específica | ✅ Pesquisa científica (Art. 7º, IV) |
| Necessidade (minimalidade) | ✅ Apenas dados necessários |
| Transparência | ✅ TCLE/TALE explicam uso |
| Segurança (criptografia) | ✅ Mencionado no projeto-detalhado |
| Retenção (5 anos) | ✅ Documentado |
| Direitos do titular (acesso, correção, exclusão) | ⚠️ Parcialmente (não detalhado no TCLE) |
| Encarregado (DPO) | ❌ Não mencionado |

**Lacunas LGPD:**
- Não há **DPO (Data Protection Officer)** identificado
- Não há **procedimento para exercício de direitos** pelo titular (criança, via pais)
- Não há **RIPD (Relatório de Impacto à Proteção de Dados)** — pode ser exigido para pesquisa com crianças

**Recomendação técnica (R04):** incluir DPO da UFRN ou responsável institucional + RIPD simplificado (LGPD Art. 38).

---

## 12. Evidências

**Status:** ⚠️ Evidências parciais — piloto limitado.

**Evidências existentes:**

| Evidência | Tipo | Onde | Status |
|---|---|---|---|
| Dados piloto (3 crianças, 17 dias) | Qualitativa primária | `01-projeto-qualitativo-criancas-ia/dados/piloto/` | ⚠️ NÃO VERSIONADO (LGPD-safe se sintético) |
| Dados sintéticos (15 crianças, 179 linhas) | Qualitativa sintética | `dados_sinteticos/P01_diarios_sinteticos.csv` | ✅ Para demo |
| 13 notas de leitura | Bibliográfica | `00-fundamentos/notas-leitura/` | ✅ |
| Manuscrito v1 (rascunho) | Rascunho | `docs/manuscritos/P01-manuscrito-rascunho-v1.md` | ⚠️ Sem revisão |
| Pipeline de análise R | Técnico | `01-projeto-qualitativo-criancas-ia/analise/` | ✅ |
| Pré-registro OSF (5 JSONs) | Metodológico | `docs/osf-json/P0*-osf.json` | ✅ Validado, NÃO submetido |

**Forças:**
- 13 notas de leitura estruturadas (papers seminais)
- Manuscrito v1 já identifica 5 temas no piloto
- Pré-registro validado (formato OSF v2 + metadados ricos para P02/P03)

**Lacunas:**
- Piloto muito limitado (3 crianças, 17 dias)
- Não há análise de poder estatístico (não se aplica a quali, mas pode-se argumentar sobre saturação)
- Não há dados de questionários dos pais ou professores
- Não há gravações de áudio transcritas (LGPD — ficaria fora do repo)

**Recomendação técnica (R05):** expandir piloto para pelo menos 5 crianças antes da coleta formal (saturação inicial).

---

## 13. Lacunas (consolidado)

**Lacunas prioritárias (bloqueiam submissão):**

1. ❌ **N de participantes:** 3 valores diferentes (20-30, 12-15, 3) — harmonizar
2. ❌ **Escolaridade:** 2 valores diferentes (3º-5º, 2º) — harmonizar
3. ❌ **Cenário (município):** 3 valores diferentes (Ipanguaçu, Currais Novos, Natal) — definir
4. ❌ **Revisão da Ângela:** não realizada (HUMAN GATE)
5. ❌ **Carta de anuência:** template pronto, NÃO obtida
6. ❌ **CAAE + Parecer CEP:** não submetido

**Lacunas secundárias (melhorariam qualidade):**

7. ⚠️ Notas de leitura sobre MToM, privacidade infantil, chatbots educacionais
8. ⚠️ Critérios de saturação operacionalizados
9. ⚠️ Estratégia para discordâncias entre codificadores
10. ⚠️ Protocolo de interrupção + encaminhamento detalhado
11. ⚠️ DPO + RIPD identificados
12. ⚠️ Hipóteses explícitas (ou posicionamento epistemológico claro)
13. ⚠️ Procedimento de devolutiva operacionalizado
14. ⚠️ Análise de questionários de pais/professores (pipeline estatístico)

---

## 14. Inconsistências entre documentos

| Tópico | projeto-detalhado | manuscrito v1 | pré-registro OSF | STATE.yaml |
|---|---|---|---|---|
| N participantes | 20-30 | 3 (piloto) | 12-15 | 12-15 |
| Escolaridade | 3º-5º ano | 2º ano | (não claro) | (não claro) |
| Idade | 8-11 anos | 7-8 anos | (não claro) | (não claro) |
| Município | Ipanguaçu/C.Novos | Natal/RN | (não claro) | (não claro) |
| Duração uso | "≥1 mês" | "8 semanas" | (não claro) | (não claro) |

**Recomendação técnica (R06):** criar **CHANGELOG-decisions.md** consolidando decisões canônicas e propagando para todos os documentos.

---

## 15. Decisões que dependem da Ângela (HUMAN GATE)

### D01 — Aceitar orientação formal do mestrado PPGED
- **Opções:** Sim / Não / Condicional
- **Bloqueia:** tudo (sem orientadora, sem CEP, sem submissão)

### D02 — Revisar o projeto-detalhado e aprovar versão final v1.0
- **Bloqueia:** submissão ao CEP
- **Estimativa:** 1 semana de revisão

### D03 — Revisar o manuscrito v1 e aprovar versão final v2.0
- **Bloqueia:** submissão a *Computers & Education*
- **Estimativa:** 2 semanas de revisão

### D04 — Indicar escola parceira (Ipanguaçu / Currais Novos / outra)
- **Bloqueia:** carta de anuência
- **Recomendação IA:** escola parceira do L+N

### D05 — Apresentar à direção da escola parceira
- **Bloqueia:** carta de anuência
- **Estimativa:** 1 reunião

### D06 — Definir cronograma de reuniões mensais de orientação
- **Bloqueia:** alinhamento do programa
- **Sugestão:** 1ª terça de cada mês, 14h (Natal) / 15h (Caicó)

### D07 — Co-autoria no manuscrito (CRediT — qual papel?)
- **Opções:** autor sênior (último) / co-autora intermediária
- **Sugestão POLITICA-AUTORIA.md:** autor sênior

### D08 — Submeter ao CEP? (decisão sua, Ângela, e Plataforma Brasil)
- **Pré-requisito:** D01 + D02 + D04 + D05

### D09 — Submeter a *Computers & Education*? (decisão sua, Ângela, e o journal)
- **Pré-requisito:** D01 + D03

### D10 — Aceitar submissão do pré-registro ao OSF em meu nome (com co-autoria Ângela)?
- **Pré-requisito:** D01

---

## 16. Próximos passos (cronograma reverso)

### Imediato (esta semana, 2026-09-19 a 2026-09-25)
- [ ] Enviar email para Ângela com kit de reunião (já pronto: `docs/email-angela-2026-09-reuniao.md`)
- [ ] Marcar data/hora com ela (3 slots oferecidos: 03-05/09)
- [ ] Atualizar Lattes + ORCID (D02 pré-requisito)
- [ ] Harmonizar N (12-15) + escolaridade (2º ano) — decidir e propagar

### Curto prazo (até 2026-09-30)
- [ ] **Reunião com Ângela** (D01 + D02 + D03 + D04 + D07)
- [ ] Carta de anuência enviada à escola (D05)
- [ ] Versões finais dos documentos (com placeholders preenchidos)

### Médio prazo (até 2026-10-15)
- [ ] Submissão P01 ao CEP via Plataforma Brasil (D08)
- [ ] Submissão P01 a *Computers & Education* (D09)
- [ ] Submissão 5 pré-registros ao OSF (D10) — `python3 osf_submit.py --all`

### Longo prazo (até 2026-12)
- [ ] Aprovação CEP prevista (1-3 meses após submissão)
- [ ] Piloto expandido (5-7 crianças, validar saturação inicial)
- [ ] Manuscrito v2 incorporando revisões Ângela

### Anual (até 2027-03)
- [ ] Coleta formal P01 (12-15 crianças)
- [ ] Análise completa (Braun & Clarke 6 fases)
- [ ] Manuscrito final
- [ ] **Publicação P01** (target Q1/2027)

---

## ✅ Checklist de entrega (o que falta)

- [ ] Submissão CEP (após D01-D05-D08)
- [ ] Submissão journal (após D01-D03-D09)
- [ ] Submissão OSF (após D01-D10 + `OSF_TOKEN`)
- [ ] Carta de anuência assinada (após D04-D05)
- [ ] Lattes + ORCID atualizado (esta semana)
- [ ] Versões finais documentos (após D02-D03)

---

## 📊 Resumo final

| Status | Significado |
|---|---|
| ✅ **DOCUMENTALMENTE COMPLETO** | 14/15 documentos obrigatórios prontos, 179 linhas de dados sintéticos, 13 notas de leitura, manuscrito v1 (rascunho) |
| ❌ **CIENTIFICAMENTE NÃO VALIDADO** | Ângela não revisou; manuscrito v1 é rascunho; hipóteses implícitas; inconsistências entre documentos |
| ❌ **ETICAMENTE NÃO APROVADO** | Não submetido ao CEP; TCLE/TALE prontos mas sem coleta real; LGPD compliance parcial |

**Recomendação do Conductor (NÃO decisão):**
> "Aguarde a reunião com a Ângela. Depois dela, com D01-D05 resolvidos, o P01 estará pronto para submissão ao CEP e ao journal em 1-2 sprints. Submissão é decisão humana — **não submeter automaticamente**."

---

## 🔗 Outputs deste playbook

- Este relatório: `.agent/reports/submission-readiness-P01-2026-09-19.md`
- Próximo passo: `.agent/playbooks/reuniao-angela.md` (gerar `meeting-angela-P01-2026-09-19.md`)

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após reunião com Ângela (atualizar D01-D10)
