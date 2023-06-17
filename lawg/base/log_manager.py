from abc import ABC, abstractmethod
import typing as t

from lawg.typings import Undefined, UNDEFINED, C, L


class BaseLogManager(ABC, t.Generic[C, L]):
    """
    A manager for a log.
    """

    __slots__ = ("client", "project_namespace", "feed_name", "id")

    def __init__(self, client: C, project_namespace: str, feed_name: str, id: str | None) -> None:
        super().__init__()
        self.client = client
        # --- super attributes --- #
        self.project_namespace = project_namespace
        self.feed_name = feed_name
        # --- attributes --- #
        self.id = id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} feed_name={self.feed_name!r} project_namespace={self.project_namespace!r}>"

    # --- LOG --- #

    @abstractmethod
    def create(
        self,
        title: str,
        description: str | None,
        emoji: str | None,
        color: str | None,
    ) -> L:
        """
        Get the log.
        """

    @abstractmethod
    def get(self) -> L:
        """
        Get the log.
        """

    @abstractmethod
    def edit(
        self,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit the log.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the log.
        """
