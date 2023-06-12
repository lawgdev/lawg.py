import typing as t

from abc import ABC, abstractmethod

from lawg.typings import UNDEFINED

if t.TYPE_CHECKING:
    from lawg.base.log import BaseLog
    from lawg.base.rest import BaseRest
    from lawg.base.project import BaseProject
    from lawg.base.room import BaseRoom
    from lawg.typings import Undefined


class BaseClient(ABC):
    """
    A client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: BaseRest

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def project(self, project_namespace: str) -> BaseProject:
        """
        Get a project.

        Args:
            project_namespace (str): namespace of project.
        """

    @abstractmethod
    def room(self, project_namespace: str, room_name: str) -> BaseRoom:
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
    ) -> BaseProject:
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
    ) -> BaseProject:
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
    ) -> BaseProject:
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
    ) -> BaseProject:
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
    ) -> BaseRoom:
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
    ) -> BaseRoom:
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
    ) -> BaseRoom:
        """
        Delete a room.

        Args:
            project_namespace (str): namespace of project.
            room_name (str): name of room.
        """

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
    ) -> BaseLog:
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
    ) -> BaseLog:
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
    ) -> list[BaseLog]:
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
    ) -> BaseLog:
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
    ) -> BaseLog:
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
