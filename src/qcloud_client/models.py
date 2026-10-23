import math
from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from enum import StrEnum
from numbers import Integral, Real
from typing import Any, ClassVar, Literal, Self, get_args

from .exceptions import QCloudError, ValidationError

_ASG = Literal["asg0", "asg1"]
_OUTPUT = Literal["out1", "out2", "off"]
_WAVEFORM = Literal["sin", "cos", "ramp"]
_BASIS = Literal["x", "p", "pi4"]

def _check_choice(name: str, value: object, choices: tuple[str, ...]) -> None:
    if value not in choices:
        msg = f"{name} must be one of {', '.join(map(repr, choices))}, got value {value!r}"
        raise ValidationError(msg)

def _check_int(name: str, value: object, *, lo: int, hi: int) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral):
        msg = f"{name} must be an integer, got {type(value).__name__}"
        raise ValidationError(msg)
    if not lo <= value <= hi:
        msg = f"{name} must be between {lo} and {hi}, got {value}"
        raise ValidationError(msg)

def _check_real(name: str, value: object, *, lo: float, hi: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real):
        msg = f"{name} must be a number, got {type(value).__name__}"
        raise ValidationError(msg)
    if not lo <= value <= hi:
        msg = f"{name} must be between {lo} and {hi}, got {value}"
        raise ValidationError(msg)

def _check_gates(name: str, value: object) -> None:
    if not isinstance(value, (list, tuple)) or not all(isinstance(g, (list, tuple)) for g in value):
        msg = f"{name} must be a list of gate operations, each itself being a list"
        raise ValidationError(msg)

def _check_cov_matrix(name: str, value: object) -> None:
    rows = value.tolist() if hasattr(value, "tolist") else value
    size = len(rows) if isinstance(rows, (list, tuple)) else 0
    if not (6 <= size <= 400 and size % 2 == 0) or not all(isinstance(r, (list, tuple)) and len(r) == size for r in rows):
        msg = f"{name} must be a square 2D array with an even size from 6 to 400 (3 to 200 modes)"
        raise ValidationError(msg)
    if not all(isinstance(x, Real) and math.isfinite(x) for row in rows for x in row):
        msg = f"{name} must contain only finite real numbers"
        raise ValidationError(msg)

@dataclass(frozen=True, kw_only=True)
class JobSpec:
    """Base class for everything :meth:`QCloudClient.submit` accepts."""

    job_type: ClassVar[str]

    def to_params(self) -> dict[str, Any]:
        return {f.name: (v.tolist() if hasattr(v := getattr(self, f.name), "tolist") else v) for f in fields(self)}

@dataclass(frozen=True, kw_only=True)
class RedPitaya(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "redpitaya"

    asg: _ASG
    output: _OUTPUT
    waveform: _WAVEFORM
    frequency: float
    amplitude: float
    offset: float

    def __post_init__(self) -> None:
        _check_choice("asg", self.asg, get_args(_ASG))
        _check_choice("output", self.output, get_args(_OUTPUT))
        _check_choice("waveform", self.waveform, get_args(_WAVEFORM))
        _check_real("frequency", self.frequency, lo=0, hi=75000000)
        _check_real("amplitude", self.amplitude, lo=0, hi=1)
        _check_real("offset", self.offset, lo=-1, hi=1)

@dataclass(frozen=True, kw_only=True)
class TNCovariance(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-covariance"

    nmodes: int
    r_db: float
    loss: float
    basis: _BASIS

    def __post_init__(self) -> None:
        _check_int("nmodes", self.nmodes, lo=1, hi=199)
        _check_real("r_db", self.r_db, lo=0, hi=16)
        _check_real("loss", self.loss, lo=0, hi=1)
        _check_choice("basis", self.basis, get_args(_BASIS))

@dataclass(frozen=True, kw_only=True)
class TNCovarianceGates(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-covariance"

    nmodes: int
    gates: Any

    def __post_init__(self) -> None:
        _check_int("nmodes", self.nmodes, lo=3, hi=199)
        _check_gates("gates", self.gates)

@dataclass(frozen=True, kw_only=True)
class TNSampling(JobSpec): # noqa: D101
    job_type: ClassVar[str] = "tn-sampling"

    cov_matrix: Any
    d: int
    chi: int
    dd: int
    N: int
    n: int

    def __post_init__(self) -> None:
        _check_cov_matrix("cov_matrix", self.cov_matrix)
        _check_int("d", self.d, lo=1, hi=12)
        _check_int("chi", self.chi, lo=1, hi=1000)
        _check_int("dd", self.dd, lo=1, hi=12)
        _check_int("N", self.N, lo=1, hi=5000000)
        _check_int("n", self.n, lo=1, hi=5000)

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
    started_at: int | None = None
    completed_at: int | None = None

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
            started_at=payload.get("started_at"),
            completed_at=payload.get("completed_at"),
        )

    @property
    def pending(self) -> bool:
        """Whether the job is pending execution."""
        return self.status == JobStatus.PENDING

    @property
    def running(self) -> bool:
        """Whether the job is actively running."""
        return self.status == JobStatus.RUNNING

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
