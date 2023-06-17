from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, F, LM

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseFeedManager(ABC, t.Generic[C, F, LM]):
    """
    A manager of a feed.
    """

    __slots__ = ("client", "project_namespace", "name")

    def __init__(
        self,
        client: C,
        project_namespace: str,
        feed_name: str,
    ) -> None:
        super().__init__()
        self.client = client
        # --- super attributes --- #
        self.project_namespace = project_namespace
        # --- attributes --- #
        self.name = feed_name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} project_namespace={self.project_namespace!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def log(self, log_id: str) -> LM:
        """
        Get a log manager.

        Args:
            feed_name (str): name of feed manager.
            log_id (str): id of log manager.
        Returns:
            the log manager.
        """

    # --- FEED METHODS --- #

    @abstractmethod
    def create(
        self,
        description: str | None = None,
        emoji: str | None = None,
    ) -> F:
        """
        Create a feed.

        Args:
            name (str): name of feed.
            description (str | None, optional): description of feed. Defaults to None.
            emoji (str | None, optional): emoji of feed. Defaults to None.

        Returns:
            L: feed
        """

    # TODO: implement

    # @abstractmethod
    # def get(self) -> F:
    #     """
    #     Get a feed.

    #     Returns:
    #         feed
    #     """

    @abstractmethod
    def edit(
        self,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> F:
        """
        Edit a feed.

        Args:
            name (str | None | Undefined, optional): name of feed. Defaults to keeping the previous value.
            description (str | None | Undefined, optional): description of feed. Defaults to keeping the previous value.
            emoji (str | None | Undefined, optional): emoji of feed. Defaults to keeping the previous value.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete a feed.

        Returns:
            None
        """
