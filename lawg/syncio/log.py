from __future__ import annotations

import typing as t
from lawg.exceptions import LawgAlreadyDeletedError

from lawg.typings import UNDEFINED, Undefined
from lawg.base.log import BaseLog


if t.TYPE_CHECKING:
    from lawg.syncio.client import Client  # noqa: F401


class Log(BaseLog["Client"]):
    """A log."""

    def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> None:
        log_data = self.client.rest.edit_log(
            project=self.client.project,
            feed=self.feed,
            log_id=self.id,
            title=title,
            description=description,
            emoji=emoji,
        )

        self.title = log_data["title"]
        self.description = log_data["description"]
        self.emoji = log_data["emoji"]

    def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeletedError()

        self.client.rest.delete_log(project=self.client.project, feed=self.feed, log_id=self.id)
        self.is_deleted = True
