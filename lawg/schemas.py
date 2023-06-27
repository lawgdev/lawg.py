"""lawg.py schemas. Based on lawg API zod schemas."""

from __future__ import annotations

import typing as t

import functools
from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate
from marshmallow_union import Union


class PikaId(fields.Field):
    """A pika id field."""

    default_error_messages = {
        "blank": "Field may not be blank.",
        "invalid_id": "Not a valid pika id.",
        "invalid_type": "Not a valid string.",
    }

    __slots__ = ("prefix",)

    def __init__(self, *, prefix: str, **kwargs) -> None:
        """Pika id field initializer.

        Args:
            prefix (str): The prefix to check for.
        """
        super().__init__(**kwargs)

        self.prefix = prefix

    def _validate(self, value: str | None | t.Any) -> None:
        """Validate a pika id."""
        if not value:
            raise self.make_error("blank")
        if not hasattr(value, "startswith"):
            raise self.make_error("invalid_type")
        if not value.startswith(f"{self.prefix}_"):
            raise self.make_error("invalid_id")

    def _serialize(self, value: str, attr, obj, **kwargs) -> str:
        """Serialize a pika id."""
        self._validate(value)
        return value

    def _deserialize(self, value: str, attr, data, **kwargs) -> str:
        """Deserialize a pika id."""
        self._validate(value)
        return value


# ----- REQUEST VALIDATION SCHEMAS ----- #
# github.com/lawgdev/api/blob/main/src/utils/zodSchemas.ts


# --- PROJECTS --- #
ProjectNamespaceSchema = functools.partial(
    fields.Str, validate=[validate.Length(min=1, max=32), validate.Regexp(r"^[a-z0-9_-]+$")]
)
ProjectNameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))

# --- USER --- #
UsernameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))

# --- FEEDS --- #
FeedNameSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=24))
FeedDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=128))

# --- EVENTS --- #
EventTitleSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))
EventDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=4096))
EventTagsSchema = functools.partial(
    fields.Dict,
    keys=fields.Str(validate=validate.Length(min=1, max=175)),
    values=Union([fields.Str(), fields.Int(), fields.Float(), fields.Bool()]),
)

# --- INSIGHTS --- #

InsightTitleSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))
InsightDescriptionSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=128))


# --- GENERAL --- #
# unfortunately marshmallow doesn't have a fields.Emoji() comparable to zod's string().emoji() :(
# additionally, JavaScript's emojis have variable length whereas (afaik) Python treats them all as a single character
EmojiSchema = functools.partial(fields.Str, validate=validate.Length(min=1, max=32))

# --- PROJECT SCHEMAS --- #


class ProjectAcceptInvitationSlugSchema(Schema):
    """Accept project invite slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class ProjectCreateBodySchema(Schema):
    """Create project body validation schema."""

    name = ProjectNameSchema(required=True)
    namespace = ProjectNamespaceSchema(required=True)


class ProjectDeleteSlugSchema(Schema):
    """Delete project slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class ProjectGetSlugSchema(Schema):
    """Get project slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class ProjectInviteMemberSlugSchema(Schema):
    """Invite member to project slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    username = UsernameSchema(required=True)


class ProjectPatchBodySchema(Schema):
    """Patch project body validation schema."""

    name = ProjectNameSchema(required=True)


class ProjectPatchSlugSchema(Schema):
    """Patch project slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class ProjectRemoveMemberSlugSchema(Schema):
    """Remove member from project slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    username = UsernameSchema(required=True)


class ProjectRevokeInvitationSlugSchema(Schema):
    """Revoke project invite slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    username = UsernameSchema(required=True)


# --- FEED SCHEMAS --- #


class FeedCreateBodySchema(Schema):
    """Feed create body validation schema."""

    name = FeedNameSchema(required=True)
    description = FeedDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)


class FeedCreateSlugSchema(Schema):
    """Feed create slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class FeedDeleteSlugSchema(Schema):
    """Feed delete slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


class FeedPatchBodySchema(Schema):
    """Feed patch body validation schema."""

    name = FeedNameSchema(required=False, allow_none=True)
    description = FeedDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)


class FeedPatchSlugSchema(Schema):
    """Feed patch slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


class FeedReadSlugSchema(Schema):
    """Feed read slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


# --- EVENTS --- #


class EventCreateSlugSchema(Schema):
    """Event create slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed = FeedNameSchema(required=True)


class EventCreateBodySchema(Schema):
    """Event create body validation schema."""

    title = EventTitleSchema(required=True)
    description = EventDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    tags = EventTagsSchema(required=False, allow_none=True)
    timestamp = fields.DateTime(required=False, allow_none=True)
    notify = fields.Boolean(required=False, allow_none=True)


class EventDeleteSlugSchema(Schema):
    """Event delete slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed = FeedNameSchema(required=True)
    event_id = PikaId(prefix="event", required=True)


class EventDeleteMultipleBodySchema(Schema):
    """Event delete multiple body validation schema."""

    event_ids = fields.List(PikaId(prefix="event"), required=False, allow_none=True)
    deleteAll = fields.Boolean(required=False, allow_none=True)


class EventDeleteMultipleSlugSchema(Schema):
    """Event delete multiple slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)
    event_id = PikaId(prefix="event", required=True)


class EventGetSlugSchema(Schema):
    """Event get slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)
    event_id = PikaId(prefix="event", required=True)


class EventGetMultipleBodySchema(Schema):
    """Event get multiple body validation schema."""

    limit = fields.Integer(required=False, default=25, validate=validate.Range(min=1, max=100))
    offset = fields.Integer(required=False, default=0, validate=validate.Range(min=0))


class EventGetMultipleSlugSchema(Schema):
    """Event get multiple slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)


