# Changelog

## 2.0.0 — 17 September 2026

- 608 infrastructure product recognition rules, including the original 444 explicit series list and 135 wireless/service rules (some refine existing entries), with manufacturer sources and examples.
- Four new compiled collector families: Arista EOS, Ruckus/Brocade FastIron, HPE/H3C Comware and Huawei VRP switches; six core read sections each.
- Engine-2 command plans allow bounded literal `display` reads as well as `show`. Engine-1 packs remain valid under the new validator.
- Synthetic parser fixtures and negative recognition checks; no live compatibility certification. Backups and advanced collection are not implied by recognition.
- Published as signed engine-2 sequence 2; requires Network Tool Kit 2.0.0.
- Alcatel health collection includes a dedicated error-counter fallback.

## 1.0.0

Initial signed engine-1 data packs: eleven existing diagram collection families, ordered core/documentation commands, product recognition databases, identity markers, conditional firmware/model variants, bounded declarative parser transforms and synthetic fixture validation. Bundled offline fallback and staged activation preserve scan consistency.
