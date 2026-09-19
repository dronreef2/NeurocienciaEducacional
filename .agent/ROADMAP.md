# ROADMAP.md — Evolução do programa + multi-agent system

> **Roadmap operacional** do programa e do Research OS.
> **Versão:** 1.0 — 2026-09-19
> **Owner:** Pesquisadora + Conductor (Mavis)

---

## 🎯 Curto prazo (2026 Q3-Q4)

### Programa de pesquisa
- [ ] **M3 (set/2026):** Reunião com Ângela → autorização formal
- [ ] **M3:** Submeter 5 pré-registros ao OSF (`osf_submit.py --all`)
- [ ] **M3:** Submeter P01 ao CEP/UFRN
- [ ] **M4 (out/2026):** Submeter P01 manuscrito a *Computers & Education*
- [ ] **M5:** Carta anuência escola + piloto expandido (12-15 crianças)
- [ ] **M6:** Defesa de qualificação no PPGED

### Research OS
- [x] Sistema multi-AGENTS inicial (ADR-001)
- [ ] **3 playbooks adicionais:** implementar-feature, revisar-metodologia, analisar-dados
- [ ] **STATE.yaml atualizado** após reunião Ângela (status P01)
- [ ] **.agent/reports/** com 1ª submission-readiness-report do P01

---

## 📅 Médio prazo (2027)

### Programa
- [ ] Coleta P02 (ECR gamificação, N=200)
- [ ] Coleta P03 (EEG tela vs papel, N=60)
- [ ] **Publicação P01** (target: Q1/2027)
- [ ] Defesa de mestrado (target: 2028.2)

### Research OS
- [ ] **3 ADRs adicionais:** decisões sobre pipeline EEG, SEM, LGCM
- [ ] **Playbook preparar-experimento** (checklist pré-coleta)
- [ ] **Playbook publicar-resultado** (workflow de submissão)
- [ ] Métricas de uso dos playbooks

---

## 🔮 Longo prazo (2028–2030)

### Programa
- [ ] Análise P04 (SEM, N=300-500)
- [ ] Início coorte P05 (T1=200 crianças, 7 anos)
- [ ] **Publicação P02 + P03**
- [ ] Defesa de doutorado (2030)
- [ ] **Publicação P04 + P05**

### Research OS
- [ ] Auto-update de STATE.yaml via git hook
- [ ] Métricas de reprodutibilidade (cobertura, drift detection)
- [ ] ADRs para decisões de infraestrutura (deploy, CI)
- [ ] Integração com Notion/Obsidian (opcional)

---

## 📊 Marcos críticos (60 meses)

```
2026 ████████████████████  ← Estamos aqui (M2)
      ├── Q3: reunião Ângela + CEP + OSF + journal
      ├── Q4: piloto + manuscrito v2
2027 ████████████████████
      ├── Q1: PUB P01
      ├── Q2-Q3: coleta P02 + P03
      ├── Q4: análise
2028 ████████████████████
      ├── Q1-Q2: PUB P02 + P03
      ├── Q3: defesa mestrado
      ├── Q4: início doutorado + P04
2029 ████████████████████
      ├── Q1: PUB P04
      ├── Q2-Q4: P05 ondas T1-T3
2030 ████████████████████
      ├── Q1-Q2: P05 ondas T4-T5
      ├── Q3: defesa doutorado
      ├── Q4: PUB P05
```

---

## 🔄 Critérios de sucesso

### Curto prazo (2026)
- P01 submetido ao CEP e a *Computers & Education* ✅
- 5 pré-registros OSF submetidos ✅
- Reunião com Ângela = orientação aceita ✅

### Médio prazo (2027–2028)
- P01 publicado ✅
- P02 + P03 coletados ✅
- Defesa de mestrado ✅

### Longo prazo (2030)
- 5 manuscritos publicados (P01-P05) ✅
- Tese de doutorado defendida ✅
- 3 sub-estudos derivados ✅
- Linha de pesquisa consolidada ✅

---

## 🚨 Anti-metas (o que NÃO buscar)

1. Publicar sem pré-registro
2. Coletar sem TCLE/TALE assinado
3. Crescer escopo sem recursos
4. Submeter manuscritos sem co-autoria
5. Modificar políticas sem aprovação

---

## 🔗 Links

- `.agent/STATE.yaml` — onde estamos agora
- `.agent/MISSION.md` — o que buscamos
- `00-fundamentos/cronograma-mestre.md` — timeline detalhada
- `docs/ROADMAP-PRATICO.md` — roadmap detalhado (programa)
- `docs/ROADMAP-GANTT.md` — Gantt visual

---

**Última atualização:** 2026-09-19
**Próxima revisão:** 2026-12 (trimestral)
