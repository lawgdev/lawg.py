from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, L

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseFeed(ABC, t.Generic[C, L]):
    """
    A feed.
    """

    __slots__ = ("client", "name")

    def __init__(
        self,
        client: C,
        name: str,
    ) -> None:
        super().__init__()
        self.client = client
        # --- attributes --- #
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} project={self.client.project!r}>"

    # --- FEED METHODS --- #

    @abstractmethod
    def log(self, *, title: str, description: str) -> L:
        """
        Create a log.

        Args:
            title (str): The title of the log.
            description (str): The description of the log.
        Returns:
            The log.
        """

    @abstractmethod
    def edit_log(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            id (str): The id of the log.
            title (str, optional): The new title of the log.
            description (str, optional): The new description of the log.
            emoji (str, optional): The new emoji of the log.
        Returns:
            The log.
        """

    @abstractmethod
    def fetch_log(self, *, id: str) -> L:
        """
        Fetch a log.

        Args:
            id (str): The id of the log.
        Returns:
            The log.
        """

    @abstractmethod
    def fetch_logs(self) -> list[L]:
        """
        Fetch all logs.

        Returns:
            A list of logs.
        """

    @abstractmethod
    def delete_log(self, *, id: str) -> None:
        """
        Delete a log.

        Args:
            id (str): The id of the log.
        Returns:
            None
        """
