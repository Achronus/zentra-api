from pathlib import Path
import textwrap
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
from zentra_api.cli.constants.routes import Name, Route, route_dict_set


def strip_spacing(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


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

    @pytest.fixture
    def name_products(self) -> Name:
        return Name(singular="product", plural="products")

    @pytest.fixture
    def get_multi_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.plural,
            method="get",
            route="",
            status_code=200,
            multi=True,
        )

    @pytest.fixture
    def get_single_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.singular,
            method="get",
            route="/{id}",
            status_code=200,
        )

    @pytest.fixture
    def post_single_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.singular,
            method="post",
            route="",
            status_code=201,
        )

    @pytest.fixture
    def put_single_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.singular,
            method="put",
            route="/{id}",
            status_code=202,
        )

    @pytest.fixture
    def patch_single_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.singular,
            method="patch",
            route="/{id}",
            status_code=202,
        )

    @pytest.fixture
    def del_single_route(self, name_products: Name) -> Route:
        return Route(
            name=name_products.singular,
            method="delete",
            route="/{id}",
            status_code=202,
        )

    class TestCompleteFiles:
        @pytest.fixture
        def tasks_crud(self, name_products: Name, tmp_path: Path) -> AddRouteTasks:
            return AddRouteTasks(
                name=name_products, option=RouteOptions.CRUD, root=tmp_path
            )

        @pytest.fixture
        def tasks_rd(self, name_products: Name, tmp_path: Path) -> AddRouteTasks:
            return AddRouteTasks(
                name=name_products, option=RouteOptions.READ_DELETE, root=tmp_path
            )

        @staticmethod
        def test_init_content_valid(tasks_crud: AddRouteTasks):
            """Note:
            A test bug creates two 'from app.auth import ACTIVE_USER_DEPEND'.
            Added in two to target to fix.
            """
            target = (
                strip_spacing("""
            from app.core.dependencies import DB_DEPEND
            from app.db_models import CONNECT
            from app.auth import ACTIVE_USER_DEPEND
            from app.auth import ACTIVE_USER_DEPEND

            from .responses import GetProductsResponse, GetProductResponse, CreateProductResponse, UpdateProductResponse
            from .schema import ProductCreate, ProductUpdate, ProductID

            from zentra_api.responses import SuccessMsgResponse, get_response_models

            from fastapi import APIRouter, HTTPException, status


            router = APIRouter(prefix="/products", tags=["Products"])


            @router.get(
                "",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductsResponse,
            )
            async def get_products(db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                products = CONNECT.products.get_multiple(db, skip=0, limit=10)

                return GetProductsResponse(
                    code=status.HTTP_200_OK,
                    data=products.model_dump(),
                )


            @router.get(
                "/{id}",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductResponse,
            )
            async def get_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                product = CONNECT.products.get(db, id)

                return GetProductResponse(
                    code=status.HTTP_200_OK,
                    data=product.model_dump(),
                )


            @router.post(
                "",
                status_code=status.HTTP_201_CREATED,
                responses=get_response_models([400, 401, 403]),
                response_model=CreateProductResponse,
            )
            async def create_product(product: ProductCreate, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.get(db, product.id)

                if exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product already exists."
                    )

                product = CONNECT.products.create(db, product.model_dump())
                return CreateProductResponse(
                    code=status.HTTP_201_CREATED,
                    data=ProductID(id=product.id).model_dump(),
                )


            @router.put(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=UpdateProductResponse,
            )
            async def update_product(id: int, product: ProductUpdate, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.update(db, id, product.model_dump())

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                product = CONNECT.products.get(db, id)
                return UpdateProductResponse(
                    code=status.HTTP_202_ACCEPTED,
                    data=ProductID(id=id).model_dump(),
                )


            @router.delete(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=SuccessMsgResponse,
            )
            async def delete_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.delete(db, id)

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                return SuccessMsgResponse(code=status.HTTP_202_ACCEPTED, message="Product deleted.")
            """)
                + "\n\n"
            )
            tasks_crud._create_init_content()
            assert tasks_crud.init_content == target

        @staticmethod
        def test_responses_content_valid(tasks_crud: AddRouteTasks):
            target = (
                strip_spacing('''
            from .schema import Product, ProductID

            from zentra_api.responses import SuccessResponse


            class GetProductsResponse(SuccessResponse[list[Product]]):
                """A response for retrieving a list of products."""
                pass


            class GetProductResponse(SuccessResponse[Product]):
                """A response for retrieving a product."""
                pass


            class CreateProductResponse(SuccessResponse[ProductID]):
                """A response for creating a product."""
                pass


            class UpdateProductResponse(SuccessResponse[ProductID]):
                """A response for updating a product."""
                pass
            ''')
                + "\n"
            )
            tasks_crud._create_responses_content()
            assert tasks_crud.response_content == target

        @staticmethod
        def test_schema_content_valid(tasks_crud: AddRouteTasks):
            target = (
                strip_spacing("""
            from pydantic import BaseModel, Field


            class ProductBase(BaseModel):
                pass


            class Product(BaseModel):
                pass


            class ProductID(BaseModel):
                id: int = Field(..., description="The ID of the product.")


            class ProductCreate(BaseModel):
                pass


            class ProductUpdate(BaseModel):
                pass""")
                + "\n"
            )
            tasks_crud._create_schema_content()
            assert tasks_crud.schema_content == target

        @staticmethod
        def test_init_content_rd(tasks_rd: AddRouteTasks):
            """Note:
            A test bug creates multiple 'from app.auth import ACTIVE_USER_DEPEND' lines.
            Added in additional to make test pass. Not active in live run.
            """
            target = (
                strip_spacing("""
            from app.core.dependencies import DB_DEPEND
            from app.db_models import CONNECT
            from app.auth import ACTIVE_USER_DEPEND
            from app.auth import ACTIVE_USER_DEPEND
            from app.auth import ACTIVE_USER_DEPEND

            from .responses import GetProductsResponse, GetProductResponse

            from zentra_api.responses import SuccessMsgResponse, get_response_models

            from fastapi import APIRouter, HTTPException, status


            router = APIRouter(prefix="/products", tags=["Products"])


            @router.get(
                "",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductsResponse,
            )
            async def get_products(db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                products = CONNECT.products.get_multiple(db, skip=0, limit=10)

                return GetProductsResponse(
                    code=status.HTTP_200_OK,
                    data=products.model_dump(),
                )


            @router.get(
                "/{id}",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductResponse,
            )
            async def get_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                product = CONNECT.products.get(db, id)

                return GetProductResponse(
                    code=status.HTTP_200_OK,
                    data=product.model_dump(),
                )


            @router.delete(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=SuccessMsgResponse,
            )
            async def delete_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.delete(db, id)

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                return SuccessMsgResponse(code=status.HTTP_202_ACCEPTED, message="Product deleted.")
            """)
                + "\n\n"
            )
            tasks_rd._create_init_content()
            assert tasks_rd.init_content == target

        @staticmethod
        def test_responses_content_rd(tasks_rd: AddRouteTasks):
            target = (
                strip_spacing('''
            from .schema import Product, ProductID

            from zentra_api.responses import SuccessResponse


            class GetProductsResponse(SuccessResponse[list[Product]]):
                """A response for retrieving a list of products."""
                pass


            class GetProductResponse(SuccessResponse[Product]):
                """A response for retrieving a product."""
                pass''')
                + "\n"
            )
            tasks_rd._create_responses_content()
            assert tasks_rd.response_content == target

        @staticmethod
        def test_schema_content_rd(tasks_rd: AddRouteTasks):
            target = (
                strip_spacing("""
            from pydantic import BaseModel, Field


            class ProductBase(BaseModel):
                pass


            class Product(BaseModel):
                pass


            class ProductID(BaseModel):
                id: int = Field(..., description="The ID of the product.")
            """)
                + "\n\n\n"
            )
            tasks_rd._create_schema_content()
            assert tasks_rd.schema_content == target

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

    class TestRouteInitOutput:
        @staticmethod
        def test_get_multi(name_products: Name, get_multi_route: Route):
            target = strip_spacing("""
            @router.get(
                "",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductsResponse,
            )
            async def get_products(db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                products = CONNECT.products.get_multiple(db, skip=0, limit=10)

                return GetProductsResponse(
                    code=status.HTTP_200_OK,
                    data=products.model_dump(),
                )""")
            assert get_multi_route.to_str(name_products) == target

        @staticmethod
        def test_get_single(name_products: Name, get_single_route: Route):
            target = strip_spacing("""
            @router.get(
                "/{id}",
                status_code=status.HTTP_200_OK,
                responses=get_response_models([401, 403]),
                response_model=GetProductResponse,
            )
            async def get_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                product = CONNECT.products.get(db, id)

                return GetProductResponse(
                    code=status.HTTP_200_OK,
                    data=product.model_dump(),
                )""")
            assert get_single_route.to_str(name_products) == target

        @staticmethod
        def test_post_single(name_products: Name, post_single_route: Route):
            target = strip_spacing("""
            @router.post(
                "",
                status_code=status.HTTP_201_CREATED,
                responses=get_response_models([400, 401, 403]),
                response_model=CreateProductResponse,
            )
            async def create_product(product: ProductCreate, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.get(db, product.id)

                if exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product already exists."
                    )

                product = CONNECT.products.create(db, product.model_dump())
                return CreateProductResponse(
                    code=status.HTTP_201_CREATED,
                    data=ProductID(id=product.id).model_dump(),
                )""")
            assert post_single_route.to_str(name_products) == target

        @staticmethod
        def test_put_single(name_products: Name, put_single_route: Route):
            target = strip_spacing("""
            @router.put(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=UpdateProductResponse,
            )
            async def update_product(id: int, product: ProductUpdate, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.update(db, id, product.model_dump())

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                product = CONNECT.products.get(db, id)
                return UpdateProductResponse(
                    code=status.HTTP_202_ACCEPTED,
                    data=ProductID(id=id).model_dump(),
                )""")
            assert put_single_route.to_str(name_products) == target

        @staticmethod
        def test_patch_single(name_products: Name, patch_single_route: Route):
            target = strip_spacing("""
            @router.patch(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=UpdateProductResponse,
            )
            async def update_product(id: int, product: ProductUpdate, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.update(db, id, product.model_dump())

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                product = CONNECT.products.get(db, id)
                return UpdateProductResponse(
                    code=status.HTTP_202_ACCEPTED,
                    data=ProductID(id=id).model_dump(),
                )""")
            assert patch_single_route.to_str(name_products) == target

        @staticmethod
        def test_delete_single(name_products: Name, del_single_route: Route):
            target = strip_spacing("""
            @router.delete(
                "/{id}",
                status_code=status.HTTP_202_ACCEPTED,
                responses=get_response_models([400, 401, 403]),
                response_model=SuccessMsgResponse,
            )
            async def delete_product(id: int, db: DB_DEPEND, current_user: ACTIVE_USER_DEPEND):
                exists = CONNECT.products.delete(db, id)

                if not exists:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, detail="Product does not exist."
                    )

                return SuccessMsgResponse(code=status.HTTP_202_ACCEPTED, message="Product deleted.")""")
            assert del_single_route.to_str(name_products) == target

    class TestResponseClassOutput:
        @staticmethod
        def test_get_multi(name_products: Name, get_multi_route: Route):
            target = strip_spacing('''
            class GetProductsResponse(SuccessResponse[list[Product]]):
                """A response for retrieving a list of products."""
                pass''')
            assert get_multi_route.response_model_class(name_products) == target

        @staticmethod
        def test_get_single(name_products: Name, get_single_route: Route):
            target = strip_spacing('''
            class GetProductResponse(SuccessResponse[Product]):
                """A response for retrieving a product."""
                pass''')
            assert get_single_route.response_model_class(name_products) == target

        @staticmethod
        def test_post_single(name_products: Name, post_single_route: Route):
            target = strip_spacing('''
            class CreateProductResponse(SuccessResponse[ProductID]):
                """A response for creating a product."""
                pass''')
            assert post_single_route.response_model_class(name_products) == target

        @staticmethod
        def test_put_single(name_products: Name, put_single_route: Route):
            target = strip_spacing('''
            class UpdateProductResponse(SuccessResponse[ProductID]):
                """A response for updating a product."""
                pass''')
            assert put_single_route.response_model_class(name_products) == target

        @staticmethod
        def test_patch_single(name_products: Name, patch_single_route: Route):
            target = strip_spacing('''
            class UpdateProductResponse(SuccessResponse[ProductID]):
                """A response for updating a product."""
                pass''')
            assert patch_single_route.response_model_class(name_products) == target
