from __future__ import annotations

import os
import typing as t
from abc import ABC, abstractmethod

import marshmallow
import httpx

from lawg.exceptions import (
    LawgHTTPException,
    LawgConflict,
    LawgBadRequest,
    LawgUnauthorized,
    LawgNotFound,
    LawgInternalServerError,
    LawgForbidden,
)
from lawg.schemas import APIErrorSchema
from lawg.typings import C

if t.TYPE_CHECKING:
    from lawg.base.client import BaseClient
    from lawg.typings import STR_DICT


class BaseRest(ABC, t.Generic[C]):
    USER_AGENT = "lawg.py; (+https://github.com/lawg/lawg.py)"
    HOSTNAME = "https://lawg.dev"
    API = os.getenv("LAWG_DEV_API", "https://api.lawg.dev")
    API_V1 = f"{API}/v1"

    def __init__(self, client: BaseClient) -> None:
        self.client: BaseClient = client
        self.http_client: C

    @property
    def headers(self) -> dict[str, str]:
        return {"User-Agent": self.USER_AGENT, "Authorization": self.client.token}

    @abstractmethod
    def request(self, *, path: str, method: str, body: STR_DICT | None = None) -> STR_DICT:
        """
        Make a request to the API.

        Args:
            path (str): path of request.
            method (str): HTTP method.
            body: (dict[str, Any] | None, optional): body of request. Defaults to None.

        Returns:
            dict: response body of request.
        """

    def validate(self, response: httpx.Response) -> None:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            data = response.json()
            schema = APIErrorSchema()

            try:
                schema.load(data)
            except marshmallow.ValidationError:
                raise LawgHTTPException(status_code=response.status_code)

            error_code: str = data["error"]["code"]
            error_message: str = data["error"]["message"]

            if error_code == "conflict":
                raise LawgConflict(message=error_message, status_code=response.status_code)
            elif error_code == "bad_request":
                raise LawgBadRequest(message=error_message, status_code=response.status_code)
            elif error_code == "unauthorized":
                raise LawgUnauthorized(message=error_message, status_code=response.status_code)
            elif error_code == "not_found":
                raise LawgNotFound(message=error_message, status_code=response.status_code)
            elif error_code == "internal_server_error":
                raise LawgInternalServerError(message=error_message, status_code=response.status_code)
            elif error_code == "forbidden":
                raise LawgForbidden(message=error_message, status_code=response.status_code)
            else:
                raise LawgHTTPException(message=error_message, status_code=response.status_code)
