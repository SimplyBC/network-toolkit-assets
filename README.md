# Network Toolkit Assets

Versioned **data-only** device-support packs for Network Tool Kit. The desktop contains the execution engine; this repository supplies reviewed command plans, product recognition, model/software variants and bounded output-normalisation rules.

This repository is public. **Never include customer output, credentials, real customer addresses, hostnames, serial numbers, configurations, vault content or signing keys.** Tests use invented equipment and documentation addresses only.

## What is here

- `vendors/*.json`: all 11 existing diagram collection families, ordered core reads, documentation reads and 5–90 second command timeouts.
- `catalogues/identity.json`: identity markers mapped to existing collection engines.
- `catalogues/infrastructureProducts.json`: recognisable infrastructure, including observed-only products.
- `catalogues/fixedEquipmentProducts.json`: confirmed fixed-equipment product patterns; existing no-login rules remain enforced by the application.
- `tools/support_pack_schema.py`: the exact engine-1 authoring validator and bounded data parser, mirrored in the application.
- `tests/`: synthetic regression tests and recognition examples.
- `channel/stable.json`: signed stable release, consumed over verified HTTPS. It contains public data only, encoded for unambiguous signature verification; **base64 is not encryption**.
- `trust.json`: public Ed25519 verification key. The private key exists only in the maintainer's protected storage and the GitHub Actions signing secret.

## Quick start

```sh
python -m venv .venv
# Activate the virtual environment for your OS, then:
python -m pip install -r requirements.txt
python tools/build.py
python -m unittest discover -s tests
python tools/audit_public.py
```

Read [AUTHORING](docs/AUTHORING.md) and [RELEASING](docs/RELEASING.md) before changing device support.

## Scope and compatibility

A new model using an existing command/transport family, a command fallback, timeout, recognition rule or compatible text-output variation can be released here. New transports, authentication flows, arbitrary Python parsers, new inventory schemas, new UI capabilities, API workflows, complex topology inference and backup engines require a desktop engine release. Packs cannot load drivers, change credential handling, enter configuration mode, enable SNMP writes or add executable plugins.

The current pack owns **diagram/discovery support**. Independent Configuration Backup and standalone Switch MAC Inventory remain application-owned in engine 1. Their behaviour is not silently changed by this repository. Existing complex vendor parsers, session setup, pagination and protocol-specific safeguards remain trusted application code. Parser rules normalise output into those existing parsers; they do not claim every model or firmware has been live-tested.

The app ships a verified bundled baseline. Updates are downloaded in the background at most daily, validated, then activated on the next launch. Existing scans and recursively discovered seeds retain one pack version. Settings → Device support provides Check, Pause and Restore previous pack. Offline operation retains installed support; metadata expiry prevents accepting stale *new* downloads, not using already installed support.
