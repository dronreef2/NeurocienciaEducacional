# 🗺️ Mapa Conceitual do Programa (Mermaid)

> **Visualização** das conexões entre os 5 projetos, papers, conceitos, e instituições parceiras.
> **Formato:** Mermaid (renderiza em GitHub, Notion, Obsidian, VS Code, etc.)
> **Uso:** compartilhar com a Angela, em slides, em papers como "framework figure".

---

## 🧭 Mapa-mestre (versão 1: projetos × instituições)

```mermaid
graph TB
    subgraph PESQUISADORA
        PESQ[Pesquisadora<br/>Mestranda PPGED/UFRN]
    end

    subgraph ORIENTADORA
        ORI[Profa. Dra.<br/>Ângela Naschold<br/>UFRN/CERES]
    end

    subgraph INSTITUIÇÕES
        UFRN[UFRN<br/>CERES · DEDUC]
        ICe[Instituto do Cérebro<br/>da UFRN]
        ESCOLAS[Escolas Parceiras<br/>Ipanguaçu<br/>Currais Novos]
        MEC[MEC<br/>EBED/PNED]
    end

    subgraph PROJETOS
        P01[P01<br/>Vozes das crianças<br/>sobre Khanmigo]
        P02[P02<br/>Gamificação<br/>+ autorregulação]
        P03[P03<br/>EEG leitura<br/>digital vs. papel]
        P04[P04<br/>IA generativa<br/>× FE]
        P05[P05<br/>Coorte<br/>longitudinal]
    end

    subgraph PUBLICAÇÕES
        PAP1[Computers & Education]
        PAP2[Learning and Instruction]
        PAP3[Dev. Cognitive Neuroscience]
        PAP4[Computers in Human Behavior]
        PAP5[Developmental Science]
    end

    PESQ -->|orienta| ORI
    ORI -->|orienta| PESQ
    ORI --> UFRN
    UFRN --> ICe
    UFRN --> ESCOLAS
    MEC --> EBED -.->|influencia| ESCOLAS

    PESQ --> P01
    PESQ --> P02
    PESQ --> P03
    PESQ --> P04
    PESQ --> P05

    P01 -->|usa plataforma| ESCOLAS
    P02 -->|testa app| ESCOLAS
    P03 -->|mede EEG| ICe
    P04 -->|avalia adolescentes| ESCOLAS
    P05 -->|acompanha longitudinal| ESCOLAS

    P01 --> PAP1
    P02 --> PAP2
    P03 --> PAP3
    P04 --> PAP4
    P05 --> PAP5
```

---

## 🧠 Mapa 2: conceitos-chave por projeto

```mermaid
graph LR
    subgraph P01[Projeto 01]
        P01C1[Metacognição]
        P01C2[AI Literacy]
        P01C3[Khanmigo]
        P01C4[Thematic Analysis]
    end

    subgraph P02[Projeto 02]
        P02C1[Autorregulação]
        P02C2[Gamificação<br/>extrínseca vs. intrínseca]
        P02C3[App prototipado]
    end

    subgraph P03[Projeto 03]
        P03C1[VWFA]
        P03C2[N170]
        P03C3[N400]
        P03C4[Leitura em tela]
    end

    subgraph P04[Projeto 04]
        P04C1[Cognitive Offloading]
        P04C2[FE Miyake 3 fatores]
        P04C3[IA Generativa]
        P04C4[Adolescentes]
    end

    subgraph P05[Projeto 05]
        P05C1[Maturação neural]
        P05C2[Trajetórias latentes]
        P05C3[Coorte]
        P05C4[5-12 anos]
    end

    P01C3 -->|mede| P01C1
    P01C3 --> P01C2
    P01C1 --> P01C4

    P02C3 -->|manipula| P02C2
    P02C2 -->|mede| P02C1

    P03C4 -->|mede| P03C1
    P03C4 --> P03C2
    P03C4 --> P03C3

    P04C3 -->|causa| P04C1
    P04C1 -->|mede| P04C2
    P04C2 -->|afeta| P04C4

    P05C4 -->|acompanha| P05C1
    P05C4 -->|acompanha| P05C3
    P05C1 -->|modela| P05C2
```

---

## 📚 Mapa 3: papers × projetos (relevância)

```mermaid
graph TB
    subgraph PAPERS
        D1[Dehaene 2010<br/>Reading in the Brain]
        D2[Diamond 2013<br/>Executive Functions]
        D3[Miyake 2000<br/>Unity of EF]
        D4[Hamari 2014<br/>Gamification]
        D5[Luck 2014<br/>ERP Technique]
        D6[Naschold 2017<br/>L+N]
        D7[Braun & Clarke 2022<br/>Thematic Analysis]
        D8[Mollick 2024<br/>Co-Intelligence]
        D9[Howard-Jones 2014<br/>Neuro + Ed]
        D10[Snowling & Hulme 2020<br/>Science of Reading]
    end

    subgraph PROJETOS
        P01[P01]
        P02[P02]
        P03[P03]
        P04[P04]
        P05[P05]
    end

    D1 -->|forte| P01
    D1 -->|forte| P03
    D1 -->|média| P05

    D2 -->|forte| P01
    D2 -->|forte| P04
    D2 -->|média| P05

    D3 -->|forte| P04
    D3 -->|média| P05

    D4 -->|forte| P02

    D5 -->|forte| P03
    D5 -->|forte| P05

    D6 -->|forte| P01
    D6 -->|forte| P02
    D6 -->|média| P05

    D7 -->|forte| P01

    D8 -->|forte| P01
    D8 -->|forte| P04

    D9 -->|transversal| P01
    D9 -->|transversal| P02
    D9 -->|transversal| P03
    D9 -->|transversal| P04
    D9 -->|transversal| P05

    D10 -->|forte| P01
    D10 -->|média| P03
    D10 -->|média| P05
```

