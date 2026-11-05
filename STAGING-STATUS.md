# Staging and Deployment Status — osint-collection-framework

- Portfolio ID: osint-collection
- Canonical registry position: 21 of 32 (20th component; master is position 1)
- GitHub owner: PCakes303
- Intended visibility: public
- Remote repository: created at https://github.com/PCakes303/osint-collection-framework
- Default branch: main
- Deployment state: deployed; 23 staged product files verified against remote by exact Git blob SHA (23/23).
- Maturity: collection-plan validator only; no network collector.
- License: scoped mixed-license policy included in LICENSE.md; file-level provenance clearance remains required.
- Dependencies: osint-source-registry, identity-trust, policy-engine, audit-provenance, emergency-control, compliance-governance, secure-supply-chain (declared only).
- Implemented: bounded request schema; strict source metadata checks; purpose/scope/rate/retention gates; typed gate evidence; synthetic tests; Python 3.10–3.12 CI.
- Not implemented: network access, crawling, scraping, downloading, authenticated APIs, DNS resolution, redirects, content storage, personal-data processing or production authorization.
- Repository CI: run 41986109238 passed all three Python matrix jobs (3.10, 3.11, 3.12) at commit 23e4248b25ea3508c75b5249335b6bc3eb5ab6c5.
- CI workflow correction: removed an unintended escape before the Python matrix expression; the corrected workflow is now passing.
- Required before production: satisfy every integration gate in docs/INTEGRATION-GATES.md; keep collection execution disabled until independently implemented and reviewed.
- Human metadata follow-up: replace the GitHub About description's trailing “experimental design.” with the approved description “Authorized public-information collection through tools and adapters.”; add portfolio-standard topics and homepage.
