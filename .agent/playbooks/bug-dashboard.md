# 📋 Playbook: bug-dashboard

> **Trigger:** "Bug no dashboard" / "Erro no Streamlit" / "Página X não funciona"
> **Domínio:** Engineering + Review
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Demonstrar a **filosofia de engenharia** do agente:
- **Reproduzir** antes de corrigir
- **Testar** antes de mexer no código de produção
- **Validar** antes de declarar "resolvido"

**REGRA:** `bug → alterar código → "resolvido"` é PROIBIDO.

---

## 🔄 Fluxo (8 passos)

### 1. BUG REPORT — Capturar

```markdown
# Bug Report — Dashboard

**Data:** AAAA-MM-DD
**Reportado por:** [humano/IA]
**Severidade:** [crítica / alta / média / baixa]

## Sintoma
[Descrição do que acontece]

## Esperado
[O que deveria acontecer]

## Reproduzir
[Passos para reproduzir]

## Ambiente
- Streamlit Cloud / local
- Página específica: pages/2_📊_P01_Qualitativo.py
- Browser: Chrome / Firefox / Safari
- Logs do Streamlit: [trecho relevante]
```

---

### 2. REPRODUZIR — Confirmar o bug

```bash
# Local
streamlit run streamlit_app.py
# Navegar até a página afetada
# Confirmar que bug acontece

# Streamlit Cloud
# Verificar logs em https://share.streamlit.io/...
# Confirmar que bug acontece em produção também
```

**Output:** bug confirmado + condições mínimas de reprodução.

---

### 3. IDENTIFICAR CAUSA — Root cause analysis

```bash
Ler:
- pages/N_*.py (página afetada)
- analise/Python/neurociencia_edu/*.py (módulos importados)
- Stack trace completo

Técnicas:
- print() estratégico
- st.write() para debug
- Verificar paths absolutos vs relativos
- Verificar imports circulares
- Verificar seed=42 (se dados sintéticos)
```

**Output:** causa raiz identificada (não sintoma).

---

### 4. CRIAR TESTE — Red (teste que reproduz o bug)

```bash
# tests/test_bug_dashboard.py
"""Teste de regressão para bug #N."""
import pytest

def test_bug_N_descricao():
    """Reproduz o bug encontrado em AAAA-MM-DD."""
    # Setup que reproduz as condições do bug
    ...
    # Assert que DEVERIA funcionar mas está falhando
    with pytest.raises(SomeError) or assert result == expected:
        call_to_broken_function(...)
```

**Regra:** o teste deve **FALHAR** antes do fix. Depois do fix, deve **PASSAR**.

```bash
pytest tests/test_bug_dashboard.py -v
# → DEVE FALHAR (RED)
```

---

### 5. CORRIGIR — Green

```bash
# Modificar código de produção
# pages/N_*.py ou neurociencia_edu/*.py
# Mínimo de mudança para corrigir o bug
```

```bash
pytest tests/test_bug_dashboard.py -v
# → DEVE PASSAR (GREEN)
```

---

### 6. REGRESSÃO — Garantir que não quebrou nada

```bash
# Rodar suite completa
pytest tests/ -q

# Verificar lint
ruff check pages/ analise/Python/neurociencia_edu/

# Verificar Streamlit
streamlit run streamlit_app.py
# Testar TODAS as 8 páginas manualmente (ou smoke test)
```

**Output:** suite verde + lint limpo + todas as páginas funcionam.

---

### 7. DOCUMENTAR — Commit + Bug fix report

```bash
git add -A
git commit -m "fix(pages): corrige bug #N em página X

PROBLEMA: [descrição do sintoma]
CAUSA: [root cause]
FIX: [o que mudou]

TESTES:
- Adicionado test_bug_dashboard.py::test_bug_N
- 182/182 testes passando
- Lint: ruff OK
- Manual: 8 páginas verificadas

Refs: bug report #N"
git push
```

**Output:** commit pushed + Streamlit Cloud auto-deploy.

---

### 8. VALIDAR EM PRODUÇÃO

```bash
# Aguardar 2-3 min para Streamlit Cloud rebuild
# Acessar https://<app>.streamlit.app/<página afetada>
# Confirmar bug corrigido
# Checar logs de produção por 24h
```

**Output:** bug corrigido em produção + logs limpos.

---

## 🚨 Anti-padrões

❌ **Bug → alterar código → "resolvido"** (sem teste que falha antes)
❌ **Múltiplas mudanças no mesmo commit** (dificulta reversão)
❌ **Pular o teste de regressão** (introduz bugs novos)
❌ **Não documentar a causa raiz** (vai acontecer de novo)
❌ **"Funciona na minha máquina"** sem testar em produção
❌ **Auto-merge sem code review** (mesmo sendo IA)
❌ **Commit sem mensagem descritiva** (perde rastreabilidade)

---

## 🐛 Bugs comuns neste projeto

### Path absoluto vs relativo
**Sintoma:** `ModuleNotFoundError: No module named 'neurociencia_edu'` no Streamlit Cloud
**Causa:** `Path("/workspace/...")` em vez de `Path(__file__).resolve().parent.parent / "..."`
**Fix:** ver `pages/AGENTS.md` para padrão correto
**Teste:** adicionar teste de import cross-environment

### Colorbar matplotlib
**Sintoma:** `UserWarning: Adding colorbar to a different Figure`
**Causa:** `plt.colorbar(im, ax=axes[i], ...)` em loop
**Fix:** `fig.colorbar(ims[0], ax=axes, ...)` (compartilhado)
**Teste:** smoke test que renderiza a página

### Dados sintéticos ausentes
**Sintoma:** página renderiza dados vazios ou erro
**Causa:** `Path("/workspace/dados_sinteticos/...")` não acessível
**Fix:** cada página tem fallback on-the-fly (gerar dados com seed=42)
**Teste:** teste com `tmp_path` mockando diretório

---

## 📂 Onde reportar bugs

| Tipo | Onde |
|---|---|
| Bug em página Streamlit | `pages/N_*.py` + teste em `tests/test_pages.py` |
| Bug em módulo Python | `analise/Python/neurociencia_edu/*.py` + teste em `tests/test_*.py` |
| Bug em dado sintético | `dados_sinteticos/*.csv` + `tests/test_synthetic.py` |
| Bug em CI workflow | `.github/workflows/*.yml` + rodar localmente com `act` |

---

## 📋 Template de Bug Report (reutilizável)

```markdown
# Bug #N — [título curto]

## Severidade
[ ] crítica (impede uso)
[ ] alta (quebra funcionalidade principal)
[ ] média (cosmético ou workaround existe)
[ ] baixa (nice-to-have)

## Ambiente
- [ ] local / Streamlit Cloud
- [ ] página: pages/N_*.py
- [ ] browser:
- [ ] logs:

## Sintoma
[descrição]

## Esperado
[descrição]

## Reproduzir
1. ...
2. ...
3. ...

## Causa raiz
[análise]

## Fix
[código]

## Teste
[teste em tests/test_*.py]

## Validação
- [ ] pytest verde
- [ ] ruff verde
- [ ] smoke test 8 páginas
- [ ] produção (Streamlit Cloud)
```

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após primeiro bug real
