"""
A collection of predefined HTTP messages created using the `HTTPMessage` model.

Messages include all types of status codes (100, 202, 404, etc.). These can be used as standardized responses in API implementations but provide generic messages relating to the status code.

Available status codes:
- 100-199: Informational
- 200-299: Success
- 300-399: Redirection
- 400-499: Client Error
- 500-599: Server Error

Usage:
```python
from zentra_api.responses.messages import HTTPMessage

# Create a custom HTTP message
custom_msg = HTTPMessage(status_code=200, detail="Operation successful")

# Create a custom HTTP message with headers
custom_msg = HTTPMessage(
    status_code=200,
    detail="Operation successful",
    headers={"X-Custom-Header": "CustomValue"},
)

# Use a predefined HTTP message
from zentra_api.responses import messages

messages.HTTP_400_BAD_REQUEST
```
"""

from pydantic import BaseModel, Field, field_validator
from fastapi import status

from .utils import get_code_status


class HTTPMessage(BaseModel):
    """
    A model for HTTP messages.

    Parameters:
        status_code (int): The HTTP response code.
        detail (str): The reason the response occured.
        headers (dict[str, str] | None, optional): The headers to send with the response.
    """

    status_code: int = Field(..., description="The HTTP response code.")
    detail: str = Field(..., description="The reason the response occured.")
    headers: dict[str, str] | None = Field(
        default=None,
        description="The headers to send with the response (optional).",
        validate_default=True,
    )

    @property
    def status(self) -> str:
        return get_code_status(self.status_code)

    @field_validator("headers")
    def validate_headers(cls, headers: dict[str, str] | None) -> dict:
        if headers is None:
            return {}

        return headers


