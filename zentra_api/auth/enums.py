from enum import StrEnum


class JWTAlgorithm(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"


class DeploymentType(StrEnum):
    RAILWAY = "railway"
    DOCKERFILE = "dockerfile"
    DOCKER_COMPOSE = "docker_compose"
