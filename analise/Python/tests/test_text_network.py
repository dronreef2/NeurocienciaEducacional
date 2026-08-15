"""Testes para neurociencia_edu.text._network."""
import networkx as nx
import pytest

from neurociencia_edu.text._network import co_occurrence_network


class TestCoOccurrenceNetwork:
    """Testes da rede de co-ocorrência."""

    def test_empty_documents(self) -> None:
        """Lista vazia deve retornar grafo vazio."""
        G = co_occurrence_network([])
        assert G.number_of_nodes() == 0
        assert G.number_of_edges() == 0

    def test_single_document(self) -> None:
        """Documento único com 1 palavra não cria arestas."""
        G = co_occurrence_network(["palavra_unica"])
        assert G.number_of_nodes() == 1
        assert G.number_of_edges() == 0

    def test_single_document_three_words(self) -> None:
        """Documento único com 3 palavras cria 3 pares (= 3 arestas)."""
        G = co_occurrence_network(["palavra1 palavra2 palavra3"])
        assert G.number_of_nodes() == 3
        assert G.number_of_edges() == 3  # (1,2), (1,3), (2,3)

    def test_co_occurrence_creates_edge(self) -> None:
        """Palavras no mesmo doc devem ter aresta."""
        G = co_occurrence_network(["a b", "a c", "b c"])
        assert G.has_edge("a", "b")
        assert G.has_edge("a", "c")
        assert G.has_edge("b", "c")

    def test_threshold_filters_edges(self) -> None:
        """Threshold alto deve filtrar arestas raras."""
        docs = ["a b"] + ["a c"] * 5
        G = co_occurrence_network(docs, threshold=0.3)
        assert G.number_of_edges() >= 1

    def test_returns_networkx_graph(self) -> None:
        """Resultado deve ser networkx.Graph."""
        G = co_occurrence_network(["a b c"])
        assert isinstance(G, nx.Graph)

    def test_node_attributes(self) -> None:
        """Nós devem ter atributo de frequência."""
        G = co_occurrence_network(["a a b", "a b c"])
        assert G.nodes["a"].get("frequency", 0) >= 2

    def test_handles_stopwords(self) -> None:
        """Deve remover stopwords comuns."""
        G = co_occurrence_network(["o a é b"], remove_stopwords=True)
        assert "o" not in G.nodes()
        assert "é" not in G.nodes()
        assert "a" not in G.nodes()  # "a" é stopword (artigo)
        assert "b" in G.nodes()
