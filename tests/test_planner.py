import unittest
from datetime import datetime, timedelta, timezone
from osint_collection.planner import GateEvidence, PlanError, validate_collection_plan
from tests.helpers import source, request

ALLOW = GateEvidence(True, True, True, True, True, True, True, True, True)

class CollectionPlannerTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        self.source = source(self.now)
        self.request = request(self.now)

    def test_valid_plan_is_not_execution_authorization(self):
        plan = validate_collection_plan(self.source, self.request, ALLOW, now=self.now)
        self.assertEqual(plan.status, "plan-validated-only")
        self.assertFalse(plan.execution_enabled)
        self.assertEqual(plan.max_records, 25)

    def test_unapproved_source_is_denied(self):
        self.source["review_status"] = "pending"
        with self.assertRaisesRegex(PlanError, "not approved"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_expired_source_review_is_denied(self):
        self.source["review_expires_at"] = (self.now-timedelta(seconds=1)).isoformat()
        with self.assertRaisesRegex(PlanError, "stale, expired"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_personal_data_source_is_denied(self):
        self.source["data_sensitivity"] = "personal_data_possible"
        with self.assertRaisesRegex(PlanError, "non-personal"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_authenticated_access_is_denied(self):
        self.source["access_auth"] = "api_key_required"
        with self.assertRaisesRegex(PlanError, "authenticated"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_unknown_robots_policy_is_denied(self):
        self.source["robots_policy"] = "unknown"
        with self.assertRaisesRegex(PlanError, "robots policy"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_purpose_must_be_explicitly_permitted(self):
        self.request["purpose"] = "general research"
        with self.assertRaisesRegex(PlanError, "not explicitly permitted"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_prohibited_purpose_is_denied(self):
        self.request["purpose"] = "credential harvesting"
        self.source["permitted_purposes"].append("credential harvesting")
        with self.assertRaisesRegex(PlanError, "not explicitly permitted"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_rate_limit_cannot_exceed_source_declaration(self):
        self.request["requested_rate_per_minute"] = 31
        with self.assertRaisesRegex(PlanError, "exceeds source"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_retention_cannot_exceed_source_ceiling(self):
        self.request["retention_days"] = 31
        with self.assertRaisesRegex(PlanError, "exceeds source ceiling"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_each_governance_gate_fails_closed(self):
        for field in GateEvidence.__dataclass_fields__:
            values = {name: True for name in GateEvidence.__dataclass_fields__}
            values[field] = False
            with self.subTest(gate=field), self.assertRaises(PlanError):
                validate_collection_plan(self.source, self.request, GateEvidence(**values), now=self.now)

    def test_gate_evidence_must_be_typed(self):
        with self.assertRaisesRegex(PlanError, "gate evidence unavailable"):
            validate_collection_plan(self.source, self.request, {"policy_allowed":True}, now=self.now)

    def test_source_id_must_match_request(self):
        self.request["source_id"] = "different-source"
        with self.assertRaisesRegex(PlanError, "does not match"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_individual_target_type_is_rejected_by_schema(self):
        self.request["target_type"] = "private_person"
        with self.assertRaisesRegex(PlanError, "request schema"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_target_reference_uses_non_personal_namespace(self):
        self.request["target_ref"] = "person:somebody"
        with self.assertRaisesRegex(PlanError, "non-personal namespace"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_malformed_source_type_fails_closed(self):
        self.source["source_type"] = []
        with self.assertRaisesRegex(PlanError, "source type"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_unknown_source_fields_are_rejected(self):
        self.source["fetch_url"] = "https://example.org/private"
        with self.assertRaisesRegex(PlanError, "unknown fields"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_request_expiry_and_future_skew_are_enforced(self):
        self.request["expires_at"] = (self.now+timedelta(minutes=6)).isoformat()
        with self.assertRaisesRegex(PlanError, "five-minute"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)
        self.request = request(self.now+timedelta(minutes=1))
        with self.assertRaisesRegex(PlanError, "future"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

    def test_embedded_credentials_in_source_url_are_rejected(self):
        self.source["canonical_url"] = "https://user:secret@example.org/"
        with self.assertRaisesRegex(PlanError, "HTTPS"):
            validate_collection_plan(self.source, self.request, ALLOW, now=self.now)

if __name__ == "__main__":
    unittest.main()
