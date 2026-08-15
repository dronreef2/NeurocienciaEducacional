"""Testes para neurociencia_edu.io._serializers."""
import numpy as np
import pytest

from neurociencia_edu.io._serializers import convert_numpy, to_json_safe


class TestConvertNumpy:
    """Testes do conversor de tipos numpy para JSON."""

    def test_numpy_int_to_python_int(self) -> None:
        """np.int64 deve virar int Python."""
        result = convert_numpy(np.int64(42))
        assert result == 42
        assert isinstance(result, int)

    def test_numpy_float_to_python_float(self) -> None:
        """np.float64 deve virar float Python."""
        result = convert_numpy(np.float64(3.14))
        assert isinstance(result, float)
        assert abs(result - 3.14) < 1e-10

    def test_numpy_array_to_list(self) -> None:
        """np.ndarray deve virar list."""
        arr = np.array([1, 2, 3])
        result = convert_numpy(arr)
        assert result == [1, 2, 3]
        assert isinstance(result, list)

    def test_dict_with_numpy_values(self) -> None:
        """Dict com valores numpy deve ser convertido."""
        d = {"a": np.int64(1), "b": np.array([2, 3])}
        result = convert_numpy(d)
        assert result == {"a": 1, "b": [2, 3]}

    def test_nested_structure(self) -> None:
        """Estruturas aninhadas devem ser convertidas."""
        data = {"x": [{"y": np.float64(1.5)}]}
        result = convert_numpy(data)
        assert result == {"x": [{"y": 1.5}]}

    def test_none_and_strings_unchanged(self) -> None:
        """None, str, int nativos passam inalterados."""
        assert convert_numpy(None) is None
        assert convert_numpy("hello") == "hello"
        assert convert_numpy(42) == 42

    def test_to_json_safe_roundtrip(self) -> None:
        """to_json_safe deve produzir JSON serializável."""
        import json
        data = {"values": np.array([1.0, 2.0, 3.0]), "label": "test"}
        safe = to_json_safe(data)
        json_str = json.dumps(safe)
        assert "test" in json_str
        assert "1.0" in json_str
