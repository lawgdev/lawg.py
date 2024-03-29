from __future__ import annotations

import typing as t

import httpx
from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT, UNDEFINED, DataWithSchema, Undefined

from lawg.schemas import (
    FeedCreateBodySchema,
    FeedCreateSlugSchema,
    FeedDeleteSlugSchema,
    FeedPatchBodySchema,
    FeedPatchSlugSchema,
    InsightCreateBodySchema,
    InsightCreateSlugSchema,
    InsightGetMultipleBodySchema,
    InsightGetSlugSchema,
    InsightPatchBodySchema,
    InsightPatchSlugSchema,
    InsightValueSchema,
    EventCreateBodySchema,
    EventCreateSlugSchema,
    EventDeleteSlugSchema,
    EventGetMultipleBodySchema,
    EventGetMultipleSlugSchema,
    EventGetSlugSchema,
    EventPatchBodySchema,
    EventPatchSlugSchema,
    ProjectDeleteSlugSchema,
    ProjectGetSlugSchema,
    ProjectPatchBodySchema,
    ProjectPatchSlugSchema,
    ProjectSchema,
    FeedSchema,
    EventSchema,
    InsightSchema,
    ProjectCreateBodySchema,
)

if t.TYPE_CHECKING:
    import datetime
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
            body_with_schema=DataWithSchema(body, ProjectCreateBodySchema()),
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
            slugs_with_schema=DataWithSchema(slugs, ProjectGetSlugSchema()),
            response_schema=ProjectSchema(),
        )
        return project_data

    async def edit_project(self, project: str, project_name: str):
        slugs = {
            "namespace": project,
        }
        body = {
            "name": project_name,
        }
        project_data = await self.request(
            url=self.API_EDIT_PROJECT,
            method="PATCH",
            slugs_with_schema=DataWithSchema(slugs, ProjectPatchSlugSchema()),
            body_with_schema=DataWithSchema(body, ProjectPatchBodySchema()),
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
            slugs_with_schema=DataWithSchema(slugs, ProjectDeleteSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, FeedCreateSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, FeedPatchSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, FeedDeleteSlugSchema()),
        )

    # --- EVENTS --- #

    async def create_event(
        self,
        project: str,
        feed: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        tags: dict[str, str | int | float | bool] | None = None,
        timestamp: datetime.datetime | None = None,
        notify: bool | None = None,
        metadata: dict[str, str | int | float | bool] | None = None,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "tags": tags,
            "timestamp": timestamp,
            "notify": notify,
            "metadata": metadata,
        }
        event_data = await self.request(
            url=self.API_CREATE_EVENT,
            method="POST",
            body_with_schema=DataWithSchema(data, EventCreateBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, EventCreateSlugSchema()),
            response_schema=EventSchema(),
        )
        return event_data

    async def fetch_event(self, project: str, feed: str, event_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "event_id": event_id,
        }
        event_data = await self.request(
            url=self.API_GET_EVENT,
            method="GET",
            slugs_with_schema=DataWithSchema(slugs, EventGetSlugSchema()),
            response_schema=EventSchema(),
        )
        return event_data

    async def fetch_events(
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
        events_data: list[STR_DICT] = await self.request(
            url=self.API_GET_EVENTS,
            method="GET",
            body_with_schema=DataWithSchema(data, EventGetMultipleBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, EventGetMultipleSlugSchema()),
            response_schema=EventSchema(many=True),
        )  # type: ignore
        return events_data

    async def edit_event(
        self,
        project: str,
        feed: str,
        event_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        tags: dict[str, str | int | float | bool] | Undefined | None = UNDEFINED,
        timestamp: datetime.datetime | Undefined | None = UNDEFINED,
    ):
        slugs = {
            "namespace": project,
            "feed": feed,
            "event_id": event_id,
        }
        data = {
            "title": title,
            "description": description,
            "emoji": emoji,
            "tags": tags,
            "timestamp": timestamp,
        }
        event_data = await self.request(
            url=self.API_EDIT_EVENT,
            method="PATCH",
            body_with_schema=DataWithSchema(data, EventPatchBodySchema()),
            slugs_with_schema=DataWithSchema(slugs, EventPatchSlugSchema()),
            response_schema=EventSchema(),
        )
        return event_data

    async def delete_event(self, project: str, feed: str, event_id: str):
        slugs = {
            "namespace": project,
            "feed": feed,
            "event_id": event_id,
        }
        await self.request(
            url=self.API_DELETE_EVENT,
            method="DELETE",
            slugs_with_schema=DataWithSchema(slugs, EventDeleteSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, InsightGetSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, InsightGetMultipleBodySchema()),
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
            slugs_with_schema=DataWithSchema(slugs, InsightPatchSlugSchema()),
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
            slugs_with_schema=DataWithSchema(slugs, InsightValueSchema()),
        )