class EventPatchBodySchema(Schema):
    """Event patch body validation schema."""

    title = EventTitleSchema(required=False, allow_none=True)
    description = EventDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    tags = EventTagsSchema(required=False, allow_none=True)
    timestamp = fields.DateTime(required=False, allow_none=True)


class EventPatchSlugSchema(Schema):
    """Event patch slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    feed_name = FeedNameSchema(required=True)
    event_id = PikaId(prefix="event", required=True)


# --- INSIGHTS --- #


class InsightCreateBodySchema(Schema):
    """Insight create body validation schema."""

    title = InsightTitleSchema(required=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    value = fields.Float(required=False, allow_none=True)


class InsightCreateSlugSchema(Schema):
    """Insight create slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class InsightDeleteSlugSchema(Schema):
    """Insight delete slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    insight_id = PikaId(prefix="insight", required=True)


class InsightGetSlugSchema(Schema):
    """Insight get slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    insight_id = PikaId(prefix="insight", required=True)


class InsightGetMultipleBodySchema(Schema):
    """Insight get multiple body validation schema."""

    namespace = ProjectNamespaceSchema(required=True)


class InsightValueSchema(Schema):
    """Insight value validation schema."""

    set = fields.Float(required=False, allow_none=True)
    increment = fields.Float(required=False, allow_none=True)


class InsightPatchBodySchema(Schema):
    """Insight patch body validation schema."""

    title = InsightTitleSchema(required=False, allow_none=True)
    description = InsightDescriptionSchema(required=False, allow_none=True)
    emoji = EmojiSchema(required=False, allow_none=True)
    value = fields.Nested(InsightValueSchema, required=False, allow_none=True)


class InsightPatchSlugSchema(Schema):
    """Insight patch slug validation schema."""

    namespace = ProjectNamespaceSchema(required=True)
    insight_id = PikaId(prefix="insight", required=True)


# ----- API VALIDATION SCHEMAS ----- #


class ErrorSchema(Schema):
    """Error validation schema."""

    code = fields.Str(required=True)
    message = fields.Str(required=True)


class APIErrorSchema(Schema):
    """API error validation schema."""

    success = fields.Boolean(required=True, validate=validate.Equal(False))
    error = fields.Nested(ErrorSchema())


class APISuccessSchema(Schema):
    """API success validation schema."""

    success = fields.Boolean(required=True, validate=validate.Equal(True))
    data = fields.Dict(required=True)


# ----- API RESPONSE SCHEMAS ----- #


class FeedSchema(Schema):
    """Feed validation schema."""

    id = PikaId(prefix="feed", required=True)
    project_id = PikaId(prefix="project", required=True)
    name = FeedNameSchema(required=True)
    description = FeedDescriptionSchema(required=True, allow_none=True)
    emoji = EmojiSchema(required=True, allow_none=True)

    class Meta:
        """Marshmallow schema meta options."""

        unknown = EXCLUDE


class MemberSchema(Schema):
    """Member validation schema."""

    id = PikaId(prefix="user", required=True)
    username = fields.Str(required=True)
    icon = fields.Str(required=True, allow_none=True)

    class Meta:
        """Marshmallow schema meta options."""

        unknown = EXCLUDE


class ProjectSchema(Schema):
    """Project validation schema."""

    id = PikaId(prefix="project", required=True)
    namespace = ProjectNamespaceSchema(required=True)
    name = ProjectNameSchema(required=True)
    flags = fields.Int(required=True)
    icon = fields.Str(required=True, allow_none=True)
    feeds = fields.List(fields.Nested(FeedSchema()), required=True)
    members = fields.List(fields.Nested(MemberSchema()), required=True)

    class Meta:
        """Marshmallow schema meta options."""

        unknown = EXCLUDE


class EventSchema(Schema):
    """Event validation schema."""

    id = PikaId(prefix="event", required=True)
    project_id = PikaId(prefix="project", required=True)
    feed_id = PikaId(prefix="feed", required=True)
    title = EventTitleSchema(required=True)
    description = EventDescriptionSchema(required=True, allow_none=True)
    emoji = EmojiSchema(required=True, allow_none=True)

    class Meta:
        """Marshmallow schema meta options."""

        unknown = EXCLUDE


class InsightSchema(Schema):
    """Insight validation schema."""

    id = PikaId(prefix="insight", required=True)
    title = InsightTitleSchema(required=True)
    description = InsightDescriptionSchema(required=True, allow_none=True)
    value = fields.Float(required=True)
    emoji = EmojiSchema(required=True, allow_none=True)
    updated_at = fields.DateTime(required=True, allow_none=True)
    created_at = fields.DateTime(required=True)

    class Meta:
        """Marshmallow schema meta options."""

        unknown = EXCLUDE


# --- WEBSOCKET SCHEMAS --- #


class WebsocketEventData(Schema):
    """Websocket event data validation schema."""

    project = fields.Str(required=True)
    feed = fields.Str(required=True)
    event = fields.Nested(EventCreateBodySchema(), required=True)


class WebsocketEvent(Schema):
    """Websocket event validation schema."""

    # event
    e = fields.Str(required=True, validate=validate.OneOf(("EVENT_CREATE", "EVENT_DELETE", "EVENT_UPDATE")))
    # data
    d = fields.Nested(WebsocketEventData(), required=True)
