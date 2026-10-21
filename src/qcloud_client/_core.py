from collections.abc import Mapping
from typing import Any
from urllib.parse import quote

import httpx

from ._version import __version__
from .exceptions import APIStatusError, QCloudError
from .models import Job

DEFAULT_BASE_URL = "https://qcloud.dtu.dk"
DEFAULT_TIMEOUT = 30
SERVICE_PREFIX = "/api/v1/service"

USER_AGENT = f"qcloud-python/{__version__} httpx/{httpx.__version__}"

_MISSING = object()


def build_headers(api_key: str | None, extra: Mapping[str, str] | None) -> dict[str, str]:
    """Assemble the default request headers, letting `extra` override them."""
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if extra:
        headers.update(extra)
    return headers


def job_path(job: Job | str) -> str:
    job_id = job.job_id if isinstance(job, Job) else job
    return f"/jobs/{quote((job_id), safe='')}"


def parse_response(response: httpx.Response) -> Any:
    """Return the decoded body, raising :class:`APIStatusError` on error statuses."""
    if response.is_error:
        raise APIStatusError(_error_message(response), status_code=response.status_code, response=response, payload=_decode(response, default=None))
    if not response.content:
        return None
    return _decode(response)


def parse_job(payload: Any) -> Job:
    """Coerce a decoded job payload into a :class:`~qcloud_client.models.Job`."""
    if not isinstance(payload, Mapping):
        msg = f"Expected a job object, got {type(payload).__name__}"
        raise QCloudError(msg)
    return Job.from_dict(payload)


def parse_jobs(payload: Any) -> list[Job]:
    """Coerce a decoded job list into :class:`~qcloud_client.models.Job` objects."""
    if isinstance(payload, Mapping):
        payload = payload.get("jobs", [])
    if not isinstance(payload, list):
        msg = f"Expected a list of jobs, got {type(payload).__name__}"
        raise QCloudError(msg)
    return [parse_job(item) for item in payload]


def _decode(response: httpx.Response, default: Any = _MISSING) -> Any:
    """Decode a JSON body, returning `default` instead of raising when given."""
    try:
        return response.json()
    except ValueError as exc:
        if default is not _MISSING:
            return default
        msg = "Response body is not valid JSON"
        raise QCloudError(msg) from exc


def _error_message(response: httpx.Response) -> str:
    """Pull the server's error message out of the body, falling back to the status text."""
    payload = _decode(response, default=None)
    if isinstance(payload, Mapping):
        for key in ("detail", "message", "error"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
    return response.reason_phrase or "request failed"
