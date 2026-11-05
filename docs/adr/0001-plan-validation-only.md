# ADR 0001: Plan validation only

- Status: accepted
- Date: 2026-11-02

## Context

A public-source catalogue alone does not authorize collection. Network collection introduces SSRF, privacy, terms, rate-limit, credential, provenance and emergency-stop risks.

## Decision

The first implementation validates a bounded plan only. It requires explicit evidence from source registry, identity, policy, terms, privacy, emergency-control, compliance and audit boundaries. It does not include a network client or execute plans. Initial scope excludes personal and sensitive data and limits targets/fields to public non-personal metadata.

## Consequences

- No live collection capability is claimed.
- Network adapters require a separate architecture and security review.
- All dependencies remain declared until reproducible cross-repository integration tests pass.
- The emergency-stop and compliance dependencies are mandatory architecture gates.
