from unittest.mock import patch
import pytest

from typer.testing import CliRunner

from zentra_api.auth.enums import JWTAlgorithm, JWTSize
from zentra_api.cli.commands.setup import Setup
from zentra_api.cli.main import app

runner = CliRunner()


class TestInit:
    @pytest.fixture
    def project_name(self) -> str:
        return "test_project"

    @staticmethod
    def test_success(project_name: str):
        with patch.object(Setup, "build", return_value=None) as mock_build:
            result = runner.invoke(app, ["init", project_name])

            assert result.exit_code == 0
            mock_build.assert_called_once()

    @staticmethod
    def test_arg_missing():
        result = runner.invoke(app, ["init"])
        assert result.exit_code != 0


class TestNewKey:
    @staticmethod
    def test_default():
        result = runner.invoke(app, ["new-key"])

        assert result.exit_code == 0
        assert len(result.output.strip()) == JWTSize[JWTAlgorithm.HS512].value // 8

    @staticmethod
    @pytest.mark.parametrize(
        "algo, size",
        [
            (JWTAlgorithm.HS256, 256 // 8),
            (JWTAlgorithm.HS384, 384 // 8),
            (JWTAlgorithm.HS512, 512 // 8),
        ],
    )
    def test_new_key_algorithms(algo: JWTAlgorithm, size: int):
        result = runner.invoke(app, ["new-key", algo.value])

        assert result.exit_code == 0
        assert len(result.output.strip()) == size
