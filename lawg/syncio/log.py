from __future__ import annotations

from lawg.typings import UNDEFINED, Undefined

from lawg.base.log import BaseLog
from lawg.syncio.client import Client


class Log(BaseLog["Client"]):
    def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ) -> None:
        return super().edit(title, description, emoji, color)

    def delete(self) -> None:
        return super().delete()
