from abc import ABC, abstractmethod
from datetime import datetime
import typing as t

from lawg.typings import C


class BaseInsight(ABC, t.Generic[C]):
    """
    An event.
    """

    __slots__ = (
        "client",
        "id",
        "title",
        "description",
        "value",
        "emoji",
        "updated_at",
        "created_at",
        "is_deleted",
    )

    def __init__(
        self,
        client: C,
        id: str,
        title: str,
        description: str | None,
        value: float | None,
        emoji: str | None,
        updated_at: datetime,
        created_at: datetime,
    ) -> None:
        super().__init__()
        self.client = client
        # --- attributes --- #
        self.id = id
        self.title = title
        self.description = description
        self.value = value
        self.emoji = emoji
        self.updated_at = updated_at
        self.created_at = created_at
        # --- extras --- #
        self.is_deleted = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title={self.title!r} value={self.value!r} project={self.client.project!r}>"

    @abstractmethod
    def set(self, value: float) -> None:
        """
        Set the insight.
        """

    @abstractmethod
    def increment(self, value: float) -> None:
        """
        Increment the insight.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete the insight.
        """
