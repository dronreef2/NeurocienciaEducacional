# AGENTS.md — Projeto P02 (Gamificação e FE, ECR)

> Instruções para IAs trabalhando no **P02 — Efeitos da Gamificação sobre Funções Executivas**.
> **Versão:** 1.0 — 2026-09-19
> **Status:** protocolo pronto, dados sintéticos ok, ECR 2×4, N=200

---

## 🎯 Sobre o P02

**Título:** Efeitos da Gamificação (Pontos + Narrativa) sobre Funções Executivas em Crianças do 3º ao 5º ano

**Pergunta:** Gamificação com pontos e narrativa melhora FE (atenção, memória de trabalho, inibição, flexibilidade)?

**Design:** ECR fatorial **2×4**
- Fator 1: Pontos (sim/não)
- Fator 2: Narrativa (sim/não)
- 4 grupos: Controle, Pontos, Narrativa, Pontos+Narrativa (50 cada, total N=200)

**Medidas:**
- FE: Stroop (inibição), TMT-B (flexibilidade), Digit Span (memória)
- Engajamento: questionário Likert

**Periódico-alvo:** *Learning and Instruction* (A1) ou *Computers in Human Behavior*

**Cronograma:**
- 2026-Q4: piloto + CEP
- 2027-Q1/Q2: coleta formal
- 2027-Q3: análise
- 2027-Q4: manuscrito

---

## 🚨 Regras ESPECÍFICAS

1. **ECR = registro ANVISA-equivalente para educação**: plano de análise PRÉ-REGISTRADO, sem desvios
2. **Dados sintéticos** em `dados_sinteticos/P02_dados_sinteticos.csv` — seed=42
3. **Randomização**: estratificada por sexo + idade (não pode falhar)
4. **Cegamento**: análise cega (analista não sabe o grupo)
5. **Blocos do ECR:**
   - A: Pontos (sim/não)
   - B: Narrativa (sim/não)
   - Interação A×B = hipótese principal H2.3

---

## 📂 Estrutura

```
02-projeto-gamificacao-funcoes-executivas/
├── AGENTS.md                  ← este arquivo
├── README.md
└── protocolo/
    └── projeto-detalhado.md
```

(Outros arquivos em `analise/Python/dados_sinteticos/P02_dados_sinteticos.csv`)

---

## 📊 Dados sintéticos

- **Arquivo:** `dados_sinteticos/P02_dados_sinteticos.csv`
- **N:** 200
- **Colunas:** participante_id, grupo, stroop_pre, stroop_pos, tmt_pre, tmt_pos, digit_span_pre, digit_span_pos, engajamento
- **Delta columns:** stroop_delta, tmt_delta, digit_span_delta

---

## 🎯 Hipóteses pré-registradas

| H | Variável | Efeito esperado | d Cohen |
|---|---|---|---|
| H2.1 | Stroop (inibição) | Pontos ↑ | 0.20 |
| H2.2 | Digit Span (memória) | Narrativa ↑ | 0.25 |
| H2.3 | TMT-B (flexibilidade) | Pontos × Narrativa ↑↑ | 0.35 |
| H2.4 | Engajamento | Mediação | Indireto ≠ 0 |

---

## 🔗 Links

- `docs/osf-json/P02-osf.json` — pré-registro
- `pages/3_🎮_P02_Gamificacao.py` — visualização Streamlit
- `analise/Python/notebooks/10_p02_ecr_simulacao.ipynb` — simulação ECR

---

**Última atualização:** 2026-09-19
