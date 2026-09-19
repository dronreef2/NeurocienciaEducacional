# Program Maturity Matrix — Programa de Pesquisa Completo

> **Executado pelo ciclo:** Discovery → Diagnóstico → Next State
> **Data:** 2026-09-19
> **Versão:** 1.0 (2º integration test do Research OS)
> **Modelo:** `.agent/maturity-model.md` (5 níveis: N0 → N5)
> **Fonte primária:** filesystem + STATE.yaml (dados verificados)

---

## 🎯 Objetivo

Aplicar o ciclo **Discovery → Diagnóstico → Next Verifiable State** ao **programa inteiro** (5 projetos), identificando:

1. Maturidade atual de cada projeto (N0–N5)
2. Gaps prioritários por projeto
3. Gargalo real do programa
4. Próximo estado verificável por projeto
5. Como chegar lá (responsável + prazo)

---

## 📊 Sumário executivo

| Projeto | Maturidade atual | Target | Gap crítico | Bloqueado por |
|---|---|---|---|---|
| **P01** (quali IA) | **N1** (transição N2) | N2 | Carta anuência + Lattes + revisão Ângela | D01-D05 (reunião Ângela) |
| **P02** (ECR gamif) | **N1** (parado) | N2 | Sem trigger para avançar | Funding (FAPERN Q2/2026) |
| **P03** (EEG tela/papel) | **N1** (parado) | N2 | Acordo ICe + instrumentos | Contato Prof. Pereira (via Ângela) |
| **P04** (SEM) | **N1** (sequencial) | N1 (manter) | Nenhum (esperando P01-P03) | Sequencing (2028+) |
| **P05** (coorte LGCM) | **N1** (parado) | N1 (manter) | Sem trigger para avançar | Funding + parcerias |

### 🚦 Gargalo real do programa

> **P01** é o gargalo real, porque está mais avançado e bloqueado pela mesma dependência (D01: reunião com Ângela). Uma vez que a Ângela aceita a orientação e libera P01, **3 dos 5 projetos desbloqueiam**:
>
> - **P02:** pode submeter FAPERN (D01 desbloqueia confiança do programa)
> - **P03:** Ângela apresenta ao Prof. Pereira (D05)
> - **P04 e P05:** sequencial, mas ganham momentum institucional

---

## 🔍 DISCOVERY (estado verificado)

### Inventário físico (2026-09-19)

| Recurso | Quantidade | Localização |
|---|---|---|
| Documentos markdown | ~28k linhas | Todo o repo |
| Arquivos Python | ~150 | `analise/Python/` |
| Testes Python | 182 | `analise/Python/tests/` |
| Workflows CI | 12 | `.github/workflows/` |
| Páginas Streamlit | 8 | `pages/` |
| Pré-registros OSF | 5 | `docs/osf-json/` |
| Datasets sintéticos | 6 | `dados_sinteticos/` |
| Notas de leitura | 23 | `00-fundamentos/notas-leitura/` |
| Manuscritos (rascunhos) | 7 | `docs/manuscritos/` |
| Figuras (300dpi) | 20+ | `resultados/` |
| Total de commits | 95+ | git log |

---

## 📊 DIAGNÓSTICO por projeto

### 🔬 P01 — Vozes das crianças sobre tutores de IA

**Maturidade atual:** **N1_PROTOCOL** (transição para N2_ETHICS_APPROVED)
**Target:** N2_ETHICS_APPROVED

**O que está pronto (N1):**
- ✅ Protocolo detalhado (269 linhas, 21k chars)
- ✅ 7 instrumentos completos (entrevista, think-aloud, diário, questionários, TCLE, TALE)
- ✅ Manuscrito v1 (rascunho, 5 temas identificados)
- ✅ Pré-registro OSF validado
- ✅ Carta de anuência (template)
- ✅ Termo de compromisso CNS 466/2012
- ✅ Checklist CEP + checklist Plataforma Brasil
- ✅ Piloto com 3 crianças (Maria, Pedro, Júlia)
- ✅ Pipeline de análise R funcional (AT 6 fases)
- ✅ Recrutamento i18n (PT/EN/ES)

