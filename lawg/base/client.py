from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod


from lawg.typings import F, E, I, R, STR_DICT, UNDEFINED, Undefined


class BaseClient(ABC, t.Generic[F, E, I, R]):
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
    def feed(self, *, name: str) -> F:
        """
        Get a feed.

        Args:
            name (str): The name of the feed.
        Returns:
            The feed.
        """

    # --- EVENTS --- #

    @abstractmethod
    def event(self, *, feed: str, title: str, description: str) -> E:
        """
        Create an event.

        Args:
            feed (str): The name of the feed.
            title (str): The title of the event.
            description (str): The description of the event.
        """

    @abstractmethod
    def edit_event(
        self,
        *,
        feed: str,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> E:
        """
        Edit an event.

        Args:
            feed (str): The name of the feed.
            id (str): The id of the event.
            title (str, optional): The new title of the event.
            description (str, optional): The new description of the event.
            emoji (str, optional): The new emoji of the event.
        """

    @abstractmethod
    def fetch_event(self, *, feed: str, id: str) -> E:
        """
        Fetch an event.

        Args:
            feed (str): The name of the feed.
            id (str): The id of the event.
        """

    @abstractmethod
    def fetch_events(self, *, feed: str) -> list[E]:
        """
        Fetch all events.

        Args:
            feed (str): The name of the feed.
        """

    @abstractmethod
    def delete_event(self, *, feed: str, id: str) -> None:
        """
        Delete an event.

        Args:
            feed (str): The name of the feed.
            id (str): The id of the event.
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
    def _construct_event(self, feed: str, event_data: STR_DICT) -> E:
        """
        Construct an event from API response data.
        """

    def _construct_events(self, feed: str, events_data: list[STR_DICT]) -> list[E]:
        return [self._construct_event(feed, event_data) for event_data in events_data]

    @abstractmethod
    def _construct_insight(self, insight_data: STR_DICT) -> I:
        """
        Construct an insight from API response data.
        """

    def _construct_insights(self, insights_data: list[STR_DICT]) -> list[I]:
        return [self._construct_insight(insight_data) for insight_data in insights_data]
