# 📝 Template de Nota de Leitura (Zettelkasten)

> **Sistema:** baseado no método de notas atômicas de Sönke Ahrens (*How to Take Smart Notes*, 2017) + ajuste para pesquisa científica.
> **Convenção:** cada paper seminal vira 1 nota atômica + 1 nota de aplicação.
> **Onde armazenar:** `00-fundamentos/notas-leitura/[autor]-[ano].md` (paper) e `[autor]-[ano]-aplicacao.md` (ligação com nossos projetos).

---

## 📋 Estrutura de uma nota de paper

```markdown
# 📄 [Sobrenome, Inicial.] ([Ano]). [Título].

> **Status:** ⬜ lido / 🟡 lendo / ✅ anotado
> **Tipo:** paper seminal / meta-análise / livro / capítulo
> **Relevância para:** P01, P02, ..., P05 (marca todos)
> **Citado em:** [futuros papers onde essa nota vai aparecer]

## 1. Citação completa (ABNT)
[Referência completa]

## 2. Tese central (1 parágrafo)
[Qual é a afirmação principal do paper/livro em 1 parágrafo]

## 3. Método
- **Tipo:** (teórico, experimental, meta-análise, revisão)
- **Amostra:** (N, faixa etária, contexto)
- **Desenho:** (within/between, fatorial, longitudinal...)
- **Medidas:** (comportamentais, EEG, surveys, etc.)
- **Análise:** (estatística, qualitativa)

## 4. 3 insights principais
1. **[Insight 1]:** em 1-2 frases
2. **[Insight 2]:** em 1-2 frases
3. **[Insight 3]:** em 1-2 frases

## 5. 1 crítica honesta
[O que o paper tem de fraco, limitado, ou que merece questionamento]

## 6. Citações literais (que valem guardar)
> "[Citação verbatim 1]" (p. X)
> "[Citação verbatim 2]" (p. Y)

## 7. Conceitos-chave (glossário)
- **[Conceito 1]:** definição operacional que o autor usa
- **[Conceito 2]:** ...

## 8. Conexões com outros papers lidos
- → [paper X] (concorda / discorda / complementa)
- → [paper Y] (mesma metodologia / mesmo achado / diferente)

## 9. Próxima leitura sugerida
[1-2 papers que o próprio autor cita como centrais e que vale a pena ler em seguida]
```

---

## 📋 Estrutura de uma nota de aplicação

```markdown
# 🎯 Aplicação: [Paper X] nos meus projetos

> **Status:** ⬜ rascunho / 🟡 em construção / ✅ consolidada
> **Aplicabilidade:** 🟢 direta / 🟡 indireta / 🔴 só conceitual
> **Para qual projeto:** P0X

## 1. Como esse paper pode alimentar o projeto?
[Parágrafo: por que esse paper é relevante para o P0X]

## 2. Que métodos posso replicar/adaptar?
- [Método 1]: como adaptar para minha realidade
- [Método 2]: ...

## 3. Que hipóteses posso gerar?
- **H1:** ...
- **H2:** ...

## 4. Que referencial teórico posso usar?
- [Conceito 1 do paper] como base do meu referencial
- [Conceito 2] como ponte para outro autor

## 5. Que armadilhas evitar?
- [Armadilha 1 que o paper teve e que eu devo evitar]
- [Armadilha 2]

## 6. Próximos passos concretos
- [ ] [Ação 1] (quando: M_X)
- [ ] [Ação 2] (quando: M_Y)
```

---

## 🗂️ Como organizar

```
00-fundamentos/notas-leitura/
├── template-nota.md                    ← este arquivo
├── template-aplicacao.md               ← (opcional, ver acima)
├── README.md                           ← índice de todas as notas
│
├── dehaene-2010.md                     ← nota do paper
├── dehaene-2010-aplicacao.md           ← aplicação aos projetos
├── diamond-2013.md
├── diamond-2013-aplicacao.md
├── miyake-2000.md
├── miyake-2000-aplicacao.md
├── hamari-2014.md
├── hamari-2014-aplicacao.md
├── luck-2014.md
├── luck-2014-aplicacao.md
├── naschold-2017.md
├── naschold-2017-aplicacao.md
├── ...
```

---

## 🔗 Regra de ouro

> **Se você não consegue usar a nota em um paper seu, ela está incompleta.**

Quando uma nota vira parte de um paper, a referência volta ao `README.md` de notas: "esta nota foi usada em: [paper X], [paper Y]". Isso cria **rastros de origem** (provenance) que vão te salvar na hora de defender tese, fazer revisão, ou responder por que decidiu X e não Y.

---

> **Inspirado em:** Sönke Ahrens, *How to Take Smart Notes* (2017); Tiago Forte, *Building a Second Brain* (2022); Andy Matuschak, "Evergreen notes" (online).
