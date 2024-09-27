from unittest.mock import patch
import pytest

import typer
from typer.testing import CliRunner

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

    @staticmethod
    def test_typer_error(project_name: str):
        with patch.object(Setup, "build", side_effect=typer.Exit(code=-1)):
            result = runner.invoke(app, ["init", project_name])

            assert result.exit_code == 0

    @staticmethod
    def test_invalid_project_name():
        result = runner.invoke(app, ["init", "."])
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


class TestAddRouteset:
    @staticmethod
    def test_default():
        result = runner.invoke(app, ["add-routeset", "projects"])
        assert result.exit_code == 0

    @staticmethod
    def test_optional():
        result = runner.invoke(app, ["add-routeset", "projects", "rud"])
        assert result.exit_code == 0

    @staticmethod
    def test_invalid_name():
        result = runner.invoke(app, ["add-routeset", "colours123"])
        assert result.exit_code != 0

    @staticmethod
    def test_invalid_name_special_characters():
        result = runner.invoke(app, ["add-routeset", "project@123"])
        assert result.exit_code != 0

    @staticmethod
    def test_missing_name():
        result = runner.invoke(app, ["add-routeset"])
        assert result.exit_code != 0
        assert "Missing argument 'NAME'" in result.output

    @staticmethod
    def test_invalid_option():
        result = runner.invoke(app, ["add-routeset", "projects", "xyz"])
        assert result.exit_code != 0

    @staticmethod
    def test_empty_option():
        result = runner.invoke(app, ["add-routeset", "projects", ""])
        assert result.exit_code != 0

    @staticmethod
    def test_uppercase_name():
        result = runner.invoke(app, ["add-routeset", "PROJECTS"])
        assert result.exit_code == 0
