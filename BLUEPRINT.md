# 🧠 BLUEPRINT — Programa de Pesquisa: Tecnologia, Cérebro e Desenvolvimento Infantil

> **Documento de contexto para IAs e humanos.** Cole este arquivo no início de qualquer conversa com um assistente de IA (Cursor, Claude Code, GitHub Copilot, Cline, Aider, etc.) e peça para continuar o trabalho a partir do estado atual.

---

## 1. TL;DR (30 segundos)

Pesquisadora pós-graduada em **gestão de projetos**, com acesso a **bolsista de produtividade da UFRN (Profa. Dra. Ângela Maria Chuvas Naschold)** e ao **Instituto do Cérebro da UFRN (ICe)**, está montando um programa de **5 projetos de pesquisa** (2026–2030) na interseção entre **tecnologia educacional, neurociência cognitiva e desenvolvimento infantil**. O programa está em fase de **estruturação** (M1 de 60): pasta criada, instrumentos do P01 prontos, cronograma definido, mas o **primeiro push pro GitHub ainda não foi feito**.

**Próximo passo concreto:** escrever o `projeto-detalhado.md` para submissão ao CEP/UFRN via Plataforma Brasil.

---

## 2. A pesquisadora — perfil e contexto

| Item | Valor |
|---|---|
| Formação | Graduada (Neuro/educação/psi), pós em **gestão de projetos** |
| Estado atual | Pós-graduada, sem vínculo institucional fixo, com horas livres |
| Objetivo | Tornar-se pesquisadora em neurociência educacional; **pretende fazer mestrado → doutorado** (provavelmente na UFRN, sob orientação da Angela) |
| Trunfo secreto | A pós em gestão de projetos dá a ela capacidade de **gerenciar 5 projetos em paralelo** com cronograma, escopo e risco bem definidos |
| Idiomas | Português (nativo) |
| Localização | Brasil (sugestão: provavelmente Natal/RN, dado o vínculo com UFRN) |

---

## 3. Linha-mãe: Leitura + Neurociências (UFRN)

**Profa. Dra. Ângela Maria Chuvas Naschold** — Professora Associada do Departamento de Educação (DEDUC) do **CERES/UFRN** (Caicó/RN) e **colaboradora do Instituto do Cérebro da UFRN (ICe)**.

- Coordena o **Projeto Leitura + Neurociências** (convênio UFRN/MEC, desde 2012)
- Coordena o **Grupo RedLeitura** (CNPq)
- Coordena curso de especialização "Leitura + Neurociências: Interfaces na Educação Integral"
- Tem **parceria institucional com o ICe** (acesso a EEG) e com **escolas municipais do RN** (Ipanguaçu, Currais Novos — cerca de 900 crianças em programas de alfabetização)
- Mais de 10 anos de pesquisa em alfabetização + neurociência
- **Esta pesquisadora é a orientadora ideal** para o programa: tem linha consolidada, acesso a EEG, escolas parceiras, e-mail institucional

**Contato:** `angela.naschold@ufrn.br`

---

## 4. Os 5 projetos (escada de viabilidade)

| # | Projeto | Tipo | Período | Paper-alvo |
|---|---|---|---|---|
| 01 | **Vozes das crianças sobre tutores de IA generativa** | Qualitativo (entrevistas, think-aloud, desenhos projetivos, diário) | M1–M9 | *Computers & Education* |
| 02 | **Gamificação e autorregulação em matemática** | Experimental (2×2, app prototipado, ~100 crianças) | M6–M18 | *Learning and Instruction* |
| 03 | **EEG de leitura digital vs. papel** | Experimental + neuro (crianças 8–10, EEG ICe) | M12–M30 | *Developmental Cognitive Neuroscience* |
| 04 | **IA generativa × funções executivas em adolescentes** | Transversal correlacional (N-back, Stroop, TTCT, ~150–300) | M24–M36 | *Computers in Human Behavior* |
| 05 | **Coorte longitudinal com EEG** | Longitudinal (5 ondas anuais, 100+ crianças) | M30+ | *Developmental Science* |

**Sequência:** P01 → P02 → P03 (flagship) → P04 → P05 (em paralelo). Cada projeto gera ≥1 paper. Em 4 anos, **5 papers + portfólio pronto para mestrado**.

---

## 5. Estado atual do programa

### ✅ Pronto
- README-mestre do programa (`README.md`)
- Cronograma-mestre 2026–2030 (`00-fundamentos/cronograma-mestre.md`)
- Trilha de formação resumida (`00-fundamentos/trilha-formacao.md`)
- Bibliografia seminal categorizada (`00-fundamentos/bibliografia-seminais.md`)
- Atalhos úteis (`docs/ATALHOS-UTEIS.md`)
- Templates de issue do GitHub
- Workflow de lint de markdown
- LICENSE (MIT para código, CC BY 4.0 para docs)
- `.gitignore` robusto
- **P01 — README do projeto, roteiro de entrevista (4 blocos), TCLE para pais, TALE para crianças (linguagem acessível), checklist do CEP**
- ✅ **Push pro GitHub concluído** — repo `dronreef2/NeurocienciaEducacional` *(2026-07-20)*
- ✅ **Reunião com Angela realizada** — plano de 4 anos validado *(2026-07-20)*
- ✅ **Tutor de IA definido** — Khanmigo (Khan Academy/Microsoft) como benchmark principal *(2026-07-20)*

