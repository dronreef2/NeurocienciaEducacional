# Meeting Agenda — Ângela × P01

> **Executado pelo playbook:** `.agent/playbooks/reuniao-angela.md` (v1.0)
> **Input:** `.agent/reports/submission-readiness-P01-2026-09-19.md`
> **Gerado por:** Conductor (Mavis) — separando FATOS / HIPÓTESES / DECISÕES / PERGUNTAS / RECOMENDAÇÕES
> **Data:** 2026-09-19
> **Duração alvo:** 30 min (versão confortável)

---

## 🎯 Objetivo da reunião

Alinhar 3 decisões críticas (orientação, autorização P01, escola parceira) para desbloquear submissão CEP e *Computers & Education* no Q3/2026.

---

## 📋 Estrutura da reunião

```
00:00-00:03  Abertura + pitch 1-min
00:03-00:08  Pitch central (programa + P01)
00:08-00:13  Decisões (D01-D10)
00:13-00:23  Negociação (respostas D01-D10, ajustar escopo)
00:23-00:27  Plano de ação (próximos 30 dias)
00:27-00:30  Fechamento (assinar termo + agendar próxima)
```

---

## 📦 FATOS VERIFICADOS (F01–F08)

> O que **foi verificado** no repositório. Ângela pode confiar.

### F01 — Documentação P01 está ~93% completa
- 14/15 documentos obrigatórios prontos
- Faltando apenas: prompt do desenho (opcional) + carta de anuência (depende escola)
- Fonte: `.agent/reports/submission-readiness-P01-2026-09-19.md` §7

### F02 — Manuscrito P01 v1 já tem 5 temas identificados (piloto)
- 3 crianças, 17 dias (Maria 7a, Pedro 8a, Júlia 8a)
- 5 temas: antropomorfização, detecção de erro, confiança calibrada, comparação humana, preferência contextual
- Fonte: `docs/manuscritos/P01-manuscrito-rascunho-v1.md`

### F03 — Pré-registro OSF do P01 validado
- JSON validado pelo `osf_submit.py --validate`
- Formato OSF v2 + metadados ricos
- Pronto para `--all` (falta `OSF_TOKEN`)
- Fonte: `docs/osf-json/P01-osf.json`

### F04 — 13 notas de leitura estruturadas
- Inclui: Braun & Clarke 2022 (ATR), Diamond 2013 (FE), Miyake 2000, Naschold 2017, Dehaene 2010, Mollick 2024
- Fonte: `00-fundamentos/notas-leitura/`

### F05 — Pipeline de análise R funcional
- `at_pipeline.R` com 6 fases Braun & Clarke
- `piloto-completo.R` já rodou com sucesso
- Fonte: `01-projeto-qualitativo-criancas-ia/analise/`

### F06 — 5 projetos do programa têm protocolo detalhado
- P01 (quali, ATR) ✅ mais maduro
- P02 (ECR 2×4, gamificação) — protocolo ok
- P03 (quase-exp EEG) — protocolo ok
- P04 (transversal SEM) — protocolo ok
- P05 (coorte LGCM) — protocolo ok
- Fonte: `AGENTS.md` raiz

### F07 — Infraestrutura técnica completa
- 159 testes Python + 23 unittest passando
- 12 CI workflows (GitHub Actions)
- Dashboard Streamlit 8 páginas
- 5 pré-registros OSF validados
- Fonte: `.agent/STATE.yaml`

### F08 — Inconsistências entre documentos do P01 (transparência)
- **3 valores diferentes para N**: projeto-detalhado (20-30), manuscrito (3 piloto), OSF (12-15)
- **2 valores para escolaridade**: projeto-detalhado (3º-5º), manuscrito (2º)
- **3 municípios diferentes**: Ipanguaçu, Currais Novos, Natal
- Fonte: relatório §14 (cross-check objetivo)

---

## 💡 HIPÓTESES PROPOSTAS (H01–H04)

> **NÃO verificadas.** Propostas pela IA com base na literatura. Ângela decide se são válidas ou se reformulam.

