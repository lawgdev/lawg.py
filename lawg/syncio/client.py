from __future__ import annotations

import typing as t

from lawg.base.client import BaseClient
from lawg.syncio.rest import Rest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema
from lawg.syncio.project import Project
from lawg.syncio.feed import Feed
from lawg.syncio.log import Log

from lawg.schemas import (
    FeedCreateBodySchema,
    FeedPatchBodySchema,
    FeedSchema,
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
    ProjectSlugSchema,
)


if t.TYPE_CHECKING:
    from lawg.typings import Undefined


class Client(BaseClient["Project", "Feed", "Log", "Rest"]):
    """
    The syncio client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.rest = Rest(self)

    # --- MANAGERS --- #

    def project(self, project_namespace: str):
        return super().project(project_namespace)

    def feed(self, project_namespace: str, feed_name: str):
        return super().feed(project_namespace, feed_name)

    # --- PROJECTS --- #

    def create_project(self, project_namespace: str, project_name: str):
        body = {
            "namespace": project_namespace,
            "name": project_name,
        }
        project_data = self.rest.request(
            url=self.rest.API_CREATE_PROJECT,
            method="POST",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return self._construct_project(project_data)

    def fetch_project(self, project_namespace: str):
        slugs = {
            "namespace": project_namespace,
        }
        project_data = self.rest.request(
            url=self.rest.API_GET_PROJECT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return self._construct_project(project_data)

    def edit_project(self, project_namespace: str, project_name: str):
        body = {
            "namespace": project_namespace,
            "name": project_name,
        }
        project_data = self.rest.request(
            url=self.rest.API_EDIT_PROJECT,
            method="PATCH",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return self._construct_project(project_data)

    def delete_project(self, project_namespace: str) -> None:
        slugs = {
            "namespace": project_namespace,
        }
        self.rest.request(
            url=self.rest.API_DELETE_PROJECT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
        )

    patch_project = edit_project
    get_project = fetch_project

    # --- FEEDS --- #

    def create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
        }
        data = {
            "name": feed_name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.rest.request(
            url=self.rest.API_CREATE_FEED,
            method="POST",
            body_with_schema=DataWithSchema(data, FeedCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedSlugSchema()),
            response_schema=FeedSchema(),
        )
        return self._construct_feed(project_namespace, feed_data)

    def edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "name": name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.rest.request(
            url=self.rest.API_EDIT_FEED,
            method="PATCH",
            body_with_schema=DataWithSchema(data, FeedPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
            response_schema=FeedSchema(),
        )
        return self._construct_feed(project_namespace, feed_data)

    def delete_feed(self, project_namespace: str, feed_name: str) -> None:
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        self.rest.request(
            url=self.rest.API_DELETE_FEED,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
        )

    patch_feed = edit_feed

    # --- LOGS --- #

    def create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "color": color,
        }
        log_data = self.rest.request(
            url=self.rest.API_CREATE_LOG,
            method="POST",
            body_with_schema=DataWithSchema(data, LogCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(),
        )
        return self._construct_log(project_namespace, feed_name, log_data)

    def fetch_log(self, project_namespace: str, feed_name: str, log_id: str):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }
        log_data = self.rest.request(
            url=self.rest.API_GET_LOG,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )

        return self._construct_log(project_namespace, feed_name, log_data)

    def fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "limit": limit,
            "offset": offset,
        }
        # this is definitely not best practice, but this is the only route with
        # a list return type and it's okay with this :p
        logs_data: list[STR_DICT] = self.rest.request(
            url=self.rest.API_GET_LOGS,
            method="GET",
            body_with_schema=DataWithSchema(data, LogGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(many=True),
        )  # type: ignore
        return self._construct_logs(project_namespace, feed_name, logs_data)

    def edit_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "color": color,
        }
        log_data = self.rest.request(
            url=self.rest.API_EDIT_LOG,
            method="PATCH",
            body_with_schema=DataWithSchema(data, LogPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )
        return Log(self, project_namespace=project_namespace, feed_name=feed_name, id=log_data["id"])

    def delete_log(self, project_namespace: str, feed_name: str, log_id: str):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }

        self.rest.request(
            url=self.rest.API_DELETE_LOG,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
        )

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_project(self, project_data: STR_DICT) -> Project:
        namespace = project_data["namespace"]
        return Project(self, namespace=namespace)

    def _construct_feed(self, project_namespace: str, feed_data: STR_DICT) -> Feed:
        name = feed_data["name"]
        return Feed(self, project_namespace=project_namespace, name=name)

    def _construct_log(self, project_namespace: str, feed_name: str, log_data: STR_DICT) -> Log:
        id = log_data["id"]
        return Log(self, project_namespace=project_namespace, feed_name=feed_name, id=id)


if __name__ == "__main__":
    import os

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None

    client = Client(token)

    project_namespace = "test"
    project_name = "test"
    feed_name = "123123"

    project = client.create_project(project_namespace, project_name)
    
    feed = project.create_feed(feed_name)
    feed.edit(name="new_name", description="new_desc", emoji="💀")

    log = feed.create_log(title="title", description="desc", emoji="👍", color="red")
    log.edit(title="new_title", description="new_desc", emoji="👎", color="blue")

    print(log)
