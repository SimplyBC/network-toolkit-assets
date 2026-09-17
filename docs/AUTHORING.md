# Authoring device support

1. Identify the actual operating-system family and existing engine. A manufacturer, OUI, hostname or open port alone is not authenticated identity.
2. Edit the corresponding `vendors/<engine>.json`. Preserve `id`, `driver` and `sectionOrder`; identity must run first. Every defined core section occurs once in that order. The engine must keep the core sections its parser expects.
3. `sections` holds ordered command alternatives. The first successful, recognisable response wins. `documentation` retains the collector's existing per-section collection/merge semantics. Commands must be literal `show ...` reads. Only `| display xml`, `| display json` and `| display set` pipes are allowed. No shell substitutions, redirects, configuration mode or privilege escalation.
4. A `variant` has `id`, `containsAll`, `sections`, `documentation`, `timeoutSeconds` and `transforms`. All markers must appear in freshly collected identity, including model/software markers where needed. Exactly one matching variant applies; ambiguous matches fall back to the base plan. Variant maps override named sections; other sections are preserved. Identity commands cannot be changed retroactively by a variant. At most eight variants per family.
5. Optional `transforms` normalise a changed CLI format into the existing parser's documented input. Fields are `section`, `containsAll`, `pattern`, `replacement`, `maxMatches`, `fixtures`. The replacement uses literal text and `\g<name>` captures, never code. At least one `{input, expected}` synthetic fixture is mandatory. Expressions have deadlines and byte/match limits; unsupported/failed transforms leave the section incomplete rather than inventing successful collection.
6. Recognition catalogue edits need specific product signatures. Infrastructure examples must match their pattern. Keep AP/controller and hypervisor/guest distinctions. A recognition rule does not grant collection support or infer physical placement. Identity aliases can only select existing engine IDs and device categories.
7. Run build validation, unit tests and public-content audit. Changes to the engine contract/validator also need the private toolkit's full adapter regression suite and a desktop release; editing the public validator cannot expand an installed engine's permissions.
8. Add a changelog entry, increment manifest sequence/version, review and release.

## Synthetic parser example

The executable test `test_synthetic_output_adapter_and_variant` demonstrates a named capture translating `System name = example-switch` to `hostname: example-switch`. It does not change the published base adapters. Use invented values, documentation IP ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`) and locally administered synthetic MACs. Never copy customer output and merely remove a password: names, topology and serials are also sensitive.

## Limits

Engine 1: 2 MiB decoded bundle, 3 MiB envelope, 11 fixed adapter families, eight alternatives per section, eight variants per family, 128 parser rules total, 512 infrastructure and 512 fixed-equipment rules. Regex matches are capped at 5 ms, substitutions at 50 ms, parser input at 1 MiB and output at 2 MiB. Parser transforms cannot fetch URLs, files or secrets. A larger response can still be handled by the built-in parser when no transform applies.

Do not present recognition or fixture coverage as universal vendor/version support. Document measured capabilities and known gaps. Test representative positive, negative, empty, privilege-denied, malformed, large and older-firmware output cases before release.
