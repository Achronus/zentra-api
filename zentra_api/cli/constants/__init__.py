from enum import Enum
import importlib.resources as pkg_resources
from rich.console import Console

from zentra_api.utils.package import package_path


console = Console()

# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/api/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"

PKG_DIR = pkg_resources.files("zentra_api")
LOG_FOLDER = PKG_DIR.joinpath("logs")

ROOT_COMMAND = "zentra-api"

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
    ],
    dev_packages=[
        "pytest",
        "pytest-cov",
    ],
)
