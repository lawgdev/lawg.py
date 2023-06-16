from __future__ import annotations

import typing as t
from lawg.exceptions import LawgAlreadyDeleted

from lawg.typings import UNDEFINED, Undefined
from lawg.base.log import BaseLog


if t.TYPE_CHECKING:
    from lawg.syncio.client import Client


class Log(BaseLog["Client"]):
    def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ) -> None:
        resp_data = self.client._edit_log(
            project_namespace=self.project_namespace,
            feed_name=self.feed_name,
            log_id=self.id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

        # self.title = resp_data["title"]
        # self.description = resp_data["description"]
        # self.emoji = resp_data["emoji"]
        # self.color = resp_data["color"]

    def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeleted()

        self.client.delete_log(project_namespace=self.project_namespace, feed_name=self.feed_name, log_id=self.id)
        self.is_deleted = True
