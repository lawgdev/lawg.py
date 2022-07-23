from __future__ import annotations

import typing as t

import httpx

from lawg.base.rest import BaseRest

if t.TYPE_CHECKING:
    from lawg.base.basic import BaseBasicClient
    from lawg.base.rest import INPUT_DATA_TYPE


class AsyncRest(BaseRest):
    def __init__(self, client: BaseBasicClient) -> None:
        super().__init__(client=client)
        self._http_client = httpx.AsyncClient()

    async def request(self, *, method: str, **kwargs: INPUT_DATA_TYPE) -> None:
        url, payload = self.prepare_request(method=method, **kwargs)
        data = await self._http_client.request(method=method, url=url, json=payload, headers=self.headers)
        print(f"{url=} {payload=} {data=}")
