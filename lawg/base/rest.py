from __future__ import annotations

import os
import typing as t
from abc import ABC, abstractmethod

import marshmallow
import httpx

from lawg.exceptions import (
    LawgEmptyBodyError,
    LawgHTTPError,
    LawgConflictError,
    LawgBadRequestError,
    LawgUnauthorizedError,
    LawgNotFoundError,
    LawgInternalServerError,
    LawgForbiddenError,
)
from lawg.schemas import APIErrorSchema, APISuccessSchema
from lawg.typings import C, H, UNDEFINED, DataWithSchema, Undefined

if t.TYPE_CHECKING:
    import datetime
    from marshmallow import Schema
    from lawg.typings import STR_DICT


class BaseRest(ABC, t.Generic[C, H]):
    USER_AGENT = "lawg.py; (+https://github.com/lawgdev/lawg.py)"
    HOSTNAME = "https://lawg.dev"

    API = os.getenv("LAWG_DEV_API", "https://api.lawg.dev")
    API_V1 = f"{API}/v1"
    API_V1_PROJECTS = f"{API_V1}/projects"

    # https://github.com/lawgdev/api/blob/main/src/routes/projects.ts#LL19C18-L19C18

    # --- PROJECTS --- #
    API_CREATE_PROJECT = API_V1_PROJECTS
    API_GET_PROJECT = f"{API_V1_PROJECTS}/{{namespace}}"
    API_EDIT_PROJECT = f"{API_V1_PROJECTS}/{{namespace}}"
    API_DELETE_PROJECT = f"{API_V1_PROJECTS}/{{namespace}}"

    # --- INVITATIONS --- #
    API_INVITE_MEMBER = f"{API_V1_PROJECTS}/{{namespace}}/invites/{{username}}"
    API_REVOKE_INVITE = f"{API_V1_PROJECTS}/{{namespace}}/invites/{{username}}"

    # --- MEMBERS --- #
    API_MEMBERS = f"{API_V1_PROJECTS}/{{namespace}}/members/{{username}}"

    # --- FEEDS --- #
    API_CREATE_FEED = f"{API_V1_PROJECTS}/{{namespace}}/feeds"
    API_EDIT_FEED = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}"
    API_DELETE_FEED = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}"

    # --- EVENTS --- #
    API_CREATE_EVENT = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}/events"
    API_GET_EVENT = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}/events/{{event_id}}"
    API_GET_EVENTS = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}/events"
    API_EDIT_EVENT = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}/events/{{event_id}}"
    API_DELETE_EVENT = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed}}/events/{{event_id}}"

    # --- INSIGHTS --- #
    API_CREATE_INSIGHT = f"{API_V1_PROJECTS}/{{namespace}}/insights"
    API_GET_INSIGHT = f"{API_V1_PROJECTS}/{{namespace}}/insights/{{insight_id}}"
    API_GET_INSIGHTS = f"{API_V1_PROJECTS}/{{namespace}}/insights"
    API_EDIT_INSIGHT = f"{API_V1_PROJECTS}/{{namespace}}/insights/{{insight_id}}"
    API_DELETE_INSIGHT = f"{API_V1_PROJECTS}/{{namespace}}/insights/{{insight_id}}"

    __slots__ = ("client", "http_client")

    def __init__(self, client: C) -> None:
        self.client: C = client
        self.http_client: H

    @property
    def headers(self) -> dict[str, str]:
        return {"User-Agent": self.USER_AGENT, "Authorization": self.client.token}

    @abstractmethod
    def request(
        self,
        *,
        url: str,
        method: str,
        body_with_schema: DataWithSchema | None = None,
        slugs_with_schema: DataWithSchema | None = None,
        response_schema: Schema | None = None,
    ) -> STR_DICT:
        """
        Make a request to the API.

        Args:
            path (str): path of request.
            method (str): HTTP method.
            body: (dict[str, Any] | None, optional): body of request. Defaults to None.

        Returns:
            dict: response body of request.
        """

    def prepare_body(self, body: DataWithSchema | None) -> STR_DICT | None:
        """
        Finalize the body of a request by removing undefined values.

        Args:
            body: body data and body schema of request.
        """
        if body is None:
            return None

        original_body: STR_DICT = body.data
        new_body: STR_DICT = {}

        for key, value in original_body.items():
            if value is UNDEFINED:
                continue
            new_body[key] = value

        loaded_body: STR_DICT = body.schema.load(new_body)  # type: ignore

        if not loaded_body:
            raise LawgEmptyBodyError()

        return loaded_body

    def prepare_url(self, url: str, slugs_with_schema: DataWithSchema | None) -> str:
        """
        Finalize the url of a request by adding slugs based on the schema.

        Args:
            url (str): url of request.
            slug_schema (Schema | None): schema of slugs.
        """

        if slugs_with_schema:
            schema = slugs_with_schema.schema
            data = slugs_with_schema.data

            slugs: STR_DICT = schema.load(data)  # type: ignore
            url = url.format(**slugs)

        return url

    def prepare_request(
        self, url: str, body_with_schema: DataWithSchema | None, slugs_with_schema: DataWithSchema | None
    ) -> tuple[str, STR_DICT | None]:
        """
        Prepare a request to the API by adding slugs to the url and finalizing the body.

        Args:
            url (str): url of request.
            body (dict[str, Any] | None, optional): body of request. Defaults to None.

        Returns:
            tuple[str, dict[str, Any] | None]: url and body of request.
        """
        body = self.prepare_body(body_with_schema)
        url = self.prepare_url(url, slugs_with_schema)
        return url, body

    def validate_response(self, response: httpx.Response) -> None:
        """
        Validate a response from the API.

        Args:
            response (httpx.Response): response from API.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            data = response.json()
            schema = APIErrorSchema()

            try:
                schema.load(data)
            except marshmallow.ValidationError as exc:
                # error follows fastify error format, meaning it never got a proper json reply from api
                # in this case, 404 can be handled pretty easily but im not sure about much else.

                if response.status_code == 404:
                    raise LawgNotFoundError(message=data["message"], status_code=response.status_code) from exc

                raise LawgHTTPError(status_code=response.status_code) from exc

            error_code: str = data["error"]["code"]
            error_message: str = data["error"]["message"]

            if error_code == "conflict":
                raise LawgConflictError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "bad_request":
                raise LawgBadRequestError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "unauthorized":
                raise LawgUnauthorizedError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "not_found":
                raise LawgNotFoundError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "internal_server_error":
                raise LawgInternalServerError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "forbidden":
                raise LawgForbiddenError(message=error_message, status_code=response.status_code) from exc
            else:
                raise LawgHTTPError(message=error_message, status_code=response.status_code) from exc

    def prepare_response(
        self,
        response: httpx.Response,
        response_schema: Schema | None,
    ) -> STR_DICT:
        """
        Prepare a response from the API by validating it and returning the body.
        """
        self.validate_response(response)

        if response.status_code == 204 or not response_schema:
            return {}

        resp_data = response.json()
        api_data: STR_DICT = APISuccessSchema().load(resp_data)  # type: ignore
        schema_data = response_schema.load(api_data["data"])

        return schema_data  # type: ignore

    # --- API INTERACTIONS METHODS --- #

    # --- PROJECTS --- #

    @abstractmethod
    def create_project(self, name: str, project: str) -> STR_DICT:
        """
        Create a project.

        Args:
            name (str): name of project.
            project (str): namespace of project.
        Returns:
            the created project data.
        """

    @abstractmethod
    def fetch_project(self, project: str) -> STR_DICT:
        """
        Fetch a project.

        Args:
            namespace (str): namespace of event.
        Returns:
            the fetched project data.
        """

    @abstractmethod
    def edit_project(self, name: str, project: str) -> STR_DICT:
        """
        Edit a project.

        Args:
            name (str): name of project, what is being changed.
            project (str): namespace of project.
        Returns:
            the edited project data.
        """

    @abstractmethod
    def delete_project(
        self,
        project: str,
    ) -> STR_DICT:
        """
        Delete a project.

        Args:
            namespace (str): namespace of project.
        Returns:
            the deleted project data.
        """

    # --- FEEDS --- #

    @abstractmethod
    def create_feed(
        self,
        project: str,
        feed: str,
        description: str | None = None,
    ) -> STR_DICT:
        """
        Create a feed.

        Args:
            project (str): namespace of project.
            feed (str): name of the feed.
            description (str | None, optional): description of feed. Defaults to None.
        Returns:
            the created feed data.
        """

    @abstractmethod
    def edit_feed(
        self,
        project: str,
        feed: str,
        name: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit a feed.

        Args:
            project (str): namespace of project.
            feed (str): name of feed
            name (str | None, optional): new name of feed. Defaults to keeping the existing value.
            description (str | None, optional): new description of feed. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of feed. Defaults to keeping the existing value.
        Returns:
            the edited feed data.
        """

    @abstractmethod
    def delete_feed(
        self,
        project: str,
        feed: str,
    ) -> None:
        """
        Delete a feed.

        Args:
            project (str): namespace of project.
            feed (str): name of feed .
        Returns:
            None
        """

    # --- EVENTS --- #

    @abstractmethod
    def create_event(
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
    ) -> STR_DICT:
        """
        Create an event.

        Args:
            project (str): namespace of project.
            feed (str): name of feed.
            title (str): title of event.
            description (str | None, optional): description of event. Defaults to None.
            emoji (str | None, optional): emoji of event. Defaults to None.
            tags (dict[str, str | int | float | bool] | None, optional): tags of event. Defaults to None.
            timestamp (datetime.datetime | None, optional): timestamp of event. Defaults to None.
            notify (bool | None, optional): notify of event. Defaults to None.
            metadata (dict[str, str | int | float | bool] | None, optional): metadata of event. Defaults to None.
        Returns:
            the created event data.
        """

    @abstractmethod
    def fetch_event(
        self,
        project: str,
        feed: str,
        event_id: str,
    ) -> STR_DICT:
        """
        Fetch an event.

        Args:
            project (str): namespace of project.
            feed (str): name of feed.
            event_id (str): id of event.
        Returns:
            the fetched event data.
        """

    @abstractmethod
    def fetch_events(
        self,
        project: str,
        feed: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[STR_DICT]:
        """
        Fetch multiple events.

        Args:
            project (str): namespace of project.
            feed (str): name of feed.
            limit (int | None, optional): limit of events. Defaults to None.
            offset (int | None, optional): offset of events. Defaults to None.
        Returns:
            the fetched events' data.
        """

    @abstractmethod
    def edit_event(
        self,
        project: str,
        feed: str,
        event_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        tags: dict[str, str | int | float | bool] | None | Undefined = UNDEFINED,
        timestamp: datetime.datetime | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit an event.

        Args:
            project (str): namespace of project.
            feed (str): name of feed.
            event_id (str): id of event.
            title (str | None, optional): new title of event. Defaults to keeping the existing value.
            description (str | None, optional): new description of event. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of event. Defaults to keeping the existing value.
            tags (dict[str, str | int | float | bool] | None, optional): new tags of event. Defaults to keeping the existing value.
            timestamp (datetime.datetime | None, optional): new timestamp of event. Defaults to keeping the existing value.
        Returns:
            the edited event data.
        """

    @abstractmethod
    def delete_event(
        self,
        project: str,
        feed: str,
        event_id: str,
    ) -> None:
        """
        Delete an event.

        Args:
            project (str): namespace of project.
            feed (str): name of feed.
            event_id (str): id of event.
        Returns:
            None
        """

    # --- INSIGHT --- #

    @abstractmethod
    def create_insight(
        self,
        project: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        value: float | None = None,
    ) -> STR_DICT:
        """
        Create an insight.

        Args:
            project (str): namespace of project.
            title (str): title of insight.
            description (str | None, optional): description of insight. Defaults to None.
            emoji (str | None, optional): emoji of insight. Defaults to None.
            value (float | None, optional): value of insight. Defaults to None.
        Returns:
            the created insight data.
        """

    @abstractmethod
    def fetch_insight(
        self,
        project: str,
        insight_id: str,
    ) -> STR_DICT:
        """
        Fetch an insight.

        Args:
            project (str): namespace of project.
            insight_id (str): id of insight.
        Returns:
            the fetched insight data.
        """

    @abstractmethod
    def fetch_insights(
        self,
        project: str,
    ) -> list[STR_DICT]:
        """
        Fetch multiple insights.

        Args:
            project (str): namespace of project.
        Returns:
            the fetched insights data.
        """

    @abstractmethod
    def edit_insight(
        self,
        project: str,
        insight_id: str,
        title: str | None | Undefined = UNDEFINED,
        description: str | None | Undefined = UNDEFINED,
        emoji: str | None | Undefined = UNDEFINED,
        value: float | None | Undefined = UNDEFINED,
    ) -> STR_DICT:
        """
        Edit an insight.

        Args:
            project (str): namespace of project.
            insight_id (str): id of insight.
            title (str | None, optional): new title of insight. Defaults to keeping the existing value.
            description (str | None, optional): new description of insight. Defaults to keeping the existing value.
            emoji (str | None, optional): new emoji of insight. Defaults to keeping the existing value.
            value (float | None, optional): new value of insight. Defaults to keeping the existing value.
        Returns:
            the edited insight data.
        """

    @abstractmethod
    def delete_insight(
        self,
        project: str,
        insight_id: str,
    ) -> None:
        """
        Delete an insight.

        Args:
            project (str): namespace of project.
            insight_id (str): id of insight.
        Returns:
            None
        """
