from enum import Enum, StrEnum


class RouteOptions(StrEnum):
    """The set of routes to add."""

    CRUD = "crud"
    CREATE_READ = "cr"
    CREATE_UPDATE = "cu"
    CREATE_DELETE = "cd"
    READ_UPDATE = "ru"
    READ_DELETE = "rd"
    UPDATE_DELETE = "ud"
    CREATE_READ_UPDATE = "cru"
    CREATE_READ_DELETE = "crd"
    CREATE_UPDATE_DELETE = "cud"
    READ_UPDATE_DELETE = "rud"


class RouteFile(StrEnum):
    """The files to create for a route."""

    INIT = "__init__.py"
    SCHEMA = "schema.py"
    RESPONSES = "responses.py"

    @classmethod
    def values(cls) -> list[str]:
        """Returns a list of the enum values."""
        return [file.value for file in cls]


class RouteParameters(Enum):
    """The parameters to add to a route."""

    ID = ("id", "int")
    DB_DEPEND = ("db", "DB_DEPEND")
    AUTH_DEPEND = ("current_user", "ACTIVE_USER_DEPEND")


class RouteResponseCodes(Enum):
    """The response codes to add to a route."""

    AUTH = [401, 403]
    BAD_REQUEST = [400]


class RouteMethods(StrEnum):
    """The available route HTTP methods."""

    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"

    @classmethod
    def values(cls, ignore: list[str] = None) -> list[str]:
        """Returns a list of the enum values."""
        if ignore:
            return [method.value for method in cls if method not in ignore]

        return [method.value for method in cls]


class RouteMethodType(StrEnum):
    """Human readable variants of HTTP methods."""

    GET = "Get"
    POST = "Create"
    PUT = "Update"
    PATCH = "Update"
    DELETE = "Delete"


class DeploymentType(StrEnum):
    RAILWAY = "railway"
    DOCKERFILE = "dockerfile"
    DOCKER_COMPOSE = "docker_compose"