### H01 — Hipóteses implícitas do manuscrito v1
- Crianças constroem Teoria da Mente de Máquina (MToM) funcional mas em desenvolvimento
- Método socrático do Khanmigo favorece detecção precoce de erro
- Confiança é calibrada por contexto (matemática vs interpretação)
- Crianças distinguem IA de humanos funcionalmente, mas antropomorfizam parcialmente
- Fonte: manuscrito v1 + nota sobre Druga et al. 2017 (não lida ainda)

### H02 — Saturação teórica atingida com 12-15 crianças
- Baseado em Guest et al. 2006 (citado em projeto-detalhado)
- **Premissa:** crianças em idade escolar, tema de pesquisa bem definido
- **Risco:** pode variar (heterogeneidade da amostra)

### H03 — Escola parceira deve ter histórico de pesquisa L+N
- Sugestão: Ipanguaçu ou Currais Novos (parceria Ângela/MEC)
- **Premissa:** confiança pré-existente = mais rápido obter carta de anuência

### H04 — Plataforma Brasil aprova em 1-3 meses se documentação estiver sólida
- Histórico CEP-UFRN
- **Premissa:** checklist completo + TCLE/TALE bem escritos
- **Risco:** pode demorar mais se houver pendências éticas

---

## 🚪 DECISÕES NECESSÁRIAS (D01–D10) — HUMAN GATE

> O que **precisa** da Ângela. Cada D tem opções claras.

### D01 — Aceitar orientação formal do mestrado PPGED?
- **Quem decide:** Ângela
- **Opções:** [Sim / Não / Condicional]
- **Bloqueia:** tudo

### D02 — Aprovar versão final do projeto-detalhado (v1.0)?
- **Quem decide:** Ângela
- **Bloqueia:** submissão CEP
- **Sugestão:** revisar em 7 dias

### D03 — Aprovar versão final do manuscrito (v2.0)?
- **Quem decide:** Ângela
- **Bloqueia:** submissão *Computers & Education*
- **Sugestão:** revisar em 14 dias

### D04 — Indicar escola parceira?
- **Quem decide:** Ângela
- **Opções:**
  - **A. Ipanguaçu** (RN, parceria L+N)
  - **B. Currais Novos** (RN, parceria L+N)
  - **C. Outra** (especificar)
- **Bloqueia:** carta de anuência

### D05 — Apresentar à direção da escola?
- **Quem decide:** Ângela
- **Opções:** [Sim, eu apresento / Eu envio email de apresentação / Eu mesmo apresento]
- **Bloqueia:** carta de anuência

### D06 — Cronograma de reuniões mensais?
- **Quem decide:** Ângela + Pesquisadora
- **Opções:**
  - **A. 1ª terça de cada mês, 14h (Natal) / 15h (Caicó)**
  - **B. 1ª quarta de cada mês**
  - **C. Ajustar para: ___**
- **Não bloqueia:** nada imediato

### D07 — Ordem de co-autoria no manuscrito (CRediT)?
- **Quem decide:** Ângela + Pesquisadora
- **Opções:**
  - **A. Pesquisadora 1º, Ângela último (autor sênior) — POLITICA-AUTORIA.md**
  - **B. Pesquisadora 1º, Ângela 2º (co-autora intermediária)**
  - **C. Outra ordem**
- **Não bloqueia:** nada imediato

### D08 — Submeter P01 ao CEP?
- **Quem decide:** Pesquisadora + Ângela
- **Pré-requisito:** D01 + D02 + D04 + D05
- **Quando:** após todos os pré-requisitos, em ~2 sprints

### D09 — Submeter P01 a *Computers & Education*?
- **Quem decide:** Pesquisadora + Ângela
- **Pré-requisito:** D01 + D03
- **Quando:** após pré-requisitos

### D10 — Submeter 5 pré-registros ao OSF?
- **Quem decide:** Pesquisadora + Ângela
- **Pré-requisito:** D01 + `OSF_TOKEN`
- **Quando:** imediato (1 dia)

---

## ❓ PERGUNTAS PARA ÂNGELA (Q01–Q05)

> O que **não sei** e depende de informação dela.

### Q01 — Qual escola parceira tem perfil + agenda aberta?
- Ipanguaçu? Currais Novos? Outra?
- Alguma restrição de calendário escolar (provas, recessos)?

