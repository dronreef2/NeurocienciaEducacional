# AGENTS.md — Projeto P05 (Coorte Longitudinal, LGCM)

> Instruções para IAs trabalhando no **P05 — COORTE-INF (Estudo Longitudinal)**.
> **Versão:** 1.0 — 2026-09-19
> **Status:** protocolo pronto, dados sintéticos 5 ondas ok, LGCM + cross-lagged

---

## 🎯 Sobre o P05

**Título:** COORTE-INF: Desenvolvimento cognitivo e neural de crianças dos 7 aos 11 anos

**Pergunta:** Quais são as trajetórias de desenvolvimento de FE em crianças expostas à IA?

**Design:** Coorte prospectiva + LGCM + Cross-Lagged Panel Models + sub-estudo EEG

**N:** 200 crianças (início aos 7 anos)

**5 ondas anuais:** T1=7 anos, T2=8, ..., T5=11 anos

**Medidas (por onda):**
- Inibição: Stroop + Go/No-Go
- Memória: Digit Span + Corsi Block
- Flexibilidade: TMT-B + Wisconsin Card Sorting
- Engajamento: questionário
- Exposição IA: questionário parental
- Sub-estudo EEG: N170, P300 (N=50 por onda)

**Periódico-alvo:** *Child Development* (A1) ou *Developmental Psychology*

**Cronograma:**
- 2026-Q4: começar T1 (7 anos)
- 2027-T5: 5 ondas anuais
- 2030-Q4: manuscrito final
- 2031-Q1: publicação

---

## 🚨 Regras ESPECÍFICAS

1. **Longitudinal = comprometimento de 5 anos**: equipe + financiamento + escola precisam estar garantidos ANTES de T1
2. **LGCM (Latent Growth Curve Models):**
   - Intercept (baseline) + Slope (crescimento)
   - Var(Intercept) > 0
   - Var(Slope) > 0
   - Cov(Int, Slope) < 0 → catch-up
3. **Cross-Lagged Panel Models:**
   - X_t → Y_{t+1} (efeito causal)
   - Y_t → X_{t+1} (efeito reverso)
   - Autoregressivo: X_t → X_{t+1}, Y_t → Y_{t+1}
4. **Análise de sobrevivência:** tempo até atingir critério de proficiência FE
5. **Attrition:** documentar dropouts, FIML se MAR
6. **Power:** n=200 detecta slope pequeno (d=0.3) com power=0.80

---

## 📊 Dados sintéticos

- **Arquivo:** `dados_sinteticos/P05_dados_longitudinais_sinteticos.csv`
- **N:** 200 crianças × 5 ondas = 1000 observações
- **Colunas:** crianca_id, onda, fe_inibicao, fe_memoria, fe_flexibilidade, idade, sexo

---

## 🎯 Hipóteses pré-registradas

| H | Parâmetro | Esperado |
|---|---|---|
| H5.1 | Slope linear β1 | +0.5 DP/ano |
| H5.2 | Var(Intercept) | > 0 |
| H5.3 | Var(Slope) | > 0 |
| H5.4 | Cov(Intercept, Slope) | < 0 (catch-up) |
| H5.5 | Cross-lagged (IA→FE) | β > 0 |
| H5.6 | Sobrevivência | Mediana = ? ondas |

---

## 🔗 Links

- `docs/osf-json/P05-osf.json` — pré-registro
- `pages/6_📅_P05_Longitudinal.py` — visualização Streamlit
- `analise/Python/notebooks/07_cross_lagged.ipynb`
- `analise/Python/notebooks/12_sobrevivencia.ipynb`

---

**Última atualização:** 2026-09-19
