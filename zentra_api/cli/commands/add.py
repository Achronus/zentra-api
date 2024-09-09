import inflect

from zentra_api.cli.builder.routes import RouteBuilder
from zentra_api.cli.constants.enums import RouteMethods, RouteOptions
from zentra_api.cli.constants.routes import Name, Route, route_dict_set


def store_name(name: str) -> Name:
    """Stores the name in a model with `singular` and `plural` variants."""
    p = inflect.engine()
    singular = p.singular_noun(name)

    if singular:
        single = singular
        plural = name
    else:
        single = name
        plural = p.plural_noun(name)

    return Name(
        singular=single,
        plural=plural,
    )


def create_api_router(name: str) -> str:
    """Creates a string representation of an APIRouter."""
    return f'router = APIRouter(prefix="/{name}", tags=["{name}"])'


class AddSetOfRoutes:
    """Performs project operations for the `add-routeset` command."""

    def __init__(self, name: str, option: RouteOptions) -> None:
        self.name = store_name(name.lower().strip())
        self.option = option

        self.route_map = route_dict_set(self.name)

    def get_routes(self) -> list[Route]:
        """Retrieves the routes from the route map."""
        routes = []

        for key, route in self.route_map.items():
            for letter in self.option:
                if letter in key:
                    routes.append(route)

        return routes

    def build(self) -> None:
        """Build a set of API routes as models."""
        routes = self.get_routes()

        for route in routes:
            print(route.to_str())


class AddRoute:
    """Performs project operations for the `add-route` command."""

    def __init__(self, name: str, route_type: RouteMethods) -> None:
        self.name = store_name(name.lower().strip())
        self.route_type = route_type

        self.type_map = {
            "post": self.create_post,
            "get": self.create_get,
            "put": self.create_put,
            "patch": self.create_patch,
            "delete": self.create_delete,
        }

    def create_get(self) -> str:
        """Creates a GET route."""
        builder = RouteBuilder(route=Route(name="/"))
        return builder.build()

    def create_post(self) -> str:
        """Creates a POST route."""
        pass

    def create_put(self) -> str:
        """Creates a PUT route."""
        pass

    def create_patch(self) -> str:
        """Creates a PATCH route."""
        pass

    def create_delete(self) -> str:
        """Creates a DELETE route."""
        pass

    def build(self) -> None:
        """Builds the route."""
        pass
