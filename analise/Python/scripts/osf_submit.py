"""
osf_submit.py
Script para submeter pré-registros ao OSF (Open Science Framework) via API v2

Auto-detecta formato do JSON:
- OSF API v2 (data.attributes.*)
- Formato flat custom (title, description, tags, license, contributors, pre_registration)

Quando encontra formato flat com bloco pre_registration rico (hipóteses, design,
análise), salva como arquivo *.metadata.json companion para upload no OSF
como arquivo suplementar da registration.

Uso:
  export OSF_TOKEN="seu-token-aqui"
  python3 osf_submit.py --all
  python3 osf_submit.py --all --dry-run  # valida sem submeter
  python3 osf_submit.py --prereg P01
  python3 osf_submit.py --validate        # só valida schema

Token: https://osf.io/settings/tokens/
"""
import os
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from urllib import request as urllib_request
from urllib.error import HTTPError as UrllibHTTPError

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None  # type: ignore[assignment]

# Config
OSF_API_BASE = "https://api.osf.io/v2"
TIMEOUT = 30
DEFAULT_DIR = "/workspace/docs/osf-json"


# ============================================================================
# Schema helpers
# ============================================================================

REQUIRED_OSF_V2_FIELDS = ["title", "description"]
REQUIRED_FLAT_FIELDS = ["title", "description"]

