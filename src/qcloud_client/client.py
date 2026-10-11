from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import httpx

from . import core
from .exceptions import QCloudError

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    from .models import Job

__all__ = ["Client"]

VALID_JOB_TYPES = frozenset({"tn-covariance", "tn-sampling", "redpitaya"})


class Client:
    """A connection to a QCloud service.

    Keep one around for as long as you need it::

        client = Client("https://qcloud.dtu.dk", api_key="...")
        job = client.submit_job("tn-covariance", {...})
        client.close()

    The client owns an :class:`httpx.Client` holding a connection pool, so
    calling :meth:`close` when you are done is good practice. Using the client
    as a context manager does that for you, including on error::

        with Client("https://qcloud.dtu.dk", api_key="...") as client:
            job = client.submit_job("tn-covariance", {...})
    """

    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = core.DEFAULT_TIMEOUT, headers: Mapping[str, str] | None = None) -> None:
        if not base_url:
            msg = "base_url is required"
            raise ValueError(msg)
        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=core.build_headers(api_key, "Bearer", headers),
            timeout=timeout,
        )

    def close(self) -> None:
        """Release the underlying connection pool."""
        self._http.close()

    def __enter__(self) -> Self:
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None) -> None:
        """Close the client on exit."""
        self.close()

    def get_jobs(self) -> list[Job]:
        """Fetch all jobs."""
        method, url = core.get_jobs()
        return core.parse_jobs(self._request_json(method, url))

    def submit_job(self, job_type: str, params: Mapping[str, Any] | None = None) -> Job:
        """Submit a new job and return it as accepted by the server.

        Args:
            job_type (str): One of "tn-covariance", "tn-sampling", "redpitaya".
            params (Mapping[str, Any] | None): Mapping of job parameters.
        """
        if job_type not in VALID_JOB_TYPES:
            raise ValueError(f"Unknown job_type {job_type!r}. It must be one of: {', '.join(sorted(VALID_JOB_TYPES))}")
        method, url, body = core.post_job(job_type, params)
        return core.parse_job(self._request_json(method, url, json=body))

    def get_job(self, job_id: str) -> Job:
        """Fetch a single job by its identifier."""
        method, url = core.get_job(job_id)
        return core.parse_job(self._request_json(method, url))

    def _request_json(self, method: str, url: str, **kwargs: Any) -> Any:
        """Send a request and return its decoded body."""
        try:
            response = self._http.request(method, url, **kwargs)
        except httpx.HTTPError as exc:
            msg = f"{method} {url} failed: {exc}"
            raise QCloudError(msg) from exc
        return core.parse_response(response)
