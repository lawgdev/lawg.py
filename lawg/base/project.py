from __future__ import annotations
from datetime import datetime

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import C, F, L, M


class BaseProject(ABC, t.Generic[C, F, L, M]):
    """
    A project.
    """

    __slots__ = ("client", "namespace", "is_deleted")

    def __init__(
        self,
        client: C,
        id: str,
        namespace: str,
        name: str,
        flags: int,
        icon: str | None,
        # created_at: datetime,
        feeds: list[F],
        members: list[M],
    ) -> None:
        super().__init__()
        self.client = client
        # --- attributes --- #
        self.id = id
        self.namespace = namespace
        self.name = name
        self.flags = flags
        self.icon = icon
        # self.created_at = created_at
        self.feeds = feeds
        self.members = members
        # --- extras --- #
        self.is_deleted = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} namespace={self.namespace!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def feed(self, feed_name: str) -> F:
        """
        Get a feed.

        Args:
            feed_name (str): name of feed.
        """

    @abstractmethod
    def log(self, log_id: str) -> L:
        """
        Get a log.

        Args:
            log_id (str): id of log.
        Returns:
            the log.
        """

    # --- PROJECT METHODS --- #

    @abstractmethod
    def edit(
        self,
        name: str,
    ) -> None:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete a project.
        """
