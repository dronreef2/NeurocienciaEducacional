# Memory Entry — 3 domínios vs 7 especializados

**Tipo:** decision
**Data:** 2026-09-19 15:35
**Agente:** Conductor (Mavis)
**Ciclo:** Após reflexão do Cycle 1
**Tags:** #architecture #decision #agents #NEURA-inspired

---

## Contexto

Após o primeiro integration test, o usuário propôs evolução: adicionar 7 agentes especializados (ResearchAgent, MethodologyAgent, CodingAgent, DataAgent, StatisticsAgent, LiteratureAgent, ReviewAgent) em vez de 3 domínios genéricos (research/, engineering/, project-management/).

**Argumento do usuário:**
> "Isso muda completamente o comportamento do agente. Em vez de 'implemente o projeto', o agente faria: 'descubra o estado → diagnostique → roadmap → implemente → teste → valide → documente → novo estado'."

---

## Decisão

**Optei por:** arquitetura híbrida com **3 domínios genéricos** + **4 agentes especializados adicionais**.

### Por quê não 7 especializados puros?

- O custo de manter 7 AGENTS.md separados é alto
- Muitos domínios se sobrepõem (Coding ⊂ Engineering, Data ⊂ Engineering/Research)
- O Orchestrator precisa entender todos — mais complexidade

### Por quê não 3 genéricos puros?

- MethodologyAgent, LiteratureAgent, StatisticsAgent, ReviewAgent têm **competências genuinamente diferentes**
- São invocados em momentos diferentes do ciclo
- Tê-los como sub-agentes formalizados facilita o roteamento

### Arquitetura híbrida adotada

**3 domínios genéricos (continuam):**
- `research/AGENTS.md` — Research Agent (alto nível)
- `engineering/AGENTS.md` — Engineering Agent (alto nível)
- `project-management/AGENTS.md` — Project Management Agent

**4 especializados (novos):**
- `methodology/AGENTS.md` — desenho de pesquisa
- `literature/AGENTS.md` — busca/síntese de papers
- `statistics/AGENTS.md` — análise estatística
- `review/AGENTS.md` — auditoria de qualidade

**Orchestrator:** Conductor (já existe)

---

## Consequências

### Positivas
- Cada agente tem escopo claro
- Roteamento mais preciso (ex: "literature review" → LiteratureAgent)
- Mantém compatibilidade com sistema atual (não quebra nada)
- Adiciona valor sem destruir o que já funciona

### Negativas
- Mais arquivos para manter (7 vs 3)
- Roteamento precisa ser explícito (qual agente para qual tarefa)
- Pode haver sobreposição (ResearchAgent vs MethodologyAgent)

### Mitigação
- AGENTS.md raiz (Conductor) tem matriz de roteamento clara
- Cada agente especializado lista quando é acionado
- Cross-references entre agentes para evitar duplicação

---

## Quem decidiu

- ✅ Humano: Pesquisadora (proposta)
- ✅ IA: Conductor (Mavis) implementou
- ✅ Conjunto: 4 agentes especializados adicionados

---

## Status

ACCEPTED

---

## Próximos passos

1. Atualizar STATE.yaml com maturity field por projeto (N0-N5)
2. Criar `.agent/maturity-model.md` (modelo de 5 níveis)
3. Criar memory layer (esta pasta)
4. Rodar novo integration test: DISCOVERY → DIAGNOSE → NEXT_STATE para todos os 5 projetos