HTTP_100_CONTINUE = HTTPMessage(
    status_code=status.HTTP_100_CONTINUE,
    detail="Continue sending the request body.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 100 status code.

```python
HTTPMessage(
    status_code=status.HTTP_100_CONTINUE,
    detail="Continue sending the request body.",
)
```
"""

HTTP_101_SWITCHING_PROTOCOLS = HTTPMessage(
    status_code=status.HTTP_101_SWITCHING_PROTOCOLS,
    detail="Switching protocols as requested.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 101 status code.

```python
HTTPMessage(
    status_code=status.HTTP_101_SWITCHING_PROTOCOLS,
    detail="Switching protocols as requested.",
)
```
"""

HTTP_102_PROCESSING = HTTPMessage(
    status_code=status.HTTP_102_PROCESSING,
    detail="Processing request.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 102 status code.

```python
HTTPMessage(
    status_code=status.HTTP_102_PROCESSING,
    detail="Processing request.",
)
```
"""

HTTP_103_EARLY_HINTS = HTTPMessage(
    status_code=status.HTTP_103_EARLY_HINTS,
    detail="Sending early hints.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 103 status code.

```python
HTTPMessage(
    status_code=status.HTTP_103_EARLY_HINTS,
    detail="Sending early hints.",
)
```
"""

HTTP_200_OK = HTTPMessage(
    status_code=status.HTTP_200_OK,
    detail="Request successful.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 200 status code.

```python
HTTPMessage(
    status_code=status.HTTP_200_OK,
    detail="Request successful.",
)
```
"""

HTTP_201_CREATED = HTTPMessage(
    status_code=status.HTTP_201_CREATED,
    detail="Request successful, new resource created.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 201 status code.

```python
HTTPMessage(
    status_code=status.HTTP_201_CREATED,
    detail="Request successful, new resource created.",
)
```
"""

HTTP_202_ACCEPTED = HTTPMessage(
    status_code=status.HTTP_202_ACCEPTED,
    detail="Request accepted.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 202 status code.

```python
HTTPMessage(
    status_code=status.HTTP_202_ACCEPTED,
    detail="Request accepted.",
)
```
"""

HTTP_203_NON_AUTHORITATIVE_INFORMATION = HTTPMessage(
    status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    detail="Request successful, info may be from third-party.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 203 status code.

```python
HTTPMessage(
    status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    detail="Request successful, info may be from third-party.",
)
```
"""

HTTP_204_NO_CONTENT = HTTPMessage(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Request successful, no content in response.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 204 status code.

```python
HTTPMessage(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Request successful, no content in response.",
)
```
"""

HTTP_205_RESET_CONTENT = HTTPMessage(
    status_code=status.HTTP_205_RESET_CONTENT,
    detail="Request successful, reset document view.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 205 status code.

```python
HTTPMessage(
    status_code=status.HTTP_205_RESET_CONTENT,
    detail="Request successful, reset document view.",
)
```
"""

HTTP_206_PARTIAL_CONTENT = HTTPMessage(
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    detail="Partial resource delivered.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 206 status code.

```python
HTTPMessage(
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    detail="Partial resource delivered.",
)
```
"""

HTTP_207_MULTI_STATUS = HTTPMessage(
    status_code=status.HTTP_207_MULTI_STATUS,
    detail="Request successful, multiple statuses in response.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 207 status code.

```python
HTTPMessage(
    status_code=status.HTTP_207_MULTI_STATUS,
    detail="Request successful, multiple statuses in response.",
)
```
"""

HTTP_208_ALREADY_REPORTED = HTTPMessage(
    status_code=status.HTTP_208_ALREADY_REPORTED,
    detail="DAV bindings already enumerated in previous response.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 208 status code.

```python
HTTPMessage(
    status_code=status.HTTP_208_ALREADY_REPORTED,
    detail="DAV bindings already enumerated in previous response.",
)
```
"""


HTTP_226_IM_USED = HTTPMessage(
    status_code=status.HTTP_226_IM_USED,
    detail="Request fulfilled, instance manipulations applied.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 226 status code.

```python
HTTPMessage(
    status_code=status.HTTP_226_IM_USED,
    detail="Request fulfilled, instance manipulations applied.",
)
```
"""


HTTP_300_MULTIPLE_CHOICES = HTTPMessage(
    status_code=status.HTTP_300_MULTIPLE_CHOICES,
    detail="Multiple choices available.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 300 status code.

```python
HTTPMessage(
    status_code=status.HTTP_300_MULTIPLE_CHOICES,
    detail="Multiple choices available.",
)
```
"""


HTTP_301_MOVED_PERMANENTLY = HTTPMessage(
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
    detail="Resource moved permanently to a new URI.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 301 status code.

```python
HTTPMessage(
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
    detail="Resource moved permanently to a new URI.",
)
```
"""

HTTP_302_FOUND = HTTPMessage(
    status_code=status.HTTP_302_FOUND,
    detail="Resource found at a different URI temporarily.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 302 status code.

```python
HTTPMessage(
    status_code=status.HTTP_302_FOUND,
    detail="Resource found at a different URI temporarily.",
)
```
"""


HTTP_303_SEE_OTHER = HTTPMessage(
    status_code=status.HTTP_303_SEE_OTHER,
    detail="Retrieve resource from a different URI.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 303 status code.

```python
HTTPMessage(
    status_code=status.HTTP_303_SEE_OTHER,
    detail="Retrieve resource from a different URI.",
)
```
"""


HTTP_304_NOT_MODIFIED = HTTPMessage(
    status_code=status.HTTP_304_NOT_MODIFIED,
    detail="Resource not modified, use cached version.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 304 status code.

```python
HTTPMessage(
    status_code=status.HTTP_304_NOT_MODIFIED,
    detail="Resource not modified, use cached version.",
)
```
"""


HTTP_305_USE_PROXY = HTTPMessage(
    status_code=status.HTTP_305_USE_PROXY,
    detail="Access resource through specified proxy.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 305 status code.

```python
HTTPMessage(
    status_code=status.HTTP_305_USE_PROXY,
    detail="Access resource through specified proxy.",
)
```
"""

HTTP_306_RESERVED = HTTPMessage(
    status_code=status.HTTP_306_RESERVED,
    detail="Reserved for future use.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 306 status code.

```python
HTTPMessage(
    status_code=status.HTTP_306_RESERVED,
    detail="Reserved for future use.",
)
```
"""

HTTP_307_TEMPORARY_REDIRECT = HTTPMessage(
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    detail="Resource temporarily under a different URI.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 307 status code.

```python
HTTPMessage(
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    detail="Resource temporarily under a different URI.",
)
```
"""

HTTP_308_PERMANENT_REDIRECT = HTTPMessage(
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    detail="Resource permanently moved to a new URI.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 308 status code.

```python
HTTPMessage(
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    detail="Resource permanently moved to a new URI.",
)
```
"""

HTTP_400_BAD_REQUEST = HTTPMessage(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 400 status code.

```python
HTTPMessage(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request.",
)
```
"""

HTTP_401_UNAUTHORIZED = HTTPMessage(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 401 status code.

```python
HTTPMessage(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required.",
)
```
"""

HTTP_402_PAYMENT_REQUIRED = HTTPMessage(
    status_code=status.HTTP_402_PAYMENT_REQUIRED,
    detail="Payment required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 402 status code.

```python
HTTPMessage(
    status_code=status.HTTP_402_PAYMENT_REQUIRED,
    detail="Payment required.",
)
```
"""

HTTP_403_FORBIDDEN = HTTPMessage(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 403 status code.

```python
HTTPMessage(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied.",
)
```
"""

HTTP_404_NOT_FOUND = HTTPMessage(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 404 status code.

```python
HTTPMessage(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found.",
)
```
"""

HTTP_405_METHOD_NOT_ALLOWED = HTTPMessage(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Method not allowed.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 405 status code.

```python
HTTPMessage(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Method not allowed.",
)
```
"""

HTTP_406_NOT_ACCEPTABLE = HTTPMessage(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Resource not available in this format.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 406 status code.

```python
HTTPMessage(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Resource not available in this format.",
)
```
"""

HTTP_407_PROXY_AUTHENTICATION_REQUIRED = HTTPMessage(
    status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    detail="Proxy authentication required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 407 status code.

```python
HTTPMessage(
    status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    detail="Proxy authentication required.",
)
```
"""

HTTP_408_REQUEST_TIMEOUT = HTTPMessage(
    status_code=status.HTTP_408_REQUEST_TIMEOUT,
    detail="Request timeout, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 408 status code.

```python
HTTPMessage(
    status_code=status.HTTP_408_REQUEST_TIMEOUT,
    detail="Request timeout, try again later.",
)
```
"""

HTTP_409_CONFLICT = HTTPMessage(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict with current resource state.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 409 status code.

```python
HTTPMessage(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict with current resource state.",
)
```
"""

HTTP_410_GONE = HTTPMessage(
    status_code=status.HTTP_410_GONE,
    detail="Resource permanently removed.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 410 status code.

```python
HTTPMessage(
    status_code=status.HTTP_410_GONE,
    detail="Resource permanently removed.",
)
```
"""

HTTP_411_LENGTH_REQUIRED = HTTPMessage(
    status_code=status.HTTP_411_LENGTH_REQUIRED,
    detail="Content-Length header required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 411 status code.

```python
HTTPMessage(
    status_code=status.HTTP_411_LENGTH_REQUIRED,
    detail="Content-Length header required.",
)
```
"""

HTTP_412_PRECONDITION_FAILED = HTTPMessage(
    status_code=status.HTTP_412_PRECONDITION_FAILED,
    detail="Precondition failed.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 412 status code.

```python
HTTPMessage(
    status_code=status.HTTP_412_PRECONDITION_FAILED,
    detail="Precondition failed.",
)
```
"""

HTTP_413_REQUEST_ENTITY_TOO_LARGE = HTTPMessage(
    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    detail="Payload too large.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 413 status code.

```python
HTTPMessage(
    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    detail="Payload too large.",
)
```
"""

HTTP_414_REQUEST_URI_TOO_LONG = HTTPMessage(
    status_code=status.HTTP_414_REQUEST_URI_TOO_LONG,
    detail="URI too long.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 414 status code.

```python
HTTPMessage(
    status_code=status.HTTP_414_REQUEST_URI_TOO_LONG,
    detail="URI too long.",
)
```
"""

HTTP_415_UNSUPPORTED_MEDIA_TYPE = HTTPMessage(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Unsupported media type.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 415 status code.

```python
HTTPMessage(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Unsupported media type.",
)
```
"""

HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = HTTPMessage(
    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    detail="Requested range not satisfiable.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 416 status code.

```python
HTTPMessage(
    status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    detail="Requested range not satisfiable.",
)
```
"""

HTTP_417_EXPECTATION_FAILED = HTTPMessage(
    status_code=status.HTTP_417_EXPECTATION_FAILED,
    detail="Expectation failed.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 417 status code.

```python
HTTPMessage(
    status_code=status.HTTP_417_EXPECTATION_FAILED,
    detail="Expectation failed.",
)
```
"""

HTTP_418_IM_A_TEAPOT = HTTPMessage(
    status_code=status.HTTP_418_IM_A_TEAPOT,
    detail="I'm a teapot, can't brew coffee.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 418 status code.

```python
HTTPMessage(
    status_code=status.HTTP_418_IM_A_TEAPOT,
    detail="I'm a teapot, can't brew coffee.",
)
```
"""

HTTP_421_MISDIRECTED_REQUEST = HTTPMessage(
    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
    detail="Request misdirected to inappropriate server.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 421 status code.

```python
HTTPMessage(
    status_code=status.HTTP_421_MISDIRECTED_REQUEST,
    detail="Request misdirected to inappropriate server.",
)
```
"""

HTTP_422_UNPROCESSABLE_ENTITY = HTTPMessage(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Unprocessable entity due to semantic errors.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 422 status code.

```python
HTTPMessage(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Unprocessable entity due to semantic errors.",
)
```
"""

HTTP_423_LOCKED = HTTPMessage(
    status_code=status.HTTP_423_LOCKED,
    detail="Resource is locked.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 423 status code.

```python
HTTPMessage(
    status_code=status.HTTP_423_LOCKED,
    detail="Resource is locked.",
)
```
"""

HTTP_424_FAILED_DEPENDENCY = HTTPMessage(
    status_code=status.HTTP_424_FAILED_DEPENDENCY,
    detail="Failed dependency in previous request.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 424 status code.

```python
HTTPMessage(
    status_code=status.HTTP_424_FAILED_DEPENDENCY,
    detail="Failed dependency in previous request.",
)
```
"""

HTTP_425_TOO_EARLY = HTTPMessage(
    status_code=status.HTTP_425_TOO_EARLY,
    detail="Request too early, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 425 status code.

```python
HTTPMessage(
    status_code=status.HTTP_425_TOO_EARLY,
    detail="Request too early, try again later.",
)
```
"""

HTTP_426_UPGRADE_REQUIRED = HTTPMessage(
    status_code=status.HTTP_426_UPGRADE_REQUIRED,
    detail="Upgrade required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 426 status code.

```python
HTTPMessage(
    status_code=status.HTTP_426_UPGRADE_REQUIRED,
    detail="Upgrade required.",
)
```
"""

HTTP_428_PRECONDITION_REQUIRED = HTTPMessage(
    status_code=status.HTTP_428_PRECONDITION_REQUIRED,
    detail="Precondition required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 428 status code.

```python
HTTPMessage(
    status_code=status.HTTP_428_PRECONDITION_REQUIRED,
    detail="Precondition required.",
)
```
"""

HTTP_429_TOO_MANY_REQUESTS = HTTPMessage(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Too many requests, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 429 status code.

```python
HTTPMessage(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Too many requests, try again later.",
)
```
"""

HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = HTTPMessage(
    status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    detail="Request headers too large.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 431 status code.

```python
HTTPMessage(
    status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    detail="Request headers too large.",
)
```
"""

HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = HTTPMessage(
    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    detail="Resource unavailable due to legal reasons.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 451 status code.

```python
HTTPMessage(
    status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    detail="Resource unavailable due to legal reasons.",
)
```
"""

HTTP_500_INTERNAL_SERVER_ERROR = HTTPMessage(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 500 status code.

```python
HTTPMessage(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error, try again later.",
)
```
"""

HTTP_501_NOT_IMPLEMENTED = HTTPMessage(
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    detail="Not implemented.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 501 status code.

```python
HTTPMessage(
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    detail="Not implemented.",
)
```
"""

HTTP_502_BAD_GATEWAY = HTTPMessage(
    status_code=status.HTTP_502_BAD_GATEWAY,
    detail="Bad gateway, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 502 status code.

```python
HTTPMessage(
    status_code=status.HTTP_502_BAD_GATEWAY,
    detail="Bad gateway, try again later.",
)
```
"""

HTTP_503_SERVICE_UNAVAILABLE = HTTPMessage(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service unavailable, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 503 status code.

```python
HTTPMessage(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Service unavailable, try again later.",
)
```
"""

HTTP_504_GATEWAY_TIMEOUT = HTTPMessage(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="Gateway timeout, try again later.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 504 status code.

```python
HTTPMessage(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="Gateway timeout, try again later.",
)
```
"""

HTTP_505_HTTP_VERSION_NOT_SUPPORTED = HTTPMessage(
    status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    detail="HTTP version not supported.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 505 status code.

```python
HTTPMessage(
    status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    detail="HTTP version not supported.",
)
```
"""

HTTP_506_VARIANT_ALSO_NEGOTIATES = HTTPMessage(
    status_code=status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    detail="Variant negotiation error.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 506 status code.

```python
HTTPMessage(
    status_code=status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    detail="Variant negotiation error.",
)
```
"""

HTTP_507_INSUFFICIENT_STORAGE = HTTPMessage(
    status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
    detail="Insufficient storage.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 507 status code.

```python
HTTPMessage(
    status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
    detail="Insufficient storage.",
)
```
"""

HTTP_508_LOOP_DETECTED = HTTPMessage(
    status_code=status.HTTP_508_LOOP_DETECTED,
    detail="Infinite loop detected.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 508 status code.

```python
HTTPMessage(
    status_code=status.HTTP_508_LOOP_DETECTED,
    detail="Infinite loop detected.",
)
```
"""

HTTP_510_NOT_EXTENDED = HTTPMessage(
    status_code=status.HTTP_510_NOT_EXTENDED,
    detail="Request requires further extensions.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 510 status code.

```python
HTTPMessage(
    status_code=status.HTTP_510_NOT_EXTENDED,
    detail="Request requires further extensions.",
)
```
"""

HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = HTTPMessage(
    status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
    detail="Network authentication required.",
)
"""
A `zentra_api.responses.HTTPMessage` model for the 511 status code.

```python
HTTPMessage(
    status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
    detail="Network authentication required.",
)
```
"""

HTTP_MSG_MAPPING = {
    100: HTTP_100_CONTINUE,
    101: HTTP_101_SWITCHING_PROTOCOLS,
    102: HTTP_102_PROCESSING,
    103: HTTP_103_EARLY_HINTS,
    200: HTTP_200_OK,
    201: HTTP_201_CREATED,
    202: HTTP_202_ACCEPTED,
    203: HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    204: HTTP_204_NO_CONTENT,
    205: HTTP_205_RESET_CONTENT,
    206: HTTP_206_PARTIAL_CONTENT,
    207: HTTP_207_MULTI_STATUS,
    208: HTTP_208_ALREADY_REPORTED,
    226: HTTP_226_IM_USED,
    300: HTTP_300_MULTIPLE_CHOICES,
    301: HTTP_301_MOVED_PERMANENTLY,
    302: HTTP_302_FOUND,
    303: HTTP_303_SEE_OTHER,
    304: HTTP_304_NOT_MODIFIED,
    305: HTTP_305_USE_PROXY,
    306: HTTP_306_RESERVED,
    307: HTTP_307_TEMPORARY_REDIRECT,
    308: HTTP_308_PERMANENT_REDIRECT,
    400: HTTP_400_BAD_REQUEST,
    401: HTTP_401_UNAUTHORIZED,
    402: HTTP_402_PAYMENT_REQUIRED,
    403: HTTP_403_FORBIDDEN,
    404: HTTP_404_NOT_FOUND,
    405: HTTP_405_METHOD_NOT_ALLOWED,
    406: HTTP_406_NOT_ACCEPTABLE,
    407: HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    408: HTTP_408_REQUEST_TIMEOUT,
    409: HTTP_409_CONFLICT,
    410: HTTP_410_GONE,
    411: HTTP_411_LENGTH_REQUIRED,
    412: HTTP_412_PRECONDITION_FAILED,
    413: HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    414: HTTP_414_REQUEST_URI_TOO_LONG,
    415: HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    416: HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    417: HTTP_417_EXPECTATION_FAILED,
    418: HTTP_418_IM_A_TEAPOT,
    421: HTTP_421_MISDIRECTED_REQUEST,
    422: HTTP_422_UNPROCESSABLE_ENTITY,
    423: HTTP_423_LOCKED,
    424: HTTP_424_FAILED_DEPENDENCY,
    425: HTTP_425_TOO_EARLY,
    426: HTTP_426_UPGRADE_REQUIRED,
    428: HTTP_428_PRECONDITION_REQUIRED,
    429: HTTP_429_TOO_MANY_REQUESTS,
    431: HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    451: HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    500: HTTP_500_INTERNAL_SERVER_ERROR,
    501: HTTP_501_NOT_IMPLEMENTED,
    502: HTTP_502_BAD_GATEWAY,
    503: HTTP_503_SERVICE_UNAVAILABLE,
    504: HTTP_504_GATEWAY_TIMEOUT,
    505: HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    506: HTTP_506_VARIANT_ALSO_NEGOTIATES,
    507: HTTP_507_INSUFFICIENT_STORAGE,
    508: HTTP_508_LOOP_DETECTED,
    510: HTTP_510_NOT_EXTENDED,
    511: HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
}
