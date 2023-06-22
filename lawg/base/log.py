from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseLog(ABC, t.Generic[C]):
    """
    A log.
    """

    __slots__ = ("client", "project_namespace", "feed_name", "id", "project_id", "feed_id", "title", "description", "emoji", "is_deleted")

    def __init__(
        self,
        client: C,
        project_namespace: str,
        feed_name: str,
        id: str,
        project_id: str,
        feed_id: str,
        title: str,
        description: str | None,
        emoji: str | None,
    ) -> None:
        super().__init__()
        self.client = client
        # --- super attributes --- #
        self.project_namespace = project_namespace
        self.feed_name = feed_name
        # --- attributes --- #
        self.id = id
        self.project_id = project_id
        self.feed_id = feed_id
        self.title = title
        self.description = description
        self.emoji = emoji
        # --- extras --- #
        self.is_deleted = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} title={self.title!r} emoji={self.emoji!r} feed_name={self.feed_name!r} project_namespace={self.project_namespace!r}>"

    # --- LOG --- #

    @abstractmethod
    def edit(
        self,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> None:
        """
        Edit the log.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the log.
        """
