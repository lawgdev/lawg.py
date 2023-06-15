from __future__ import annotations

from lawg.base.feed import BaseFeed
from lawg.typings import UNDEFINED, Undefined
from lawg.syncio.client import Client
from lawg.syncio.log import Log


class Feed(BaseFeed["Client", "Log"]):
    def create_log(
        self, title: str, description: str | None = None, emoji: str | None = None, color: str | None = None
    ):
        return super().create_log(title, description, emoji, color)

    def fetch_log(self, log_id: str):
        return super().fetch_log(log_id)

    def fetch_logs(self, limit: int | None = None, offset: int | None = None):
        return super().fetch_logs(limit, offset)

    def edit_log(
        self,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ):
        return super().edit_log(log_id, title, description, emoji, color)

    def delete_log(self, log_id: str):
        return super().delete_log(log_id)

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
