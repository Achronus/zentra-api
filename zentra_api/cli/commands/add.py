import json
import os
from typing import Callable
from pathlib import Path

from zentra_api.cli.conf.checks import zentra_config_path
from zentra_api.cli.constants import (
    ROUTE_RESPONSE_MODEL_BLACKLIST,
    Import,
    RouteErrorCodes,
    RouteSuccessCodes,
)
from zentra_api.cli.builder.routes import RouteBuilder
from zentra_api.cli.constants.enums import RouteFile, RouteMethods, RouteOptions
from zentra_api.cli.constants.routes import (
    Name,
    Route,
    RouteFilepaths,
    route_dict_set,
    route_imports,
)
from zentra_api.cli.constants.models import Config, Imports

import inflect
import typer
from rich.progress import track


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
    """
    Creates a string representation of an APIRouter.

    Parameters:
        name (str): The name of the route set.

    Returns:
        str: The string representation of the APIRouter.
    """
    return f'router = APIRouter(prefix="/{name.lower()}", tags=["{name.capitalize()}"])'


def get_route_folder(name: Name, root: Path) -> Path:
    """
    Retrieves the path to the route folder.

    Parameters:
        name (Name): The name of the route set.
        root (Path): The root directory of the project.

    Returns:
        Path: The path to the route folder.
    """
    return Path(root, "app", "api", name.plural)


class AddSetOfRoutes:
    """
    Performs project operations for the `add-routeset` command.

    Parameters:
        name (str): The name of the route set.
        option (RouteOptions): The type of route set to create.
        root (Path): The root directory of the project. Defaults to the parent of the config file. (optional)
    """

    def __init__(self, name: str, option: RouteOptions, root: Path = None) -> None:
        self.name = store_name(name.lower().strip())
        self.root = root if root else zentra_config_path().parent
        self.route_tasks = AddRouteTasks(name=self.name, root=self.root, option=option)

    def check_folder_exists(self) -> bool:
        """Checks if the folder name exists in the API directory."""
        return get_route_folder(self.name, self.root).exists()

    def build(self) -> None:
        """Build a set of API routes as models."""
        if self.check_folder_exists():
            raise typer.Exit(code=RouteErrorCodes.FOLDER_EXISTS)

        tasks = self.route_tasks.get_tasks_for_set()

        for task in track(tasks, description="Building..."):
            task()

        raise typer.Exit(code=RouteSuccessCodes.CREATED)


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


class AddRouteTasks:
    """Contains the tasks for the `add-routeset` and `add-route` commands."""

    def __init__(self, name: Name, root: Path, option: RouteOptions) -> None:
        self.name = name
        self.root = root
        self.option = option

        self.config: Config = Config(**json.loads(zentra_config_path().read_text()))
        self.route_map = route_dict_set(self.name)
        self.api_route_str = create_api_router(self.name.plural)
        self.route_path = get_route_folder(self.name, self.root)
        self.asset_paths = RouteFilepaths(root=self.route_path)

        self.init_content = None
        self.schema_content = None
        self.response_content = None

    def _get_routes(self) -> list[Route]:
        """Retrieves the routes from the route map."""
        routes = []

        for key, route in self.route_map.items():
            for letter in self.option:
                if letter in key:
                    routes.append(route)

        return routes

    def _create_init_content(self, routes: list[Route]) -> None:
        """Creates the '__init__.py' file content."""
        response_models = [
            route.response_model
            for route in routes
            if route.response_model not in ROUTE_RESPONSE_MODEL_BLACKLIST
        ]
        schema_models = [route.schema_model for route in routes if route.schema_model]
        add_auth = any([route.auth for route in routes])

        folder_imports = [
            Import(
                root=".",
                modules=[RouteFile.RESPONSES.value.split(".")[0]],
                items=response_models,
                add_dot=False,
            ),
            Import(
                root=".",
                modules=[RouteFile.SCHEMA.value.split(".")[0]],
                items=schema_models,
                add_dot=False,
            ),
        ]
        file_imports: list[list[Import]] = route_imports(add_auth=add_auth)
        file_imports.insert(1, folder_imports)
        file_imports = Imports(items=file_imports).to_str()

        self.init_content = "\n".join(
            [
                file_imports,
                "",
                self.api_route_str,
                "\n",
                "\n".join([route.to_str(self.name) + "\n\n" for route in routes]),
            ]
        )

    def _create_schema_content(self, routes: list[Route]) -> None:
        """Creates the 'schema.py' file content."""
        pass

    def _create_responses_content(self, routes: list[Route]) -> None:
        """Creates the 'responses.py' file content."""
        name = self.name.singular.title()
        schema_models = [name, f"{name}ID"]
        response_classes = [
            route.response_model_class(self.name)
            for route in routes
            if route.method != RouteMethods.DELETE
        ]

        file_imports = [
            [
                Import(
                    root="app",
                    modules=["api", self.name.plural, "schema"],
                    items=schema_models,
                )
            ],
            [
                Import(
                    root="zentra_api",
                    modules=[RouteFile.RESPONSES.value.split(".")[0]],
                    items=["SuccessResponse"],
                )
            ],
        ]

        self.response_content = (
            "\n".join(
                [
                    Imports(items=file_imports).to_str(),
                    "",
                    "\n".join([response + "\n\n" for response in response_classes]),
                ]
            ).rstrip("\n")
            + "\n"
        )

    def _update_files(self) -> None:
        """Updates the '__init__.py', 'schema.py', and 'responses.py' files."""
        self.asset_paths.init_file.write_text(self.init_content)
        # self.asset_paths.schema_file.write_text(self.schema_content)
        self.asset_paths.responses_file.write_text(self.response_content)

    def _create_route_files(self) -> None:
        """Creates a new set of route files."""
        os.makedirs(self.route_path, exist_ok=True)

        for file in RouteFile.values():
            open(Path(self.route_path, file), "w").close()

    def get_tasks_for_set(self) -> list[Callable]:
        """Retrieves the tasks for the `add-routeset` command."""
        tasks = []

        if not self.route_path.exists():
            tasks.append(self._create_route_files)

        routes = self._get_routes()
        self._create_init_content(routes)
        # self._create_schema_content(routes)
        self._create_responses_content(routes)

        tasks.extend([self._update_files])
        return tasks

    def get_tasks_for_route(self) -> list[Callable]:
        """Retrieves the tasks for the `add-route` command."""
        pass
