# 🧠 Projeto 03 — EEG de leitura digital vs. papel em crianças (flagship)

> **Status:** ⚪ Planejado
> **Período previsto:** M12–M30 (2027-07 → 2028-12)
> **Dificuldade:** 🟠 Alta
> **Paper-alvo principal:** *Developmental Cognitive Neuroscience* (Qualis A1)
> **Linha-mãe:** Leitura + Neurociências (UFRN) — **projeto carro-chefe do programa**
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold
> **Parceiro-chave:** Instituto do Cérebro da UFRN (ICe) — acesso a EEG

---

## ❓ Pergunta de pesquisa

**Quais marcadores eletrofisiológicos de atenção e integração semântica (P300, N400, theta frontal) diferenciam a leitura de textos informativos em tela vs. papel em crianças de 8–10 anos, e como esses marcadores se relacionam com compreensão leitora e fluência de leitura?**

### Perguntas secundárias
1. A **complexidade do meio** (papel simples, tela simples, tela com hipertexto) modula a carga atencional durante a leitura?
2. Os efeitos do meio são **moderados** por idade, sexo, fluência de leitura ou exposição prévia a telas?
3. **Marcadores de maturação neural** (theta/beta ratio, conectividade em repouso) correlacionam-se com o desempenho em leitura digital?
4. O **tipo de texto** (narrativo vs. informativo) interage com o meio (papel vs. tela)?

---

## 💡 Por que é inovadora

- **Cruza dois campos** que raramente se cruzam: estudos cognitivos de leitura + EEG desenvolvimental
- **Em crianças brasileiras**, numa faixa etária (8–10) com janela desenvolvimental única (maturação pré-frontal)
- Inclui uma condição **ecologicamente válida**: **hipertexto com links** (que a criança realmente encontra na tela), ausente em estudos anteriores
- Permite falar de **plasticidade e janela desenvolvimental** — diferencial claro
- **Linha direta** com a expertise do ICe (acesso a EEG) e da Angela (leitura)

---

## 🔬 Metodologia

### Tipo
**Experimento within-subjects** 3 (meio: papel / tela-simples / tela-hipertexto) × 2 (tipo de texto: narrativo / informativo), com **registro EEG simultâneo**.

### Amostra
- **N** = 30–40 crianças (com poder para detectar efeitos ERPs médios)
- **Faixa etária:** 8–10 anos (3º ao 5º ano)
- **Critérios de inclusão:** fluência leitora mínima (≥ 50 palavras/min), sem histórico de epilepsia ou fotossensibilidade, sem uso de medicação psicoativa
- **Recrutamento:** escola parceira (transporte até o ICe)

### Equipamentos
- **EEG de 32 ou 64 canais** (disponível no ICe — verificar modelo)
- **Touca com gel seco** (preferível para crianças — facilita setup)
- **Tela calibrada** para leitura
- **Software de apresentação:** E-Prime ou PsychoPy

### Paradigma experimental
1. **Baseline (5 min):** EEG em repouso (olhos abertos/fechados) — para maturação
2. **Leitura estruturada (4 blocos × 6 textos):** cada condição (papel, tela-simples, tela-hipertexto) com 2 textos
3. **Questionários de compreensão** após cada texto
4. **Teste de fluência** (avaliação externa)

### Medidas
- **Componentes ERP:** P300 (saliência atencional), N400 (integração semântica), P600 (reparsing), theta frontal (controle atencional)
- **Conectividade funcional** em repouso (coerência inter-hemisférica)
- **Comportamentais:** compreensão, fluência, tempo de leitura
- **Auto-relato:** engajamento, esforço percebido, preferência

### Análise
- **Pré-processamento:** EEGLAB + ERPLAB (filtragem, ICA, rejeição de artefatos)
- **Análise ERP:** mass-univariate cluster-based permutation
- **Análise de conectividade:** coerência e PLV (phase-locking value) por banda
- **Modelos mistos** para integrar EEG + comportamento

---

## 📅 Cronograma (previsão)

| Mês | Atividade |
|---|---|
| M12 | Revisão de literatura; alinhamento com ICe; submissão CEP |
| M13 | Aprovação CEP; piloto do paradigma (n=5) — ajustes de UX |
| M14 | Aquisição / verificação de equipamentos EEG |
| M15 | Setup de pipeline EEG (EEGLAB/ERPLAB no ICe) |
| M18 | Coleta principal (n=30–40, ao longo de 2–3 meses) |
| M21 | Pré-processamento EEG; análises preliminares |
| M24 | Análise estatística completa; escrita do paper |
| M27 | Submissão à *Developmental Cognitive Neuroscience* (1ª tentativa) |
| M30 | Resubmissão ou submissão alternativa (Brain and Language) |

---

## 🤝 Aspectos críticos

- **Captação de sinal limpo em crianças** é o maior desafio: movimentos, cabelo, tédio
  - **Mitigação:** touca com gel seco, protocolo de 5 crianças piloto antes do estudo principal, equipe de 2 pessoas por coleta (1 com criança, 1 no EEG)
- **Acesso ao ICe:** alinhar formalmente com Prof. Antonio Pereira (vice-coordenador do curso de especialização da Angela) e com o diretor do ICe
- **Transporte das crianças:** precisa combinar com a escola + termo de transporte assinado pelos pais
- **Aspectos éticos:** cuidados extras com biossegurança, consentimento para filmagem/vídeo, debriefing

---

## 🧪 Pré-requisitos técnicos

- Curso/intensivo de EEG (Luck 2014 + Cohen 2014) — **3 meses de estudo**
- Treinamento hands-on no ICe (acompanhar uma coleta de outro pesquisador)
- Domínio de EEGLAB/ERPLAB ou MNE-Python
- Estatística: modelos mistos + correção de múltiplas comparações (cluster-permutation)

---

## 📚 Leitura-base

- **Luck, S. J. (2014).** *An Introduction to the ERP Technique* — **BÍBLIA**
- **Cohen, M. X. (2014).** *Analyzing Neural Time Series Data*
- Dehaene, S. (2010). *Reading in the Brain*
- Wolf, M. (2018). *Reader, Come Home*
- Clinton, V. (2019). "Reading from paper compared to screens" — meta-análise
- Stavanger, C. J. et al. (2024). "Screen reading and the brain in children" — *npj Science of Learning*
- **Naschold, A. (2017).** *Projeto Leitura + Neurociências*

Ver bibliografia completa em `00-fundamentos/bibliografia-seminais.md` (seção 🧠 e 📺).

---

## 🎯 Por que esse é o flagship

- **Maior impacto acadêmico** (journal A1 em neurociência)
- **Mais visível** (a Angela vai coautorar e isso pode virar capítulo de livro dela)
- **Gera mais papers derivados** (análises secundárias: maturação, gênero, hipertexto)
- **Diferencial competitivo** raro no Brasil (poucos labs com EEG + leitura + escola)

---

## 📂 Estrutura local

```
03-projeto-eeg-leitura-digital/
├── README.md                    ← este arquivo
├── instrumentos/                ← a criar (TCLE, TALE, tarefas, textos)
├── protocolo/                   ← a criar (submissão CEP, plano de biossegurança)
├── analise/                     ← a criar (pipeline EEG, scripts)
└── scripts/                     ← a criar (código de pré-processamento)
```

---

> **Próximo passo:** marcar reunião com a Angela + Prof. Antonio Pereira (ICe) para alinhar uso do equipamento e plano de coletas.
