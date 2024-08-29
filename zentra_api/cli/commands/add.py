import inflect
from pydantic import BaseModel

from zentra_api.cli.constants.enums import RouteOptions


class Name(BaseModel):
    """A storage container for the name of the route."""

    singular: str
    plural: str


class AddRoutes:
    """Performs project operations for the `add-route` command."""

    def __init__(self, name: str, option: RouteOptions) -> None:
        self.p = inflect.engine()

        self.name = self._store_name(name.lower().strip())
        self.type = option

    def _store_name(self, name: str) -> Name:
        """Stores the name in a model with `singular` and `plural` variants."""
        singular = self.p.singular_noun(name)

        if singular:
            single = singular
            plural = name
        else:
            single = name
            plural = self.p.plural_noun(name)

        return Name(
            singular=single,
            plural=plural,
        )

    def build(self) -> None:
        pass
