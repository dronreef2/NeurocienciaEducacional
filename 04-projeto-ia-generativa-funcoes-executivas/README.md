# 🤖 Projeto 04 — IA generativa × funções executivas em adolescentes

> **Status:** ⚪ Planejado
> **Período previsto:** M24–M36 (2028-07 → 2029-06)
> **Dificuldade:** 🟠 Alta
> **Paper-alvo principal:** *Computers in Human Behavior* (Qualis A1)
> **Linha-mãe:** Tecnologia + cognição (transversal à linha Leitura + Neurociências)
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold

---

## ❓ Pergunta de pesquisa

**Qual a relação entre o padrão de uso de IA generativa (ChatGPT, Claude, Gemini) para escrita e o desempenho em tarefas de funções executivas (memória de trabalho, controle inibitório, flexibilidade cognitiva) e criatividade em adolescentes de 12–16 anos?**

### Perguntas secundárias
1. A **frequência de uso** de IA generativa para escrita prediz menor desempenho em FE?
2. O **tipo de uso** (cognitively offloading vs. scaffolding) modula essa relação?
3. **Controle inibitório** é a FE mais afetada pelo uso de IA?
4. Há efeito **dose-resposta** (mais uso → menor FE) ou efeito de **curva em U invertido** (uso moderado = benéfico)?
5. Criatividade é **prejudicada ou estimulada** pelo uso de IA generativa?

---

## 💡 Por que é inovadora

- **Tema emergente com quase zero dados em desenvolvimento** — janela de oportunidade
- Conecta com a discussão internacional de **"cognitive offloading"** (Risko & Gilbert, 2016) e com debates regulatórios (EU AI Act, políticas do MEC)
- **Em adolescentes** (12–16) — faixa etária pouco estudada, mas com uso intenso de IA
- **Fronteira** do programa: pode ser **independente** da linha da Angela (ela não tem tradição em IA generativa ainda), o que te posiciona como pesquisadora autônoma

---

## 🔬 Metodologia

### Tipo
**Estudo transversal correlacional** com componente qualitativo complementar.

### Amostra
- **N** = 150–300 adolescentes (poder estatístico robusto)
- **Faixa etária:** 12–16 anos (6º ao 9º ano)
- **Critérios:** matriculados em escola parceira, com consentimento dos pais e assentimento
- **Recrutamento:** 3–5 escolas (presenciais ou amostragem online com verificação parental)

### Instrumentos

#### Bateria cognitiva
- **Memória de trabalho:** N-back (1, 2, 3-back) — versão computadorizada (PsychoPy)
- **Controle inibitório:** Stroop (cores/palavras) + Go/No-Go
- **Flexibilidade cognitiva:** Wisconsin Card Sorting Test (versão computadorizada) ou Trail Making B
- **Criatividade:** Torrance Test of Creative Thinking (TTCT) — fluência, flexibilidade, originalidade, elaboração

#### Tarefa de escrita
- **Com IA:** escrever uma redação com ChatGPT/Claude disponível
- **Sem IA:** escrever a mesma redação sem ajuda
- **Comparação:** qualidade textual, originalidade, esforço percebido

#### Questionários
- **Padrões de uso de IA:** questionário validado (a adaptar — buscar: "AI literacy questionnaire", "ChatGPT usage scale")
- **Socioemocional:** autorrelato de esforço, ansiedade, autoeficácia
- **Sociodemográfico:** idade, sexo, SES, escolaridade dos pais

### Análise
- **Correlação e regressão múltipla** (FE ~ uso de IA, controlando por covariáveis)
- **Análise de mediação:** uso de IA → autoeficácia → FE
- **Análise de moderação:** sexo, idade, SES
- **Equações estruturais (SEM):** modelo integrando todos os constructos
- **Análise qualitativa:** comparação das redações com/sem IA (categorização)

---

## 📅 Cronograma (previsão)

| Mês | Atividade |
|---|---|
| M24 | Revisão de literatura (rápida, tema novo); validação do questionário de uso de IA |
| M25 | Submissão ao CEP |
| M27 | Piloto dos instrumentos (n=20) — ajustes |
| M28 | Coleta principal (dados online + presencial) |
| M30 | Análise estatística (R + lavaan para SEM) |
| M33 | Submissão do paper (revista intl) |
| M36 | Apresentação em congresso (SRCD ou EARLI) |

---

## 🤝 Aspectos críticos

- **Tamanho amostral grande** (N=150–300) é um desafio logístico — considerar parceria com survey nacional (IBGE, INEP)
- **Aspectos éticos extras:** uso de IA generativa em adolescentes levanta questões sobre dependência, vício, impacto na formação crítica → CEP pode pedir mais detalhes
- **Atualização rápida:** a tecnologia muda de 6 em 6 meses — o "ChatGPT" de 2028 pode ser muito diferente; considerar reportar "qual IA foi usada na coleta X" como metadado

---

## 📚 Leitura-base

- Miyake, A. et al. (2000). "The unity and diversity of executive functions" — **OBRIGATÓRIA**
- Diamond, A. (2013). "Executive functions" — **OBRIGATÓRIA**
- Zelazo, P. D. (2020). "Executive function and psychopathopathy"
- Risko, E. F. & Gilbert, S. J. (2016). "Cognitive offloading" — *Trends in Cognitive Sciences*
- Kasneci, E. et al. (2023). "ChatGPT for good?"
- Mollick, E. (2023–2024). "Co-Intelligence" (livro)
- Bai, L. et al. (2024). "Effects of generative AI on learning" (buscar)
- Anthropic / OpenAI white papers (2024–2025) sobre cognitive offloading

Ver bibliografia completa em `00-fundamentos/bibliografia-seminais.md` (seção 🤖).

---

## 📂 Estrutura local

```
04-projeto-ia-generativa-funcoes-executivas/
├── README.md                    ← este arquivo
├── instrumentos/                ← a criar (TCLE, escalas, tarefas computadorizadas)
├── protocolo/                   ← a criar (submissão CEP)
└── analise/                     ← a criar (scripts R/SEM)
```

---

> **Próximo passo:** revisar questionários existentes de uso de IA e adaptar para o contexto brasileiro.
