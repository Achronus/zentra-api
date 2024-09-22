from pydantic import BaseModel

from zentra_api.cli.constants import Import


class APIRouteDetails(BaseModel):
    """A model for API routes."""

    name: str
    path: str
    method: str


class Config(BaseModel):
    """A model for the Zentra config."""

    project_name: str
    # api_routes: dict[str, APIRouteDetails] | None = None


class Imports(BaseModel):
    """A model for a list of imports."""

    items: list[list[Import]]

    def to_str(self) -> str:
        """Converts the imports to a string."""
        imports = []

        for item in self.items:
            block = []
            for import_item in item:
                block.append(import_item.to_str())

            block.append("")
            imports.append("\n".join(block))

        return "\n".join(imports)
