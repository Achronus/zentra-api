import textwrap

from zentra_api.cli.constants import MAGIC, ROOT_COMMAND

from rich.panel import Panel


def complete_msg(project_name: str) -> str:
    return f"""
    [cyan]Next Steps[/cyan]
        1. Access the project with [dark_goldenrod]cd {project_name}[/dark_goldenrod]
        2. Install its packages [yellow]poetry install[/yellow]

    [dark_goldenrod]Start Building![/dark_goldenrod]
        - Create some database tables 
        [yellow]{ROOT_COMMAND} add-table <>[/yellow]
        - And some routes 
        [cyan]{ROOT_COMMAND} add-route <>[/cyan]
    """


def create_panel(
    text: str,
    colour: str = "bright_green",
    padding: tuple[int, int] = (0, 4),
) -> Panel:
    """A utility function for building panels."""
    return Panel.fit(
        textwrap.dedent(text),
        border_style=colour,
        padding=padding,
    )


def success_panel(title: str, desc: str) -> Panel:
    return create_panel(f"""
    {MAGIC} [bright_green]{title}[/bright_green] {MAGIC}
    {desc}""")


def setup_complete_panel(project_name: str) -> Panel:
    """Creates a printable panel after successfully completing the `init` command."""
    return success_panel("Project created successfully!", complete_msg(project_name))


def already_configured_panel(project_name: str) -> Panel:
    """Creates a printable panel for the `init` command if the project already exists."""
    return success_panel("Project already exists!", complete_msg(project_name))