**O que falta (N1 → N2):**
- ❌ Carta de anuência da escola **assinada** (template pronto, falta escola)
- ❌ Lattes + ORCID atualizados
- ❌ **Revisão da Ângela** (D02 — projeto-detalhado, D03 — manuscrito)
- ❌ Submissão ao CEP/UFRN
- ❌ Submissão OSF (com `OSF_TOKEN`)
- ❌ Submissão a *Computers & Education*

**Inconsistências detectadas (cross-check):**
- N de participantes: 20-30 (projeto) / 3 (manuscrito) / 12-15 (OSF)
- Escolaridade: 3º-5º (projeto) / 2º (manuscrito)
- Município: Ipanguaçu/Currais Novos (projeto) / Natal (manuscrito)

**Bloqueado por:** D01-D10 (10 decisões humanas — todas requerem reunião com Ângela)

**Próximo estado verificável (P01 → N2):**
- [ ] Carta de anuência da escola parceira **obtida** (data: __/___/____)
- [ ] Lattes + ORCID atualizados (data: hoje)
- [ ] Reunião com Ângela **realizada** (data: __/___/____)
- [ ] Submissão CEP **aceita na Plataforma Brasil** (CAAE obtido)
- [ ] Parecer CEP **aprovado** (estimativa: 1-3 meses após submissão)

---

### 🎮 P02 — Gamificação e FE (ECR 2×4)

**Maturidade atual:** **N1_PROTOCOL**
**Target:** N2_ETHICS_APPROVED (após funding)

**O que está pronto (N1):**
- ✅ Projeto detalhado (protocolo completo)
- ✅ Dados sintéticos (200 crianças, ECR 2×4, 4 grupos)
- ✅ Pré-registro OSF validado
- ✅ Análise estatística: ANCOVA + mediação (Hayes PROCESS)
- ✅ Hipóteses pré-registradas (H2.1-H2.4)

**⚠️ Duplicação detectada:**
- Duas pastas: `02-projeto-gamificacao-autorregulacao/` e `02-projeto-gamificacao-funcoes-executivas/`
- Verificar qual é a canônica (provavelmente a 2ª — alinhada com programa atual)

**O que falta (N1 → N2):**
- ❌ Instrumentos específicos (Stroop, TMT-B, Digit Span — não há versões P02)
- ❌ TCLE + TALE (se envolver crianças diretamente)
- ❌ Submissão FAPERN Demanda Espontânea (R$ 30k, Q2/2026)
- ❌ Submissão CEP (após funding)

**Bloqueado por:** funding + falta de instrumentos específicos

**Próximo estado verificável (P02 → N2):**
- [ ] Submissão FAPERN **aceita** (ou edit.alternativo)
- [ ] Instrumentos (Stroop/TMT-B/Digit Span) **adaptados** para 3º-5º ano
- [ ] TCLE + TALE elaborados
- [ ] Submissão CEP **realizada**

---

### 🧠 P03 — EEG leitura tela vs papel

**Maturidade atual:** **N1_PROTOCOL**
**Target:** N2_ETHICS_APPROVED (após acordo ICe)

**O que está pronto (N1):**
- ✅ Projeto detalhado
- ✅ Dados sintéticos EEG (30 sujeitos × 32 canais × 500 amostras — papel + tela)
- ✅ Pré-registro OSF validado (rich metadata)
- ✅ Análise: ANOVA mista + cluster permutation + time-frequency
- ✅ Componentes ERP definidos (N170, P200, P300, N400, P600)
- ✅ Pipeline EEG (`neurociencia_edu/eeg/`)

**⚠️ Duplicação detectada:**
- Duas pastas: `03-projeto-eeg-leitura/` e `03-projeto-eeg-leitura-digital/`
- Verificar qual é a canônica (provavelmente a 2ª)

**O que falta (N1 → N2):**
- ❌ Acordo com ICe (Prof. Antonio Pereira) — D04 via Ângela
- ❌ Instrumentos (tarefa de leitura controlada, teste compreensão, eye-tracker)
- ❌ TCLE + TALE (pais + criança para EEG)
- ❌ Submissão CEP

**Bloqueado por:** contato ICe (D04, depende de Ângela)

