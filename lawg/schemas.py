import functools
import typing as t
from marshmallow import Schema, ValidationError, fields, validate
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


class ProjectCreateSchema(Schema):
    name = ProjectNameSchema(required=True)
    namespace = ProjectNamespaceSchema(required=True)


class ProjectGetSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)


class ProjectPatchSchema(Schema):
    name = ProjectNameSchema(required=True)
    namespace = ProjectNamespaceSchema(required=True)


class ProjectDeleteSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)


class ProjectUpgradeSchema(Schema):
    # TODO - WAITING ON CODY
    ...


class ProjectInviteMemberSchema(Schema):
    username = ProjectUsernameSchema(required=True)
    namespace = ProjectNamespaceSchema(required=True)


class ProjectRemoveMemberSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    username = ProjectUsernameSchema(required=True)


class ProjectAcceptInviteSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)


# --- ROOMS --- #

RoomNameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=24))
RoomDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=128))


class RoomCreateSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    name = RoomNameSchema(required=True)
    description = RoomDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)


class RoomPatchSchema(Schema):
    name = RoomNameSchema(required=False, allow_none=True)
    description = RoomDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)

    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)


class RoomDeleteSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)


# --- LOGS --- #

LogTitleSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))
LogDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=4096))


class LogCreateSchema:
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)
    title = LogTitleSchema(required=True)
    description = LogDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    color = ColorSchema(required=False, allow_none=True)


class LogGetSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)
    log_id = fields.Str(required=True, validate=PikaId("log"))


class LogGetMultipleSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)
    limit = fields.Integer(required=False, default=25, validate=validate.Range(min=1, max=100))
    offset = fields.Integer(required=False, default=0, validate=validate.Range(min=0))


class LogPatchSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)
    log_id = fields.Str(required=True, validate=PikaId("log"))
    title = LogTitleSchema(required=False)
    description = LogDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    color = ColorSchema(required=False, allow_none=True)


class LogDeleteSchema(Schema):
    namespace = ProjectNamespaceSchema(required=True)
    room_name = RoomNameSchema(required=True)
    log_id = fields.Str(required=True, validate=PikaId("log"))
