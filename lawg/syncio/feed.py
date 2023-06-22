from __future__ import annotations

import typing as t

from lawg.base.feed import BaseFeed
from lawg.exceptions import LawgAlreadyDeleted
from lawg.typings import UNDEFINED, Undefined
from lawg.syncio.log_manager import LogManager

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client


class Feed(BaseFeed["Client", "LogManager"]):
    # --- MANAGERS --- #

    def log(self, id: str | None = None):
        return LogManager(client=self.client, project_namespace=self.project_namespace, feed_name=self.name, id=id)

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
        feed_data = self.client.rest._edit_feed(
            project_namespace=self.project_namespace,
            feed_name=self.name,
            name=name,
            description=description,
            emoji=emoji,
        )
        self.name = feed_data["name"]
        self.description = feed_data["description"]
        self.emoji = feed_data["emoji"]

    def delete(self):
        """
        Deletes the feed.
        """
        if self.is_deleted:
            raise LawgAlreadyDeleted("feed")

        self.client.rest._delete_feed(project_namespace=self.project_namespace, feed_name=self.name)
        self.is_deleted = True
