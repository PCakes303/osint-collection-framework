# Security Policy

This repository contains a collection-plan validator only. It does not fetch sources, make network requests, store content or execute collection.

## Reporting

Do not publish exploitable vulnerability details, credentials, personal data or confidential operational information in public issues. Use GitHub private vulnerability reporting or a private security advisory only if enabled for this repository. No dedicated private reporting address is published here; configure an owner-approved private channel if GitHub private reporting is unavailable.

## Security invariants

- Deny by default if any identity, policy, source, legal/terms, privacy, emergency-stop, compliance or audit gate is absent or false.
- Public accessibility does not imply permission to access or reuse.
- Reject authenticated source access and all personal/sensitive-data collection in the initial profile.
- Never follow untrusted URLs or resolve DNS in this scaffold.
- A validated plan does not authorize execution.
- No live collection capability is implemented.
