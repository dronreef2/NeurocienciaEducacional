# 🏛️ Arquitetura AI — Diagrama Visual

> **Diagrama oficial** do AI Project Agent do Neurociência Educacional.
> Renderiza automaticamente em GitHub, GitLab, MkDocs, e Mermaid Live Editor.
> **Versão:** 1.0 — 2026-09-19

---

## 🎯 Diagrama principal (Mermaid)

```mermaid
graph TD
    ROOT["🧠 NEUROCIÊNCIA EDUCACIONAL<br/>AI PROJECT AGENT<br/><i>(root session / conductor)</i>"]
    
    ROOT --> P["🔬 PESQUISA<br/>CIENTÍFICA"]
    ROOT --> E["🛠️ ENGENHARIA"]
    ROOT --> G["📋 GESTÃO<br/>DO PROJETO"]
    
    P --> P1["literatura"]
    P --> P2["hipóteses"]
    P --> P3["metodologia"]
    
    E --> E1["código / dados"]
    E --> E2["pipelines"]
    E --> E3["testes"]
    
    G --> G1["issues / roadmap"]
    G --> G2["documentação"]
    G --> G3["status"]
    
    P --> V
    E --> V
    G --> V
    
    V["✅ VALIDAÇÃO / AUDITORIA"]
    V --> V1["schema"]
    V --> V2["testes"]
    V --> V3["científica (LGPD)"]
    V --> V4["honesta"]
    
    V --> OUT["📦 artefato<br/>reproduzível"]
    
    style ROOT fill:#1E40AF,color:#fff,stroke:#000,stroke-width:3px
    style P fill:#3B82F6,color:#fff,stroke:#000
    style E fill:#10B981,color:#fff,stroke:#000
    style G fill:#F59E0B,color:#fff,stroke:#000
    style V fill:#EF4444,color:#fff,stroke:#000,stroke-width:3px
    style OUT fill:#8B5CF6,color:#fff,stroke:#000,stroke-width:3px
```

---

## 🔄 Fluxo de trabalho típico

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant R as 🧠 Root (Mavis)
    participant P as 🔬 Pesquisa
    participant E as 🛠️ Engenharia
    participant G as 📋 Gestão
    participant V as ✅ Validação
    
    U->>R: "Submeter P01 a Computers & Education"
    
    R->>R: Mapear para: Gestão + Pesquisa
    
    par Paralelo
        R->>G: Verificar manuscrito + carta
        G-->>R: Draft da carta
    and
        R->>P: Revisar coerência científica
        P-->>R: Checklist de submissão
    end
    
    R->>E: Gerar PDF de visualizações
    E-->>R: figures_300dpi.zip
    
    R->>V: Checar LGPD + checklist journal
    V-->>R: Status final
    
    R->>U: Carta + figuras + checklist + status
    
    Note over R,U: Entrega honesta:<br/>o que mudou, validou, não pôde, risco
```

---

## 🔀 Mapa Domínios ↔ AGENTS.md

```mermaid
graph LR
    ROOT["AGENTS.md raiz"]
    
    subgraph "🔬 PESQUISA"
        P_AGENTS["01-.../AGENTS.md<br/>02-.../AGENTS.md<br/>03-.../AGENTS.md<br/>04-.../AGENTS.md<br/>05-.../AGENTS.md"]
    end
    
    subgraph "🛠️ ENGENHARIA"
        E_AGENTS["analise/Python/AGENTS.md<br/>analise/AGENTS.md<br/>pages/AGENTS.md<br/>dados_sinteticos/AGENTS.md"]
    end
    
    subgraph "📋 GESTÃO"
        G_AGENTS["docs/AGENTS.md<br/>docs/atas/AGENTS.md<br/>docs/osf-json/AGENTS.md"]
    end
    
    ROOT --> P_AGENTS
    ROOT --> E_AGENTS
    ROOT --> G_AGENTS
    
    P_AGENTS -.lê quando.-> PESQ["IA em pesquisa"]
    E_AGENTS -.lê quando.-> ENG["IA em código"]
    G_AGENTS -.lê quando.-> GES["IA em gestão"]
    
    style ROOT fill:#1E40AF,color:#fff
    style P_AGENTS fill:#3B82F6,color:#fff
    style E_AGENTS fill:#10B981,color:#fff
    style G_AGENTS fill:#F59E0B,color:#fff
```

---

## 📦 Saídas reproduzíveis

```mermaid
graph TD
    V["✅ Validação completa"]
    
    V --> A1["📄 PDF relatório"]
    V --> A2["🌐 Dashboard"]
    V --> A3["📊 Figura 300dpi"]
    V --> A4["📋 Tabela CSV"]
    V --> A5["🔗 Pré-registro OSF"]
    V --> A6["📝 Manuscrito"]
    V --> A7["📜 Ata"]
    
    A1 -.seed=42.-> REPRO["🔁 Reproduzível"]
    A2 -.git+pages.-> REPRO
    A3 -.notebook.-> REPRO
    A4 -.pipeline.-> REPRO
    A5 -.osf_submit.py.-> REPRO
    A6 -.Quarto+manual.-> PARCIAL["⚠️ Parcial"]
    A7 -.humano-espec.-> NAO["❌ Não"]
    
    style V fill:#EF4444,color:#fff
    style REPRO fill:#10B981,color:#fff
    style PARCIAL fill:#F59E0B,color:#fff
    style NAO fill:#6B7280,color:#fff
```

---

## 📊 Métricas da arquitetura atual

| Métrica | Valor |
|---|---|
| **Domínios** | 3 (Pesquisa, Engenharia, Gestão) |
| **Sub-áreas por domínio** | 3 cada = 9 |
| **AGENTS.md arquivos** | 11 |
| **Skills carregáveis** | 20+ |
| **Outputs reproduzíveis** | 6 tipos |
| **Validações** | 4 tipos |
| **Linhas de orquestração** | ~300 (este doc) |

---

## 🔗 Links

- [`docs/AI-ARCHITECTURE.md`](AI-ARCHITECTURE.md) — versão completa em texto
- [`AGENTS.md`](../AGENTS.md) — visão geral
- [`docs/AGENTS-SYSTEM.md`](AGENTS-SYSTEM.md) — sistema multi-AGENTS

---

**Última atualização:** 2026-09-19
