# Security

Public support data only. Report security problems privately to the repository maintainer; do not include customer data or credentials in public issues.

The desktop verifies an embedded Ed25519 trust root before parsing data, then enforces engine/schema, timestamp/expiry, increasing sequence, size, command and parser limits. Installed support stays immutable throughout the process. Downloads use fixed verified HTTPS without proxies, redirects or customer authentication. Downloaded Python and generic command execution are forbidden.

A signature authenticates the publisher; it is not proof that commands/parsers are correct or that the publishing account cannot be compromised. Maintainer review, synthetic fixtures, app regression checks and last-known-good rollback remain necessary. Device-support releases can influence authenticated reads, so protect signing credentials and repository/workflow access accordingly.
