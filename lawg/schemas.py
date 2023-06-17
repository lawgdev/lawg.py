from __future__ import annotations

import functools
from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate
from marshmallow_union import Union


class PikaId(validate.Validator):
    """
    Validator which succeeds if the ``value`` passed to it is
    a valid pika id with the given prefix.

    Args:
        prefix (str): The prefix to check for.
    """

    default_message = "Pika id must start with {other}."

    def __init__(self, prefix: str):
        self.prefix = prefix

    def _repr_args(self) -> str:
        return f"prefix={self.prefix!r}"

    def _format_error(self, value: str) -> str:
        return self.default_message.format(input=value, other=self.prefix)

    def __call__(self, value: str) -> str:
        if not value.startswith(f"{self.prefix}_"):
            raise ValidationError(self._format_error(value))
        return value


# TODO: edit these schemas to split slugs and req.body

# ----- REQUEST VALIDATION SCHEMAS ----- #

# unfortunately marshmallow doesn't have a fields.Emoji() comparable to zod's string().emoji() :(
# another thing is that JavaScript's emojis have variable length whereas (afaik) Python treats them all as a single character
EmojiSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))


ColorSchema = functools.partial(
    Union, fields=[fields.Integer(), fields.String(validate=validate.Length(min=1, max=16))]
)

# --- PROJECTS --- #

# github.com/lawgdev/api/blob/main/src/utils/zodSchemas.ts
ProjectNameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))
ProjectNamespaceSchema = functools.partial(
    fields.Str, validate=[validate.Length(min=1, max=32), validate.Regexp(r"^[a-z0-9_-]+$")]
)
ProjectUsernameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))


class ProjectSlugSchema(Schema):
    """Used for getting and deleting projects and accepting invites."""

    namespace = ProjectNamespaceSchema(required=True)


class ProjectBodySchema(Schema):
    """Used for creating and patching projects."""

    name = ProjectNameSchema(required=True)
    namespace = ProjectNamespaceSchema(required=True)


class ProjectUpgradeSchema(Schema):
    """TODO"""


class ProjectMemberSchema(Schema):
    """Used for both adding and removing members."""

    namespace = ProjectNamespaceSchema(required=True)
    username = ProjectUsernameSchema(required=True)


# --- FEEDS --- #

FeedNameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=24))
FeedDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=128))


class FeedSlugSchema(Schema):
    """Used for creating feeds."""

    namespace = ProjectNamespaceSchema(required=True)


class FeedWithNameSlugSchema(Schema):
    """Used for patching, and deleting feeds."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


class FeedCreateBodySchema(Schema):
    name = FeedNameSchema(required=True)
    description = FeedDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)


class FeedPatchBodySchema(Schema):
    name = FeedNameSchema(required=False, allow_none=True)
    description = FeedDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)


# --- LOGS --- #

LogTitleSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))
LogDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=4096))


class LogSlugSchema(Schema):
    """
    Used for creating and getting multiple logs.
    """

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


class LogWithIdSlugSchema(Schema):
    """
    Used for getting, patching, and deleting logs.
    """

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)
    log_id = fields.Str(required=True, validate=PikaId("log"))


class LogCreateBodySchema(Schema):
    title = LogTitleSchema(required=True)
    description = LogDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    color = ColorSchema(required=False, allow_none=True)


class LogGetMultipleBodySchema(Schema):
    limit = fields.Integer(required=False, default=25, validate=validate.Range(min=1, max=100))
    offset = fields.Integer(required=False, default=0, validate=validate.Range(min=0))


class LogPatchBodySchema(Schema):
    title = LogTitleSchema(required=False)
    description = LogDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    color = ColorSchema(required=False, allow_none=True)


# ----- API VALIDATION SCHEMAS ----- #


class ErrorSchema(Schema):
    code = fields.Str(required=True)
    message = fields.Str(required=True)


class APIErrorSchema(Schema):
    success = fields.Boolean(required=True, validate=validate.Equal(False))
    error = fields.Nested(ErrorSchema())


class APISuccessSchema(Schema):
    success = fields.Boolean(required=True, validate=validate.Equal(True))
    data = fields.Dict(required=True)


# ----- API RESPONSE SCHEMAS ----- #


class FeedSchema(Schema):
    id = fields.Str(required=True, validate=PikaId("feed"))
    project_id = fields.Str(required=True, validate=PikaId("project"))
    name = FeedNameSchema(required=True)
    description = FeedDescriptionSchema(required=True, allow_none=True)
    emoji = EmojiSchema(required=True, allow_none=True)

    class Meta:
        unknown = EXCLUDE


class MemberSchema(Schema):
    id = fields.Str(required=True, validate=PikaId("user"))
    username = fields.Str(required=True)
    icon = fields.Str(required=True, allow_none=True)

    class Meta:
        unknown = EXCLUDE


class ProjectSchema(Schema):
    id = fields.Str(required=True, validate=PikaId("project"))
    namespace = ProjectNamespaceSchema(required=True)
    name = ProjectNameSchema(required=True)
    flags = fields.Int(required=True)
    icon = fields.Str(required=True, allow_none=True)
    feeds = fields.List(fields.Nested(FeedSchema()), required=True)
    members = fields.List(fields.Nested(MemberSchema()), required=True)

    class Meta:
        unknown = EXCLUDE


class LogSchema(Schema):
    id = fields.Str(required=True, validate=PikaId("log"))
    project_id = fields.Str(required=True, validate=PikaId("project"))
    feed_id = fields.Str(required=True, validate=PikaId("feed"))
    title = LogTitleSchema(required=True)
    description = LogDescriptionSchema(required=True, allow_none=True)
    emoji = EmojiSchema(required=True, allow_none=True)
    color = ColorSchema(required=True, allow_none=True)

    class Meta:
        unknown = EXCLUDE
