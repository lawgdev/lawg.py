from __future__ import annotations


import typing as t

from lawg.base.client import BaseClient
from lawg.syncio.rest import Rest
from lawg.typings import STR_DICT, UNDEFINED, Undefined

from lawg.syncio.feed import Feed
from lawg.syncio.event import Event
from lawg.syncio.insight import Insight

if t.TYPE_CHECKING:
    import datetime


class Client(BaseClient["Feed", "Event", "Insight", "Rest"]):
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

    # --- MANAGERS --- #

    def feed(self, *, name: str):
        # TODO(<hexiro>): figure out why pylance is erroring here.
        return Feed(client=self, name=name)  # type: ignore

    # --- EVENTS --- #

    def event(
        self,
        *,
        feed: str,
        title: str,
        description: str,
        emoji: str | None = None,
        tags: dict[str, str | int | float | bool] | None = None,
        timestamp: datetime.datetime | None = None,
        notify: bool | None = None,
        metadata: dict[str, str | int | float | bool] | None = None,
    ):
        event_data = self.rest.create_event(
            project=self.project,
            feed=feed,
            title=title,
            description=description,
            emoji=emoji,
            tags=tags,
            timestamp=timestamp,
            notify=notify,
            metadata=metadata,
        )
        return self._construct_event(feed, event_data)

    def edit_event(
        self,
        *,
        feed: str,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        tags: dict[str, str | int | float | bool] | Undefined | None = UNDEFINED,
        timestamp: datetime.datetime | Undefined | None = UNDEFINED,
    ):
        event_data = self.rest.edit_event(
            project=self.project,
            feed=feed,
            event_id=id,
            title=title,
            description=description,
            emoji=emoji,
            tags=tags,
            timestamp=timestamp,
        )
        return self._construct_event(feed, event_data)

    def fetch_event(self, *, feed: str, id: str):
        event_data = self.rest.fetch_event(
            project=self.project,
            feed=feed,
            event_id=id,
        )
        return self._construct_event(feed, event_data)

    def fetch_events(self, *, feed: str):
        events_data = self.rest.fetch_events(
            project=self.project,
            feed=feed,
        )
        return self._construct_events(feed, events_data)

    def delete_event(self, *, feed: str, id: str):
        self.rest.delete_event(
            project=self.project,
            feed=feed,
            event_id=id,
        )

    # --- INSIGHTS --- #

    def insight(self, *, title: str, description: str, value: int, emoji: str | None = None):
        insight_data = self.rest.create_insight(
            project=self.project,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
        )
        return self._construct_insight(insight_data)

    def edit_insight(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ):
        insight_data = self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_insight(insight_data)

    def increment_insight(self, *, id: str, value: float):
        insight_data = self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            value={"increment": value},
        )
        return self._construct_insight(insight_data)

    def set_insight(self, *, id: str, value: int):
        insight_data = self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            value={"set": value},
        )
        return self._construct_insight(insight_data)

    def fetch_insight(self, *, id: str):
        insight_data = self.rest.fetch_insight(
            project=self.project,
            insight_id=id,
        )
        return self._construct_insight(insight_data)

    def fetch_insights(self):
        insights_data = self.rest.fetch_insights(
            project=self.project,
        )
        return self._construct_insights(insights_data)

    def delete_insight(self, *, id: str):
        self.rest.delete_insight(
            project=self.project,
            insight_id=id,
        )

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_event(self, feed: str, event_data: STR_DICT) -> Event:
        id = event_data["id"]  # noqa: A001
        project_id = event_data["project_id"]
        feed_id = event_data["feed_id"]
        title = event_data["title"]
        description = event_data["description"]
        emoji = event_data["emoji"]
        return Event(
            self,
            feed=feed,
            id=id,
            project_id=project_id,
            feed_id=feed_id,
            title=title,
            description=description,
            emoji=emoji,
        )

    def _construct_insight(
        self,
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
    event = client.event(
        feed="handler-test",
        title="title",
        description="desc",
    )
    event.edit(description="new_desc")
    print(event)
