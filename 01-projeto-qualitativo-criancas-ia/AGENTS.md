# AGENTS.md — Projeto P01 (IA e MToM, qualitativo)

> Instruções específicas para IAs trabalhando no **P01 — Vozes das crianças sobre tutores de IA**.
> **Versão:** 1.0 — 2026-09-19
> **Status:** M2 de 24 (P01 = 2026–2027), CEP-ready, piloto com 3 crianças ok, manuscrito v1 ok

---

## 🎯 Sobre o P01

**Título:** Vozes das crianças sobre tutores de IA: um estudo qualitativo com crianças do 2º ano do ensino fundamental

**Pergunta de pesquisa:** Como crianças de 7-11 anos interpretam, vivenciam e confiam no tutor de IA Khanmigo após 8 semanas de uso?

**Metodologia:** Análise Temática Reflexiva (Braun & Clarke 2022) — qualitativa exploratória

**N:** 12-15 crianças (saturação teórica)

**Periódico-alvo:** *Computers & Education* (A1, Elsevier)

**Cronograma:**
- 2026-Q3: submissão CEP + manuscrito v2
- 2026-Q4: piloto expandido (12-15 crianças)
- 2027-Q1: coleta formal
- 2027-Q2: análise
- 2027-Q3: manuscrito final
- 2027-Q4: **publicação**

---

## 📂 Estrutura do diretório

```
01-projeto-qualitativo-criancas-ia/
├── AGENTS.md                       ← este arquivo
├── README.md
├── protocolo/
│   ├── projeto-detalhado.md        ← protocolo completo
│   ├── carta-anuencia-escola.md    ← template TCLE escola
│   ├── statement-of-purpose-mestrado.md
│   ├── termo-compromisso.md
│   ├── checklist-cep.md
│   └── plataforma-brasil-checklist.md
├── instrumentos/
│   ├── 01-roteiro-entrevista.md
│   ├── 02-protocolo-thinkaloud.md
│   ├── 04-diario-uso.md
│   ├── 05-questionario-pais.md
│   ├── 06-questionario-professores.md
│   ├── 07-tcle-pais.md              ← TCLE + TALE
│   └── 08-tale-crianca.md
├── dados/                          ← VAZIO (aguarda aprovação CEP)
├── analise/
├── recrutamento/                   ← página i18n PT/EN/ES
└── manuscritos/
    └── P01_manuscrito_v1.md        ← rascunho atual
```

---

## 🚨 Regras ESPECÍFICAS do P01

1. **LGPD RÍGIDO**: NUNCA versionar dados brutos (entrevistas, áudios, TCLEs assinados)
2. **Pré-registro OSF JÁ FEITO**: `docs/osf-json/P01-osf.json` (não modificar)
3. **Manuscrito**: alterar apenas com revisão da Ângela
4. **TCLE/TALE**: versões com placeholders `[NOME_CRIANCA]` etc. — preencher antes de aplicar
5. **Piloto**: dados das 3 crianças (Maria, Pedro, Júlia) são **fictícios** — usados só para demonstração
6. **5 temas emergentes**: NÃO criar novos sem fundamentação teórica

---

## 📝 Convenções

- **Nomes:** `[NN]-[tipo]-[descrição].md` (01-roteiro-entrevista.md)
- **Citação:** Braun, V., & Clarke, V. (2022). *Thematic Analysis: A Practical Guide*. SAGE.
- **Software:** Khanmigo (Khan Academy) como tutor de IA
- **Análise:** Python (pandas, scikit-learn) + R (tidyverse) + Atlas.ti (opcional)

---

## 🎯 Próximas tarefas (P01)

1. **Reunião Ângela** — apresentar + pedir autorização
2. **Submeter CEP** (UFRN) — após autorização
3. **Submeter Computers & Education** — após autorização
4. **Submeter OSF pré-registro** (com `--all` ou `--prereg P01`)
5. **Coletar TCLE/TALE assinados** (post-CEP)
6. **Expandir piloto** (3 → 12 crianças)
7. **Manuscrito v2** (incorporar revisões)

---

## 🔗 Links úteis

- `protocolo/projeto-detalhado.md` — leia primeiro
- `docs/osf-json/P01-osf.json` — pré-registro
- `docs/atas/2026-XX-XX-reuniao-angela-briefing.md` — página do P01 no briefing
- `pages/2_📊_P01_Qualitativo.py` — visualização Streamlit
- `analise/Python/tests/test_pdf_export.py` — PDF do P01

---

**Última atualização:** 2026-09-19
