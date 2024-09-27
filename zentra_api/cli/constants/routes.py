from pathlib import Path
import textwrap
from typing import Any, Literal

from zentra_api.cli.constants import SUCCESS_MSG_RESPONSE_MODEL, RouteImports, Import
from zentra_api.cli.constants.enums import (
    RouteFile,
    RouteMethodType,
    RouteMethods,
    RouteParameters,
    RouteResponseCodes,
    RouteResponseType,
)

from pydantic import BaseModel, ConfigDict, PrivateAttr

from zentra_api.cli.utils import indent


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


class RouteFilepaths(BaseModel):
    """A storage container for the route filepaths."""

    root: Path

    _init = PrivateAttr(None)
    _schema = PrivateAttr(None)
    _response = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        self._init = Path(self.root, RouteFile.INIT.value)
        self._schema = Path(self.root, RouteFile.SCHEMA.value)
        self._response = Path(self.root, RouteFile.RESPONSES.value)

    @property
    def init_file(self) -> Path:
        return self._init

    @property
    def schema_file(self) -> Path:
        return self._schema

    @property
    def responses_file(self) -> Path:
        return self._response


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
    multi: bool = False
    auth: bool = True

    _func_name = PrivateAttr(None)
    _response_model = PrivateAttr(None)
    _schema_model = PrivateAttr(None)

    model_config = ConfigDict(use_enum_values=True)

    def model_post_init(self, __context: Any) -> None:
        self._func_name = f"{self.func_name_start()}_{self.name.lower()}"
        self._response_model = self.set_response_model()
        self._schema_model = self.set_schema_model()

        details = RouteDefaultDetails(
            method=self.method,
            multi=self.multi,
            name=self.name,
            schema_model=self._schema_model,
            auth=self.auth,
        )

        self.parameters += [
            param for param in details.parameters if param not in self.parameters
        ]  # Keep parameter order
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

    def func_name_start(self) -> str:
        """
        Sets the start of the function name based on self.method.

        Example:
            `self.method == "get"` => `get`
            `self.method == "post"` => `create`
            `self.method == "put" | "patch"` => `update`
            `self.method == "delete"` => `delete`
        """
        if self.method == RouteMethods.POST:
            return "create"
        elif self.method == RouteMethods.PUT or self.method == RouteMethods.PATCH:
            return "update"

        return self.method.lower()

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
        if self.method == RouteMethods.DELETE:
            return SUCCESS_MSG_RESPONSE_MODEL

        method = RouteMethodType[self.method.upper()]
        name = self.name.title()
        return f"{method}{name}Response"

    def set_schema_model(self) -> str | None:
        """Creates the schema model (parameter) name."""
        if self.method == RouteMethods.GET or self.method == RouteMethods.DELETE:
            return None

        method = RouteMethodType[self.method.upper()]
        name = self.name.title()
        return f"{name}{method}"

    def params_to_str(self) -> str:
        """Converts the parameters to a string."""
        if not self.parameters:
            return ""

        return ", ".join(f"{param[0]}: {param[1]}" for param in self.parameters)

    def to_str(self, name: Name) -> str:
        """Converts the route to a string."""
        text = [
            f"@router.{self.method}(",
            indent(f'"{self.route}",'),
            indent(f"status_code=status.{status_codes[self.status_code]},"),
        ]

        if self.response_codes:
            text.append(
                indent(
                    f"responses=get_response_models({self.response_codes}),",
                )
            )

        text += [
            indent(f"response_model={self.response_model},"),
            ")",
            f"async def {self.func_name}({self.params_to_str()}):",
            route_content(name, self.method, self.multi, self.response_model),
        ]
        return "\n".join(text).rstrip()

    def response_model_class(self, name: Name) -> str:
        """
        Creates the route response model class.
        """

        def data_type() -> str:
            """A helper method for creating the response data type T."""
            dtype = name.singular.title()

            if self.method != RouteMethods.GET:
                dtype += "ID"

            if self.multi:
                return f"list[{dtype}]"

            return dtype

        return textwrap.dedent(f'''
        class {self.response_model}(SuccessResponse[{data_type()}]):
            """A response for {RouteResponseType[self.method.upper()].value} a {"list of " if self.multi else ''}{name.plural if self.multi else name.singular}."""
            pass
        ''').strip("\n")


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


def route_content(
    name: Name, method: RouteMethods, multi: bool, response_model: str
) -> str:
    """
    Creates the route content for a single route.

    Parameters:
        name (Name): The name model containing a single and multi variant of the routeset name.
        method (RouteMethods): The type of route.
        multi (bool): A flag to determine if the route returns a list of values.
        response_model (str): The name of the response model.

    Returns:
        str: A string of route content.
    """

    def db_get_method(param: str | None = None) -> str:
        """A utility method for retrieving the database get method."""
        if multi:
            return "get_multiple(db, skip=0, limit=10)"

        if param:
            return f"get(db, {param}.id)"

        return "get(db, id)"

    content = "pass"

    out_name = name.plural if multi else name.singular
    if method == RouteMethods.GET:
        content = textwrap.dedent(f"""
        {out_name} = CONNECT.{name.plural}.{db_get_method()}
        
        return {response_model}(
            code=status.HTTP_200_OK,
            data={out_name}.model_dump(),
        )
        """)
    elif method == RouteMethods.POST:
        content = textwrap.dedent(f"""
        exists = CONNECT.{name.plural}.{db_get_method(name.singular)}

        if exists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="{name.singular.title()} already exists."
            )

        {out_name} = CONNECT.{name.plural}.create(db, {name.singular}.model_dump())
        return {response_model}(
            code=status.HTTP_201_CREATED,
            data={name.singular}.model_dump(),
        )
        """)
    elif method == RouteMethods.PATCH or method == RouteMethods.PUT:
        content = textwrap.dedent(f"""
        exists = CONNECT.{name.plural}.update(db, id, {name.singular}.model_dump())

        if not exists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="{name.singular.title()} does not exist."
            )

        {out_name} = CONNECT.{name.plural}.{db_get_method()}
        return {response_model}(
            code=status.HTTP_202_ACCEPTED,
            data={out_name}.model_dump(),
        )
        """)
    elif method == RouteMethods.DELETE:
        content = textwrap.dedent(f"""
        exists = CONNECT.{name.plural}.delete(db, id)

        if not exists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="{name.singular.title()} does not exist."
            )

        return SuccessMsgResponse(code=status.HTTP_202_ACCEPTED, message="{name.singular.title()} deleted.")
        """)

    content = [
        indent(line) if line.strip() else line
        for line in content.strip("\n").split("\n")
    ]
    return "\n".join(content)
