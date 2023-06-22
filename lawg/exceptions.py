class LawgError(Exception):
    """Base exception for all lawg exceptions."""

    message = "An error occurred."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.message)


class LawgHTTPError(LawgError):
    """Base exception for all lawg HTTP exceptions."""

    message = "An HTTP error occurred."

    def __init__(
        self,
        *,
        status_code: int,
        message: str | None = None,
    ) -> None:
        super().__init__(message or self.message)
        self.status_code: int = status_code


class LawgConflictError(LawgHTTPError):
    """Exception raised when a request is made that conflicts with another resource."""


class LawgBadRequestError(LawgHTTPError):
    """Exception raised when a bad request is made."""


class LawgUnauthorizedError(LawgHTTPError):
    """Exception raised when an unauthorized request is made."""


class LawgNotFoundError(LawgHTTPError):
    """Exception raised when a request is made to a non-existent resource."""


class LawgInternalServerError(LawgHTTPError):
    """Exception raised when an internal server error occurs."""


class LawgForbiddenError(LawgHTTPError):
    """Exception raised when a forbidden request is made."""


class LawgAlreadyDeletedError(LawgError):
    """Exception raised when a log is already deleted and the user tries again."""

    message = "The {type} has already been deleted."

    def __init__(self, type: str = "log") -> None:
        super().__init__(self.message.format(type=type))


class LawgEmptyBodyError(LawgError):
    """Exception raised when a request body is empty."""

    message = "The request body is empty."


class LawgEventUndefinedError(LawgError):
    """Exception raised when an event isn't defined."""

    message = "The event {event} is not defined."

    def __init__(self, event: str) -> None:
        super().__init__(self.message.format(event=event))
