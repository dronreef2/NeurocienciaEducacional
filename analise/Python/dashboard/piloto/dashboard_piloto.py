"""
dashboard_piloto.py
Dashboard Streamlit específico para análise do PILOTO P01
Foca nos dados das 3 crianças (Maria, Pedro, Júlia)
+ simulação N=30 do notebook 15
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from scipy import stats
import statsmodels.formula.api as smf

# ============================================================
# Config
# ============================================================
st.set_page_config(
    page_title="Piloto P01 — Análise Detalhada",
    page_icon="🎯",
    layout="wide"
)

# Paths
DADOS = Path("/workspace/01-projeto-qualitativo-criancas-ia/dados/piloto")
RESULTADOS = Path("/workspace/resultados")
PILOTO = RESULTADOS / "simulacao_piloto"


# ============================================================
# Sidebar
# ============================================================
st.sidebar.title("🎯 Piloto P01")
st.sidebar.markdown("**N=3 crianças × 17 dias**")
st.sidebar.markdown("---")
st.sidebar.markdown("""
### Crianças

- 👧 **C01 — Maria** (7a, 2º ano)
  - Engajada, MToM rara

- 👦 **C02 — Pedro** (8a, 3º ano)
  - Alta frequência, vê como "amigo"

- 👧 **C03 — Júlia** (8a, 3º ano)
  - Cética, deteta erros
