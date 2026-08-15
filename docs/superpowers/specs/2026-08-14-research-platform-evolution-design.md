# Design: Evolução da Plataforma de Pesquisa em Neurociência Educacional

**Data:** 2026-08-14
**Status:** Rascunho aguardando revisão
**Autor:** Mavis (assistente de IA) + usuário
**Versão:** 1.0

---

## 1. Resumo Executivo

Este design descreve a evolução da plataforma de pesquisa em **três fases
sequenciais e bounded** (A → B → C), cada uma adicionando capacidades
específicas sem alterar a arquitetura fundamental do monorepo.

**Fase A — Productionize Notebooks** (Sessões 1-3)
**Fase B — Data Pipeline & Versioning** (Sessões 4-6)
**Fase C — Interactive Research Dashboard** (Sessões 7-9)

**Tempo total estimado:** 9-12 sessões
**Resultado:** Plataforma pronta para execução real do programa de 5 projetos.

---

## 2. Contexto e Justificativa

### 2.1. Estado atual (verificado em 2026-08-14)

| Métrica | Valor |
|---|---|
| Commits | 84 (v1.0.0 tagged) |
| Arquivos | 494 |
| Linhas Python + R | 16,348 |
| Notebooks | 15 (não CI-testados) |
| Testes | 70 passing, 13 skip |
| Workflows CI/CD | 11 |
| Pré-registros OSF | 5/5 |
| Manuscritos | 6 drafts |
| Dashboards | 5 (vários níveis de maturidade) |
| Documentação | 30+ arquivos |

### 2.2. Pontos fracos identificados

1. **Notebooks não são CI-tested** — bugs em produção, resultados não verificados
2. **Código de notebooks é descartável** — mesma função reescrita várias vezes
3. **Sem caching de análises** — re-roda tudo do zero a cada execução
4. **Sem versionamento de dados** — impossível rastrear "qual dataset gerou qual resultado"
5. **Dashboard root é minimal** — `streamlit_app.py` (2 KB) vs `dashboard_piloto.py` (20 KB)
6. **Sem CLI tool** — operações manuais no terminal
7. **i18n só em recrutamento** — manuscritos só em PT
8. **Notebooks sem progresso** — sem tqdm em loops longos
9. **Sem data catalog** — difícil encontrar "qual dataset para P04?"

### 2.3. Restrições

- **Não mudar arquitetura:** Monorepo atual é sólido; preservá-lo.
- **LGPD compliance:** Manter anonimização em todas as transformações.
- **Reprodutibilidade:** Toda análise deve poder ser re-executada com mesmos inputs.
- **Bounded context:** Cada fase é independente e entregável.
- **Custo zero de cloud:** Tudo roda em CI GitHub Actions (free tier) e Streamlit Cloud.

---

## 3. Arquitetura-Alvo

### 3.1. Diagrama de componentes

```
┌────────────────────────────────────────────────────────────────────┐
│                  neurociencia_edu (pacote)                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐         │
│  │  stats/     │   eeg/      │   text/     │  cli.py     │  ← NOVO │
│  │  (refact)   │  (refact)   │  (existente)│  (Fase B)   │         │
│  ├─────────────┼─────────────┼─────────────┼─────────────┤         │
│  │  config.py  │ exceptions  │ validators  │ cache.py    │  ← NOVO │
│  │  (existente)│  (existente)│  (existente)│  (Fase B)   │         │
│  └─────────────┴─────────────┴─────────────┴─────────────┘         │
└────────────────────────────────────────────────────────────────────┘
        ▲                  ▲                  ▲
        │                  │                  │
┌───────┴──────┐  ┌────────┴────────┐  ┌─────┴──────────┐
│  Notebooks   │  │  CLI tool       │  │   Dashboard    │
│  (CI-tested) │  │  (Fase B)       │  │   (Fase C)     │
│  + Papermill │  │  neuro <cmd>    │  │   Streamlit    │
└──────────────┘  └─────────────────┘  │   multi-page   │
                                      └────────────────┘
        ▲                  ▲                  ▲
        │                  │                  │
┌───────┴──────────────────┴──────────────────┴─────────────┐
│              Dados (DVC-tracked)                            │
│  dados_sinteticos/P0X_*.csv + .npy                        │
│  + .dvc/ (metadata, versionamento)         ← NOVO Fase B   │
│  + catalog.yaml (data catalog)             ← NOVO Fase B   │
└──────────────────────────────────────────────────────────┘
```

