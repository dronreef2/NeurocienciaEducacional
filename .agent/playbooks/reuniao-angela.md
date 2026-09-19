# 📋 Playbook: reuniao-angela

> **Trigger:** "Preparar reunião com Ângela" / "Reunião sobre P0X"
> **Domínio:** Conductor + Research + Project-Mgmt
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Gerar pasta `meeting/AAAA-MM-DD-angela-P0X/` com 6 artefatos, separando rigorosamente:

- **FATOS** (verificados)
- **HIPÓTESES** (propostas, não verificadas)
- **DECISÕES PENDENTES** (precisam de humano)
- **PERGUNTAS** (o que não sei)
- **RECOMENDAÇÕES TÉCNICAS** (da IA, não da Ângela)

**REGRA:** Misturar esses 5 = reunião confusa. Separar = reunião produtiva.

---

## 🔄 Fluxo (6 passos)

### 1. CONDUCTOR — Identificar escopo da reunião

```bash
Perguntar ao usuário (se ambíguo):
- Qual projeto? (P01, P02, ...)
- Qual decisão crítica? (orientação, submissão, recurso, etc.)
- Qual o prazo? (urgente vs. planejamento)
```

**Output:** escopo claro.

---

### 2. CONDUCTOR — Coletar fatos

**Fontes:**
- `.agent/STATE.yaml` (status verificado)
- `0X-.../AGENTS.md` (status do projeto)
- Git log (commits recentes)
- Documentos do projeto (protocolo, manuscrito, etc.)

**Output:** `meeting/AAAA-MM-DD-angela-P0X/context.md`

```markdown
# Context — Reunião com Ângela sobre P0X

## FATOS (verificados)
- [Fato 1 com fonte]
- [Fato 2 com fonte]
- ...

## Cronograma
- [Marco A em data B]

## Pessoas envolvidas
- [Pesquisadora]: [papel]
- [Ângela]: [papel]
- [Outros]: [papel]
```

---

### 3. RESEARCH — Estado da arte do P0X

**Output:** `meeting/AAAA-MM-DD-angela-P0X/current-state.md`

```markdown
# Current State — P0X

## HIPÓTESES (propostas pela literatura)
- H1: ... (fonte: paper X)
- H2: ... (fonte: paper Y)
- ...

## Lacunas identificadas
- [Lacuna 1]
- [Lacuna 2]

## Status do protocolo
- Versão: vN
- Última atualização: AAAA-MM-DD
- Pendências: [...]

## Status do manuscrito (se houver)
- Versão: vN
- Palavras: N
- Pendências: [...]
```

---

### 4. PROJECT-MGMT — Decisões pendentes

**Output:** `meeting/AAAA-MM-DD-angela-P0X/decisions-needed.md`

```markdown
# Decisions Needed — P0X

## DECISÕES PENDENTES (precisam Ângela)
1. **Aceitar orientação formal do mestrado** — opções: [Sim / Não / Condicional]
2. **Autorizar submissão P0X ao CEP** — opções: [Sim / Não / Após ajustes]
3. **Indicar escola parceira** — opções: [Ipanguaçu / Currais Novos / Outra]
4. **Apresentar ao Prof. Pereira (ICe)** — opções: [Sim / Email / Eu mesmo]
5. **Revisar protocolo até AAAA-MM-DD** — opções: [Sim / Prazo diferente]

## DECISÕES TÉCNICAS (IA pode implementar após autorização)
- Implementar análise X no notebook Y
- Adicionar teste Z para função W
- Refatorar módulo M
```

---

### 5. CONDUCTOR — Perguntas em aberto

**Output:** `meeting/AAAA-MM-DD-angela-P0X/open-questions.md`

```markdown
# Open Questions — P0X

## PERGUNTAS (o que NÃO sei)
1. **Escola parceira:** qual escola tem perfil para o piloto?
2. **Cronograma:** a Ângela tem disponibilidade mensal? (dia/hora preferido)
3. **Recursos:** existe verba institucional para deslocamento Caicó-Natal?
4. **EEG (se P03/P05):** o ICe tem agenda aberta para uso em 2027?
5. **Lattes/ORCID:** a Ângela prefere ser co-autora ou autor sênior (último)?
```