**Próximo estado verificável (P03 → N2):**
- [ ] Reunião com Prof. Pereira **agendada** (via Ângela)
- [ ] Acordo ICe **formalizado** (termo de uso do EEG)
- [ ] Instrumentos EEG **adaptados** para 8-12 anos
- [ ] TCLE + TALE específicos para EEG elaborados
- [ ] Submissão CEP **realizada**

---

### 📈 P04 — IA generativa × FE (SEM transversal)

**Maturidade atual:** **N1_PROTOCOL**
**Target:** N1 (manter — sequencial após P01-P03)

**O que está pronto (N1):**
- ✅ Projeto detalhado
- ✅ Dados sintéticos SEM (400 crianças)
- ✅ Pré-registro OSF validado
- ✅ Modelo conceitual (mediação + moderação)
- ✅ Análise SEM (lavaan, R)
- ✅ Hipóteses pré-registradas (H4.1-H4.5)

**O que falta:**
- ⏳ Aguardar P01-P03 (sequencial, target 2028)
- Instrumentos quando chegar a hora

**Bloqueado por:** sequencing (não precisa de ação agora)

**Próximo estado verificável (P04 → N2):** 2028+

---

### 📅 P05 — Coorte longitudinal EEG

**Maturidade atual:** **N1_PROTOCOL**
**Target:** N1 (manter — sequencial)

**O que está pronto (N1):**
- ✅ Projeto detalhado
- ✅ Dados sintéticos longitudinais (200 crianças × 5 ondas = 1000 obs)
- ✅ Pré-registro OSF validado
- ✅ Análise LGCM + cross-lagged + Kaplan-Meier

**O que falta:**
- ⏳ Aguardar funding (R$ 200k CNPq Universal) + parcerias
- Coorte é **long-term commitment** (5 anos) — não iniciar sem garantias

**Bloqueado por:** funding + parcerias (não pode iniciar sem)

**Próximo estado verificável (P05 → N2):** quando funding garantido

---

## 🚦 ROADMAP — Próximo estado verificável por projeto

### P01 (mais maduro)

**Próximo gate:** N2_ETHICS_APPROVED

**Ações necessárias (próximos 30 dias):**
| # | Ação | Quem | Prazo |
|---|---|---|---|
| 1 | Atualizar Lattes + ORCID | Pesquisadora | 2026-09-25 |
| 2 | Enviar email para Ângela | Pesquisadora | 2026-09-20 |
| 3 | Marcar data da reunião | Pesquisadora | 2026-09-22 |
| 4 | Realizar reunião (D01-D10) | Pesquisadora + Ângela | 2026-09-XX |
| 5 | Harmonizar N para 12-15 (R02) | Pesquisadora | Imediato |
| 6 | Criar CHANGELOG-decisions.md (R06) | IA + Pesquisadora | Imediato |
| 7 | Indicar e contatar escola parceira (D04) | Ângela | 2026-09-30 |
| 8 | Obter carta de anuência | Direção da escola | 2026-10-15 |
| 9 | Submeter ao CEP | Pesquisadora | 2026-10-15 |
| 10 | Submeter a *Computers & Education* | Pesquisadora | 2026-10-01 |
| 11 | Submeter 5 OSF | Pesquisadora | 2026-09-25 |

**Quando vira N2:** parecer CEP aprovado (estimativa 1-3 meses após submissão).

---

### P02 (parado)

**Próximo gate:** N2_ETHICS_APPROVED

**Ações necessárias (próximos 90 dias):**
| # | Ação | Quem | Prazo |
|---|---|---|---|
| 1 | Resolver duplicação de pastas | Pesquisadora | 2026-09-25 |
| 2 | Elaborar instrumentos (Stroop/TMT-B/Digit Span) | Pesquisadora | 2026-10-30 |
| 3 | Elaborar TCLE + TALE | Pesquisadora | 2026-11-15 |
| 4 | Submeter FAPERN Demanda Espontânea | Pesquisadora | 2026-10-15 |
| 5 | Aguardar resultado FAPERN | FAPERN | 2026-12-15 |
| 6 | Se aprovado: submeter CEP | Pesquisadora | 2027-01-15 |

**Quando vira N2:** parecer CEP aprovado (depende de funding FAPERN).

---

### P03 (parado por dependência ICe)

