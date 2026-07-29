# 📄 Singer, J. D. & Willett, J. B. (2003). *Applied Longitudinal Data Analysis*.

> **Status:** ✅ anotado
> **Tipo:** livro metodológico
> **Relevância para:** P05 (coorte), secundariamente P02 (medidas repetidas)
> **Citado em:** (a atualizar)

## 1. Citação completa (ABNT)

SINGER, Judith D.; WILLETT, John B. **Applied Longitudinal Data Analysis: Modeling Change and Event Occurrence**. New York: Oxford University Press, 2003.

## 2. Tese central (1 parágrafo)

A maioria das pesquisas em ciências sociais e da saúde **mede o mesmo indivíduo em múltiplos pontos no tempo**, mas a maioria dos pesquisadores **não sabe analisar esses dados direito**. Singer & Willett oferecem o **guia definitivo** para análise de dados longitudinais, desde a visualização (trajetórias individuais), passando por modelos de crescimento (latent growth curve models — LGCM), até modelos de eventos (survival analysis, hazard models). O livro é didático, com exemplos em SAS, R, Stata, e HLM, e tem foco em **aplicação prática** — como qualquer pesquisador pode modelar trajetórias individuais e populacionais.

## 3. Método (do livro)

- **Tipo:** livro metodológico
- **Estrutura:** 3 partes — (1) Explorando dados longitudinais, (2) Modelando mudança (LGCM), (3) Modelando eventos
- **Público:** pesquisadores e alunos de pós-graduação em ciências sociais, psicologia, educação, saúde
- **Posição:** integração de modelagem multinível e análise de sobrevivência, com exemplos reais

## 4. 3 insights principais

1. **Sempre comece visualizando as trajetórias individuais.** Antes de qualquer modelo, plote os dados de cada participante ao longo do tempo. Muitas perguntas se respondem só com visualização. **Implicação para P05:** plotar as trajetórias EEG, FE, leitura de cada criança separadamente ANTES de ajustar modelos populacionais.

2. **A LGCM (Latent Growth Curve Model) tem 3 parâmetros básicos:** intercept (valor inicial), slope (taxa de mudança), e variâncias (heterogeneidade individual). A pergunta "as crianças têm trajetórias diferentes?" é respondida pela variância do slope. **Implicação para P05:** ajustar LGCM para cada medida, e se a variância do slope for significativa → ajustar LGMM (misture models) para identificar subgrupos.

3. **O tempo precisa ser modelado de forma significativa.** Tempo pode ser métrico (anos), mas também pode ser "número de ondas" ou "número de eventos". A escolha afeta interpretação. **Implicação para P05:** se as coletas forem anuais, tempo = ano; se houver atrasos, ajustar.

## 5. 1 crítica honesta

O livro usa **SAS, Stata, e HLM** como exemplos — não R. Para usar R, é preciso adaptar (lavaan, lme4, OpenMx). Além disso, o livro é de 2003 — avanços em modelos Bayesianos, modelos não-lineares, e modelagem multinível avançada não estão cobertos. Para o P05, vale complementar com Singer & Willett (2003) + documentação atual de R packages.

## 6. Citações literais (que valem guardar)

> "Change is the essential subject matter of science." (Cap. 1)

> "There are many ways to model change over time, and no one method is best for all questions." (Cap. 1)

> "Longitudinal data analysis is fundamentally about describing and explaining individual change." (Cap. 2)

## 7. Conceitos-chave (glossário)

- **Trajetória:** padrão de mudança individual ao longo do tempo
- **LGCM (Latent Growth Curve Model):** modelo que estima intercept e slope médios, e variâncias individuais
- **LGMM (Latent Growth Mixture Model):** extensão que identifica subgrupos de trajetórias distintas (latent classes)
- **Time-varying covariate:** variável que muda ao longo do tempo (ex: sono, exposição digital)
- **Time-invariant covariate:** variável estável (ex: sexo, SES)
- **Multilevel model:** modelagem multinível (medidas aninhadas em indivíduos)
- **Event history analysis:** análise de eventos (quando algo acontece pela primeira vez)

## 8. Conexões com outros papers lidos

- → **Raudenbush & Bryk (2002).** *Hierarchical Linear Models* — base teórica
- → **Diamond (2013).** *Executive Functions* — FE como outcome longitudinal
- → **Dehaene (2010).** *Reading in the Brain* — leitura como outcome longitudinal
- → **Naschold (2017).** *Projeto L+N* — modelo de pesquisa longitudinal em escola

## 9. Próxima leitura sugerida

- **Raudenbush, S. W. & Bryk, A. S. (2002).** *Hierarchical Linear Models* (HLM) — base teórica
- **Bolger, N. & Laurenceau, J.-P. (2013).** *Intensive Longitudinal Methods* — para medições diárias
- **Skrondal, A. & Rabe-Hesketh, S. (2004).** *Generalized Latent Variable Modeling* — bayesiano
- Documentação do pacote R `lavaan` (para SEM) — Rosseel (2012)
- Documentação do pacote R `OpenMx` — para LGCM/LGMM

---

## 🎯 Aplicação direta

Ver `singer-willett-2003-aplicacao.md` (a criar).
