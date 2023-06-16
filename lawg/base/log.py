from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseLog(ABC, t.Generic[C]):
    """
    A manager for a log.
    """

    def __init__(self, client: C, project_namespace: str, feed_name: str, id: str) -> None:
        super().__init__()
        self.client = client
        self.project_namespace = project_namespace
        self.feed_name = feed_name
        self.id = id
        # --- extras --- #
        self.is_deleted = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} feed_name={self.feed_name!r} project_namespace={self.project_namespace!r}>"

    @abstractmethod
    def edit(
        self,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> None:
        """
        Edit the log.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the log.
        """
