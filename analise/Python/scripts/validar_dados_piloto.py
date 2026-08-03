"""
validar_dados_piloto.py
Validações automatizadas dos dados piloto P01

Garante consistência, completude e qualidade dos dados antes da análise.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime


def validar_diarios(diarios_dir: Path) -> dict:
    """Valida os CSVs de diários."""
    results = {
        "arquivos_encontrados": 0,
        "arquivos_validos": 0,
        "erros": [],
        "warnings": [],
    }

    expected_columns = ["data", "participante_id", "duracao_min", "atividades", "dificuldades", "observacoes"]

    for csv_file in diarios_dir.glob("*.csv"):
        results["arquivos_encontrados"] += 1
        try:
            df = pd.read_csv(csv_file)
            for col in expected_columns:
                if col not in df.columns:
                    results["erros"].append(f"{csv_file.name}: coluna {col} ausente")
                    continue

            # Verificar duração negativa
            if (df["duracao_min"] < 0).any():
                results["erros"].append(f"{csv_file.name}: duracao_min negativa")

            # Verificar duração excessiva (> 4h)
            if (df["duracao_min"] > 240).any():
                results["warnings"].append(f"{csv_file.name}: duracao_min > 240 min")

            # Verificar range de datas (deve ser julho 2026)
            try:
                df["data_dt"] = pd.to_datetime(df["data"])
                mes_min = df["data_dt"].dt.month.min()
                mes_max = df["data_dt"].dt.month.max()
                if mes_min < 6 or mes_max > 8:
                    results["warnings"].append(f"{csv_file.name}: datas fora do esperado (jun-ago)")
            except Exception:
                results["warnings"].append(f"{csv_file.name}: formato de data inválido")

            # Calcular uso total
            total_uso = df["duracao_min"].sum()
            print(f"  ✓ {csv_file.name}: {len(df)} registros, {total_uso} min totais")

            results["arquivos_validos"] += 1

        except Exception as e:
            results["erros"].append(f"{csv_file.name}: {e}")

    return results


def validar_questionarios(q_dir: Path) -> dict:
    """Valida os CSVs de questionários."""
    results = {
        "arquivos_encontrados": 0,
        "arquivos_validos": 0,
        "erros": [],
    }

    for csv_file in q_dir.glob("*.csv"):
        results["arquivos_encontrados"] += 1
        try:
            df = pd.read_csv(csv_file)

            # Verificar IDs únicos
            if df["participante_id"].duplicated().any():
                results["erros"].append(f"{csv_file.name}: IDs duplicados")

            # Verificar ranges de variáveis
            if "conhecimento_ia" in df.columns:
                if (df["conhecimento_ia"] < 1).any() or (df["conhecimento_ia"] > 5).any():
                    results["erros"].append(f"{csv_file.name}: conhecimento_ia fora de [1,5]")

            if "preocupacao_ia" in df.columns:
                if (df["preocupacao_ia"] < 1).any() or (df["preocupacao_ia"] > 5).any():
                    results["erros"].append(f"{csv_file.name}: preocupacao_ia fora de [1,5]")

            print(f"  ✓ {csv_file.name}: {len(df)} respondentes")
            results["arquivos_validos"] += 1

        except Exception as e:
            results["erros"].append(f"{csv_file.name}: {e}")

    return results


def validar_codebook(cb_path: Path) -> dict:
    """Valida o codebook."""
    results = {"erros": [], "warnings": []}

    if not cb_path.exists():
        results["erros"].append("codebook-piloto.csv não encontrado")
        return results

    df = pd.read_csv(cb_path)
    required = ["codigo", "frequencia", "participantes", "descricao", "exemplos"]
    for col in required:
        if col not in df.columns:
            results["erros"].append(f"coluna {col} ausente")

    # Verificar que códigos são únicos
    if df["codigo"].duplicated().any():
        results["erros"].append("códigos duplicados")

    print(f"  ✓ codebook: {len(df)} códigos, {df['frequencia'].sum()} ocorrências totais")
    return results


def validar_transcricoes(trans_dir: Path) -> dict:
    """Valida arquivos de transcrição."""
    results = {
        "arquivos_encontrados": 0,
        "arquivos_validos": 0,
        "erros": [],
    }

    for txt_file in trans_dir.glob("*.txt"):
        results["arquivos_encontrados"] += 1
        try:
            content = txt_file.read_text()
            if len(content) < 100:
                results["erros"].append(f"{txt_file.name}: muito curto ({len(content)} chars)")
                continue

            if "Entrevistador" not in content and "P:" not in content:
                results["erros"].append(f"{txt_file.name}: não parece entrevista")

            # Verificar PII (CPF, telefone, email)
            pii_patterns = [
                ("\d{3}\.\d{3}\.\d{3}-\d{2}", "CPF"),
                ("\d{4,5}-\d{4}", "telefone"),
                ("@.*\.com", "email"),
            ]
            import re
            for pattern, name in pii_patterns:
                if re.search(pattern, content):
                    results["erros"].append(f"{txt_file.name}: possível {name} detectado!")

            print(f"  ✓ {txt_file.name}: {len(content)} chars")
            results["arquivos_validos"] += 1

        except Exception as e:
            results["erros"].append(f"{txt_file.name}: {e}")

    return results


def main():
    print("=" * 70)
    print(f"  VALIDAÇÃO DOS DADOS PILOTO P01 — {datetime.now().isoformat()}")
    print("=" * 70)

    base = Path("01-projeto-qualitativo-criancas-ia/dados/piloto")
    results = {}

    # Diários
    print("\n📅 DIÁRIOS:")
    results["diarios"] = validar_diarios(base / "diarios")

    # Questionários
    print("\n📋 QUESTIONÁRIOS:")
    results["questionarios"] = validar_questionarios(base / "questionarios")

    # Codebook
    print("\n📖 CODEBOOK:")
    results["codebook"] = validar_codebook(base / "codebook" / "codebook-piloto.csv")

    # Transcrições
    print("\n🎙️ TRANSCRIÇÕES:")
    results["transcricoes"] = validar_transcricoes(base / "transcricoes")

    # Relatório
    total_erros = sum(len(r.get("erros", [])) for r in results.values())
    total_warnings = sum(len(r.get("warnings", [])) for r in results.values())

    print("\n" + "=" * 70)
    if total_erros == 0:
        print(f"  ✅ VALIDAÇÃO OK — 0 erros, {total_warnings} warnings")
    else:
        print(f"  ❌ VALIDAÇÃO FALHOU — {total_erros} erros, {total_warnings} warnings")
        for key, r in results.items():
            for e in r.get("erros", []):
                print(f"     [{key}] {e}")
    print("=" * 70)

    # Salvar relatório
    output_path = Path("resultados/validacao_dados.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_erros": total_erros,
            "total_warnings": total_warnings,
            "results": results,
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  Relatório salvo: {output_path}")

    return 0 if total_erros == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
