# Collection Plan Contract v1.0

## Purpose

A collection request is a bounded proposal to retrieve a narrow set of public metadata. This package validates the proposal and its gate evidence; it does not execute the request or fetch the source.

## Required gates

A future trusted integration must provide verified evidence for:
- source approval and current review expiry from osint-source-registry;
- requester identity and role from identity-trust;
- exact permitted-purpose policy decision from policy-engine;
- current terms and license review;
- privacy/legal review and applicable compliance controls;
- robots/access-policy compliance;
- emergency-stop state clear from agent-emergency-control;
- compliance gate clear from agent-compliance-governance;
- audit readiness and attributable event reference from agent-audit-provenance.

Every gate is deny-by-default. A missing, stale, malformed or false value rejects the plan.

## Initial data scope

Only public non-personal metadata is eligible. Allowed target types are public datasets, publications, registries, organizations and software projects. Target references use typed namespaces (dataset:, publication:, registry:, organization:, software:). Only enumerated metadata fields are permitted; arbitrary query text is not accepted.

Private individuals, sensitive personal data, profiling, doxxing, stalking, harassment, credential harvesting, private-record collection, access-control bypass and mass surveillance are prohibited.

## Bounded plan

Each request specifies maximum records, bytes, request rate, retention days, timeout, retry count and a five-minute expiry. Requested rate and retention must not exceed the source registry's declarations. Source access must be public and unauthenticated, with a current terms URL and license expression.

## Output semantics

A successful result has status plan-validated-only and execution_enabled=false. It is not permission to collect, a legal conclusion, an identity assertion or a production authorization. A future executor must independently revalidate all gates at execution time.
