"""
bench_pipeline.py
Benchmarks do pipeline de análise

Mede tempo de execução de cada etapa do pipeline para detectar
regressões de performance.
"""

import time
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime


def benchmark(name: str, func, *args, n_runs: int = 3, **kwargs) -> dict:
    """Roda função n vezes e retorna tempo médio."""
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "name": name,
        "mean_seconds": float(np.mean(times)),
        "std_seconds": float(np.std(times)),
        "min_seconds": float(np.min(times)),
        "max_seconds": float(np.max(times)),
        "n_runs": n_runs,
        "success": success,
        "error": error,
    }


def bench_at_pipeline():
    """Benchmark do AT pipeline."""
    from neurociencia_edu.stats.at_pipeline import at_pipeline

    # Setup
    tmp = Path("/tmp/bench_at")
    tmp.mkdir(parents=True, exist_ok=True)
    in_dir = tmp / "in"
    out_dir = tmp / "out"
    in_dir.mkdir(exist_ok=True)
    out_dir.mkdir(exist_ok=True)

    # Criar 10 transcrições
    for i in range(10):
        (in_dir / f"P{i:02d}.txt").write_text(
            f"Entrevistador: Como foi?\nCriança P{i:02d}: Foi legal. Eu aprendi coisas novas."
        )

    return at_pipeline, (str(in_dir), str(out_dir), False), {}


def bench_eeg_preprocessing():
    """Benchmark de preprocessamento EEG."""
    from neurociencia_edu.eeg.preprocessing import preprocess_eeg

    n_channels, n_samples, sfreq = 32, 5000, 500
    eeg = np.random.randn(n_channels, n_samples) * 1e-6

    return preprocess_eeg, (eeg,), {"sfreq": sfreq, "l_freq": 0.1, "h_freq": 40}


def bench_ancova():
    """Benchmark de ANCOVA."""
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        "x1": np.random.randn(n),
        "x2": np.random.randn(n),
        "y": np.random.randn(n),
        "grupo": np.random.choice(["A", "B"], n)
    })
    try:
        from neurociencia_edu.stats.ancova import run_ancova
        return run_ancova, (df, "y", "grupo", ["x1", "x2"]), {}
    except ImportError:
        return None, (), {}


def bench_mediation():
    """Benchmark de mediação."""
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        "X": np.random.randn(n),
        "M": np.random.randn(n),
        "Y": np.random.randn(n),
    })
    try:
        from neurociencia_edu.stats.mediation import run_mediation
        return run_mediation, (df, "X", "M", "Y"), {}
    except ImportError:
        return None, (), {}


def bench_lgcm():
    """Benchmark de Latent Growth Curve Model."""
    np.random.seed(42)
    n = 200
    waves = 5
    df = pd.DataFrame(
        np.random.randn(n, waves),
        columns=[f"T{i+1}" for i in range(waves)]
    )
    try:
        from neurociencia_edu.stats.sem import run_lgcm
        return run_lgcm, (df,), {}
    except ImportError:
        return None, (), {}


def main():
    print("=" * 60)
    print(f"  BENCHMARKS — {datetime.now().isoformat()}")
    print("=" * 60)

    benchmarks_to_run = [
        ("at_pipeline", bench_at_pipeline),
        ("eeg_preprocessing", bench_eeg_preprocessing),
        ("ancova", bench_ancova),
        ("mediation", bench_mediation),
        ("lgcm", bench_lgcm),
    ]

    results = []
    for name, setup_fn in benchmarks_to_run:
        print(f"\n  ⏱️  {name}...", end=" ", flush=True)
        try:
            func, args, kwargs = setup_fn()
            if func is None:
                print("SKIP (módulo não disponível)")
                continue
            result = benchmark(name, func, *args, n_runs=3, **kwargs)
            results.append(result)
            print(f"{result['mean_seconds']*1000:.1f}ms (±{result['std_seconds']*1000:.1f})")
        except Exception as e:
            print(f"ERRO: {e}")
            results.append({"name": name, "error": str(e), "success": False})

    # Salvar resultados
    output_path = Path("benchmarks/benchmark_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "python_version": __import__("sys").version,
            "results": results,
        }, f, indent=2, default=str)

    print(f"\n{'=' * 60}")
    print(f"✅ {sum(1 for r in results if r.get('success', False))}/{len(results)} benchmarks OK")
    print(f"   Resultados salvos em: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
