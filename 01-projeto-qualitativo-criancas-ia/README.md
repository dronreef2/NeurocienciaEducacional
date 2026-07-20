# 📘 Projeto 01 — Vozes das crianças sobre tutores de IA generativa

> **Status:** 🟡 Em planejamento
> **Período previsto:** M1–M9 (2026-07 → 2027-03)
> **Dificuldade:** 🟢 Baixa
> **Paper-alvo principal:** *Computers & Education* (Qualis A1)
> **Linha-mãe:** Leitura + Neurociências (UFRN)
> **Orientadora:** Profa. Dra. Ângela Maria Chuvas Naschold

---

## ❓ Pergunta de pesquisa

**Como crianças de 8–11 anos percebem, interpretam e (re)negociam sua relação de aprendizagem com tutores de IA generativa em atividades escolares?**

### Perguntas secundárias
1. Que noção de "inteligência" e "confiança" as crianças constroem sobre o tutor de IA?
2. Quando e por que decidem seguir vs. ignorar as sugestões da IA?
3. Que estratégias metacognitivas emergem da interação com o tutor?
4. Como a relação com o tutor se diferencia da relação com o professor humano?

---

## 💡 Por que é inovadora

- **Inverte o foco**: do desempenho para a **experiência e metacognição** da criança.
- Inclui a **voz da criança** como dado central (alinhado à Convenção dos Direitos da Criança).
- Conecta com a discussão de "AI literacy" sem cair no moralismo pró/contra.
- **Em 2026**, com tutores generativos (Khanmigo, MagicSchool, etc.) entrando em escolas brasileiras, é a hora certa para escutar as crianças — antes que o mercado padronize a experiência.

---

## 🔬 Metodologia

### Tipo
Estudo qualitativo + componentes mistos. Triangulação de:
1. Entrevistas semiestruturadas (~30–45 min)
2. Sessões de "pensar em voz alta" (think-aloud) durante uso do tutor
3. Desenhos projetivos ("desenha como é estudar com o robô")
4. Diário de uso (2 semanas, observação participante)
5. Questionário breve para pais/professores

### Amostra
- **N** = 20–30 crianças (saturação teórica)
- **Faixa etária:** 8–11 anos (3º ao 5º ano)
- **Critérios de inclusão:** matriculadas em escola parceira, com consentimento dos pais e assentimento da criança
- **Critérios de exclusão:** crianças com diagnóstico neuropsiquiátrico formal (para não enviesar), ou que nunca usaram o tutor

### Instrumentos (em `instrumentos/`)
- `01-roteiro-entrevista.md` — roteiro semiestruturado
- `02-protocolo-thinkaloud.md` — protocolo de pensar em voz alta
- `03-prompt-desenho.md` — instrução para o desenho projetivo
- `04-diario-uso.md` — template do diário
- `05-questionario-pais.md`
- `06-questionario-professores.md`
- `07-tcle-pais.md` — Termo de Consentimento Livre e Esclarecido
- `08-tale-crianca.md` — Termo de Assentimento Livre e Esclarecido

### Análise
- **Análise temática reflexiva** (Braun & Clarke, 2022) — 6 fases
- Software: Taguette (grátis) → NVivo trial se necessário
- Triangulação: comparar falas, desenhos, diários, observações

---

## 📅 Cronograma detalhado

| Mês | Atividade |
|---|---|
| M1 | Reuniões com Angela, revisão de literatura, definição do tutor de IA a usar |
| M2 | Submissão ao CEP (Plataforma Brasil) |
| M3 | Cartas de anuência, piloto do roteiro (n=3 crianças) |
| M4 | Ajustes pós-piloto, treinamento da equipe de campo |
| M5 | Início das coletas formais |
| M6–M7 | Coletas (entrevistas + think-aloud + diário) |
| M8 | Análise temática (codificação + temas) |
| M9 | Submissão do paper (revista BR primeiro) |

---

## 🤝 Aspectos éticos (atenção especial)

1. **CEP via Plataforma Brasil** — UFRN (CAAE a obter)
2. **TCLE dos pais** + **TALE das crianças** (específicos para idade)
3. **Direito de desistência** a qualquer momento, sem prejuízo
4. **Anonimização** rigorosa (nomes fictícios, dados sensíveis protegidos)
5. **Cuidado com IA generativa**: evitar exposição a respostas inadequadas da IA durante o estudo
6. **Devolutiva** para a escola e para as famílias após o estudo
7. **Comunicação de achados** em linguagem acessível para as crianças participantes

---

## 📚 Leitura-base (rever `00-fundamentos/bibliografia-seminais.md`)

- ⬜ Braun & Clarke (2006, 2022) — análise temática
- ⬜ Kvale & Brinkmann (2015) — entrevistas qualitativas
- ⬜ Mollick (2023) — IA generativa
- ⬜ Kasneci et al. (2023) — ChatGPT e educação
- ⬜ Naschold (2017) — linha da orientadora
- ⬜ Creswell & Creswell (2018) — design qualitativo

---

## 📤 Entregáveis (deliverables)

- [ ] Protocolo CEP aprovado
- [ ] Banco de dados anonimizado (~20–30 entrevistas transcritas)
- [ ] Codificação completa em Taguette/NVivo
- [ ] Paper 1: revista brasileira (Qualis A1–A2)
- [ ] Paper 2 (versão expandida): revista internacional
- [ ] Apresentação SBPC
- [ ] Apresentação ICOMVE

---

## 📝 Issues abertas (a serem criadas)

- [x] ~~Definir qual tutor de IA generativa será usado~~ → **Khanmigo** (Khan Academy / Microsoft, gratuito para professores) como benchmark principal. MVP open-source será desenhado apenas se a pergunta de pesquisa exigir manipular comportamento do tutor, logs ou prompts de forma que a plataforma fechada não permita. *(Decidido em 2026-07-20)*
- [/] Negociar escola parceira — candidatas: Ipanguaçu, Currais Novos, Natal (parceria em andamento via Angela)
- [ ] Confirmar quais critérios éticos o CEP da UFRN exige para pesquisa com IA
- [ ] Verificar se há necessidade de seguro para participantes

---

> **Próxima ação imediata:** escrever `protocolo/projeto-detalhado.md` para submissão ao CEP/UFRN via Plataforma Brasil.
