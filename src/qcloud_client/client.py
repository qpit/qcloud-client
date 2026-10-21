import time
from collections.abc import Mapping
from types import TracebackType
from typing import Any, Self

import httpx

from ._core import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, SERVICE_PREFIX, build_headers, job_path, parse_job, parse_jobs, parse_response
from .exceptions import JobTimeoutError, QCloudError
from .models import Job, JobSpec


class QCloudClient:
    """Synchronous connection to the QCloud service.

    Use the client as a context manager so the connection pool is closed for you::

        with QCloudClient(api_key="...") as client:
            cov = TNCovariance(nmodes=64, r_db=8, loss=0.5, basis="pi4")
            job = client.submit(cov)

            result = client.wait(job, timeout=300).result
            print(result)

    Or keep one around for as long as you need it::

        client = QCloudClient(api_key="...")

        cov = TNCovariance(nmodes=64, r_db=8, loss=0.5, basis="pi4")
        job = client.submit(cov)

        result = client.wait(job, timeout=300).result
        print(result)

        client.close()
    """

    def __init__(self, api_key: str | None = None, base_url: str = DEFAULT_BASE_URL, *, timeout: float = DEFAULT_TIMEOUT, headers: Mapping[str, str] | None = None) -> None:
        self._http = httpx.Client(
            base_url=base_url.rstrip("/") + SERVICE_PREFIX,
            headers=build_headers(api_key, headers),
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

    def submit(self, spec: JobSpec) -> Job:
        if not isinstance(spec, JobSpec):
            msg = f"submit() needs a job spec such as TNCovariance(...), got {type(spec).__name__}"
            raise TypeError(msg)
        payload = {"job_type": spec.job_type, "params": spec.to_params()}
        return parse_job(self._request("POST", "/jobs", json=payload))

    def get(self, job: Job | str) -> Job:
        """Fetch the current state of a job."""
        return parse_job(self._request("GET", job_path(job)))

    def list_jobs(self) -> list[Job]:
        """Fetch all of your jobs."""
        return parse_jobs(self._request("GET", "/jobs"))

    def wait(self, job: Job | str, *, timeout: float | None, poll_interval: float = 2.0, max_poll_interval: float = 30.0) -> Job:
        deadline = None if timeout is None else time.monotonic() + timeout
        delay = poll_interval
        while True:
            current = self.get(job)
            if current.finished:
                return current
            pause = delay
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    msg = f"Job {current.job_id} did not finish within {timeout}s (status: {current.status})"
                    raise JobTimeoutError(msg)
                pause = min(pause, remaining)
            time.sleep(pause)
            delay = min(delay * 1.5, max_poll_interval)
            job = current

    def update(self, job: Job | str, **params: Any) -> None:
        """Change parameters of a pending job."""
        if not params:
            msg = "update() needs at least one parameter to change"
            raise ValueError(msg)
        self._request("PATCH", job_path(job), json={"params": params})

    def delete(self, job: Job | str) -> None:
        """Delete a pending job."""
        self._request("DELETE", job_path(job))

    def _request(self, method: str, path: str, *, json: Any = None) -> Any:
        """Send a request and return its decoded body."""
        try:
            response = self._http.request(method, path, json=json)
        except httpx.HTTPError as exc:
            msg = f"{method} {path} failed: {exc}"
            raise QCloudError(msg) from exc
        return parse_response(response)