### 3.2. Princípios arquiteturais (preservados)

1. **Config centralizada** — `config.py` singleton
2. **Logging padronizado** — `logging_config.py`
3. **Exceções tipadas** — `exceptions.py`
4. **Validação rigorosa** — `validators.py` com LGPD
5. **Imutabilidade** — dataclasses frozen
6. **Reprodutibilidade** — `random_state=42` em tudo

### 3.3. Princípios adicionados (novos)

7. **Reusabilidade de código** — Notebooks são discovery, package é produção
8. **Versionamento de dados** — DVC + `.dvc/`
9. **Cache determinístico** — hash de inputs/outputs
10. **Interface CLI padronizada** — argparse-based

---

## 4. FASE A — Productionize Notebooks (Sessões 1-3)

### 4.1. Objetivo
Garantir que **todos os 15 notebooks** rodem em CI sem erro e que código
estável migre para o pacote `neurociencia_edu/`.

### 4.2. Entregas

**A.1 — CI de notebooks com Papermill**
- Adicionar `papermill` e `pytest-notebook` como dependências dev
- Criar `.github/workflows/notebooks.yml` que executa todos os 15 notebooks
- Tempo limite: 10 min por notebook, 60 min total
- Modo `continue-on-error: true` para warnings não-bloqueantes

**A.2 — Refactor de funções estáveis**
Migrar para o pacote:

| Função | Origem | Destino |
|---|---|---|
| `mann_kendall(x)` | notebooks/15 | `neurociencia_edu/stats/_trends.py` |
| `convert_numpy(obj)` | scripts/analise_piloto_real | `neurociencia_edu/io/_serializers.py` |
| `power_analysis()` | notebooks/08 | `neurociencia_edu/stats/_power.py` |
| `fit_rasch()` | notebooks/09 | `neurociencia_edu/stats/_irt.py` |
| `kaplan_meier()` | notebooks/12 | `neurociencia_edu/stats/_survival.py` |
| `preprocess_eeg()` | notebooks/02 | `neurociencia_edu/eeg/_preprocess.py` |
| `compute_erp()` | notebooks/02 | `neurociencia_edu/eeg/_erp.py` |
| `analyze_sentiment()` | scripts/sentiment_network | `neurociencia_edu/text/_sentiment.py` |
| `co_occurrence_network()` | scripts/sentiment_network | `neurociencia_edu/text/_network.py` |

Cada função migrada recebe:
- Type hints completos
- Docstring (Google style)
- Teste em `tests/test_<module>.py`
- Logging via `get_logger(__name__)`
- Error handling via exceções customizadas

**A.3 — Vectorização + tqdm**
- Notebooks 11 (EEG) e 09 (IRT): vectorizar loops com NumPy
- Adicionar `tqdm` em loops longos
- Adicionar `time` para logging de performance

**A.4 — Testes de notebooks**
- Fixture pytest que executa notebook com papermill
- Verifica que `outputs/` contém figuras/JSONs esperados
- Threshold: ~70% dos notebooks rodam sem erro

### 4.3. Critérios de aceitação (Fase A)

- [ ] Todos os 15 notebooks têm ao menos 1 assertion/print final
- [ ] CI executa notebooks em <60 min
- [ ] 9 funções refatoradas + testadas
- [ ] Cobertura de testes ≥ 85% nos módulos refatorados
- [ ] Notebooks 11 e 09 vectorizados (3-5x speedup)

### 4.4. Riscos e mitigações (Fase A)

| Risco | Mitigação |
|---|---|
| Papermill falha em alguns notebooks | Marcar com `continue-on-error: true` |
| Refactor quebra notebooks existentes | Manter fallback de compatibilidade |
| Vectorização introduz bugs | Comparar output antes/depois |

---

## 5. FASE B — Data Pipeline & Versioning (Sessões 4-6)

### 5.1. Objetivo
Versionar datasets, criar CLI tool, e adicionar cache inteligente de análises.

### 5.2. Entregas

**B.1 — DVC para versionamento de dados**
- Adicionar `dvc` como dependência
- Inicializar `dvc init` no repositório
- Configurar remote (S3 ou local para dev)
- Tracking: `dados_sinteticos/*.csv` e `dados_sinteticos/*.npy`
- Git LFS alternativo se S3 não disponível

