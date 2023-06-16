from __future__ import annotations

import typing as t

import httpx

if t.TYPE_CHECKING:
    import marshmallow

STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)

C = t.TypeVar("C")  # C for client
P = t.TypeVar("P")  # P for project
F = t.TypeVar("F")  # F for feed
L = t.TypeVar("L")  # L for log
R = t.TypeVar("R")  # R for rest

H = t.TypeVar("H", httpx.Client, httpx.AsyncClient)  # H for httpx client


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
    schema: marshmallow.Schema
