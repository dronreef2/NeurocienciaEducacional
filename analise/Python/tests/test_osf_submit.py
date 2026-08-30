"""Testes para analise/Python/scripts/osf_submit.py."""
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Adicionar scripts/ ao path para importar o módulo
SCRIPTS_DIR = Path("/workspace/analise/Python/scripts")
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import osf_submit  # noqa: E402


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def v2_payload() -> dict:
    return {
        "data": {
            "type": "preregistration",
            "attributes": {
                "title": "Estudo piloto sobre IA e cognição",
                "description": "Pré-registro do estudo piloto.",
                "category": "project",
                "tags": ["IA", "cognição"],
                "subjects": ["Education"],
                "license": {
                    "name": "CC0 1.0 Universal",
                    "url": "https://creativecommons.org/publicdomain/zero/1.0/",
                },
            },
        }
    }


@pytest.fixture
def flat_payload() -> dict:
    return {
        "title": "ECR sobre gamificação",
        "description": "Pré-registro do ECR.",
        "category": "project",
        "tags": ["gamification", "ECR"],
        "subjects": ["Education"],
        "license": "CC0 1.0 Universal",
        "contributors": [
            {"name": "Pesquisador X", "email": "x@ufrn.br", "orcid": "0000-0000-0000-0000"}
        ],
        "pre_registration": {
            "type": "registered-report",
            "hypotheses": [{"id": "H1", "statement": "Hipótese 1"}],
            "design": {"type": "RCT", "sample_size": 200},
            "instruments": ["Stroop"],
            "analysis_plan": {"primary": "ANCOVA"},
        },
        "funding": "CAPES",
        "ethics": "CEP/UFRN #123",
        "date_created": "2026-08-13",
    }


@pytest.fixture
def v2_json(tmp_path, v2_payload) -> Path:
    p = tmp_path / "P01-osf.json"
    p.write_text(json.dumps(v2_payload))
    return p


@pytest.fixture
def flat_json(tmp_path, flat_payload) -> Path:
    p = tmp_path / "P02-osf.json"
    p.write_text(json.dumps(flat_payload))
    return p


# ============================================================================
# detect_format
# ============================================================================

class TestDetectFormat:
    def test_v2_format_detected(self, v2_payload) -> None:
        assert osf_submit.detect_format(v2_payload) == "v2"

    def test_flat_format_detected(self, flat_payload) -> None:
        assert osf_submit.detect_format(flat_payload) == "flat"

    def test_unknown_format(self) -> None:
        assert osf_submit.detect_format({"foo": "bar"}) == "unknown"


# ============================================================================
# validate_payload
# ============================================================================

class TestValidatePayload:
    def test_valid_v2(self, v2_payload) -> None:
        ok, errs = osf_submit.validate_payload(v2_payload)
        assert ok is True
        assert errs == []

    def test_valid_flat(self, flat_payload) -> None:
        ok, errs = osf_submit.validate_payload(flat_payload)
        assert ok is True
        assert errs == []

    def test_v2_missing_title(self, v2_payload) -> None:
        del v2_payload["data"]["attributes"]["title"]
        ok, errs = osf_submit.validate_payload(v2_payload)
        assert ok is False
        assert any("title" in e for e in errs)

    def test_v2_missing_type(self, v2_payload) -> None:
        del v2_payload["data"]["type"]
        ok, errs = osf_submit.validate_payload(v2_payload)
        assert ok is False
        assert any("type" in e for e in errs)

    def test_flat_missing_description(self, flat_payload) -> None:
        del flat_payload["description"]
        ok, errs = osf_submit.validate_payload(flat_payload)
        assert ok is False
        assert any("description" in e for e in errs)

    def test_title_too_short(self, v2_payload) -> None:
        v2_payload["data"]["attributes"]["title"] = "abc"
        ok, errs = osf_submit.validate_payload(v2_payload)
        assert ok is False
        assert any("curto" in e for e in errs)

    def test_title_too_long(self, v2_payload) -> None:
        v2_payload["data"]["attributes"]["title"] = "x" * 201
        ok, errs = osf_submit.validate_payload(v2_payload)
        assert ok is False
        assert any("longo" in e for e in errs)

    def test_unknown_format(self) -> None:
        ok, errs = osf_submit.validate_payload({"random": "data"})
        assert ok is False
        assert any("Desconhecido" in e or "desconhecido" in e for e in errs)


# ============================================================================
# flat_to_v2
# ============================================================================

class TestFlatToV2:
    def test_basic_conversion(self, flat_payload) -> None:
        v2 = osf_submit.flat_to_v2(flat_payload)
        assert v2["data"]["type"] == "preregistration"
        assert v2["data"]["attributes"]["title"] == flat_payload["title"]
        assert v2["data"]["attributes"]["description"] == flat_payload["description"]
        assert v2["data"]["attributes"]["tags"] == flat_payload["tags"]

    def test_license_normalized(self, flat_payload) -> None:
        v2 = osf_submit.flat_to_v2(flat_payload)
        assert v2["data"]["attributes"]["license"]["name"] == "CC0 1.0 Universal"
        assert "creativecommons" in v2["data"]["attributes"]["license"]["url"].lower()

    def test_contributors_preserved(self, flat_payload) -> None:
        v2 = osf_submit.flat_to_v2(flat_payload)
        assert "contributors" in v2["data"]["attributes"]
        assert v2["data"]["attributes"]["contributors"][0]["name"] == "Pesquisador X"

    def test_pre_registration_not_in_v2(self, flat_payload) -> None:
        v2 = osf_submit.flat_to_v2(flat_payload)
        assert "pre_registration" not in v2["data"]["attributes"]


