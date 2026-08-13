"""
Validators: Validadores de entrada e dados.

Fornece validadores para dados de pesquisa (LGPD), inputs de funções e
sanitização de PII.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd

from .exceptions import DataAnonymizationError, DataNotFoundError, DataValidationError
from .logging_config import get_logger

logger = get_logger(__name__)


# ============================================================
# Padrões de PII (Personal Identifiable Information)
# ============================================================

PII_PATTERNS = {
    "cpf": re.compile(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}"),
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone_br": re.compile(r"\(?\d{2}\)?\s?9?\d{4}-?\d{4}"),
    "rg": re.compile(r"\d{1,2}\.?\d{3}\.?\d{3}-?[0-9Xx]"),
    "cep": re.compile(r"\d{5}-?\d{3}"),
    "date_br": re.compile(r"\d{2}/\d{2}/\d{4}"),
    "url": re.compile(r"https?://[^\s]+"),
    "ipv4": re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
}


# ============================================================
# Funções públicas
# ============================================================

def validar_colunas_obrigatorias(
    df: pd.DataFrame,
    colunas: list[str],
    nome_dataset: str = "dataset",
) -> None:
    """Valida que o DataFrame tem as colunas obrigatórias.

    Args:
        df: DataFrame a validar.
        colunas: Lista de colunas obrigatórias.
        nome_dataset: Nome descritivo (para mensagens de erro).

    Raises:
        DataValidationError: se faltar alguma coluna.
    """
    if df is None:
        raise DataValidationError(f"{nome_dataset} é None")

    if not isinstance(df, pd.DataFrame):
        raise DataValidationError(
            f"{nome_dataset} deve ser DataFrame, recebido {type(df).__name__}"
        )

    if df.empty:
        raise DataValidationError(f"{nome_dataset} está vazio")

    faltantes = [c for c in colunas if c not in df.columns]
    if faltantes:
        raise DataValidationError(
            f"{nome_dataset} não tem colunas obrigatórias: {faltantes}",
            details={"present": list(df.columns), "missing": faltantes}
        )

    logger.debug(f"✓ {nome_dataset} validado: {len(df)} linhas, {len(df.columns)} colunas")


def validar_range(
    df: pd.DataFrame,
    coluna: str,
    minimo: Optional[float] = None,
    maximo: Optional[float] = None,
) -> None:
    """Valida que valores estão dentro de um range.

    Args:
        df: DataFrame.
        coluna: Coluna a validar.
        minimo: Valor mínimo (None = sem limite).
        maximo: Valor máximo (None = sem limite).

    Raises:
        DataValidationError: se houver valores fora do range.
    """
    if coluna not in df.columns:
        raise DataValidationError(f"Coluna '{coluna}' não existe")

    valores = df[coluna].dropna()
    if valores.empty:
        return

    if minimo is not None:
        abaixo = (valores < minimo).sum()
        if abaixo > 0:
            raise DataValidationError(
                f"{abaixo} valores abaixo do mínimo em '{coluna}': {minimo}",
                details={"min": float(valores.min()), "max": float(valores.max())}
            )

    if maximo is not None:
        acima = (valores > maximo).sum()
        if acima > 0:
            raise DataValidationError(
                f"{acima} valores acima do máximo em '{coluna}': {maximo}",
                details={"min": float(valores.min()), "max": float(valores.max())}
            )


def detectar_pii(texto: str) -> dict[str, list[str]]:
    """Detecta possíveis PII em um texto.

    Args:
        texto: Texto a analisar.

    Returns:
        Dict com tipo de PII -> lista de matches.
    """
    encontrados = {}
    for tipo, pattern in PII_PATTERNS.items():
        matches = pattern.findall(texto)
        if matches:
            encontrados[tipo] = matches
    return encontrados


def tem_pii(texto: str) -> bool:
    """Verifica se texto contém PII.

    Args:
        texto: Texto a verificar.

    Returns:
        True se contém PII.
    """
    return bool(detectar_pii(texto))


def anonimizar_texto(texto: str, substituir_por: str = "[REMOVIDO]") -> str:
    """Anonimiza PII em um texto.

    Args:
        texto: Texto a anonimizar.
        substituir_por: String substituta (default "[REMOVIDO]").

    Returns:
        Texto anonimizado.
    """
    resultado = texto
    for tipo, pattern in PII_PATTERNS.items():
        resultado = pattern.sub(substituir_por, resultado)
    return resultado


def anonimizar_dataframe(
    df: pd.DataFrame,
    colunas_sensiveis: list[str],
    metodo: str = "hash",
    sal: str = "neurociencia_edu_2026",
) -> pd.DataFrame:
    """Anonimiza colunas sensíveis de um DataFrame.

    Args:
        df: DataFrame original.
        colunas_sensiveis: Colunas a anonimizar.
        metodo: 'hash' (SHA256) ou 'remove' (drop).
        sal: Salt para hash (garante irreversibilidade).

    Returns:
        DataFrame anonimizado.

    Raises:
        DataAnonymizationError: se método desconhecido.
    """
    if metodo not in ("hash", "remove"):
        raise DataAnonymizationError(f"Método desconhecido: {metodo}")

    df_anon = df.copy()

    for col in colunas_sensiveis:
        if col not in df.columns:
            logger.warning(f"Coluna '{col}' não existe, pulando")
            continue

        if metodo == "hash":
            df_anon[col] = df_anon[col].astype(str).apply(
                lambda x: hashlib.sha256(f"{sal}{x}".encode()).hexdigest()[:16]
            )
            logger.info(f"Coluna '{col}' anonimizada via SHA256")
        else:  # remove
            df_anon = df_anon.drop(columns=[col])
            logger.info(f"Coluna '{col}' removida")

    return df_anon


def sanitizar_nome(nome: str) -> str:
    """Sanitiza nome para uso em filename/ID.

    Args:
        nome: Nome a sanitizar.

    Returns:
        Nome sanitizado (sem espaços, acentos, caracteres especiais).
    """
    import unicodedata

    # Remove acentos
    nome = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode("ASCII")
    # Substitui não-alfanuméricos por underscore
    nome = re.sub(r"[^a-zA-Z0-9]+", "_", nome)
    # Remove underscores duplicados
    nome = re.sub(r"_+", "_", nome).strip("_")
    return nome.lower()


def caminho_existe(path: Union[str, Path], criar: bool = False) -> Path:
    """Valida que um caminho existe, criando-o se necessário.

    Args:
        path: Path a validar.
        criar: Se True, cria o diretório.

    Returns:
        Path validado.

    Raises:
        DataNotFoundError: se não existir e criar=False.
    """
    path = Path(path)
    if not path.exists():
        if criar:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Diretório criado: {path}")
        else:
            raise DataNotFoundError(
                f"Caminho não encontrado: {path}",
                details={"parent": str(path.parent)}
            )
    return path
