"""
osf_submit.py
Script para submeter pré-registros ao OSF (Open Science Framework) via API

Uso:
  1. Criar token em https://osf.io/settings/tokens/
  2. export OSF_TOKEN="seu-token-aqui"
  3. python3 osf_submit.py --prereg P01 --title "Meu título"

Ou submeter todos:
  python3 osf_submit.py --all
"""

import os
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
import sys

# Configurações
OSF_API_BASE = "https://api.osf.io/v2"
TIMEOUT = 30


def get_token():
    """Obtém token do environment."""
    token = os.environ.get("OSF_TOKEN")
    if not token:
        print("❌ OSF_TOKEN não encontrado no environment")
        print("   Configure: export OSF_TOKEN='seu-token'")
        print("   Obtenha em: https://osf.io/settings/tokens/")
        sys.exit(1)
    return token


def submit_preregistration(json_path: Path, dry_run: bool = False):
    """Submete um pré-registro ao OSF."""
    if not json_path.exists():
        print(f"❌ Arquivo não encontrado: {json_path}")
        return False

    with open(json_path) as f:
        payload = json.load(f)

    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    if dry_run:
        print(f"🧪 DRY RUN: {json_path.name}")
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:500] + "...")
        return True

    print(f"📤 Submetendo: {json_path.name}")
    print(f"   Título: {payload['data']['attributes']['title'][:60]}...")

    try:
        response = requests.post(
            f"{OSF_API_BASE}/registrations/",
            headers=headers,
            json=payload,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        result = response.json()

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
        }, indent=2, ensure_ascii=False))
        print(f"   Salvo: {output_path}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"   ❌ Erro HTTP: {e.response.status_code}")
        print(f"   {e.response.text[:300]}")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False


def submit_all(osf_dir: Path, dry_run: bool = False):
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
    print(f"Total: {len(results)} | Sucesso: {n_ok} | Falhas: {len(results) - n_ok}")
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} {r['file']}")

    return n_ok == len(results)


def main():
    parser = argparse.ArgumentParser(description="Submeter pré-registros ao OSF")
    parser.add_argument("--prereg", help="ID do pré-registro (P01, P02, ...)")
    parser.add_argument("--all", action="store_true", help="Submeter todos")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simular")
    parser.add_argument("--dir", type=Path, default="/workspace/docs/osf-json",
                        help="Diretório com JSONs")

    args = parser.parse_args()

    if args.all:
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
