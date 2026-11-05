# Threat Model

## Assets

- Source approval and permitted-purpose decisions.
- Public-source access constraints and terms.
- Identity, policy, emergency-stop, compliance and audit gate evidence.
- Integrity and privacy of future collected metadata.

## Threats and controls

| Threat | Current control | Remaining requirement |
|---|---|---|
| Unreviewed or expired source | Approved state and review expiry required | Authenticated source-registry integration |
| Purpose drift | Exact purpose allowlist and source-permitted purpose | Runtime policy evaluation |
| Personal-data collection | Public-only sensitivity and typed non-personal target namespaces | Data classification and content inspection at a future adapter |
| Credentialed or private access | Unauthenticated public access only | Adapter-level enforcement |
| Excessive collection | Record, byte, rate, timeout, retry and retention ceilings | Global quotas, rate limiters and backoff |
| Emergency stop bypass | Emergency-stop gate evidence required | Local enforcement and stop propagation |
| Compliance bypass | Compliance-review evidence required | Counsel-reviewed obligations and control enforcement |
| Audit gaps | Audit-ready gate and event reference required | Durable audit sink and tamper-evident records |
| SSRF / DNS rebinding / redirects | No network code exists | Isolated egress proxy, DNS/IP validation, redirect revalidation and private-address blocking |
| Source poisoning | No source content ingested | Provenance, content validation and human review |

## Non-goals

This scaffold does not crawl, scrape, download, resolve DNS, follow redirects, authenticate to providers, parse arbitrary source content or perform entity profiling.
