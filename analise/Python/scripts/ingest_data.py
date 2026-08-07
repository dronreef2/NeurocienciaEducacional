"""
ingest_data.py
Pipeline de ingestão de dados brutos para o programa
Converte dados em diferentes formatos para o padrão BIDS-like do programa
"""

from pathlib import Path
import json
import pandas as pd
import argparse
import shutil
from datetime import datetime
import hashlib


# ============================================================
# Constantes
# ============================================================

DATA_STANDARDS = {
    "transcripts": {
        "format": "txt",
        "encoding": "utf-8",
        "delimiter": "paragraph",
        "required": ["participant_id", "interviewer", "child"],
    },
    "diary": {
        "format": "csv",
        "encoding": "utf-8",
        "delimiter": ",",
        "required_columns": ["data", "participante_id", "duracao_min"],
    },
    "questionnaire": {
        "format": "csv",
        "encoding": "utf-8",
        "delimiter": ",",
        "required_columns": ["participante_id"],
    },
    "eeg": {
        "format": "bids",
        "encoding": "utf-8",
        "required": ["sub-XX_task-Y_eeg.vhdr", "sub-XX_task-Y_eeg.vhdr"],
    },
}


# ============================================================
# Validações
# ============================================================

def validate_transcript(content: str) -> dict:
    """Valida transcrição."""
    issues = []

    if len(content) < 100:
        issues.append("Transcrição muito curta (<100 chars)")

    if "Entrevistador" not in content and "P:" not in content and "Criança" not in content:
        issues.append("Não parece uma entrevista (sem marcadores)")

    # Detecta PII
    import re
    pii_patterns = {
        r"\d{3}\.\d{3}\.\d{3}-\d{2}": "CPF",
        r"\d{4,5}-\d{4}": "telefone",
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}": "email",
    }
    for pattern, name in pii_patterns.items():
        if re.search(pattern, content):
            issues.append(f"Possível {name} detectado")

    return {"valid": len(issues) == 0, "issues": issues}


def validate_csv(filepath: Path, required_columns: list) -> dict:
    """Valida CSV."""
    issues = []
    try:
        df = pd.read_csv(filepath)

        # Colunas obrigatórias
        missing = set(required_columns) - set(df.columns)
        if missing:
            issues.append(f"Colunas faltando: {missing}")

        # Verificar IDs únicos (apenas para questionários; diários têm mesmo ID várias vezes)
        if "participante_id" in df.columns and required_columns == ["participante_id"]:
            if df["participante_id"].duplicated().any():
                issues.append("IDs duplicados")

        # Verificar ranges numéricos
        if "duracao_min" in df.columns:
            if (df["duracao_min"] < 0).any():
                issues.append("duracao_min negativa")
            if (df["duracao_min"] > 1440).any():
                issues.append("duracao_min > 24h")

    except Exception as e:
        issues.append(f"Erro ao ler: {e}")

    return {"valid": len(issues) == 0, "issues": issues}


# ============================================================
# Operações
# ============================================================

def compute_hash(filepath: Path) -> str:
    """Calcula SHA256 do arquivo."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def anonymize_text(content: str) -> str:
    """Remove/anonomiza PII básico."""
    import re
    # CPF
    content = re.sub(r"\d{3}\.\d{3}\.\d{3}-\d{2}", "[CPF_REMOVIDO]", content)
    # Telefone
    content = re.sub(r"\d{4,5}-\d{4}", "[TEL_REMOVIDO]", content)
    # Email
    content = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL_REMOVIDO]", content)
    return content


def ingest_transcripts(input_dir: Path, output_dir: Path) -> dict:
    """Ingere transcrições."""
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    for txt_file in input_dir.glob("*.txt"):
        content = txt_file.read_text()
        validation = validate_transcript(content)

        if validation["valid"]:
            # Anonimizar
            safe_content = anonymize_text(content)
            output_file = output_dir / txt_file.name
            output_file.write_text(safe_content)

            manifest.append({
                "file": txt_file.name,
                "hash_sha256": compute_hash(txt_file),
                "size_bytes": txt_file.stat().st_size,
                "ingested_at": datetime.now().isoformat(),
                "status": "ok",
            })
        else:
            manifest.append({
                "file": txt_file.name,
                "status": "failed",
                "issues": validation["issues"],
            })

    return {"type": "transcripts", "manifest": manifest, "n_ok": sum(1 for m in manifest if m["status"] == "ok")}


def ingest_csvs(input_dir: Path, output_dir: Path, type_name: str, required_columns: list) -> dict:
    """Ingere CSVs de questionários/diários."""
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    for csv_file in input_dir.glob("*.csv"):
        validation = validate_csv(csv_file, required_columns)

        if validation["valid"]:
            output_file = output_dir / csv_file.name
            shutil.copy2(csv_file, output_file)
            manifest.append({
                "file": csv_file.name,
                "hash_sha256": compute_hash(csv_file),
                "size_bytes": csv_file.stat().st_size,
                "ingested_at": datetime.now().isoformat(),
                "status": "ok",
            })
        else:
            manifest.append({
                "file": csv_file.name,
                "status": "failed",
                "issues": validation["issues"],
            })

    return {"type": type_name, "manifest": manifest, "n_ok": sum(1 for m in manifest if m["status"] == "ok")}


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Ingere dados brutos para o padrão do programa")
    parser.add_argument("--input", type=Path, required=True, help="Diretório de entrada")
    parser.add_argument("--output", type=Path, required=True, help="Diretório de saída")
    parser.add_argument("--type", choices=["transcripts", "diary", "questionnaire"],
                        required=True, help="Tipo de dado")
    parser.add_argument("--anonymize", action="store_true", help="Anonimizar (apenas transcripts)")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"❌ Diretório de entrada não existe: {args.input}")
        return 1

    print(f"=== INGESTÃO DE {args.type.upper()} ===")
    print(f"  De: {args.input}")
    print(f"  Para: {args.output}")
    print()

    if args.type == "transcripts":
        result = ingest_transcripts(args.input, args.output)
    elif args.type == "diary":
        result = ingest_csvs(args.input, args.output, "diary", ["data", "participante_id", "duracao_min"])
    elif args.type == "questionnaire":
        # Para questionários, IDs devem ser únicos (1 respondente = 1 linha)
        result = ingest_csvs(args.input, args.output, "questionnaire", ["participante_id"])
        # Validar IDs únicos separadamente
        from pathlib import Path as P
        for csv_file in args.input.glob("*.csv"):
            df_check = pd.read_csv(csv_file)
            if "participante_id" in df_check.columns and df_check["participante_id"].duplicated().any():
                print(f"  ⚠️ {csv_file.name}: IDs duplicados (esperado para questionários)")

    # Salvar manifesto
    manifest_path = args.output / "manifest.json"
    manifest_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    n_ok = result["n_ok"]
    n_total = len(result["manifest"])
    n_failed = n_total - n_ok

    print(f"✅ Ingestão concluída:")
    print(f"   Total: {n_total}")
    print(f"   Sucesso: {n_ok}")
    print(f"   Falhas: {n_failed}")

    if n_failed > 0:
        print()
        print("⚠️ Arquivos com problemas:")
        for m in result["manifest"]:
            if m["status"] == "failed":
                print(f"   - {m['file']}: {', '.join(m.get('issues', []))}")

    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