# ============================================================================
# extract_rich_metadata
# ============================================================================

class TestExtractRichMetadata:
    def test_extracts_pre_registration(self, flat_payload) -> None:
        rich = osf_submit.extract_rich_metadata(flat_payload)
        assert "pre_registration" in rich
        assert "funding" in rich
        assert "ethics" in rich
        assert "contributors" in rich
        assert "date_created" in rich

    def test_extracts_hypotheses(self, flat_payload) -> None:
        rich = osf_submit.extract_rich_metadata(flat_payload)
        assert len(rich["pre_registration"]["hypotheses"]) == 1

    def test_empty_for_v2(self, v2_payload) -> None:
        rich = osf_submit.extract_rich_metadata(v2_payload)
        assert rich == {}


# ============================================================================
# load_and_validate (integração)
# ============================================================================

class TestLoadAndValidate:
    def test_load_v2(self, v2_json) -> None:
        v2, rich = osf_submit.load_and_validate(v2_json)
        assert v2["data"]["type"] == "preregistration"
        assert rich == {}

    def test_load_flat(self, flat_json) -> None:
        v2, rich = osf_submit.load_and_validate(flat_json)
        assert v2["data"]["type"] == "preregistration"
        assert "pre_registration" in rich
        assert "funding" in rich

    def test_invalid_file_raises(self, tmp_path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"foo": "bar"}))
        with pytest.raises(ValueError, match="Schema inválido"):
            osf_submit.load_and_validate(bad)


# ============================================================================
# submit_preregistration (dry-run + real)
# ============================================================================

class TestSubmitPreregistration:
    def test_dry_run_v2(self, v2_json) -> None:
        assert osf_submit.submit_preregistration(v2_json, dry_run=True) is True
        # Não deve criar *.submitted.json em dry-run
        assert not v2_json.with_suffix(".submitted.json").exists()

    def test_dry_run_flat_creates_metadata(self, flat_json) -> None:
        assert osf_submit.submit_preregistration(flat_json, dry_run=True) is True
        # Deve criar *.metadata.json companion
        meta = flat_json.with_suffix(".metadata.json")
        assert meta.exists()
        meta_data = json.loads(meta.read_text())
        assert "pre_registration" in meta_data

    def test_missing_file(self, tmp_path) -> None:
        assert osf_submit.submit_preregistration(tmp_path / "nope.json") is False

    def test_real_submission_calls_api(self, v2_json) -> None:
        """Submissão real deve chamar requests.post e salvar .submitted.json."""
        with patch("osf_submit.HAS_REQUESTS", True), \
             patch("osf_submit.requests") as mock_req, \
             patch("osf_submit.get_token", return_value="fake-token"):
            mock_req.post.return_value.json.return_value = {
                "data": {"id": "abc123"}
            }
            mock_req.post.return_value.raise_for_status = lambda: None

            assert osf_submit.submit_preregistration(v2_json) is True
            mock_req.post.assert_called_once()
            assert v2_json.with_suffix(".submitted.json").exists()

    def test_real_submission_http_error(self, v2_json) -> None:
        """Erro HTTP deve retornar False sem crash."""
        from requests.exceptions import HTTPError
        with patch("osf_submit.HAS_REQUESTS", True), \
             patch("osf_submit.requests") as mock_req, \
             patch("osf_submit.get_token", return_value="fake-token"):
            resp = mock_req.post.return_value
            resp.raise_for_status.side_effect = HTTPError(response=resp)
            resp.status_code = 401
            resp.text = "Unauthorized"

            assert osf_submit.submit_preregistration(v2_json) is False


# ============================================================================
# validate_all
# ============================================================================

class TestValidateAll:
    def test_validate_5_files(self, tmp_path) -> None:
        # Criar 5 JSONs válidos (3 v2 + 2 flat)
        for i in range(3):
            (tmp_path / f"P0{i + 1}-osf.json").write_text(json.dumps({
                "data": {
                    "type": "preregistration",
                    "attributes": {
                        "title": f"Estudo P0{i + 1} sobre neurociência educacional",
                        "description": "Descrição.",
                    },
                }
            }))
        for i in range(3, 5):
            (tmp_path / f"P0{i + 1}-osf.json").write_text(json.dumps({
                "title": f"Estudo P0{i + 1} sobre gamificação",
                "description": "Descrição.",
                "pre_registration": {"hypotheses": []},
            }))

        assert osf_submit.validate_all(tmp_path) is True

    def test_validate_empty_dir(self, tmp_path) -> None:
        assert osf_submit.validate_all(tmp_path) is False

    def test_validate_mixed_validity(self, tmp_path) -> None:
        (tmp_path / "P01-osf.json").write_text(json.dumps({
            "data": {
                "type": "preregistration",
                "attributes": {
                    "title": "Título válido do estudo",
                    "description": "Desc",
                },
            }
        }))
        (tmp_path / "P02-osf.json").write_text(json.dumps({"foo": "bar"}))

        assert osf_submit.validate_all(tmp_path) is False
