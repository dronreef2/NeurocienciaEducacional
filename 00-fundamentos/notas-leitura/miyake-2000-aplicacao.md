# 🎯 Aplicação: Miyake et al. (2000) *Unity and Diversity of EF* nos projetos

> **Status:** ✅ consolidada
> **Aplicabilidade:** 🟢 direta em P04
> **Para qual projeto:** P04, P05

## 1. Como esse paper pode alimentar o programa?

Miyake et al. é o **paper de referência metodológica** para qualquer pesquisa sobre FE — estabeleceu o modelo de 3 FE (shifting, updating, inhibition) com análise fatorial confirmatória, e é citado em quase todo estudo sobre FE. Para o **P04**, é a base para construir a **bateria de avaliação de FE** e para a **análise estatística** (SEM).

## 2. Que métodos posso replicar/adaptar?

- **Modelo de 3 FE com SEM** (modelo de equações estruturais). **Para o P04**: usar o pacote `lavaan` no R para replicar a estrutura fatorial na amostra brasileira.
- **Bateria de 9 tarefas originais** (Wisconsin, Trail Making, Stroop, Stop-Signal, Random Number Generation, Tone Monitoring, N-back, Keeping Track, Letter Memory). **Para o P04**: adaptar para adolescentes (12–16 anos) com:
  - Wisconsin Card Sorting Test (computadorizado)
  - Trail Making A e B
  - Stroop computadorizado
  - Stop-Signal Task
  - N-back (1, 2, 3-back)
  - Keeping Track
- **Análise fatorial confirmatória** com índices de ajuste (CFI, TLI, RMSEA). **Para o P04**: alvo mínimo N=200 para ajustar bem o modelo.

## 3. Que hipóteses posso gerar?

- **H1 (P04):** A estrutura fatorial de 3 FE (shifting, updating, inhibition) replica em adolescentes brasileiros. **Risco:** a estrutura é menos clara em crianças e adolescentes do que em adultos — pode ser necessário modelo de 2 fatores.
- **H2 (P04):** O uso de IA generativa correlaciona-se mais fortemente com **updating** (memória de trabalho) do que com shifting/inhibition. **Mecanismo plausível:** a IA "faz o trabalho" da memória de trabalho (offloading).
- **H3 (P04):** O **fator comum de EF** (latente, acima dos 3 fatores específicos) é mais preditor de uso problemático de IA do que os fatores específicos.

## 4. Que referencial teórico posso usar?

- **Modelo de 3 FE (unity + diversity):** base conceitual
- **Common EF factor:** base para discutir "FE geral" vs. "FE específicas"
- **Análise fatorial confirmatória:** base metodológica para o P04 e para o P05

## 5. Que armadilhas evitar?

- ❌ **Não assumir que o modelo replica em outras idades/culturas** sem testar — modelo é robusto em adultos americanos, mas precisa ser testado em adolescentes brasileiros
- ❌ **Não usar amostra pequena** (N < 100) para SEM — modelos de 3 fatores com 3 indicadores cada exigem **N mínimo 200** para ajuste estável
- ❌ **Não confundir os nomes dos fatores** — Miyake usa "shifting" (não "flexibility"), "updating" (não "working memory"), "inhibition" (não "executive control")
- ❌ **Não cair em "FE como variável única"** — sempre que possível, descrever resultados por fator específico E pelo fator comum

## 6. Próximos passos concretos

- [ ] **Mapear as 9 tarefas originais** do Miyake para versões computadorizadas disponíveis em PT-BR (PsychoPy, Inquisit, PEBL)
- [ ] **Pré-registrar a hipótese de replicação do modelo** no OSF (ver `preregistracao/template-osf.md`)
- [ ] **Verificar Diamond 2013** (já em nota) — usar como base para interpretação desenvolvimental
- [ ] **Para o P01**, considerar que as crianças de 8–11 anos **têm FE já parcialmente dissociáveis** — então é viável investigar metacognição como FE aplicada
- [ ] **Ler Karr et al. (2018)** "A meta-analysis of the factor structure of executive functions" — meta-análise que confirma o modelo, mas levanta questões sobre年纪-effects
