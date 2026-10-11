from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import httpx

__all__ = [
    "APIStatusError",
    "QCloudError",
]

class QCloudError(Exception):
    """Base exception for every error raised by this package."""


class APIStatusError(QCloudError):
    """An error response from the API (any 4xx/5xx status)."""

    def __init__(self, message: str, *, status_code: int, response: httpx.Response | None = None, payload: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.payload = payload

    def __str__(self) -> str:
        """Render as ``[HTTP <status>] <message>``."""
        return f"[HTTP {self.status_code}] {self.message}"
