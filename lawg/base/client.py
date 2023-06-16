from __future__ import annotations

import typing as t

from abc import ABC, abstractmethod

from lawg.schemas import (
    APISuccessSchema,
    FeedSlugSchema,
    FeedWithNameSlugSchema,
    LogCreateBodySchema,
    LogGetMultipleBodySchema,
    LogPatchBodySchema,
    LogSchema,
    LogSlugSchema,
    LogWithIdSlugSchema,
    ProjectBodySchema,
    ProjectSchema,
    FeedCreateBodySchema,
    FeedPatchBodySchema,
    FeedSchema,
    ProjectSlugSchema,
)

from lawg.typings import UNDEFINED, P, F, L, R

if t.TYPE_CHECKING:
    from lawg.base.rest import BaseRest
    from lawg.typings import Undefined
    from marshmallow import Schema


class BaseClient(ABC, t.Generic[P, F, L, R]):
    """
    The base client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.rest: R

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
    def feed(self, project_namespace: str, feed_name: str) -> F:
        """
        Get a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
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

    # --- FEEDS --- #

    @abstractmethod
    def create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
    ) -> F:
        """
        Create a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of the feed.
            description (str | None, optional): description of feed. Defaults to None.
        """

    @abstractmethod
    def edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> F:
        """
        Edit a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed
            name (str | None, optional): new name of feed. Defaults to keeping the existing value.
            description (str | None, optional): new description of feed. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of feed. Defaults to keeping the existing value.
        """

    @abstractmethod
    def delete_feed(
        self,
        project_namespace: str,
        feed_name: str,
    ) -> None:
        """
        Delete a feed.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
        """

    patch_feed = edit_feed

    # --- LOGS --- #

    @abstractmethod
    def create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> L:
        """
        Create a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            title (str): title of log.
            description (str | None, optional): description of log. Defaults to None.
            emoji (str | None, optional): emoji of log. Defaults to None.
            color (str | None, optional): color of log. Defaults to None.
        """

    @abstractmethod
    def fetch_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
    ) -> L:
        """
        Fetch a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    @abstractmethod
    def fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[L]:
        """
        Fetch multiple logs.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            limit (int | None, optional): limit of logs. Defaults to None.
            offset (int | None, optional): offset of logs. Defaults to None.
        """

    @abstractmethod
    def edit_log(
        self,
        project_namespace: str,
        feed_name: str,
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
            feed_name (str): name of feed.
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
        feed_name: str,
        log_id: str,
    ) -> None:
        """
        Delete a log.

        Args:
            project_namespace (str): namespace of project.
            feed_name (str): name of feed.
            log_id (str): id of log.
        """

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log

    # --- MANAGER CONSTRUCTORS --- #

    # @abstractmethod
    # def construct_project(self, project_data: STR_DICT) -> P:
    #     """
    #     Construct a project from API response data.
    #     """

    # @abstractmethod
    # def construct_feed(self, feed_data: STR_DICT) -> F:
    #     """
    #     Construct a feed from API response data.
    #     """

    # @abstractmethod
    # def construct_log(self, log_data: STR_DICT) -> L:
    #     """
    #     Construct a log from API response data.
    #     """
