from __future__ import annotations

import os
import typing as t
from abc import ABC, abstractmethod

import marshmallow
import httpx

from lawg.exceptions import (
    LawgEmptyBody,
    LawgHTTPException,
    LawgConflict,
    LawgBadRequest,
    LawgUnauthorized,
    LawgNotFound,
    LawgInternalServerError,
    LawgForbidden,
)
from lawg.schemas import APIErrorSchema, APISuccessSchema
from lawg.typings import H, UNDEFINED, DataWithSchema

if t.TYPE_CHECKING:
    from lawg.base.client import BaseClient
    from lawg.typings import STR_DICT
    from marshmallow import Schema


class BaseRest(ABC, t.Generic[H]):
    USER_AGENT = "lawg.py; (+https://github.com/lawg/lawg.py)"
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
    API_EDIT_FEED = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}"
    API_DELETE_FEED = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}"

    # --- LOGS --- #
    API_CREATE_LOG = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}/logs"
    API_GET_LOG = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}/logs/{{log_id}}"
    API_GET_LOGS = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}/logs"
    API_EDIT_LOG = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}/logs/{{log_id}}"
    API_DELETE_LOG = f"{API_V1_PROJECTS}/{{namespace}}/feeds/{{feed_name}}/logs/{{log_id}}"

    __slots__ = ("client", "http_client")

    def __init__(self, client: BaseClient) -> None:
        self.client: BaseClient = client
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
        body: DataWithSchema | None = None,
        slugs: DataWithSchema | None = None,
        response_schema: Schema,
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

        original_body: STR_DICT = body.schema.load(body.data)  # type: ignore
        new_body: STR_DICT = {}

        for key, value in original_body.items():
            if value is UNDEFINED:
                continue
            new_body[key] = value

        if not new_body:
            raise LawgEmptyBody()

        return new_body

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
                    raise LawgNotFound(message=data["message"], status_code=response.status_code) from exc

                raise LawgHTTPException(status_code=response.status_code) from exc

            error_code: str = data["error"]["code"]
            error_message: str = data["error"]["message"]

            if error_code == "conflict":
                raise LawgConflict(message=error_message, status_code=response.status_code) from exc
            elif error_code == "bad_request":
                raise LawgBadRequest(message=error_message, status_code=response.status_code) from exc
            elif error_code == "unauthorized":
                raise LawgUnauthorized(message=error_message, status_code=response.status_code) from exc
            elif error_code == "not_found":
                raise LawgNotFound(message=error_message, status_code=response.status_code) from exc
            elif error_code == "internal_server_error":
                raise LawgInternalServerError(message=error_message, status_code=response.status_code) from exc
            elif error_code == "forbidden":
                raise LawgForbidden(message=error_message, status_code=response.status_code) from exc
            else:
                raise LawgHTTPException(message=error_message, status_code=response.status_code) from exc

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
