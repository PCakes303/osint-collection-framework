# Agent instructions

- This repository validates collection plans only; never add a network client, crawler, scraper, downloader or authenticated API integration without a separate security review and explicit approval.
- Restrict the initial profile to non-personal public metadata and the enumerated target types/fields.
- Never target private individuals, build personal profiles, collect sensitive personal data, harvest credentials, bypass access controls or evade robots/terms/rate limits.
- Require an approved, unexpired source record, exact permitted-purpose match, current terms, privacy review, policy approval, identity authorization, emergency-stop clearance, compliance-gate clearance and audit readiness.
- All gate evidence must be supplied by trusted adapters in a future integration; synthetic test evidence is not authorization.
- Fail closed on missing, stale, malformed or negative evidence.
- Respect source rate limits and retention ceilings; never raise a limit above the source declaration.
- Do not infer legal permission from public accessibility or HTTPS.
- Do not store credentials, cookies, API keys, collected content or personal data.
- Run python -m unittest discover -s tests -v before committing.
