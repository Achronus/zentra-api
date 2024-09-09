import re
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError


ENV_FILE_NAME = r"^\.env(\.[a-zA-Z0-9-]+)*$"
SINGLE_WORD = r"^[a-zA-Z]+$"


class EnvFilename(BaseModel):
    name: str

    @field_validator("name")
    def validate_filename(cls, name: str) -> str:
        if not re.match(ENV_FILE_NAME, name):
            raise PydanticCustomError(
                "invalid_filename",
                "Invalid filename. Must start with '.env' and contain only letters (a-zA-Z), dots (.) or dashes (-)",
                dict(wrong_value=name),
            )
        return name


class SingleWord(BaseModel):
    value: str

    @field_validator("value")
    def validate_word(cls, value: str) -> str:
        if not re.match(SINGLE_WORD, value):
            raise PydanticCustomError(
                "invalid_string",
                "Invalid string. Must contain only letters (a-zA-Z)",
                dict(wrong_value=value),
            )
        return value
