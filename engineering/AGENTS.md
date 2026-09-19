# 🛠️ engineering/AGENTS.md — Engineering Agent

> **Agente especializado** em engenharia de software e dados.
> **Domínio:** Engineering
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Quem é

O **Engineering Agent** constrói pipelines de dados, código, dashboards, e ferramentas:

- Código Python (pacote `neurociencia_edu`)
- Código R (pacote `neurocienciasedu`)
- Pipelines (Snakemake)
- Dashboard (Streamlit)
- Testes (pytest + unittest)
- CI/CD (12 GitHub Actions)
- Infra (Docker, Docker Compose)

**Quem decide:** IA para decisões técnicas delegadas, humano para mudanças arquiteturais grandes (registrar em ADR).

---

## 📂 Saídas (outputs físicos)

| Output | Pasta | Quem valida |
|---|---|---|
| Pacote Python | `analise/Python/neurociencia_edu/` | pytest (182 testes) |
| Pacote R | `analise/R/` | R CMD check |
| Notebook | `analise/Python/notebooks/` | Smoke test |
| Teste | `analise/Python/tests/` | pytest |
| Dashboard page | `pages/` | Streamlit deploy |
| Dados sintéticos | `dados_sinteticos/` | Schema + LGPD |
| Script | `analise/Python/scripts/` | Smoke test |
| CI workflow | `.github/workflows/` | GitHub Actions |

---

## 🛠️ Skills

- `senior-fullstack-developer:engineering-workflow` (engine)
- `senior-fullstack-developer:frontend-dev` (UI)
- `senior-fullstack-developer:fullstack-dev` (cross-layer)
- `superpowers:test-driven-development` (TDD)
- `superpowers:verification-before-completion` (validar antes de "pronto")

---

## 📐 Stack técnico

| Camada | Ferramenta |
|---|---|
| Linguagem | Python 3.11 (Streamlit Cloud) + R 4.4 |
| Deps | Poetry + pip (extras: eeg, bayesian, dashboard, docs, all) |
| Testes | pytest + unittest stdlib |
| Lint | ruff (permissivo: select=["F","E"]) |
| Pipeline | Snakemake |
| Container | Docker + docker-compose |
| Dashboard | Streamlit + reportlab |
| Docs | Sphinx + Quarto + Mermaid |
| CI | GitHub Actions (12 workflows) |

---

## 🚨 Regras ESPECÍFICAS

1. **TDD: Red → Green → Refactor** — não escrever código de produção sem teste
2. **Path resolution:** SEMPRE `Path(__file__).resolve().parent.parent / "..."` (relativo)
3. **Matplotlib colorbar:** `fig.colorbar(im, ax=axes, ...)` (compartilhado)
4. **R 4.4:** identificadores **NÃO** podem começar com `_` (use `helper_xxx`)
5. **Dados sintéticos:** `np.random.seed(42)` para reprodutibilidade
6. **CI non-blocking** (atual): `continue-on-error: true` ou `|| echo`
7. **Type hints** obrigatórios em funções públicas
8. **Docstrings** Google style

---

## 📋 Workflow típico

### Adicionar nova função ao pacote

```bash
1. Escrever teste primeiro (RED)
   tests/test_X.py::test_Y
2. Implementar função (GREEN)
   neurociencia_edu/modulo/X.py
3. Refatorar (REFACTOR)
4. pytest tests/test_X.py -v
5. ruff check neurociencia_edu/modulo/X.py
6. Commit: "feat(modulo): adicionar X para Y"
```

### Corrigir bug no dashboard

```bash
→ USAR PLAYBOOK: .agent/playbooks/bug-dashboard.md
```

### Deploy de nova feature

```bash
1. TDD (testes primeiro)
2. Code review (ler própria PR)
3. CI verde (pytest + ruff)
4. Update docs (API-REFERENCE.md se API pública)
5. Commit + push
6. Streamlit Cloud auto-deploy
```

---

## 🔗 Sub-agentes / Tools

- `task` (sub-agent general) — para refactorings longos
- `bash` (run tests, lint)
- `read/write/edit` (código)
- `grep/glob` (buscar)

---

## 🔗 Links

- AGENTS.md raiz (Conductor)
- `analise/Python/AGENTS.md` (Python specifics)
- `pages/AGENTS.md` (Streamlit)
- `dados_sinteticos/AGENTS.md`
- `.agent/playbooks/bug-dashboard.md`

---

**Última atualização:** 2026-09-19
