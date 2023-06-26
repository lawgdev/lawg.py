from __future__ import annotations

import typing as t
from lawg.exceptions import LawgAlreadyDeletedError

from lawg.typings import UNDEFINED, Undefined
from lawg.base.event import BaseEvent


if t.TYPE_CHECKING:
    from lawg.syncio.client import Client  # noqa: F401


class Event(BaseEvent["Client"]):
    """An event."""

    def edit(
        self,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> None:
        event_data = self.client.rest.edit_event(
            project=self.client.project,
            feed=self.feed,
            event_id=self.id,
            title=title,
            description=description,
            emoji=emoji,
        )

        self.title = event_data["title"]
        self.description = event_data["description"]
        self.emoji = event_data["emoji"]

    def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeletedError()

        self.client.rest.delete_event(project=self.client.project, feed=self.feed, event_id=self.id)
        self.is_deleted = True
