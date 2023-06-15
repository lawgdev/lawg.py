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
from lawg.typings import H, UNDEFINED

if t.TYPE_CHECKING:
    from lawg.base.client import BaseClient
    from lawg.typings import STR_DICT


class BaseRest(ABC, t.Generic[H]):
    USER_AGENT = "lawg.py; (+https://github.com/lawg/lawg.py)"
    HOSTNAME = "https://lawg.dev"
    API = os.getenv("LAWG_DEV_API", "https://api.lawg.dev")
    API_V1 = f"{API}/v1"

    def __init__(self, client: BaseClient) -> None:
        self.client: BaseClient = client
        self.http_client: H

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

    def prepare_body(self, body: STR_DICT) -> STR_DICT:
        """
        Finalize the body of a request by removing undefined values.

        Args:
            body (dict[str, Any]): body of request.
        """

        new_body: STR_DICT = {}

        for key, value in body.items():
            if value is UNDEFINED:
                continue

            new_body[key] = value

        return new_body

    def prepare_request(self, *, path: str, body: STR_DICT | None = None) -> tuple[str, STR_DICT | None]:
        """
        Prepare a request to the API by calculating the url and finalizing the body.

        Args:
            path (str): path of request.
            body (dict[str, Any] | None, optional): body of request. Defaults to None.

        Returns:
            tuple[str, dict[str, Any] | None]: url and body of request.
        """

        if body:
            body = self.prepare_body(body)

        url = f"{self.API_V1}/{path}"

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
                # error follows httpx error format, meaning it never got a proper json reply from api
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

    def prepare_response(self, response: httpx.Response) -> STR_DICT:
        """
        Prepare a response from the API by validating it and returning the body.
        """
        self.validate_response(response)

        if response.status_code == 204:
            return {}

        return response.json()
