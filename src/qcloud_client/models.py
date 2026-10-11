from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = [
    "Job",
    "JobStatus",
]


class JobStatus:
    """Terminal job states reported by the API."""

    COMPLETED: Final = "completed"
    FAILED: Final = "failed"


@dataclass(frozen=True)
class Job:
    """A single job submitted to the service."""

    job_id: str
    status: str
    job_type: str | None = None
    params: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: str | None = None
    created_at: int | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> Job:
        """Build a job from a decoded API payload, ignoring unknown fields."""
        job_id = payload.get("job_id")
        if not job_id:
            msg = "Job payload is missing 'job_id'"
            raise ValueError(msg)
        params = payload.get("params") or {}
        return cls(
            job_id=str(job_id),
            status=str(payload.get("status", "")),
            job_type=payload.get("job_type"),
            params=dict(params),
            result=payload.get("result"),
            error=payload.get("error"),
            created_at=payload.get("created_at"),
        )

    @property
    def succeeded(self) -> bool:
        """Whether the job finished successfully."""
        return self.status == JobStatus.COMPLETED

    @property
    def failed(self) -> bool:
        """Whether the job finished with an error."""
        return self.status == JobStatus.FAILED

    @property
    def finished(self) -> bool:
        """Whether the job reached a terminal state and will not change again."""
        return self.succeeded or self.failed
