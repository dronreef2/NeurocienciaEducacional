#!/usr/bin/env python3
"""
status.py - Status checker para SLURM

Snakemake chama este script para verificar o status de um job.
Retorna "running", "success", ou "failed".
"""

import subprocess
import sys


def get_status(jobid: str) -> str:
    """Retorna status de um job SLURM."""
    try:
        result = subprocess.run(
            ["sacct", "-j", jobid, "--format=State", "--noheader", "-P"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return "failed"

        states = result.stdout.strip().split("\n")
        if not states:
            return "running"

        # Pega o primeiro estado (geralmente o job principal)
        first_state = states[0].strip()

        if first_state in ("COMPLETED",):
            return "success"
        elif first_state in ("FAILED", "TIMEOUT", "CANCELLED", "NODE_FAIL"):
            return "failed"
        else:
            return "running"
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return "failed"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: status.py <jobid>", file=sys.stderr)
        sys.exit(1)

    jobid = sys.argv[1]
    status = get_status(jobid)
    print(status)
    sys.exit(0 if status != "failed" else 1)
