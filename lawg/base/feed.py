from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, L

if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class BaseFeed(ABC, t.Generic[C, L]):
    """
    A manager for a feed.
    """

    def __init__(self, client: C, project_namespace: str, name: str) -> None:
        super().__init__()
        self.client = client
        self.project_namespace = project_namespace
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} project_namespace={self.project_namespace!r}>"

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        log_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            log_id (str): id of log.
            title (str | None, optional): new title of log. Defaults to keeping the existing value.
            description (str | None, optional): new description of log. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of log. Defaults to keeping the existing value.
            color (str | None, optional): new color of log. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_log(
        self,
        log_id: str,
    ) -> L:
        """
        Delete a log.

        Args:
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
