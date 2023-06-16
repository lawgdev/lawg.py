from __future__ import annotations

import typing as t

import httpx
from marshmallow import Schema

from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT, DataWithSchema

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client


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
