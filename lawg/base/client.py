from abc import ABC, abstractmethod


from lawg.base.log import BaseLog
from lawg.base.rest import BaseRest
from lawg.base.project import BaseProject
from lawg.base.room import BaseRoom


class BaseClient(ABC):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: BaseRest

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r}>"

    # other class handlers

    @abstractmethod
    def project(self, namespace: str) -> BaseProject:
        """
        Get a project.

        Args:
            namespace (str): namespace of project.
        """

    @abstractmethod
    def room(self, namespace: str, room_name: str) -> BaseRoom:
        """
        Get a room.

        Args:
            namespace (str): namespace of project.
            room_name (str): name of room.
        """

    # project

    @abstractmethod
    def create_project(
        self,
        name: str,
        namespace: str,
    ) -> BaseLog:
        """
        Create a project.

        Args:
            name (str): name of project.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def edit_project(
        self,
        name: str,
        namespace: str,
    ) -> BaseLog:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            namespace (str): namespace of project.
        """

    @abstractmethod
    def delete_project(
        self,
        namespace: str,
    ) -> BaseLog:
        """
        Delete a project.

        Args:
            namespace (str): namespace of project.
        """

    @abstractmethod
    def fetch_project(
        self,
        namespace: str,
    ) -> BaseLog:
        """
        Fetch a project.

        Args:
            namespace (str): namespace of log.
        """

    patch_project = edit_project
    get_project = fetch_project

    # room

    @abstractmethod
    def create_room(
        self,
        name: str,
        namespace: str,
        description: str | None = None,
    ) -> BaseLog:
        """
        Create a room.

        Args:
            name (str): name of room.
            namespace (str): namespace of project.
            description (str | None, optional): description of room. Defaults to None.
        """

    @abstractmethod
    def edit_room(
        self,
        name: str,
        namespace: str,
        description: str | None = None,
    ) -> BaseLog:
        """
        Edit a room.

        Args:
            name (str): name of room, what is being changed.
            namespace (str): namespace of project.
            description (str | None, optional): description of room. Defaults to None.
        """
