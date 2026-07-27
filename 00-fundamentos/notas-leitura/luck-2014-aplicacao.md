# 🎯 Aplicação: Luck (2014) *Introduction to the ERP Technique* nos projetos

> **Status:** ✅ consolidada
> **Aplicabilidade:** 🟢 direta em P03 e P05
> **Para qual projeto:** P03, P05

## 1. Como esse paper/livro pode alimentar o programa?

Luck é o **manual obrigatório** para quem vai trabalhar com ERPs. Para o **P03 (EEG leitura digital vs. papel)** e para o **P05 (coorte longitudinal)**, é a base para o pipeline técnico completo: aquisição, pré-processamento, análise de componentes, estatística.

## 2. Que métodos posso replicar/adaptar?

- **Pipeline de pré-processamento EEG** (Luck Cap. 4–6):
  - Filtragem: 0.1–30 Hz (passa-banda) + 60 Hz notch
  - Re-amostragem: 250 Hz (suficiente para ERPs)
  - Rejeição de artefatos: amplitude threshold + ICA
  - Referência: average reference (ou mastoids para ERPs frontais)
  - Baseline: 200 ms pré-stimulus
- **Análise de componentes** (Luck Cap. 8–12):
  - **N170 (170 ms):** diferencia letras de outros estímulos visuais; **ideal para P03**
  - **N400 (400 ms):** integração semântica; **útil para P03 com tarefas de leitura**
  - **P300 (300 ms):** atenção e memória; **útil para P03 com oddball paradigm**
  - **P600 (600 ms):** reanálise sintática; **útil para P03 com manipulação de complexidade**
- **Análise estatística** (Luck Cap. 14): **mass-univariate cluster-permutation** (evita problema de múltiplas comparações)
- **Adaptações para crianças** (Luck Cap. 16): pausas curtas, ensaio, número mínimo de trials (≥ 30 por condição)

## 3. Que hipóteses posso gerar?

- **H1 (P03):** A amplitude de **N170** é menor para leitura na tela vs. papel em crianças de 8–10 anos, refletindo menor automatização perceptual.
- **H2 (P03):** A latência de **N400** é maior para leitura na tela com hipertexto (criança precisa integrar mais informação, então processa mais devagar).
- **H3 (P03):** A amplitude de **P300** é maior para textos informativos vs. narrativos, refletindo maior demanda atencional.
- **H4 (P05):** A **razão theta/beta** em repouso (medida de maturação) correlaciona-se com o desempenho em leitura — prediz quem vai ler melhor aos 8 anos.

## 4. Que referencial teórico posso usar?

- **Componentes ERP como marcadores de processos cognitivos:** base metodológica
- **Mass-univariate analysis:** solução para múltiplas comparações em séries temporais
- **ICA para remoção de artefatos:** alternativa ao threshold-based rejection
- **Adaptações infantis:** base para protocolo de coleta com crianças

## 5. Que armadilhas evitar?

- ❌ **Não usar referência inadequada** — escolha da referência (average, mastoids, tip of nose) pode mudar a topografia inteira. Decidir antes da coleta, não depois.
- ❌ **Não fazer ANOVA pico-a-pico** — usar mass-univariate cluster-permutation (Luck é explícito sobre isso)
- ❌ **Não filtrar demais** — filtragem excessiva pode distorcer componentes reais. Padrão: 0.1–30 Hz, mas ajustar para o componente de interesse.
- ❌ **Não usar canais inadequados para crianças** — alta densidade (128 canais) é difícil com crianças. Usar 32 ou 64 canais.
- ❌ **Não confundir P300 com P3a/P3b** — são subtipos diferentes (P3a = novelty, frontal; P3b = target, parietal)
- ❌ **Não ignorar a fadiga em crianças** — protocolos > 30 min com crianças geram ruído

## 6. Próximos passos concretos

- [ ] **Ler Cohen (2014)** *Analyzing Neural Time Series Data* — livro prático complementar
- [ ] **Assistir tutoriais de Mike Cohen** (mikexcohen.com) — práticos, com código MATLAB/Python
- [ ] **Treinar no pipeline do ICe** (acompanhar uma coleta de outro pesquisador) — **essencial antes de coletar**
- [ ] **Definir o pipeline ANTES da coleta piloto** (n=5 do P03) — testar com criança adulta voluntária primeiro
- [ ] **Pré-registrar hipóteses no OSF** (template em `preregistracao/template-osf.md`)
- [ ] **Ler Stavanger et al. (2024)** "Screen reading and the brain in children" — exemplo de aplicação em crianças
- [ ] **Para o P05**, **incluir medida de EEG em repouso** (5 min, olhos abertos/fechados) — para maturação
