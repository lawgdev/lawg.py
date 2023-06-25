from lawg.base.insight import BaseInsight

import typing as t

from lawg.exceptions import LawgAlreadyDeletedError

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client  # noqa: F401


class Insight(BaseInsight["Client"]):
    """An insight."""

    def set(self, value: float) -> None:
        insight_data = self.client.rest.edit_insight(
            project=self.client.project,
            insight_id=self.id,
            value={"set": value},
        )
        return_value: float = insight_data["value"]
        self.value = return_value

    def increment(self, value: float) -> None:
        insight_data = self.client.rest.edit_insight(
            project=self.client.project,
            insight_id=self.id,
            value={"increment": value},
        )
        return_value: float = insight_data["value"]
        self.value = return_value

    def delete(self) -> None:
        if self.is_deleted:
            raise LawgAlreadyDeletedError("insight")

        self.client.rest.delete_insight(project=self.client.project, insight_id=self.id)
        self.is_deleted = True
