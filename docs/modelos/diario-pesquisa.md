# 📓 Diário de Pesquisa — Modelo

> **Propósito:** documentar o dia-a-dia da pesquisa para (a) rastrear decisões, (b) facilitar a escrita, (c) cumprir boas práticas de pesquisa, (d) defesa em caso de auditoria.
> **Convenção:** 1 arquivo por **mês** em `docs/diario-pesquisa/AAAA-MM.md`. Entradas dentro do arquivo organizadas por **dia**.
> **Tempo estimado:** 5–10 min por dia. Não é para ser longo.

---

## 🗂️ Como usar

### Estrutura recomendada

```
docs/diario-pesquisa/
├── README.md                       ← este arquivo
├── 2026-08.md                      ← agosto 2026 (M3)
├── 2026-09.md                      ← setembro 2026 (M4)
├── 2026-10.md                      ← outubro 2026 (M5)
└── ...
```

### Template de entrada diária

```markdown
## [Data — ex: 2026-08-15 (sexta-feira, M3)

### ⏱️ Tempo investido
- Total: Xh
- Distribuição: leitura (Yh) | escrita (Zh) | código (Wh) | reunião (Kh)

### 🎯 O que planejei fazer hoje
- [ ] Item 1
- [ ] Item 2

### ✅ O que realmente fiz
- Item 1 ✓ (nota)
- Item 2 ✓ (nota)
- Item 3 não foi possível porque...

### 💡 Insights / decisões
- Decisão X foi tomada porque Y. Impacto: Z.
- Aprendizado: [link para paper, conversa, observação]

### 🚧 Bloqueios
- [Descrição do bloqueio] — ação: [próximo passo]

### 📅 Próximo dia
- [ ] Item prioritário 1
- [ ] Item prioritário 2
```

---

## 🧠 O que registrar

### ✅ **Sempre registre:**

1. **Decisões importantes** (mesmo pequenas)
   - "Decidi usar MNE 1.5 ao invés de 0.X porque Y"
   - "Mudei o nome do constructo de X para Y porque ficou confuso na revisão"
2. **Mudanças de plano**
   - "Adiei a entrevista com o professor para a semana que vem porque..."
3. **Insights / "eurekas"**
   - "O paper de Singer-Willett sugere que LGCM precisa de pelo menos 3 ondas — isso muda o P05"
4. **Reuniões** (resumo)
   - "Reunião com Angela: definimos que o mestrado vai focar no P02 + P03"
5. **Bloqueios / frustrações**
   - "Estou há 2 dias sem conseguir rodar o ICA. Vou pedir ajuda no fórum MNE."

### ⚠️ **Às vezes registre:**

- **Estado emocional** (breve): "Hoje tava desmotivado, mas..."
- **Conversas informais** com colegas: "Conversei com X sobre Y — pode ser útil para..."
- **Observações** durante coleta de dados

### ❌ **Não registre:**

- Atividades não relacionadas (a menos que afetem o trabalho)
- Reclamações longas
- Conteúdo sigiloso de terceiros sem consentimento

---

## 📋 Templates por tipo de dia

### 📅 Dia comum

```markdown
## 2026-MM-DD

**Tempo:** Xh
**Foco:** [Projeto X]

- Li: [paper X]
- Escrevi: [seção Y]
- Código: [script Z]
- Reunião: [nome + pauta]

**Insight:** [curto]

**Amanhã:** [próxima tarefa]
```

### 🧪 Dia de coleta de dados

```markdown
## 2026-MM-DD — Coleta P03, Escola X, 3ª criança

- **Participante:** C03, 8 anos, menina, 2º ano
- **Consentimento:** OK (TCLE assinado em 2026-MM-DD)
- **Aplicação:**
  - Stroop: 8 min (sem intercorrências)
  - EEG: 25 min (2 trocas de boné, 1 criança ficou agitada)
- **Observações:** C03 pediu para pausar entre blocos. Mãe presente o tempo todo.
- **Dados:** salvos em `dados/raw/P03/C03_2026-MM-DD.vhdr`
- **Notas:** [adicionar arquivo se houver]

**Ajustes para próximos:**
- [ ] Reservar mais 5 min entre blocos (estresse)
- [ ] Levar lanche (criança ficou com fome)
```

### 💬 Dia de reunião

```markdown
## 2026-MM-DD — Reunião com Angela

**Participantes:** [você], Angela, [outros]
**Duração:** 50 min
**Pauta:**
1. Status do P02 (CEP)
2. Pré-registro OSF
3. P03 EEG — questão do equipamento

**Decisões:**
- Submeter o pré-registro até M6 (definir data)
- P03 EEG vai usar o equipamento do ICe (Dr. Antonio cedeu)
- Angela vai apresentar meu projeto no seminário do ICe (data a marcar)

**Pendências:**
- [ ] Eu: finalizar pré-registro
- [ ] Angela: marcar seminário

**Próxima reunião:** 2026-MM-DD
```

