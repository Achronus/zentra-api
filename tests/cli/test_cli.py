from unittest.mock import patch
import pytest
from math import ceil

from typer.testing import CliRunner

from zentra_api.cli.commands.setup import Setup
from zentra_api.cli.main import app

runner = CliRunner()


def key_length(size: int) -> int:
    return ceil((size // 8) * 8 / 6)


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
        assert len(result.output.strip()) == key_length(256)

    @staticmethod
    @pytest.mark.parametrize(
        "size, target_len",
        [
            (256 // 8, key_length(256)),
            (384 // 8, key_length(384)),
            (512 // 8, key_length(512)),
        ],
    )
    def test_new_key_algorithms(size: int, target_len: int):
        result = runner.invoke(app, ["new-key", str(size)])

        assert result.exit_code == 0
        assert len(result.output.strip()) == target_len