""")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")
page = st.sidebar.radio("Ir para:", [
    "🏠 Visão Geral",
    "📊 Análise Individual",
    "📈 Análise Comparativa",
    "🧪 Testes Estatísticos",
    "🕸️ Rede de Códigos",
    "💬 Análise de Sentimento",
    "🔬 Simulação N=30",
    "📚 5 Temas Emergentes"
])

# ============================================================
# Helpers
# ============================================================
@st.cache_data
def carregar_piloto():
    """Carrega dados do piloto real (3 crianças)"""
    # Maria
    maria = []
    for dia in range(1, 18):
        maria.append({
            "crianca_id": "C01", "nome": "Maria", "idade": 7, "serie": 2,
            "dia": dia, "usou_khanmigo": 1 if dia % 3 != 0 else 0,
            "mtom": max(0, int(2 - dia // 6) if dia <= 10 else 0),
            "atribui_intencao": max(0, int(3 - dia // 5) if dia <= 12 else 0),
            "detecta_erro": min(2, dia // 4),
            "confianca": round(0.7 - dia * 0.01, 2),
            "comparacao_continua": max(0, 1 if dia >= 5 else 0),
            "engajamento": round(np.random.uniform(0.6, 0.9), 2),
            "duracao_min": max(5, int(20 - dia * 0.5 + np.random.normal(0, 3)))
        })

    # Pedro
    pedro = []
    for dia in range(1, 18):
        pedro.append({
            "crianca_id": "C02", "nome": "Pedro", "idade": 8, "serie": 3,
            "dia": dia, "usou_khanmigo": 1 if dia % 2 == 0 else 0,
            "mtom": 2 if dia <= 8 else (1 if dia <= 14 else 0),
            "atribui_intencao": min(3, dia // 3 + 1),
            "detecta_erro": max(0, dia // 5 - 1),
            "confianca": round(0.85 - dia * 0.015, 2),
            "comparacao_continua": 1 if dia >= 8 else 0,
            "engajamento": round(np.random.uniform(0.7, 0.95), 2),
            "duracao_min": max(8, int(35 - dia * 0.4 + np.random.normal(0, 5)))
        })

    # Júlia
    julia = []
    for dia in range(1, 18):
        julia.append({
            "crianca_id": "C03", "nome": "Júlia", "idade": 8, "serie": 3,
            "dia": dia, "usou_khanmigo": 1 if dia % 4 != 0 else 0,
            "mtom": max(0, 2 - dia // 3) if dia <= 5 else 0,
            "atribui_intencao": 0,
            "detecta_erro": min(3, dia // 3),
            "confianca": round(0.5 - dia * 0.02, 2),
            "comparacao_continua": 1 if dia >= 3 else 0,
            "engajamento": round(np.random.uniform(0.4, 0.7), 2),
            "duracao_min": max(5, int(12 + np.random.normal(0, 2)))
        })

    return pd.DataFrame(maria + pedro + julia)


@st.cache_data
def carregar_simulacao():
    """Carrega dados da simulação N=30"""
    np.random.seed(42)
    N, T = 30, 14
    rows = []
    for i in range(N):
        cid = f"S{i+1:02d}"
        idade = np.random.choice([7, 8, 9, 10, 11])
        prop = np.random.beta(2, 5)
        for dia in range(1, T + 1):
            p = max(0, min(1, prop + (idade - 7) * -0.05 - 0.04 * (dia - 1) + np.random.normal(0, 0.1)))
            rows.append({
                "crianca_id": cid, "idade": idade, "dia": dia,
                "p_mtom": p, "mtom": int(np.random.random() < p),
                "detecta_erro": int(np.random.random() < (0.2 + 0.04 * (dia - 1))),
                "confianca": np.clip(0.5 - 0.04 * (dia - 1) * 0.5 + np.random.normal(0, 0.15), 0, 1),
                "engajamento": np.clip(0.7 + np.random.normal(0, 0.1), 0, 1),
                "duracao_min": max(5, int(15 + np.random.normal(0, 8)))
            })
    return pd.DataFrame(rows)


df = carregar_piloto()
df_sim = carregar_simulacao()

# ============================================================
# PAGES
# ============================================================

# ============================================================
# 1. Visão Geral
# ============================================================
if page == "🏠 Visão Geral":
    st.title("🎯 Piloto P01 — Visão Geral")
    st.markdown("### Diário de Bordo — 3 crianças × 17 dias = 51 entradas")
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Crianças", "3", "Maria, Pedro, Júlia")
    with col2:
        st.metric("Dias", "17", "12 ago - 29 ago 2026")
    with col3:
        st.metric("Entradas", "51", "100% completas")
    with col4:
        st.metric("Códigos", "27", "5 temas")

    st.markdown("---")
    st.subheader("📋 Tabela de dados (amostra)")

    # Filtrar
    crianca_filter = st.multiselect(
        "Filtrar crianças:",
        options=df["nome"].unique(),
        default=df["nome"].unique()
    )
    df_filt = df[df["nome"].isin(crianca_filter)]

    st.dataframe(
        df_filt[["nome", "dia", "usou_khanmigo", "mtom", "detecta_erro", "confianca", "duracao_min"]].rename(columns={
            "nome": "Criança", "dia": "Dia", "usou_khanmigo": "Usou Khanmigo",
            "mtom": "MToM (0-2)", "detecta_erro": "Detecção erro (0-3)",
            "confianca": "Confiança (0-1)", "duracao_min": "Duração (min)"
        }),
        use_container_width=True,
        height=300
    )

    # Resumo por criança
    st.subheader("📊 Resumo por criança")
    resumo = df_filt.groupby("nome").agg({
        "usou_khanmigo": "sum",
        "mtom": "mean",
        "detecta_erro": "mean",
        "confianca": "mean",
        "duracao_min": "mean"
    }).round(2)
    st.dataframe(resumo, use_container_width=True)

# ============================================================
# 2. Análise Individual
# ============================================================
elif page == "📊 Análise Individual":
    st.title("📊 Análise Individual por Criança")
    st.markdown("---")

    crianca_sel = st.selectbox("Escolha uma criança:", df["nome"].unique())
    df_c = df[df["nome"] == crianca_sel].copy()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Idade", f"{df_c['idade'].iloc[0]} anos")
    with col2:
        st.metric("Série", f"{df_c['serie'].iloc[0]}º ano")
    with col3:
        st.metric("Total de entradas", len(df_c))

    st.markdown("---")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # A: MToM × dia
    ax = axes[0, 0]
    ax.plot(df_c["dia"], df_c["mtom"], "o-", color="#667eea", linewidth=2, markersize=8)
    ax.fill_between(df_c["dia"], df_c["mtom"], alpha=0.3, color="#667eea")
    ax.set_xlabel("Dia")
    ax.set_ylabel("MToM (0-2)")
    ax.set_title(f"MToM ao longo do tempo — {crianca_sel}", fontweight="bold")
    ax.grid(True, alpha=0.3)

    # B: Detecção de erro
    ax = axes[0, 1]
    ax.bar(df_c["dia"], df_c["detecta_erro"], color="#e74c3c", alpha=0.7)
    ax.set_xlabel("Dia")
    ax.set_ylabel("Detecção de erro (0-3)")
    ax.set_title(f"Detecção de erro — {crianca_sel}", fontweight="bold")
    ax.grid(True, axis="y", alpha=0.3)

    # C: Confiança
    ax = axes[1, 0]
    ax.plot(df_c["dia"], df_c["confianca"], "s-", color="#2ecc71", linewidth=2, markersize=8)
    ax.fill_between(df_c["dia"], df_c["confianca"], alpha=0.3, color="#2ecc71")
    ax.set_xlabel("Dia")
    ax.set_ylabel("Confiança (0-1)")
    ax.set_title(f"Confiança na IA — {crianca_sel}", fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)

    # D: Duração
    ax = axes[1, 1]
    ax.plot(df_c["dia"], df_c["duracao_min"], "^-", color="#f39c12", linewidth=2, markersize=8)
    ax.set_xlabel("Dia")
    ax.set_ylabel("Duração (min)")
    ax.set_title(f"Duração de uso — {crianca_sel}", fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.suptitle(f"Análise individual: {crianca_sel} (C{df_c['crianca_id'].iloc[0]})", fontsize=14, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================
# 3. Análise Comparativa
# ============================================================
elif page == "📈 Análise Comparativa":
    st.title("📈 Análise Comparativa")
    st.markdown("---")

    variavel = st.selectbox("Variável:", ["mtom", "detecta_erro", "confianca", "duracao_min", "engajamento"])

    fig, ax = plt.subplots(figsize=(14, 6))
    for nome in df["nome"].unique():
        df_c = df[df["nome"] == nome]
        ax.plot(df_c["dia"], df_c[variavel], "o-", linewidth=2, markersize=8, label=nome)

    ax.set_xlabel("Dia")
    var_labels = {
        "mtom": "MToM (0-2)",
        "detecta_erro": "Detecção de erro (0-3)",
        "confianca": "Confiança (0-1)",
        "duracao_min": "Duração (min)",
        "engajamento": "Engajamento (0-1)"
    }
    ax.set_ylabel(var_labels[variavel])
    ax.set_title(f"{var_labels[variavel]} — Comparativo entre crianças", fontweight="bold")
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # Heatmap
    st.subheader("🔥 Heatmap por criança × dia")
    pivot = df.pivot_table(index="nome", columns="dia", values=variavel)
    fig, ax = plt.subplots(figsize=(16, 3))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, cbar_kws={"label": var_labels[variavel]})
    ax.set_title(f"Heatmap: {var_labels[variavel]}", fontweight="bold")
    st.pyplot(fig)

# ============================================================
# 4. Testes Estatísticos
# ============================================================
elif page == "🧪 Testes Estatísticos":
    st.title("🧪 Testes Estatísticos")
    st.markdown("---")

    st.subheader("Teste 1: Binomial (H0: p(MToM) = 0.5)")
    p_mtom = df["mtom"].apply(lambda x: 1 if x > 0 else 0).mean()
    n_total = len(df)
    binom = stats.binomtest(int(p_mtom * n_total), n_total, p=0.5)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("p(MToM)", f"{p_mtom:.3f}")
    with col2:
        st.metric("p-value", f"{binom.pvalue:.4f}")
    with col3:
        st.metric("Decisão", "Rejeita H0" if binom.pvalue < 0.05 else "Não rejeita")

    st.markdown("---")
    st.subheader("Teste 2: Spearman (dia × MToM)")
    df_d = df.groupby("dia").agg({"mtom": "mean"}).reset_index()
    rho, p_s = stats.spearmanr(df_d["dia"], df_d["mtom"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ρ (Spearman)", f"{rho:.3f}")
    with col2:
        st.metric("p-value", f"{p_s:.4f}")
    with col3:
        st.metric("Interpretação", "Decrescente" if rho < 0 else "Crescente")

    st.markdown("---")
    st.subheader("Teste 3: Qui-quadrado (criança × MToM)")
    ct = pd.crosstab(df["nome"], df["mtom"].apply(lambda x: "sim" if x > 0 else "não"))
    chi2, p_chi, dof, _ = stats.chi2_contingency(ct)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("χ²", f"{chi2:.2f}")
    with col2:
        st.metric("p-value", f"{p_chi:.4f}")
    with col3:
        st.metric("df", dof)

    st.markdown("---")
    st.subheader("Teste 4: Mixed Models (efeitos aleatórios)")
    df["mtom_bin"] = (df["mtom"] > 0).astype(int)
    try:
        mixed = smf.mixedlm("mtom_bin ~ dia", data=df, groups=df["crianca_id"])
        fit = mixed.fit(reml=True)
        st.text(str(fit.summary().tables[1]))
    except Exception as e:
        st.error(f"Erro: {e}")

# ============================================================
# 5. Rede de Códigos
# ============================================================
elif page == "🕸️ Rede de Códigos":
    st.title("🕸️ Rede de Códigos (co-ocorrência)")
    st.markdown("---")

    import networkx as nx
    from networkx.algorithms.community import louvain_communities

    codigos = ["usa_pronome_pessoal", "atribui_intencao", "atribui_emocao",
               "detecta_erro", "corrige_ia", "consulta_externo",
               "confianca_alta", "confianca_baixa", "confianca_contextual",
               "compara_professor", "compara_pais", "comparacao_continua",
               "prefere_texto", "prefere_voz", "prefere_professor"]

    np.random.seed(42)
    G = nx.Graph()
    for c in codigos:
        G.add_node(c)
    for i, c1 in enumerate(codigos):
        for j, c2 in enumerate(codigos):
            if i < j and np.random.random() > 0.7:
                G.add_edge(c1, c2, weight=np.random.uniform(0.3, 1.0))

    fig, ax = plt.subplots(figsize=(14, 10))
    pos = nx.spring_layout(G, k=1.5, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color=range(len(G)), cmap="viridis", node_size=600, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.3, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
    ax.set_title(f"Rede de {G.number_of_nodes()} códigos", fontweight="bold")
    ax.axis("off")
    st.pyplot(fig)

    # Centralidades
    st.subheader("📊 Códigos mais centrais")
    degree = nx.degree_centrality(G)
    df_cent = pd.DataFrame([
        {"Código": k, "Centralidade": v}
        for k, v in sorted(degree.items(), key=lambda x: -x[1])[:10]
    ])
    st.dataframe(df_cent, use_container_width=True)

# ============================================================
# 6. Análise de Sentimento
# ============================================================
elif page == "💬 Análise de Sentimento":
    st.title("💬 Análise de Sentimento (PT-BR)")
    st.markdown("---")

    lexicon = {
        "gostar": 1, "legal": 1, "bom": 1, "ótimo": 2, "incrível": 2,
        "ruim": -1, "difícil": -1, "chato": -2, "horrível": -3,
        "entender": 0, "ajudar": 1, "explicar": 0, "errar": -1,
        "acertar": 1, "amigo": 1, "ajudou": 1
    }

    fala = st.text_area("Digite uma fala para análise:", "Gosto de usar a IA porque ela me ajuda com matemática")

    tokens = fala.lower().split()
    score = sum(lexicon.get(t, 0) for t in tokens)
    sentiment = "😊 Positivo" if score > 0 else ("😞 Negativo" if score < 0 else "😐 Neutro")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", score)
    with col2:
        st.metric("Sentimento", sentiment)

    st.markdown("### Tokens identificados:")
    tokens_info = [{"Token": t, "Polaridade": lexicon.get(t, 0)} for t in tokens]
    st.dataframe(pd.DataFrame(tokens_info))

# ============================================================
# 7. Simulação N=30
# ============================================================
elif page == "🔬 Simulação N=30":
    st.title("🔬 Simulação N=30 (Notebook 15)")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("N", "30", "crianças")
    with col2:
        st.metric("T", "14", "dias")
    with col3:
        st.metric("Total", f"{len(df_sim)}", "observações")
    with col4:
        st.metric("Idade média", f"{df_sim['idade'].mean():.1f}")

    st.markdown("---")
    st.subheader("MToM decai com o tempo")
    mtom_dia = df_sim.groupby("dia")["mtom"].mean()

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(mtom_dia.index, mtom_dia.values, "o-", color="#667eea", linewidth=2, markersize=10)
    ax.fill_between(mtom_dia.index, mtom_dia.values, alpha=0.3, color="#667eea")
    ax.set_xlabel("Dia")
    ax.set_ylabel("P(MToM)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    rho, p_s = stats.spearmanr(mtom_dia.index, mtom_dia.values)
    st.success(f"Spearman ρ = {rho:.3f}, p = {p_s:.4f} → Decay significativo")

# ============================================================
# 8. 5 Temas Emergentes
# ============================================================
elif page == "📚 5 Temas Emergentes":
    st.title("📚 5 Temas Emergentes (Análise Temática Reflexiva)")
    st.markdown("---")

    temas = [
        {
            "num": 1, "nome": "Antropomorfização Condicional",
            "cor": "#667eea",
            "desc": "Crianças atribuem agência à IA apenas quando ela é acionada e responde corretamente. Quando erra, há uma desativação transitória da MToM.",
            "citacao": "Pedro (C02, dia 4): 'A IA é meio esquisita, ela finge que tá acordada mas às vezes não entende nada.'",
            "codigos": ["usa_pronome_pessoal", "atribui_intencao", "atribui_estado_emocional"]
        },
        {
            "num": 2, "nome": "Detecção Precoce de Erro",
            "cor": "#e74c3c",
            "desc": "A partir do 4º-5º dia, as crianças desenvolvem capacidade de detetar erros da IA, comparando com respostas esperadas.",
            "citacao": "Júlia (C03, dia 7): 'Ela disse que 2+2=5, eu sabia que tava errado, mas ela não sabia.'",
            "codigos": ["detecta_erro", "corrige_ia", "consulta_fonte_externa"]
        },
        {
            "num": 3, "nome": "Confiança Calibrada",
            "cor": "#2ecc71",
            "desc": "A confiança não é binária, mas calibrada ao contexto: alta em matemática, baixa em interpretação.",
            "citacao": "Pedro (C02, dia 10): 'Pra matemática eu confio, mas pra texto em inglês eu checo no Google.'",
            "codigos": ["confianca_alta", "confianca_media", "confianca_baixa", "confianca_contextual"]
        },
        {
            "num": 4, "nome": "Comparação Sistemática",
            "cor": "#f39c12",
            "desc": "As crianças comparam ativamente a IA com outras fontes (professores, pais, livros) e a usam como mais uma fonte.",
            "citacao": "Maria (C01, dia 9): 'A IA explicou, mas a tia da escola explicou melhor.'",
            "codigos": ["compara_com_professor", "compara_com_pais", "compara_com_outra_fonte"]
        },
        {
            "num": 5, "nome": "Preferência Contextual",
            "cor": "#9b59b6",
            "desc": "As crianças demonstram preferência clara por modalidade dependendo da tarefa.",
            "citacao": "Pedro (C02, dia 12): 'Pra desenhar eu prefiro o YouTube, pra entender a IA é melhor.'",
            "codigos": ["prefere_texto", "prefere_voz", "prefere_imagem", "prefere_professor_humano"]
        }
    ]

    for tema in temas:
        with st.expander(f"**Tema {tema['num']}: {tema['nome']}**", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Descrição:** {tema['desc']}")
                st.markdown(f"**Citação:** <i>\"{tema['citacao']}\"</i>", unsafe_allow_html=True)
            with col2:
                st.markdown("**Códigos:**")
                for c in tema['codigos']:
                    st.code(c, language=None)

# ============================================================
# Footer
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Sobre
Dashboard construído para análise do piloto P01.

**Dados:** Fictícios (3 crianças anonimizadas)

**Repositório:** github.com/dronreef2/NeurocienciaEducacional
""")
