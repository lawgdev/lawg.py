import typing as t

from abc import ABC


if t.TYPE_CHECKING:
    from lawg.base.client import BaseClient


class BaseProject(ABC):
    def __init__(
        self,
        client: BaseClient,
        namespace: str,
    ) -> None:
        super().__init__()
        self.client = client
        self.namespace = namespace

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} namespace={self.namespace!r}>"

    def create(
        self,
        name: str,
    ) -> BaseProject:
        """
        Create a project.

        Args:
            name (str): name of project.
        """
