from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, E

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseFeed(ABC, t.Generic[C, E]):
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
    def event(self, *, title: str, description: str) -> E:
        """
        Create an event.

        Args:
            title (str): The title of the event.
            description (str): The description of the event.
        Returns:
            The event.
        """

    @abstractmethod
    def edit_event(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> E:
        """
        Edit an event.

        Args:
            id (str): The id of the event.
            title (str, optional): The new title of the event.
            description (str, optional): The new description of the event.
            emoji (str, optional): The new emoji of the event.
        Returns:
            The event.
        """

    @abstractmethod
    def fetch_event(self, *, id: str) -> E:
        """
        Fetch an event.

        Args:
            id (str): The id of the event.
        Returns:
            The event.
        """

    @abstractmethod
    def fetch_events(self) -> list[E]:
        """
        Fetch all events.

        Returns:
            A list of events.
        """

    @abstractmethod
    def delete_event(self, *, id: str) -> None:
        """
        Delete an event.

        Args:
            id (str): The id of the event.
        Returns:
            None
        """
