from __future__ import annotations

import typing as t

from lawg.base.client import BaseClient
from lawg.syncio.rest import Rest
from lawg.typings import STR_DICT

from lawg.syncio.project_manager import ProjectManager
from lawg.syncio.project import Project
from lawg.syncio.feed import Feed
from lawg.syncio.log import Log
from lawg.syncio.insight import Insight


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
    feed = project.feed(feed_name).create()

    log = feed.log().create(title="title", description="desc", emoji="👍", color="red")
    log.edit(title="new_title", description="new_desc", emoji="👎", color="blue")

    print(log)

    # insight = project.insight().create(title="profit", value=123, description="desc", emoji="👍")

    # print(insight)

    # insight.increment(5)
    # insight.increment(5)
    # insight.increment(5)
    # insight.increment(5)

    # insight_2 = project.insight().get(insight.id)
    # print(insight_2)

    # feed = project.create_feed(feed_name)
    # feed.edit(name="new_name", description="new_desc", emoji="💀")

    # log = feed.create_log(title="title", description="desc", emoji="👍", color="red")
    # log.edit(title="new_title", description="new_desc", emoji="👎", color="blue")

    # print(log)
