from __future__ import annotations


from lawg.base.client import BaseClient
from lawg.syncio.rest import Rest
from lawg.typings import STR_DICT, UNDEFINED, Undefined

from lawg.syncio.log import Log
from lawg.syncio.insight import Insight


class Client(BaseClient["Log", "Insight", "Rest"]):
    """
    The syncio client for lawg.
    """

    def __init__(
        self,
        *,
        token: str,
        project: str,
    ):
        super().__init__(token, project)
        self.rest = Rest(self)

    # --- LOGS --- #

    def log(self, *, feed_name: str, title: str, description: str, emoji: str | None = None):
        log_data = self.rest._create_log(
            project_namespace=self.project,
            feed_name=feed_name,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_log(self.project, feed_name, log_data)

    def edit_log(
        self,
        *,
        feed_name: str,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        log_data = self.rest._edit_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_log(self.project, feed_name, log_data)

    def fetch_log(self, *, feed_name: str, id: str):
        log_data = self.rest._fetch_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
        )
        return self._construct_log(self.project, feed_name, log_data)

    def fetch_logs(self, *, feed_name: str):
        logs_data = self.rest._fetch_logs(
            project_namespace=self.project,
            feed_name=feed_name,
        )
        return self._construct_logs(self.project, feed_name, logs_data)

    def delete_log(self, *, feed_name: str, id: str):
        self.rest._delete_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
        )

    # --- INSIGHTS --- #

    def insight(self, *, title: str, description: str, value: int, emoji: str | None = None):
        insight_data = self.rest._create_insight(
            project_namespace=self.project,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
        )
        return self._construct_insight(self.project, insight_data)

    def edit_insight(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ):
        insight_data = self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_insight(self.project, insight_data)

    def increment_insight(self, *, id: str, value: float):
        insight_data = self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            value={"increment": value},
        )
        return self._construct_insight(self.project, insight_data)

    def set_insight(self, *, id: str, value: int):
        insight_data = self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            value={"set": value},
        )
        return self._construct_insight(self.project, insight_data)

    def fetch_insight(self, *, id: str):
        insight_data = self.rest._fetch_insight(
            project_namespace=self.project,
            insight_id=id,
        )
        return self._construct_insight(self.project, insight_data)

    def fetch_insights(self):
        insights_data = self.rest._fetch_insights(
            project_namespace=self.project,
        )
        return self._construct_insights(self.project, insights_data)

    def delete_insight(self, *, id: str):
        self.rest._delete_insight(
            project_namespace=self.project,
            insight_id=id,
        )

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_log(self, project_namespace: str, feed_name: str, log_data: STR_DICT) -> Log:
        id = log_data["id"]  # noqa: A001
        project_id = log_data["project_id"]
        feed_id = log_data["feed_id"]
        title = log_data["title"]
        description = log_data["description"]
        emoji = log_data["emoji"]
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
        )

    def _construct_insight(
        self,
        project_namespace: str,
        insight_data: STR_DICT,
    ):
        id = insight_data["id"]  # noqa: A001
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
    assert token is not None  # noqa: S101

    client = Client(token=token, project="lawg-py")
    log = client.log(
        feed_name="handler-test",
        title="title",
        description="desc",
    )
    log.edit(description="new_desc")
    print(log)