LICENSE_MAP = {
    "CC0 1.0 Universal": {
        "id": "cc0-1.0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "CC-BY 4.0": {
        "id": "cc-by-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
    "CC-BY-SA 4.0": {
        "id": "cc-by-sa-4.0",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "MIT License": {
        "id": "mit-license",
        "url": "https://opensource.org/licenses/MIT",
    },
    "Apache License 2.0": {
        "id": "apache-2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
}


def detect_format(payload: dict) -> str:
    """Detecta se o JSON está em formato OSF v2 ou flat custom."""
    if "data" in payload and "attributes" in payload.get("data", {}):
        return "v2"
    if "title" in payload and "description" in payload:
        return "flat"
    return "unknown"


def validate_payload(payload: dict) -> tuple[bool, list[str]]:
    """Valida payload contra schema mínimo.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    fmt = detect_format(payload)

    if fmt == "unknown":
        return False, [
            "Formato desconhecido. Esperado: OSF v2 (data.attributes.*) ou flat (title, description, ...)"
        ]

    if fmt == "v2":
        attrs = payload["data"]["attributes"]
        for field in REQUIRED_OSF_V2_FIELDS:
            if field not in attrs or not attrs[field]:
                errors.append(f"Campo obrigatório faltando: data.attributes.{field}")
        if "type" not in payload.get("data", {}):
            errors.append("Campo obrigatório faltando: data.type (deve ser 'preregistration')")
    else:  # flat
        for field in REQUIRED_FLAT_FIELDS:
            if field not in payload or not payload[field]:
                errors.append(f"Campo obrigatório faltando: {field}")

    # Sanity checks
    if fmt == "v2":
        attrs = payload["data"]["attributes"]
        title = attrs.get("title", "")
    else:
        title = payload.get("title", "")

    if len(title) < 10:
        errors.append(f"Título muito curto ({len(title)} chars, mínimo 10)")
    if len(title) > 200:
        errors.append(f"Título muito longo ({len(title)} chars, máximo 200)")

    return (len(errors) == 0, errors)


def flat_to_v2(flat: dict) -> dict:
    """Converte formato flat para OSF API v2.

    Preserva o bloco rico 'pre_registration' separadamente.
    """
    license_str = flat.get("license", "CC0 1.0 Universal")
    license_info = LICENSE_MAP.get(license_str, LICENSE_MAP["CC0 1.0 Universal"])

    v2 = {
        "data": {
            "type": "preregistration",
            "attributes": {
                "title": flat["title"],
                "description": flat["description"],
                "category": flat.get("category", "project"),
                "tags": flat.get("tags", []),
                "subjects": flat.get("subjects", []),
                "license": {
                    "name": license_str,
                    "url": license_info["url"],
                },
            },
        }
    }

    if "contributors" in flat:
        v2["data"]["attributes"]["contributors"] = flat["contributors"]

    return v2


def extract_rich_metadata(flat: dict) -> dict:
    """Extrai bloco pre_registration rico (hipóteses, design, análise)."""
    rich = {}
    for key in [
        "pre_registration",
        "design",
        "hypotheses",
        "instruments",
        "analysis_plan",
        "funding",
        "ethics",
        "data_availability",
        "contributors",
        "date_created",
        "date_modified",
        "version",
    ]:
        if key in flat:
            rich[key] = flat[key]
    return rich


# ============================================================================
# OSF API
# ============================================================================

def get_token() -> str:
    """Obtém token do environment."""
    token = os.environ.get("OSF_TOKEN")
    if not token:
        print("❌ OSF_TOKEN não encontrado no environment")
        print("   Configure: export OSF_TOKEN='seu-token'")
        print("   Obtenha em: https://osf.io/settings/tokens/")
        sys.exit(1)
    return token


def load_and_validate(json_path: Path) -> tuple[dict, dict]:
    """Carrega JSON, valida schema, retorna (payload_v2, rich_metadata).

    Args:
        json_path: caminho do JSON

    Returns:
        (payload_v2, rich_metadata) — rich_metadata é {} se nada relevante

    Raises:
        ValueError: se payload inválido
    """
    with open(json_path) as f:
        raw = json.load(f)

    is_valid, errors = validate_payload(raw)
    if not is_valid:
        raise ValueError(f"Schema inválido em {json_path.name}:\n  - " + "\n  - ".join(errors))

    fmt = detect_format(raw)
    if fmt == "flat":
        payload_v2 = flat_to_v2(raw)
        rich = extract_rich_metadata(raw)
    else:
        payload_v2 = raw
        rich = {}

    return payload_v2, rich


def submit_preregistration(json_path: Path, dry_run: bool = False, save_metadata: bool = True) -> bool:
    """Submete um pré-registro ao OSF.

    Args:
        json_path: caminho do JSON
        dry_run: se True, apenas simula e valida
        save_metadata: se True, salva bloco rico como *.metadata.json companion

    Returns:
        True se sucesso
    """
    if not json_path.exists():
        print(f"❌ Arquivo não encontrado: {json_path}")
        return False

    try:
        payload, rich = load_and_validate(json_path)
    except ValueError as e:
        print(f"❌ {e}")
        return False

    if dry_run:
        print(f"🧪 DRY RUN: {json_path.name}")
        print(f"   Título: {payload['data']['attributes']['title'][:60]}...")
        print(f"   Tags: {len(payload['data']['attributes'].get('tags', []))}")
        print(f"   Subjects: {len(payload['data']['attributes'].get('subjects', []))}")
        if rich:
            # Salvar metadata rica também no dry-run (idempotente)
            if save_metadata:
                meta_path = json_path.with_suffix(".metadata.json")
                with open(meta_path, "w") as f:
                    json.dump(rich, f, indent=2, ensure_ascii=False)
                print(f"   📎 Metadata rica salva: {meta_path.name} ({len(rich)} campos)")
            else:
                print(f"   Metadata rica disponível: {len(rich)} campos")
        return True

    # Submissão real — primeiro salvar metadata rica (antes da chamada à API)
    if rich and save_metadata:
        meta_path = json_path.with_suffix(".metadata.json")
        with open(meta_path, "w") as f:
            json.dump(rich, f, indent=2, ensure_ascii=False)
        print(f"   📎 Metadata rica salva: {meta_path.name}")

    # Submissão real
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    print(f"📤 Submetendo: {json_path.name}")
    print(f"   Título: {payload['data']['attributes']['title'][:60]}...")

    try:
        if HAS_REQUESTS:
            response = requests.post(
                f"{OSF_API_BASE}/registrations/",
                headers=headers,
                json=payload,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            result = response.json()
        else:
            # Fallback para urllib (caso requests não esteja disponível)
            data = json.dumps(payload).encode("utf-8")
            req = urllib_request.Request(
                f"{OSF_API_BASE}/registrations/",
                data=data,
                headers=headers,
                method="POST",
            )
            with urllib_request.urlopen(req, timeout=TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))

        reg_id = result["data"]["id"]
        reg_url = f"https://osf.io/{reg_id}"

        print(f"   ✅ Sucesso! ID: {reg_id}")
        print(f"   URL: {reg_url}")

        # Salvar resultado
        output_path = json_path.with_suffix(".submitted.json")
        output_path.write_text(json.dumps({
            "submitted_at": datetime.now().isoformat(),
            "registration_id": reg_id,
            "url": reg_url,
            "title": payload["data"]["attributes"]["title"],
            "rich_metadata_file": str(json_path.with_suffix(".metadata.json")) if rich else None,
        }, indent=2, ensure_ascii=False))
        print(f"   Salvo: {output_path}")
        return True

    except UrllibHTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        print(f"   ❌ Erro HTTP: {e.code}")
        print(f"   {body[:300]}")
        return False
    except Exception as e:
        # Captura também requests.exceptions.HTTPError quando HAS_REQUESTS=True
        if HAS_REQUESTS and hasattr(e, "response") and e.response is not None:
            print(f"   ❌ Erro HTTP: {e.response.status_code}")
            print(f"   {e.response.text[:300]}")
        else:
            print(f"   ❌ Erro: {e}")
        return False


def submit_all(osf_dir: Path, dry_run: bool = False) -> bool:
    """Submete todos os JSONs do diretório."""
    json_files = sorted(osf_dir.glob("P*-osf.json"))

    if not json_files:
        print(f"❌ Nenhum JSON encontrado em {osf_dir}")
        return False

    print(f"📋 Encontrados {len(json_files)} pré-registros\n")

    results = []
    for json_file in json_files:
        success = submit_preregistration(json_file, dry_run=dry_run)
        results.append({"file": json_file.name, "success": success})
        print()

    # Resumo
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    n_ok = sum(1 for r in results if r["success"])
    n_fail = len(results) - n_ok
    print(f"Total: {len(results)} | ✅ Sucesso: {n_ok} | ❌ Falhas: {n_fail}")
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} {r['file']}")

    if n_fail > 0:
        print("\n⚠️  Algumas submissões falharam. Verifique:")
        print("   1. OSF_TOKEN configurado? (export OSF_TOKEN='...')")
        print("   2. Token tem scope 'osf.full_write'?")
        print("   3. Payload válido? Rode --validate primeiro")

    return n_ok == len(results)


def validate_all(osf_dir: Path) -> bool:
    """Valida todos os JSONs sem submeter."""
    json_files = sorted(osf_dir.glob("P*-osf.json"))

    if not json_files:
        print(f"❌ Nenhum JSON encontrado em {osf_dir}")
        return False

    print(f"🔍 Validando {len(json_files)} pré-registros...\n")

    all_ok = True
    for json_file in json_files:
        try:
            with open(json_file) as f:
                raw = json.load(f)
            fmt = detect_format(raw)
            payload, rich = load_and_validate(json_file)
            n_meta = len(rich)
            print(f"  ✅ {json_file.name}  [formato: {fmt}, metadata rica: {n_meta} campos]")
        except ValueError as e:
            print(f"  ❌ {json_file.name}")
            for line in str(e).split("\n"):
                print(f"      {line}")
            all_ok = False

    print()
    if all_ok:
        print(f"✅ Todos os {len(json_files)} pré-registros são válidos!")
    else:
        print(f"❌ Alguns pré-registros têm problemas. Corrija antes de submeter.")
    return all_ok


def main():
    parser = argparse.ArgumentParser(
        description="Submeter pré-registros ao OSF (auto-detecta formato)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prereg", help="ID do pré-registro (P01, P02, ...)")
    parser.add_argument("--all", action="store_true", help="Submeter todos")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simular (não submete)")
    parser.add_argument("--validate", action="store_true", help="Apenas validar schema (não submete)")
    parser.add_argument(
        "--dir", type=Path, default=Path(DEFAULT_DIR),
        help=f"Diretório com JSONs (default: {DEFAULT_DIR})",
    )

    args = parser.parse_args()

    if args.validate:
        ok = validate_all(args.dir)
        sys.exit(0 if ok else 1)
    elif args.all:
        success = submit_all(args.dir, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    elif args.prereg:
        json_path = args.dir / f"{args.prereg}-osf.json"
        success = submit_preregistration(json_path, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
