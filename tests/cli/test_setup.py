import pytest
from unittest import mock
import subprocess
from pathlib import Path

import toml
import typer

from zentra_api.cli.commands.setup import Setup, SetupTasks
from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.constants import (
    CORE_PIP_PACKAGES,
    DEV_PIP_PACKAGES,
    ENV_FILENAME,
    TEMPLATE_DIR,
    SetupSuccessCodes,
)


class TestSetup:
    @pytest.fixture
    def setup(self, tmp_path) -> Setup:
        return Setup("test_project", root=tmp_path)

    class TestProjectExists:
        @staticmethod
        def test_exists_with_files(setup: Setup):
            setup.details.project_path.mkdir()
            (setup.details.project_path / "test.txt").write_text("content")
            assert setup.project_exists()

        @staticmethod
        def test_exists_empty_directory(setup: Setup):
            setup.details.project_path.mkdir()
            assert not setup.project_exists()

        @staticmethod
        def test_does_not_exist(setup: Setup):
            assert not setup.project_exists()

    class TestBuild:
        @pytest.fixture
        def setup(self) -> Setup:
            return Setup("test_project")

        @mock.patch.object(Setup, "project_exists", return_value=False)
        @mock.patch.object(
            SetupTasks,
            "get_tasks",
            return_value=[mock.Mock(), mock.Mock()],
        )
        def test_tasks_executed(self, mock_exists, mock_tasks, setup: Setup):
            with pytest.raises(typer.Exit) as excinfo:
                setup.build()

            for task in mock_tasks.get_tasks():
                task.assert_called_once()

        @mock.patch.object(Setup, "project_exists", return_value=False)
        @mock.patch.object(SetupTasks, "get_tasks", return_value=[])
        def test_completes(self, mock_exists, mock_tasks, setup: Setup):
            with pytest.raises(typer.Exit) as excinfo:
                setup.build()

            assert excinfo.value.exit_code == SetupSuccessCodes.COMPLETE

        @mock.patch.object(Setup, "project_exists", return_value=True)
        def test_project_exists(self, mock_exists, setup: Setup):
            with pytest.raises(typer.Exit) as excinfo:
                setup.build()

            assert excinfo.value.exit_code == SetupSuccessCodes.ALREADY_CONFIGURED


class TestSetupTasks:
    @pytest.fixture
    def project_details(self, tmp_path) -> ProjectDetails:
        return ProjectDetails(project_name="test_project", root=tmp_path)

    @pytest.fixture
    def setup_tasks(self, project_details: ProjectDetails) -> SetupTasks:
        return SetupTasks(details=project_details, test_logging=True)

    def test_run_command(self, setup_tasks: SetupTasks):
        with mock.patch("subprocess.run") as mock_subprocess:
            mock_subprocess.return_value = subprocess.CompletedProcess(
                args=["echo", "test"], returncode=0, stdout=b"output", stderr=b"error"
            )

            setup_tasks._run_command(["echo", "test"])
            mock_subprocess.assert_called_once_with(
                ["echo", "test"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

    def test_make_toml(self, setup_tasks: SetupTasks):
        toml_path = Path(setup_tasks.details.project_path, "pyproject.toml")
        toml_path.parent.mkdir(parents=True, exist_ok=True)

        setup_tasks._make_toml()

        with open(toml_path, "r") as f:
            result = toml.load(f)

        target = setup_tasks.file_builder.build(
            CORE_PIP_PACKAGES, DEV_PIP_PACKAGES
        ).to_dict()
        assert result == target

    def test_move_assets(self, setup_tasks: SetupTasks):
        with mock.patch("shutil.copytree") as mock_shutil:
            template_dir = Path(setup_tasks.details.project_path, "template")
            template_dir.mkdir(parents=True, exist_ok=True)
            (template_dir / "file.txt").write_text("test content")

            mock_shutil.return_value = None
            setup_tasks._move_assets()

            mock_shutil.assert_called_once_with(
                TEMPLATE_DIR,
                setup_tasks.details.project_path,
                dirs_exist_ok=True,
            )

    def test_add_secret_key(self, setup_tasks: SetupTasks):
        env_path = Path(setup_tasks.details.project_path, ENV_FILENAME)
        env_path.parent.mkdir(parents=True, exist_ok=True)

        setup_tasks._move_assets()
        setup_tasks._add_secret_key()

        with open(env_path, "r") as f:
            content = f.readlines()

        important_lines = all(
            [
                content[1].strip() == 'DB__URL="sqlite:///./dev_db.db"',
                content[6].strip()
                == "AUTH__ALGORITHM=HS512  # Options: HS256, HS384, or HS512",
                content[7].strip() == "AUTH__ACCESS_TOKEN_EXPIRE_MINS=30",
                content[8].strip() == "AUTH__ROUNDS=12",
            ]
        )

        key_name = "AUTH__SECRET_KEY="
        secret_key = content[5][len(key_name) :].strip()
        checks = [
            important_lines,
            key_name in "\n".join(content),
            len(secret_key) == 512 // 8,
        ]

        assert all(checks), (secret_key, len(secret_key))

    def test_get_tasks(self, setup_tasks: SetupTasks):
        tasks = setup_tasks.get_tasks()

        assert len(tasks) == 3
        assert tasks == [
            setup_tasks._make_toml,
            setup_tasks._move_assets,
            setup_tasks._add_secret_key,
        ]
