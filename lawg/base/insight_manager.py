import typing as t
from abc import ABC, abstractmethod
from lawg.typings import C, I


class BaseInsightManager(ABC, t.Generic[C, I]):
    """
    A manager for a insight.
    """

    __slots__ = ("client", "project_namespace", "title")

    def __init__(self, client: C, project_namespace: str) -> None:
        super().__init__()
        self.client = client
        self.project_namespace = project_namespace

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title={self.title!r} project_namespace={self.project_namespace!r}>"

    @abstractmethod
    def create(
        self,
        title: str,
        description: str | None,
        emoji: str | None,
        value: float | None,
    ) -> I:
        """
        Create a insight.
        """

    @abstractmethod
    def increment(self, id: str, value: float) -> I:
        """
        Increment the insight.
        """

    @abstractmethod
    def set(self, id: str, value: float) -> I:
        """
        Set the insight.
        """

    @abstractmethod
    def get(self, id: str) -> I:
        """
        Get the insight.
        """
