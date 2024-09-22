"""
Prebuilt JSON response models for API routes. Used in the `zentra_api.responses.get_response_models()` method for dynamic generation.

Available status codes:
- 100-199: Informational
- 300-399: Redirection
- 400-499: Client Error
- 500-599: Server Error

Usage:
```python
from zentra_api.responses import models

models.HTTP_ERROR_404
```
"""

from . import build_json_response_model
from .messages import HTTP_MSG_MAPPING

HTTP_INFO_100 = build_json_response_model(HTTP_MSG_MAPPING[100])
"""
A dictionary response model for the HTTP 100 status code.

```python
{
    "100": {
        "model": MessageResponse,
        "description": "Continue",
        "content": {
            "application/json": {
                "example": {
                    "status": "info",
                    "code": 100,
                    "response": "100_CONTINUE",
                    "message": "Continue sending the request body.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_INFO_101 = build_json_response_model(HTTP_MSG_MAPPING[101])
"""
A dictionary response model for the HTTP 101 status code.

```python
{
    "101": {
        "model": MessageResponse,
        "description": "Switching Protocols",
        "content": {
            "application/json": {
                "example": {
                    "status": "info",
                    "code": 101,
                    "response": "101_SWITCHING_PROTOCOLS",
                    "message": "Switching protocols as requested.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_INFO_102 = build_json_response_model(HTTP_MSG_MAPPING[102])
"""
A dictionary response model for the HTTP 102 status code.

```python
{
    "102": {
        "model": MessageResponse,
        "description": "Processing",
        "content": {
            "application/json": {
                "example": {
                    "status": "info",
                    "code": 102,
                    "response": "102_PROCESSING",
                    "message": "Processing as requested.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_INFO_103 = build_json_response_model(HTTP_MSG_MAPPING[103])
"""
A dictionary response model for the HTTP 103 status code.

```python
{
    "103": {
        "model": MessageResponse,
        "description": "Early Hints",
        "content": {
            "application/json": {
                "example": {
                    "status": "info",
                    "code": 103,
                    "response": "103_EARLY_HINTS",
                    "message": "Early hints provided.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_300 = build_json_response_model(HTTP_MSG_MAPPING[300])
"""
A dictionary response model for the HTTP 300 status code.

```python
{
    "300": {
        "model": MessageResponse,
        "description": "Multiple Choices",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 300,
                    "response": "300_MULTIPLE_CHOICES",
                    "message": "Multiple choices available.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_301 = build_json_response_model(HTTP_MSG_MAPPING[301])
"""
A dictionary response model for the HTTP 301 status code.

```python
{
    "301": {
        "model": MessageResponse,
        "description": "Moved Permanently",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 301,
                    "response": "301_MOVED_PERMANENTLY",
                    "message": "Resource moved permanently.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_302 = build_json_response_model(HTTP_MSG_MAPPING[302])
"""
A dictionary response model for the HTTP 302 status code.

```python
{
    "302": {
        "model": MessageResponse,
        "description": "Found",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 302,
                    "response": "302_FOUND",
                    "message": "Resource found at different URI.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_303 = build_json_response_model(HTTP_MSG_MAPPING[303])
"""
A dictionary response model for the HTTP 303 status code.

```python
{
    "303": {
        "model": MessageResponse,
        "description": "See Other",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 303,
                    "response": "303_SEE_OTHER",
                    "message": "Resource can be found at another URI.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_304 = build_json_response_model(HTTP_MSG_MAPPING[304])
"""
A dictionary response model for the HTTP 304 status code.

```python
{
    "304": {
        "model": MessageResponse,
        "description": "Not Modified",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 304,
                    "response": "304_NOT_MODIFIED",
                    "message": "Resource has not been modified.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_305 = build_json_response_model(HTTP_MSG_MAPPING[305])
"""
A dictionary response model for the HTTP 305 status code.

```python
{
    "305": {
        "model": MessageResponse,
        "description": "Use Proxy",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 305,
                    "response": "305_USE_PROXY",
                    "message": "Resource must be accessed through a proxy.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_306 = build_json_response_model(HTTP_MSG_MAPPING[306])
"""
A dictionary response model for the HTTP 306 status code.

```python
{
    "306": {
        "model": MessageResponse,
        "description": "Switch Proxy",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 306,
                    "response": "306_SWITCH_PROXY",
                    "message": "Subsequent requests should use the specified proxy.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_307 = build_json_response_model(HTTP_MSG_MAPPING[307])
"""
A dictionary response model for the HTTP 307 status code.

```python
{
    "307": {
        "model": MessageResponse,
        "description": "Temporary Redirect",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 307,
                    "response": "307_TEMPORARY_REDIRECT",
                    "message": "Resource temporarily moved to another URI.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_REDIRECT_308 = build_json_response_model(HTTP_MSG_MAPPING[308])
"""
A dictionary response model for the HTTP 308 status code.

```python
{
    "308": {
        "model": MessageResponse,
        "description": "Permanent Redirect",
        "content": {
            "application/json": {
                "example": {
                    "status": "redirect",
                    "code": 308,
                    "response": "308_PERMANENT_REDIRECT",
                    "message": "Resource permanently moved to another URI.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_400 = build_json_response_model(HTTP_MSG_MAPPING[400])
"""
A dictionary response model for the HTTP 400 status code.

```python
{
    "400": {
        "model": MessageResponse,
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 400,
                    "response": "400_BAD_REQUEST",
                    "message": "Bad request.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_401 = build_json_response_model(HTTP_MSG_MAPPING[401])
"""
A dictionary response model for the HTTP 401 status code.

```python
{
    "401": {
        "model": MessageResponse,
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 401,
                    "response": "401_UNAUTHORIZED",
                    "message": "Unauthorized.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_402 = build_json_response_model(HTTP_MSG_MAPPING[402])
"""
A dictionary response model for the HTTP 402 status code.

```python
{
    "402": {
        "model": MessageResponse,
        "description": "Payment Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 402,
                    "response": "402_PAYMENT_REQUIRED",
                    "message": "Payment required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_403 = build_json_response_model(HTTP_MSG_MAPPING[403])
"""
A dictionary response model for the HTTP 403 status code.

```python
{
    "403": {
        "model": MessageResponse,
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 403,
                    "response": "403_FORBIDDEN",
                    "message": "Forbidden.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_404 = build_json_response_model(HTTP_MSG_MAPPING[404])
"""
A dictionary response model for the HTTP 404 status code.

```python
{
    "404": {
        "model": MessageResponse,
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 404,
                    "response": "404_NOT_FOUND",
                    "message": "Resource not found.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_405 = build_json_response_model(HTTP_MSG_MAPPING[405])
"""
A dictionary response model for the HTTP 405 status code.

```python
{
    "405": {
        "model": MessageResponse,
        "description": "Method Not Allowed",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 405,
                    "response": "405_METHOD_NOT_ALLOWED",
                    "message": "Method not allowed.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_406 = build_json_response_model(HTTP_MSG_MAPPING[406])
"""
A dictionary response model for the HTTP 406 status code.

```python
{
    "406": {
        "model": MessageResponse,
        "description": "Not Acceptable",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 406,
                    "response": "406_NOT_ACCEPTABLE",
                    "message": "Not acceptable.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_407 = build_json_response_model(HTTP_MSG_MAPPING[407])
"""
A dictionary response model for the HTTP 407 status code.

```python
{
    "407": {
        "model": MessageResponse,
        "description": "Proxy Authentication Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 407,
                    "response": "407_PROXY_AUTHENTICATION_REQUIRED",
                    "message": "Proxy authentication required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_408 = build_json_response_model(HTTP_MSG_MAPPING[408])
"""
A dictionary response model for the HTTP 408 status code.

```python
{
    "408": {
        "model": MessageResponse,
        "description": "Request Timeout",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 408,
                    "response": "408_REQUEST_TIMEOUT",
                    "message": "Request timeout.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_409 = build_json_response_model(HTTP_MSG_MAPPING[409])
"""
A dictionary response model for the HTTP 409 status code.

```python
{
    "409": {
        "model": MessageResponse,
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 409,
                    "response": "409_CONFLICT",
                    "message": "Conflict.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_410 = build_json_response_model(HTTP_MSG_MAPPING[410])
"""
A dictionary response model for the HTTP 410 status code.

```python
{
    "410": {
        "model": MessageResponse,
        "description": "Gone",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 410,
                    "response": "410_GONE",
                    "message": "Resource has been deleted.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_411 = build_json_response_model(HTTP_MSG_MAPPING[411])
"""
A dictionary response model for the HTTP 411 status code.

```python
{
    "411": {
        "model": MessageResponse,
        "description": "Length Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 411,
                    "response": "411_LENGTH_REQUIRED",
                    "message": "Length required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_412 = build_json_response_model(HTTP_MSG_MAPPING[412])
"""
A dictionary response model for the HTTP 412 status code.

```python
{
    "412": {
        "model": MessageResponse,
        "description": "Precondition Failed",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 412,
                    "response": "412_PRECONDITION_FAILED",
                    "message": "Precondition failed.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_413 = build_json_response_model(HTTP_MSG_MAPPING[413])
"""
A dictionary response model for the HTTP 413 status code.

```python
{
    "413": {
        "model": MessageResponse,
        "description": "Payload Too Large",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 413,
                    "response": "413_PAYLOAD_TOO_LARGE",
                    "message": "Payload too large.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_414 = build_json_response_model(HTTP_MSG_MAPPING[414])
"""
A dictionary response model for the HTTP 414 status code.

```python
{
    "414": {
        "model": MessageResponse,
        "description": "URI Too Long",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 414,
                    "response": "414_URI_TOO_LONG",
                    "message": "URI too long.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_415 = build_json_response_model(HTTP_MSG_MAPPING[415])
"""
A dictionary response model for the HTTP 415 status code.

```python
{
    "415": {
        "model": MessageResponse,
        "description": "Unsupported Media Type",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 415,
                    "response": "415_UNSUPPORTED_MEDIA_TYPE",
                    "message": "Unsupported media type.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_416 = build_json_response_model(HTTP_MSG_MAPPING[416])
"""
A dictionary response model for the HTTP 416 status code.

```python
{
    "416": {
        "model": MessageResponse,
        "description": "Range Not Satisfiable",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 416,
                    "response": "416_RANGE_NOT_SATISFIABLE",
                    "message": "Range not satisfiable.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_417 = build_json_response_model(HTTP_MSG_MAPPING[417])
"""
A dictionary response model for the HTTP 417 status code.

```python
{
    "417": {
        "model": MessageResponse,
        "description": "Expectation Failed",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 417,
                    "response": "417_EXPECTATION_FAILED",
                    "message": "Expectation failed.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_418 = build_json_response_model(HTTP_MSG_MAPPING[418])
"""
A dictionary response model for the HTTP 418 status code.

```python
{
    "418": {
        "model": MessageResponse,
        "description": "I'm a teapot",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 418,
                    "response": "418_IM_A_TEAPOT",
                    "message": "I'm a teapot.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_421 = build_json_response_model(HTTP_MSG_MAPPING[421])
"""
A dictionary response model for the HTTP 421 status code.

```python
{
    "421": {
        "model": MessageResponse,
        "description": "Misdirected Request",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 421,
                    "response": "421_MISDIRECTED_REQUEST",
                    "message": "Misdirected request.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_422 = build_json_response_model(HTTP_MSG_MAPPING[422])
"""
A dictionary response model for the HTTP 422 status code.

```python
{
    "422": {
        "model": MessageResponse,
        "description": "Unprocessable Content",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 422,
                    "response": "422_UNPROCESSABLE_CONTENT",
                    "message": "Unprocessable content.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_423 = build_json_response_model(HTTP_MSG_MAPPING[423])
"""
A dictionary response model for the HTTP 423 status code.

```python
{
    "423": {
        "model": MessageResponse,
        "description": "Locked",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 423,
                    "response": "423_LOCKED",
                    "message": "Resource is locked.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_424 = build_json_response_model(HTTP_MSG_MAPPING[424])
"""
A dictionary response model for the HTTP 424 status code.

```python
{
    "424": {
        "model": MessageResponse,
        "description": "Failed Dependency",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 424,
                    "response": "424_FAILED_DEPENDENCY",
                    "message": "Failed dependency.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_425 = build_json_response_model(HTTP_MSG_MAPPING[425])
"""
A dictionary response model for the HTTP 425 status code.

```python
{
    "425": {
        "model": MessageResponse,
        "description": "Too Early",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 425,
                    "response": "425_TOO_EARLY",
                    "message": "Too early.",
                    "headers": {},
                }
            }
        }
    }
```
"""

HTTP_ERROR_426 = build_json_response_model(HTTP_MSG_MAPPING[426])
"""
A dictionary response model for the HTTP 426 status code.

```python
{
    "426": {
        "model": MessageResponse,
        "description": "Upgrade Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 426,
                    "response": "426_UPGRADE_REQUIRED",
                    "message": "Upgrade required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_428 = build_json_response_model(HTTP_MSG_MAPPING[428])
"""
A dictionary response model for the HTTP 428 status code.

```python
{
    "428": {
        "model": MessageResponse,
        "description": "Precondition Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 428,
                    "response": "428_PRECONDITION_REQUIRED",
                    "message": "Precondition required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_429 = build_json_response_model(HTTP_MSG_MAPPING[429])
"""
A dictionary response model for the HTTP 429 status code.

```python
{
    "429": {
        "model": MessageResponse,
        "description": "Too Many Requests",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 429,
                    "response": "429_TOO_MANY_REQUESTS",
                    "message": "Too many requests.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_431 = build_json_response_model(HTTP_MSG_MAPPING[431])
"""
A dictionary response model for the HTTP 431 status code.

```python
{
    "431": {
        "model": MessageResponse,
        "description": "Request Header Fields Too Large",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 431,
                    "response": "431_REQUEST_HEADER_FIELDS_TOO_LARGE",
                    "message": "Request header fields too large.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_451 = build_json_response_model(HTTP_MSG_MAPPING[451])
"""
A dictionary response model for the HTTP 451 status code.

```python
{
    "451": {
        "model": MessageResponse,
        "description": "Unavailable For Legal Reasons",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 451,
                    "response": "451_UNAVAILABLE_FOR_LEGAL_REASONS",
                    "message": "Unavailable for legal reasons.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_500 = build_json_response_model(HTTP_MSG_MAPPING[500])
"""
A dictionary response model for the HTTP 500 status code.

```python
{
    "500": {
        "model": MessageResponse,
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 500,
                    "response": "500_INTERNAL_SERVER_ERROR",
                    "message": "Internal server error.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_501 = build_json_response_model(HTTP_MSG_MAPPING[501])
"""
A dictionary response model for the HTTP 501 status code.

```python
{
    "501": {
        "model": MessageResponse,
        "description": "Not Implemented",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 501,
                    "response": "501_NOT_IMPLEMENTED",
                    "message": "Not implemented.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_502 = build_json_response_model(HTTP_MSG_MAPPING[502])
"""
A dictionary response model for the HTTP 502 status code.

```python
{
    "502": {
        "model": MessageResponse,
        "description": "Bad Gateway",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 502,
                    "response": "502_BAD_GATEWAY",
                    "message": "Bad gateway.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_503 = build_json_response_model(HTTP_MSG_MAPPING[503])
"""
A dictionary response model for the HTTP 503 status code.

```python
{
    "503": {
        "model": MessageResponse,
        "description": "Service Unavailable",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 503,
                    "response": "503_SERVICE_UNAVAILABLE",
                    "message": "Service unavailable.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_504 = build_json_response_model(HTTP_MSG_MAPPING[504])
"""
A dictionary response model for the HTTP 504 status code.

```python
{
    "504": {
        "model": MessageResponse,
        "description": "Gateway Timeout",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 504,
                    "response": "504_GATEWAY_TIMEOUT",
                    "message": "Gateway timeout.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_505 = build_json_response_model(HTTP_MSG_MAPPING[505])
"""
A dictionary response model for the HTTP 505 status code.

```python
{
    "505": {
        "model": MessageResponse,
        "description": "HTTP Version Not Supported",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 505,
                    "response": "505_HTTP_VERSION_NOT_SUPPORTED",
                    "message": "HTTP version not supported.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_506 = build_json_response_model(HTTP_MSG_MAPPING[506])
"""
A dictionary response model for the HTTP 506 status code.

```python
{
    "506": {
        "model": MessageResponse,
        "description": "Variant Also Negotiates",
        "content": {    
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 506,
                    "response": "506_VARIANT_ALSO_NEGOTIATES",
                    "message": "Variant also negotiates.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_507 = build_json_response_model(HTTP_MSG_MAPPING[507])
"""
A dictionary response model for the HTTP 507 status code.

```python
{
    "507": {
        "model": MessageResponse,
        "description": "Insufficient Storage",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 507,
                    "response": "507_INSUFFICIENT_STORAGE",
                    "message": "Insufficient storage.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_508 = build_json_response_model(HTTP_MSG_MAPPING[508])
"""
A dictionary response model for the HTTP 508 status code.

```python
{
    "508": {
        "model": MessageResponse,
        "description": "Loop Detected",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 508,
                    "response": "508_LOOP_DETECTED",
                    "message": "Loop detected.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_510 = build_json_response_model(HTTP_MSG_MAPPING[510])
"""
A dictionary response model for the HTTP 510 status code.

```python
{
    "510": {
        "model": MessageResponse,
        "description": "Not Extended",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 510,
                    "response": "510_NOT_EXTENDED",
                    "message": "Not extended.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""

HTTP_ERROR_511 = build_json_response_model(HTTP_MSG_MAPPING[511])
"""
A dictionary response model for the HTTP 511 status code.

```python
{
    "511": {
        "model": MessageResponse,
        "description": "Network Authentication Required",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "code": 511,
                    "response": "511_NETWORK_AUTHENTICATION_REQUIRED",
                    "message": "Network authentication required.",
                    "headers": {},
                }
            }
        }
    }
}
```
"""
