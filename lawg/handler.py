from __future__ import annotations

import typing as t
import logging

if t.TYPE_CHECKING:
    from logging import _FormatStyle, _Level
    from collections.abc import Mapping

from lawg.schemas import WebsocketEvent
from lawg.typings import STR_DICT


class LogRecord(logging.LogRecord):
    title: str | None
    description: str | None
    emoji: str | None
    color: str | None


class Formatter(logging.Formatter):
    EMOJI_DEFAULT = "📝"
    COLOR_DEFAULT = "#57F287"

    EMOJI_MAP: dict[int, str] = {
        logging.DEBUG: "🔍",
        logging.INFO: EMOJI_DEFAULT,
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🚨",
    }

    COLOR_MAP = {
        logging.DEBUG: "#676765",  # gray
        logging.INFO: COLOR_DEFAULT,  # green
        logging.WARNING: "#F3E702",  # yellow
        logging.ERROR: "#E31937",  # red
        logging.CRITICAL: "#8B0000",  # dark red
    }

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

    @staticmethod
    def prepare(record: LogRecord) -> LogRecord:
        record_dict = record.__dict__
        attrs = ("title", "description", "emoji", "color")
        for attr in attrs:
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

        title = record.title or f"{record.name} ({record.levelname})"
        description = record.description or record.getMessage()
        emoji = record.emoji or self.EMOJI_MAP.get(record.levelno, self.EMOJI_DEFAULT)
        color = record.color or self.COLOR_MAP.get(record.levelno, self.COLOR_DEFAULT)

        return {
            "title": title,
            "description": description,
            "emoji": emoji,
            "color": color,
        }


class Handler(logging.Handler):
    __slots__ = ("level", "namespace", "feed_name")

    def __init__(self, *, namespace: str, feed_name: str, level: _Level = 0) -> None:
        super().__init__(level)
        self.namespace = namespace
        self.feed_name = feed_name
        self.formatter: Formatter = Formatter(handler=self)

    def emit(self, record: LogRecord) -> None:
        """
        Emit a log record.
        """

        formatted = self.format(record)
        print(formatted)

        # TODO: implement emitting to websocket functionality
        # once websocket has been made


if __name__ == "__main__":
    from rich import print

    logger = logging.getLogger("handler-test")
    logger.setLevel(logging.DEBUG)

    handler = Handler(namespace="lawg-py", feed_name="handler-test")
    logger.addHandler(handler)

    logger.debug("Screen resized to 860x420 pixels", extra={"title": "Screen Resize", "emoji": "🖥️"})
    logger.info("User logged in", extra={"title": "User Login", "emoji": "👤"})
    logger.warning("User tried to login with incorrect password", extra={"title": "User Login", "emoji": "👤"})
    logger.error("API call timed out", extra={"title": "API Call Failed", "emoji": "🔌"})
    logger.critical("Database connection failed", extra={"title": "Database Connection", "emoji": "💾"})
