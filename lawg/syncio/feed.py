from __future__ import annotations

import typing as t

from lawg.base.feed import BaseFeed
from lawg.exceptions import LawgAlreadyDeleted
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.log import Log


class Feed(BaseFeed["Client", "Log"]):
    # --- FEED --- #

    def edit(
        self,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ):
        """
        Edits the feed.

        Args:
            name (str, None, Undefined, optional): The new name of the feed. Defaults to keeping the previous value.
            description (str, None, Undefined, optional): The new description of the feed. Defaults to keeping the previous value.
            emoji (str, None, Undefined, optional): The new emoji of the feed. Defaults to keeping the previous value.
        """
        return self.client.edit_feed(
            project_namespace=self.project_namespace,
            feed_name=self.name,
            name=name,
            description=description,
            emoji=emoji,
        )

    def delete(self):
        """
        Deletes the feed.
        """
        if self.is_deleted:
            raise LawgAlreadyDeleted("feed")

        self.client.delete_feed(project_namespace=self.project_namespace, feed_name=self.name)
        self.is_deleted = True

    # --- LOG --- #

    def create_log(
        self, title: str, description: str | None = None, emoji: str | None = None, color: str | None = None
    ):
        return self.client.create_log(
            project_namespace=self.project_namespace,
            feed_name=self.name,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def fetch_log(self, id: str):
        return self.client.fetch_log(project_namespace=self.project_namespace, feed_name=self.name, log_id=id)

    def fetch_logs(self, limit: int | None = None, offset: int | None = None):
        return self.client.fetch_logs(
            project_namespace=self.project_namespace, feed_name=self.name, limit=limit, offset=offset
        )

    def edit_log(
        self,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ):
        return self.client.edit_log(
            project_namespace=self.project_namespace,
            feed_name=self.name,
            log_id=id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def delete_log(self, id: str):
        return self.client.delete_log(project_namespace=self.project_namespace, feed_name=self.name, log_id=id)

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
