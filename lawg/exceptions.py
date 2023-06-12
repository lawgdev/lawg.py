class LawgException(Exception):
    """Base exception for all lawg exceptions."""


class LawgHTTPException(LawgException):
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


class LawgConflict(LawgHTTPException):
    """Exception raised when a request is made that conflicts with another resource."""


class LawgBadRequest(LawgHTTPException):
    """Exception raised when a bad request is made."""


class LawgUnauthorized(LawgHTTPException):
    """Exception raised when an unauthorized request is made."""


class LawgNotFound(LawgHTTPException):
    """Exception raised when a request is made to a non-existent resource."""


class LawgInternalServerError(LawgHTTPException):
    """Exception raised when an internal server error occurs."""


class LawgForbidden(LawgHTTPException):
    """Exception raised when a forbidden request is made."""
