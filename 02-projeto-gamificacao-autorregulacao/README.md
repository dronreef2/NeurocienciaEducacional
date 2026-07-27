# 🎮 Projeto 02 — Gamificação e autorregulação em crianças do ensino fundamental

> **Status:** ⚪ Planejado
> **Período previsto:** M6–M18 (2026-12 → 2028-06)
> **Dificuldade:** 🟡 Média
> **Paper-alvo principal:** *Learning and Instruction* (Qualis A1)
> **Linha-mãe:** Leitura + Neurociências (UFRN) — desdobramento em Educação Matemática
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold

---

## ❓ Pergunta de pesquisa

**Diferentes elementos de gamificação (extrínsecos vs. intrínsecos) em aplicativos de matemática para crianças de 7–10 anos afetam de forma distinta a autorregulação da aprendizagem e o desempenho matemático?**

### Perguntas secundárias
1. Mecânicas extrínsecas (pontos, rankings, avatares) e intrínsecas (narrativa, autonomia, mastery) afetam **subcomponentes específicos** da autorregulação (planejamento, monitoramento, ajuste)?
2. Qual a relação entre **engajamento** (métrico comportamental) e **autorregulação percebida** (auto-relato) durante a atividade gamificada?
3. Os efeitos de gamificação são **moderados** por características da criança (sexo, idade, perfil de leitura)?
4. Efeitos de curto prazo (na sessão) se sustentam em **longo prazo** (1 mês depois)?

---

## 💡 Por que é inovadora

- **Move o foco** de "gamificação funciona?" para "**quais mecânicas de gamificação afetam quais processos cognitivos**" — distinguindo gamificação extrínseca de intrínseca.
- **Integra autorregulação** (constructo preditor de longo prazo) com **métricas comportamentais finas** (logs de uso).
- **Em crianças brasileiras** — literatura dominada por estudos com universitários americanos/europeus.
- Conecta com a linha de **Neurociência Cognitiva e Educação Matemática** que a Angela tem desenvolvido (projetos 2021/2024).

---

## 🔬 Metodologia

### Tipo
**Experimento 2×2 fatorial** (Tipo de gamificação: extrínseca vs. intrínseca) × (Presença/ausência), com **medidas repetidas** (pré-teste, pós-teste, follow-up 1 mês).

### Amostra
- **N** = 80–120 crianças (poder estatístico para detectar d ≥ 0.5)
- **Faixa etária:** 7–10 anos (2º ao 5º ano)
- **Critérios:** matriculadas em escolas parceiras; sem experiência prévia com o app prototipado
- **Recrutamento:** 2 escolas (1 piloto + 1 experimento principal)

### Instrumentos
- App prototipado com 4 versões (PsychoPy/Pavlovia ou Construct 3)
- Bateria de matemática adaptada (pré e pós)
- Escala de autorregulação para crianças (OSLIS-Brasil ou adaptada)
- Escala de motivação (adaptada de Children's Academic Intrinsic Motivation Inventory — CAIMI)
- Logs comportamentais (tempo na tarefa, número de tentativas, pedidos de dica, abandonos)
- Diário de auto-relato (escala emoji: 😊 😐 😕)

### Análise
- ANOVA mista 2×2×3 (Tipo × Presença × Tempo)
- Modelos lineares generalizados (GLM) para outcomes binários
- Análise de mediação: gamificação → engajamento → autorregulação
- Análise de cluster para identificar perfis de crianças

---

## 📅 Cronograma (previsão)

| Mês | Atividade |
|---|---|
| M6 | Revisão de literatura; parceria com designer/programador para prototipar o app |
| M7 | Submissão ao CEP (paralelo ao P01) |
| M8 | Piloto do app (n=10); ajustes de UX |
| M9 | Coleta principal — 4 condições experimentais |
| M10 | Coleta principal — follow-up curto (2 semanas) |
| M11 | Análise quantitativa (R/JASP) |
| M12 | Submissão do paper (revista BR + intl) |
| M18 | Follow-up longo (1 mês) — segunda submissão |

---

## 🤝 Aspectos críticos

- **Prototipagem do app** é o gargalo → parceria com curso de Design ou Ciência da Computação
- **Aspectos éticos:** consentimento parental, debate sobre "gamificação" e vício, debriefing pós-experimento
- **Equidade:** atentar para que as crianças sem acesso a tecnologia em casa não sejam duplamente desfavorecidas

---

## 📚 Leitura-base

- Hamari, J. et al. (2014). "Does gamification work?" — **LEITURA OBRIGATÓRIA**
- Mekler, E. D. et al. (2017). "Towards understanding the effects of individual gamification elements"
- Zimmerman, B. J. (2002). "Becoming a self-regulated learner"
- Kapp, K. (2012). *The Gamification of Learning and Instruction*
- Howard-Jones, P. et al. — neurociência da matemática

Ver bibliografia completa em `00-fundamentos/bibliografia-seminais.md` (seção 🎮).

---

## 📂 Estrutura local

```
02-projeto-gamificacao-autorregulacao/
├── README.md                    ← este arquivo
├── instrumentos/                ← a criar (TCLE, escalas, roteiro de teste)
├── protocolo/                   ← a criar (submissão CEP)
└── analise/                     ← a criar (scripts R/JASP)
```

---

> **Próximo passo:** abrir conversa com a Angela sobre a linha de Educação Matemática dela + parceria com curso de Design/CC para prototipar o app.
