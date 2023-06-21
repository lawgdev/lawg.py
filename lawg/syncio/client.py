from __future__ import annotations

import typing as t

from lawg.base.client import BaseClient
from lawg.syncio.rest import Rest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema

from lawg.syncio.project_manager import ProjectManager
from lawg.syncio.project import Project
from lawg.syncio.feed import Feed
from lawg.syncio.log import Log
from lawg.syncio.insight import Insight

from lawg.schemas import (
    FeedCreateBodySchema,
    FeedPatchBodySchema,
    FeedSchema,
    FeedSlugSchema,
    FeedWithNameSlugSchema,
    InsightCreateBodySchema,
    InsightCreateSlugSchema,
    InsightPatchBodySchema,
    InsightSchema,
    InsightSlugSchema,
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


class Client(BaseClient["ProjectManager", "Project", "Feed", "Log", "Insight", "Rest"]):
    """
    The syncio client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.rest = Rest(self)

    # --- MANAGERS --- #

    def project(self, project_namespace: str):
        return ProjectManager(self, project_namespace)

    # --- PROJECTS --- #

    def _create_project(self, project_namespace: str, project_name: str):
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
        return project_data

    def _fetch_project(self, project_namespace: str):
        slugs = {
            "namespace": project_namespace,
        }
        project_data = self.rest.request(
            url=self.rest.API_GET_PROJECT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def _edit_project(self, project_namespace: str, project_name: str):
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
        return project_data

    def _delete_project(self, project_namespace: str) -> None:
        slugs = {
            "namespace": project_namespace,
        }
        self.rest.request(
            url=self.rest.API_DELETE_PROJECT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
        )

    # --- FEEDS --- #

    def _create_feed(
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
        return feed_data

    def _edit_feed(
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
        return feed_data

    def _delete_feed(self, project_namespace: str, feed_name: str) -> None:
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        self.rest.request(
            url=self.rest.API_DELETE_FEED,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
        )

    # --- LOGS --- #

    def _create_log(
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
        return log_data

    def _fetch_log(self, project_namespace: str, feed_name: str, log_id: str):
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
        return log_data

    def _fetch_logs(
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
        # a list return type and I couldn't get the generic working :p
        logs_data: list[STR_DICT] = self.rest.request(
            url=self.rest.API_GET_LOGS,
            method="GET",
            body_with_schema=DataWithSchema(data, LogGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(many=True),
        )  # type: ignore
        return logs_data

    def _edit_log(
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
        return log_data

    def _delete_log(self, project_namespace: str, feed_name: str, log_id: str):
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

    # --- INSIGHTS --- #

    def _create_insight(
        self,
        project_namespace: str,
        title: str,
        description: str | None = None,
        value: float | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.rest.request(
            url=self.rest.API_CREATE_INSIGHT,
            method="POST",
            body_with_schema=DataWithSchema(data, InsightCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightCreateSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _fetch_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        insight_data = self.rest.request(
            url=self.rest.API_GET_INSIGHT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _edit_insight(
        self,
        project_namespace: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: dict[str, float] | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.rest.request(
            url=self.rest.API_EDIT_INSIGHT,
            method="PATCH",
            body_with_schema=DataWithSchema(data, InsightPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _delete_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        self.rest.request(
            url=self.rest.API_DELETE_INSIGHT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
        )

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_project(self, project_data: STR_DICT) -> Project:
        id = project_data["id"]
        namespace = project_data["namespace"]
        name = project_data["name"]
        flags = project_data["flags"]
        icon = project_data["icon"]
        # created_at = project_data["created_at"]
        # TODO: make these objects
        feeds = project_data["feeds"]
        members = project_data["members"]

        return Project(
            client=self,
            id=id,
            namespace=namespace,
            name=name,
            flags=flags,
            icon=icon,
            # created_at=created_at,
            feeds=feeds,
            members=members,
        )

    def _construct_feed(self, project_namespace: str, feed_data: STR_DICT) -> Feed:
        id = feed_data["id"]
        project_id = feed_data["project_id"]
        name = feed_data["name"]
        description = feed_data["description"]
        emoji = feed_data["emoji"]

        return Feed(
            self,
            project_namespace=project_namespace,
            id=id,
            project_id=project_id,
            name=name,
            description=description,
            emoji=emoji,
        )

    def _construct_log(self, project_namespace: str, feed_name: str, log_data: STR_DICT) -> Log:
        id = log_data["id"]
        project_id = log_data["project_id"]
        feed_id = log_data["feed_id"]
        title = log_data["title"]
        description = log_data["description"]
        emoji = log_data["emoji"]
        color = log_data["color"]
        return Log(
            self,
            project_namespace=project_namespace,
            feed_name=feed_name,
            id=id,
            project_id=project_id,
            feed_id=feed_id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def _construct_insight(
        self,
        project_namespace: str,
        insight_data: STR_DICT,
    ):
        id = insight_data["id"]
        title = insight_data["title"]
        description = insight_data["description"]
        value = insight_data["value"]
        emoji = insight_data["emoji"]
        updated_at = insight_data["updated_at"]
        created_at = insight_data["created_at"]

        return Insight(
            self,
            project_namespace=project_namespace,
            id=id,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
            updated_at=updated_at,
            created_at=created_at,
        )


if __name__ == "__main__":
    import os
    from rich import print

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None

    client = Client(token)

    project_namespace = "test"
    project_name = "test"
    feed_name = "123123"

    project = client.project("hop").create()
    # feed = project.feed(feed_name).create()
    # log = feed.log().create(title="title", description="desc", emoji="👍", color="red")
    # log.edit(title="new_title", description="new_desc", emoji="👎", color="blue")

    insight = project.insight().create(title="profit", value=123, description="desc", emoji="👍")

    print(insight)

    insight.increment(5)
    insight.increment(5)
    insight.increment(5)
    insight.increment(5)

    insight_2 = project.insight().get(insight.id)
    print(insight_2)

    # feed = project.create_feed(feed_name)
    # feed.edit(name="new_name", description="new_desc", emoji="💀")

    # log = feed.create_log(title="title", description="desc", emoji="👍", color="red")
    # log.edit(title="new_title", description="new_desc", emoji="👎", color="blue")

    # print(log)
