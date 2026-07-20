# AGENTS.md — Instruções para IAs trabalhando neste repositório

> Este arquivo segue o padrão **AGENTS.md** reconhecido por Cursor, Claude Code, Aider, Cline, e outros.

Você está em um **programa de pesquisa científica** de 5 projetos (2026–2030) na interseção entre **tecnologia educacional, neurociência cognitiva e desenvolvimento infantil**. A pesquisadora responsável é uma pós-graduada em gestão de projetos, com orientação da Profa. Dra. Ângela Maria Chuvas Naschold (UFRN).

## Estado atual
- **M1 de 60** (mês 1 de um programa de 5 anos)
- **P01** (qualitativo sobre crianças e IA) em fase de estruturação
- **P02–P05** ainda em fase de planejamento
- Estrutura de pastas, cronograma, trilha de formação e instrumentos do P01 já criados
- ✅ Push pro GitHub concluído (`dronreef2/NeurocienciaEducacional`)
- ✅ Reunião com Angela realizada — plano validado
- ✅ Tutor definido: **Khanmigo** (benchmark principal)
- Pendente: escrever `projeto-detalhado.md` para submissão ao CEP/UFRN

## Convenções obrigatórias
- **Idioma**: português brasileiro
- **Commits**: Conventional Commits em PT-BR (`docs:`, `analise:`, `protocolo:`, `instrumento:`, `paper:`, `fix:`, `refactor:`, `chore:`)
- **Nomes de arquivo**: `[NN]-[tipo]-[descrição-curta].md`
- **Tipos**: `roteiro`, `protocolo`, `tcle`, `tale`, `analise`, `rascunho`, `final`
- **Estrutura**: monorepo com pastas `00-fundamentos/`, `01-…` a `05-…`, `docs/`, `.github/`
- **Documentos**: começar com `> **Status:** v0.X — …` quando aplicável
- **Dados sensíveis**: NUNCA versionar (TCLE, áudios, dados brutos). `.gitignore` já trata

## Regras de ouro
1. **Não inventar** dados de escolas, pessoas, ou procedimentos que não existem
2. **Não versionar** dados, TCLEs assinados, ou qualquer coisa com PII
3. **Sempre ler o contexto** (`BLUEPRINT.md`, `00-fundamentos/cronograma-mestre.md`, READMEs dos projetos) antes de criar/modificar algo
4. **Manter coerência** com a linha de pesquisa da orientadora (Leitura + Neurociências)
5. **Em caso de dúvida**: perguntar à pesquisadora, não decidir sozinho

## Comandos úteis
- Próxima tarefa prioritária: escrever `01-projeto-qualitativo-criancas-ia/protocolo/projeto-detalhado.md` para submissão ao CEP/UFRN
- Para subir o repo (SSH já configurado):
  ```bash
  Start-Service ssh-agent
  ssh-add $HOME\.ssh\github_neurociencia
  git push -u origin main
  ```

## Referências
- `BLUEPRINT.md` — contexto completo
- `00-fundamentos/cronograma-mestre.md` — timeline 2026–2030
- `00-fundamentos/bibliografia-seminais.md` — papers-chave
- `01-projeto-qualitativo-criancas-ia/README.md` — projeto em execução
- `docs/ATALHOS-UTEIS.md` — links críticos e contatos