**B.2 — Data catalog (`catalog.yaml`)**
```yaml
datasets:
  P01_diarios_sinteticos:
    path: dados_sinteticos/P01_diarios_sinteticos.csv
    projeto: P01
    tipo: csv
    n_rows: 255  # 15 × 17
    columns: [crianca_id, dia, mtom, detecta_erro, ...]
    criado_por: gerar_dados_sinteticos.py::gen_p01
    versao: v1
    dvc_hash: abc123...
    anonimizado: true
  P03_eeg_papel:
    path: dados_sinteticos/P03_eeg_papel.npy
    shape: [60, 32, 500]
    tipo: npy
    ...
```

**B.3 — CLI tool (`neurociencia_edu/cli.py`)**

Comandos:
```bash
neuro validate --dataset P01_diarios_sinteticos
neuro generate --project P01 --n 15
neuro analyze --notebook 01_tutorial_basico
neuro catalog list
neuro catalog show P01_diarios_sinteticos
neuro cache list
neuro cache clear
```

Implementação:
- `argparse` para parsing
- Logging estruturado
- Saída em JSON (machine-readable) ou tabela
- Exit codes apropriados (0=ok, 1=erro, 2=warning)

**B.4 — Cache inteligente (`neurociencia_edu/cache.py`)**

```python
from neurociencia_edu.cache import cached_analysis

@cached_analysis("mixed_models_p01")
def run_mixed_models(df_path: str) -> pd.DataFrame:
    # Cached based on hash of df_path content + function code
    ...
```

- Hash SHA256 de inputs (file content + function source)
- Storage: `.neuro_cache/` (excluído do git)
- LRU eviction (max 1 GB)
- CLI para gerenciar: `neuro cache list/clear`

**B.5 — Métricas de drift**
- `neurociencia_edu/stats/_drift.py`
- Compara distribuições entre versões de datasets
- PSI (Population Stability Index), KS test
- Gera relatório `drift_report.html`

### 5.3. Critérios de aceitação (Fase B)

- [ ] `dvc add` aplicado a 5 datasets sintéticos
- [ ] `catalog.yaml` completo e validado
- [ ] CLI `neuro` funcional com 6+ comandos
- [ ] Cache hit rate ≥ 80% em re-runs
- [ ] Drift detector gera relatório em HTML

### 5.4. Riscos e mitigações (Fase B)

| Risco | Mitigação |
|---|---|
| DVC storage local cheio | Configurar `cache.type = symlink` |
| CLI quebra em Windows | Testar em `pathlib` cross-platform |
| Cache invalida errado | Documentar hash logic claramente |

---

## 6. FASE C — Interactive Research Dashboard (Sessões 7-9)

### 6.1. Objetivo
Construir dashboard Streamlit central que serve como hub para os 5 projetos.

### 6.2. Entregas

**C.1 — Multi-page Streamlit app**

Estrutura:
```
streamlit_app.py (entry)
└── pages/
    ├── 1_🏠_Visao_Geral.py
    ├── 2_📊_P01_Qualitativo.py
    ├── 3_🎮_P02_Gamificacao.py
    ├── 4_🧠_P03_EEG.py
    ├── 5_📈_P04_SEM.py
    ├── 6_📅_P05_Longitudinal.py
    ├── 7_📚_Manuscritos.py
    └── 8_⚙️_Admin.py
```

Cada página P0X:
- Visão geral do projeto
- Estatísticas descritivas (synthetic + real quando disponível)
- Filtros: escola, idade, sexo
- Visualizações interativas (Plotly)
- Export: PDF + CSV

**C.2 — Filtros interativos**
- `streamlit-aggrid` para tabelas filtráveis
- `streamlit-extras` para componentes extras
- Session state para persistir filtros entre páginas

**C.3 — Export de relatórios**
- Botão "Gerar PDF" em cada página P0X
- Usa `reportlab` (já temos no Resumo Executivo)
- Inclui figuras + tabelas filtradas
- Download direto no browser

**C.4 — Storytelling mode**
- `pages/0_🎬_Tour.py`
- Walkthrough guiado pelos 5 projetos
- Step-by-step com `streamlit-extras` cards
- Links cruzados entre páginas

