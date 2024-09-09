from typing import Any, Literal

from zentra_api.cli.constants.enums import RouteMethodType, RouteMethods

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


class Route(BaseModel):
    """A model representation of a route."""

    name: str
    method: RouteMethods
    route: str
    status_code: StatusCodeLiteral
    response_codes: list[int] = []
    parameters: list[tuple[str, str]] = []
    content: str | None = None
    multi: bool = False

    _func_name = PrivateAttr(None)
    _response_model = PrivateAttr(None)
    _input_model = PrivateAttr(None)

    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context: Any) -> None:
        self._func_name = f"{self.method.lower()}_{self.name.lower()}"
        self._response_model = self.get_response_model()
        self._input_model = self.get_input_model()

        self.add_default_params()

    @property
    def func_name(self) -> str:
        return self._func_name

    @property
    def response_model(self) -> str:
        return self._response_model

    @property
    def input_model(self) -> str:
        return self._input_model

    def add_default_params(self) -> None:
        """Adds default parameters depending on the method type."""
        if self.method in [RouteMethods.PUT, RouteMethods.PATCH, RouteMethods.DELETE]:
            self.parameters.append(("id", "int"))

        if self.method in [RouteMethods.POST, RouteMethods.PATCH, RouteMethods.PUT]:
            self.parameters.append((self.name, self.input_model))

    def get_response_model(self) -> str:
        """A utility function for creating response model names.

        Examples:
        ```python
            response_model_name("get", "products")  # GetProductsResponse
            response_model_name("post", "product")  # CreateProductResponse
            response_model_name("put", "product")  # UpdateProductResponse
            response_model_name("patch", "product")  # UpdateProductResponse
            response_model_name("delete", "product")  # DeleteProductResponse
        ```
        """
        method = RouteMethodType[self.method.upper()]
        name = self.name.title()
        return f"{method}{name}Response"

    def get_input_model(self) -> str:
        """A utility function for creating input model names."""
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
        ]
        return "\n".join(text)


def route_dict_set(name: Name) -> dict[str, Route]:
    """Creates a dictionary for a set of routes given a `Name` model."""
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
            response_codes=[400],
        ),
        "u": Route(
            name=name.singular,
            method="put",
            route="/{id}",
            status_code=202,
            response_codes=[400, 401],
        ),
        "d": Route(
            name=name.singular,
            method="delete",
            route="/{id}",
            status_code=202,
            response_codes=[400, 401],
        ),
    }
