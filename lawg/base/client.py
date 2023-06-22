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
