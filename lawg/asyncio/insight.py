from lawg.base.insight import BaseInsight

import typing as t

from lawg.exceptions import LawgAlreadyDeletedError


if t.TYPE_CHECKING:
    from lawg.asyncio.client import AsyncClient  # noqa: F401


class AsyncInsight(BaseInsight["AsyncClient"]):
    """An insight."""

    async def set(self, value: float) -> None:
        insight_data = await self.client.rest._edit_insight(
            project=self.client.project,
            insight_id=self.id,
            value={"set": value},
        )
        return_value: float = insight_data["value"]
        self.value = return_value

    async def increment(self, value: float) -> None:
        insight_data = await self.client.rest._edit_insight(
            project=self.client.project,
            insight_id=self.id,
            value={"increment": value},
        )
        return_value: float = insight_data["value"]
        self.value = return_value

    async def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeletedError("insight")

        await self.client.rest._delete_insight(project=self.client.project, insight_id=self.id)
        self.is_deleted = True
