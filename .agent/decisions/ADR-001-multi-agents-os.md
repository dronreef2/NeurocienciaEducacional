# ADR-001 — Sistema multi-AGENTS como Research Operating System

> **Primeira decisão arquitetural** do programa.
> **Data:** 2026-09-19
> **Status:** ACCEPTED
> **Decisor:** Conjunto (humano + IA)

---

## Metadata

| Campo | Valor |
|---|---|
| **ADR #** | 001 |
| **Título** | Sistema multi-AGENTS como Research Operating System |
| **Data** | 2026-09-19 |
| **Status** | ACCEPTED |
| **Decisor** | Conjunto (humano propôs, IA implementou) |
| **Domínio** | Cross (Research + Engineering + Project-Mgmt) |

---

## Contexto

O Programa de Pesquisa em Neurociência Educacional (5 projetos, 60 meses, parceria com UFRN) precisa de:

1. **Contexto para IAs** que auxiliam no desenvolvimento (Cursor, Claude Code, Copilot)
2. **Reprodutibilidade** de decisões (por que fizemos X e não Y)
3. **Separação clara** entre o que é pesquisa, engenharia, e gestão
4. **HUMAN GATE** explícito para decisões científicas críticas
5. **Operacionalização** (não apenas documentação passiva)

O padrão `AGENTS.md` (reconhecido por múltiplos assistentes de IA) oferece um caminho, mas apenas como **documentação** — não como **sistema operacional**.

---

## Problema

**Pergunta:** Como evoluir o `AGENTS.md` (documentação estática) para um **sistema operacional** que:
- Engata automaticamente skills por domínio
- Mantém estado verificado do projeto
- Registra decisões arquiteturais (ADR)
- Tem playbooks para cenários recorrentes
- Força HUMAN GATE em decisões críticas

---

## Opções consideradas

### Opção A — Apenas AGENTS.md raiz + sub-AGENTS.md (status quo até 2026-09-19)

**Descrição:** Manter o padrão AGENTS.md hierárquico simples (raiz + por projeto + por área).

**Prós:**
- Simples de manter
- Reconhecido por todos os assistentes
- Baixo overhead

**Contras:**
- Sem estado verificado (só docs)
- Sem decisões registradas
- Sem playbooks
- Sem enforcement de HUMAN GATE
- Sem separação rigorosa de papéis

**Custos:** Baixo (já está em produção)

---

### Opção B — Sistema multi-AGENTS como Research OS (escolhida)

**Descrição:** Evoluir para sistema operacional com `.agent/` directory:
- `STATE.yaml` (estado verificado)
- `MISSION.md` (missão)
- `decisions/` (ADRs)
- `playbooks/` (procedimentos)
- `reports/` (outputs)
- `templates/` (formatos)
- 3 AGENTS.md de domínio (research/engineering/project-management)

**Prós:**
- Operacional (não só docs)
- Estado verificado (não inferido)
- Decisões rastreáveis (ADRs)
- Procedimentos padronizados (playbooks)
- HUMAN GATE explícito
- Separação rigorosa de papéis

**Contras:**
- Mais arquivos para manter (~15-20 novos)
- Overhead inicial maior
- Curva de aprendizado

**Custos:** Médio (1-2 sprints para criar estrutura + playbooks prioritários)

---

### Opção C — Sistema ainda mais elaborado (com ML, observability, CI específico para ADRs)

**Descrição:** Adicionar tools de validação automática, métricas de uso, etc.

**Prós:**
- Máxima automação
- Métricas de uso dos playbooks

**Contras:**
- Complexidade excessiva para programa de pesquisa (YAGNI)
- Custo de manutenção alto

**Custos:** Alto (não justificado agora)

---

## Decisão

**Opção escolhida:** **B**

**Justificativa:**
- Programa é pesquisa científica (não engenharia de software puro)
- Decisões precisam ser rastreáveis por 5+ anos (mestrado + doutorado)
- LGPD + crianças + EEG exigem HUMAN GATE explícito
- Custo médio é absorvível (já investimos em CI/CD, dashboard, etc.)

---

## Quem decidiu

- ✅ **Humano:** Pesquisadora responsável (proposta original do design)
- ✅ **IA:** Mavis (root session) implementou a estrutura técnica
- ✅ **Conjunto:** Decisão aprovada por ambos

**Data da decisão:** 2026-09-19

---

## Consequências

### Positivas
- IAs têm contexto rico e atualizado (STATE.yaml)
- Decisões ficam registradas para futuro (ADRs)
- Procedimentos padronizados (playbooks) reduzem erros
- HUMAN GATE explícito protege contra decisões IA indevidas
- Separação de papéis facilita auditoria (LGPD)

### Negativas
- Mais arquivos para manter (~15-20 novos no `.agent/`)
- Overhead inicial (criar playbooks para cada cenário)
- Pode ser excessivo para projetos pequenos (não é nosso caso)

### Neutras (side-effects)
- Convenções YAML + Markdown para todas as decisões
- Cada playbook tem versão (evolução rastreável)

---

## Riscos residuais

| Risco | Prob. | Mitigação |
|---|---|---|
| `.agent/` não ser mantido atualizado | Média | STATE.yaml atualizado por hook pós-commit |
| Playbooks ficarem desatualizados | Média | Revisão trimestral |
| IA ignorar HUMAN GATE | Baixa | Checklist de validação obrigatório antes de "pronto" |
| Sobrecarga cognitiva (15+ arquivos novos) | Baixa | Documentação clara + mapa visual |

---

## Estrutura criada

```
.agent/
├── STATE.yaml               # estado verificado
├── MISSION.md               # missão do programa
├── ROADMAP.md               # (a criar) evolução
├── decisions/
│   ├── ADR-template.md      # template para futuras ADRs
│   └── ADR-001-multi-agents-os.md  # esta decisão
├── playbooks/
│   ├── submeter-p01.md      # submissão P01 (CEP/OSF/journal)
│   ├── reuniao-angela.md    # reunião com Ângela
│   └── bug-dashboard.md     # bug no Streamlit
├── reports/                 # (a criar) outputs dos agentes
└── templates/               # (a criar) formatos padronizados

research/AGENTS.md           # AGENTS do domínio Research
engineering/AGENTS.md        # AGENTS do domínio Engineering
project-management/AGENTS.md # AGENTS do domínio Project-Mgmt

AGENTS.md                    # CONDUCTOR (reescrito, raiz)
```

---

## Referências

- Padrão AGENTS.md (https://agents.md/)
- CRediT (Contributor Roles Taxonomy, NISO)
- LGPD Art. 7º, IV
- OSF Best Practices for Preregistration
- YAGNI principle (You Aren't Gonna Need It)

---

## Notas de revisão

| Data | Quem | O que mudou |
|---|---|---|
| 2026-09-19 | Pesquisadora + Mavis | ADR criado e accepted |
