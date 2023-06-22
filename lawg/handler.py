from __future__ import annotations
from types import MappingProxyType

import typing as t
import logging
from lawg.exceptions import LawgEventUndefinedError

if t.TYPE_CHECKING:
    from lawg.typings import STR_DICT
    from logging import _FormatStyle, _Level
    from collections.abc import Mapping

from lawg.schemas import WebsocketEvent


class Event(t.TypedDict):
    title: t.NotRequired[str]
    description: t.NotRequired[str]
    emoji: t.NotRequired[str]


class LogRecord(logging.LogRecord):
    event: str | None
    title: str | None
    description: str | None
    emoji: str | None


class Formatter(logging.Formatter):
    EMOJI_DEFAULT = "📝"
    EMOJI_MAP: MappingProxyType[int, str] = MappingProxyType({
        logging.DEBUG: "🔍",
        logging.INFO: EMOJI_DEFAULT,
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🚨",
    })

    def __init__(
        self,
        *,
        handler: "Handler",
        fmt: str | None = None,
        datefmt: str | None = None,
        style: _FormatStyle = "%",
        validate: bool = True,
        defaults: Mapping[str, t.Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self.handler = handler

    def prepare(self, record: LogRecord) -> LogRecord:
        record_dict = record.__dict__
        for attr in LogRecord.__annotations__:
            record_dict[attr] = record_dict.get(attr, None)
        return record

    def format(self, record: LogRecord) -> STR_DICT:
        record = self.prepare(record)

        schema = WebsocketEvent()
        data: STR_DICT = schema.load(
            {
                "e": "LOG_CREATE",
                "d": {
                    "project_namespace": self.handler.namespace,
                    "feed_name": self.handler.feed_name,
                    "log": self.format_log(record),
                },
            }
        )  # type: ignore
        return data

    def format_log(self, record: LogRecord) -> STR_DICT:
        """
        Format the lawg log request body.
        """
        title: str | None = None
        description: str | None = None
        emoji: str | None = None

        if record.event:
            event = self.handler.events.get(record.event)
            if not event:
                raise LawgEventUndefinedError(record.event)
            title = event.get("title")
            description = event.get("description")
            emoji = event.get("emoji")

        if record.title:
            title = record.title
        elif not title:
            title = f"{record.name} ({record.levelname})"

        if record.description:
            description = record.description
        elif not description:
            description = record.getMessage()

        if record.emoji:
            emoji = record.emoji
        elif not emoji:
            emoji = self.EMOJI_MAP.get(record.levelno, self.EMOJI_DEFAULT)

        return {
            "title": title,
            "description": description,
            "emoji": emoji,
        }


class Handler(logging.Handler):
    __slots__ = ("namespace", "feed_name", "events", "formatter")

    def __init__(self, *, namespace: str, feed_name: str, events: dict[str, Event], level: _Level = 0) -> None:
        super().__init__(level)
        self.namespace = namespace
        self.feed_name = feed_name
        self.events = events
        self.formatter: Formatter = Formatter(handler=self)

    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record.
        """

        formatted = self.format(record)
        print(formatted)

        # TODO(<hexiro>): implement emitting to websocket functionality
        # once websocket has been made


if __name__ == "__main__":
    from rich import print

    logger = logging.getLogger("handler-test")
    logger.setLevel(logging.DEBUG)

    handler = Handler(
        namespace="lawg-py",
        feed_name="handler-test",
        events={
            "screen-resize": {"title": "Screen Resize", "emoji": "🖥️"},
            "user-login": {"title": "User Login", "emoji": "👤"},
            "user-login-failed": {"title": "User Login Failed", "emoji": "❌"},
            "api-call-failed": {"title": "API Call Failed", "emoji": "🔌"},
            "database-connection": {"title": "Database Connection", "emoji": "💾"},
        },
    )
    logger.addHandler(handler)

    logger.debug("Screen resized to 860x420 pixels", extra={"event": "screen-resize"})
    logger.info("User logged in", extra={"event": "user-login"})
    logger.warning("User tried to login with incorrect password", extra={"event": "user-login-failed"})
    logger.error("API call timed out", extra={"event": "api-call-failed"})
    logger.critical("Database connection failed", extra={"event": "database-connection"})
