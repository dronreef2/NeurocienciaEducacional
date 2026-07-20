# 🔗 Atalhos úteis — referências rápidas

> Este é o seu "post-it digital". Mantenha atualizado à medida que o programa avança.

## 📂 Estrutura de pastas — referência rápida

```
/00-fundamentos/         → trilha, cronograma, bibliografia
/01-projeto-qualitativo/ → instrumentos, protocolo, análise
/02-projeto-gamificacao/
/03-projeto-eeg/
/04-projeto-ia-generativa/
/05-projeto-coorte/
/docs/                   → atas, modelos, referências, atalhos
```

**Convenção de nomes de arquivos:**
- `[NN]-[tipo]-[descrição-curta].md`
- Exemplos: `01-roteiro-entrevista.md`, `02-protocolo-thinkaloud.md`, `07-tcle-pais.md`
- Tipos: `roteiro`, `protocolo`, `tcle`, `tale`, `analise`, `rascunho`, `final`

---

## 🌐 Links críticos (acesso diário)

### Pesquisa e publicação
- **Google Scholar**: https://scholar.google.com/
- **Connected Papers**: https://www.connectedpapers.com/
- **Litmaps**: https://www.litmaps.com/
- **ORCID**: https://orcid.org/
- **Lattes**: https://lattes.cnpq.br/
- **ResearchGate**: https://www.researchgate.net/

### Pesquisa no Brasil
- **Plataforma Brasil (CEP)**: https://plataformabrasil.saude.gov.br/
- **CAPES (Qualis)**: https://sucupira.capes.gov.br/
- **FAPERN**: http://www.fapern.rn.gov.br/
- **CNPq**: https://www.gov.br/cnpq/
- **FAPESP** (edital universal): https://fapesp.br/

### Pesquisa internacional
- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/
- **PsycINFO** (acesso via CAPES / Café com Letras)
- **Web of Science** (acesso via CAPES)
- **Scopus** (acesso via CAPES)
- **OpenAlex**: https://openalex.org/ (grátis, alternativo ao WoS)

### Sociedade científica
- **ICOMVE (Mind, Brain, and Education Society)**: https://mbesociety.org/
- **SRCD**: https://www.srcd.org/
- **EARLI**: https://www.earli.org/
- **CBP**: https://www.sbponline.org.br/

### Escrita e referência
- **Zotero** (gerenciador): https://www.zotero.org/
- **Grammarly**: https://www.grammarly.com/
- **DeepL Write** (escrita acadêmica): https://www.deepl.com/write
- **LanguageTool** (PT-BR): https://languagetool.org/pt
- **Overleaf** (LaTeX): https://www.overleaf.com/

### Estatística
- **JASP** (grátis): https://jasp-stats.org/
- **R + RStudio** (grátis): https://posit.co/download/rstudio-desktop/
- **PsychoPy** (grátis): https://www.psychopy.org/

### Análise EEG
- **EEGLAB** (grátis): https://sccn.ucsd.edu/eeglab/
- **ERPLAB** (grátis): https://erpinfo.org/erplab
- **MNE-Python** (grátis): https://mne.tools/
- **FieldTrip** (grátis): https://www.fieldtriptoolbox.org/

### Análise qualitativa
- **Taguette** (grátis, open source): https://www.taguette.org/
- **NVivo trial**: https://lumivero.com/products/nvivo/

### Gestão
- **Notion**: https://www.notion.so/
- **Trello**: https://trello.com/
- **Obsidian**: https://obsidian.md/
- **Google Drive UFRN**: https://drive.google.com/

---

## 📞 Contatos-chave

| Quem | Onde | Papel |
|---|---|---|
| Profa. Ângela Naschold | UFRN/CERES — `angela.naschold@ufrn.br` | Orientadora |
| Instituto do Cérebro (ICe) | UFRN — Natal | Parceiro EEG |
| Secretaria de Educação Ipanguaçu | RN | Escola parceira |
| Secretaria de Educação Currais Novos | RN | Escola parceira |
| PPGED UFRN | https://www.posgraduacao.ufrn.br/ppged | Mestrado |
| Comitê de Ética UFRN | https://cep.ufpe.br/ (exemplo) | Submissão CEP |

---

## 📋 Comandos git úteis

```bash
# Configurar (uma vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Inicializar (uma vez)
cd /seu/repo
git init
git branch -M main
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main

# Workflow diário
git status                                       # ver o que mudou
git add .                                        # adicionar tudo
git commit -m "docs: atualiza cronograma"        # comitar
git push                                         # enviar pro GitHub

# Criar branch para um projeto
git checkout -b 01-qualitativo/instrumentos

# Voltar para main
git checkout main

# Merge
git merge 01-qualitativo/instrumentos
```

### Convenção de commits (Conventional Commits em PT-BR)
- `docs:` documentação
- `analise:` scripts, dados processados, planilhas
- `protocolo:` documentos do CEP, TCLE, TALE
- `instrumento:` roteiros, escalas, questionários
- `paper:` manuscritos
- `fix:` correção
- `refactor:` reorganização sem mudança de conteúdo
- `chore:` tarefas administrativas

**Exemplo:** `instrumento: adiciona roteiro entrevista v0.2 (P01)`

---

## 📅 Cadência de revisão

- **Diário:** revisar issues abertas no GitHub Projects
- **Semanal:** atualizar status no Notion
- **Mensal:** revisar cronograma-mestre.md
- **Trimestral:** reunião presencial com Angela (Caicó ou Natal)
- **Anual:** auto-avaliação do programa (ver `docs/AVALIACAO-ANUAL.md` — a criar)
