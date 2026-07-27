# 🎯 Aplicação: Hamari et al. (2014) *Does gamification work?* nos projetos

> **Status:** ✅ consolidada
> **Aplicabilidade:** 🟢 direta em P02
> **Para qual projeto:** P02

## 1. Como esse paper pode alimentar o programa?

Hamari et al. é a **revisão sistemática de referência** sobre gamificação em contextos reais. Para o **P02**, é a base para: (a) definir o que é "gamificação" operacionalmente, (b) identificar o gap (poucos estudos com crianças), (c) escolher os elementos de gamificação a testar, e (d) evitar as armadilhas metodológicas dos 24 estudos revisados.

## 2. Que métodos posso replicar/adaptar?

- **Decomposição de elementos de gamificação.** Hamari identificou que os 24 estudos usavam diferentes combinações. **Para o P02**: o design 2×2 (extrínseca vs. intrínseca × presença/ausência) já está no README — mas **definir cada elemento** operacionalmente:
  - **Extrínseca:** pontos, badges, leaderboards (ranking)
  - **Intrínseca:** narrativa, escolha/autonomia, mastery (níveis de dificuldade adaptáveis)
- **Medidas de engajamento e aprendizagem** em conjunto. **Para o P02**: já planejado, mas adicionar **medida de esforço percebido** (escala Likert) e **métrica comportamental de persistência** (tempo na tarefa após erro).
- **Follow-up de longo prazo.** Hamari identificou que a maioria dos estudos tem follow-up curto. **Para o P02**: já planejado 1 mês — **manter**.

## 3. Que hipóteses posso gerar?

- **H1 (P02):** Gamificação **intrínseca** (narrativa + autonomia) tem efeito maior sobre **autorregulação** do que gamificação extrínseca (pontos + ranking).
- **H2 (P02):** Gamificação extrínseca tem efeito **curto prazo** sobre engajamento, mas **neutro ou negativo** sobre autorregulação em longo prazo.
- **H3 (P02):** O efeito de gamificação é **moderado por idade** — crianças de 7–8 anos respondem mais a extrínseca, crianças de 9–10 anos respondem mais a intrínseca.
- **H4 (P02):** O efeito de gamificação é **moderado por sexo** — meninas podem responder melhor a narrativa, meninos a ranking (cuidado com viés de gênero!).

## 4. Que referencial teórico posso usar?

- **Sailer & Homner (2020)** meta-análise — para base quantitativa mais robusta
- **Mekler et al. (2017)** "Towards understanding the effects of individual gamification elements" — para descer ao nível de cada elemento
- **Teoria da Autodeterminação (Deci & Ryan)** — para fundamentar diferença intrínseca vs. extrínseca
- **Teoria da Autoregulação (Zimmerman, Schunk)** — para a variável dependente do P02

## 5. Que armadilhas evitar?

- ❌ **Não chamar de "gamificação" sem definir elementos** — sempre explicitar quais mecânicas estão sendo testadas
- ❌ **Não comparar com "no gamification" como controle placebo** — grupo controle deve ter app equivalente sem elementos de jogo
- ❌ **Não medir só engajamento** — Hamari identificou que poucos estudos medem aprendizagem real
- ❌ **Não extrapolar de adultos para crianças** — efeito pode ser qualitativamente diferente
- ❌ **Não ignorar o viés de gênero** — meninas e meninos podem responder de forma diferente
- ❌ **Não cair no viés de publicação** — considerar que muitos estudos nulos não foram publicados

## 6. Próximos passos concretos

- [ ] **Ler Sailer & Homner (2020)** meta-análise quantitativa — atualiza Hamari com mais dados
- [ ] **Ler Mekler et al. (2017)** — foco em elementos individuais
- [ ] **Construir o app protótipo** (4 versões) com parceria com curso de Design/CC
- [ ] **Definir operacionalmente cada elemento** (quantos pontos, quais badges, qual narrativa)
- [ ] **Pré-registrar hipóteses** no OSF (template em `preregistracao/template-osf.md`)
- [ ] **Para o P02**, considerar **medida de "dark patterns"** (gamificação manipulativa) — distinguir de gamificação ética
