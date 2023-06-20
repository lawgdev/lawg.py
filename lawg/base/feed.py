from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, LM

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseFeed(ABC, t.Generic[C, LM]):
    """
    A feed.
    """

    __slots__ = ("client", "project_namespace", "id", "project_id", "name", "description", "emoji" "is_deleted")

    def __init__(
        self,
        client: C,
        project_namespace: str,
        id: str,
        project_id: str,
        name: str,
        description: str | None,
        emoji: str | None,
    ) -> None:
        super().__init__()
        self.client = client
        # --- super attributes --- #
        self.project_namespace = project_namespace
        # --- attributes --- #
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.emoji = emoji
        # --- extras --- #
        self.is_deleted = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} project_namespace={self.project_namespace!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def log(self, id: str | None = None) -> LM:
        """
        Get a log.

        Args:
            id (str | None, optional): id of log. Defaults to None.

        Returns:
            log.
        """

    # --- FEED --- #

    @abstractmethod
    def edit(
        self,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> None:
        """
        Edit the feed.

        Args:
            name (str | None | Undefined, optional): name of feed. Defaults to keeping the previous value.
            description (str | None | Undefined, optional): description of feed. Defaults to keeping the previous value.
            emoji (str | None | Undefined, optional): emoji of feed. Defaults to keeping the previous value.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the feed.
        """
