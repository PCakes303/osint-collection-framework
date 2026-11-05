from datetime import datetime, timedelta, timezone

def source(now=None):
    now = now or datetime.now(timezone.utc)
    return {
        "source_id":"example.public-api","source_type":"public_api",
        "canonical_url":"https://api.example.org/catalog","access_method":"public_api","access_auth":"none",
        "terms_url":"https://example.org/terms","license_expression":"CC-BY-4.0",
        "data_sensitivity":"public","robots_policy":"not_applicable",
        "permitted_purposes":["research","verification"],"prohibited_purposes":["credential harvesting","targeted surveillance"],
        "declared_rate_limit_per_minute":30,"retention_days":30,"review_status":"approved",
        "reviewed_at":(now-timedelta(days=1)).isoformat().replace("+00:00","Z"),
        "review_expires_at":(now+timedelta(days=30)).isoformat().replace("+00:00","Z"),
    }

def request(now=None):
    now = now or datetime.now(timezone.utc)
    return {
        "request_version":"1.0","request_id":"synthetic-request-001","source_id":"example.public-api",
        "purpose":"research","target_type":"public_dataset","target_ref":"dataset:synthetic-catalog-01",
        "requested_fields":["dataset_metadata","terms_license_metadata"],"max_records":25,"max_bytes":65536,
        "requested_rate_per_minute":10,"retention_days":14,"timeout_seconds":10,"max_retries":1,
        "requested_at":now.isoformat().replace("+00:00","Z"),
        "expires_at":(now+timedelta(minutes=4)).isoformat().replace("+00:00","Z"),
        "requester_id":"synthetic-operator-1","legal_review_ref":"legal-review-synthetic",
        "privacy_review_ref":"privacy-review-synthetic","policy_decision_ref":"policy-decision-synthetic",
        "emergency_state_ref":"emergency-state-synthetic","compliance_review_ref":"compliance-review-synthetic",
        "audit_event_ref":"audit-event-synthetic"
    }
