# 📋 Playbook: submeter-p01

> **Trigger:** "Preparar P01 para submissão" / "Submeter P01 a [journal/CEP/OSF]"
> **Domínio:** Conductor + Research + Methodology + Compliance + Review
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Objetivo

Gerar **submission-readiness-report.md** auditável, separando:
- O que está pronto
- O que falta (com responsável + prazo)
- Decisões pendentes (HUMAN GATE)

**REGRA:** IA **NÃO submete** automaticamente. Submeter é decisão humana.

---

## 🔄 Fluxo (8 passos)

### 1. CONDUCTOR — Ler contexto

```bash
Ler:
- .agent/STATE.yaml
- AGENTS.md (raiz)
- 01-projeto-qualitativo-criancas-ia/AGENTS.md
- 01-projeto-qualitativo-criancas-ia/protocolo/projeto-detalhado.md
- 01-projeto-qualitativo-criancas-ia/instrumentos/ (todos)
- docs/osf-json/P01-osf.json (se existe)
- docs/manuscritos/P01_manuscrito_v1.md (se existe)
```

**Output:** snapshot do estado atual.

---

### 2. RESEARCH — Verificar literatura

```bash
- Notas de leitura relevantes para P01 (00-fundamentos/notas-leitura/)
- Identificar lacunas teóricas
- Verificar referências citadas no manuscrito
- Conferir se referências estão atualizadas (papers 2024-2026)
```

**Output:** lista de papers faltantes + referências inconsistentes.

---

### 3. METHODOLOGY — Verificar método

```bash
Checklist:
- [ ] Hipóteses claras (H1, H2, H3...)
- [ ] Objetivos (geral + específicos)
- [ ] População definida (N, idade, sexo, escolaridade)
- [ ] Critérios inclusão/exclusão
- [ ] Instrumentos validados (referências)
- [ ] Procedimentos de coleta (passo a passo)
- [ ] Plano de análise (técnicas estatísticas)
- [ ] Pré-registro OSF consistente
```

**Output:** checklist de gaps metodológicos.

---

### 4. COMPLIANCE — Verificar ética

```bash
Checklist LGPD + CEP:
- [ ] TCLE (termo de consentimento livre e esclarecido) — versão final
- [ ] TALE (termo de assentimento da criança) — versão final
- [ ] Carta de anuência da escola
- [ ] Plataforma Brasil checklist preenchido
- [ ] Riscos e benefícios documentados
- [ ] Como dados serão anonimizados
- [ ] Como dados serão armazenados (local, prazo)
- [ ] Direito de retrait (criança pode sair a qualquer momento)
- [ ] Confidencialidade (quem tem acesso)
- [ ] LGPD Art. 7º, IV — consentimento específico
```

**Output:** checklist LGPD + gaps éticos.

---

### 5. REVIEW — Identificar inconsistências

```bash
Procurar por:
- Hipótese X não tem variável dependente clara
- Manuscrito cita instrumento Y que não está em /instrumentos/
- Pré-registro OSF tem N=15 mas manuscrito diz N=12
- Análise estatística X não está no plano de análise
- TCLE não menciona EEG (se houver)
- Cronograma do estudo conflita com plano de mestrado
```

**Output:** lista de inconsistências + severidade (alta/média/baixa).

---

### 6. CONDUCTOR — Gerar relatório

**Arquivo:** `.agent/reports/submission-readiness-P01-AAAA-MM-DD.md`

**Estrutura:**

```markdown
# Submission Readiness Report — P01

**Data:** AAAA-MM-DD
**Versão:** vN (incrementar a cada rodada)
**Target:** [CEP / OSF / Computers & Education]

## Status: [READY / NEEDS WORK / BLOCKED]

## ✅ Pronto
- [item verificado]

## ⏳ Pendente (com responsável + prazo)
- [item] — responsável: [nome] — prazo: AAAA-MM-DD

## 🚨 Bloqueios (HUMAN GATE)
- [decisão crítica que precisa de humano]

## 📊 Inventário
- Protocolo: [caminho] — versão vN
- Instrumentos: N arquivos — versões
- Manuscrito: [caminho] — versão vN — X palavras
- Pré-registro: [caminho] — status [validado/submetido]
- TCLE: [caminho] — versão final?
- TALE: [caminho] — versão final?
- Carta anuência: [caminho] — obtida?
- Dados piloto: sim/não — quantos?

## 🎯 Próximos passos
1. [ação] — [responsável] — [prazo]
2. ...
```

---

### 7. CONDUCTOR — Apresentar ao usuário

```
🤖 Submission Readiness Report — P01

Status: NEEDS WORK

✅ Pronto (8):
  - Protocolo v3
  - 8 instrumentos
  - Manuscrito v1 (6k palavras)
  - Pré-registro OSF validado

⏳ Pendente (5):
  - TCLE versão final — você — até 2026-09-25
  - TALE versão final — você — até 2026-09-25
  - Carta anuência escola — Ângela — até 2026-09-30
  - Plataforma Brasil checklist — você — até 2026-09-30
  - Referência X atualizar — eu — até 2026-09-22

🚨 Bloqueios (2):
  - Submeter ao CEP? (decisão sua + Ângela)
  - Submeter a Computers & Education? (decisão sua + Ângela)

Deseja que eu corrija as pendências? Submissão NÃO será automática.
```

---

### 8. SUBMETER (HUMAN GATE)

```bash
# Usuário confirma + executa
python3 analise/Python/scripts/osf_submit.py --prereg P01  # OSF
# OU
# Acessar Plataforma Brasil manualmente (não automatizável)
# OU
# Acessar Computers & Education submission portal (não automatizável)
```

---

## 📁 Arquivos relacionados

- `01-projeto-qualitativo-criancas-ia/AGENTS.md`
- `docs/osf-json/P01-osf.json` (validado)
- `docs/manuscritos/P01_manuscrito_v1.md` (rascunho)
- `01-projeto-qualitativo-criancas-ia/protocolo/projeto-detalhado.md`
- `01-projeto-qualitativo-criancas-ia/protocolo/checklist-cep.md`
- `01-projeto-qualitativo-criancas-ia/protocolo/plataforma-brasil-checklist.md`
- `analise/Python/scripts/osf_submit.py`

---

## 🔗 Outputs deste playbook

| Output | Arquivo | Quem |
|---|---|---|
| Submission Readiness Report | `.agent/reports/submission-readiness-P01-AAAA-MM-DD.md` | IA |
| Decisão final | (humano) | Usuário + Ângela |
| Submissão | (humano ou OSF API) | Humano |

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após 1ª submissão real do P01