### Q02 — Você tem disponibilidade mensal recorrente?
- Qual dia/horário prefere?
- Presencial (Natal/Caicó) ou Meet?

### Q03 — Verba institucional para deslocamento Caicó–Natal?
- Se não houver, quais editais posso buscar (FAPERN, CAPES)?

### Q04 — ICe (Prof. Antonio Pereira) — você tem agenda aberta para EEG em 2027?
- Para alinhamento P03 e P05
- Quando você pode fazer a apresentação?

### Q05 — Há outros mestrandos no PPGED fazendo pesquisa similar?
- Possível co-orientação compartilhada?
- Algum cuidado específico do programa?

---

## 🤖 RECOMENDAÇÕES DA IA (R01–R06)

> **NÃO decisões.** Sugestões técnicas da IA. Ângela pode ignorar.

### R01 — Ler 3 papers adicionais antes de submeter
- MToM em crianças (Liu et al. 2023 — citado mas não lido)
- Privacidade infantil + IA (McReynolds et al. 2017)
- Chatbots educacionais + crianças (Maples et al. 2024)
- **Por quê:** fortalecer fundamentação teórica
- **Risco:** atrasar submissão em 1-2 semanas

### R02 — Harmonizar N para 12-15 crianças
- Alinhar com pré-registro OSF
- Justificar com Guest et al. 2006
- **Por quê:** eliminar inconsistência

### R03 — Detalhar protocolo de interrupção e encaminhamento
- CNS 510/2016 exige
- Incluir: sinais de desconforto, procedimento, encaminhamento
- **Por quê:** requisito ético formal

### R04 — Incluir DPO + RIPD simplificado
- LGPD Art. 38 (RIPD obrigatório para pesquisa com crianças)
- DPO da UFRN: identificar responsável
- **Por quê:** compliance LGPD

### R05 — Expandir piloto para 5-7 crianças antes da coleta formal
- Validar saturação inicial
- Testar logística
- **Por quê:** evitar surpresas na coleta formal

### R06 — Criar CHANGELOG-decisions.md
- Consolidar decisões canônicas (N, escolaridade, município)
- Propagar para todos os documentos
- **Por quê:** evitar inconsistências futuras

---

## 📊 Resumo da reunião (template para preencher durante)

### Decisões tomadas

| D | Decisão |
|---|---|
| D01 | [ ] Sim [ ] Não [ ] Condicional: ___ |
| D02 | [ ] Aprovado [ ] Com ajustes [ ] Aguardando |
| D03 | [ ] Aprovado [ ] Com ajustes [ ] Aguardando |
| D04 | [ ] A: Ipanguaçu [ ] B: Currais Novos [ ] C: Outra: ___ |
| D05 | [ ] Você apresenta [ ] Email de apresentação [ ] Eu mesmo |
| D06 | [ ] A: 1ª terça [ ] B: 1ª quarta [ ] C: ___ |
| D07 | [ ] A: Pesquisadora 1º + Ângela último [ ] B: ___ [ ] C: ___ |
| D08 | [ ] Sim [ ] Após ajustes |
| D09 | [ ] Sim [ ] Após ajustes |
| D10 | [ ] Sim [ ] Após OSF_TOKEN |

### Pendências pós-reunião

| # | Ação | Responsável | Prazo |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Próxima reunião

- **Data:** ___/___/______, ___:___
- **Local:** [ ] Natal [ ] Caicó [ ] Meet

---

## 🔗 Material de apoio (já pronto)

| Material | Caminho |
|---|---|
| Email inicial | `docs/email-angela-2026-09-reuniao.md` |
| Briefing pack (2 páginas) | `docs/atas/2026-XX-XX-reuniao-angela-briefing.md` |
| Termo de orientação | `docs/atas/2026-XX-XX-reuniao-angela-autorizacao.md` |
| Agenda + pitch | `docs/atas/2026-XX-XX-reuniao-angela-agenda.md` |
| Ata pré-preenchida | `docs/atas/2026-XX-XX-reuniao-angela-ata.md` |
| Checklist operacional | `docs/CHECKLIST-PRE-REUNIAO-ANGELA.md` |
| Submission readiness (input) | `.agent/reports/submission-readiness-P01-2026-09-19.md` |

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após reunião com Ângela
