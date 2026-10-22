import httpx


class QCloudError(Exception):
    """Base exception for every error raised by this package."""


class APIStatusError(QCloudError):
    """An error response from the API (any 4xx/5xx status)."""

    def __init__(self, message: str, *, status_code: int, response: httpx.Response | None = None, payload: object = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.payload = payload

    def __str__(self) -> str:
        """Render as ``[HTTP <status>] <message>``."""
        return f"[HTTP {self.status_code}] {self.message}"


class JobTimeoutError(QCloudError):
    """A job did not reach a terminal state within the allowed time."""


class ValidationError(QCloudError, ValueError):
    """A job parameter was rejected locally."""
