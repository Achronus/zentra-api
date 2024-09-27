from enum import Enum
import importlib.resources as pkg_resources
from pydantic import BaseModel
from rich.console import Console

from zentra_api.utils.package import package_path


console = Console()

# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/api/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"
API_REFERENCE_URL = f"{DOCS_URL}/api/reference/"

PKG_DIR = pkg_resources.files("zentra_api")
LOG_FOLDER = PKG_DIR.joinpath("logs")

ROOT_COMMAND = "zentra-api"

# Used in 'zentra_api.responses.get_response_models()'
RESPONSE_ROOT_PATH = "zentra_api.responses"
RESPONSE_MODEL_DIR = "models"

# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"
MAGIC = ":sparkles:"


def pypi_url(package: str) -> str:
    return f"https://pypi.org/pypi/{package}/json"


ENV_FILENAME = ".env"
PYTHON_VERSION = "3.12"

# Poetry scripts
POETRY_SCRIPTS = [
    ("run-dev", "scripts.run:development"),
    ("run-prod", "scripts.run:production"),
    ("db-migrate", "scripts.db_migrate:main"),
]


class SetupSuccessCodes(Enum):
    TEST_SUCCESS = -2
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    PROJECT_NOT_FOUND = 20
    UNKNOWN_ERROR = 1000


class RouteSuccessCodes(Enum):
    CREATED = 30


class RouteErrorCodes(Enum):
    FOLDER_EXISTS = 40


class BuildDetails:
    """A storage container for project build details."""

    def __init__(
        self,
        build_type: str,
        core_packages: list[str],
        dev_packages: list[str] | None = [],
        deployment_files: dict[str, list[str]] | None = None,
    ) -> None:
        self.build_type = build_type
        self.TEMPLATE_DIR = package_path(
            "zentra_api", ["cli", "template", build_type, "project"]
        )
        self.DEPLOYMENT_DIR = package_path(
            "zentra_api", ["cli", "template", build_type, "deployment"]
        )

        self.CORE_PACKAGES = core_packages
        self.DEV_PACKAGES = dev_packages
        self.DEPLOYMENT_FILE_MAPPING = deployment_files


# Deployment file options
DOCKER_FILES = [".dockerignore", "Dockerfile.backend"]
DOCKER_COMPOSE_FILES = DOCKER_FILES + ["docker-compose.yml"]
RAILWAY_FILES = DOCKER_FILES + ["railway.toml"]

# Build details
FASTAPI_DETAILS = BuildDetails(
    build_type="fastapi",
    deployment_files={
        "railway": RAILWAY_FILES,
        "dockerfile": DOCKER_FILES,
        "docker_compose": DOCKER_COMPOSE_FILES,
    },
    core_packages=[
        "fastapi",
        "sqlalchemy",
        "alembic",
        "pydantic-settings",
        "pyjwt",
        "bcrypt",
        "zentra-api",
    ],
    dev_packages=[
        "pytest",
        "pytest-cov",
    ],
)


class Import(BaseModel):
    """A model for imports."""

    root: str
    modules: list[str] | None = None
    items: list[str]
    add_dot: bool = True

    def to_str(self) -> str:
        """Converts the import to a string."""
        return f"from {self.root}{'.' if self.add_dot else ''}{'.'.join(self.modules) if self.modules else ''} import {", ".join(self.items)}"


BASE_IMPORTS = [
    Import(
        root="app",
        modules=["core", "dependencies"],
        items=["DB_DEPEND"],
    ),
    Import(
        root="app",
        modules=["db_models"],
        items=["CONNECT"],
    ),
]

AUTH_IMPORTS = [
    Import(
        root="app",
        modules=["auth"],
        items=["ACTIVE_USER_DEPEND"],
    )
]

ZENTRA_IMPORTS = [
    Import(
        root="zentra_api",
        modules=["responses"],
        items=["SuccessMsgResponse", "get_response_models"],
    )
]

FASTAPI_IMPORTS = [
    Import(
        root="fastapi",
        items=["APIRouter", "HTTPException", "status"],
        add_dot=False,
    )
]


class RouteImports(Enum):
    BASE = BASE_IMPORTS
    AUTH = AUTH_IMPORTS
    ZENTRA = ZENTRA_IMPORTS
    FASTAPI = FASTAPI_IMPORTS


SUCCESS_MSG_RESPONSE_MODEL = "SuccessMsgResponse"
ROUTE_RESPONSE_MODEL_BLACKLIST = [None, SUCCESS_MSG_RESPONSE_MODEL]
