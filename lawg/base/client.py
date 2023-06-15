from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod
from lawg.schemas import (
    APISuccessSchema,
    ProjectBodySchema,
    ProjectGetSchema,
    ProjectSchema,
    RoomCreateBodySchema,
    RoomDeleteSchema,
    RoomPatchBodySchema,
    RoomSchema,
)

from lawg.typings import STR_DICT, UNDEFINED, P, R, L

if t.TYPE_CHECKING:
    from lawg.base.rest import BaseRest
    from lawg.typings import Undefined


class BaseClient(ABC, t.Generic[P, R, L]):
    """
    The base client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: BaseRest

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def project(self, project_namespace: str) -> P:
        """
        Get a project.

        Args:
            project_namespace (str): namespace of project.
        """

    @abstractmethod
    def room(self, project_namespace: str, room_name: str) -> R:
        """
        Get a room.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
        """

    # --- PROJECTS --- #

    @abstractmethod
    def create_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> P:
        """
        Create a project.

        Args:
            name (str): name of project.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def fetch_project(
        self,
        project_namespace: str,
    ) -> P:
        """
        Fetch a project.

        Args:
            namespace (str): namespace of log.
        """

    @abstractmethod
    def edit_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> P:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def delete_project(
        self,
        project_namespace: str,
    ) -> P:
        """
        Delete a project.

        Args:
            namespace (str): namespace of project.
        """

    patch_project = edit_project
    get_project = fetch_project

    # --- ROOMS --- #

    @abstractmethod
    def create_room(
        self,
        project_namespace: str,
        room_name: str,
        description: str | None = None,
    ) -> R:
        """
        Create a room.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of the room.
            description (str | None, optional): description of room. Defaults to None.
        """

    @abstractmethod
    def edit_room(
        self,
        project_namespace: str,
        room_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> R:
        """
        Edit a room.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room
            name (str | None, optional): new name of room. Defaults to keeping the existing value.
            description (str | None, optional): new description of room. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of room. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_room(
        self,
        project_namespace: str,
        room_name: str,
    ) -> R:
        """
        Delete a room.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
        """

    patch_room = edit_room

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        project_namespace: str,
        room_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        project_namespace: str,
        room_name: str,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        project_namespace: str,
        room_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        project_namespace: str,
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
            project_namespace (str): namespace of project.
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
        project_namespace: str,
        room_name: str,
        log_id: str,
    ) -> L:
        """
        Delete a log.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log

    # --- ROOMS --- #

    def _validate_project_response(self, response_data: STR_DICT) -> STR_DICT:
        resp_schema = APISuccessSchema()
        resp_data: STR_DICT = resp_schema.load(response_data)  # type: ignore

        project_schema = ProjectSchema()
        project_data: STR_DICT = project_schema.load(resp_data["data"])  # type: ignore

        return project_data

    def _validate_create_request(self, project_namespace: str, project_name: str) -> STR_DICT:
        req_schema = ProjectBodySchema()
        req_data: STR_DICT = req_schema.load({"name": project_name, "namespace": project_namespace})  # type: ignore
        return req_data

    def _validate_fetch_request(self, project_namespace: str) -> None:
        req_schema = ProjectGetSchema()
        req_schema.load({"namespace": project_namespace})

    _validate_edit_request = _validate_create_request
    _validate_delete_request = _validate_fetch_request

    def _validate_room_response(self, response_data: STR_DICT) -> STR_DICT:
        resp_schema = APISuccessSchema()
        resp_data: STR_DICT = resp_schema.load(response_data)  # type: ignore

        room_schema = RoomSchema()
        room_data: STR_DICT = room_schema.load(resp_data["data"])  # type: ignore
        return room_data

    def _validate_room_create_request(
        self, project_namespace: str, room_name: str, description: str | None = None, emoji: str | None = None
    ) -> None:
        req_schema = RoomCreateBodySchema()
        req_schema.load(
            {
                "namespace": project_namespace,
                "name": room_name,
                "description": description,
                "emoji": emoji,
            }
        )
        return None

    def _validate_room_edit_request(
        self,
        project_namespace: str,
        room_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> None:
        req_schema = RoomPatchBodySchema()
        req_schema.load(
            {
                "namespace": project_namespace,
                "name": room_name,
                "new_name": name,
                "description": description,
                "emoji": emoji,
            }
        )

    def _validate_room_delete_request(self, project_namespace: str, room_name: str) -> None:
        req_schema = RoomDeleteSchema()
        req_schema.load({"namespace": project_namespace, "name": room_name})
