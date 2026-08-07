# 📅 Roadmap Visual do Programa (Mermaid Gantt)

> **Programa:** Neurociência Educacional 2026-2030
> **Período total:** 60 meses
> **Atualizado:** 2026-08-06

## 🎯 Visão geral (Gantt Mermaid)

```mermaid
gantt
    title Programa de Pesquisa em Neurociência Educacional (2026-2030)
    dateFormat YYYY-MM
    axisFormat %b-%Y
    
    section P01 - Qualitativo
    P01 - Submissão CEP           :p01-cep, 2026-01, 3M
    P01 - Recrutamento            :p01-rec, after p01-cep, 2M
    P01 - Coleta T0 + T1          :p01-col, after p01-rec, 3M
    P01 - Análise Temática        :p01-anal, after p01-col, 3M
    P01 - Manuscrito + submissão  :p01-man, after p01-anal, 4M
    P01 - R1/R2 (revisão)         :p01-rev, after p01-man, 6M
    
    section P02 - ECR 2x4
    P02 - Submissão CEP           :p02-cep, 2026-06, 3M
    P02 - Recrutamento + baseline :p02-rec, after p02-cep, 2M
    P02 - Intervenção 8 sem       :p02-int, after p02-rec, 3M
    P02 - Coleta T1               :p02-col1, after p02-int, 1M
    P02 - Análise                 :p02-anal, after p02-col1, 3M
    P02 - Manuscrito              :p02-man, after p02-anal, 4M
    
    section P03 - EEG/ERP
    P03 - Submissão CEP           :p03-cep, 2026-09, 3M
    P03 - Setup EEG               :p03-set, after p03-cep, 3M
    P03 - Piloto EEG              :p03-pil, after p03-set, 2M
    P03 - Coleta (N=60)           :p03-col, after p03-pil, 6M
    P03 - Análise ERP             :p03-anal, after p03-col, 4M
    P03 - Manuscrito              :p03-man, after p03-anal, 5M
    
    section P04 - Transversal SEM
    P04 - Submissão CEP           :p04-cep, 2026-06, 3M
    P04 - Adaptação instrumentos  :p04-adap, after p04-cep, 2M
    P04 - Coleta (N=300-500)      :p04-col, after p04-adap, 6M
    P04 - CFA + SEM               :p04-sem, after p04-col, 4M
    P04 - Manuscrito              :p04-man, after p04-sem, 4M
    
    section P05 - Coorte Longitudinal
    P05 - Submissão CEP + setup   :p05-cep, 2026-01, 4M
    P05 - Recrutamento (N=200)    :p05-rec, after p05-cep, 3M
    P05 - Onda T1 (baseline)      :p05-t1, after p05-rec, 3M
    P05 - Onda T2                 :p05-t2, after p05-t1, 3M
    P05 - Onda T3 + EEG           :p05-t3, after p05-t2, 3M
    P05 - Onda T4                 :p05-t4, after p05-t3, 3M
    P05 - Onda T5 + EEG           :p05-t5, after p05-t4, 3M
    P05 - Análises longitudinais  :p05-anal, after p05-t5, 6M
    P05 - Manuscritos (3+)        :p05-man, after p05-anal, 12M
```

## 📊 Marcos críticos (Milestones)

```mermaid
gantt
    title Marcos Críticos do Programa
    dateFormat YYYY-MM
    
    section Marcos
    🎯 M0 - Programa iniciado              :milestone, m0, 2026-01, 0d
    📋 M6 - CEPs aprovados (P01, P02, P04)  :milestone, m6, 2026-06, 0d
    🔬 M9 - Primeiro piloto concluído      :milestone, m9, 2026-09, 0d
    📊 M12 - Análise P01 completa          :milestone, m12, 2026-12, 0d
    📝 M15 - 1º manuscrito submetido (P01) :milestone, m15, 2027-03, 0d
    🧠 M18 - EEG piloto OK (P03)           :milestone, m18, 2027-06, 0d
    📈 M24 - P02 e P04 com coleta pronta   :milestone, m24, 2027-12, 0d
    🧒 M30 - Coorte P05 baseline (N=200)   :milestone, m30, 2028-06, 0d
    📊 M36 - 2º ano coorte (P05 T2)        :milestone, m36, 2028-12, 0d
    🧠 M45 - EEG sub-estudo T3 (P05)       :milestone, m45, 2029-09, 0d
    📝 M48 - 5+ manuscritos submetidos     :milestone, m48, 2029-12, 0d
    🎓 M60 - Defesa de mestrado            :milestone, m60, 2030-12, 0d
```

## 🔄 Dependências entre projetos

```mermaid
graph TD
    A[P01 - Qualitativo] --> B[P02 - ECR]
    A --> C[P04 - SEM]
    D[P03 - EEG] --> E[P05 - Coorte]
    B --> E
    C --> E
    E --> F[Defesa Mestrado]
    
    style A fill:#27ae60
    style B fill:#f39c12
    style C fill:#9b59b6
    style D fill:#e67e22
    style E fill:#e74c3c
    style F fill:#3498db
```

## 📈 Marcos anuais

| Ano | Marcos principais |
|---|---|
| **2026** (M0-M12) | Setup + CEPs + P01 piloto + P02 setup + P05 baseline |
| **2027** (M13-M24) | P01 manuscrito + P02 coleta + P03 EEG piloto + P04 coleta |
| **2028** (M25-M36) | P02 manuscrito + P04 manuscrito + P03 coleta + P05 T2/T3 |
| **2029** (M37-M48) | P03 manuscrito + P05 T4 + EEG + manuscritos longitudinais |
| **2030** (M49-M60) | P05 T5 + EEG + manuscritos finais + defesa |

## ⚠️ Riscos críticos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| CEP atrasar | Média | Alto | Submissão antecipada; carta de justificativa |
| Attrition P05 | Alta (24% em 5 anos) | Alto | N inicial 250; estratégias retenção |
| Recrutamento lento | Média | Alto | 5+ escolas; parcerias múltiplas |
| Equipamento EEG quebrar | Baixa | Alto | Backup com 2 sistemas; seguro |
| Perda de orientadora | Baixa | Crítico | Co-orientação; comitê independente |

## 💰 Orçamento estimado (parcial)

| Item | Valor (R$) | Período |
|---|---|---|
| Bolsas (CAPES) | 84.000 | 24 meses |
| Material escolar (participantes) | 15.000 | 5 anos |
| EEG (manutenção + periféricos) | 20.000 | 5 anos |
| Software (MNE, R, etc) | 5.000 | 5 anos |
| Congressos | 25.000 | 5 anos |
| **Total** | **~150.000** | **5 anos** |
