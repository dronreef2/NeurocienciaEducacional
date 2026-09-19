# Maturity Model — Modelo de Maturidade dos Projetos

> **Sistema operacional** para classificar e progredir projetos de pesquisa.
> **Versão:** 1.1 — 2026-09-19 (3 dimensões adicionadas)
> **Inspiração:** NEURA, Capability Maturity Model (CMM), TRL (Technology Readiness Levels)

---

## 🚨 Conceito central: MATURITY ≠ READINESS ≠ VALIDATION

Desde Cycle 3, separamos **3 dimensões ortogonais** que estavam sendo confundidas:

| Dimensão | Pergunta que responde | Quem avalia |
|---|---|---|
| **Maturity** | Onde o projeto está no pipeline? | Agente (N0-N5) |
| **Readiness** | O que está bloqueando o próximo passo? | Agente + humano |
| **Validation** | O que foi **verificado de fato**? | Humano + peer review |

**Exemplo (P01, Cycle 3):**

```yaml
P01:
  maturity: N1_PROTOCOL          # está em N1
  readiness:
    protocol: high               # docs prontos
    ethics: blocked              # bloqueado por D01
    implementation: high         # piloto + pipeline ok
  validation:
    scientific: pending_human_review   # Ângela não revisou
    technical: verified                # 182 testes passam
    ethical: pending_human_review      # CEP não submetido
```

**Por que isso importa:**

- N2 (maturity) ≠ "projeto cientificamente validado" (validation)
- Um projeto pode ser N1 com documentação excelente e estar **cientificamente não validado**
- O próximo gate pode ser **readiness** (fazer algo) ou **validation** (revisar algo existente)

**Anti-padrão:** confundir maturity com validation leva a claims tipo "P01 está pronto" quando, na verdade, ele está "documentado mas não revisado".

---

## 🎯 Conceito

Cada projeto de pesquisa passa por **5 níveis de maturidade**, do mais imaturo ao mais maduro. Cada nível tem:

- **Critérios verificáveis** (o que precisa estar pronto)
- **Gate humano** (HUMAN GATE obrigatório para avançar)
- **Outputs físicos** (artefatos produzidos)

O agente **não avança** sozinho entre níveis. Ele **prepara** o avanço, **valida** que os critérios estão prontos, e **pede aprovação** humana.

---

## 📊 Os 5 níveis

### Nível 0 — PLANNING (Planejamento)

**Descrição:** ideia inicial, sem protocolo formal.

**Critérios verificáveis:**
- [ ] Tema definido (1 frase)
- [ ] Pergunta de pesquisa preliminar
- [ ] 1-3 referências bibliográficas iniciais
- [ ] Conexão com linha-mãe (Leitura + Neurociências) identificada

**Outputs físicos:**
- `0X-.../README.md` (página inicial)
- 1 nota de leitura inicial

**Gate humano:** aprovação para iniciar protocolo formal.

---

### Nível 1 — PROTOCOL (Protocolo detalhado)

**Descrição:** projeto detalhado escrito, instrumentos desenhados, mas ainda não submetido a comitê de ética.

**Critérios verificáveis:**
- [ ] `protocolo/projeto-detalhado.md` completo (introdução, método, ética, cronograma, orçamento)
- [ ] Todos os instrumentos elaborados (`instrumentos/0X-*.md`)
- [ ] TCLE + TALE (se pesquisa com humanos)
- [ ] Plano de análise definido
- [ ] Pré-registro OSF validado (`docs/osf-json/P0X-osf.json`)

**Outputs físicos:**
- `0X-.../protocolo/projeto-detalhado.md`
- `0X-.../instrumentos/*.md` (5-10 arquivos)
- `docs/osf-json/P0X-osf.json`

**Gate humano:** revisão da Ângela (orientadora) + aprovação para submissão ética.

---

### Nível 2 — ETHICS_APPROVED (Ética aprovada)

**Descrição:** projeto submetido e aprovado pelo CEP. Pronto para coletar dados.

**Critérios verificáveis:**
- [ ] CAAE obtido
- [ ] Parecer CEP aprovado (sem pendências)
- [ ] Carta de anuência da escola/instituição parceira assinada
- [ ] Currículo Lattes + ORCID atualizados
- [ ] TCLE/TALE prontos para aplicação

**Outputs físicos:**
- Parecer CEP arquivado em `0X-.../protocolo/cep-parecer.pdf` (privado, NÃO versionado)
- Carta de anuência assinada (privada, NÃO versionada)

**Gate humano:** aprovação Ângela para iniciar coleta.

---

### Nível 3 — DATA_COLLECTED (Dados coletados)

**Descrição:** coleta de campo realizada, dados anonimizados.

**Critérios verificáveis:**
- [ ] Coleta realizada (N atingido)
- [ ] Dados anonimizados (LGPD compliance)
- [ ] Dados primários arquivados em local seguro (NÃO versionado)
- [ ] Dados sintéticos/derivados versionados em `dados_sinteticos/` (se aplicável)
- [ ] Pipeline de análise testado com dados reais

**Outputs físicos:**
- Dados primários: storage criptografado (NÃO versionado)
- Dados sintéticos/derivados: `dados_sinteticos/P0X_*.csv` (se houver)

**Gate humano:** aprovação Ângela para iniciar análise.

