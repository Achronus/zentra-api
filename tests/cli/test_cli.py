from unittest.mock import patch
import pytest


from typer.testing import CliRunner

from zentra_api.cli.commands.setup import Setup
from zentra_api.cli.constants.enums import BuildType
from zentra_api.cli.main import app

runner = CliRunner()


class TestInit:
    @pytest.fixture
    def project_name(self) -> str:
        return "test_project"

    @staticmethod
    def test_success(project_name: str):
        with patch.object(Setup, "build", return_value=None) as mock_build:
            result = runner.invoke(app, ["init", BuildType.FASTAPI, project_name])

            assert result.exit_code == 0
            mock_build.assert_called_once()

    @staticmethod
    def test_arg_missing():
        result = runner.invoke(app, ["init"])
        assert result.exit_code != 0


class TestNewKey:
    @staticmethod
    def test_default(key_length):
        result = runner.invoke(app, ["new-key"])

        assert result.exit_code == 0
        assert len(result.output.strip()) == key_length(256)

    @staticmethod
    @pytest.mark.parametrize("size", [256 // 8, 384 // 8, 512 // 8])
    def test_new_key_algorithms(size: int, key_length):
        target_len = key_length(size * 8)
        result = runner.invoke(app, ["new-key", str(size)])

        assert result.exit_code == 0
        assert len(result.output.strip()) == target_len
