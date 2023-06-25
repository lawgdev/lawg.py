from __future__ import annotations

import typing as t
from lawg.base.log import BaseLog
from lawg.exceptions import LawgAlreadyDeletedError
from lawg.typings import UNDEFINED, Undefined


if t.TYPE_CHECKING:
    from lawg.asyncio.client import AsyncClient  # noqa: F401


class AsyncLog(BaseLog["AsyncClient"]):
    """An async log."""

    async def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> None:
        log_data = await self.client.rest.edit_log(
            project=self.client.project,
            feed=self.feed,
            log_id=self.id,
            title=title,
            description=description,
            emoji=emoji,
        )

        self.title = log_data["title"]
        self.description = log_data["description"]
        self.emoji = log_data["emoji"]

    async def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeletedError()

        await self.client.rest.delete_log(project=self.client.project, feed=self.feed, log_id=self.id)
        self.is_deleted = True
