# 🎯 Aplicação: Dehaene (2010) *Reading in the Brain* nos projetos

> **Status:** ✅ consolidada
> **Aplicabilidade:** 🟢 direta em P01 e P03
> **Para qual projeto:** P01, P03, P05

## 1. Como esse paper pode alimentar o programa?

Dehaene oferece o **framework conceitual de reciclagem neuronal** que pode estruturar todo o programa. A ideia central — "o cérebro não evoluiu pra ler, ele recicla áreas existentes" — é uma lente poderosa pra pensar como a IA generativa (que não existia há 5 anos) também vai **reciclar** as mesmas áreas, ou criar padrões novos. P01 pergunta exatamente isso. P03 pode medir isso com EEG (VWFA, N170). P05 pode ver como o recrutamento muda ao longo do desenvolvimento.

## 2. Que métodos posso replicar/adaptar?

- **Paradigma de leitura em crianças (fMRI/EEG):** Dehaene e colaboradores usaram tarefas de leitura de palavras vs. símbolos em crianças de 6–12 anos. **Para o P03**: adaptar com EEG (em vez de fMRI) — mais barato, mais fácil com crianças, sem necessidade de imobilidade total.
- **Tarefa de "leitura passiva"** com apresentação de palavras isoladas e palavras em frases: **Para o P01**: usar como atividade do think-aloud.
- **Comparação cross-cultural** (Dehaene et al. 2010, *PNAS*): a VWFA funciona igual em leitores de francês, português, chinês. **Para o P03**: controlar por exposição prévia a leitura em diferentes meios.

## 3. Que hipóteses posso gerar?

- **H1 (P01):** Crianças que usam Khanmigo há mais tempo vão descrever o tutor como "mais inteligente" se a experiência reforçar a sensação de "aprendizagem" (vs. "resposta pronta"). **Conexão:** metacognição.
- **H2 (P03):** A leitura na tela vai ativar a VWFA mais tardiamente em crianças (N170 mais lento) do que a leitura em papel, refletindo menor automatização. **Conexão:** EEG/ERP.
- **H3 (P05):** Crianças com maior exposição a leitura digital na primeira infância (5–6 anos) terão padrão de recrutamento diferente de crianças com mais exposição a leitura em papel, mensurável por N170 aos 8 anos. **Conexão:** janela desenvolvimental.

## 4. Que referencial teórico posso usar?

- **Recycling hypothesis:** base teórica do P01 (sobre como crianças processam o "novo" da IA) e do P03 (sobre como crianças processam leitura digital vs. papel)
- **VWFA e N170:** variável dependente concreta para o P03
- **Letter-position coding:** base para discussão de erros do tutor (quando o Khanmigo erra uma palavra, como a criança percebe?)

## 5. Que armadilhas evitar?

- ❌ **Não tratar a leitura como "natural"** — Dehaene é explícito que é invenção cultural. Cuidado com afirmações deterministas ("o cérebro não foi feito pra isso, então...")
- ❌ **Não simplificar a N400 como "integração semântica"** sem cuidar do contexto: a N400 também modula por frequência lexical, concreção, idade, etc.
- ❌ **Não superestimar poder explicativo da VWFA** — é uma das áreas, não a única. Sistema de leitura é distribuído.

## 6. Próximos passos concretos

- [ ] Ler **Stavanger et al. (2024)** "Screen reading and the brain in children" — aplicação direta ao P03
- [ ] Adicionar **Dehaene 2010** ao referencial teórico do `projeto-detalhado.md` do P01 (✅ feito em 2026-07-26)
- [ ] No M3 (quando o P01 entrar em análise), **usar recycling hypothesis como categoria de codificação temática** ("como a criança vê o Khanmigo — como máquina nova, como extensão de algo conhecido, como novo 'objeto' cultural?")
- [ ] Para o P03, **incluir tarefa de leitura de palavras isoladas** (não só textos) — permite análise de N170 individual
