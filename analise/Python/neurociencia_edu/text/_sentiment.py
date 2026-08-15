"""Análise de sentimento em português brasileiro."""
from __future__ import annotations

from typing import Optional

from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


DEFAULT_PT_LEXICON: dict[str, int] = {
    # Verbos (infinitivo + conjugações comuns)
    "gostar": 1, "gosto": 1, "gosta": 1, "gostamos": 1, "gostaram": 1,
    "ajudar": 1, "ajudo": 1, "ajuda": 1, "ajudou": 1, "ajudam": 1,
    "ensinar": 1, "ensina": 1, "ensinou": 1,
    "aprender": 1, "aprendo": 1, "aprende": 1, "aprendi": 1, "aprendeu": 1,
    "entender": 0, "entendo": 0, "entende": 0, "entendi": 0,
    "explicar": 0, "explico": 0, "explica": 0, "explicou": 0,
    "errar": -1, "erro": -1, "erra": -1, "errou": -1, "errado": -1,
    # Adjetivos
    "legal": 1, "bom": 1, "boa": 1, "bons": 1,
    "ótimo": 2, "ótima": 2,
    "incrível": 2, "maravilhoso": 3, "maravilhosa": 3,
    "ruim": -1, "ruins": -1, "difícil": -1, "difíceis": -1,
    "chato": -2, "chata": -2,
    "horrível": -3, "horríveis": -3,
    "confuso": -1, "confusa": -1, "aborrecido": -2, "aborrecida": -2,
    "divertido": 2, "divertida": 2,
    "amigo": 1, "amiga": 1, "amigos": 1, "amigas": 1,
    "dúvida": -0.5, "dúvidas": -0.5,
}


def analyze_sentiment(
    text: str,
    lexicon: Optional[dict[str, int]] = None,
) -> dict:
    """Analisa o sentimento de um texto em português.

    Args:
        text: Texto a ser analisado.
        lexicon: Lexicon customizado (opcional).

    Returns:
        Dict com score, sentiment, tokens_found.
    """
    lex = lexicon if lexicon is not None else DEFAULT_PT_LEXICON

    if not text or not text.strip():
        return {"score": 0, "sentiment": "neutro", "tokens_found": []}

    tokens = text.lower().split()
    score = 0
    found = []

    for token in tokens:
        clean = token.strip(".,!?;:()[]\"'")
        if clean in lex:
            score += lex[clean]
            found.append(clean)

    if score > 0:
        sentiment = "positivo"
    elif score < 0:
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    return {
        "score": score,
        "sentiment": sentiment,
        "tokens_found": found,
    }