---

## 🔬 Mapa 4: arcabouço teórico (relação entre conceitos)

```mermaid
graph TB
    subgraph FUNDAMENTOS
        NE[Neurociência<br/>Educacional]
        DC[Desenvolvimento<br/>Cognitivo]
        PS[Psicologia<br/>da Leitura]
        ET[EdTech]
    end

    subgraph CONSTRUTOS
        REC[Recycling<br/>Hypothesis<br/>Dehaene]
        FE[Funções<br/>Executivas]
        META[Metacognição]
        GAM[Gamificação]
        OFF[Cognitive<br/>Offloading]
        CI[AI<br/>Literacy]
    end

    subgraph METODOS
        AT[Análise<br/>Temática]
        EEG[EEG/ERP]
        SEM[Structural<br/>Equation Models]
        LGMM[Latent Growth<br/>Mixture Models]
    end

    NE --> REC
    NE --> FE
    NE --> EEG
    DC --> FE
    DC --> META
    PS --> REC
    PS --> FE
    ET --> GAM
    ET --> OFF
    ET --> CI

    REC --> P01
    REC --> P03
    FE --> P01
    FE --> P04
    FE --> P05
    META --> P01
    GAM --> P02
    OFF --> P04
    CI --> P01
    CI --> P04

    AT --> P01
    EEG --> P03
    EEG --> P05
    SEM --> P04
    SEM --> P05
    LGMM --> P05
```

---

## 🧬 Mapa 5: pipeline de pesquisa (workflow)

```mermaid
graph LR
    A[Leitura<br/>papers seminais] --> B[Nota de leitura<br/>+ aplicação]
    B --> C[Projeto<br/>detalhado]
    C --> D[Submissão<br/>CEP]
    D --> E{Parecer}
    E -->|aprovado| F[Coleta<br/>de dados]
    E -->|pendências| G[Resposta<br/>CEP]
    G --> E
    F --> H[Análise<br/>estatística]
    H --> I[Pré-registro<br/>análise]
    I --> J[Manuscrito]
    J --> K[Submissão<br/>revista]
    K --> L{Revisão}
    L -->|aceito| M[Publicação]
    L -->|revisões| N[Resposta<br/>revisores]
    N --> L
    M --> O[Devolutiva<br/>comunidade]
    O --> P[Próximo<br/>projeto]
    P --> A
```

---

## 🎯 Mapa 6: arcabouço temporal (5 anos)

```mermaid
gantt
    title Cronograma do Programa (2026-2030)
    dateFormat YYYY-MM-DD
    axisFormat %Y

    section P01 - Qualitativo
    Submissão CEP      :a1, 2026-08-01, 90d
    Coleta             :a2, after a1, 120d
    Análise            :a3, after a2, 90d
    Paper 1            :a4, after a3, 60d

    section P02 - Gamificação
    Construção app     :b1, 2026-10-01, 120d
    Submissão CEP      :b2, after b1, 90d
    Coleta             :b3, after b2, 120d
    Paper 2            :b4, after b3, 90d

    section P03 - EEG leitura
    Treinamento EEG    :c1, 2027-04-01, 120d
    Piloto             :c2, after c1, 60d
    Coleta principal   :c3, after c2, 180d
    Análise            :c4, after c3, 120d
    Paper 3            :c5, after c4, 90d

    section P04 - IA × FE
    Adaptação instrum. :d1, 2028-01-01, 90d
    Submissão CEP      :d2, after d1, 60d
    Coleta             :d3, after d2, 180d
    Paper 4            :d4, after d3, 120d

    section P05 - Coorte
    Edital fomento     :e1, 2028-06-01, 365d
    Onda 1 (5 anos)    :e2, after e1, 365d
    Onda 2 (6 anos)    :e3, after e2, 365d
    Onda 3 (7 anos)    :e4, after e3, 365d
    Onda 4 (8 anos)    :e5, after e4, 365d
    Onda 5 (9 anos)    :e6, after e5, 365d
```

---

## 🛠️ Como usar esses mapas

1. **No GitHub:** abra o `.md` direto, GitHub renderiza Mermaid automaticamente
2. **Em slides:** exporte o Mermaid como PNG (https://mermaid.live/)
3. **Em paper:** exporte como figura vetorial
4. **Em reunião com a Angela:** use o Mapa 1 ou 2 para apresentar
5. **Em GitHub Projects:** use como referência visual

---

> **Para editar:** abra no https://mermaid.live/ — tem editor visual + preview em tempo real.
