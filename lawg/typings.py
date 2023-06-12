import typing as t

STR_DICT: t.TypeAlias = "dict[str, t.Any]"

Undefined = t.NewType("Undefined", object)
UNDEFINED = Undefined(object)

T = t.TypeVar("T")

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
