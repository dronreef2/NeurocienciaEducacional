# Playbook: consolidar-projeto

> **Trigger:** "Consolidar projeto duplicado" / "Resolver duplicação P0X"
> **Domínio:** Conductor + Review + Project-Mgmt
> **Versão:** 1.0 — 2026-09-19

---

## 🚨 REGRA DE OURO

> **A IA NÃO deleta pastas. A IA INVESTIGA e PROPOE. Humano decide.**

Este playbook é para investigar duplicações de pastas de projetos (ex: `02-a/` e `02-b/`) e propor um caminho. **Nenhuma operação destrutiva sem HUMAN GATE explícito.**

---

## 🔄 Fluxo (10 passos)

### 1. DISCOVERY — Inventário das duplicatas

```bash
Para cada pasta candidata:
- Listar todos os arquivos
- Contar linhas / tamanho
- Identificar tipo de conteúdo (protocolo, instrumento, análise, etc.)
- Capturar metadados (última modificação, autor)
```

### 2. COMPARAR DIRETÓRIOS — Estrutura

```bash
diff <(ls -R pasta-A) <(ls -R pasta-B)
# Identificar: arquivos únicos em cada, arquivos em comum
```

### 3. COMPARAR DOCUMENTOS — Conteúdo

```bash
Para arquivos em comum (ex: projeto-detalhado.md):
- diff file-A file-B
- Verificar qual é mais recente / completo / alinhado com o programa atual
```

### 4. COMPARAR REFERÊNCIAS — Quem aponta para cada

```bash
grep -l "pasta-A" --include="*.md" -r .
grep -l "pasta-B" --include="*.md" -r .
# Identificar: AGENTS.md, STATE.yaml, BLUEPRINT.md, ADRs
# Descobrir qual é a canônica "oficial"
```

### 5. COMPARAR CÓDIGO — Pipelines / análises

```bash
grep -l "pasta-A\|pasta-B" analise/ scripts/ dados_sinteticos/
# Identificar: pipelines que usam dados de qual pasta?
```

### 6. IDENTIFICAR ORIGEM — Histórico git

```bash
git log --follow pasta-A/projeto-detalhado.md
git log --follow pasta-B/projeto-detalhado.md
# Identificar: qual foi criada primeiro? por quê?
```

### 7. PROPOR CANONICAL SOURCE

```bash
Output: .agent/reports/consolidation-P0X-AAAA-MM-DD.md

Estrutura:
- Tabela comparativa (A vs B em cada dimensão)
- Recomendação da IA (com justificativa)
- Riscos da operação
- HUMAN GATE: pedir aprovação humana
```

### 8. MERGE/MOVE/ARCHIVE — Executar após aprovação

```bash
# 3 opções (HUMAN escolhe):

# OPÇÃO A: MERGE (combinar conteúdo único)
# - Copiar arquivos únicos de A para B
# - B vira canônica
# - A é arquivada (.archive/2026-XX-XX/)

# OPÇÃO B: ARCHIVE (B é canônica, A vai para arquivo)
# - Mover A para .archive/2026-XX-XX/02-projeto-gamificacao-autorregulacao/
# - Manter em git history
# - Atualizar referências para B

# OPÇÃO C: SPLIT (são projetos diferentes)
# - Renomear A para P0Xa/, B para P0Xb/
# - Atualizar STATE.yaml para refletir 6 projetos
# - Atualizar BLUEPRINT.md
```

### 9. ATUALIZAR STATE — Refletir decisão

```bash
Atualizar STATE.yaml:
- projects: refletir nova estrutura
- maturity: por projeto (renomeado se necessário)
- references_to_archived: lista de arquivos em .archive/
```

### 10. TESTES + ADR

```bash
- pytest tests/ (garantir que nada quebrou)
- ruff check . (lint)
- Atualizar CI workflows se necessário
- Criar ADR-XXX-consolidation-P0X.md com a decisão
```

---

## 📋 Caso de uso atual: P02 e P03 (Cycle 3)

### P02

| Aspecto | autorregulacao/ | funcoes-executivas/ |
|---|---|---|
| Versão projeto-detalhado | v0.1 piloto | **v2.0 (Aguardando CEP)** |
| Tamanho | 173 linhas | **212 linhas** |
| Tem AGENTS.md próprio | ❌ | ✅ |
| Tem README.md | ✅ | ❌ |
| Última modificação projeto | 2026-08-08 | **2026-08-08** |
| Foco | autorregulação | **funções executivas** |
| Alinhado com programa atual | ❌ | ✅ |

**Recomendação da IA (NÃO decisão):** B (archive `autorregulacao/`)

**Justificativa:**
- Mesma data de modificação, mas `funcoes-executivas` é mais recente (v2.0)
- Foco em **FE** está alinhado com programa (linha-mãe da Ângela)
- Tem AGENTS.md próprio (já foi atualizado)
- `autorregulacao/` v0.1 é histórica, vale preservar

**Riscos da operação:**
- Baixo — só move, não deleta
- Estado git preserva histórico
- AGENTS.md raiz referencia a versão correta

### P03

| Aspecto | eeg-leitura/ | eeg-leitura-digital/ |
|---|---|---|
| Versão projeto-detalhado | v0.1 piloto | **v2.0 (Aguardando CEP)** |
| Tamanho | 206 linhas | **231 linhas** |
| Tem AGENTS.md próprio | ❌ | ✅ |
| Tem README.md | ❌ | ✅ |
| Última modificação projeto | 2026-08-08 | **2026-08-08** |
| Foco | EEG leitura | **EEG leitura digital vs papel** |
| Componentes ERP | N170, P300 | **N170, P300, P600** |
| Parceiro ICe | Implícito | **Explícito (Pereira)** |

**Recomendação da IA (NÃO decisão):** B (archive `eeg-leitura/`)

**Justificativa:**
- Mesma evolução que P02 (v0.1 piloto → v2.0)
- Foco em EEG digital vs papel alinhado com programa flagship
- Mais componentes ERP definidos
- Co-orientador ICe explícito

---

## ⚠️ O que NÃO fazer

- ❌ Deletar pasta antiga sem aprovação humana
- ❌ Mesclar conteúdo sem verificar overlaps
- ❌ Atualizar AGENTS.md/STATE.yaml antes da aprovação
- ❌ Fechar issue como "resolvida" sem merge commit + ADR
- ❌ Renomear arquivos sem atualizar todas as referências

---

## 🔗 Links relacionados

- `.agent/reports/program-maturity-2026-09-19.md` (Cycle 2 detectou as duplicações)
- `.agent/decisions/ADR-001-multi-agents-os.md` (precisa de ADR-002 para esta consolidação)
- `AGENTS.md` raiz (referencia estrutura canônica)

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após primeira consolidação aprovada
