from __future__ import annotations

import typing as t

from lawg.base.feed_manager import BaseFeedManager
from lawg.syncio.feed import Feed
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.feed import Feed
    from lawg.syncio.log_manager import LogManager


class FeedManager(BaseFeedManager["Client", "Feed", "LogManager"]):
    """
    A manager of a feed.
    """

    # --- MANAGERS --- #

    def log(self, id: str | None = None) -> LogManager:
        return LogManager(
            client=self.client,
            project_namespace=self.project_namespace,
            feed_name=self.name,
            id=id,
        )

    # --- FEED METHODS --- #

    def create(self, description: str | None = None, emoji: str | None = None) -> Feed:
        feed_data = self.client.rest._create_feed(
            project_namespace=self.project_namespace, feed_name=self.name, description=description, emoji=emoji
        )
        return self.client._construct_feed(self.project_namespace, feed_data)

    # def get(self) -> Feed:
    #     feed_data = self.client._fetch_feed(project_namespace=self.project_namespace, feed_name=self.name)
    #     return self.client._construct_feed(self.project_namespace, feed_data)

    def edit(
        self,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> Feed:
        feed_data = self.client.rest._edit_feed(
            project_namespace=self.project_namespace,
            feed_name=self.name,
            name=name,
            description=description,
            emoji=emoji,
        )
        return self.client._construct_feed(self.project_namespace, feed_data)

    def delete(self):
        self.client.rest._delete_feed(project_namespace=self.project_namespace, feed_name=self.name)
