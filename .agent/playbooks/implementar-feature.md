# 📋 Playbook: implementar-feature

> **Trigger:** "Implementar feature X" / "Adicionar funcionalidade Y"
> **Domínio:** Engineering + Review
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Adicionar nova feature ao programa com **TDD estrito** e **revisão antes de merge**.

---

## 🔄 Fluxo (7 passos)

### 1. CONDUCTOR — Entender o requisito

```bash
Perguntar ao usuário (se ambíguo):
- Qual problema a feature resolve?
- Quem é o usuário?
- Qual o critério de "pronto"?
- Qual a prioridade (bloqueante, alta, média, baixa)?
```

**Output:** requisito claro + critérios de aceitação.

---

### 2. ENGINEERING — Especificação técnica

```bash
Ler:
- engineering/AGENTS.md
- analise/Python/AGENTS.md (se Python)
- AGENTS.md do módulo afetado (se existir)

Decidir:
- Onde mora o código? (qual módulo?)
- Qual a interface pública?
- Quais dependências novas?
- Há mudança breaking? (registrar em ADR)
```

**Output:** spec técnica + ADR se necessário.

---

### 3. TDD — Red (escrever teste que falha)

```bash
# tests/test_feature_X.py
def test_feature_X():
    """Feature X: [descrição]."""
    # Arrange
    setup_data = create_test_data()
    # Act
    result = feature_X(setup_data)
    # Assert
    assert result == expected

pytest tests/test_feature_X.py -v
# → DEVE FALHAR (RED)
```

---

### 4. TDD — Green (implementação mínima)

```bash
# Implementar o mínimo para o teste passar
# analise/Python/neurociencia_edu/modulo/X.py

pytest tests/test_feature_X.py -v
# → DEVE PASSAR (GREEN)
```

---

### 5. TDD — Refactor (melhorar sem quebrar)

```bash
# Melhorar legibilidade, performance, type hints
# pytest deve continuar passando

pytest tests/test_feature_X.py -v
ruff check analise/Python/neurociencia_edu/modulo/X.py
# → GREEN + lint OK
```

---

### 6. REGRESSÃO — Suite completa

```bash
pytest tests/ -q
ruff check .
# → 182/182 testes passando + lint limpo
```

---

### 7. CONDUCTOR — Commit + push + reportar

```bash
git add -A
git commit -m "feat(modulo): adicionar feature X

REQUISITO: [link]
TDD: Red → Green → Refactor
- tests/test_feature_X.py (3 testes novos)
- analise/Python/neurociencia_edu/modulo/X.py (função X)

VALIDAÇÃO:
- 182/182 testes passando
- ruff OK
- smoke test manual: ✓
- ADR-XXX criado (se mudança breaking)"

git push
```

**Output:** feature em produção (Streamlit Cloud auto-deploy).

---

## 🚨 Anti-padrões

❌ Implementar sem teste
❌ Múltiplas features em 1 commit
❌ Não rodar regressão
❌ Não atualizar docs (API-REFERENCE se API pública)
❌ Não comunicar ao usuário

---

**Última atualização:** 2026-09-19