### ❌ Pendente (próximos alvos)
- **P01 — protocolo detalhado** para submissão ao CEP/UFRN
- **P01 — questionário para pais e professores**, **protocolo de think-aloud**, **template de diário**
- **READMEs iniciais** de P02, P03, P04, P05
- **Documentos institucionais**: ata de reunião, política de dados, avaliação anual
- **Template de manuscrito** (IMRaD)
- **Notas de leitura** dos papers seminais
- **Confirmar critérios do CEP/UFRN** para pesquisa com IA e crianças
- **Negociar escola parceira** (candidatas: Ipanguaçu, Currais Novos, Natal)

---

## 6. Convenções do projeto

### Estrutura de pastas (monorepo)
```
programa-pesquisa/
├── 00-fundamentos/                # trilha, cronograma, bibliografia unificada
├── 01-projeto-qualitativo-criancas-ia/
│   ├── README.md
│   ├── instrumentos/              # roteiros, escalas, TCLE, TALE
│   ├── protocolo/                 # submissão CEP
│   └── analise/                   # scripts, planilhas
├── 02-projeto-gamificacao-autorregulacao/   (mesma estrutura)
├── 03-projeto-eeg-leitura-digital/          (com pasta scripts/)
├── 04-projeto-ia-generativa-funcoes-executivas/  (mesma estrutura)
├── 05-projeto-coorte-longitudinal/          (mesma estrutura)
├── docs/                          # atas, modelos, referências cruzadas
└── .github/                       # templates de issue, workflows
```

### Convenção de nomes
- `[NN]-[tipo]-[descrição-curta].md`
- Tipos: `roteiro`, `protocolo`, `tcle`, `tale`, `analise`, `rascunho`, `final`
- Exemplo: `01-roteiro-entrevista.md`, `07-tcle-pais.md`

### Convenção de commits (PT-BR, Conventional Commits)
- `docs:` documentação
- `analise:` scripts, dados processados
- `protocolo:` documentos do CEP
- `instrumento:` roteiros, escalas
- `paper:` manuscritos
- `fix:` correção
- `refactor:` reorganização
- `chore:` tarefas administrativas

