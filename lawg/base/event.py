from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseEvent(ABC, t.Generic[C]):
    """
    An event.
    """

    __slots__ = (
        "client",
        "feed",
        "id",
        "project_id",
        "feed_id",
        "title",
        "description",
        "emoji",
        "is_deleted",
    )

    def __init__(
        self,
        client: C,
        feed: str,
        id: str,
        project_id: str,
        feed_id: str,
        title: str,
        description: str | None,
        emoji: str | None,
    ) -> None:
        super().__init__()
        self.client = client
        self.feed = feed
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
        return f"<{self.__class__.__name__} id={self.id!r} title={self.title!r} emoji={self.emoji!r} feed={self.feed!r} project={self.client.project!r}>"

    # --- EVENT --- #

    @abstractmethod
    def edit(
        self,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> None:
        """
        Edit the event.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the event.
        """
