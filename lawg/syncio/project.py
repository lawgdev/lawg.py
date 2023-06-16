from __future__ import annotations

import typing as t

from lawg.base.project import BaseProject
from lawg.typings import UNDEFINED

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.feed import Feed
    from lawg.syncio.log import Log
    from lawg.typings import Undefined


class Project(BaseProject["Client", "Feed", "Log"]):
    # --- MANAGERS --- #

    def feed(self, feed_name: str):
        return self.client.feed(project_namespace=self.namespace, feed_name=feed_name)

    # --- FEEDS --- #

    def create_feed(self, feed_name: str, description: str | None = None):
        return self.client.create_feed(project_namespace=self.namespace, feed_name=feed_name, description=description)

    def edit_feed(
        self,
        feed_name: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> Feed:
        return self.client.edit_feed(
            project_namespace=self.namespace, feed_name=feed_name, name=name, description=description, emoji=emoji
        )

    def delete_feed(self, feed_name: str):
        return self.client.delete_feed(project_namespace=self.namespace, feed_name=feed_name)

    patch_feed = edit_feed

    # --- LOGS --- #

    def create_log(
        self,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> Log:
        return self.client.create_log(
            project_namespace=self.namespace,
            feed_name=feed_name,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def fetch_log(self, feed_name: str, log_id: str) -> Log:
        return self.client.fetch_log(project_namespace=self.namespace, feed_name=feed_name, log_id=log_id)

    def fetch_logs(self, feed_name: str, limit: int | None = None, offset: int | None = None) -> list[Log]:
        return self.client.fetch_logs(
            project_namespace=self.namespace, feed_name=feed_name, limit=limit, offset=offset
        )

    def edit_log(
        self,
        feed_name: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ) -> Log:
        return self.client.edit_log(
            project_namespace=self.namespace,
            feed_name=feed_name,
            log_id=log_id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def delete_log(self, feed_name: str, log_id: str):
        return self.client.delete_log(
            project_namespace=self.namespace,
            feed_name=feed_name,
            log_id=log_id,
        )

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