**C.5 — Auth simples (opcional)**
- Se Streamlit Cloud permitir: `streamlit-authenticator`
- Modo público (read-only) vs autenticado (admin)
- Senha via env var `DASHBOARD_PASSWORD`

### 6.3. Critérios de aceitação (Fase C)

- [ ] Multi-page app com 8 páginas navegáveis
- [ ] Filtros funcionais em todas as páginas P0X
- [ ] Export PDF funciona em pelo menos 3 páginas
- [ ] Storytelling mode completo
- [ ] Dashboard deploy em `https://neurociencia-educacional.streamlit.app`

### 6.4. Riscos e mitigações (Fase C)

| Risco | Mitigação |
|---|---|
| Streamlit Cloud timeout (1 GB) | Lazy loading de dados |
| Mobile não suportado bem | Testar em viewport pequeno |
| Performance ruim com filtros | Usar `@st.cache_data` |

---

## 7. Arquitetura de Testes

### 7.1. Pirâmide de testes (atual → alvo)

```
                  ▲
                 / \
                / E2E\         (futuro, manual)
               /------\
              / Integr.\      (test_pipeline_integration.py, atual)
             /----------\
            / Unit tests \   (test_infrastructure.py + novos, alvo: 200+)
           /--------------\
```

### 7.2. Cobertura-alvo por módulo

| Módulo | Atual | Alvo |
|---|---|---|
| `neurociencia_edu/config.py` | ~80% | 100% |
| `neurociencia_edu/logging_config.py` | ~70% | 95% |
| `neurociencia_edu/exceptions.py` | ~90% | 100% |
| `neurociencia_edu/validators.py` | ~85% | 100% |
| `neurociencia_edu/stats/*` (novo) | 0% | 90% |
| `neurociencia_edu/eeg/*` (novo) | 0% | 90% |
| `neurociencia_edu/text/*` (novo) | 0% | 90% |
| `neurociencia_edu/cli.py` (novo) | 0% | 90% |
| `neurociencia_edu/cache.py` (novo) | 0% | 95% |
| Notebooks (papermill) | 0% | 100% run success |

### 7.3. Estratégia de testes (TDD)

Para cada nova função, seguir:
1. **Red:** Escrever teste falhando primeiro
2. **Green:** Implementar mínimo para passar
3. **Refactor:** Limpar mantendo testes verdes

Testes devem cobrir:
- Casos felizes
- Edge cases (vazio, None, NaN)
- Error handling (exceções corretas)
- Performance (não 10x mais lento que baseline)

---

## 8. Plano de Implementação (alto nível)

### 8.1. Sequência das fases

```
Sessão 1: Setup CI notebooks
Sessão 2: Refactor stats/ (Fase A.2)
Sessão 3: Refactor eeg/ + text/ (Fase A.2) + vectorização (Fase A.3)
─── checkpoint: 15 notebooks CI-tested ───
Sessão 4: DVC + catalog (Fase B.1, B.2)
Sessão 5: CLI tool (Fase B.3)
Sessão 6: Cache + drift (Fase B.4, B.5)
─── checkpoint: DVC + CLI funcionais ───
Sessão 7: Multi-page dashboard (Fase C.1, C.2)
Sessão 8: Export PDF + Storytelling (Fase C.3, C.4)
Sessão 9: Auth + deploy final (Fase C.5)
─── checkpoint: Dashboard público online ───
```

### 8.2. Dependências novas

| Fase | Dependência | Versão | Justificativa |
|---|---|---|---|
| A | `papermill` | ≥2.5 | Executar notebooks em CI |
| A | `pytest-notebook` | ≥0.10 | Testes de notebooks |
| A | `tqdm` | ≥4.66 | Progress bars |
| B | `dvc` | ≥3.50 | Data versionamento |
| B | `dvc-s3` | ≥3.0 | Remote S3 (opcional) |
| B | `psutil` | ≥5.9 | Memory tracking |
| C | `streamlit-aggrid` | ≥0.3 | Tabelas filtráveis |
| C | `streamlit-extras` | ≥0.4 | Componentes extras |
| C | `streamlit-authenticator` | ≥0.3 | Auth (opcional) |

### 8.3. Variáveis de ambiente

