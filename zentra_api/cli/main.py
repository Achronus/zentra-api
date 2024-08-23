import secrets
from typing import Annotated
import typer

from zentra_api.auth.enums import DeploymentType

from zentra_api.cli.commands.build import Build
from zentra_api.cli.commands.setup import Setup

from zentra_api.cli.constants import console
from zentra_api.cli.constants.enums import AddItem, DefaultFolderOptions
from zentra_api.cli.constants.message import MSG_MAPPER, MessageHandler


init_command = typer.style("init", typer.colors.YELLOW)
add_command = typer.style("add", typer.colors.YELLOW)

app = typer.Typer(
    help=f"Welcome to Zentra API! Create a project with {init_command} or add something with {add_command}.",
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


@app.command("add")
def add(
    item: Annotated[
        AddItem,
        typer.Argument(
            help="The type of item to add.",
            show_default=False,
        ),
    ],
    folder: Annotated[
        str,
        typer.Option(
            help="The folder to add the item to. E.g., 'auth'. When <item='route'>, defaults to 'api'. When <item='test'> defaults to 'tests'.",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Adds a new <ITEM> into the project in <FOLDER> with <NAME>."""
    try:
        if not folder:
            folder = getattr(DefaultFolderOptions, item.upper())

        print(folder)

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
