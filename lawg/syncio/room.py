from __future__ import annotations
from lawg.base.log import BaseLog

from lawg.base.room import BaseRoom
from lawg.typings import UNDEFINED, Undefined


class Room(BaseRoom):
    def create_log(
        self, title: str, description: str | None = None, emoji: str | None = None, color: str | None = None
    ) -> BaseLog:
        return super().create_log(title, description, emoji, color)

    def fetch_log(self, log_id: str) -> BaseLog:
        return super().fetch_log(log_id)

    def fetch_logs(self, limit: int | None = None, offset: int | None = None) -> list[BaseLog]:
        return super().fetch_logs(limit, offset)

    def edit_log(
        self,
        log_id: str,
        title: str | Undefined | None = ...,
        description: str | Undefined | None = ...,
        emoji: str | Undefined | None = ...,
        color: str | Undefined | None = ...,
    ) -> BaseLog:
        return super().edit_log(log_id, title, description, emoji, color)

    def delete_log(self, log_id: str) -> BaseLog:
        return super().delete_log(log_id)

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
