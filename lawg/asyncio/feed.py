import typing as t

from lawg.base.feed import BaseFeed
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.asyncio.client import AsyncClient
    from lawg.asyncio.event import AsyncEvent


class AsyncFeed(BaseFeed["AsyncClient", "AsyncEvent"]):
    """An async feed."""

    # --- ASYNCIO --- #

    async def __aenter__(self) -> "AsyncFeed":
        return self

    async def __aexit__(self, _exc_type, _exc_value, _traceback) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client.close()

    # --- EVENTS --- #

    async def event(self, *, title: str, description: str):
        return await self.client.event(
            feed=self.name,
            title=title,
            description=description,
        )

    async def edit_event(
        self,
        *,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        return await self.client.edit_event(
            feed=self.name,
            id=id,
            title=title,
            description=description,
            emoji=emoji,
        )

    async def fetch_event(self, *, id: str):
        return await self.client.fetch_event(feed=self.name, id=id)

    async def fetch_events(self):
        return await self.client.fetch_events(feed=self.name)

    async def delete_event(self, *, id: str):
        return await self.client.delete_event(feed=self.name, id=id)
