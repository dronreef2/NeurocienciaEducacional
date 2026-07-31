"""
neurociencia_edu.io.bids
Funções para trabalhar com datasets BIDS (Brain Imaging Data Structure).
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_bids_dataset(bids_root: str | Path) -> dict:
    """Carrega estrutura de um dataset BIDS.

    Args:
        bids_root: Diretório raiz do dataset BIDS.

    Returns:
        Dict com a estrutura do dataset (participants, modalities).
    """
    bids_root = Path(bids_root)
    if not bids_root.exists():
        raise FileNotFoundError(f"Diretório BIDS não encontrado: {bids_root}")

    dataset = {
        "root": str(bids_root),
        "participants": participant_ids(bids_root),
        "modalities": {},
    }

    # Detectar modalidades
    for modality_dir in bids_root.iterdir():
        if modality_dir.is_dir() and not modality_dir.name.startswith("."):
            if modality_dir.name in ["eeg", "meg", "ieeg", "anat", "dwi", "func"]:
                dataset["modalities"][modality_dir.name] = _list_subject_files(modality_dir)

    logger.info(f"BIDS dataset carregado: {len(dataset['participants'])} participantes")
    return dataset


def participant_ids(bids_root: str | Path) -> list[str]:
    """Retorna lista de IDs de participantes.

    Args:
        bids_root: Diretório raiz BIDS.

    Returns:
        Lista ordenada de IDs (e.g. ["sub-01", "sub-02", ...]).
    """
    bids_root = Path(bids_root)
    sub_dirs = sorted([d.name for d in bids_root.iterdir() if d.is_dir() and d.name.startswith("sub-")])
    return sub_dirs


def _list_subject_files(modality_dir: Path) -> dict[str, list[str]]:
    """Lista arquivos de uma modalidade para todos os participantes."""
    files: dict[str, list[str]] = {}
    for sub_dir in sorted(modality_dir.iterdir()):
        if sub_dir.is_dir() and sub_dir.name.startswith("sub-"):
            files[sub_dir.name] = sorted([
                f.name for f in sub_dir.iterdir() if f.is_file()
            ])
    return files


def create_bids_structure(
    output_root: str | Path,
    project_name: str = "neurociencia",
    participants: list[str] | None = None,
    modalities: list[str] | None = None,
) -> Path:
    """Cria estrutura de diretórios BIDS.

    Args:
        output_root: Diretório raiz de saída.
        project_name: Nome do projeto.
        participants: Lista de IDs (sem prefixo "sub-").
        modalities: Lista de modalidades (e.g. ["eeg", "anat"]).

    Returns:
        Path do diretório criado.
    """
    output_root = Path(output_root)
    if modalities is None:
        modalities = ["eeg", "anat"]
    if participants is None:
        participants = []

    # Criar diretórios
    output_root.mkdir(parents=True, exist_ok=True)
    for mod in modalities:
        (output_root / mod).mkdir(exist_ok=True)
        for sub in participants:
            (output_root / mod / f"sub-{sub}").mkdir(exist_ok=True)

    # Criar dataset_description.json
    import json
    description = {
        "Name": project_name,
        "BIDSVersion": "1.6.0",
        "DatasetType": "raw",
    }
    (output_root / "dataset_description.json").write_text(
        json.dumps(description, indent=2)
    )

    logger.info(f"Estrutura BIDS criada em {output_root}")
    return output_root
