from __future__ import annotations

import typing as t

from lawg.base.log_manager import BaseLogManager
from lawg.exceptions import LawgIDMissing
from lawg.syncio.log import Log
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.log import Log


class LogManager(BaseLogManager["Client", "Log"]):
    """
    A manager for a log.
    """

    def create(self, title: str, description: str | None, emoji: str | None, color: str | None) -> Log:
        log_data = self.client.rest._create_log(
            project_namespace=self.project_namespace,
            feed_name=self.feed_name,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )
        return self.client._construct_log(self.project_namespace, self.feed_name, log_data)

    def get(self) -> Log:
        if not self.id:
            raise LawgIDMissing("id is required to get a log")

        log_data = self.client.rest._fetch_log(
            project_namespace=self.project_namespace,
            feed_name=self.feed_name,
            log_id=self.id,
        )
        return self.client._construct_log(self.project_namespace, self.feed_name, log_data)

    def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ) -> Log:
        if not self.id:
            raise LawgIDMissing("id is required to edit a log")

        log_data = self.client.rest._edit_log(
            project_namespace=self.project_namespace,
            feed_name=self.feed_name,
            log_id=self.id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )
        return self.client._construct_log(self.project_namespace, self.feed_name, log_data)

    def delete(self) -> None:
        if not self.id:
            raise LawgIDMissing("id is required to delete a log")

        self.client.rest._delete_log(project_namespace=self.project_namespace, feed_name=self.feed_name, log_id=self.id)
