from enum import StrEnum


class JWTAlgorithm(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
