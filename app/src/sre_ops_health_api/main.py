import os
import time
from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


Status = Literal["healthy", "warning", "critical"]


class VersionResponse(BaseModel):
    app: str
    version: str
    environment: str
    commit_sha: str


class CheckResult(BaseModel):
    name: str
    status: Status
    message: str
    last_run: str


class ChecksResponse(BaseModel):
    environment: str
    checks: list[CheckResult]


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def maybe_sleep() -> None:
    if not env_bool("SLOW_MODE"):
        return
    seconds = float(os.getenv("SLOW_SECONDS", "2"))
    time.sleep(max(seconds, 0))


def build_checks() -> list[CheckResult]:
    now = utc_now()
    return [
        CheckResult(
            name="linux-patching",
            status="healthy",
            message="Linux patch compliance is within policy.",
            last_run=now,
        ),
        CheckResult(
            name="windows-patching",
            status="healthy",
            message="Windows patch compliance is within policy.",
            last_run=now,
        ),
        CheckResult(
            name="backup-status",
            status="warning",
            message="Last backup is older than the target recovery policy.",
            last_run=now,
        ),
        CheckResult(
            name="certificate-expiry",
            status="critical",
            message="One certificate expires within seven days.",
            last_run=now,
        ),
    ]


app = FastAPI(title="SRE Ops Health API", version="0.1.0")


@app.on_event("startup")
def fail_startup_when_requested() -> None:
    if env_bool("FAIL_STARTUP"):
        raise RuntimeError("FAIL_STARTUP=true requested startup failure")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "timestamp": utc_now()}


@app.get("/ready")
def ready() -> dict[str, str]:
    if not env_bool("READY", default=True):
        raise HTTPException(status_code=503, detail="application is not ready")
    return {"status": "ready", "timestamp": utc_now()}


@app.get("/api/v1/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(
        app=os.getenv("APP_NAME", "sre-ops-health-api"),
        version=os.getenv("APP_VERSION", "0.1.0"),
        environment=os.getenv("APP_ENV", "local"),
        commit_sha=os.getenv("COMMIT_SHA", "unknown"),
    )


@app.get("/api/v1/checks", response_model=ChecksResponse)
def checks() -> ChecksResponse:
    maybe_sleep()
    return ChecksResponse(
        environment=os.getenv("APP_ENV", "local"),
        checks=build_checks(),
    )


@app.get("/api/v1/checks/{check_name}", response_model=CheckResult)
def check_by_name(check_name: str) -> CheckResult:
    maybe_sleep()
    for check in build_checks():
        if check.name == check_name:
            return check
    raise HTTPException(status_code=404, detail=f"unknown check: {check_name}")
