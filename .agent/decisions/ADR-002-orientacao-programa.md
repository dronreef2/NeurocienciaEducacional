# ADR-002 — D01: Orientação Formal da Ângela como Dependência Crítica

> **Status:** ACCEPTED (proposta)
> **Data:** 2026-09-19
> **Decisor:** Conjunto (humano propôs, IA formalizou)
> **Domínio:** Cross (Research + Engineering + Project-Mgmt)

---

## Metadata

| Campo | Valor |
|---|---|
| ADR # | 002 |
| Título | D01 — Orientação formal como dependência crítica do programa |
| Data | 2026-09-19 |
| Status | ACCEPTED (proposta) |
| Decisor | Conjunto (proposto pela pesquisadora, formalizado pela IA) |
| Domínio | Cross |

---

## Contexto

Cycle 2 do Research OS (program-maturity-2026-09-19.md) identificou que **3 dos 5 projetos** dependem de uma única decisão humana: a aceitação formal da Ângela como orientadora do mestrado PPGED.

Esta dependência estava mencionada em **vários documentos** (kit de reunião, briefing, reports) mas **nunca foi formalizada** como uma dependência crítica explícita do sistema.

O risco de não formalizar:
- Agente pode propor ações que assumem "Ângela aceita" sem ter verificado
- Estado do sistema pode divergir do estado real
- Decisões críticas podem ser tomadas sem considerar esta dependência

---

## Problema

Como representar **explicitamente** uma decisão humana crítica como dependência formal do Research OS?

**Requisitos:**
- Visível para agentes
- Atualizável com mudança de status
- Bloqueia ações de alto impacto (submissões)
- Não automatizável (HUMAN GATE obrigatório)

---

## Opções consideradas

### Opção A — Só no STATE.yaml (implementado)
**Descrição:** bloco `critical_dependencies` no STATE.yaml com campos estruturados.

**Prós:**
- Local central e verificado
- Lê junto com outras métricas
- Estrutura consistente com resto do STATE

**Contras:**
- Sem histórico de mudanças
- Sem justificativa formal
- Sem consequências detalhadas

### Opção B — Só em ADR próprio
**Descrição:** ADR-002 contém toda a info, STATE.yaml só referencia.

**Prós:**
- Histórico e justificativa formal
- Cross-referenced com decisão-original

**Contras:**
- Mais disperso (procure em 2 lugares)

### Opção C — Híbrido (escolhida)
**Descrição:** STATE.yaml tem o status atual + pointer. ADR-002 contém história + justificativa + consequências detalhadas.

**Prós:**
- Status rápido via STATE.yaml (curl/cat)
- História completa via ADR (legado)
- Separação de concerns

**Contras:**
- Manter coerência entre os dois (Risco: drift)

---

## Decisão

**Opção escolhida: C (híbrido)**

Justificativa: o STATE.yaml é o **snapshot atual** (verificado, lido frequentemente). O ADR é o **legado** (histórico, lido quando há dúvida). Separar evita que o STATE vire um documento gigante.

---

## Implementação

### STATE.yaml (status atual)

```yaml
critical_dependencies:
  D01:
    description: "Orientação formal da Ângela no mestrado PPGED"
    owner: "Ângela Maria Chuvas Naschold"
    status: pending_human_decision
    blocks:
      - P01_submission_CEP
      - P03_acesso_ICe
      - confidence_program
    affects:
      - funding_opportunities
      - academic_supervision
      - institutional_access_ICe
```

### ADR-002 (este documento)

- Contexto + problema + opções + decisão (acima)
- Quem decidiu (abaixo)
- Consequências + monitoramento

---

## Quem decidiu

- ✅ **Humano:** Pesquisadora propôs "D01 é gargalo do programa"
- ✅ **IA:** Conductor (Mavis) formalizou em critical_dependencies + ADR
- ✅ **Conjunto:** Aceito em 2026-09-19 via Cycle 2

---

## Consequências

### Positivas

- D01 visível em qualquer inspeção do STATE.yaml
- Agente pode checar `critical_dependencies.D01.status` antes de propor submissões
- Próximo cycle pode adicionar D02, D03, ... conforme necessário

### Negativas

- Mais um bloco para manter em sync entre STATE e ADR
- Risco de drift (status atualizado em um lugar mas não outro)

### Mitigação do drift

- Toda atualização do STATE deve referenciar o ADR (`decision_record:`)
- CI pode checar que todo critical_dependency tem `decision_record` válido (futuro)

---

## Monitoramento

```bash
# Como checar D01:
grep -A 10 "D01:" .agent/STATE.yaml

# Como atualizar:
# 1. Mudar status em STATE.yaml
# 2. Adicionar entry em .agent/memory/AAAA-MM-DD-D01-update.md
# 3. Se mudança estrutural, atualizar este ADR
```

---

## Como resolver D01

Playbook: `.agent/playbooks/reuniao-angela.md`

Outputs esperados:
- Reunião realizada
- Ângela aceita/nega/condicional
- `state.critical_dependencies.D01.status` → `accepted` / `rejected` / `conditional`
- Plano de próximos passos atualizado

---

## Referências

- `.agent/reports/program-maturity-2026-09-19.md` (Cycle 2)
- `docs/atas/2026-XX-XX-reuniao-angela-briefing.md`
- `docs/email-angela-2026-09-reuniao.md`
- `AGENTS.md` (HUMAN GATE rule)

---

## Histórico de revisões

| Data | Quem | O que mudou |
|---|---|---|
| 2026-09-19 | Pesquisadora + Mavis | ADR criado e aceito (proposta) |
