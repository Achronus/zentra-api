class Build:
    """Performs production build creation for the `build` command."""

    def __init__(self, type: str) -> None:
        self.type: type

    def create(self) -> None:
        """Creates the production build of the application."""
        pass


class BuildTasks:
    """Contains the tasks for the `build` command."""

    pass
