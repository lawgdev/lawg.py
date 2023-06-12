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

    @abstractmethod
    def create(
        self,
        name: str,
        namespace: str,
    ) -> BaseLog:
        """
        Create a log.

        Args:
            name (str): name of log.
            namespace (str): namespace of log.
        """

    @abstractmethod
    def edit(
        self,
        name: str,
        namespace: str,
    ) -> BaseLog:
        """
        Edit a log.

        Args:
            name (str): name of log, what is being changed.
            namespace (str): namespace of log.
        """

    @abstractmethod
    def delete(
        self,
        namespace: str,
    ) -> BaseLog:
        """
        Delete a log.

        Args:
            namespace (str): id of event.
        """

    @abstractmethod
    def fetch(
        self,
        namespace: str,
    ) -> BaseLog:
        """
        Fetch a log.

        Args:
            namespace (str): namespace of log.
        """

    patch = edit
    get = fetch

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