### 🐛 Dia de "não saiu nada"

```markdown
## 2026-MM-DD — Dia improdutivo

**O que planejei:** terminar de escrever a seção de métodos do P02
**O que aconteceu:** fiquei 3h travado tentando estruturar o parágrafo sobre amostragem. Não avancei.

**Por quê:** não tinha clareza sobre como justificar o N=200.
**Ação:** marquei uma hora com [colega X] para discutir. Vou ler o paper de [Y] antes.

**Aprendizado:** pedir ajuda antes de ficar travado mais de 1h.

**Amanhã:** ler 2 papers + reunião com X
```

---

## 📊 Revisão semanal (recomendado, 30 min)

Reserve 30 min todo domingo ou segunda de manhã para revisar a semana.

```markdown
## 📊 Revisão da semana 2026-MM-DD a 2026-MM-DD (M3-S2)

**Total investido:** Xh
**Distribuição:** P01 (Yh) | P02 (Zh) | P03 (Wh) | gestão (Kh)

**O que avancei:**
- ✅ Pré-registro do P02 enviado para revisão da Angela
- ✅ Script R de AT testado com dados de exemplo
- ✅ Reunião produtiva com o ICe

**O que NÃO avancei:**
- ❌ Leitura dos 2 papers pendentes
- ❌ Atualização do ROADMAP

**Por que travou:**
- Sobre-carga de trabalho (Xh a mais que planejado)
- Dificuldade em priorizar entre projetos

**Plano para próxima semana:**
- Foco em P02 (submissão CEP dia DD)
- P03 em stand-by até resolução do equipamento
- Ler 1 paper/dia (não 2)

**Nota emocional:** [opcional, breve]
```

---

## 🗓️ Revisão mensal (recomendado, 1h)

Reserve 1h no fim de cada mês para fazer revisão mensal.

```markdown
## 🗓️ Revisão do mês [Nome do mês] (M3)

**Marcos do mês:**
- [Marco principal 1]
- [Marco principal 2]

**Indicadores:**
- Papers lidos: 5 (meta: 4) ✓
- Horas de trabalho: Yh (meta: Zh) ✓/❌
- Reuniões: 3
- Decisões importantes: 2

**O que funcionou:**
- ...

**O que não funcionou:**
- ...

**Ajustes para o próximo mês:**
- ...

**Estado do ROADMAP-PRATICO:**
- [Onde estou vs. onde deveria estar]

**Reflexão sobre o programa como um todo:**
- [Conexões entre projetos que ficaram mais claras]
- [Mudanças de escopo que estou considerando]
```

---

## 🛠️ Ferramentas complementares

| Necessidade | Ferramenta | Quando usar |
|---|---|---|
| Tracking de tarefas | Todoist / Trello / GitHub Issues | Diário, por tarefa |
| Tracking de tempo | Toggl / Clockify | Opcional (recomendado para revisar distribuição) |
| Notas soltas | Obsidian / Logseq | Quando vier uma ideia |
| Backup | Git (commit diário) | Fim do dia |
| Backup em nuvem | Google Drive / OneDrive | Backup semanal |
| Screenshot de decisões | Notion / GitHub | Quando decidir algo polêmico |

> **Recomendação:** mantenha o diário em **Markdown** (não Word) — versionável em Git, pesquisável, exportável.

---

## 📚 Por que diário de pesquisa importa

1. **Defesa em auditoria:** "Por que você mudou o N de 150 para 200?" → Diário responde
2. **Memória institucional:** você vai esquecer. O diário lembra.
3. **Reflexão:** padrões ficam visíveis ("percebo que eu sempre empaco em...")
4. **Produtividade:** força você a planejar e revisar
5. **Publicação:** revisão de literatura fica mais fácil
6. **Ética:** bons princípios de pesquisa (Forscher 2021 sobre Research Integrity)

---

## 📖 Referências sobre diário de pesquisa

- **Forscher et al. (2021).** Research integrity. *Advances in Methods and Practices in Psychological Science.*
- **Stanley et al. (2018).** Meta-Openness. *Advances in Methods and Practices in Psychological Science.*
- **Field (2015).** A Scientist's Guide to Talking with the Media.

---

**Criado:** 2026-07-28
**Última atualização:** 2026-07-28
**Próxima ação:** criar `docs/diario-pesquisa/2026-08.md` quando o M3 começar (Agosto 2026).