### Padrão de documentos
- Idioma: **português brasileiro**
- Markdown com títulos hierárquicos claros (##, ###)
- Listas curtas, com checkboxes quando aplicável
- Links em formato relativo (`./00-fundamentos/...`)
- Toda referência a paper: `(autor, ano)` no texto + link Scholar no final
- Todo instrumento: incluir `> **Status:** v0.X — ...` no topo

---

## 7. Stack técnico (já decidida)

| Categoria | Ferramenta | Custo |
|---|---|---|
| Repositório | GitHub (privado inicialmente) | Grátis |
| Editor recomendado | **Cursor** (com Claude/GPT-4) — ou VS Code + Copilot | Freemium |
| Referências | Zotero + Better BibTeX | Grátis |
| Escrita acadêmica | Overleaf (LaTeX) ou Markdown+pandoc | Grátis |
| Análise qualitativa | Taguette → NVivo (trial) | Grátis |
| Análise estatística | JASP (inicial) → R/RStudio (avançado) | Grátis |
| Análise EEG | EEGLAB+ERPLAB ou MNE-Python | Grátis |
| Experimentação | PsychoPy (P02) | Grátis |
| Gestão | Notion ou Obsidian (segundo cérebro) | Freemium |
| Kanban | GitHub Projects | Grátis |
| Áudio (transcrição) | Whisper local (whisper.cpp) ou Otter.ai | Grátis/pago |

---

## 8. Próximos passos concretos (executar em ordem)

### Imediato (esta semana)
1. ~~**Push pro GitHub via SSH**~~ ✅ *(concluído em 2026-07-20 — repo `dronreef2/NeurocienciaEducacional`)*
2. ~~**Reunião com a Angela**~~ ✅ *(realizada — plano de 4 anos validado)*
3. **Comprar/baixar 2 livros prioritários**: Dehaene (2010) *Reading in the Brain* + Luck (2014) *An Introduction to the ERP Technique*

### Curto prazo (M1–M3)
4. **P01 — `projeto-detalhado.md`** para submissão ao CEP/UFRN (Plataforma Brasil)
5. **P01 — questionário para pais** + **questionário para professores** + **protocolo de think-aloud** + **template de diário**
6. **READMEs de P02, P03, P04, P05** (análogos ao do P01)
7. **Cadastrar ORCID** e atualizar Lattes
8. **Tornar-se membro estudante da ICOMVE** (US$ 50/ano)

### Médio prazo (M3–M12)
9. Submissão do P01 ao CEP
10. Carta de anuência das escolas (Ipanguaçu, Currais Novos) — via Angela
11. Piloto do P01 (n=3 crianças)
12. Coleta formal do P01
13. Análise temática (Braun & Clarke)
14. Submissão do P01 a revista brasileira (Qualis A1–A2)
15. Aplicar para o mestrado PPGED/UFRN (edital outubro/novembro)

---

## 9. Pessoas-chave e contatos

| Quem | Onde | Papel |
|---|---|---|
| **Profa. Ângela Naschold** | UFRN/CERES — `angela.naschold@ufrn.br` | Orientadora |
| Instituto do Cérebro (ICe) | UFRN — Natal | Parceiro EEG |
| Secretaria de Educação Ipanguaçu | RN | Escola parceira (P01) |
| Secretaria de Educação Currais Novos | RN | Escola parceira (P01) |
| PPGED UFRN | https://www.posgraduacao.ufrn.br/ppged | Mestrado em Educação |
| Comitê de Ética UFRN | https://www.ufrn.br/comitedeetica/ | Submissão CEP |
| ICOMVE | https://mbesociety.org/ | Mind, Brain, and Education Society |

---

## 10. Referências bibliográficas fundacionais (núcleo)

- Dehaene, S. (2010). *Reading in the Brain*. Penguin.
- Luck, S. J. (2014). *An Introduction to the Event-Related Potential Technique* (2nd ed.). MIT Press.
- Braun, V. & Clarke, V. (2022). *Thematic Analysis: A Practical Guide*. SAGE.
- Diamond, A. (2013). Executive functions. *Annual Review of Psychology*, 64, 135–168.
- Miyake, A. et al. (2000). The unity and diversity of executive functions. *Cognitive Psychology*, 41, 49–100.
- Howard-Jones, P. (2014). *Neurociência e Educação*. Artmed. **(em PT-BR)**
- Hamari, J. et al. (2014). Does gamification work? A systematic review. *Journal of Educational Technology & Society*.
- **Naschold, A. (2017).** *Projeto Leitura + Neurociências*. Edufrn. **(PRIORIDADE — específico da orientadora)**

---

## 11. ⚠️ Armadilhas conhecidas (NÃO COMETER)

1. **Não versionar dados brutos** — `.gitignore` já exclui `.csv`, `.xlsx`, `.set`, `.edf`, `.fdt` etc. Manter assim.
2. **Não colar PAT/SSH key em arquivos** — usar sempre em variável de ambiente ou via SSH.
3. **Não usar `git remote add` com PAT na URL** — vaza credencial em `.git/config`. Preferir SSH.
4. **Não submeter ao CEP sem TCLE + TALE + carta de anuência** — checklist em `01-projeto-qualitativo-criancas-ia/protocolo/checklist-cep.md`.
5. **Não chamar o P01 de "pesquisa com IA" sem especificar qual tutor** — fixar a plataforma antes da coleta.
6. **Não pular o piloto** (n=3) antes da coleta formal.
7. **Não publicar em revista predatory** — verificar no **Qualis/CAPES** + **Beall's List** (negativa) + **DOAJ** (positiva).
8. **Não confundir "Leitura + Neurociências" (linha) com "Neurociência da leitura" (campo)** — a primeira é específica da Angela.

---

## 12. Como continuar de onde parou (instrução para próxima IA)

Se você é uma IA lendo este blueprint em uma IDE (Cursor, Claude Code, Copilot, etc.), siga esta sequência:

1. **Leia este BLUEPRINT.md inteiro** — ele é o estado atual do programa.
2. **Leia o `00-fundamentos/cronograma-mestre.md`** — para entender o timeline.
3. **Leia o `01-projeto-qualitativo-criancas-ia/README.md`** — é o projeto em execução.
4. **Tarefas pendentes estão em §8 acima** — comece pelo passo 1 (push via SSH) ou 4 (projeto-detalhado), conforme prioridade do usuário.
5. **Convenção**: português brasileiro, Conventional Commits em PT-BR, estrutura de pastas fixa, nomes `[NN]-[tipo]-[desc].md`.
6. **Em caso de dúvida**: pergunte ao usuário, **não invente**. Especialmente sobre o tutor de IA específico do P01, o cronograma exato, ou a escola parceira.
7. **Para contexto expandido**: cada `README.md` de projeto contém pergunta de pesquisa, metodologia, cronograma e contribuição esperada.

**Status atual do programa:** M1 (mês 1) de 60. P01 em fase de estruturação/protocolo.

---

> **Última atualização:** 2026-07-20 (push GitHub + decisões Khanmigo/Angela)
> **Versão do blueprint:** 0.2
> **Próxima revisão:** mensal
