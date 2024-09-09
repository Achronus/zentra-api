import secrets
from typing import Annotated
import typer

from zentra_api.cli.commands.add import AddRoutes
from zentra_api.cli.commands.build import Build
from zentra_api.cli.commands.setup import Setup

from zentra_api.cli.constants import console
from zentra_api.cli.constants.enums import RouteOptions, DeploymentType
from zentra_api.cli.constants.message import MSG_MAPPER, MessageHandler
from zentra_api.validation import SingleWord


init_command = typer.style("init", typer.colors.YELLOW)
add_command = typer.style("add-", typer.colors.YELLOW)

app = typer.Typer(
    help=f"Welcome to Zentra API! Create a project with {init_command} or add something with one of the {add_command} commands.",
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

msg_handler = MessageHandler(console, MSG_MAPPER)


@app.command("init")
def init(
    project_name: Annotated[
        str,
        typer.Argument(
            help="The name of the project to create",
            show_default=False,
        ),
    ],
    hide_output: Annotated[
        bool,
        typer.Option(
            "--hide-output",
            "-ho",
            help="Suppress console output",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Creates a new FastAPI project in a folder called <PROJECT_NAME>."""
    try:
        if len(project_name) < 2:
            raise ValueError("'project_name' must be at least 2 characters long.")

        setup = Setup(project_name, no_output=hide_output)
        setup.build()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("add-route")
def add(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the route set to add. Must be a single word that only contains letters (a-zA-Z).",
            show_default=False,
        ),
    ],
    option: Annotated[
        RouteOptions,
        typer.Argument(
            help="A string of characters representing the set of routes to add. 'c' = create, 'r' = read, 'u' = update, 'd' = delete.",
        ),
    ] = "crud",
) -> None:
    """Adds a new set of routes based on <OPTION> into the project in a folder called <NAME>."""
    try:
        SingleWord(value=name)

        routes = AddRoutes(name=name, option=option)
        routes.build()

    except typer.Exit as e:
        msg_handler.msg(e)


@app.command("new-key")
def new_key(
    size: Annotated[
        int, typer.Argument(help="The number of bytes of randomness", min=32)
    ] = 32,
) -> None:
    """Generates a new SECRET_KEY given a <SIZE>."""
    key = secrets.token_urlsafe(size)
    print(key)


@app.command("build")
def build(
    type: Annotated[
        DeploymentType,
        typer.Argument(help="The type of deployment to generate", show_choices=True),
    ] = DeploymentType.RAILWAY,
) -> None:
    """Creates a <TYPE> of production ready build for your project."""
    try:
        build = Build(type)
        build.create()

    except typer.Exit as e:
        msg_handler.msg(e)


if __name__ == "__main__":
    app()
