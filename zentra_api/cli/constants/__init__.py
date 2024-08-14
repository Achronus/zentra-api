from enum import Enum
from rich.console import Console

from zentra_api.cli.constants.enums import BuildType
from zentra_api.utils.package import package_path


console = Console()


# Core URLs
DOCS_URL = "https://zentra.achronus.dev"
GITHUB_ROOT = "https://github.com/Achronus/zentra"
GITHUB_ISSUES_URL = f"{GITHUB_ROOT}/issues"

GETTING_STARTED_URL = f"{DOCS_URL}/starting/api/"
ERROR_GUIDE_URL = f"{DOCS_URL}/help/errors/"

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


class SetupSuccessCodes(Enum):
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
        build_type: BuildType,
        core_packages: list[str],
        dev_packages: list[str] | None = None,
        deployment_files: dict[str, list[str]] | None = None,
    ) -> None:
        self.build_type = build_type
        self.TEMPLATE_DIR = package_path(
            "zentra_api", ["cli", "template", build_type.value, "project"]
        )
        self.DEPLOYMENT_DIR = package_path(
            "zentra_api", ["cli", "template", build_type.value, "deployment"]
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
    build_type=BuildType.FASTAPI,
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

DJANGO_DETAILS = BuildDetails(
    build_type=BuildType.DJANGO,
    core_packages=[
        "django",
        "django-cors-headers",
        "python-dotenv",
        "pyjwt",
        "djangorestframework",
        "djangorestframework-simplejwt",
    ],
)

BUILD_DETAILS_MAPPING = {
    "fastapi": FASTAPI_DETAILS,
    "django": DJANGO_DETAILS,
}
