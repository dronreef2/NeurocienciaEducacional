# 📋 Playbook: analisar-dados

> **Trigger:** "Analisar dados de P0X" / "Rodar análise estatística"
> **Domínio:** Engineering + Statistics + Research
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Executar análise estatística com **rastreabilidade** + **reprodutibilidade** + **HUMAN GATE na interpretação**.

---

## 🔄 Fluxo (6 passos)

### 1. CONDUCTOR — Verificar pré-requisitos

```bash
Checklist:
- [ ] Pré-registro OSF submetido (não HARKing)
- [ ] Dados anonimizados (LGPD)
- [ ] Plano de análise pré-registrado
- [ ] Dados em formato tidy (1 linha por observação)
- [ ] Seed definido (reprodutibilidade)
```

**Output:** GO / NO-GO.

---

### 2. STATISTICS — Preparar script de análise

```bash
- Notebook ou script versionado (git)
- Carregar dados com seed=42
- Aplicar transformações pré-registradas
- NUNCA inventar transformações novas (HARKing)
```

**Output:** `analise/Python/notebooks/NN_analise_P0X.ipynb` versionado.

---

### 3. ENGINEERING — Rodar análise

```bash
jupyter nbconvert --execute notebook.ipynb
# OU
pytest tests/test_analysis_P0X.py -v  # se houver testes
```

**Output:** outputs (figuras, tabelas) versionados.

---

### 4. STATISTICS — Validar resultados

```bash
Checklist:
- [ ] Power atingido?
- [ ] Assumptions verificadas (normalidade, homocedasticidade, etc.)?
- [ ] Outliers tratados (pré-registrado)?
- [ ] Effect size + IC 95% reportados?
- [ ] p-values corrigidos (se múltiplos testes)?
- [ ] Dados missing documentados (padrão, %)?
```

**Output:** lista de warnings + sanity checks.

---

### 5. RESEARCH — Gerar relatório

**Arquivo:** `resultados/analise_P0X_AAAA-MM-DD.md`

```markdown
# Análise — P0X

## Dados
- N total: N
- Período: AAAA-MM-DD a AAAA-MM-DD
- Fonte: dados_sinteticos/P0X_*.csv (sintético) / real

## Métodos
- Análise 1: [técnica, pressupostos verificados]
- Análise 2: [...]
- Software: Python 3.11 + scipy + statsmodels
- Seed: 42

## Resultados
### Tabela 1: [descritiva]
| Variável | N | Média | DP | Min | Max |
|---|---|---|---|---|---|
| X | ... | ... | ... | ... | ... |

### Tabela 2: [inferencial]
| Hipótese | β | IC 95% | p | d Cohen |
|---|---|---|---|---|
| H1 | ... | ... | ... | ... |

### Figura 1: [visualização]
- `resultados/figuras/P0X_*.png`

## ⚠️ Limitações
- [limitação 1]
- [limitação 2]

## 🚨 INTERPRETAÇÃO (HUMAN GATE)
- IA NÃO interpreta resultados — apenas reporta
- Humano (pesquisadora + Ângela) interpreta + escreve discussão
```

---

### 6. CONDUCTOR — Entregar ao usuário

```
🤖 Análise completa — P0X

N: [N]
Resultados: [resumo tabular]
Outputs: [links para figuras + tabelas]

⚠️ INTERPRETAÇÃO é com você (e Ângela).
IA reportou fatos, não conclusões.
```

---

## 🚨 Anti-padrões

❌ **HARKing** (Hypothesizing After Results are Known)
❌ **Interpretar resultados automaticamente** (HUMAN GATE)
❌ **Rodar sem pré-registro**
❌ **Mudar análise após ver dados**
❌ **Esconder resultados negativos**
❌ **Não reportar effect size + IC**

---

**Última atualização:** 2026-09-19
