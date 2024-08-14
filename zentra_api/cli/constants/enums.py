from enum import StrEnum


class AddItem(StrEnum):
    """The type of item to add."""

    ROUTE = "route"
    TEST = "test"


class DefaultFolderOptions(StrEnum):
    """The default folder options for each item in the `add` command."""

    ROUTE = "api"
    TEST = "test"


class BuildType(StrEnum):
    """The type of project to build."""

    FASTAPI = "fastapi"
    DJANGO = "django"
