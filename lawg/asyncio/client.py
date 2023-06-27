from __future__ import annotations

import typing as t

from lawg.base.client import BaseClient
from lawg.asyncio.feed import AsyncFeed
from lawg.asyncio.rest import AsyncRest
from lawg.asyncio.event import AsyncEvent
from lawg.asyncio.insight import AsyncInsight

from lawg.typings import STR_DICT, UNDEFINED, Undefined

if t.TYPE_CHECKING:
    import datetime


class AsyncClient(BaseClient["AsyncFeed", "AsyncEvent", "AsyncInsight", "AsyncRest"]):
    """
    The syncio client for lawg.
    """

    def __init__(
        self,
        *,
        token: str,
        project: str,
    ) -> None:
        super().__init__(token, project)
        self.rest = AsyncRest(self)

    # --- ASYNCIO --- #

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, _exc_type, _exc_value, _traceback) -> None:
        await self.close()

    async def close(self) -> None:
        await self.rest.close()

    # --- MANAGERS --- #

    def feed(self, *, name: str):
        return AsyncFeed(self, name=name)

    # --- EVENTS --- #

    async def event(
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
        event_data = await self.rest.create_event(
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

    async def edit_event(
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
        event_data = await self.rest.edit_event(
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

    async def fetch_event(self, *, feed: str, id: str):
        event_data = await self.rest.fetch_event(
            project=self.project,
            feed=feed,
            event_id=id,
        )
        return self._construct_event(feed, event_data)

    async def fetch_events(self, *, feed: str):
        events_data = await self.rest.fetch_events(
            project=self.project,
            feed=feed,
        )
        return self._construct_events(feed, events_data)

    async def delete_event(self, *, feed: str, id: str):
        await self.rest.delete_event(
            project=self.project,
            feed=feed,
            event_id=id,
        )

    # --- INSIGHTS --- #

    async def insight(self, *, title: str, description: str, value: int, emoji: str | None = None):
        insight_data = await self.rest.create_insight(
            project=self.project,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
        )
        return self._construct_insight(insight_data)

    async def edit_insight(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ):
        insight_data = await self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_insight(insight_data)

    async def increment_insight(self, *, id: str, value: float):
        insight_data = await self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            value={"increment": value},
        )
        return self._construct_insight(insight_data)

    async def set_insight(self, *, id: str, value: int):
        insight_data = await self.rest.edit_insight(
            project=self.project,
            insight_id=id,
            value={"set": value},
        )
        return self._construct_insight(insight_data)

    async def fetch_insight(self, *, id: str):
        insight_data = await self.rest.fetch_insight(
            project=self.project,
            insight_id=id,
        )
        return self._construct_insight(insight_data)

    async def fetch_insights(self):
        insights_data = await self.rest.fetch_insights(
            project=self.project,
        )
        return self._construct_insights(insights_data)

    async def delete_insight(self, *, id: str):
        await self.rest.delete_insight(
            project=self.project,
            insight_id=id,
        )

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_event(self, feed: str, event_data: STR_DICT):
        id = event_data["id"]  # noqa: A001
        project_id = event_data["project_id"]
        feed_id = event_data["feed_id"]
        title = event_data["title"]
        description = event_data["description"]
        emoji = event_data["emoji"]
        return AsyncEvent(
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

        return AsyncInsight(
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
    import os, asyncio
    from rich import print

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None  # noqa: S101

    async def main():
        feed = AsyncClient(token=token, project="lawg-py").feed(name="test-feed")
        tasks_1: list[asyncio.Task[AsyncEvent]] = []

        for i in range(10):
            coro = feed.event(title=str(i + 1), description="async event :)")
            task = asyncio.create_task(coro)
            tasks_1.append(task)

        events: list[AsyncEvent] = await asyncio.gather(*tasks_1)
        tasks_2: list[asyncio.Task[None]] = []

        print(events)

        for event in events:
            coro = event.delete()
            task = asyncio.create_task(coro)
            tasks_2.append(task)

        await asyncio.gather(*tasks_2)
        await feed.close()

    asyncio.run(main())
