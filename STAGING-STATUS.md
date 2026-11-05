# Staging Status — osint-collection-framework

- Portfolio ID: osint-collection
- Canonical registry position: 21 of 32 (20th component; master is position 1)
- GitHub owner: PCakes303
- Intended visibility: public
- Remote repository: not yet created; the connected GitHub integration cannot create repositories.
- Staging state: initial scaffold prepared in the master repository; matrix validated.
- Maturity: collection-plan validator only; no network collector.
- License: scoped mixed-license policy included in staged LICENSE.md; file-level provenance clearance remains required.
- Dependencies: osint-source-registry, identity-trust, policy-engine, audit-provenance, emergency-control, compliance-governance, secure-supply-chain (declared only).
- Implemented in this staging packet: bounded request schema; strict source metadata checks; purpose/scope/rate/retention gates; typed gate evidence; synthetic tests; Python 3.10–3.12 CI.
- Not implemented: network access, crawling, scraping, downloading, authenticated APIs, DNS resolution, redirects, content storage, personal-data processing or production authorization.
- Staging CI: master workflow run 41514134921 passed 19 tests on Python 3.10, 3.11 and 3.12.
- Required before remote deployment: owner creates public repository PCakes303/osint-collection-framework, then the staging product files are pushed and repository CI verified.
- Required before production: satisfy every integration gate in docs/INTEGRATION-GATES.md.
