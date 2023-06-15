from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED, C, R, L

if t.TYPE_CHECKING:
    from lawg.base.log import BaseLog
    from lawg.base.client import BaseClient
    from lawg.base.room import BaseRoom
    from lawg.typings import Undefined


class BaseProject(ABC, t.Generic[C, R, L]):
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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} namespace={self.namespace!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def room(self, room_name: str) -> R:
        """
        Get a room.

        Args:
            room_name (str): name of room.
        """

    # --- ROOMS --- #

    @abstractmethod
    def create_room(
        self,
        room_name: str,
        description: str | None = None,
    ) -> R:
        """
        Create a room.

        Args:
            room_name (str): name of the room.
            description (str | None, optional): description of room. Defaults to None.
        """

    @abstractmethod
    def edit_room(
        self,
        room_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> R:
        """
        Edit a room.

        Args:
            room_name (str): name of room
            name (str | None, optional): new name of room. Defaults to keeping the existing value.
            description (str | None, optional): new description of room. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of room. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_room(
        self,
        room_name: str,
    ) -> None:
        """
        Delete a room.

        Args:
            room_name (str): name of room.
        """

    patch_room = edit_room

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        room_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            room_name (str): name of room.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        room_name: str,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            room_name (str): name of room.
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        room_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            room_name (str): name of room.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        room_name: str,
        log_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            room_name (str): name of room.
            log_id (str): id of log.
            title (str | None, optional): new title of log. Defaults to keeping the existing value.
            description (str | None, optional): new description of log. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of log. Defaults to keeping the existing value.
            color (str | None, optional): new color of log. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_log(
        self,
        room_name: str,
        log_id: str,
    ) -> L:
        """
        Delete a log.

        Args:
            room_name (str): name of room.
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