---

### 6. CONDUCTOR — Recomendações técnicas

**Output:** `meeting/AAAA-MM-DD-angela-P0X/evidence.md` (sugestões da IA)

```markdown
# Evidence — Recomendações técnicas (NÃO decisões da Ângela)

## RECOMENDAÇÕES TÉCNICAS (propostas pela IA, podem ser ignoradas)

### Sobre P0X:
1. **Análise estatística:** usar ANCOVA com pré-teste como covariável (literatura: Cohen 1988)
   - Justificativa: controlar variabilidade individual
   - Risco: requer N mínimo

2. **Tamanho da amostra:** N=200 (P02) ou N=12-15 (P01 quali)
   - Justificativa: power analysis Monte Carlo (10k replicações)
   - Risco: dropout em coorte longitudinal

3. **Pré-registro:** submeter ANTES da coleta (não depois)
   - Justificativa: evitar HARKing
   - Referência: OSF best practices

### Sobre o programa:
- Priorizar P01 no mestrado (2 anos)
- P02-P05 viram papers paralelos

## PRÓXIMOS PASSOS PROPOSTOS (se autorizada)
- 2026-09-30: submeter P01 ao CEP
- 2026-10-01: submeter P01 a Computers & Education
- 2026-09-05: submeter 5 pré-registros ao OSF
```

---

### 7. CONDUCTOR — Juntar tudo + briefing

**Output:** `meeting/AAAA-MM-DD-angela-P0X/proposed-next-steps.md`

```markdown
# Proposed Next Steps — P0X

## Antes da reunião (você)
- [ ] Imprimir 3 cópias do briefing
- [ ] Imprimir 2 vias do termo de orientação
- [ ] Levar 1 página do manuscrito P0X
- [ ] Memorizar pitch de 5min

## Durante a reunião (15-30 min)
- [ ] Pitch de 5min (programa + P0X)
- [ ] Apresentar decisions-needed.md
- [ ] Anotar respostas no decisions-needed.md
- [ ] Assinar termo (se ok)
- [ ] Agendar próxima reunião

## Após a reunião (24-48h)
- [ ] Preencher ata (.agent/reports/ata-AAAA-MM-DD-angela-P0X.md)
- [ ] Atualizar .agent/STATE.yaml com decisões
- [ ] Atualizar AGENTS.md do projeto se mudou status
- [ ] Follow-up por e-mail (modelo em docs/email-angela-*.md)
- [ ] Iniciar ações autorizadas
```

---

## 📁 Estrutura final

```
meeting/
└── AAAA-MM-DD-angela-P0X/
    ├── context.md              ← fatos verificados
    ├── current-state.md        ← hipóteses + status
    ├── decisions-needed.md     ← o que precisa Ângela decidir
    ├── open-questions.md       ← o que não sei
    ├── evidence.md             ← recomendações técnicas (IA)
    └── proposed-next-steps.md  ← checklist operacional
```

---

## 🚨 Anti-padrões (o que NÃO fazer)

❌ **Misturar FATOS com HIPÓTESES** → Ângela não vai saber o que foi verificado
❌ **Colocar RECOMENDAÇÕES TÉCNICAS como DECISÕES PENDENTES** → confunde autoridade
❌ **Listar PERGUNTAS como DECISÕES** → Ângela não decide o que ela não sabe
❌ **Esconder gaps** → Ângela descobre na reunião e perde confiança
❌ **Submeter manuscrito sem autorização** → quebra regra do programa

---

## 📂 Onde já existe material relacionado

- `docs/email-angela-2026-09-reuniao.md` (email modelo)
- `docs/atas/2026-XX-XX-reuniao-angela-briefing.md` (briefing pack)
- `docs/atas/2026-XX-XX-reuniao-angela-autorizacao.md` (termo)
- `docs/atas/2026-XX-XX-reuniao-angela-agenda.md` (agenda + pitch)
- `docs/atas/2026-XX-XX-reuniao-angela-ata.md` (ata)
- `docs/CHECKLIST-PRE-REUNIAO-ANGELA.md` (checklist operacional)

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após 1ª reunião real com Ângela
