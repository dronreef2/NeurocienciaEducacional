# Memory Layer — Log cronológico dos agentes

> **Inspiração:** NEURA — log estruturado de ações, reflexões e artefatos.
> **Versão:** 1.0 — 2026-09-19
> **Convenção:** `AAAA-MM-DD-HHMM-[agente]-[ação].md` ou `.jsonl`

---

## 🎯 O que é

Memory layer é um **log cronológico** de tudo que os agentes fazem, decidem, e produzem. É a "memória institucional" do Research OS.

**Diferente de:**
- `STATE.yaml` — estado atual verificado (snapshot)
- `decisions/` — ADRs imutáveis
- `playbooks/` — procedimentos reutilizáveis
- `reports/` — outputs de ciclos específicos

**Memory é:** o que aconteceu, quando, por que, e o que aprendemos.

---

## 📂 Estrutura

```
.agent/memory/
├── README.md              ← este arquivo
├── schema.md              ← schema dos memory entries
├── index.yaml             ← índice cronológico (auto-gerado)
└── YYYY-MM-DD-*.md        ← entradas individuais
```

---

## 📝 Tipos de memory entries

### Type 1: Action log (ação executada)
**Quando:** após cada ação significativa do agente.
**Exemplo:** submeter pré-registro, gerar relatório, criar teste.

### Type 2: Reflection (reflexão sobre ciclo)
**Quando:** após cada integration test / ciclo completo.
**Exemplo:** o que funcionou, o que não funcionou, próximos improvements.

### Type 3: Decision log (decisão operacional)
**Quando:** após decisão operacional (vs arquitetural em decisions/).
**Exemplo:** "escolhi X ao invés de Y porque Z".

### Type 4: Learning (aprendizado)
**Quando:** após insight novo ou erro corrigido.
**Exemplo:** "descobri que PATH relativo é necessário para Streamlit Cloud".

### Type 5: Failure log (falha registrada)
**Quando:** após falha + correção.
**Exemplo:** "test falhou por causa de Y, corrigido trocando Z".

---

## 📋 Schema (Markdown)

```markdown
# Memory Entry — [título curto]

**Tipo:** [action|reflection|decision|learning|failure]
**Data:** AAAA-MM-DD HH:MM
**Agente:** [Conductor|ResearchAgent|MethodologyAgent|...]
**Ciclo:** [qual integration test ou fase]
**Tags:** [#P01 #CEP #LGPD #pytest]

## Contexto
[Por que essa ação? O que estava acontecendo?]

## Ação
[O que foi feito]

## Inputs
- [arquivo 1]
- [arquivo 2]

## Outputs
- [arquivo 3] (criado/modificado)
- [arquivo 4]

## Validação
- [✓] Check 1
- [✓] Check 2

## Aprendizado (opcional)
[O que aprendemos que pode ser útil no futuro]

## Referências
- [link interno]
- [paper]
```

---

## 📋 Schema alternativo (JSONL)

Para parsing automático, cada linha de `.jsonl`:

```json
{"timestamp": "2026-09-19T15:30:00", "type": "action", "agent": "Conductor", "action": "submission-readiness-P01", "inputs": ["projeto-detalhado.md", "instrumentos/*.md"], "outputs": [".agent/reports/submission-readiness-P01-2026-09-19.md"], "validations": ["16 sections generated", "F/H/D/Q/R separated"], "tags": ["#P01", "#CEP", "#first-cycle"]}
```

---

## 🎯 Como o agente usa

### Ao iniciar
```bash
# Ler últimas N entries para contexto
tail -10 .agent/memory/2026-09-*.md

# Ou usar índice
cat .agent/memory/index.yaml
```

### Durante
```bash
# Após cada ação significativa
echo "nova entrada" >> .agent/memory/2026-09-19-1430-conductor-submission-readiness.md
```

### Ao terminar ciclo
```bash
# Criar reflection
echo "# Reflection — primeiro integration test" >> .agent/memory/2026-09-19-reflection-cycle-1.md
```

---

## ⚠️ LGPD

- **NÃO** versionar memory entries com PII (nomes reais de crianças, endereços)
- **Anonimizar** antes de escrever
- **Se necessário**, manter memory em pasta separada (não versionada)

---

## 🔗 Links

- `.agent/memory/` (esta pasta)
- `.agent/STATE.yaml` (estado verificado)
- `.agent/decisions/` (ADRs)
- `.agent/reports/` (outputs de ciclos)
- `AGENTS.md` (Conductor)

---

**Última atualização:** 2026-09-19
