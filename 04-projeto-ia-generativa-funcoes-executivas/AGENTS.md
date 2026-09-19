# AGENTS.md — Projeto P04 (SEM, IA × FE)

> Instruções para IAs trabalhando no **P04 — Modelagem de Equações Estruturais**.
> **Versão:** 1.0 — 2026-09-19
> **Status:** protocolo pronto, dados sintéticos SEM ok, N=400

---

## 🎯 Sobre o P04

**Título:** Uso de IA generativa e funções executivas em crianças do 2º ao 5º ano: estudo transversal com SEM

**Pergunta:** Quais processos explicam a relação entre uso de IA e FE?

**Design:** Transversal + Modelagem de Equações Estruturais (SEM)

**N:** 300-500 crianças (transversal)

**Modelo conceitual:**

```
Uso de IA (X) ──a──> Engajamento (M) ──b──> FE (Y)
   │                                              ↑
   └──────c' (direto)─────────────────────────────┘
   │
   └──────W×X (moderação por letramento)──┘
```

**Periódico-alvo:** *Computers in Human Behavior* (A1, Elsevier)

**Cronograma:**
- 2028-Q1: CEP + coleta
- 2028-Q2/Q3: análise SEM
- 2028-Q4: manuscrito
- 2029-Q1: publicação

---

## 🚨 Regras ESPECÍFICAS

1. **SEM exige N grande** — mínimo N=200, ideal N=300+
2. **Índices de ajuste obrigatórios:**
   - CFI ≥ 0.95
   - TLI ≥ 0.95
   - RMSEA ≤ 0.06
   - SRMR ≤ 0.08
3. **Mediação + moderação** = modelo mais complexo — usar software apropriado (lavaan, R)
4. **Pré-registrar** SEM mesmo em transversal — análise SEM é flexível demais
5. **Missing data:** reportar padrão, usar FIML se >5%
6. **Multicolinearidade:** VIF < 5 para todos os preditores

---

## 📊 Dados sintéticos

- **Arquivo:** `dados_sinteticos/P04_dados_sinteticos.csv`
- **N:** 400
- **Colunas:** respondente_id, ia_uso, engajamento, fe_inibicao, fe_memoria, fe_flexibilidade, letramento_pais, sexo, idade

---

## 🎯 Hipóteses pré-registradas

| H | Caminho | Coef. esperado | IC 95% |
|---|---|---|---|
| H4.1 | a (X→M) | 0.30 | [0.20, 0.40] |
| H4.2 | b (M→Y) | 0.40 | [0.30, 0.50] |
| H4.3 | c' (X→Y direto) | 0.15 | [0.00, 0.20] |
| H4.4 | Indireto (a×b) | 0.12 | [0.06, 0.18] |
| H4.5 | W×X (moderação) | 0.15 | [0.05, 0.25] |

---

## 🔗 Links

- `docs/osf-json/P04-osf.json` — pré-registro
- `pages/5_📈_P04_SEM.py` — visualização Streamlit
- `analise/Python/notebooks/04_tutorial_sem.ipynb` — tutorial SEM

---

**Última atualização:** 2026-09-19
