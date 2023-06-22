from __future__ import annotations

import typing as t

import httpx
from marshmallow import Schema

from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema, Undefined

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client


from lawg.schemas import (
    FeedCreateBodySchema,
    FeedPatchBodySchema,
    FeedSchema,
    FeedSlugSchema,
    FeedWithNameSlugSchema,
    InsightCreateBodySchema,
    InsightCreateSlugSchema,
    InsightPatchBodySchema,
    InsightSchema,
    InsightSlugSchema,
    LogCreateBodySchema,
    LogGetMultipleBodySchema,
    LogPatchBodySchema,
    LogSchema,
    LogSlugSchema,
    LogWithIdSlugSchema,
    ProjectBodySchema,
    ProjectSchema,
    ProjectSlugSchema,
)


class Rest(BaseRest[httpx.Client]):
    """The syncio rest manager."""

    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.http_client = httpx.Client()
        self.http_client.headers.update(self.headers)

    def request(
        self,
        *,
        url: str,
        method: str,
        body_with_schema: DataWithSchema | None = None,
        slugs_with_schema: DataWithSchema | None = None,
        response_schema: Schema | None = None,
    ) -> STR_DICT:
        url, body_dict = self.prepare_request(url, body_with_schema, slugs_with_schema)

        resp = self.http_client.request(method=method, url=url, json=body_dict)

        return self.prepare_response(resp, response_schema=response_schema)

    # --- PROJECTS --- #

    def _create_project(self, project_namespace: str, project_name: str):
        body = {
            "namespace": project_namespace,
            "name": project_name,
        }
        project_data = self.request(
            url=self.API_CREATE_PROJECT,
            method="POST",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def _fetch_project(self, project_namespace: str):
        slugs = {
            "namespace": project_namespace,
        }
        project_data = self.request(
            url=self.API_GET_PROJECT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def _edit_project(self, project_namespace: str, project_name: str):
        body = {
            "namespace": project_namespace,
            "name": project_name,
        }
        project_data = self.request(
            url=self.API_EDIT_PROJECT,
            method="PATCH",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    def _delete_project(self, project_namespace: str) -> None:
        slugs = {
            "namespace": project_namespace,
        }
        self.request(
            url=self.API_DELETE_PROJECT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
        )

    # --- FEEDS --- #

    def _create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
        }
        data = {
            "name": feed_name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.request(
            url=self.API_CREATE_FEED,
            method="POST",
            body_with_schema=DataWithSchema(data, FeedCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    def _edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "name": name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = self.request(
            url=self.API_EDIT_FEED,
            method="PATCH",
            body_with_schema=DataWithSchema(data, FeedPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    def _delete_feed(self, project_namespace: str, feed_name: str) -> None:
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        self.request(
            url=self.API_DELETE_FEED,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
        )

    # --- LOGS --- #

    def _create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = self.request(
            url=self.API_CREATE_LOG,
            method="POST",
            body_with_schema=DataWithSchema(data, LogCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def _fetch_log(self, project_namespace: str, feed_name: str, log_id: str):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }
        log_data = self.request(
            url=self.API_GET_LOG,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def _fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
        }
        data = {
            "limit": limit,
            "offset": offset,
        }
        # this is definitely not best practice, but this is the only route with
        # a list return type and I couldn't get the generic working :p
        logs_data: list[STR_DICT] = self.request(
            url=self.API_GET_LOGS,
            method="GET",
            body_with_schema=DataWithSchema(data, LogGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(many=True),
        )  # type: ignore
        return logs_data

    def _edit_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = self.request(
            url=self.API_EDIT_LOG,
            method="PATCH",
            body_with_schema=DataWithSchema(data, LogPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    def _delete_log(self, project_namespace: str, feed_name: str, log_id: str):
        slugs = {
            "namespace": project_namespace,
            "feed_name": feed_name,
            "log_id": log_id,
        }
        self.request(
            url=self.API_DELETE_LOG,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
        )

    # --- INSIGHTS --- #

    def _create_insight(
        self,
        project_namespace: str,
        title: str,
        description: str | None = None,
        value: float | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project_namespace,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.request(
            url=self.API_CREATE_INSIGHT,
            method="POST",
            body_with_schema=DataWithSchema(data, InsightCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightCreateSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _fetch_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        insight_data = self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _fetch_insights(
        self,
        project_namespace: str,
    ):
        slugs = {
            "namespace": project_namespace,
        }
        insights_data: list[STR_DICT] = self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(many=True),
        )  # type: ignore
        return insights_data

    def _edit_insight(
        self,
        project_namespace: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: dict[str, float] | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = self.request(
            url=self.API_EDIT_INSIGHT,
            method="PATCH",
            body_with_schema=DataWithSchema(data, InsightPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    def _delete_insight(
        self,
        project_namespace: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project_namespace,
            "insight_id": insight_id,
        }
        self.request(
            url=self.API_DELETE_INSIGHT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
        )
