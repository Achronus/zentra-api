import pytest
from unittest import mock
import subprocess
from pathlib import Path

import toml
import typer

from zentra_api.cli.commands.setup import Setup, SetupTasks
from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.constants import ENV_FILENAME, SetupSuccessCodes


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

    class TestFastAPIBuild:
        @pytest.fixture
        def setup(self) -> Setup:
            return Setup(
                "test_project",
            )

        @mock.patch.object(Setup, "project_exists", return_value=False)
        @mock.patch.object(
            SetupTasks,
            "get_tasks",
            return_value=[mock.Mock(), mock.Mock()],
        )
        def test_tasks_executed(
            self, mock_exists, mock_tasks: SetupTasks, setup: Setup
        ):
            with pytest.raises(typer.Exit):
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
        return SetupTasks(project_details=project_details, test_logging=True)

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
        toml_path = Path(setup_tasks.project_details.project_path, "pyproject.toml")
        toml_path.parent.mkdir(parents=True, exist_ok=True)

        setup_tasks._make_toml()

        with open(toml_path, "r") as f:
            result = toml.load(f)

        target = setup_tasks.file_builder.build(
            setup_tasks.build_details.CORE_PACKAGES,
            setup_tasks.build_details.DEV_PACKAGES,
        ).to_dict()
        assert result == target

    def test_move_assets(self, setup_tasks: SetupTasks):
        with mock.patch("shutil.copytree") as mock_copytree, mock.patch(
            "os.rename"
        ) as mock_rename:
            template_dir = Path(setup_tasks.project_details.project_path, "template")
            template_dir.mkdir(parents=True, exist_ok=True)
            (template_dir / "file.txt").write_text("test content")

            mock_copytree.return_value = None
            mock_rename.return_value = None

            setup_tasks._move_assets()

            mock_copytree.assert_called_once_with(
                setup_tasks.build_details.TEMPLATE_DIR,
                setup_tasks.project_details.project_path,
                dirs_exist_ok=True,
            )

            mock_rename.assert_called_once_with(
                Path(setup_tasks.project_details.project_path, ".env.template"),
                Path(setup_tasks.project_details.project_path, ENV_FILENAME),
            )

    def test_update_env(self, key_length, setup_tasks: SetupTasks):
        env_path = Path(setup_tasks.project_details.project_path, ENV_FILENAME)
        env_path.parent.mkdir(parents=True, exist_ok=True)

        setup_tasks._move_assets()
        setup_tasks._update_env()

        with open(env_path, "r") as f:
            content = f.readlines()

        pairs = [
            ("AUTH__SECRET_KEY", key_length(32)),
            ("DB__FIRST_SUPERUSER_PASSWORD", key_length(16)),
            ("PROJECT_NAME", setup_tasks.project_details.project_name),
            ("STACK_NAME", f"{setup_tasks.project_details.project_name}-stack"),
        ]

        checks = []
        for key, value in pairs:
            for line in content:
                if line.startswith(key):
                    current_value = line.strip().split("=", 1)
                    target = (
                        len(current_value) if isinstance(value, int) else current_value
                    )
                    checks.append(target)
                    break

        assert all(checks)

    def test_get_tasks(self, setup_tasks: SetupTasks):
        tasks = setup_tasks.get_tasks()

        assert len(tasks) == 3
        assert [
            setup_tasks._make_toml,
            setup_tasks._move_assets,
            setup_tasks._update_env,
        ]