```bash
# Fase B
DVC_REMOTE_URL=s3://bucket/path  # ou local
NEURO_CACHE_DIR=.neuro_cache
NEURO_CACHE_MAX_GB=1

# Fase C
DASHBOARD_PASSWORD=xxx  # opcional, para auth
STREAMLIT_THEME=dark
```

### 8.4. Estrutura de arquivos (delta)

```
NOVOS ARQUIVOS:
.github/workflows/notebooks.yml
neurociencia_edu/stats/_trends.py
neurociencia_edu/stats/_power.py
neurociencia_edu/stats/_irt.py
neurociencia_edu/stats/_survival.py
neurociencia_edu/eeg/_preprocess.py
neurociencia_edu/eeg/_erp.py
neurociencia_edu/text/_sentiment.py
neurociencia_edu/text/_network.py
neurociencia_edu/io/_serializers.py
neurociencia_edu/cli.py
neurociencia_edu/cache.py
neurociencia_edu/stats/_drift.py
tests/test_stats.py
tests/test_eeg_refactored.py
tests/test_text_refactored.py
tests/test_cache.py
tests/test_cli.py
tests/test_drift.py
tests/test_notebooks.py
tests/fixtures/
scripts/notebook_helpers.py
dados_sinteticos/catalog.yaml
dados_sinteticos/.dvc/.gitignore
pages/0_🎬_Tour.py
pages/1_🏠_Visao_Geral.py
... (8 páginas)

ARQUIVOS MODIFICADOS:
notebooks/01-15 (imports de neurociencia_edu.refactored)
pyproject.toml (deps)
.github/workflows/ci.yml (adiciona notebook step)
.dvcignore (criado por dvc init)
```

---

## 9. Conformidade LGPD

Manter durante toda a evolução:

- **Anonimização:** SHA256 com salt (`LGPD_SALT` env var)
- **PII detection:** `validators.detectar_pii()` em todos os uploads
- **Audit log:** `neurociencia_edu/audit.py` (NOVO) registra acessos a dados
- **Direito ao esquecimento:** Função `neuro anonymize --subject <id>`

---

## 10. Critérios de Sucesso (Fase Final = Sessão 9)

### 10.1. Métricas técnicas
- [ ] 15/15 notebooks rodam em CI (<60 min total)
- [ ] Cobertura de testes ≥ 90% em módulos refatorados
- [ ] ≥ 200 testes passando
- [ ] Cache hit rate ≥ 80%
- [ ] Dashboard online em `https://neurociencia-educacional.streamlit.app`

### 10.2. Métricas de valor
- [ ] Tempo para re-rodar análise P01: < 5 min (era ~30 min)
- [ ] Tempo para validar novo dataset: < 1 min (era manual)
- [ ] Tempo para gerar relatório de projeto: < 1 min (era manual)
- [ ] Onboarding de novo colaborador: < 30 min (era dias)

### 10.3. Métricas de compliance
- [ ] 100% dos dados sintéticos em DVC
- [ ] 100% dos dados com PII detectados
- [ ] Audit log completo
- [ ] LGPD checklist passando

---

## 11. Não-Objetivos (YAGNI Explícito)

❌ **Não fazer:**
- Migração para monorepo de pacotes separados (overkill)
- API REST separada (Streamlit é suficiente)
- Banco de dados PostgreSQL (SQLite/CSV ok)
- Kubernetes/Orquestração complexa (Snakemake já basta)
- MLflow (DVC cobre)
- Re-escrita completa dos notebooks (refactor cirúrgico)
- Internacionalização completa de código (só docs PT/EN/ES)
- Mobile app (foco web)
- Microserviços (acoplamento atual é OK)
- GraphQL (REST/Streamlit suficiente)
- WebSockets (polling é suficiente)
- Auth com OAuth (senha simples ok para piloto)

---

## 12. Aprovações

**Aprovações necessárias ANTES de começar a implementar:**

- [ ] **Usuário** aprova este design
- [ ] **Usuário** aprova o plano de implementação (próxima fase: `writing-plans`)

---

## 13. Próximos Passos (após aprovação)

1. Invocar skill `superpowers:writing-plans`
2. Gerar plano de implementação detalhado (task-by-task)
3. Plano será commitado em `docs/superpowers/plans/`
4. Iniciar Fase A (Sessão 1)

---

**Mantido por:** Programa de Pesquisa em Neurociência Educacional
**Licença:** MIT
**Última atualização:** 2026-08-14
