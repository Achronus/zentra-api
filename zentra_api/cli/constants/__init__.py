from enum import Enum
from rich.console import Console

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


ENV_FILENAME = ".env.backend"
PYTHON_VERSION = "3.12"

# Define packages
CORE_PIP_PACKAGES = [
    "fastapi",
    "sqlalchemy",
    "alembic",
    "pydantic-settings",
    "pyjwt",
    "bcrypt",
    "zentra_api",
]

DEV_PIP_PACKAGES = [
    "pytest",
    "pytest-cov",
]

# Filepaths
TEMPLATE_DIR = package_path("zentra_api", ["cli", "template", "project"])
DEPLOYMENT_DIR = package_path("zentra_api", ["cli", "template", "deployment"])

# Deployment file options
DOCKER_FILES = [".dockerignore", "Dockerfile.backend"]
DOCKER_COMPOSE_FILES = DOCKER_FILES + ["docker-compose.yml"]
RAILWAY_FILES = DOCKER_FILES + ["railway.toml"]

DEPLOYMENT_FILE_MAPPING = {
    "railway": RAILWAY_FILES,
    "dockerfile": DOCKER_FILES,
    "docker_compose": DOCKER_COMPOSE_FILES,
}


class SetupSuccessCodes(Enum):
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    UNKNOWN_ERROR = 1000
