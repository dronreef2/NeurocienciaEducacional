# 🤖 Arquitetura do AI Project Agent

> **Arquitetura oficial** do agente de IA que trabalha no programa de pesquisa.
> **Versão:** 1.0 — 2026-09-19
> **Status:** ativa, em uso pela Mavis (root session)

---

## 🎯 Visão geral

O **Neurociência Educacional AI Project Agent** é um agente orquestrador que opera em **3 domínios paralelos** (Pesquisa, Engenharia, Gestão), valida tudo por uma **camada de auditoria**, e produz **artefatos reproduzíveis**.

```
                  ┌─────────────────────────────────────┐
                  │   NEUROCIÊNCIA EDUCACIONAL          │
                  │        AI PROJECT AGENT             │
                  │   (root session / conductor)        │
                  └────────────────┬────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
   PESQUISA                  ENGENHARIA                  GESTÃO
   CIENTÍFICA                                          DO PROJETO
        │                          │                          │
        ▼                          ▼                          ▼
   literatura              código / dados            issues / roadmap
   hipóteses               pipelines                 documentação
   metodologia             testes                    status
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   ▼
                         VALIDAÇÃO / AUDITORIA
                                   │
                                   ▼
                       artefato reproduzível
```

---

## 🧠 Camada 0 — Orquestrador (root)

**Função:** recebe pedidos, decide qual(is) sub-agente(s) engatar, valida, entrega.

**Implementação:** `Mavis` (root session) — persona de líder dequipe, fala PT-BR, conhece o programa inteiro.

**Responsabilidades:**
- Audição ativa (entender o que o usuário realmente quer)
- Roteamento entre domínios (Pesquisa / Engenharia / Gestão)
- Validação explícita antes de declarar "pronto"
- Entrega honesta (o que mudou, o que não foi possível)

---

## 🔬 Domínio 1 — PESQUISA CIENTÍFICA

**Função:** gerar conhecimento científico válido (literatura, hipóteses, metodologia).

**Outputs típicos:**
- Protocolo de pesquisa (P01–P05)
- Hipóteses pré-registradas (H1.x, H2.x, ...)
- Análise temática (ATR, Braun & Clarke 2022)
- Manuscritos para journals A1
- Pré-registros OSF
- Notas de leitura de papers

**AGENTS.md relacionados:**
- `00-fundamentos/notas-leitura/AGENTS.md` (a criar)
- `01-.../AGENTS.md` (P01)
- `02-.../AGENTS.md` (P02)
- ...

**Skills / fontes:**
- `superpowers:brainstorming` — explorar intenção
- `superpowers:writing-plans` — plano estruturado
- `deep-research` — pesquisa profunda (5 etapas)

**Restrições:**
- LGPD sempre
- Pré-registro antes da coleta
- Coerência com linha da Ângela (Leitura + Neurociências)

---

## 🛠️ Domínio 2 — ENGENHARIA

**Função:** construir pipelines de dados, código, dashboards, ferramentas.

**Outputs típicos:**
- Pacote Python `neurociencia_edu` (stats, eeg, io, text)
- Pacote R `neurocienciasedu`
- Pipeline Snakemake
- Dashboard Streamlit (8 páginas)
- CLI `neuro` (catalog, validate, cache)
- Testes (159 pytest + 23 unittest)
- Dados sintéticos + catalog YAML
- Documentação Sphinx → GitHub Pages
- PDF reports (reportlab)

**AGENTS.md relacionados:**
- `analise/Python/AGENTS.md`
- `analise/AGENTS.md`
- `pages/AGENTS.md`
- `dados_sinteticos/AGENTS.md`

**Skills / fontes:**
- `senior-fullstack-developer:engineering-workflow` (engine)
- `senior-fullstack-developer:frontend-dev` (UI)
- `senior-fullstack-developer:fullstack-dev` (cross-layer)
- `superpowers:test-driven-development` (TDD)
- `superpowers:verification-before-completion` (validar antes de dizer "ok")

**Restrições:**
- TDD: Red → Green → Refactor
- Ruff: select=["F","E"]
- Path resolution: relativo (funciona local + Streamlit Cloud)
- CI non-blocking (continue-on-error)

---

## 📋 Domínio 3 — GESTÃO DO PROJETO

**Função:** manter roadmap, issues, documentação, status do programa.

**Outputs típicos:**
- ROADMAP-PRATICO.md / ROADMAP-GANTT.md
- Cronograma-mestre.md
- Atas de reunião (Ângela, equipe, parceiros)
- POLITICA-AUTORIA.md (CRediT)
- POLITICA-DADOS.md (LGPD)
- Press releases
- Lattes + ORCID
- Comunicação com stakeholders

**AGENTS.md relacionados:**
- `docs/AGENTS.md`
- `00-fundamentos/cronograma-mestre.md` (com AGENTS.md específico)
- `docs/atas/AGENTS.md` (a criar)

**Skills / fontes:**
- `mavis cron` (lembretes assíncronos)
- Todo lists (todowrite tool)
- `mavis` CLI (management de agent/session/drive/cron)
- `memory_search/read/append` (memória persistente)

**Restrições:**
- Atas podem conter info sensível → LGPD
- Documentos oficiais (POLITICA-*) só com aprovação

---

## ✅ Camada final — VALIDAÇÃO / AUDITORIA

**Função:** garantir que tudo que é entregue é correto, reproduzível, honesto.

**4 tipos de validação:**

### 1. Validação de Schema
- OSF pré-registros: `--validate`
- JSON/YAML válido
- Estrutura de pastas correta

### 2. Validação de Testes
- pytest (159 testes Python)
- unittest (23 testes stdlib)
- R CMD check (quando aplicável)
- CI workflows (12 GitHub Actions)

