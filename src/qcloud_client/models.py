from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from enum import StrEnum
from typing import Any, ClassVar, Literal, Self

from .exceptions import QCloudError


@dataclass(frozen=True, kw_only=True)
class JobSpec:
    """Base class for everything :meta:`QCloudClient.submit` accepts."""

    job_type: ClassVar[str]

    def to_params(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}


@dataclass(frozen=True, kw_only=True)
class RedPitaya(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "redpitaya"

    asg: Literal["asg0", "asg1"]
    output: Literal["out1", "out2", "off"]
    waveform: Literal["sin", "cos", "ramp"]
    frequency: float
    amplitude: float
    offset: float


@dataclass(frozen=True, kw_only=True)
class TNCovariance(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-covariance"

    nmodes: int
    r_db: float
    loss: float
    basis: Literal["x", "p", "pi4"]


@dataclass(frozen=True, kw_only=True)
class TNCovarianceGates(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-covariance"

    nmodes: int
    gates: Any


@dataclass(frozen=True, kw_only=True)
class TNSampling(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-sampling"

    cov_matrix: Any
    d: int
    chi: int
    dd: int
    N: int
    n: int


class JobStatus(StrEnum):
    """Job states reported by the API."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
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
    def from_dict(cls, payload: Mapping[str, Any]) -> Self:
        """Build a job from a decoded API payload, ignoring unknown fields."""
        job_id = payload.get("job_id")
        if not job_id:
            msg = "Job payload is missing 'job_id'"
            raise QCloudError(msg)
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
