from enum import StrEnum


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
    CREATE = "c"
    READ = "r"
    UPDATE = "u"
    DELETE = "d"


class RouteMethods(StrEnum):
    """The available route HTTP methods."""

    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class DeploymentType(StrEnum):
    RAILWAY = "railway"
    DOCKERFILE = "dockerfile"
    DOCKER_COMPOSE = "docker_compose"
