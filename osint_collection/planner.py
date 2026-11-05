"""Fail-closed public collection-plan validation; no network or collection is performed."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit
import json

from jsonschema import Draft202012Validator, FormatChecker

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "collection-request.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
MAX_REQUEST_LIFETIME = timedelta(minutes=5)
MAX_FUTURE_SKEW = timedelta(seconds=30)
ALLOWED_SOURCE_TYPES = {"website", "public_api", "dataset", "publication", "document_repository", "public_registry"}
ALLOWED_ACCESS_METHODS = {"public_web", "public_api", "downloadable_dataset"}
SUPPORTED_PURPOSES = {
    "research", "verification", "public-interest-research",
    "security-advisory-monitoring", "open-source-software-intelligence",
    "public-disclosure-monitoring", "public-registry-verification",
}
PROHIBITED_PURPOSES = {
    "credential harvesting", "credential-harvesting", "doxxing", "stalking",
    "harassment", "mass surveillance", "mass-surveillance",
    "individual profiling", "individual-profiling", "private record collection",
    "sensitive data collection", "access-control bypass",
}

class PlanError(ValueError):
    """Raised when a collection plan cannot be proven eligible for separate review."""

@dataclass(frozen=True)
class GateEvidence:
    source_approval_verified: bool = False
    identity_authorized: bool = False
    policy_allowed: bool = False
    terms_current: bool = False
    privacy_reviewed: bool = False
    robots_compliant: bool = False
    emergency_stop_clear: bool = False
    compliance_gate_clear: bool = False
    audit_ready: bool = False

@dataclass(frozen=True)
class CollectionPlan:
    request_id: str
    source_id: str
    purpose: str
    target_type: str
    target_ref: str
    requested_fields: tuple[str, ...]
    max_records: int
    max_bytes: int
    requested_rate_per_minute: int
    retention_days: int
    expires_at: datetime
    status: str = "plan-validated-only"
    execution_enabled: bool = False

def _parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise PlanError(f"{label} must be a timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise PlanError(f"{label} is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise PlanError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)

def _https_url(value: Any) -> bool:
    if not isinstance(value, str) or len(value) > 2048 or any(ch.isspace() for ch in value):
        return False
    try:
        parts = urlsplit(value)
        parts.port
        return parts.scheme == "https" and bool(parts.hostname) and parts.username is None and parts.password is None
    except ValueError:
        return False

def _require_gate(evidence: GateEvidence) -> None:
    if not isinstance(evidence, GateEvidence):
        raise PlanError("deny:trusted gate evidence unavailable")
    for field in GateEvidence.__dataclass_fields__:
        if getattr(evidence, field) is not True:
            raise PlanError(f"deny:gate:{field}")

def _validate_source(source: Mapping[str, Any], request: Mapping[str, Any], now: datetime) -> None:
    if not isinstance(source, Mapping):
        raise PlanError("source record must be an object")
    required = {
        "source_id", "source_type", "canonical_url", "access_method", "access_auth",
        "terms_url", "license_expression", "data_sensitivity", "robots_policy",
        "permitted_purposes", "prohibited_purposes", "declared_rate_limit_per_minute",
        "retention_days", "review_status", "reviewed_at", "review_expires_at",
    }
    allowed = required | {"review_notes"}
    missing = required - set(source)
    unknown = set(source) - allowed
    if missing:
        raise PlanError(f"source record missing fields: {sorted(missing)}")
    if unknown:
        raise PlanError(f"source record contains unknown fields: {sorted(unknown)}")
    if source["source_id"] != request["source_id"]:
        raise PlanError("source_id does not match request")
    if source["review_status"] != "approved":
        raise PlanError("source is not approved")
    if not isinstance(source["source_type"], str) or source["source_type"] not in ALLOWED_SOURCE_TYPES:
        raise PlanError("source type is not permitted")
    if not isinstance(source["access_method"], str) or source["access_method"] not in ALLOWED_ACCESS_METHODS or source["access_auth"] != "none":
        raise PlanError("authenticated or unsupported source access is prohibited")
    if source["data_sensitivity"] != "public":
        raise PlanError("only public non-personal source data is allowed")
    if not isinstance(source["robots_policy"], str) or source["robots_policy"] not in {"respect", "not_applicable"}:
        raise PlanError("robots policy requires manual review or is unknown")
    if not _https_url(source["canonical_url"]) or not _https_url(source["terms_url"]):
        raise PlanError("canonical and terms URLs must be HTTPS without credentials")
    if not isinstance(source["license_expression"], str) or not source["license_expression"].strip():
        raise PlanError("source license expression is missing")
    if not isinstance(source["permitted_purposes"], (list, tuple)) or not isinstance(source["prohibited_purposes"], (list, tuple)):
        raise PlanError("source purpose declarations are malformed")
    if any(not isinstance(item, str) for item in source["permitted_purposes"] + source["prohibited_purposes"]):
        raise PlanError("source purpose declarations contain non-text values")
    purpose = request["purpose"].strip().casefold()
    permitted = {item.casefold() for item in source["permitted_purposes"]}
    prohibited = {item.casefold() for item in source["prohibited_purposes"]}
    if purpose not in SUPPORTED_PURPOSES or purpose not in permitted or purpose in prohibited or purpose in PROHIBITED_PURPOSES:
        raise PlanError("requested purpose is not explicitly permitted")
    rate = source["declared_rate_limit_per_minute"]
    if isinstance(rate, bool) or not isinstance(rate, int) or rate < 1:
        raise PlanError("source must declare a positive rate limit")
    if request["requested_rate_per_minute"] > rate:
        raise PlanError("requested rate exceeds source declaration")
    retention = source["retention_days"]
    if isinstance(retention, bool) or not isinstance(retention, int) or retention < 1:
        raise PlanError("source must declare a positive retention ceiling")
    if request["retention_days"] > retention:
        raise PlanError("requested retention exceeds source ceiling")
    reviewed = _parse_time(source["reviewed_at"], "source reviewed_at")
    expiry = _parse_time(source["review_expires_at"], "source review_expires_at")
    if reviewed > now + MAX_FUTURE_SKEW or expiry <= now or expiry <= reviewed:
        raise PlanError("source review is stale, expired or malformed")

def validate_collection_plan(
    source: Mapping[str, Any], request: Mapping[str, Any], evidence: GateEvidence, *, now: datetime
) -> CollectionPlan:
    """Validate a bounded plan. A successful result never enables execution."""
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise PlanError("now must be timezone-aware")
    errors = sorted(_VALIDATOR.iter_errors(request), key=lambda e: (list(e.absolute_path), e.message))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise PlanError(f"request schema error at {location}: {first.message}")
    target_prefix = {
        "public_dataset": "dataset:",
        "public_publication": "publication:",
        "public_registry": "registry:",
        "public_organization": "organization:",
        "public_software_project": "software:",
    }[request["target_type"]]
    if not request["target_ref"].startswith(target_prefix):
        raise PlanError("target_ref must use the non-personal namespace for target_type")
    current = now.astimezone(timezone.utc)
    requested_at = _parse_time(request["requested_at"], "requested_at")
    expires_at = _parse_time(request["expires_at"], "expires_at")
    if requested_at > current + MAX_FUTURE_SKEW:
        raise PlanError("request is issued too far in the future")
    if expires_at <= current or expires_at <= requested_at or expires_at - requested_at > MAX_REQUEST_LIFETIME:
        raise PlanError("request is expired or exceeds the five-minute lifetime")
    _validate_source(source, request, current)
    _require_gate(evidence)
    return CollectionPlan(
        request_id=request["request_id"], source_id=request["source_id"], purpose=request["purpose"],
        target_type=request["target_type"], target_ref=request["target_ref"],
        requested_fields=tuple(request["requested_fields"]), max_records=request["max_records"],
        max_bytes=request["max_bytes"], requested_rate_per_minute=request["requested_rate_per_minute"],
        retention_days=request["retention_days"], expires_at=expires_at,
    )
