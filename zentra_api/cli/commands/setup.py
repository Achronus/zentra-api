import os
from pathlib import Path
import secrets
import shutil
import subprocess
from typing import Callable
import typer

from zentra_api.cli.builder.poetry import PoetryFileBuilder
from zentra_api.cli.conf import ProjectDetails
from zentra_api.cli.conf.logger import set_loggers
from zentra_api.cli.constants import (
    CORE_PIP_PACKAGES,
    DEV_PIP_PACKAGES,
    ENV_FILENAME,
    TEMPLATE_DIR,
    SetupSuccessCodes,
    console,
)
from zentra_api.cli.constants.display import (
    already_configured_panel,
    setup_complete_panel,
)
from zentra_api.cli.constants.message import creation_msg

from rich.progress import track


class Setup:
    """Performs project creation for the `init` command."""

    def __init__(self, project_name: str, root: Path = Path(os.getcwd())) -> None:
        self.project_name = project_name

        self.details = ProjectDetails(project_name=project_name, root=root)
        self.setup_tasks = SetupTasks(self.details)

    def project_exists(self) -> bool:
        """A helper method to check if a project with the `project_name` exists."""
        if self.details.project_path.exists():
            dirs = list(self.details.project_path.iterdir())
            if len(dirs) > 0:
                return True

        return False

    def build(self) -> None:
        """Builds the project."""
        if self.project_exists():
            console.print(already_configured_panel(self.project_name))
            raise typer.Exit(code=SetupSuccessCodes.ALREADY_CONFIGURED)

        tasks = self.setup_tasks.get_tasks()

        for task in track(tasks, description="Building..."):
            task()

        console.print(setup_complete_panel(self.project_name))
        raise typer.Exit(code=SetupSuccessCodes.COMPLETE)


class SetupTasks:
    """Contains the tasks for the `init` command."""

    def __init__(self, details: ProjectDetails, test_logging: bool = False) -> None:
        self.details = details

        self.logger = set_loggers(test_logging)

        self.file_builder = PoetryFileBuilder(self.details.author)

    def _run_command(self, command: list[str]) -> None:
        """A helper method for running Python commands. Stores output to separate loggers."""
        response = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.logger.stdout.debug(response.stdout)
        self.logger.stderr.error(response.stderr)

    def _make_toml(self) -> None:
        """Creates the `pyproject.toml` file."""
        toml_path = Path(self.details.project_path, "pyproject.toml")
        open(toml_path, "x").close()

        self.file_builder.update(toml_path, CORE_PIP_PACKAGES, DEV_PIP_PACKAGES)

    def _move_assets(self) -> None:
        """Moves the template assets into the project directory."""
        shutil.copytree(TEMPLATE_DIR, self.details.project_path, dirs_exist_ok=True)

        os.rename(
            Path(self.details.project_path, ".env.template"),
            Path(self.details.project_path, ENV_FILENAME),
        )

    def _update_env(self) -> None:
        """Adds missing environment variables dynamically."""
        pairs = {
            "AUTH__SECRET_KEY": secrets.token_urlsafe(32),
            "DB__FIRST_SUPERUSER_PASSWORD": secrets.token_urlsafe(16),
            "PROJECT_NAME": self.details.project_name,
            "STACK_NAME": f"{self.details.project_name}-stack",
        }

        env_path = Path(self.details.project_path, ENV_FILENAME)
        with open(env_path, "r") as f:
            content = f.readlines()

        updated_file = []
        for line in content:
            update = line
            if "=" in line:
                key, _ = line.strip().split("=", 1)
                update = f"{key}={pairs[key]}\n" if key in pairs else line

            updated_file.append(update)

        with open(env_path, "w") as f:
            f.writelines(updated_file)

    def get_tasks(self) -> list[Callable]:
        """Gets the tasks to run as a list of methods."""
        os.makedirs(self.details.project_path, exist_ok=True)
        os.chdir(self.details.project_path)

        console.print(
            creation_msg(
                self.details.project_name,
                self.details.project_path,
            )
        )

        return [
            self._make_toml,
            self._move_assets,
            self._update_env,
        ]
