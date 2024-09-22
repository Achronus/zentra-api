from pathlib import Path
from unittest import mock
import pytest
import typer

from zentra_api.cli.commands.add import (
    AddRouteTasks,
    AddSetOfRoutes,
    store_name,
    create_api_router,
    get_route_folder,
)
from zentra_api.cli.commands.setup import Setup
from zentra_api.cli.constants import RouteErrorCodes, RouteSuccessCodes
from zentra_api.cli.constants.enums import RouteOptions
from zentra_api.cli.constants.routes import Name, route_dict_set


class TestStoreName:
    @staticmethod
    def test_plural() -> None:
        assert store_name("projects") == Name(singular="project", plural="projects")

    @staticmethod
    def test_singular() -> None:
        assert store_name("child") == Name(singular="child", plural="children")


class TestCreateAPIRouter:
    @staticmethod
    def test_output() -> None:
        assert (
            create_api_router("projects")
            == 'router = APIRouter(prefix="/projects", tags=["Projects"])'
        )


class TestGetRouteFolder:
    @staticmethod
    def test_tmp_path(tmp_path: Path) -> None:
        assert get_route_folder(
            name=Name(singular="project", plural="projects"),
            root=tmp_path,
        ) == Path(tmp_path, "app", "api", "projects")

    @staticmethod
    def test_custom() -> None:
        assert get_route_folder(
            name=Name(singular="project", plural="projects"),
            root=Path("test_project"),
        ) == Path("test_project", "app", "api", "projects")


class TestAddSetOfRoutes:
    @pytest.fixture
    def set_of_routes(self, tmp_path: Path) -> AddSetOfRoutes:
        try:
            setup = Setup("test_project", no_output=True, root=tmp_path)
            setup.build()
        except typer.Exit:
            pass

        return AddSetOfRoutes(name="projects", option=RouteOptions.CRUD, root=tmp_path)

    class TestCheckFolderExists:
        @staticmethod
        def test_false(set_of_routes: AddSetOfRoutes) -> None:
            assert set_of_routes.check_folder_exists() is False

        @staticmethod
        def test_true(set_of_routes: AddSetOfRoutes) -> None:
            set_of_routes.route_tasks._create_route_files()
            assert set_of_routes.check_folder_exists()

    class TestBuild:
        @staticmethod
        def test_folder_exists_error(set_of_routes: AddSetOfRoutes) -> None:
            set_of_routes.route_tasks._create_route_files()
            with pytest.raises(typer.Exit) as excinfo:
                set_of_routes.build()

            assert excinfo.value.exit_code == RouteErrorCodes.FOLDER_EXISTS

        @staticmethod
        def test_completes(set_of_routes: AddSetOfRoutes) -> None:
            with pytest.raises(typer.Exit) as excinfo:
                set_of_routes.build()

            assert excinfo.value.exit_code == RouteSuccessCodes.CREATED

        @staticmethod
        @mock.patch.object(AddRouteTasks, "get_tasks_for_set", return_value=[])
        def test_tasks_executed(
            mock_tasks: AddRouteTasks, set_of_routes: AddSetOfRoutes
        ) -> None:
            set_of_routes.route_tasks._create_route_files()
            with pytest.raises(typer.Exit):
                set_of_routes.build()

            for task in mock_tasks.get_tasks_for_set():
                task.assert_called_once()


class TestAddRouteTasks:
    @pytest.fixture
    def create_project(self, tmp_path: Path) -> None:
        try:
            setup = Setup("test_project", no_output=True, root=tmp_path)
            setup.build()
        except typer.Exit:
            pass

    class TestGetRoutes:
        @staticmethod
        def test_crud(create_project, tmp_path) -> None:
            name = Name(singular="project", plural="projects")
            tasks = AddRouteTasks(
                name=name,
                root=tmp_path,
                option=RouteOptions.CRUD,
            )
            routes = route_dict_set(name)
            assert tasks._get_routes() == [value for value in routes.values()]

        @staticmethod
        def test_cr(create_project, tmp_path) -> None:
            name = Name(singular="project", plural="projects")
            tasks = AddRouteTasks(
                name=name,
                root=tmp_path,
                option=RouteOptions.CREATE_READ,
            )
            routes = route_dict_set(name)
            keys = ["r1", "r2", "c"]
            assert tasks._get_routes() == [routes[key] for key in keys]

        @staticmethod
        def test_ud(create_project, tmp_path) -> None:
            name = Name(singular="project", plural="projects")
            tasks = AddRouteTasks(
                name=name,
                root=tmp_path,
                option=RouteOptions.UPDATE_DELETE,
            )
            routes = route_dict_set(name)
            keys = ["u", "d"]
            assert tasks._get_routes() == [routes[key] for key in keys]
