from zentra_api.cli.constants.routes import Route


class RouteBuilder:
    """A class for building FastAPI routes."""

    def __init__(self, route: Route) -> None:
        self.route = route

    def build(self) -> None:
        pass
