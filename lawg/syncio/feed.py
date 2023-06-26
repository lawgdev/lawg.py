import typing as t

from lawg.base.feed import BaseFeed
from lawg.syncio.event import Event
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.event import Event


class Feed(BaseFeed["Client", "Event"]):
    """A feed."""

    # --- EVENTS --- #

    def event(self, *, title: str, description: str):
        return self.client.event(
            feed=self.name,
            title=title,
            description=description,
        )

    def edit_event(
        self,
        *,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        return self.client.edit_event(
            feed=self.name,
            id=id,
            title=title,
            description=description,
            emoji=emoji,
        )

    def fetch_event(self, *, id: str):
        return self.client.fetch_event(feed=self.name, id=id)

    def fetch_events(self):
        return self.client.fetch_events(feed=self.name)

    def delete_event(self, *, id: str):
        return self.client.delete_event(feed=self.name, id=id)
