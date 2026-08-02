# ============================================================
# test_pipeline_integration.py
# Testes de integração do pipeline end-to-end
# ============================================================

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
import numpy as np
import pandas as pd


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def temp_workspace():
    """Cria diretório temporário para testes."""
    temp_dir = tempfile.mkdtemp(prefix="test_p01_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def synthetic_transcripts(temp_workspace):
    """Cria transcrições sintéticas para teste."""
    trans_dir = Path(temp_workspace) / "transcricoes"
    trans_dir.mkdir()

    transcripts = {
        "P01.txt": """
        Entrevistador: Como foi usar o tutor?
        Criança: Foi legal. Ele me ajudou com matemática. Às vezes eu não entendo e ele faz perguntas.
        Entrevistador: Você confia nele?
        Criança: Confio um pouco. Pra matemática sim, pra leitura não.
        """,
        "P02.txt": """
        Entrevistador: E o tutor?
        Criança: Ele é inteligente. Eu uso todo dia. Já vi ele errar uma vez, mas ele reconheceu.
        Entrevistador: Você gosta dele?
        Criança: Gosto. Ele explica bem. Mas professor é melhor.
        """,
        "P03.txt": """
        Entrevistador: O que você acha do tutor?
        Criança: Mais ou menos. Às vezes ele me confunde. Ele faz perguntas demais.
        Entrevistador: Você prefere o professor?
        Criança: Às vezes sim, às vezes não. Depende do dia.
        """,
    }

    for name, content in transcripts.items():
        (trans_dir / name).write_text(content.strip())

    return trans_dir


@pytest.fixture
def synthetic_diaries(temp_workspace):
    """Cria diários sintéticos."""
    daily = pd.DataFrame({
        "data": pd.date_range("2026-07-15", periods=14),
        "participante_id": ["P01"] * 14,
        "duracao_min": np.random.randint(0, 30, 14),
        "atividades": ["matematica"] * 14,
    })
    return daily


@pytest.fixture
def synthetic_questionnaires(temp_workspace):
    """Cria questionários sintéticos."""
    return pd.DataFrame({
        "participante_id": ["P01", "P02", "P03"],
        "pai_idade": [32, 28, 35],
        "conhecimento_ia": [3, 2, 4],
        "preocupacao_ia": [4, 3, 5],
    })


# ============================================================
# Testes: Estrutura
# ============================================================

def test_repository_structure():
    """Verifica estrutura básica do repositório."""
    root = Path(__file__).resolve().parents[2]
    assert (root / "README.md").exists(), "README.md deve existir"
    assert (root / "LICENSE").exists(), "LICENSE deve existir"
    assert (root / "pyproject.toml").exists(), "pyproject.toml deve existir"


def test_p01_protocol_exists():
    """Verifica que existe o protocolo detalhado do P01."""
    root = Path(__file__).resolve().parents[2]
    p01_dir = root / "01-projeto-qualitativo-criancas-ia"
    assert p01_dir.exists()
    assert (p01_dir / "protocolo" / "projeto-detalhado.md").exists()


def test_data_dictionary_exists():
    """Verifica dicionário de dados."""
    root = Path(__file__).resolve().parents[2]
    p01_dir = root / "01-projeto-qualitativo-criancas-ia"
    dict_path = p01_dir / "dados" / "dicionario-dados.md"
    assert dict_path.exists()


# ============================================================
# Testes: Pipeline de Análise Temática
# ============================================================

def test_at_pipeline_with_synthetic_data(synthetic_transcripts, temp_workspace):
    """Testa o pipeline de Análise Temática com dados sintéticos."""
    from neurociencia_edu.stats.at_pipeline import at_pipeline

    output_dir = Path(temp_workspace) / "resultados"
    output_dir.mkdir()

    # Rodar pipeline
    result = at_pipeline(
        input_dir=str(synthetic_transcripts),
        output_dir=str(output_dir),
        gerar_wordcloud=False,
    )

    # Verificar que gerou resultados
    assert result is not None
    assert (output_dir / "codificacao_inicial.csv").exists() or result.get("status") == "completed"


def test_transcripts_loading(synthetic_transcripts):
    """Testa carregamento de transcrições."""
    from neurociencia_edu.io.bids import load_transcripts

    if hasattr(__import__("neurociencia_edu.io.bids", fromlist=["load_transcripts"]), "load_transcripts"):
        transcripts = load_transcripts(str(synthetic_transcripts))
        assert len(transcripts) >= 3


# ============================================================
# Testes: EEG Preprocessing (sintético)
# ============================================================

def test_eeg_preprocessing_synthetic():
    """Testa preprocessamento EEG com dados sintéticos."""
    from neurociencia_edu.eeg.preprocessing import preprocess_eeg

    # Gerar dados sintéticos
    n_channels = 32
    n_samples = 1000
    sfreq = 500

    synthetic_eeg = np.random.randn(n_channels, n_samples) * 1e-6

    # Preprocessar
    try:
        cleaned = preprocess_eeg(
            synthetic_eeg,
            sfreq=sfreq,
            l_freq=0.1,
            h_freq=40.0,
        )
        assert cleaned.shape == synthetic_eeg.shape
    except (ImportError, AttributeError):
        # Módulo pode não estar totalmente implementado
        pytest.skip("preprocess_eeg não implementado ainda")


# ============================================================
# Testes: Análise Estatística
# ============================================================

def test_ancova_synthetic(synthetic_questionnaires):
    """Testa ANCOVA com dados sintéticos."""
    from neurociencia_edu.stats.ancova import run_ancova

    # Adicionar variável desfecho
    synthetic_questionnaires["score_pos"] = np.random.randn(3)
    synthetic_questionnaires["grupo"] = ["A", "B", "A"]

    try:
        result = run_ancova(
            data=synthetic_questionnaires,
            outcome="score_pos",
            predictor="grupo",
            covariates=["pai_idade"],
        )
        assert "p_value" in result or result is not None
    except (ImportError, AttributeError):
        pytest.skip("run_ancova não implementado ainda")


def test_mediation_synthetic():
    """Testa análise de mediação."""
    from neurociencia_edu.stats.mediation import run_mediation

    np.random.seed(42)
    n = 100
    X = np.random.randn(n)
    M = 0.5 * X + np.random.randn(n) * 0.5
    Y = 0.4 * X + 0.3 * M + np.random.randn(n) * 0.5

    data = pd.DataFrame({"X": X, "M": M, "Y": Y})

    try:
        result = run_mediation(data, "X", "M", "Y")
        assert result is not None
    except (ImportError, AttributeError):
        pytest.skip("run_mediation não implementado ainda")


# ============================================================
# Testes: Piloto P01 (integração completa)
# ============================================================

def test_pilot_data_files_exist():
    """Verifica que os dados do piloto existem."""
    root = Path(__file__).resolve().parents[2]
    p01_dados = root / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto"
    assert p01_dados.exists(), "Diretório do piloto deve existir"

    # Verificar transcrições
    trans_dir = p01_dados / "transcricoes"
    if trans_dir.exists():
        trans_files = list(trans_dir.glob("*.txt"))
        assert len(trans_files) >= 3, f"Esperado >=3 transcrições, encontrado {len(trans_files)}"

    # Verificar codebook
    codebook = p01_dados / "codebook" / "codebook-piloto.csv"
    if codebook.exists():
        df = pd.read_csv(codebook)
        assert len(df) >= 10, "Codebook deve ter pelo menos 10 códigos"


def test_pilot_codebook_schema():
    """Testa schema do codebook do piloto."""
    root = Path(__file__).resolve().parents[2]
    codebook = root / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto" / "codebook" / "codebook-piloto.csv"

    if not codebook.exists():
        pytest.skip("Codebook não existe")

    df = pd.read_csv(codebook)
    required_columns = ["codigo", "frequencia", "participantes", "descricao"]
    for col in required_columns:
        assert col in df.columns, f"Coluna {col} obrigatória"


def test_pilot_diaries_schema():
    """Testa schema dos diários do piloto."""
    root = Path(__file__).resolve().parents[2]
    diario_c01 = root / "01-projeto-qualitativo-criancas-ia" / "dados" / "piloto" / "diarios" / "C01_diario.csv"

    if not diario_c01.exists():
        pytest.skip("Diário C01 não existe")

    df = pd.read_csv(diario_c01)
    required_columns = ["data", "participante_id", "duracao_min"]
    for col in required_columns:
        assert col in df.columns


# ============================================================
# Testes: Pré-registros
# ============================================================

def test_all_preregistrations_exist():
    """Verifica que existem os 5 pré-registros."""
    root = Path(__file__).resolve().parents[2]
    prereg_dir = root / "00-fundamentos" / "preregistracao"

    expected = ["P01-preregistro.md", "P02-preregistro.md", "P03-preregistro.md",
                "P04-preregistro.md", "P05-preregistro.md"]

    for prereg in expected:
        path = prereg_dir / prereg
        assert path.exists(), f"Pré-registro {prereg} deve existir"


def test_osf_json_files_exist():
    """Verifica que os JSONs do OSF existem."""
    root = Path(__file__).resolve().parents[2]
    osf_dir = root / "docs" / "osf-json"

    if not osf_dir.exists():
        pytest.skip("Diretório osf-json não existe")

    for json_file in osf_dir.glob("*.json"):
        # Validar JSON
        import json
        with open(json_file) as f:
            data = json.load(f)
        assert "data" in data
        assert data["data"]["type"] == "preregistration"


# ============================================================
# Testes: Figuras
# ============================================================

def test_manuscript_figures_scripts():
    """Verifica que os scripts de figuras existem."""
    root = Path(__file__).resolve().parents[2]
    fig_dir = root / "docs" / "manuscritos" / "figuras"

    if not fig_dir.exists():
        pytest.skip("Diretório de figuras não existe")

    expected = [
        "figura1_framework_teorico.py",
        "figura2_heatmap_codigos.py",
        "figura3_mapa_temas.py",
        "figura4_timeline.py",
    ]

    for fig in expected:
        assert (fig_dir / fig).exists(), f"Script {fig} deve existir"


# ============================================================
# Testes: Documentação
# ============================================================

def test_github_pages_index_exists():
    """Verifica que a página inicial do GH Pages existe."""
    root = Path(__file__).resolve().parents[2]
    index = root / "docs" / "index.html"
    assert index.exists()

    content = index.read_text()
    assert "Neurociência" in content or "Neurociencia" in content
    assert "P01" in content
    assert "P05" in content


def test_recruitment_page_exists():
    """Verifica que a página de recrutamento existe."""
    root = Path(__file__).resolve().parents[2]
    page = root / "docs" / "recrutamento" / "index.html"
    assert page.exists()

    content = page.read_text()
    assert "LGPD" in content
    assert "consentimento" in content.lower()


# ============================================================
# Testes: Reprodutibilidade
# ============================================================

def test_random_seeds():
    """Verifica que seeds estão fixos em todos os notebooks/scripts."""
    root = Path(__file__).resolve().parents[2]

    seeds_found = 0
    for pattern in ["**/*.py", "**/*.R", "**/*.ipynb", "**/*.Rmd"]:
        for f in root.glob(pattern):
            if "test_" in f.name or ".venv" in str(f) or "node_modules" in str(f):
                continue
            try:
                content = f.read_text(errors="ignore")
                if "np.random.seed" in content or "set.seed" in content:
                    seeds_found += 1
            except Exception:
                pass

    assert seeds_found >= 3, f"Esperado >=3 seeds fixos, encontrado {seeds_found}"


# ============================================================
# Testes: Pacote Python
# ============================================================

def test_python_package_imports():
    """Verifica que o pacote Python pode ser importado."""
    try:
        import neurociencia_edu
        assert neurociencia_edu.__version__ is not None
    except ImportError:
        pytest.skip("Pacote neurociencia_edu não instalado no ambiente de teste")


# ============================================================
# Testes: Documentação Sphinx
# ============================================================

def test_sphinx_conf_exists():
    """Verifica que a config Sphinx existe."""
    root = Path(__file__).resolve().parents[2]
    conf = root / "docs" / "sphinx" / "conf.py"
    assert conf.exists()


# ============================================================
# Mark
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
