"""
Custom response models and utility methods for API routes.
"""

from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from zentra_api.cli.constants import RESPONSE_MODEL_DIR, RESPONSE_ROOT_PATH
from zentra_api.responses.base import BaseResponse, BaseSuccessResponse
from zentra_api.responses.messages import HTTP_MSG_MAPPING, HTTPMessage
from zentra_api.responses.utils import build_response, get_code_status, merge_dicts_list
from zentra_api.utils.package import load_module

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    validate_call,
)


T = TypeVar("T", bound=BaseModel)


class MessageResponse(BaseResponse):
    """
    A message response model for API responses. Intended for client responses.

    Parameters:
        message (str): The reason the response occurred.
        headers (dict[str, str] | None, optional): The headers to send with the response.

    Returns:
        MessageResponse: An instance of the `MessageResponse` class.
    """

    message: str = Field(..., description="The reason the response occured.")
    headers: dict[str, str] | None = Field(
        default=None, description="The headers to send with the response (optional)."
    )


class ErrorResponse(MessageResponse):
    """
    An error response model. Intended for client responses.

    Parameters:
        message (str): The reason the error response occurred.
        headers (dict[str, str] | None, optional): The headers to send with the response.

    Returns:
        ErrorResponse: An instance of the `ErrorResponse` class.
    """

    status: str = Field(
        default="error",
        frozen=True,
        description="The status of the response. Cannot be changed.",
    )


class SuccessMsgResponse(MessageResponse):
    """
    A success response model. Intended for client responses. Provides a message instead of data.

    Parameters:
        message (str): The reason for the success response.
        headers (dict[str, str] | None, optional): The headers to send with the response.

    Returns:
        SuccessMsgResponse: An instance of the `SuccessMsgResponse` class.
    """

    status: str = Field(
        default="success",
        frozen=True,
        description="The status of the response. Cannot be changed.",
    )


class SuccessResponse(BaseSuccessResponse, Generic[T]):
    """
    A success response model. Intended for client responses.
    Uses generics to change the data model.

    Parameters:
        data (T): The response data model, where `T` is a subclass of `pydantic.BaseModel`.
        headers (dict[str, str] | None, optional): The headers to send with the response.

    Returns:
        SuccessResponse[T]: An instance of the `SuccessResponse` class with the specified data type `T`.

    Example:
    ```python
    class Car(BaseModel):
        make: str
        model: str
        year: int

    class CarListResponse(SuccessResponse[list[Car]]):
        '''A response for returning a list of cars.'''
        pass

    class CarResponse(SuccessResponse[Car]):
        '''A response for returning a single car.'''
        pass
    ```
    """

    data: T


@validate_call(validate_return=True)
def build_json_response_model(message: HTTPMessage) -> dict[int, dict[str, Any]]:
    """
    A utility function for building JSON response schemas.

    Parameters:
        message (HTTPMessage): The HTTP message containing status code and other information.

    Returns:
        dict[int, dict[str, Any]]: A dictionary representing the JSON response schema.

    Example:
        ```python
        build_json_response_model(HTTPMessage(status_code=400, detail="Car not found."))
        ```

        Equates to:
        ```python
        {
            400: {
                "model": MessageResponse,
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "error",
                            "code": 400,
                            "response": "400_BAD_REQUEST",
                            "message": "Car not found.",
                            "headers": None
                        }
                    }
                }
            }
        }
        ```
    """
    response = build_response(message.status_code)
    status = get_code_status(message.status_code)
    title = " ".join(response.split("_")[1:]).title()

    return {
        message.status_code: {
            "model": MessageResponse,
            "description": title,
            "content": {
                "application/json": {
                    "example": {
                        "status": status,
                        "code": message.status_code,
                        "response": response,
                        "message": message.detail,
                        "headers": message.headers,
                    },
                }
            },
        }
    }


class HTTPDetails(BaseModel):
    """
    A model for HTTP response details. Useful for customizing JSON responses.

    Parameters:
        code (int): The HTTP response code.
        msg (str | None): The reason the response occured.
        headers (dict[str, str] | None, optional): The headers to send with the response.

    Returns:
        HTTPDetails: An instance of the `HTTPDetails` class.
    """

    code: int
    msg: str | None = Field(None, validate_default=True)
    headers: dict[str, str] | None = None

    @field_validator("msg", mode="before")
    def validate_msg(cls, msg: str | None, info: ValidationInfo) -> str:
        code = info.data.get("code")
        custom_msg = HTTP_MSG_MAPPING[code]

        response = build_response(code)
        title = " ".join(response.split("_")[1:]).title()

        if msg == title or msg is None:
            return custom_msg.detail

        return msg

    @property
    def response(self) -> MessageResponse:
        """The message response model."""
        msg = HTTP_MSG_MAPPING[self.code]

        return MessageResponse(
            status=msg.status,
            code=msg.status_code,
            message=self.msg,
            headers=self.headers,
        )


@validate_call(validate_return=True, config=ConfigDict(arbitrary_types_allowed=True))
def zentra_json_response(exc: HTTPException) -> JSONResponse:
    """
    Returns a detailed HTTP response using the `ZentraAPI` package.

    Parameters:
        exc (fastapi.HTTPException): The HTTP exception to respond with.

    Returns:
        JSONResponse: A detailed JSON response.
    """
    details = HTTPDetails(code=exc.status_code, msg=exc.detail, headers=exc.headers)
    return JSONResponse(
        details.response.model_dump(),
        status_code=exc.status_code,
        headers=exc.headers,
    )


@validate_call(validate_return=True)
def get_response_models(codes: int | list[int]) -> dict[int, dict[str, Any]]:
    """
    Returns a dictionary of response model schemas given a set of HTTP codes.

    Parameters:
        codes (int | list[int]): The HTTP response codes.

    Returns:
        dict[int, dict[str, Any]]: A dictionary of response model schemas.

    Example:
        ```python
        get_response_models([400, 401])
        ```

        Equates to:
        ```python
        {
            400: {
                "model": MessageResponse,
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "error",
                            "code": 400,
                            "response": "400_BAD_REQUEST",
                            "message": "Bad request.",
                            "headers": None
                        }
                    }
                }
            },
            401: {
                "model": MessageResponse,
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "error",
                            "code": 401,
                            "response": "401_UNAUTHORIZED",
                            "message": "Authentication required.",
                            "headers": None
                        }
                    }
                }
            }
        }
        ```
    """
    if isinstance(codes, int):
        codes = [codes]

    models = []
    for code in codes:
        response = build_response(code, no_strip=True).split("_")[:2]
        code_type = get_code_status(code)
        const_name = f"{response[0]}_{code_type}_{str(code)}".upper()

        module = load_module(RESPONSE_ROOT_PATH, RESPONSE_MODEL_DIR)
        models.append(getattr(module, const_name))

    return merge_dicts_list(models)
