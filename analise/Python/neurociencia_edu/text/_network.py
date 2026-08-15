"""Análise de rede de co-ocorrência."""
from __future__ import annotations

from typing import Iterable, Optional

import networkx as nx
from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


DEFAULT_STOPWORDS: set[str] = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "na", "no",
    "para", "por", "com", "sem", "é", "foi", "são",
    "e", "ou", "mas", "que", "se", "não", "sim",
}


def co_occurrence_network(
    documents: Iterable[str],
    threshold: float = 0.0,
    remove_stopwords: bool = False,
    stopwords: Optional[set[str]] = None,
) -> nx.Graph:
    """Constrói rede de co-ocorrência a partir de documentos.

    Args:
        documents: Iterable de strings.
        threshold: Limiar mínimo de peso normalizado.
        remove_stopwords: Se True, remove stopwords.
        stopwords: Set customizado de stopwords.

    Returns:
        networkx.Graph com nós = palavras, arestas = co-ocorrência.
    """
    docs = list(documents)
    sw = (stopwords if stopwords is not None else DEFAULT_STOPWORDS) if remove_stopwords else set()

    G = nx.Graph()
    pair_counts: dict[tuple[str, str], int] = {}
    word_counts: dict[str, int] = {}

    for doc in docs:
        tokens = [
            t.strip(".,!?;:()[]\"'").lower()
            for t in doc.split()
            if t.strip(".,!?;:()[]\"'").lower() not in sw
        ]
        tokens = [t for t in tokens if t]

        if not tokens:
            continue

        for token in tokens:
            word_counts[token] = word_counts.get(token, 0) + 1

        unique_tokens = list(set(tokens))
        for i, t1 in enumerate(unique_tokens):
            G.add_node(t1, frequency=word_counts[t1])
            for t2 in unique_tokens[i + 1:]:
                pair = tuple(sorted([t1, t2]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

    max_count = max(pair_counts.values()) if pair_counts else 1

    for (t1, t2), count in pair_counts.items():
        normalized_weight = count / max_count
        if normalized_weight >= threshold:
            G.add_edge(t1, t2, weight=count, normalized=normalized_weight)

    logger.info(
        f"Co-occurrence network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, "
        f"from {len(docs)} documents"
    )
    return G
