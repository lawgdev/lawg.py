from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, F, L

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseProject(ABC, t.Generic[C, F, L]):
    """
    A manager for a project.
    """

    def __init__(
        self,
        client: C,
        namespace: str,
    ) -> None:
        super().__init__()
        self.client = client
        self.namespace = namespace
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

    # --- PROJECT --- #

    @abstractmethod
    def edit(
        self,
        name: str,
        namespace: str,
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

    # --- FEEDS --- #

    @abstractmethod
    def create_feed(
        self,
        feed_name: str,
        description: str | None = None,
    ) -> F:
        """
        Create a feed.

        Args:
            feed_name (str): name of the feed.
            description (str | None, optional): description of feed. Defaults to None.
        """

    @abstractmethod
    def edit_feed(
        self,
        feed_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> F:
        """
        Edit a feed.

        Args:
            feed_name (str): name of feed
            name (str | None, optional): new name of feed. Defaults to keeping the existing value.
            description (str | None, optional): new description of feed. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of feed. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_feed(
        self,
        feed_name: str,
    ) -> None:
        """
        Delete a feed.

        Args:
            feed_name (str): name of feed.
        """

    patch_feed = edit_feed

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            feed_name (str): name of feed.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        feed_name: str,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            feed_name (str): name of feed.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        feed_name: str,
        log_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            feed_name (str): name of feed.
            log_id (str): id of log.
            title (str | None, optional): new title of log. Defaults to keeping the existing value.
            description (str | None, optional): new description of log. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of log. Defaults to keeping the existing value.
            color (str | None, optional): new color of log. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_log(
        self,
        feed_name: str,
        log_id: str,
    ) -> L:
        """
        Delete a log.

        Args:
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
