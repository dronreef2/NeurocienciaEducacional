"""Serializers para conversão numpy → tipos Python nativos."""
from __future__ import annotations

import json
from typing import Any

import numpy as np


def convert_numpy(obj: Any) -> Any:
    """Converte tipos numpy para tipos Python nativos.

    Args:
        obj: Qualquer objeto que possa conter tipos numpy.

    Returns:
        Versão do objeto com tipos Python nativos.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        converted = [convert_numpy(item) for item in obj]
        return type(obj)(converted) if isinstance(obj, tuple) else converted
    return obj


def to_json_safe(obj: Any) -> Any:
    """Converte um objeto para um formato seguro para json.dumps."""
    converted = convert_numpy(obj)

    def _make_safe(o: Any) -> Any:
        if isinstance(o, dict):
            return {str(k): _make_safe(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_make_safe(item) for item in o]
        if isinstance(o, (str, int, float, bool)) or o is None:
            return o
        return str(o)

    return _make_safe(converted)


def save_json(data: Any, path: str) -> None:
    """Salva dados em arquivo JSON, convertendo tipos numpy."""
    from pathlib import Path
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    safe = to_json_safe(data)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(safe, f, ensure_ascii=False, indent=2)
