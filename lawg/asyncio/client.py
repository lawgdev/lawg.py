from __future__ import annotations


from lawg.base.client import BaseClient
from lawg.asyncio.feed import AsyncFeed
from lawg.asyncio.rest import AsyncRest
from lawg.asyncio.log import AsyncLog
from lawg.asyncio.insight import AsyncInsight

from lawg.typings import STR_DICT, UNDEFINED, Undefined


class AsyncClient(BaseClient["AsyncFeed", "AsyncLog", "AsyncInsight", "AsyncRest"]):
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

    # --- LOGS --- #

    async def log(self, *, feed_name: str, title: str, description: str, emoji: str | None = None):
        log_data = await self.rest._create_log(
            project_namespace=self.project,
            feed_name=feed_name,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_log(self.project, feed_name, log_data)

    async def edit_log(
        self,
        *,
        feed_name: str,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        log_data = await self.rest._edit_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_log(self.project, feed_name, log_data)

    async def fetch_log(self, *, feed_name: str, id: str):
        log_data = await self.rest._fetch_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
        )
        return self._construct_log(self.project, feed_name, log_data)

    async def fetch_logs(self, *, feed_name: str):
        logs_data = await self.rest._fetch_logs(
            project_namespace=self.project,
            feed_name=feed_name,
        )
        return self._construct_logs(self.project, feed_name, logs_data)

    async def delete_log(self, *, feed_name: str, id: str):
        await self.rest._delete_log(
            project_namespace=self.project,
            feed_name=feed_name,
            log_id=id,
        )

    # --- INSIGHTS --- #

    async def insight(self, *, title: str, description: str, value: int, emoji: str | None = None):
        insight_data = await self.rest._create_insight(
            project_namespace=self.project,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
        )
        return self._construct_insight(self.project, insight_data)

    async def edit_insight(
        self,
        *,
        id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ):
        insight_data = await self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            title=title,
            description=description,
            emoji=emoji,
        )
        return self._construct_insight(self.project, insight_data)

    async def increment_insight(self, *, id: str, value: float):
        insight_data = await self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            value={"increment": value},
        )
        return self._construct_insight(self.project, insight_data)

    async def set_insight(self, *, id: str, value: int):
        insight_data = await self.rest._edit_insight(
            project_namespace=self.project,
            insight_id=id,
            value={"set": value},
        )
        return self._construct_insight(self.project, insight_data)

    async def fetch_insight(self, *, id: str):
        insight_data = await self.rest._fetch_insight(
            project_namespace=self.project,
            insight_id=id,
        )
        return self._construct_insight(self.project, insight_data)

    async def fetch_insights(self):
        insights_data = await self.rest._fetch_insights(
            project_namespace=self.project,
        )
        return self._construct_insights(self.project, insights_data)

    async def delete_insight(self, *, id: str):
        await self.rest._delete_insight(
            project_namespace=self.project,
            insight_id=id,
        )

    # --- MANAGER CONSTRUCTORS --- #

    def _construct_log(self, project_namespace: str, feed_name: str, log_data: STR_DICT):
        id = log_data["id"]  # noqa: A001
        project_id = log_data["project_id"]
        feed_id = log_data["feed_id"]
        title = log_data["title"]
        description = log_data["description"]
        emoji = log_data["emoji"]
        return AsyncLog(
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

        return AsyncInsight(
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
    import os, asyncio
    from rich import print

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None  # noqa: S101

    async def main():
        feed = AsyncClient(token=token, project="lawg-py").feed(name="test-feed") 
        tasks_1: list[asyncio.Task[AsyncLog]] = []

        for i in range(10):
            coro = feed.log(title=str(i + 1), description="async log :)")
            task = asyncio.create_task(coro)
            tasks_1.append(task)

        logs: list[AsyncLog] = await asyncio.gather(*tasks_1)
        tasks_2: list[asyncio.Task[None]] = []

        print(logs)

        for log in logs:
            coro = log.delete()
            task = asyncio.create_task(coro)
            tasks_2.append(task)

        await asyncio.gather(*tasks_2)
        await feed.close()

    asyncio.run(main())
