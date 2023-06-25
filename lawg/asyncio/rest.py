from __future__ import annotations

import typing as t

import httpx
from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema, Undefined

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

if t.TYPE_CHECKING:
    from marshmallow import Schema
    from lawg.asyncio.client import AsyncClient


class AsyncRest(BaseRest["AsyncClient", httpx.AsyncClient]):
    """Async rest client for lawg."""

    def __init__(self, client: AsyncClient) -> None:
        super().__init__(client)
        self.http_client = httpx.AsyncClient()
        self.http_client.headers.update(self.headers)

    async def request(
        self,
        *,
        url: str,
        method: str,
        body_with_schema: DataWithSchema | None = None,
        slugs_with_schema: DataWithSchema | None = None,
        response_schema: Schema | None = None,
    ) -> STR_DICT:
        url, body_dict = self.prepare_request(url, body_with_schema, slugs_with_schema)

        resp = await self.http_client.request(method=method, url=url, json=body_dict)

        return self.prepare_response(resp, response_schema=response_schema)

    # --- ASYNCIO --- #

    async def close(self) -> None:
        await self.http_client.aclose()

    # --- PROJECTS --- #

    async def create_project(self, project: str, project_name: str):
        body = {
            "namespace": project,
            "name": project_name,
        }
        project_data = await self.request(
            url=self.API_CREATE_PROJECT,
            method="POST",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    async def fetch_project(self, project: str):
        slugs = {
            "namespace": project,
        }
        project_data = await self.request(
            url=self.API_GET_PROJECT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    async def edit_project(self, project: str, project_name: str):
        body = {
            "namespace": project,
            "name": project_name,
        }
        project_data = await self.request(
            url=self.API_EDIT_PROJECT,
            method="PATCH",
            body_with_schema=DataWithSchema(body, ProjectBodySchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    async def delete_project(self, project: str) -> None:
        slugs = {
            "namespace": project,
        }
        await self.request(
            url=self.API_DELETE_PROJECT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, ProjectSlugSchema()),
        )

    # --- FEEDS --- #

    async def create_feed(
        self,
        project: str,
        feed: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
        }
        data = {
            "name": feed,
            "description": description,
            "emoji": emoji,
        }
        feed_data = await self.request(
            url=self.API_CREATE_FEED,
            method="POST",
            body_with_schema=DataWithSchema(data, FeedCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    async def edit_feed(
        self,
        project: str,
        feed: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "name": name,
            "description": description,
            "emoji": emoji,
        }
        feed_data = await self.request(
            url=self.API_EDIT_FEED,
            method="PATCH",
            body_with_schema=DataWithSchema(data, FeedPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
            response_schema=FeedSchema(),
        )
        return feed_data

    async def delete_feed(self, project: str, feed: str) -> None:
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        await self.request(
            url=self.API_DELETE_FEED,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, FeedWithNameSlugSchema()),
        )

    # --- LOGS --- #

    async def create_log(
        self,
        project: str,
        feed: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = await self.request(
            url=self.API_CREATE_LOG,
            method="POST",
            body_with_schema=DataWithSchema(data, LogCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    async def fetch_log(self, project: str, feed: str, log_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        log_data = await self.request(
            url=self.API_GET_LOG,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    async def fetch_logs(
        self,
        project: str,
        feed: str,
        limit: int | None = None,
        offset: int | None = None,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "limit": limit,
            "offset": offset,
        }
        logs_data: list[STR_DICT] = await self.request(
            url=self.API_GET_LOGS,
            method="GET",
            body_with_schema=DataWithSchema(data, LogGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogSlugSchema()),
            response_schema=LogSchema(many=True),
        )  # type: ignore
        return logs_data

    async def edit_log(
        self,
        project: str,
        feed: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
        }
        log_data = await self.request(
            url=self.API_EDIT_LOG,
            method="PATCH",
            body_with_schema=DataWithSchema(data, LogPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
            response_schema=LogSchema(),
        )
        return log_data

    async def delete_log(self, project: str, feed: str, log_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "log_id": log_id,
        }
        await self.request(
            url=self.API_DELETE_LOG,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, LogWithIdSlugSchema()),
        )

    # --- INSIGHTS --- #

    async def create_insight(
        self,
        project: str,
        title: str,
        description: str | None = None,
        value: float | None = None,
        emoji: str | None = None,
    ):
        slugs = {
            "namespace": project,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = await self.request(
            url=self.API_CREATE_INSIGHT,
            method="POST",
            body_with_schema=DataWithSchema(data, InsightCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightCreateSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    async def fetch_insight(
        self,
        project: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        insight_data = await self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    async def fetch_insights(
        self,
        project: str,
    ):
        slugs = {
            "namespace": project,
        }
        insights_data: list[STR_DICT] = await self.request(
            url=self.API_GET_INSIGHTS,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(many=True),
        )  # type: ignore
        return insights_data

    async def edit_insight(
        self,
        project: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: dict[str, float] | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "value": value,
        }
        insight_data = await self.request(
            url=self.API_EDIT_INSIGHT,
            method="PATCH",
            body_with_schema=DataWithSchema(data, InsightPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
            response_schema=InsightSchema(),
        )
        return insight_data

    async def delete_insight(
        self,
        project: str,
        insight_id: str,
    ):
        slugs = {
            "namespace": project,
            "insight_id": insight_id,
        }
        await self.request(
            url=self.API_DELETE_INSIGHT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, InsightSlugSchema()),
        )
