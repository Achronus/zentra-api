from typing import Any, Literal

from zentra_api.cli.constants import RouteImports, Import
from zentra_api.cli.constants.enums import (
    RouteMethodType,
    RouteMethods,
    RouteParameters,
    RouteResponseCodes,
)

from pydantic import BaseModel, ConfigDict, PrivateAttr


status_codes = {
    200: "HTTP_200_OK",
    201: "HTTP_201_CREATED",
    202: "HTTP_202_ACCEPTED",
    400: "HTTP_400_BAD_REQUEST",
    401: "HTTP_401_UNAUTHORIZED",
}

StatusCodeLiteral = Literal[200, 201, 202, 400, 401]


class Name(BaseModel):
    """A storage container for the name of the route."""

    singular: str
    plural: str


class RouteDefaultDetails(BaseModel):
    """A helper model for retrieving default route details."""

    method: RouteMethods
    multi: bool
    name: str
    schema_model: str | None
    auth: bool

    _response_codes = PrivateAttr(None)
    _parameters = PrivateAttr(None)

    @property
    def response_codes(self) -> list[int]:
        """The response codes for the route."""
        return self._response_codes

    @property
    def parameters(self) -> list[tuple[str, str]]:
        """The parameters for the route."""
        return self._parameters

    def model_post_init(self, __context: Any) -> None:
        self._response_codes = self.set_response_codes()
        self._parameters = self.set_parameters()

    def set_response_codes(self) -> list[int]:
        """Sets the response codes for the route."""
        codes = []

        if self.auth:
            codes.extend(RouteResponseCodes.AUTH.value)

        if self.method in RouteMethods.values(ignore=["get"]):
            codes.extend(RouteResponseCodes.BAD_REQUEST.value)

        return codes

    def set_parameters(self) -> list[tuple[str, str]]:
        """Sets the parameters for the route."""
        params = []

        if self.method in RouteMethods.values(ignore=["post"]) and not self.multi:
            params.append(RouteParameters.ID.value)

        if self.schema_model:
            params.append((self.name, self.schema_model))

        params.append(RouteParameters.DB_DEPEND.value)

        if self.auth:
            params.append(RouteParameters.AUTH_DEPEND.value)

        return params


class Route(BaseModel):
    """A model representation of a route."""

    name: str
    method: RouteMethods
    route: str
    status_code: StatusCodeLiteral
    response_codes: list[int] = []
    parameters: list[tuple[str, str]] = []
    content: str | None = "pass"
    multi: bool = False
    auth: bool = True

    _func_name = PrivateAttr(None)
    _response_model = PrivateAttr(None)
    _schema_model = PrivateAttr(None)

    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context: Any) -> None:
        self._func_name = f"{self.method.lower()}_{self.name.lower()}"
        self._response_model = self.set_response_model()
        self._schema_model = self.set_schema_model()

        details = RouteDefaultDetails(
            method=self.method,
            multi=self.multi,
            name=self.name,
            schema_model=self._schema_model,
            auth=self.auth,
        )

        self.parameters = list(set(self.parameters).union(set(details.parameters)))
        self.response_codes = list(
            set(self.response_codes).union(set(details.response_codes))
        )

    @property
    def func_name(self) -> str:
        """The function name for the route."""
        return self._func_name

    @property
    def response_model(self) -> str:
        """The response model name for the route."""
        return self._response_model

    @property
    def schema_model(self) -> str:
        """The schema model name for the route."""
        return self._schema_model

    def set_response_model(self) -> str:
        """Creates the response model name.

        Examples:
        ```python
            response_model_name("get", "products")  # GetProductsResponse
            response_model_name("get", "product")  # GetProductResponse
            response_model_name("post", "product")  # CreateProductResponse
            response_model_name("put", "product")  # UpdateProductResponse
            response_model_name("patch", "product")  # UpdateProductResponse
        ```
        """
        if self.method == "delete":
            return None

        method = RouteMethodType[self.method.upper()]
        name = self.name.title()
        return f"{method}{name}Response"

    def set_schema_model(self) -> str | None:
        """Creates the schema model (parameter) name."""
        if self.method in ["get", "delete"]:
            return None

        method = RouteMethodType[self.method.upper()]
        name = self.name.title()
        return f"{name}{method}"

    def params_to_str(self) -> str:
        """Converts the parameters to a string."""
        if not self.parameters:
            return ""

        return ", ".join(f"{param[0]}: {param[1]}" for param in self.parameters)

    @staticmethod
    def indent(line: str, spaces: int = 4) -> str:
        """Indents a line of text."""
        return " " * spaces + line

    def to_str(self) -> str:
        """Converts the route to a string."""
        text = [
            f"@router.{self.method}(",
            self.indent(f'"{self.route}",'),
            self.indent(f"status_code=status.{status_codes[self.status_code]},"),
        ]

        if self.response_codes:
            text.append(
                self.indent(
                    f"responses=get_response_models({self.response_codes}),",
                )
            )

        text += [
            self.indent(f"response_model={self.response_model},"),
            ")",
            f"async def {self.func_name}({self.params_to_str()}):",
            self.indent(self.content),
        ]
        return "\n".join(text)


def route_dict_set(name: Name) -> dict[str, Route]:
    """
    Creates a dictionary for a set of routes.

    Parameters:
        name (Name): The name of the route.

    Returns:
        dict[str, Route]: A dictionary of routes.
    """
    return {
        "r1": Route(
            name=name.plural,
            method="get",
            route="",
            status_code=200,
            multi=True,
        ),
        "r2": Route(
            name=name.singular,
            method="get",
            route="/{id}",
            status_code=200,
        ),
        "c": Route(
            name=name.singular,
            method="post",
            route="",
            status_code=201,
        ),
        "u": Route(
            name=name.singular,
            method="put",
            route="/{id}",
            status_code=202,
        ),
        "d": Route(
            name=name.singular,
            method="delete",
            route="/{id}",
            status_code=202,
        ),
    }


def route_imports(add_auth: bool = True) -> list[list[Import]]:
    """
    Creates the route imports for a set of routes.

    Parameters:
        add_auth (bool): A flag to add authentation imports. True by default.

    Returns:
        list[list[Import]]: A list of route imports.
    """
    base = RouteImports.BASE.value

    if add_auth:
        base.extend(RouteImports.AUTH.value)

    return [base, RouteImports.ZENTRA.value, RouteImports.FASTAPI.value]
