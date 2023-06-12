from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod


if t.TYPE_CHECKING:
    import httpx
    from lawg.base.client import BaseClient
    from lawg.typings import STR_DICT


class BaseRest(ABC):
    USER_AGENT = "lawg.py; (+https://github.com/lawg/lawg.py)"
    HOSTNAME = "https://lawg.dev"
    API = "https://api.lawg.dev"
    API_V1 = f"{API}/v1"

    def __init__(self, client: BaseClient) -> None:
        self._client: BaseClient = client

    @property
    def headers(self) -> dict[str, str]:
        return {"User-Agent": self.USER_AGENT, "Authorization": f"Bearer {self._client.token}"}

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
