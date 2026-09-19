# AGENTS.md — Diretório `analise/`

> Instruções para IAs trabalhando na pasta `analise/` (Python, R, Snakemake).
> **Versão:** 1.0 — 2026-09-19

---

## 📂 Estrutura

```
analise/
├── AGENTS.md              ← este arquivo
├── Python/                ← código principal
│   ├── AGENTS.md          ← específico do Python
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── neurociencia_edu/  ← pacote principal
│   ├── notebooks/         ← 12 Jupyter notebooks
│   ├── tests/             ← 159 pytest + 23 unittest
│   ├── dashboard/
│   ├── scripts/           ← osf_submit.py
│   ├── benchmarks/
│   └── resultados/
├── R/                     ← pacote R `neurocienciasedu`
├── Snakemake/             ← pipeline
├── config/                ← YAML configs
├── dados/                 ← dados brutos (NÃO versionar sensíveis)
├── resultados/            ← outputs
└── rules/                 ← Snakemake rules
```

---

## 🚨 Regras ESPECÍFICAS de `analise/`

1. **TDD estrito** — Red → Green → Refactor. Não escrever código de produção sem teste.
2. **Dados sintéticos** ficam em `dados_sinteticos/` (raiz), não em `analise/dados/`
3. **Dados reais** (pós-CEP) em `analise/dados/` — NUNCA versionar
4. **Notebooks** usam imports refatorados: `from neurociencia_edu.stats import fit_rasch` (não de utils antigos)
5. **Linting:** ruff permissivo (`select=["F","E"]` apenas)
6. **CI workflows** são non-blocking (`continue-on-error: true` ou `|| echo`)

---

## 🛠️ Stack técnico

- **Python 3.11** (Streamlit Cloud) + 3.14 (sandbox)
- **Poetry** para deps (pyproject.toml)
- **pytest** + **unittest** para testes
- **ruff** para lint
- **R 4.4** (não 4.3 — underscores em identifiers proibidos)
- **Snakemake** 7+
- **Mamba/Conda** para ambientes

---

## 🎯 Comandos rápidos

```bash
# Rodar todos os testes
cd analise/Python && python3 -m pytest tests/ -q

# Validar schemas
python3 analise/Python/scripts/osf_submit.py --validate

# Submeter OSF (requer OSF_TOKEN)
export OSF_TOKEN="..."
python3 analise/Python/scripts/osf_submit.py --all

# Build docs (Sphinx)
cd docs && make html
```

---

## 🔗 Links

- `AGENTS.md` raiz → visão geral
- `analise/Python/AGENTS.md` → específico Python
- `analise/R/AGENTS.md` → (criar se necessário)

---

**Última atualização:** 2026-09-19
