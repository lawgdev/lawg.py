"""lawg.py custom type definitions."""

from __future__ import annotations

import typing as t

import httpx

if t.TYPE_CHECKING:
    from marshmallow import Schema
    from lawg.syncio.client import Client
    from lawg.asyncio.client import AsyncClient
    from lawg.syncio.feed import Feed
    from lawg.asyncio.feed import AsyncFeed
    from lawg.syncio.rest import Rest
    from lawg.asyncio.rest import AsyncRest
    from lawg.syncio.event import Event
    from lawg.asyncio.event import AsyncEvent
    from lawg.syncio.insight import Insight
    from lawg.asyncio.insight import AsyncInsight


STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)


C = t.TypeVar("C", "Client", "AsyncClient")
F = t.TypeVar("F", "Feed", "AsyncFeed")
R = t.TypeVar("R", "Rest", "AsyncRest")
H = t.TypeVar("H", httpx.Client, httpx.AsyncClient)
E = t.TypeVar("E", "Event", "AsyncEvent")
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
    """Data with schema."""

    data: STR_DICT
    schema: Schema
