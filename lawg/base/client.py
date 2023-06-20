from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod


from lawg.typings import PM, P, F, L, I, R, STR_DICT, UNDEFINED, Undefined


class BaseClient(ABC, t.Generic[PM, P, F, L, I, R]):
    """
    The base client for lawg.
    """

    __slots__ = ("token", "rest")

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: R

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} token={self.token!r}>"

    # --- MANAGERS --- #

    @abstractmethod
    def project(self, project_namespace: str) -> PM:
        """
        Get a project manager.

        Args:
            project_namespace (str): namespace of project.
        Returns:
            the project manager.
        """

    # --- API INTERACTIONS METHODS --- #

    # --- PROJECTS --- #

    @abstractmethod
    def _create_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> STR_DICT:
        """
        Create a project.

        Args:
            name (str): name of project.
            namespace (str): namespace of project.
        Returns:
            the created project data.
        """

    @abstractmethod
    def _fetch_project(
        self,
        project_namespace: str,
    ) -> STR_DICT:
        """
        Fetch a project.

        Args:
            namespace (str): namespace of log.
        Returns:
            the fetched project data.
        """

    @abstractmethod
    def _edit_project(
        self,
        project_name: str,
        project_namespace: str,
    ) -> STR_DICT:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            namespace (str): namespace of project.
        Returns:
            the edited project data.
        """

    @abstractmethod
    def _delete_project(
        self,
        project_namespace: str,
    ) -> STR_DICT:
        """
        Delete a project.

        Args:
            namespace (str): namespace of project.
        Returns:
            the deleted project data.
        """

    # --- FEEDS --- #

    @abstractmethod
    def _create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
    ) -> STR_DICT:
        """
        Create a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of the feed.
            description (str | None, optional): description of feed. Defaults to None.
        Returns:
            the created feed data.
        """

    @abstractmethod
    def _edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed
            name (str | None, optional): new name of feed. Defaults to keeping the existing value.
            description (str | None, optional): new description of feed. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of feed. Defaults to keeping the existing value.
        Returns:
            the edited feed data.
        """

    @abstractmethod
    def _delete_feed(
        self,
        project_namespace: str,
        feed_name: str,
    ) -> None:
        """
        Delete a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed .
        Returns:
            None
        """

    # --- LOGS --- #

    @abstractmethod
    def _create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> STR_DICT:
        """
        Create a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        Returns:
            the created log data.
        """

    @abstractmethod
    def _fetch_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
    ) -> STR_DICT:
        """
        Fetch a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        Returns:
            the fetched log data.
        """

    @abstractmethod
    def _fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[STR_DICT]:
        """
        Fetch multiple logs.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        Returns:
            the fetched logs' data.
        """

    @abstractmethod
    def _edit_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        color: str | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
            title (str | None, optional): new title of log. Defaults to keeping the existing value.
            description (str | None, optional): new description of log. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of log. Defaults to keeping the existing value.
            color (str | None, optional): new color of log. Defaults to keeping the existing value.
        Returns:
            the edited log data.
        """

    @abstractmethod
    def _delete_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
    ) -> None:
        """
        Delete a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        Returns:
            None
        """

    # --- INSIGHT --- #

    @abstractmethod
    def _create_insight(
        self,
        project_namespace: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        value: float | None = None,
    ) -> STR_DICT:
        """
        Create an insight.

        Args:
            project_namespace (str): namespace of project.
            title (str): title of insight.
            description (str | None, optional): description of insight. Defaults to None.
            emoji (str | None, optional): emoji of insight. Defaults to None.
            value (float | None, optional): value of insight. Defaults to None.
        Returns:
            the created insight data.
        """

    @abstractmethod
    def _fetch_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ) -> STR_DICT:
        """
        Fetch an insight.

        Args:
            project_namespace (str): namespace of project.
            insight_id (str): id of insight.
        Returns:
            the fetched insight data.
        """

    @abstractmethod
    def _edit_insight(
        self,
        project_namespace: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: float | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit an insight.

        Args:
            project_namespace (str): namespace of project.
            insight_id (str): id of insight.
            title (str | None, optional): new title of insight. Defaults to keeping the existing value.
            description (str | None, optional): new description of insight. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of insight. Defaults to keeping the existing value.
            value (float | None, optional): new value of insight. Defaults to keeping the existing value.
        Returns:
            the edited insight data.
        """

    @abstractmethod
    def _delete_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ) -> None:
        """
        Delete an insight.

        Args:
            project_namespace (str): namespace of project.
            insight_id (str): id of insight.
        Returns:
            None
        """

    # --- MANAGER CONSTRUCTORS --- #

    @abstractmethod
    def _construct_project(self, project_data: STR_DICT) -> P:
        """
        Construct a project from API response data.
        """

    @abstractmethod
    def _construct_feed(self, project_namespace: str, feed_data: STR_DICT) -> F:
        """
        Construct a feed from API response data.
        """

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
