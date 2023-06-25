from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod


from lawg.typings import F, L, I, R, STR_DICT, UNDEFINED, Undefined


class BaseClient(ABC, t.Generic[F, L, I, R]):
    """
    The base client for lawg.
    """

    __slots__ = ("token", "project", "rest")

    def __init__(self, token: str, project: str) -> None:
        super().__init__()
        self.token: str = token
        self.project: str = project
        self.rest: R

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r} project={self.project!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def feed(self, * name: str) -> F:
        """
        Get a feed.

        Args:
            name (str): The name of the feed.
        Returns:
            The feed.
        """

    # --- LOGS --- #

    @abstractmethod
    def log(self, *, feed_name: str, title: str, description: str) -> L:
        """
        Create a log.

        Args:
            feed_name (str): The name of the feed.
            title (str): The title of the log.
            description (str): The description of the log.
        """

    @abstractmethod
    def edit_log(
        self,
        *,
        feed_name: str,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> L:
        """
        Edit a log.

        Args:
            feed_name (str): The name of the feed.
            id (str): The id of the log.
            title (str, optional): The new title of the log.
            description (str, optional): The new description of the log.
            emoji (str, optional): The new emoji of the log.
        """

    @abstractmethod
    def fetch_log(self, *, feed_name: str, id: str) -> L:
        """
        Fetch a log.

        Args:
            feed_name (str): The name of the feed.
            id (str): The id of the log.
        """

    @abstractmethod
    def fetch_logs(self, *, feed_name: str) -> list[L]:
        """
        Fetch all logs.

        Args:
            feed_name (str): The name of the feed.
        """

    @abstractmethod
    def delete_log(self, *, feed_name: str, id: str) -> None:
        """
        Delete a log.

        Args:
            feed_name (str): The name of the feed.
            id (str): The id of the log.
        """

    # --- INSIGHTS --- #

    @abstractmethod
    def insight(self, *, title: str, description: str, value: int, emoji: str | None = None) -> I:
        """
        Create an insight.

        Args:
            title (str): The title of the insight.
            description (str): The description of the insight.
            value (int): The value of the insight.
            emoji (str, optional): The emoji of the insight.
        """

    @abstractmethod
    def edit_insight(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> I:
        """
        Edit an insight.

        Args:
            id (str): The id of the insight.
            title (str, optional): The new title of the insight.
            description (str, optional): The new description of the insight.
            emoji (str, optional): The new emoji of the insight.
        """

    @abstractmethod
    def increment_insight(self, *, id: str, value: float) -> I:
        """
        Increment the value of an insight.

        Args:
            id (str): The id of the insight.
            value (int): The value to increment the insight by.
        """

    @abstractmethod
    def set_insight(
        self,
        *,
        id: str,
        value: float,
    ) -> I:
        """
        Set the value of an insight.

        Args:
            id (str): The id of the insight.
            value (int): The value to set the insight to.
        """

    @abstractmethod
    def fetch_insight(self, *, id: str) -> I:
        """
        Fetch an insight.

        Args:
            id (str): The id of the insight.
        """

    @abstractmethod
    def fetch_insights(self) -> list[I]:
        """
        Fetch all insights.
        """

    @abstractmethod
    def delete_insight(self, *, id: str) -> None:
        """
        Delete an insight.

        Args:
            id (str): The id of the insight.
        """

    # --- MANAGER CONSTRUCTORS --- #

    @abstractmethod
    def _construct_log(self, project_namespace: str, feed_name: str, log_data: STR_DICT) -> L:
        """
        Construct a log from API response data.
        """

    def _construct_logs(self, project_namespace: str, feed_name: str, logs_data: list[STR_DICT]) -> list[L]:
        return [self._construct_log(project_namespace, feed_name, log_data) for log_data in logs_data]

    @abstractmethod
    def _construct_insight(self, project_namespace: str, insight_data: STR_DICT) -> I:
        """
        Construct an insight from API response data.
        """

    def _construct_insights(self, project_namespace: str, insights_data: list[STR_DICT]) -> list[I]:
        return [self._construct_insight(project_namespace, insight_data) for insight_data in insights_data]
