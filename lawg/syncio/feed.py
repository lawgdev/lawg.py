import typing as t

from lawg.base.feed import BaseFeed
from lawg.syncio.log import Log
from lawg.typings import UNDEFINED, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.log import Log


class Feed(BaseFeed["Client", "Log"]):
    """A feed."""

    # --- LOGS --- #

    def log(self, *, title: str, description: str):
        return self.client.log(
            feed=self.name,
            title=title,
            description=description,
        )

    def edit_log(
        self,
        *,
        id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        return self.client.edit_log(
            feed=self.name,
            id=id,
            title=title,
            description=description,
            emoji=emoji,
        )

    def fetch_log(self, *, id: str):
        return self.client.fetch_log(feed=self.name, id=id)

    def fetch_logs(self):
        return self.client.fetch_logs(feed=self.name)

    def delete_log(self, *, id: str):
        return self.client.delete_log(feed=self.name, id=id)
