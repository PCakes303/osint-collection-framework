# OSINT Collection Framework

Portfolio ID: osint-collection  
Maturity: scaffolded, policy-gated collection-plan validator only.

A review-gated framework for planning authorized collection of non-personal public information from sources catalogued by osint-source-registry.

## Safety boundary

This repository does not crawl, scrape, download, query APIs, resolve DNS, follow redirects, authenticate to providers or collect source content. It validates a bounded collection plan and its required gate evidence only. It is not a collector or a permission grant.

The initial profile is deliberately restricted to public, non-personal metadata from approved sources with current terms, an explicit permitted purpose, public unauthenticated access, a declared rate limit and retention ceiling. Individual targeting, profiling, doxxing, credential collection, private records, sensitive personal data and access-control bypass are prohibited.

A validated plan is not execution authorization. Future collectors require separately reviewed network adapters, identity and policy enforcement, emergency-stop integration, compliance review, audit provenance, SSRF protection, rate limiting and actual runtime controls.

## Quick start

Python 3.10+:

    python -m pip install -r requirements-dev.txt
    python -m unittest discover -s tests -v

See docs/COLLECTION-CONTRACT.md, docs/PRIVACY-AND-LAWFULNESS.md and docs/INTEGRATION-GATES.md.

## Licensing

The repository documents the ecosystem's intended scoped mixed-license policy: Apache-2.0 for eligible original code and machine-readable contracts, and CC BY 4.0 for eligible original human-readable documentation. The manifest remains `pending-review` until contributor authority, file-level provenance and third-party notices are checked. Do not assume every file is cleared for redistribution. Datasets, evidence, fixtures, sample payloads, media and uncertain-provenance material receive no blanket license. See [LICENSE.md](LICENSE.md).
