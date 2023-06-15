import typing as t

import httpx

STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)

C = t.TypeVar("C")  # C for client
P = t.TypeVar("P")  # P for project
R = t.TypeVar("R")  # R for room
L = t.TypeVar("L")  # L for log

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
