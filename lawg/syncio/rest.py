from __future__ import annotations

import typing as t

import httpx

from lawg.base.rest import BaseRest
from lawg.typings import STR_DICT

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client


class Rest(BaseRest[httpx.Client]):
    """The syncio rest manager."""

    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.http_client = httpx.Client()
        self.http_client.headers.update(self.headers)

    def request(self, *, path: str, method: str, body: STR_DICT | None = None) -> STR_DICT:
        url, body = self.prepare_request(path=path, body=body)
        resp = self.http_client.request(method=method, url=url, json=body)
        return self.prepare_response(resp)
