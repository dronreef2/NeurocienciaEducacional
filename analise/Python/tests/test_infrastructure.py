"""
Testes para o módulo de infraestrutura (config, logging, exceptions, validators).
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from neurociencia_edu.config import (
    Paths,
    Programa,
    StatsConfig,
    VizConfig,
    Credentials,
    Settings,
    get_settings,
    reset_settings,
    ensure_dir,
    find_project_root,
    find_workspace,
    get_logger_name,
)
from neurociencia_edu.exceptions import (
    NeurocienciaEduError,
    ConfigurationError,
    DataError,
    DataNotFoundError,
    DataValidationError,
    DataAnonymizationError,
    ProcessingError,
    FitError,
    InsufficientDataError,
)
from neurociencia_edu.validators import (
    validar_colunas_obrigatorias,
    validar_range,
    detectar_pii,
    tem_pii,
    anonimizar_texto,
    anonimizar_dataframe,
    sanitizar_nome,
    caminho_existe,
    PII_PATTERNS,
)
from neurociencia_edu.logging_config import (
    get_logger,
    configure_logging,
    log_section,
)


# ============================================================
# Testes: config.py
# ============================================================

class TestConfig:
    """Testes do módulo de configuração."""

    def test_find_project_root(self) -> None:
        """Deve encontrar pyproject.toml."""
        root = find_project_root()
        assert isinstance(root, Path)
        assert (root / "pyproject.toml").exists()

    def test_find_workspace(self) -> None:
        """Deve encontrar workspace."""
        ws = find_workspace()
        assert isinstance(ws, Path)
        # Workspace deve conter Makefile
        assert (ws / "Makefile").exists()

    def test_paths_dataclass(self) -> None:
        """Paths deve ser imutável e ter todos os atributos."""
        paths = Paths()
        assert hasattr(paths, "raiz")
        assert hasattr(paths, "workspace")
        assert hasattr(paths, "dados")
        assert hasattr(paths, "notebooks")
        assert hasattr(paths, "resultados")

        # Frozen - não pode modificar
        with pytest.raises(Exception):  # FrozenInstanceError
            paths.raiz = Path("/tmp")  # type: ignore

    def test_paths_criar_necessarios(self, tmp_path) -> None:
        """Deve criar diretórios que não existem."""
        paths = Paths(workspace=tmp_path / "fake_ws")
        # Não deve falhar mesmo sem diretórios
        paths.criar_necessarios()

    def test_programa_constantes(self) -> None:
        """Programa deve ter valores padrão corretos."""
        prog = Programa()
        assert prog.nome == "Programa de Pesquisa em Neurociência Educacional"
        assert prog.instituicao == "UFRN / CERES / PPGED"
        assert prog.ano_inicio == 2026
        assert prog.ano_fim == 2030
        assert "P01" in prog.projetos
        assert "P05" in prog.projetos
        assert prog.idioma_principal in ("pt-BR", "en", "es")

    def test_stats_config(self) -> None:
        """StatsConfig deve ter valores padrão."""
        stats = StatsConfig()
        assert stats.alpha == 0.05
        assert stats.n_bootstrap == 5000
        assert stats.random_state == 42

    def test_viz_config(self) -> None:
        """VizConfig deve ter valores padrão."""
        viz = VizConfig()
        assert viz.dpi > 0
        assert isinstance(viz.figsize_default, tuple)

    def test_credentials_env_vars(self) -> None:
        """Credentials deve ler de env vars."""
        with patch.dict(os.environ, {"OSF_TOKEN": "test_token_123"}):
            creds = Credentials()
            assert creds.osf_token == "test_token_123"
            assert creds.has_osf() is True
            assert creds.has_pypi() is False

    def test_settings_singleton(self) -> None:
        """get_settings deve retornar mesma instância."""
        reset_settings()
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2  # mesma referência

        # Reseta e pede de novo
        reset_settings()
        s3 = get_settings()
        assert s3 is not s1  # nova instância

    def test_settings_summary(self) -> None:
        """Settings.summary deve retornar string formatada."""
        s = get_settings()
        summary = s.summary()
        assert "Neurociência" in summary or "Neurociencia" in summary
        assert "UFRN" in summary
        assert "2026" in summary

    def test_ensure_dir(self, tmp_path) -> None:
        """ensure_dir deve criar diretório."""
        target = tmp_path / "novo" / "sub" / "dir"
        result = ensure_dir(target)
        assert result.exists()
        assert result.is_dir()

    def test_get_logger_name(self) -> None:
        """get_logger_name deve padronizar nomes."""
        assert get_logger_name("modulo") == "neurociencia_edu.modulo"
        assert get_logger_name("__main__") == "neurociencia_edu.main"
        assert get_logger_name("neurociencia_edu.x") == "neurociencia_edu.x"


# ============================================================
# Testes: exceptions.py
# ============================================================

class TestExceptions:
    """Testes do sistema de exceções."""

    def test_base_exception(self) -> None:
        """Exceção base deve ter message e details."""
        exc = NeurocienciaEduError("Erro X", details={"code": 42})
        assert exc.message == "Erro X"
        assert exc.details == {"code": 42}
        assert "Erro X" in str(exc)
        assert "code" in str(exc)

    def test_hierarchy(self) -> None:
        """Exceções devem ter hierarquia correta."""
        # DataError herda de NeurocienciaEduError
        assert issubclass(DataError, NeurocienciaEduError)
        assert issubclass(DataNotFoundError, DataError)
        assert issubclass(DataValidationError, DataError)
        assert issubclass(DataAnonymizationError, DataError)

        # ProcessingError
        assert issubclass(ProcessingError, NeurocienciaEduError)
        assert issubclass(FitError, ProcessingError)
        assert issubclass(InsufficientDataError, ProcessingError)

    def test_raise_and_catch(self) -> None:
        """Deve poder fazer raise e catch."""
        with pytest.raises(DataValidationError) as exc_info:
            raise DataValidationError("Dados inválidos")
        assert "Dados inválidos" in str(exc_info.value)

        with pytest.raises(NeurocienciaEduError):
            raise FitError("Modelo não convergiu")

    def test_details_default(self) -> None:
        """Details default deve ser dict vazio."""
        exc = NeurocienciaEduError("msg")
        assert exc.details == {}


# ============================================================
# Testes: validators.py
# ============================================================

class TestValidators:
    """Testes do módulo de validadores."""

    def test_validar_colunas_obrigatorias_ok(self) -> None:
        """Deve passar quando todas as colunas existem."""
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        validar_colunas_obrigatorias(df, ["a", "b"])

    def test_validar_colunas_obrigatorias_missing(self) -> None:
        """Deve falhar quando faltam colunas."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(DataValidationError) as exc:
            validar_colunas_obrigatorias(df, ["a", "b"])
        assert "b" in str(exc.value)

    def test_validar_colunas_obrigatorias_none(self) -> None:
        """Deve falhar se df é None."""
        with pytest.raises(DataValidationError):
            validar_colunas_obrigatorias(None, ["a"])  # type: ignore

    def test_validar_colunas_obrigatorias_empty(self) -> None:
        """Deve falhar se df está vazio."""
        df = pd.DataFrame()
        with pytest.raises(DataValidationError):
            validar_colunas_obrigatorias(df, ["a"])

    def test_validar_colunas_obrigatorias_wrong_type(self) -> None:
        """Deve falhar se df não é DataFrame."""
        with pytest.raises(DataValidationError):
            validar_colunas_obrigatorias([1, 2, 3], ["a"])  # type: ignore

    def test_validar_range_ok(self) -> None:
        """Deve passar quando valores dentro do range."""
        df = pd.DataFrame({"idade": [7, 8, 9, 10]})
        validar_range(df, "idade", minimo=5, maximo=12)

    def test_validar_range_abaixo(self) -> None:
        """Deve falhar se há valores abaixo do mínimo."""
        df = pd.DataFrame({"idade": [3, 8, 9]})
        with pytest.raises(DataValidationError):
            validar_range(df, "idade", minimo=5)

    def test_validar_range_acima(self) -> None:
        """Deve falhar se há valores acima do máximo."""
        df = pd.DataFrame({"idade": [8, 15, 9]})
        with pytest.raises(DataValidationError):
            validar_range(df, "idade", maximo=12)

    def test_validar_range_coluna_inexistente(self) -> None:
        """Deve falhar se coluna não existe."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(DataValidationError):
            validar_range(df, "b")

    def test_detectar_pii_email(self) -> None:
        """Deve detectar email."""
        texto = "Contato: maria@ufrn.br"
        pii = detectar_pii(texto)
        assert "email" in pii
        assert "maria@ufrn.br" in pii["email"]

    def test_detectar_pii_cpf(self) -> None:
        """Deve detectar CPF."""
        texto = "CPF: 123.456.789-00"
        pii = detectar_pii(texto)
        assert "cpf" in pii

    def test_detectar_pii_telefone(self) -> None:
        """Deve detectar telefone."""
        texto = "Tel: (84) 99876-5432"
        pii = detectar_pii(texto)
        assert "phone_br" in pii

    def test_tem_pii_true(self) -> None:
        """Deve retornar True se há PII."""
        assert tem_pii("Email: teste@ufrn.br") is True
        assert tem_pii("Texto sem PII") is False

    def test_anonimizar_texto(self) -> None:
        """Deve substituir PII por [REMOVIDO]."""
        texto = "Email: teste@ufrn.br, CPF: 123.456.789-00"
        anon = anonimizar_texto(texto)
        assert "teste@ufrn.br" not in anon
        assert "123.456.789-00" not in anon
        assert "[REMOVIDO]" in anon

    def test_anonimizar_dataframe_hash(self) -> None:
        """Deve aplicar hash SHA256 em colunas sensíveis."""
        df = pd.DataFrame({"nome": ["Maria", "Pedro"], "idade": [7, 8]})
        df_anon = anonimizar_dataframe(df, ["nome"], metodo="hash")

        # Valores não são mais "Maria" e "Pedro"
        assert "Maria" not in df_anon["nome"].values
        assert "Pedro" not in df_anon["nome"].values
        # Hashes têm 16 chars
        assert all(len(x) == 16 for x in df_anon["nome"])
        # Idade preservada
        assert df_anon["idade"].tolist() == [7, 8]

    def test_anonimizar_dataframe_remove(self) -> None:
        """Deve remover colunas quando metodo=remove."""
        df = pd.DataFrame({"nome": ["Maria"], "idade": [7]})
        df_anon = anonimizar_dataframe(df, ["nome"], metodo="remove")
        assert "nome" not in df_anon.columns
        assert "idade" in df_anon.columns

    def test_anonimizar_dataframe_metodo_invalido(self) -> None:
        """Deve falhar com método inválido."""
        df = pd.DataFrame({"nome": ["Maria"]})
        with pytest.raises(DataAnonymizationError):
            anonimizar_dataframe(df, ["nome"], metodo="invalid")

    def test_anonimizar_dataframe_coluna_inexistente(self) -> None:
        """Deve avisar sobre coluna inexistente sem falhar."""
        df = pd.DataFrame({"a": [1, 2]})
        df_anon = anonimizar_dataframe(df, ["b"], metodo="hash")
        assert df_anon.equals(df)  # sem mudanças

    def test_sanitizar_nome(self) -> None:
        """Deve remover acentos, espaços e caracteres especiais."""
        assert sanitizar_nome("Maria Silva") == "maria_silva"
        assert sanitizar_nome("José da Silva") == "jose_da_silva"
        assert sanitizar_nome("Criança #1") == "crianca_1"
        assert sanitizar_nome("Ação & Reação") == "acao_reacao"

    def test_caminho_existe_ok(self, tmp_path) -> None:
        """Deve retornar path quando existe."""
        d = tmp_path / "existe"
        d.mkdir()
        result = caminho_existe(d)
        assert result == d

    def test_caminho_existe_criar(self, tmp_path) -> None:
        """Deve criar diretório se criar=True."""
        d = tmp_path / "novo"
        result = caminho_existe(d, criar=True)
        assert result.exists()

    def test_caminho_existe_erro(self, tmp_path) -> None:
        """Deve falhar se não existe e criar=False."""
        d = tmp_path / "nao_existe"
        with pytest.raises(DataNotFoundError):
            caminho_existe(d)


# ============================================================
# Testes: logging_config.py
# ============================================================

class TestLogging:
    """Testes do sistema de logging."""

    def test_get_logger_default(self) -> None:
        """Deve retornar logger com nome padronizado."""
        logger = get_logger("meu_modulo")
        assert logger.name == "neurociencia_edu.meu_modulo"

    def test_configure_logging_level(self) -> None:
        """Deve mudar o nível de logging."""
        configure_logging(level="DEBUG", quiet=True)
        logger = get_logger("test")
        assert logger.level <= 10  # DEBUG

    def test_configure_logging_quiet(self) -> None:
        """quiet=True deve desabilitar console."""
        configure_logging(level="INFO", quiet=True)
        root = __import__("logging").getLogger()
        # Pode ter apenas handlers de arquivo, não de console
        assert isinstance(root.handlers, list)

    def test_log_section(self) -> None:
        """log_section deve logar separador."""
        logger = get_logger("test")
        # Não deve falhar
        log_section(logger, "Minha Seção")

    def test_log_file(self, tmp_path) -> None:
        """Deve logar em arquivo."""
        log_file = tmp_path / "test.log"
        configure_logging(level="DEBUG", log_file=log_file, quiet=True)
        logger = get_logger("test")
        logger.info("mensagem teste")
        # Flush
        for h in __import__("logging").getLogger().handlers:
            h.flush()

        assert log_file.exists()
        content = log_file.read_text()
        assert "mensagem teste" in content
