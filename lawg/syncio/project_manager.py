from __future__ import annotations

import typing as t
from lawg.base.project_manager import BaseProjectManager
from lawg.syncio.feed_manager import FeedManager
from lawg.syncio.project import Project


if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.project import Project
    from lawg.syncio.feed_manager import FeedManager


class ProjectManager(
    BaseProjectManager[
        "Client",
        "Project",
        "FeedManager",
    ]
):
    """
    A manager of a project.
    """

    # --- MANAGERS --- #

    def feed(self, feed_name: str) -> FeedManager:
        return FeedManager(
            client=self.client,
            project_namespace=self.namespace,
            feed_name=feed_name,
        )

    # --- PROJECT --- #

    def create(self, name: str | None = None):
        if name is None:
            name = self.namespace
        project_data = self.client._create_project(project_namespace=self.namespace, project_name=name)
        return self.client._construct_project(project_data)

    def get(self) -> Project:
        project_data = self.client._fetch_project(project_namespace=self.namespace)
        return self.client._construct_project(project_data)

    def edit(self, name: str):
        project_data = self.client._edit_project(project_namespace=self.namespace, project_name=name)
        return self.client._construct_project(project_data)

    def delete(self):
        self.client._delete_project(project_namespace=self.namespace)
