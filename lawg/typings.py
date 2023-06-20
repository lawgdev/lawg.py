from __future__ import annotations

import typing as t

import httpx

if t.TYPE_CHECKING:
    from marshmallow import Schema

STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)


P = t.TypeVar("P")  # P for project
PM = t.TypeVar("PM")  # PM for project manager

F = t.TypeVar("F")  # F for feed
FM = t.TypeVar("FM")  # FM for feed manager

L = t.TypeVar("L")  # L for log
LM = t.TypeVar("LM")  # LM for log manager

I = t.TypeVar("I")  # I for insight
C = t.TypeVar("C")  # C for client
R = t.TypeVar("R")  # R for rest
M = t.TypeVar("M")  # M for member
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
    schema: Schema
