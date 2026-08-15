"""Testes para neurociencia_edu.text._sentiment."""
import pytest

from neurociencia_edu.text._sentiment import analyze_sentiment


class TestAnalyzeSentiment:
    """Testes da análise de sentimento PT-BR."""

    def test_positive_text_high_score(self) -> None:
        """Texto positivo deve ter score > 0."""
        result = analyze_sentiment("Gosto de usar a IA porque me ajuda")
        assert result["score"] > 0
        assert result["sentiment"] == "positivo"

    def test_negative_text_low_score(self) -> None:
        """Texto negativo deve ter score < 0."""
        result = analyze_sentiment("A IA é chata e horrível")
        assert result["score"] < 0
        assert result["sentiment"] == "negativo"

    def test_neutral_text_zero_score(self) -> None:
        """Texto sem palavras do lexicon deve ter score = 0."""
        result = analyze_sentiment("xyz abc def")
        assert result["score"] == 0
        assert result["sentiment"] == "neutro"

    def test_empty_text(self) -> None:
        """Texto vazio deve retornar score=0."""
        result = analyze_sentiment("")
        assert result["score"] == 0
        assert result["sentiment"] == "neutro"

    def test_custom_lexicon(self) -> None:
        """Lexicon customizado deve sobrescrever o padrão."""
        custom = {"awesome": 5, "terrible": -5}
        pos = analyze_sentiment("awesome", lexicon=custom)
        neg = analyze_sentiment("terrible", lexicon=custom)
        assert pos["score"] == 5
        assert neg["score"] == -5

    def test_case_insensitive(self) -> None:
        """Análise deve ser case-insensitive."""
        result = analyze_sentiment("GOSTO DE TUDO")
        assert result["score"] > 0

    def test_returns_dict(self) -> None:
        """Resultado deve ser dict com chaves esperadas."""
        result = analyze_sentiment("teste")
        assert "score" in result
        assert "sentiment" in result
        assert "tokens_found" in result
