# 🧠 Programa de Pesquisa: Tecnologia, Cérebro e Desenvolvimento Infantil

> Repositório-mestre do programa de pesquisa de 5 projetos (2026–2030) na interseção entre **Tecnologia Educacional**, **Neurociência Cognitiva** e **Desenvolvimento Infantil**, conduzido em parceria com a Profa. Dra.  e o Instituto 

---

## 🎯 Visão do programa

Investigar, em uma série coordenada de 5 estudos, como diferentes tecnologias educacionais (tutores de IA generativa, gamificação, leitura digital, assistentes de escrita com IA) moldam o desenvolvimento cognitivo, atencional e metacognitivo de crianças entre 5 e 12 anos — e como o cérebro responde a essas tecnologias em janelas desenvolvimentais críticas.

**Linha de pesquisa ancorada em:** *Leitura + Neurociências* (RedLeitura ), sob coordenação da Profa. 

---

## 📦 Os 5 projetos (visão integrada)

| # | Projeto | Tipo | Período | Dificuldade | Paper-alvo principal |
|---|---|---|---|---|---|
| 01 | Vozes das crianças sobre tutores de IA | Qualitativo | 6–9 m | 🟢 | *Computers & Education* |
| 02 | Gamificação e autorregulação em matemática | Experimental | 9–12 m | 🟡 | *Learning and Instruction* |
| 03 | EEG de leitura digital vs. papel | Experimental + neuro | 12–18 m | 🟠 | *Developmental Cognitive Neuroscience* |
| 04 | IA generativa × funções executivas | Transversal correlacional | 10–14 m | 🟠 | *Computers in Human Behavior* |
| 05 | Coorte longitudinal com EEG | Longitudinal + neuro | 5+ anos | 🔴 | *Developmental Science* |

---

## 🗂️ Estrutura do repositório

```
.
├── 00-fundamentos/                  # Trilha formativa e bibliografia unificada
│   ├── bibliografia-seminais.md
│   ├── trilha-formacao.md
│   └── cronograma-mestre.md
├── 01-projeto-qualitativo-criancas-ia/
├── 02-projeto-gamificacao-autorregulacao/
├── 03-projeto-eeg-leitura-digital/
├── 04-projeto-ia-generativa-funcoes-executivas/
├── 05-projeto-coorte-longitudinal/
├── docs/                            # Atas, modelos, referências cruzadas
└── .github/                         # Templates de issue, workflows
```

Cada pasta de projeto segue o padrão: `instrumentos/` (TCLE, TALE, escalas), `protocolo/` (submissão CEP), `analise/` (scripts R/Python, planilhas), `dados/` (NÃO versionado — ver `.gitignore`).

---

## 🚀 Como usar este repositório

1. **Kanban central** (GitHub Projects): `Backlog → Em curso → Aguardando revisão → Concluído`
2. **Issues por projeto** com labels: `projeto-01`, `projeto-02`, ..., `fundamentos`, `cep`, `paper`, `congresso`
3. **Branches por projeto**: `main`, `01-qualitativo/*`, `02-gamificacao/*`, etc.
4. **Tags para versões de manuscrito**: `v0.1-rascunho`, `v1.0-submissao-cep`, `v2.0-submissao-journal`
5. **Conventional Commits** em PT-BR: `docs:`, `analise:`, `protocolo:`, `dados:`

---

## 📚 Como citar

> [Seu nome]. (2026). *Programa de Pesquisa: Tecnologia, Cérebro e Desenvolvimento Infantil* (v0.1). GitHub. https://github.com/[seu-usuario]/[nome-repo]

---

## 📜 Licença

- **Código** (scripts, pipelines): MIT — ver `LICENSE`
- **Documentos e manuscritos** (`.md` e `.tex`): CC BY 4.0
- **Dados**: não versionados por padrão (privacidade e ética); ver política em `docs/POLITICA-DADOS.md` (a criar)

---

## 🤝 Contato

- Pesquisadora: [Seu nome]
- Orientadora: Profa. Dra. Ângela Maria Chuvas Naschold — `angela.naschold@ufrn.br`
- Linha de pesquisa: RedLeitura / Leitura + Neurociências (UFRN)
- Laboratório parceiro: Instituto do Cérebro da UFRN (ICe)
