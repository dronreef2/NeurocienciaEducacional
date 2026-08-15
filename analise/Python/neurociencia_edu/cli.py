"""CLI tool para o pacote neurociencia_edu.

Fornece comandos para interagir com dados, catálogo e cache do programa.

Uso:
    neuro catalog list
    neuro catalog show P01_diarios_sinteticos
    neuro validate P01_diarios_sinteticos
    neuro cache list
    neuro cache clear
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import yaml

from neurociencia_edu.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================
# Catalog
# ============================================================

class Catalog:
    """Wrapper para o arquivo catalog.yaml de datasets."""

    def __init__(self, path: str | Path) -> None:
        """Carrega o catalog de um arquivo YAML.

        Args:
            path: Caminho para o arquivo catalog.yaml.
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Catalog não encontrado: {path}")
        with open(self.path) as f:
            self.data: dict = yaml.safe_load(f) or {}

    def list_datasets(self) -> list[str]:
        """Retorna nomes de todos os datasets.

        Returns:
            Lista de nomes de datasets.
        """
        return list(self.data.get("datasets", {}).keys())

    def show(self, name: str) -> dict:
        """Retorna metadata de um dataset.

        Args:
            name: Nome do dataset.

        Returns:
            Dict com metadata.

        Raises:
            KeyError: Se dataset não existir.
        """
        if name not in self.data.get("datasets", {}):
            raise KeyError(f"Dataset '{name}' não encontrado no catalog")
        return self.data["datasets"][name]

    def by_projeto(self, projeto: str) -> list[str]:
        """Filtra datasets por projeto.

        Args:
            projeto: ID do projeto (P01, P02, P03, P04, P05).

        Returns:
            Lista de datasets do projeto.
        """
        return [
            name for name, info in self.data.get("datasets", {}).items()
            if info.get("projeto") == projeto
        ]


# ============================================================
# Commands
# ============================================================

def cmd_catalog(args: argparse.Namespace) -> int:
    """Comando: catalog."""
    cat_path = Path("dados_sinteticos/catalog.yaml")
    if not cat_path.exists():
        # Tenta a partir do workspace
        cat_path = Path("/workspace/dados_sinteticos/catalog.yaml")
    if not cat_path.exists():
        print(f"❌ Catalog não encontrado", file=sys.stderr)
        return 1

    cat = Catalog(cat_path)

    if args.subcommand == "list":
        print("📊 Datasets disponíveis:")
        for name in cat.list_datasets():
            info = cat.show(name)
            print(f"  • {name} ({info.get('projeto', '?')}, {info.get('tipo', '?')})")
    elif args.subcommand == "show":
        try:
            info = cat.show(args.dataset)
            print(f"📋 {args.dataset}:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
        except KeyError as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
    elif args.subcommand == "by-projeto":
        datasets = cat.by_projeto(args.projeto)
        print(f"📊 Datasets do projeto {args.projeto}:")
        for name in datasets:
            print(f"  • {name}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Comando: validate."""
    from neurociencia_edu.validators import validar_colunas_obrigatorias
    import pandas as pd

    dataset_path = Path(args.path)
    if not dataset_path.exists():
        # Tenta resolver via catalog
        cat_path = Path("/workspace/dados_sinteticos/catalog.yaml")
        if cat_path.exists():
            cat = Catalog(cat_path)
            try:
                info = cat.show(args.path)
                dataset_path = Path("/workspace") / info["path"]
            except KeyError:
                pass

    if not dataset_path.exists():
        print(f"❌ Arquivo não encontrado: {args.path}", file=sys.stderr)
        return 1

    if dataset_path.suffix == ".csv":
        df = pd.read_csv(dataset_path)
        print(f"📊 Carregado: {dataset_path.name} ({len(df)} linhas, {len(df.columns)} colunas)")
        print("✓ CSV válido")
        return 0
    elif dataset_path.suffix == ".npy":
        import numpy as np
        arr = np.load(dataset_path)
        print(f"📊 Carregado: {dataset_path.name} (shape={arr.shape}, dtype={arr.dtype})")
        print("✓ NPY válido")
        return 0
    else:
        print(f"❌ Formato não suportado: {dataset_path.suffix}", file=sys.stderr)
        return 1


def cmd_cache(args: argparse.Namespace) -> int:
    """Comando: cache."""
    from neurociencia_edu.cache import get_cache

    cache = get_cache()

    if args.subcommand == "list":
        items = cache.list()
        if not items:
            print("📦 Cache vazio")
            return 0
        print(f"📦 {len(items)} itens no cache:")
        for item in items:
            print(f"  • {item['key'][:16]}... ({item['size_kb']:.1f} KB)")
    elif args.subcommand == "clear":
        n = cache.clear()
        print(f"🗑️  {n} itens removidos do cache")
    elif args.subcommand == "stats":
        stats = cache.stats()
        print(f"📊 Cache stats:")
        print(json.dumps(stats, indent=2))
    return 0


# ============================================================
# Main
# ============================================================

def main(argv: Optional[list[str]] = None) -> int:
    """Entry point do CLI."""
    parser = argparse.ArgumentParser(
        prog="neuro",
        description="CLI do Programa de Pesquisa em Neurociência Educacional",
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # catalog
    cat_parser = subparsers.add_parser("catalog", help="Gerenciar data catalog")
    cat_subs = cat_parser.add_subparsers(dest="subcommand")
    cat_subs.add_parser("list", help="Listar datasets")
    show_parser = cat_subs.add_parser("show", help="Mostrar metadata de dataset")
    show_parser.add_argument("dataset", help="Nome do dataset")
    proj_parser = cat_subs.add_parser("by-projeto", help="Filtrar por projeto")
    proj_parser.add_argument("projeto", help="ID do projeto (P01-P05)")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validar dataset")
    val_parser.add_argument("path", help="Caminho do dataset ou nome no catalog")

    # cache
    cache_parser = subparsers.add_parser("cache", help="Gerenciar cache")
    cache_subs = cache_parser.add_subparsers(dest="subcommand")
    cache_subs.add_parser("list", help="Listar itens")
    cache_subs.add_parser("clear", help="Limpar cache")
    cache_subs.add_parser("stats", help="Estatísticas")

    args = parser.parse_args(argv)

    if args.command == "catalog":
        return cmd_catalog(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "cache":
        return cmd_cache(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
