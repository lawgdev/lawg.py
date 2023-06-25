import typing as t

from lawg.base.feed import BaseFeed
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.asyncio.client import AsyncClient
    from lawg.asyncio.log import AsyncLog


class AsyncFeed(BaseFeed["AsyncClient", "AsyncLog"]):
    """An async feed."""

    # --- ASYNCIO --- #

    async def __aenter__(self) -> "AsyncFeed":
        return self

    async def __aexit__(self, _exc_type, _exc_value, _traceback) -> None:
        await self.close()

    async def close(self) -> None:
        await self.client.close()

    # --- LOGS --- #

    async def log(self, *, title: str, description: str):
        return await self.client.log(
            feed=self.name,
            title=title,
            description=description,
        )

    async def edit_log(
        self,
        *,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        return await self.client.edit_log(
            feed=self.name,
            id=id,
            title=title,
            description=description,
            emoji=emoji,
        )

    async def fetch_log(self, *, id: str):
        return await self.client.fetch_log(feed=self.name, id=id)

    async def fetch_logs(self):
        return await self.client.fetch_logs(feed=self.name)

    async def delete_log(self, *, id: str):
        return await self.client.delete_log(feed=self.name, id=id)
