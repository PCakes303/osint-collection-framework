# Contributing

Contributions may improve plan validation, schemas, synthetic fixtures and safety documentation. Any network collection adapter requires a separate architecture decision, threat model, privacy/legal review and explicit authorization.

## Development

- Python 3.10+
- Install: python -m pip install -r requirements-dev.txt
- Test: python -m unittest discover -s tests -v

Changes to target types, permitted fields, source approval, retention, rate limits or authorization gates require positive, negative and boundary tests. Do not add real source approvals or live collected data to this repository.
