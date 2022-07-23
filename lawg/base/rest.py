from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod


if t.TYPE_CHECKING:
    from lawg.base.basic import BaseBasicClient
    import httpx

INPUT_DATA_TYPE: t.TypeAlias = "str | bool | dict[str, str] | None"


class BaseRest(ABC):
    USER_AGENT = "lawg.py; (+https://github.com/lawg/lawg.py)"
    HOSTNAME = "https://lawg.dev"
    API = "https://api.lawg.dev"
    API_V1 = f"{API}/v1"
    API_V1_LOG_BODY = f"{API_V1}/log"
    API_V1_LOG_NO_BODY = API_V1_LOG_BODY + "/{project}/{channel}/{id}"

    def __init__(self, client: BaseBasicClient) -> None:
        self._client: BaseBasicClient = client
        # self._http_client

    @property
    def headers(self) -> dict[str, str]:
        return {"User-Agent": self.USER_AGENT, "Authorization": f"Bearer {self._client.token}"}

    @abstractmethod
    def request(self, *, method: str, **kwargs: INPUT_DATA_TYPE):
        """
        Make a request to the API.
        Args:
            method (str): HTTP method.
            payload (dict | None, optional): payload of request. Defaults to None.
        Returns:
            dict: response of request.
        """
        # url, payload = self.prepare_request(method=method, **kwargs)

    def prepare_request(self, *, method: str, **kwargs: INPUT_DATA_TYPE) -> tuple[str, dict]:
        if method in {"POST", "PATCH"}:
            url, payload = self.request_with_body(**kwargs)
        else:
            url, payload = self.request_without_body(**kwargs)
        return url, payload

    def request_with_body(self, **kwargs: INPUT_DATA_TYPE) -> tuple[str, dict]:
        return self.API_V1_LOG_BODY, kwargs

    def request_without_body(self, **kwargs: str | bool | dict[str, str]) -> tuple[str, dict]:
        project = kwargs.pop("project")
        channel = kwargs.pop("channel")
        _id = kwargs.pop("id")
        url = self.API_V1_LOG_NO_BODY.format(project=project, channel=channel, id=_id)
        return url, kwargs
