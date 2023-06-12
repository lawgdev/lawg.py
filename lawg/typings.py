import typing as t

STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)

C = t.TypeVar("C")
P = t.TypeVar("P")
R = t.TypeVar("R")
L = t.TypeVar("L")

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
