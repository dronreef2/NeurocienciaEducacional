"""Página 7: Modo Storytelling - Tour guiado pelos 5 projetos."""
import streamlit as st

st.set_page_config(page_title="Storytelling", page_icon="🎬", layout="wide")

# Inicializar estado de tour
if "tour_step" not in st.session_state:
    st.session_state.tour_step = 0

# Sidebar
with st.sidebar:
    st.markdown("## 🎬 Tour Guiado")
    st.markdown("5 atos · 1 epílogo")
    st.markdown("---")
    if st.button("⏮ Voltar", use_container_width=True):
        st.session_state.tour_step = max(0, st.session_state.tour_step - 1)
    if st.button("⏭ Próximo", use_container_width=True, type="primary"):
        st.session_state.tour_step = min(6, st.session_state.tour_step + 1)
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.tour_step = 0
    st.markdown("---")
    st.markdown(f"### Passo {st.session_state.tour_step + 1} de 7")

# Passos do tour
tour = [
    {
        "titulo": "🎬 Ato 1 — Contexto",
        "subtitulo": "Por que estudar IA na educação básica?",
        "conteudo": """
        ### Cenário atual (2025)

        - **73% das escolas** brasileiras já têm acesso a IA (CETIC, 2024)
        - **Pouco se sabe** sobre como crianças interagem com IA generativa
        - **Cognição social** infantil é construída na infância (Korkmaz, 2011)
        - **Há um gap** entre tecnologia e teoria da mente

        ### Pergunta de pesquisa

        > Como crianças do 2º ao 5º ano do Ensino Fundamental desenvolvem
        > cognição de teoria da mente ao usar IA generativa com mediação?

        ### Por que 5 projetos?

        - **P01**: Explorar qualitativamente (teoria fundamentada)
        - **P02**: Confirmar experimentalmente (ECR)
        - **P03**: Aprofundar com neurociência (EEG)
        - **P04**: Testar mecanismos (SEM)
        - **P05**: Acompanhar ao longo do tempo (LGCM)
        """,
    },
    {
        "titulo": "🎬 Ato 2 — P01 (IA e MToM)",
        "subtitulo": "O que as crianças pensam sobre IA?",
        "conteudo": """
        ### Pergunta de P01

        > Como crianças de 7-11 anos interpretam a cognição de IA generativa?

        ### Metodologia

        - **N** = 12-15 crianças (saturação)
        - **Desenho**: qualitativo exploratório (Análise Temática Reflexiva - ATR)
        - **Instrumentos**:
          1. TCLE + TALE (consentimento)
          2. Diário de bordo (17 dias com Khanmigo)
          3. Entrevistas semiestruturadas
          4. Questionários pré/pós
          5. Desenhos + produção textual

        ### 5 Temas emergentes (pilotagem)

        1. **Antropomorfização condicional** — atribui agência só quando IA acerta
        2. **Detecção precoce de erro** — a partir do 4º-5º dia
        3. **Confiança calibrada** — modulada por contexto
        4. **Comparação sistemática** — IA vs professor/pais
        5. **Preferência contextual** — texto/voz/imagem varia por tarefa

        ### Status

        ✅ Pré-registro OSF pronto
        ✅ Manuscrito (Computers & Education) pronto
        ✅ Dados piloto (3 crianças, 17 dias) disponíveis
        """,
    },
    {
        "titulo": "🎬 Ato 3 — P02 (Gamificação e FE)",
        "subtitulo": "Pontos e narrativa melhoram funções executivas?",
        "conteudo": """
        ### Pergunta de P02

        > Qual a efetividade da gamificação com pontos e narrativa
        > em crianças do 4º ano?

        ### Design Experimental (2×4)

        |  | Sem Pontos | Com Pontos |
        |---|---|---|
        | **Sem Narrativa** | Controle | Pontos |
        | **Com Narrativa** | Narrativa | Pontos + Narrativa |

        ### Medidas

        - **FE**: Stroop (inibição), TMT-B (flexibilidade), Digit Span (memória)
        - **Engajamento**: escala Likert + observacional
        - **N** = 200 (50 por célula)

        ### Hipóteses

        | H | Predição | d Cohen |
        |---|---|---|
        | H2.1 | Pontos → inibição | 0.20 |
        | H2.2 | Narrativa → memória | 0.25 |
        | H2.3 | Pontos × Narrativa → flexibilidade | 0.35 |
        | H2.4 | Engajamento medeia | efeito indireto |

        ### Status

        ✅ Pré-registro OSF pronto
        ✅ Dados sintéticos (N=200) gerados
        ⏳ Aguardando coleta (Q1 2027)
        """,
    },
    {
        "titulo": "🎬 Ato 4 — P03 (EEG — Tela vs Papel)",
        "subtitulo": "O cérebro lê diferente na tela?",
        "conteudo": """
        ### Pergunta de P03

        > Quais são as diferenças neurofisiológicas na leitura em
        > tela vs papel em crianças?

        ### Desenho

        - **Quase-experimental** within-subjects
        - **N** = 60 crianças (8-12 anos)
        - **EEG** 32-canais (Brain Vision ActiCHamp)
        - **Análise** ERP + topografia

        ### Componentes analisados

        | Componente | Latência | Função |
        |---|---|---|
        | N170 | 170ms | Processamento visual de palavras |
        | P300 | 300ms | Atenção |
        | N400 | 400ms | Semântica |
        | P600 | 600ms | Processamento sintático |

        ### Hipóteses

        - **H3.1**: Tela → N170 ↑ (processamento)
        - **H3.2**: Tela → P300 ↓ (atenção)
        - **H3.3**: Tela → N400 ↑ (semântica)
        - **H3.4**: Idade modula efeitos
        - **H3.5**: Comportamental: papel d=0.30 melhor

        ### Status

        ✅ Pré-registro OSF pronto
        ✅ Dados sintéticos EEG (npy) gerados
        ⏳ Aguardando aprovação comitê de ética
        """,
    },
    {
        "titulo": "🎬 Ato 5 — P04 (IA e FE - SEM)",
        "subtitulo": "Qual o mecanismo entre IA e funções executivas?",
        "conteudo": """
        ### Pergunta de P04

        > Quais processos explicam a relação entre uso de IA
        > generativa e funções executivas?

        ### Modelo Conceitual

        ```
        Uso de IA (X) ──a──> Engajamento (M) ──b──> FE (Y)
           │                                              ↑
           └──────c' (direto)─────────────────────────────┘
        ```

        ### Mediação + Moderação

        - **Mediação**: Engajamento medeia IA → FE
        - **Moderação**: Letramento parental (W) modula X→Y
        - **N** = 300-500 crianças (transversal)

        ### Hipóteses SEM

        | H | Caminho | Coef. esperado |
        |---|---|---|
        | H4.1 | a (X→M) | 0.30 |
        | H4.2 | b (M→Y) | 0.40 |
        | H4.3 | c' (X→Y) | 0.15 |
        | H4.4 | Indireto (a×b) | 0.12 |
        | H4.5 | W×X | 0.15 |

        ### Índices de ajuste

        - **CFI** ≥ 0.95
        - **TLI** ≥ 0.95
        - **RMSEA** ≤ 0.06
        - **SRMR** ≤ 0.08

        ### Status

        ✅ Pré-registro OSF pronto
        ✅ Dados sintéticos (N=400) gerados
        ⏳ Aguardando coleta
        """,
    },
    {
        "titulo": "🎬 Ato 6 — P05 (Coorte Longitudinal)",
        "subtitulo": "Como FE se desenvolvem ao longo do tempo?",
        "conteudo": """
        ### Pergunta de P05

        > Quais são as trajetórias de desenvolvimento de funções
        > executivas em crianças expostas à IA?

        ### Desenho

        - **Coorte prospectiva** de 5 anos (2026-2030)
        - **N** = 200 crianças (4-9 anos inicialmente)
        - **5 ondas** anuais
        - **LGCM** + sobreposição de hazards

        ### Medidas

        - **Inibição**: Stroop + Go/No-Go
        - **Memória de trabalho**: Digit Span + Corsi Block
        - **Flexibilidade**: TMT-B + Wisconsin Card Sorting
        - **Engajamento**: questionário
        - **Exposição à IA**: questionário parental

        ### Hipóteses LGCM

        - **H5.1**: Slope linear β1 = +0.5 DP/ano
        - **H5.2**: Variação individual no intercepto
        - **H5.3**: Variação individual no slope
        - **H5.4**: Cov(int, slope) < 0 (catch-up)

        ### Análise de Sobrevivência

        - Tempo até atingir critério de proficiência FE
        - Kaplan-Meier + Cox regression
        - Hazards concorrentes

        ### Status

        ✅ Pré-registro OSF pronto
        ✅ Dados sintéticos (5 ondas) gerados
        ⏳ Aguardando parcerias
        """,
    },
    {
        "titulo": "🎬 Epílogo — Impacto esperado",
        "subtitulo": "O que este programa pode contribuir?",
        "conteudo": """
        ### Impacto científico

        - **5 manuscritos** em revistas A1 (Computers & Education, NeuroImage, etc.)
        - **5 pré-registros** OSF
        - **3 métodos** distintos (ATR, ECR, EEG, SEM, LGCM)
        - **Reprodutibilidade** completa (código + dados abertos)

        ### Impacto educacional

        - **Política educacional** baseada em evidências
        - **Capacitação** de professores para uso crítico de IA
        - **Devolutivas** para escolas parceiras
        - **Material didático** (i18n PT/EN/ES)

        ### Impacto social

        - **Direitos de crianças** na era da IA (LGPD)
        - **Equidade digital** — perfil socioeconomico controlado
        - **Formação** de futuros pesquisadores (mestrado + doutorado)
        - **Disseminação** para sociedade

        ### Cronograma

        | Ano | Marcos |
        |---|---|
        | 2026 | Submissão P01 + aprovação comitê |
        | 2027 | Coleta P02 + P03 + publicação P01 |
        | 2028 | Análise P04 + publicação P02 + P03 |
        | 2029 | Análise P05 + publicação P04 |
        | 2030 | Publicação P05 + tese |

        ### Agradecimentos

        - **Orientadora**: Profa. Dra. Ângela M. C. Naschold (PPGED/UFRN)
        - **CERES/UFRN**: apoio institucional
        - **PPGED/UFRN**: programa de pós-graduação
        - **Escolas parceiras**: campo de pesquisa
        - **Família**: suporte emocional
        """,
    },
]

# Renderizar passo atual
step = tour[st.session_state.tour_step]

st.markdown(f"# {step['titulo']}")
st.markdown(f"## *{step['subtitulo']}*")
st.markdown("---")
st.markdown(step["conteudo"])

# Barra de progresso
progress = (st.session_state.tour_step + 1) / 7
st.progress(progress)
st.caption(f"Passo {st.session_state.tour_step + 1} de 7 — use a sidebar para navegar")