**Próximo gate:** N2_ETHICS_APPROVED

**Ações necessárias (próximos 60 dias):**
| # | Ação | Quem | Prazo |
|---|---|---|---|
| 1 | Resolver duplicação de pastas | Pesquisadora | 2026-09-25 |
| 2 | Ângela apresentar ao Prof. Pereira (D05) | Ângela | 2026-09-30 |
| 3 | Reunião com Prof. Pereira | Pesquisadora + Pereira | 2026-10-15 |
| 4 | Acordo ICe formalizado | ICe | 2026-11-30 |
| 5 | Elaborar instrumentos EEG | Pesquisadora | 2026-12-15 |
| 6 | Elaborar TCLE + TALE específicos para EEG | Pesquisadora | 2027-01-15 |
| 7 | Submeter CEP | Pesquisadora | 2027-02-01 |

**Quando vira N2:** parecer CEP aprovado (Q1/2027 se tudo correr ok).

---

### P04 (sequencial — não fazer agora)

**Próximo gate:** N2 (2028+)

**Status atual:** aguardar P01-P03.

---

### P05 (sequencial — não fazer agora)

**Próximo gate:** N2 (quando funding garantido)

**Status atual:** aguardar funding + parcerias.

---

## 🚨 Gargalo real do programa

```
                ┌─────────────────────────────────┐
                │   D01 — Ângela aceitar          │
                │   orientação formal            │
                │   do mestrado PPGED            │
                └────────────┬────────────────────┘
                             │
                             ▼
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   P01 desbloqueia    P03 desbloqueia    Confiança do programa
   (CEP, journal)     (acordo ICe)       (FAPERN, CNPq)
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                  Momentum institucional
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
       P02                  P04                  P05
    (submeter             (2028+)            (sequencial)
     FAPERN)
```

**Conclusão:** resolver D01 (reunião Ângela) é o **gargalo real** do programa inteiro. Sem Ângela aceitando, **nada** avança de N1 para N2.

---

## 📋 Recomendações da IA (R01-R06 atualizadas)

### R01 — Resolver duplicação de pastas (P02, P03)
- Decidir qual pasta é canônica
- Consolidar (mover conteúdo + remover duplicata)
- Atualizar AGENTS.md raiz e STATE.yaml

### R02 — Criar CHANGELOG-decisions.md
- Lista consolidada de decisões canônicas
- N, escolaridade, município, plataformas (Khanmigo), etc.
- Cross-referenced por todos os documentos

### R03 — Submeter 5 pré-registros ao OSF (imediato)
- Requer `OSF_TOKEN`
- Após D01 (autorização Ângela)
- Comando: `python3 osf_submit.py --all`

### R04 — Lattes + ORCID (esta semana)
- Atualizar antes da reunião com Ângela
- Necessário para D02 (submissão CEP)

### R05 — Lançar memory layer
- Cada ação significativa = entrada em `.agent/memory/`
- Permitirá retrospectiva de 5 anos

### R06 — Adicionar CI workflow para validar STATE.yaml schema
- Bloquear merge se STATE.yaml inválido
- Previne drift

---

## 🎯 Conclusão do Conductor

**O sistema funciona.** O ciclo Discovery → Diagnóstico → Next State identificou:

1. **P01 está pronto para D02-D05** (bloqueado por reunião Ângela)
2. **P02-P03 estão parados em N1** (por funding e dependência, respectivamente)
3. **P04-P05 estão sequenciais** (corretamente esperando)
4. **Gargalo real:** D01 (reunião Ângela)

**Não adicionar complexidade.** O sistema atual já detecta:
- Maturidade por projeto
- Bloqueios reais
- Próximas ações verificáveis
- Recomendações técnicas vs decisões humanas

**Próximo integration test:** executar playbook `reuniao-angela` (após ela aceitar a reunião).

---

## 🔗 Outputs deste ciclo

- Este relatório: `.agent/reports/program-maturity-2026-09-19.md`
- STATE.yaml atualizado com maturity field
- `.agent/maturity-model.md` (definição dos 5 níveis)
- `.agent/memory/2026-09-19-reflection-cycle-2.md` (a criar)

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após reunião com Ângela (atualizar D01-D10 e maturity)