---

### Nível 4 — ANALYZED (Análise completa)

**Descrição:** análise estatística/qualitativa completa, resultados documentados.

**Critérios verificáveis:**
- [ ] Análise completa conforme plano pré-registrado
- [ ] Resultados em formato tabelado + figuras
- [ ] Relatório de análise (`.agent/reports/analise-P0X-AAAA-MM-DD.md`)
- [ ] Reproductibilidade verificada (seed=42, scripts versionados)
- [ ] INTERPRETAÇÃO validada pela Ângela (HUMAN GATE)

**Outputs físicos:**
- `resultados/P0X_*/` (tabelas, figuras)
- `analise/Python/notebooks/NN_*.ipynb` (analyses)
- `.agent/reports/analise-P0X-*.md`

**Gate humano:** aprovação Ângela para iniciar escrita do manuscrito.

---

### Nível 5 — PUBLISHED (Publicado)

**Descrição:** manuscrito publicado em journal com revisão por pares.

**Critérios verificáveis:**
- [ ] Manuscrito submetido a journal (Qualis A1/A2 ou Scopus Q1/Q2)
- [ ] Manuscrito aceito (peer review passed)
- [ ] Publicado online (DOI)
- [ ] Dados anonimizados depositados em repositório aberto (OSF, Zenodo)
- [ ] Preprint disponível (PsyArXiv, SSRN, etc.)

**Outputs físicos:**
- `docs/manuscritos/P0X_published.pdf` ou link DOI
- Dados em OSF/Zenodo (DOI)

**Gate humano:** N/A (peer review fez a validação).

---

## 📈 Progressão típica

```
N0 ──→ N1 ──→ N2 ──→ N3 ──→ N4 ──→ N5
PLANNING  PROTOCOL  ETHICS  DATA  ANALYZED  PUBLISHED
   │         │        │       │       │          │
   │         │        │       │       │          └ peer review
   │         │        │       │       └────────────┘
   │         │        │       └ análise + interpretação
   │         │        └ CEP aprovado
   │         └ protocolo + OSF
   └ ideia
```

**Estimativa realista:**
- N0 → N1: 2-4 meses
- N1 → N2: 2-3 meses (CEP)
- N2 → N3: 6-18 meses (coleta)
- N3 → N4: 2-6 meses (análise)
- N4 → N5: 6-12 meses (submissão + peer review)

**Total típico por projeto:** 18-43 meses.

---

## 🎯 Estado atual dos 5 projetos (verificado 2026-09-19)

| Projeto | Maturidade | Próximo gate | Responsável |
|---|---|---|---|
| **P01** (quali IA) | N1 → N2 (transição) | D02 + D08 (CEP) | Pesquisadora + Ângela |
| **P02** (ECR gamif) | N1 (protocolo ok) | Submeter FAPERN + CEP | Pesquisadora |
| **P03** (EEG) | N1 (protocolo ok) | Acordo ICe + CEP | Pesquisadora + Ângela |
| **P04** (SEM) | N1 (protocolo ok) | Aguardar P01-P03 (sequencial) | Pesquisadora |
| **P05** (coorte) | N1 (protocolo ok) | Aguardar funding + parcerias | Pesquisadora |

**Insight:** P01 está **na frente** (transição N1→N2). P02-P05 estão **parados em N1** (protocolo pronto mas sem trigger para avançar).

---

## 🔧 Como o agente usa o modelo

### Descoberta (Discovery)
```bash
# Para cada projeto, verificar:
- Quais critérios do nível atual estão ✅?
- Quais estão ❌?
- Qual é o próximo gate?
- Quem é responsável?
```

### Diagnóstico
```bash
Output: program-maturity-matrix-AAAA-MM-DD.md
- Tabela com 5 projetos × 5 níveis
- Gaps prioritários por projeto
- Gargalo real (qual projeto está bloqueando o quê)
```

### Roadmap (Next verifiable state)
```bash
Output: next-actions.md
- Para cada projeto, qual é a próxima ação verificável?
- Quem? (humano vs IA)
- Quando? (cronograma)
- Como validar? (critério de "feito")
```

### Implementação + Testes + Validação + Documentação
```bash
Segue playbooks específicos (.agent/playbooks/)
```

---

## 🎯 Separação importante

```
Nível atual     = onde o projeto ESTÁ (verificado)
Próximo gate    = onde PRECISA IR (decidido)
Como chegar     = caminho (proposto pela IA, aprovado pelo humano)
Quando          = cronograma (verificado)
```

**A IA pode:**
- Verificar nível atual
- Propor caminho
- Sugerir cronograma
- Executar ações técnicas delegadas (código, docs, dados)

**A IA NÃO pode:**
- Avançar nível sem aprovação humana
- Decidir submeter ao CEP / journal / OSF
- Interpretar resultados como "conclusões"

---

## 🔗 Links

- `.agent/STATE.yaml` — onde estamos agora (state verificado)
- `.agent/reports/program-maturity-*.md` — diagnóstico por ciclo
- `.agent/playbooks/` — como fazer
- `.agent/decisions/` — decisões arquiteturais (passadas)
- `.agent/memory/` — log cronológico de ações dos agentes

---

**Última atualização:** 2026-09-19
**Próxima revisão:** após próximo integration test
