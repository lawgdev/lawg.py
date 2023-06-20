from lawg.base.insight_manager import BaseInsightManager

import typing as t

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.insight import Insight


class InsightManager(BaseInsightManager["Client", "Insight"]):
    def create(self, title: str, description: str | None = None, value: float | None = None, emoji: str | None = None):
        insight_data = self.client._create_insight(
            project_namespace=self.project_namespace,
            title=title,
            description=description,
            value=value,
            emoji=emoji,
        )
        return self.client._construct_insight(self.project_namespace, insight_data)

    def get(self, id: str):
        insight_data = self.client._fetch_insight(project_namespace=self.project_namespace, insight_id=id)
        return self.client._construct_insight(self.project_namespace, insight_data)

    def set(self, id: str, value: float):
        insight_data = self.client._edit_insight(
            project_namespace=self.project_namespace,
            insight_id=id,
            value={"set": value},
        )
        return self.client._construct_insight(self.project_namespace, insight_data)

    def increment(self, id: str, value: float):
        insight_data = self.client._edit_insight(
            project_namespace=self.project_namespace,
            insight_id=id,
            value={"increment": value},
        )
        return self.client._construct_insight(self.project_namespace, insight_data)
