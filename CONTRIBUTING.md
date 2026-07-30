# 🤝 Guia de Contribuição

> Obrigado por considerar contribuir com o **Programa de Pesquisa em Neurociência Educacional**! Este documento explica como participar — seja você orientador, colaborador, estudante ou desenvolvedor.

## 📑 Índice

- [Código de Conduta](#código-de-conduta)
- [Como posso contribuir?](#como-posso-contribuir)
- [Fluxo de trabalho](#fluxo-de-trabalho)
- [Padrões de código](#padrões-de-código)
- [Padrões de documentação](#padrões-de-documentação)
- [Commits e PRs](#commits-e-prs)
- [Questões éticas](#questões-éticas)
- [Reportar bugs](#reportar-bugs)
- [Sugerir melhorias](#sugerir-melhorias)

---

## 📜 Código de Conduta

Este projeto segue o [Código de Conduta do Contributor Covenant](https://www.contributor-covenant.org/pt/version/1/4/code-of-conduct/). Ao participar, você concorda em manter um ambiente acolhedor e respeitoso para todos.

**Comportamentos esperados:**
- Linguagem acolhedora e inclusiva
- Respeito por diferentes pontos de vista
- Aceitar crítica construtiva
- Foco no que é melhor para a comunidade

**Comportamentos inaceitáveis:**
- Linguagem ou imagens sexualizadas
- Comentários insultuosos/depreciativos
- Assédio público ou privado
- Publicar informações privadas de terceiros sem permissão

---

## 🎯 Como posso contribuir?

### 1. 🐛 Reportar bugs
Encontrou um erro? Abra uma [issue](../../issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. observado
- Screenshots (se aplicável)
- Ambiente (OS, R/Python version, etc.)

### 2. 💡 Sugerir melhorias
Tem uma ideia? Abra uma issue com:
- Descrição da melhoria
- Motivação (por que é importante?)
- Alternativas consideradas
- Possível implementação (opcional)

### 3. 📚 Melhorar documentação
- Corrigir typos
- Adicionar exemplos
- Traduzir conteúdo (PT/EN)
- Melhorar clareza

### 4. 💻 Contribuir com código
- Resolver issues marcadas como `good first issue`
- Adicionar testes
- Refatorar código
- Adicionar novas funcionalidades

### 5. 📊 Revisar conteúdo científico
- Revisar protocolos
- Sugerir análises
- Validar pré-registros

---

## 🔄 Fluxo de trabalho

### Para mudanças pequenas (typos, pequenos fixes)

1. **Fork** o repositório
2. **Crie uma branch:** `git checkout -b fix/nome-do-fix`
3. **Faça as mudanças**
4. **Teste localmente**
5. **Commit:** `git commit -m "fix: corrige typo no protocolo P01"`
6. **Push:** `git push origin fix/nome-do-fix`
7. **Abra um Pull Request**

### Para mudanças grandes (novos scripts, novos projetos)

1. **Abra uma issue primeiro** para discutir a abordagem
2. Espere feedback da equipe
3. Siga o mesmo fluxo de branch → commit → PR

### Revisão de código
- PRs requerem **pelo menos 1 aprovação**
- CI deve passar (lint + tests)
- Discussão via comentários do PR

---

## 💻 Padrões de código

### R

- **Estilo:** [tidyverse style guide](https://style.tidyverse.org/)
- **Lint:** `lintr::lint_dir("analise/R/")`
- **Formatação:** `styler::style_dir("analise/R/")`
- **Documentação:** roxygen2 (`#'` comments)
- **Testes:** testthat (em `analise/R/tests/`)

```r
# Bom ✅
calcular_media <- function(valores, remover_na = TRUE) {
  if (remover_na) {
    valores <- valores[!is.na(valores)]
  }
  mean(valores)
}

# Ruim ❌
calcMed=function(x,rm=T){
  if(rm)x<-x[!is.na(x)]
  return(mean(x))
}
```

### Python

- **Estilo:** [PEP 8](https://peps.python.org/pep-0008/) + [Google Style](https://google.github.io/styleguide/pyguide.html)
- **Lint:** `ruff check analise/Python/`
- **Formatação:** `ruff format analise/Python/`
- **Type hints:** obrigatórios em funções públicas
- **Docstrings:** Google style
- **Testes:** pytest (em `analise/Python/tests/`)

```python
# Bom ✅
def calcular_media(valores: list[float], remover_na: bool = True) -> float:
    """Calcula a média aritmética de uma lista de valores.

    Args:
        valores: Lista de valores numéricos.
        remover_na: Se True, remove valores NaN antes do cálculo.

    Returns:
        Média aritmética dos valores.

    Raises:
        ValueError: Se a lista estiver vazia após remover NaN.
    """
    valores_limpos = [v for v in valores if not np.isnan(v)] if remover_na else valores
    if not valores_limpos:
        raise ValueError("Lista vazia")
    return sum(valores_limpos) / len(valores_limpos)

# Ruim ❌
def calc(v,rm=True):
  if rm:v=[x for x in v if x==x]
  return sum(v)/len(v)
```

### Markdown

- **Lint:** `markdownlint-cli2`
- **Configuração:** ver `.markdownlint.json` (se existir)
- **Quebras de linha:** 80 colunas (soft wrap)
- **Links:** preferir relativos para arquivos no repo

---

## 📚 Padrões de documentação

### Nomes de arquivos
- Markdown: `NN-tipo-descricao.md` (kebab-case)
- R: `snake_case.R` ou `snake_case.Rmd`
- Python: `snake_case.py`

### Estrutura de documentos

#### Protocolo de pesquisa
```markdown
# [Título do Projeto]

> Resumo executivo (1-2 parágrafos)

## 1. Introdução
## 2. Objetivos
## 3. Métodos
## 4. Análise
## 5. Ética
## 6. Cronograma
## 7. Orçamento
## 8. Limitações
## 9. Referências
```

#### Nota de leitura
```markdown
# [Autor] ([Ano]) - [Título]

## 📋 Metadados
## 📝 Resumo
## 💡 Conceitos-chave
## 🔗 Conexões com o programa
## 📚 Citação
```

### Commits semânticos

Usamos [Conventional Commits](https://www.conventionalcommits.org/) em **português**:

| Prefixo | Uso | Exemplo |
|---|---|---|
| `feat:` | Nova funcionalidade | `feat: adiciona pipeline de AT` |
| `fix:` | Correção de bug | `fix: corrige erro no ICA` |
| `docs:` | Só documentação | `docs: atualiza README` |
| `analise:` | Scripts de análise | `analise: adiciona SEM do P04` |
| `protocolo:` | Protocolos de pesquisa | `protocolo: finaliza P02` |
| `instrumento:` | Instrumentos de coleta | `instrumento: adiciona TCLE` |
| `paper:` | Artigos/manuscritos | `paper: rascunho da introdução` |
| `refactor:` | Refatoração | `refactor: modulariza função` |
| `test:` | Testes | `test: adiciona testes do P04` |
| `chore:` | Tarefas de manutenção | `chore: atualiza deps` |
| `ci:` | CI/CD | `ci: adiciona GitHub Actions` |
| `docker:` | Docker | `docker: configura ambiente` |

**Formato:** `<tipo>: <descrição em português> [BREAKING CHANGE opcional]`

```bash
# Bom ✅
git commit -m "feat: adiciona pipeline de LGCM do P05"
git commit -m "fix: corrige cálculo de TF-IDF quando há 0 ocorrências"
git commit -m "docs: atualiza pré-registro do P02"

# Ruim ❌
git commit -m "stuff"
git commit -m "fix bug"
git commit -m "WIP"
```

---

## 🔬 Questões éticas

Este projeto envolve **pesquisa com seres humanos** (crianças e adultos) e dados sensíveis. Por isso:

### Antes de contribuir com dados
- Certifique-se de que o **CEP aprovou** a pesquisa
- **Anonimize** todos os dados (sem nomes, CPF, endereços)
- Use **IDs numéricos** (C01, C02, ...)
- Documente o **processo de anonimização**

### Para mudanças em instrumentos/protocolos
- Mudanças em TCLE/TALE requerem **reaprovação do CEP**
- Documente a mudança e o motivo
- Adicione a nova versão ao pré-registro

### LGPD
- Respeite a [LGPD](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)
- Veja `docs/POLITICA-DADOS.md`
- Em caso de dúvida, consulte o orientador

---

## 🐛 Reportar bugs

### Template de issue para bug
```markdown
## Descrição
[Descrição clara do bug]

## Como reproduzir
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Comportamento esperado
[O que deveria acontecer]

## Comportamento observado
[O que aconteceu]

## Ambiente
- OS: [e.g. Ubuntu 22.04, Windows 11, macOS 14]
- R: [versão]
- Python: [versão]
- MNE: [versão]
- Dependências relevantes: [versões]

## Screenshots
[Se aplicável]

## Logs
```
[logs aqui]
```

## Severidade
- [ ] Crítico (impede uso)
- [ ] Alto (funcionalidade principal quebrada)
- [ ] Médio (workaround existe)
- [ ] Baixo (cosmético)
```

---

## 💡 Sugerir melhorias

### Template de issue para feature request
```markdown
## Resumo
[Descrição breve]

## Motivação
[Por que é importante? Que problema resolve?]

## Solução proposta
[Como você imagina a implementação?]

## Alternativas consideradas
[Outras opções que você pensou]

## Critérios de aceitação
- [ ] Critério 1
- [ ] Critério 2

## Contexto adicional
[Links, screenshots, etc.]
```

---

## 📞 Contato

- **Issues:** [GitHub Issues](../../issues)
- **Email:** angela.naschold@ufrn.br (orientadora)
- **Discussões:** [GitHub Discussions](../../discussions) (quando ativo)

---

## 🙏 Reconhecimento

Contribuidores serão reconhecidos em:
- `CONTRIBUTORS.md` (gerado automaticamente)
- Seção de agradecimentos em artigos publicados
- Menção em relatórios (quando autorizado pelo participante)

---

## 📚 Referências

- [GitHub: Setting up a project for healthy contributions](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Open Source Guide](https://opensource.guide/)
- [tidyverse style guide](https://style.tidyverse.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Última atualização:** 2026-07-30
**Versão:** 1.0
