# Integration Gates Before Any Collection Execution

1. **Source registry:** retrieve a validated, current approved source record; authenticate the reviewer approval.
2. **Identity:** authenticate requester and verify least-privilege collection role.
3. **Policy:** evaluate exact source, purpose, target type, fields, scope, rate and retention at request and execution time.
4. **Terms and privacy:** verify current terms/license, lawful purpose, privacy review, data minimization and retention/deletion.
5. **Emergency stop:** query authoritative monotonic stop state at every enforcement point; deny if unavailable, stale or active.
6. **Compliance:** evaluate applicable obligations and controls; do not substitute the public legal register for counsel.
7. **Audit:** record request, decision, source version, policy evidence, collection limits, result digest and deletion event.
8. **Network security:** use an isolated egress adapter with DNS rebinding/SSRF controls, redirect validation, private/reserved IP blocking, TLS verification, timeouts, byte limits and provider-specific rate limits.
9. **Execution isolation:** no credentials or source-provided code; enforce OS/container/network/resource isolation for any parser or tool.
10. **Conformance:** test denied source, expired approval, revocation, emergency stop, policy outage, audit outage, scope escalation, rate limit, retention and data-classification failures.

A passing plan validator does not satisfy any runtime gate. No network collection is enabled by this repository.
