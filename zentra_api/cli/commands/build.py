from zentra_api.cli.constants import DEPLOYMENT_FILE_MAPPING


class Build:
    """Performs production build creation for the `build` command."""

    def __init__(self, type: str) -> None:
        self.type: type

        self.deployment_files = DEPLOYMENT_FILE_MAPPING[type]

    def create(self) -> None:
        """Creates the production build of the application."""


class BuildTasks:
    """Contains the tasks for the `build` command."""

    pass
