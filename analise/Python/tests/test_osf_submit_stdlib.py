"""Testes para osf_submit.py usando stdlib unittest (sem dependências externas)."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Adicionar scripts/ ao path
SCRIPTS_DIR = Path("/workspace/analise/Python/scripts")
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import osf_submit  # noqa: E402


class TestDetectFormat(unittest.TestCase):
    def test_v2_format(self) -> None:
        p = {"data": {"type": "preregistration", "attributes": {}}}
        self.assertEqual(osf_submit.detect_format(p), "v2")

    def test_flat_format(self) -> None:
        p = {"title": "x", "description": "y"}
        self.assertEqual(osf_submit.detect_format(p), "flat")

    def test_unknown(self) -> None:
        self.assertEqual(osf_submit.detect_format({"foo": "bar"}), "unknown")


class TestValidatePayload(unittest.TestCase):
    def test_valid_v2(self) -> None:
        p = {
            "data": {
                "type": "preregistration",
                "attributes": {
                    "title": "Estudo piloto sobre IA e cognição",
                    "description": "Descrição válida.",
                },
            }
        }
        ok, errs = osf_submit.validate_payload(p)
        self.assertTrue(ok, f"Esperado válido, erros: {errs}")
        self.assertEqual(errs, [])

    def test_valid_flat(self) -> None:
        p = {
            "title": "ECR sobre gamificação em crianças",
            "description": "Descrição.",
            "license": "CC0 1.0 Universal",
            "pre_registration": {"hypotheses": []},
        }
        ok, errs = osf_submit.validate_payload(p)
        self.assertTrue(ok, f"Esperado válido, erros: {errs}")

    def test_v2_missing_title(self) -> None:
        p = {"data": {"type": "preregistration", "attributes": {"description": "x"}}}
        ok, errs = osf_submit.validate_payload(p)
        self.assertFalse(ok)
        self.assertTrue(any("title" in e for e in errs))

    def test_v2_missing_type(self) -> None:
        p = {"data": {"attributes": {"title": "Titulo válido longo", "description": "x"}}}
        ok, errs = osf_submit.validate_payload(p)
        self.assertFalse(ok)
        self.assertTrue(any("type" in e for e in errs))

    def test_title_too_short(self) -> None:
        p = {
            "data": {
                "type": "preregistration",
                "attributes": {"title": "abc", "description": "x"},
            }
        }
        ok, errs = osf_submit.validate_payload(p)
        self.assertFalse(ok)
        self.assertTrue(any("curto" in e for e in errs))

    def test_unknown_format(self) -> None:
        ok, errs = osf_submit.validate_payload({"random": "data"})
        self.assertFalse(ok)
        self.assertTrue(any("esconhecido" in e.lower() for e in errs))


class TestFlatToV2(unittest.TestCase):
    def test_basic(self) -> None:
        flat = {
            "title": "Estudo X",
            "description": "Desc",
            "tags": ["a", "b"],
            "subjects": ["Education"],
            "license": "CC0 1.0 Universal",
        }
        v2 = osf_submit.flat_to_v2(flat)
        self.assertEqual(v2["data"]["type"], "preregistration")
        self.assertEqual(v2["data"]["attributes"]["title"], "Estudo X")
        self.assertEqual(v2["data"]["attributes"]["tags"], ["a", "b"])
        self.assertEqual(v2["data"]["attributes"]["license"]["name"], "CC0 1.0 Universal")

    def test_contributors_preserved(self) -> None:
        flat = {
            "title": "X",
            "description": "Y",
            "license": "CC0 1.0 Universal",
            "contributors": [{"name": "Z", "email": "z@ufrn.br"}],
        }
        v2 = osf_submit.flat_to_v2(flat)
        self.assertIn("contributors", v2["data"]["attributes"])
        self.assertEqual(v2["data"]["attributes"]["contributors"][0]["name"], "Z")

    def test_pre_registration_excluded(self) -> None:
        flat = {
            "title": "X",
            "description": "Y",
            "license": "CC0 1.0 Universal",
            "pre_registration": {"hypotheses": []},
        }
        v2 = osf_submit.flat_to_v2(flat)
        self.assertNotIn("pre_registration", v2["data"]["attributes"])


class TestExtractRichMetadata(unittest.TestCase):
    def test_extracts_known_keys(self) -> None:
        flat = {
            "title": "X",
            "description": "Y",
            "pre_registration": {"hypotheses": []},
            "funding": "CAPES",
            "ethics": "CEP #1",
            "contributors": [],
            "date_created": "2026-08-13",
            "data_availability": "OSF",
            "version": "1.0",
        }
        rich = osf_submit.extract_rich_metadata(flat)
        for key in [
            "pre_registration", "funding", "ethics", "contributors",
            "date_created", "data_availability", "version",
        ]:
            self.assertIn(key, rich)

    def test_v2_has_no_rich(self) -> None:
        v2 = {
            "data": {
                "type": "preregistration",
                "attributes": {"title": "X", "description": "Y"},
            }
        }
        self.assertEqual(osf_submit.extract_rich_metadata(v2), {})


class TestLoadAndValidate(unittest.TestCase):
    def _write(self, path: Path, payload: dict) -> Path:
        path.write_text(json.dumps(payload))
        return path

    def test_load_v2(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = self._write(
                Path(td) / "P01-osf.json",
                {
                    "data": {
                        "type": "preregistration",
                        "attributes": {
                            "title": "Estudo piloto sobre IA e cognição",
                            "description": "Descrição.",
                        },
                    }
                },
            )
            v2, rich = osf_submit.load_and_validate(p)
            self.assertEqual(v2["data"]["type"], "preregistration")
            self.assertEqual(rich, {})

    def test_load_flat(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = self._write(
                Path(td) / "P02-osf.json",
                {
                    "title": "ECR sobre gamificação",
                    "description": "Descrição.",
                    "license": "CC0 1.0 Universal",
                    "pre_registration": {"hypotheses": []},
                    "funding": "CAPES",
                },
            )
            v2, rich = osf_submit.load_and_validate(p)
            self.assertEqual(v2["data"]["type"], "preregistration")
            self.assertIn("pre_registration", rich)
            self.assertEqual(rich["funding"], "CAPES")

    def test_invalid_raises(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = self._write(Path(td) / "bad.json", {"foo": "bar"})
            with self.assertRaises(ValueError) as ctx:
                osf_submit.load_and_validate(p)
            self.assertIn("Schema inválido", str(ctx.exception))


class TestSubmitPreregistration(unittest.TestCase):
    def test_dry_run_v2(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "P01-osf.json"
            p.write_text(json.dumps({
                "data": {
                    "type": "preregistration",
                    "attributes": {
                        "title": "Estudo piloto sobre IA",
                        "description": "Desc",
                    },
                }
            }))
            self.assertTrue(osf_submit.submit_preregistration(p, dry_run=True))
            # Não deve criar .submitted.json em dry-run
            self.assertFalse(p.with_suffix(".submitted.json").exists())

    def test_dry_run_flat_creates_metadata(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "P02-osf.json"
            p.write_text(json.dumps({
                "title": "ECR sobre gamificação",
                "description": "Desc",
                "license": "CC0 1.0 Universal",
                "pre_registration": {"hypotheses": [{"id": "H1"}]},
            }))
            self.assertTrue(osf_submit.submit_preregistration(p, dry_run=True))
            # Deve criar .metadata.json
            meta = p.with_suffix(".metadata.json")
            self.assertTrue(meta.exists())
            self.assertIn("pre_registration", json.loads(meta.read_text()))

    def test_missing_file(self) -> None:
        self.assertFalse(osf_submit.submit_preregistration(Path("/nope/nope.json")))

    def test_real_submission_with_mock(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "P01-osf.json"
            p.write_text(json.dumps({
                "data": {
                    "type": "preregistration",
                    "attributes": {
                        "title": "Estudo piloto sobre IA",
                        "description": "Desc",
                    },
                }
            }))
            with patch("osf_submit.HAS_REQUESTS", True), \
                 patch("osf_submit.requests") as mock_req, \
                 patch("osf_submit.get_token", return_value="fake-token"):
                mock_resp = mock_req.post.return_value
                mock_resp.json.return_value = {"data": {"id": "abc123"}}
                mock_resp.raise_for_status = lambda: None
                self.assertTrue(osf_submit.submit_preregistration(p))
                mock_req.post.assert_called_once()
                self.assertTrue(p.with_suffix(".submitted.json").exists())


class TestValidateAll(unittest.TestCase):
    def test_5_valid_files(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            for i in range(3):
                (td_path / f"P0{i + 1}-osf.json").write_text(json.dumps({
                    "data": {
                        "type": "preregistration",
                        "attributes": {
                            "title": f"Estudo P0{i + 1} sobre neurociência educacional",
                            "description": "Descrição.",
                        },
                    }
                }))
            for i in range(3, 5):
                (td_path / f"P0{i + 1}-osf.json").write_text(json.dumps({
                    "title": f"Estudo P0{i + 1} sobre gamificação",
                    "description": "Descrição.",
                    "pre_registration": {"hypotheses": []},
                }))
            self.assertTrue(osf_submit.validate_all(td_path))

    def test_empty_dir(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            self.assertFalse(osf_submit.validate_all(Path(td)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
