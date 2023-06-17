from abc import ABC, abstractmethod
import typing as t

from lawg.typings import C, P, FM


class BaseProjectManager(ABC, t.Generic[C, P, FM]):
    """
    A manager of a project.
    """

    __slots__ = ("client", "namespace")

    def __init__(
        self,
        client: C,
        namespace: str,
    ) -> None:
        super().__init__()
        self.client = client
        # --- attributes --- #
        self.namespace = namespace

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} namespace={self.namespace!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def feed(self, feed_name: str) -> FM:
        """
        Get a feed manager.

        Args:
            feed_name (str): name of feed manager.
        Returns:
            the feed manager.
        """

    # --- PROJECT METHODS --- #

    @abstractmethod
    def create(self, name: str | None) -> P:
        """
        Create a project.

        Args:
            name (str): Name of project. Defaults to being the same as the namespace.
        Returns:
            the project.
        """

    @abstractmethod
    def get(self) -> P:
        """
        Get a project.

        Returns:
            the project.
        """

    @abstractmethod
    def edit(self, name: str) -> P:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
        Returns:
            the project.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete a project.

        Returns:
            None.
        """