### 3. Validação Científica
- LGPD compliance
- Pré-registro consistente com coleta
- Coerência com linha de pesquisa
- CRediT (autoria)
- Reproductibilidade (seed=42 em dados sintéticos)

### 4. Validação Honesta
```markdown
## O que mudei
[bullets]

## O que validei
[bullets]

## O que NÃO validei
[bullets]

## Risco residual
[bullets]
```

---

## 📦 Output — Artefato Reproduzível

**Definição:** qualquer entrega que pode ser regenerada de forma idêntica a partir de:
- Código versionado (Git)
- Dados (sintéticos ou reais com TCLE)
- Configs (YAML, TOML)
- Documentação (Markdown)
- Ambiente (Docker / Poetry / Conda)

**Tipos de artefato:**
| Tipo | Exemplo | Reproduzível? |
|---|---|---|
| PDF relatório | `P01_relatorio.pdf` | ✓ (via `pdf_export.py`) |
| Dashboard | `streamlit_app.py` + `pages/` | ✓ (deploy automático) |
| Figura | `figures/P01_*.png` | ✓ (via notebook) |
| Tabela | `resultados/tabela_*.csv` | ✓ (via pipeline) |
| Pré-registro OSF | `P01-osf.json` | ✓ (via `osf_submit.py`) |
| Manuscrito | `P01_manuscrito_v1.md` | Quase (precisa de revisão) |
| Ata | `ata_2026-XX-XX.md` | ✗ (humano-específica) |

---

## 🔄 Fluxo de trabalho típico

```
USER: "Submeter P01 a Computers & Education"
   │
   ▼
[ROOT] Mavis entende:        → mapeia para "GESTÃO + PESQUISA"
   │
   ├──► [GESTÃO] verificar manuscrito + carta de apresentação
   │       └─ output: draft da carta
   │
   ├──► [PESQUISA] revisar coerência científica
   │       └─ output: checklist de submissão
   │
   ├──► [ENGENHARIA] gerar PDF de visualizações
   │       └─ output: figures_300dpi.zip
   │
   ├──► [VALIDAÇÃO] checar LGPD, checklist journal
   │       └─ output: status final
   │
   └──► [ROOT] entrega: carta + figuras + checklist + status
```

---

## 🔀 Mapa de Skills ↔ Domínios

| Skill / Ferramenta | Pesquisa | Engenharia | Gestão |
|---|:---:|:---:|:---:|
| `superpowers:brainstorming` | ✅ | | |
| `superpowers:writing-plans` | ✅ | ✅ | |
| `superpowers:test-driven-development` | | ✅ | |
| `superpowers:verification-before-completion` | ✅ | ✅ | ✅ |
| `superpowers:subagent-driven-development` | | ✅ | |
| `senior-fullstack-developer:engineering-workflow` | | ✅ | |
| `senior-fullstack-developer:frontend-dev` | | ✅ | |
| `senior-fullstack-developer:fullstack-dev` | | ✅ | |
| `app-builder` | | ✅ | |
| `deep-research` | ✅ | | |
| `pdf` (skill) | | ✅ | |
| `pptx` (skill) | ✅ | | ✅ |
| `xlsx` (skill) | | ✅ | |
| `docx` (skill) | ✅ | | ✅ |
| `superdesign:superdesign` | | ✅ | |
| `visual-content-generator` | ✅ | | ✅ |
| `visual-page` | | ✅ | ✅ |
| `mavis` (CLI) | | | ✅ |
| `cron` (mavis) | | | ✅ |
| `memory_*` | ✅ | | ✅ |
| Bash / Read / Write / Edit | | ✅ | |

---

## 📊 Mapa de outputs ↔ Outputs físicos

| Domínio | Output abstrato | Arquivo físico | Tamanho |
|---|---|---|---|
| Pesquisa | Protocolo | `0X-.../protocolo/projeto-detalhado.md` | ~50KB |
| Pesquisa | Pré-registro OSF | `docs/osf-json/P0X-osf.json` | ~3KB |
| Pesquisa | Manuscrito | `docs/manuscritos/P0X_vN.md` | ~30KB |
| Pesquisa | Notas leitura | `00-fundamentos/notas-leitura/*.md` | ~5KB cada |
| Engenharia | Pacote Python | `analise/Python/neurociencia_edu/` | ~50 módulos |
| Engenharia | Testes | `analise/Python/tests/` | 182 testes |
| Engenharia | Dashboard | `streamlit_app.py` + `pages/` | ~50KB |
| Engenharia | Dados sintéticos | `dados_sinteticos/` | ~6 datasets |
| Gestão | ROADMAP | `docs/ROADMAP-PRATICO.md` | ~10KB |
| Gestão | Ata | `docs/atas/AAAA-MM-DD-*.md` | ~3KB cada |
| Gestão | Política | `docs/POLITICA-*.md` | ~5KB cada |
| Validação | CI workflows | `.github/workflows/` | 12 workflows |

---

## 🚀 Como estender esta arquitetura

1. **Novo domínio** → criar AGENTS.md na pasta relevante
2. **Nova skill** → atualizar tabela "Skills ↔ Domínios"
3. **Novo tipo de artefato** → atualizar tabela "Outputs físicos"
4. **Novo fluxo** → adicionar diagrama Mermaid

---

## 🔗 Links relacionados

- `AGENTS.md` (raiz) — visão geral
- `docs/AGENTS-SYSTEM.md` — sistema multi-AGENTS.md
- `AGENT-SKILLS.md` (a criar) — skills por contexto

---

**Última atualização:** 2026-09-19
**Mantido por:** Mavis (root session)
