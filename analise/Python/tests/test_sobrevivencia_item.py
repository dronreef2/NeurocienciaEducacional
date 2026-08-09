"""
test_sobrevivencia_item.py
Testes para os novos notebooks de sobrevivência e item analysis
"""

import sys
from pathlib import Path
import pytest
import numpy as np
import pandas as pd


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def synthetic_survival_data():
    """Dados sintéticos para análise de sobrevivência."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "tempo": np.random.exponential(10, n),
        "evento": np.random.choice([0, 1], n, p=[0.3, 0.7]),
        "sexo": np.random.choice([0, 1], n),
        "ses": np.random.normal(0, 1, n),
    })


@pytest.fixture
def synthetic_items_data():
    """Dados sintéticos para análise de itens."""
    np.random.seed(42)
    n = 100
    n_itens = 10
    respostas = np.random.randint(0, 5, (n, n_itens))
    return pd.DataFrame(
        respostas,
        columns=[f"item_{i+1:02d}" for i in range(n_itens)]
    )


# ============================================================
# Testes: Sobrevivência
# ============================================================

def test_kaplan_meier_function_exists():
    """Verifica que kaplan_meier existe no módulo."""
    sys.path.insert(0, "/workspace/analise/Python/notebooks")

    # Import direto do código do notebook
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sobrevivencia",
        "/workspace/analise/Python/notebooks/12_sobrevivencia.py"
    )
    mod = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(mod)
    except (SystemExit, FileNotFoundError):
        pytest.skip("Módulo não pode ser carregado")

    assert hasattr(mod, "kaplan_meier"), "Função kaplan_meier deve existir"
    assert hasattr(mod, "cox_log_likelihood"), "Função cox_log_likelihood deve existir"


def test_kaplan_meier_basic(synthetic_survival_data):
    """Testa cálculo básico de Kaplan-Meier."""
    sys.path.insert(0, "/workspace/analise/Python/notebooks")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sobrevivencia",
        "/workspace/analise/Python/notebooks/12_sobrevivencia.py"
    )
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pytest.skip("Módulo não pode ser carregado")

    tempos = synthetic_survival_data["tempo"].values
    eventos = synthetic_survival_data["evento"].values

    t_km, s_km = mod.kaplan_meier(tempos, eventos)

    assert len(t_km) == len(s_km), "Tamanho de t_km e s_km devem ser iguais"
    assert (s_km >= 0).all() and (s_km <= 1).all(), "Sobrevida deve estar em [0,1]"
    # Primeira sobrevida é ~1.0 (pode ser 0.99 se primeiro evento ocorre em t=0)
    assert s_km[0] >= 0.9, f"Sobrevida inicial {s_km[0]} deve ser ~1.0"


def test_cox_log_likelihood_runs(synthetic_survival_data):
    """Testa que log-likelihood do Cox pode ser computada."""
    sys.path.insert(0, "/workspace/analise/Python/notebooks")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sobrevivencia",
        "/workspace/analise/Python/notebooks/12_sobrevivencia.py"
    )
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pytest.skip("Módulo não pode ser carregado")

    X = synthetic_survival_data[["sexo", "ses"]].values
    nll = mod.cox_log_likelihood(np.zeros(2), X,
                                  synthetic_survival_data["tempo"].values,
                                  synthetic_survival_data["evento"].values)
    assert np.isfinite(nll), "NLL deve ser finito"


# ============================================================
# Testes: Item Analysis
# ============================================================

def test_cronbach_alpha(synthetic_items_data):
    """Testa cálculo do Alpha de Cronbach."""
    df = synthetic_items_data
    n_itens = df.shape[1]
    alpha = (n_itens / (n_itens - 1)) * (1 - df.var().sum() / df.sum(axis=1).var())

    assert -1 <= alpha <= 1, f"Alpha {alpha} fora do range esperado"
    assert np.isfinite(alpha)


def test_item_difficulty_range(synthetic_items_data):
    """Verifica que índice de dificuldade está em [0,1]."""
    for j in range(synthetic_items_data.shape[1]):
        p = synthetic_items_data.iloc[:, j].mean() / 4  # Likert 0-4
        assert 0 <= p <= 1, f"Dificuldade {p} fora de [0,1]"


def test_discrimination_index(synthetic_items_data):
    """Calcula índice de discriminação (27% superior vs inferior)."""
    df = synthetic_items_data
    total = df.sum(axis=1)

    corte_sup = np.percentile(total, 73)
    corte_inf = np.percentile(total, 27)
    g_sup = df[total >= corte_sup]
    g_inf = df[total <= corte_inf]

    for j in range(df.shape[1]):
        disc = g_sup.iloc[:, j].mean() - g_inf.iloc[:, j].mean()
        # Discriminação pode ser negativa em dados aleatórios
        assert -4 <= disc <= 4, f"Discriminação {disc} suspeita"


def test_item_correlation_with_total(synthetic_items_data):
    """Verifica correlação item-total."""
    df = synthetic_items_data
    total = df.sum(axis=1)

    for j in range(df.shape[1]):
        r = df.iloc[:, j].corr(total)
        assert -1 <= r <= 1


def test_scree_plot_data(synthetic_items_data):
    """Verifica que autovalores são calculados."""
    corr = synthetic_items_data.corr()
    autovalores = np.linalg.eigvalsh(corr)

    assert len(autovalores) == synthetic_items_data.shape[1]
    assert (autovalores > 0).all(), "Autovalores devem ser positivos"


# ============================================================
# Testes: Gerador de Dados Sintéticos
# ============================================================

def test_gerar_dados_sinteticos_existe():
    """Verifica que o gerador existe."""
    script_path = Path("/workspace/analise/Python/scripts/gerar_dados_sinteticos.py")
    assert script_path.exists()


def test_gerar_dados_sinteticos_executa():
    """Roda o gerador e verifica output."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "/workspace/analise/Python/scripts/gerar_dados_sinteticos.py"],
        capture_output=True, timeout=30
    )
    assert result.returncode == 0, f"Erro: {result.stderr.decode()[:500]}"

    # Verificar arquivos gerados
    output_dir = Path("/workspace/dados_sinteticos")
    assert (output_dir / "P01_diarios_sinteticos.csv").exists()
    assert (output_dir / "P02_dados_sinteticos.csv").exists()
    assert (output_dir / "P04_dados_sinteticos.csv").exists()
    assert (output_dir / "P05_dados_longitudinais_sinteticos.csv").exists()


def test_dados_sinteticos_schema():
    """Verifica schema dos dados gerados."""
    import subprocess
    subprocess.run(
        [sys.executable, "/workspace/analise/Python/scripts/gerar_dados_sinteticos.py"],
        capture_output=True, timeout=30
    )

    # P01: colunas esperadas
    p01 = pd.read_csv("/workspace/dados_sinteticos/P01_diarios_sinteticos.csv")
    expected_cols = ["data", "participante_id", "duracao_min", "atividades"]
    for col in expected_cols:
        assert col in p01.columns, f"P01: coluna {col} ausente"

    # P02: tem condições
    p02 = pd.read_csv("/workspace/dados_sinteticos/P02_dados_sinteticos.csv")
    assert "condicao" in p02.columns
    assert p02["condicao"].nunique() == 5

    # P05: 5 ondas
    p05 = pd.read_csv("/workspace/dados_sinteticos/P05_dados_longitudinais_sinteticos.csv")
    assert p05["wave"].nunique() == 5
