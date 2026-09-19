# 📋 Playbook: revisar-metodologia

> **Trigger:** "Revisar metodologia do P0X" / "Validar protocolo"
> **Domínio:** Research + Methodology + Review
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Garantir que o protocolo de um projeto (P0X) está cientificamente sólido antes de submeter/coletar.

---

## 🔄 Fluxo (6 passos)

### 1. CONDUCTOR — Identificar projeto

```bash
Ler:
- 0X-.../AGENTS.md
- 0X-.../protocolo/projeto-detalhado.md
- 0X-.../instrumentos/
- 00-fundamentos/hipoteses/ (se existir)
```

**Output:** snapshot do estado do projeto.

---

### 2. RESEARCH — Validar literatura

```bash
- Notas de leitura relevantes (00-fundamentos/notas-leitura/)
- Papers citados no protocolo (recentes? canônicos?)
- Lacunas teóricas (o protocolo cobre?)
- Coerência com linha de pesquisa (Leitura + Neurociências)
```

**Output:** lista de gaps teóricos.

---

### 3. METHODOLOGY — Validar método

```bash
Checklist:
- [ ] Hipóteses operacionais (H1, H2, ...) com variáveis claras
- [ ] Variáveis operacionalizadas (independente, dependente, mediador, moderador)
- [ ] População (N, idade, sexo, contexto)
- [ ] Critérios de inclusão/exclusão (justificados)
- [ ] Instrumentos (validados? cite refs)
- [ ] Procedimentos de coleta (passo a passo)
- [ ] Plano de análise (técnicas + software)
- [ ] Power analysis (N suficiente?)
- [ ] Pré-registro OSF consistente
- [ ] Considerações éticas (LGPD, CEP)
```

**Output:** checklist de gaps metodológicos.

---

### 4. REVIEW — Validar consistência

```bash
Procurar:
- Hipótese X sem variável dependente
- Instrumento Y não validado para a idade-alvo
- Plano de análise com técnica X mas dados Y não permite
- N muito pequeno para detectar d=Z
- Cronograma irrealista
- Conflito com plano de mestrado
```

**Output:** lista de inconsistências + severidade.

---

### 5. CONDUCTOR — Gerar relatório de revisão

**Arquivo:** `.agent/reports/methodology-review-P0X-AAAA-MM-DD.md`

```markdown
# Methodology Review — P0X

**Data:** AAAA-MM-DD
**Versão do protocolo:** vN

## Status: [OK / NEEDS REVISION / BLOCKED]

## ✅ Pontos fortes
- [item]

## ⚠️ Pontos a melhorar
- [item] — sugestão: [...]

## 🚨 Bloqueios (HUMAN GATE)
- [decisão que precisa Ângela]

## 📋 Checklist metodológico
- [ ] Hipóteses: status
- [ ] Variáveis: status
- [ ] População: status
- [...]

## 🎯 Recomendações (NÃO decisões)
- IA sugere: [...]
- Risco: [...]
```

---

### 6. CONDUCTOR — Apresentar ao usuário

```
🤖 Methodology Review — P0X

Status: NEEDS REVISION

✅ Fortes (3): [...]
⚠️ Melhorar (5): [...]
🚨 Bloqueios (1): [...]

Deseja que eu corrija os pontos ⚠️ ?
Os 🚨 precisam de decisão sua (e/ou da Ângela).
```

---

**Última atualização:** 2026-09-19
