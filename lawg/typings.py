from __future__ import annotations

import typing as t

import httpx

if t.TYPE_CHECKING:
    from marshmallow import Schema
    from lawg.syncio.client import Client
    from lawg.asyncio.client import AsyncClient
    from lawg.syncio.rest import Rest
    from lawg.asyncio.rest import AsyncRest
    from lawg.syncio.log import Log
    from lawg.asyncio.log import AsyncLog
    from lawg.syncio.insight import Insight
    from lawg.asyncio.insight import AsyncInsight


STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)


C = t.TypeVar("C", "Client", "AsyncClient")
R = t.TypeVar("R", "Rest", "AsyncRest")
H = t.TypeVar("H", httpx.Client, httpx.AsyncClient)
L = t.TypeVar("L", "Log", "AsyncLog")
I = t.TypeVar("I", "Insight", "AsyncInsight")


ErrorCode: t.TypeAlias = (
    str
    | t.Literal[
        "conflict",
        "bad_request",
        "unauthorized",
        "not_found",
        "internal_server_error",
        "forbidden",
    ]
)


class DataWithSchema(t.NamedTuple):
    data: STR_DICT
    schema: Schema
