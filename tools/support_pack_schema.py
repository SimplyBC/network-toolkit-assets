"""Versioned data-only support-pack contract; also shipped to the asset authoring repo.

No imports, expressions, shell expansion or callable parser names come from a pack.
Regular expressions run with native deadlines, capped input/output and fixture checks.
"""

from __future__ import annotations

import copy
import json
import re
import time
from functools import lru_cache
from typing import Any

import regex  # type: ignore[import-untyped]

ENGINE = 2
MAX_BYTES = 2 * 1024 * 1024
DRIVERS = {
    "infoblox_nios": "",
    "juniper_junos": "juniper_junos",
    "aruba_os": "aruba_os",
    "alcatel_aos": "alcatel_aos",
    "paloalto_panos": "paloalto_panos",
    "paloalto_panos_ssh": "paloalto_panos",
    "aruba_aoscx": "aruba_aoscx",
    "hp_procurve": "hp_procurve",
    "cisco_ios": "cisco_ios",
    "cisco_nxos": "cisco_nxos",
    "cisco_s300": "cisco_s300",
}
LEGACY_DRIVERS = dict(DRIVERS)
DRIVERS.update(
    {
        "arista_eos": "arista_eos",
        "ruckus_fastiron": "ruckus_fastiron",
        "hp_comware": "hp_comware",
        "huawei_vrp": "huawei",
    }
)
KINDS = frozenset({"switch", "paloalto", "clearpass", "infoblox", "fortinac", "mobility"})
SECTIONS = frozenset(
    {
        "identity",
        "hostname",
        "interfaces",
        "interface_details",
        "arp",
        "bgp",
        "ospf",
        "lldp",
        "vlans",
        "aggregation",
        "stack",
        "fdb",
        "aliases",
        "memberships",
        "ha",
        "routes",
        "vpn",
        "poe",
        "transceivers",
        "cdp",
        "trunks",
        "accessPoints",
        "services",
        "addressing",
        "redundancy",
        "spanningTree",
        "policy",
        "health",
    }
)
CATEGORIES = frozenset(
    {"access_point", "camera", "access_control", "printer", "power", "sensor", "iot", "storage"}
)
DEVICE_TYPES = frozenset(
    {"switch", "firewall", "router", "server", "storage", "hypervisor", "management", "loadbalancer"}
)


def exact(value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("Support-pack object has invalid fields.")
    return value


def text(value: Any, maximum: int = 512, *, empty: bool = False) -> str:
    if (
        not isinstance(value, str)
        or len(value) > maximum
        or (not value and not empty)
        or any(ord(c) < 32 for c in value)
    ):
        raise ValueError("Invalid support-pack text.")
    return value


def rows(value: Any, maximum: int) -> list[Any]:
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Support-pack list exceeds its limit.")
    return value


def command(value: Any) -> str:
    value = text(value, 160)
    # No substitution, CLI command separators, output files, remote transfers or privilege changes.
    if not re.fullmatch(
        r"(?:show|display) [A-Za-z0-9][A-Za-z0-9 _./:-]*(?: \| display (?:xml|json|set))?", value
    ):
        raise ValueError("Only literal read-only show/display commands are supported.")
    return value


def command_map(value: Any) -> None:
    if not isinstance(value, dict) or set(value) - SECTIONS:
        raise ValueError("Unknown command section.")
    for candidates in value.values():
        if not rows(candidates, 8) or len(set(map(command, candidates))) != len(candidates):
            raise ValueError("Command alternatives must be nonempty and unique.")


@lru_cache(maxsize=2048)
def expression(value: str) -> Any:
    text(value, 512)
    if any(token in value for token in ("(?R", "(?0", "(?&", "(?P>", "(*", "(?C")):
        raise ValueError("Recursive or executable expression extensions are not supported.")
    if any(int(count) > 4096 for count in re.findall(r"\d+", " ".join(re.findall(r"\{[0-9,]+\}", value)))):
        raise ValueError("Expression repetition exceeds its limit.")
    try:
        return regex.compile(value, regex.IGNORECASE | regex.VERSION0)
    except regex.error:
        raise ValueError("Invalid support-pack expression.") from None


def matches(pattern: str, value: str) -> bool:
    try:
        return bool(expression(pattern).search(value[:65536], timeout=0.005))
    except TimeoutError:
        return False


def transform(rule: dict[str, Any], output: str) -> str:
    if len(output) > 1024 * 1024:
        raise ValueError("Parser input exceeds its support-pack limit.")
    try:
        result = expression(rule["pattern"]).sub(
            rule["replacement"], output, count=rule["maxMatches"], timeout=0.05
        )
    except (TimeoutError, regex.error, IndexError):
        raise ValueError("Support-pack parser exceeded its budget or has invalid captures.") from None
    if len(result) > 2 * 1024 * 1024:
        raise ValueError("Support-pack parser output exceeded its limit.")
    return str(result)


def transforms(value: Any) -> None:
    for rule in rows(value, 16):
        exact(rule, {"section", "containsAll", "pattern", "replacement", "maxMatches", "fixtures"})
        if rule["section"] not in SECTIONS:
            raise ValueError("Unknown parser section.")
        selectors(rule["containsAll"])
        expression(rule["pattern"])
        if (
            not isinstance(rule["replacement"], str)
            or len(rule["replacement"]) > 1024
            or "\x00" in rule["replacement"]
        ):
            raise ValueError("Invalid parser replacement.")
        if type(rule["maxMatches"]) is not int or not 1 <= rule["maxMatches"] <= 4096:
            raise ValueError("Invalid parser match limit.")
        if not rows(rule["fixtures"], 16):
            raise ValueError("Each parser requires synthetic input/expected fixtures.")
        for fixture in rule["fixtures"]:
            exact(fixture, {"input", "expected"})
            if any(not isinstance(fixture[k], str) or len(fixture[k]) > 8192 for k in fixture):
                raise ValueError("Invalid parser fixture.")
            if transform(rule, fixture["input"]) != fixture["expected"]:
                raise ValueError("Support-pack parser fixture failed.")


def selectors(value: Any) -> None:
    if not rows(value, 8):
        raise ValueError("A variant needs explicit identity markers.")
    for marker in value:
        text(marker, 120)


def selected(markers: list[str], identity: str) -> bool:
    return all(marker.casefold() in identity.casefold() for marker in markers)


def validate(data: Any) -> dict[str, Any]:
    exact(
        data,
        {
            "schemaVersion",
            "engine",
            "sequence",
            "version",
            "issuedAt",
            "expiresAt",
            "profiles",
            "infrastructureProducts",
            "fixedEquipmentProducts",
            "identity",
        },
    )
    if (
        type(data["schemaVersion"]) is not int
        or data["schemaVersion"] != 1
        or type(data["engine"]) is not int
        or data["engine"] not in {1, ENGINE}
    ):
        raise ValueError("This support pack requires a different toolkit engine.")
    if type(data["sequence"]) is not int or not 1 <= data["sequence"] <= 2**31:
        raise ValueError("Invalid pack sequence.")
    if not re.fullmatch(r"\d{1,4}\.\d{1,4}\.\d{1,4}", text(data["version"], 20)):
        raise ValueError("Invalid pack version.")
    if (
        any(type(data[k]) is not int for k in ("issuedAt", "expiresAt"))
        or not 0 < data["expiresAt"] - data["issuedAt"] <= 366 * 86400
    ):
        raise ValueError("Invalid pack validity period.")
    if not isinstance(data["profiles"], dict) or set(data["profiles"]) != set(
        LEGACY_DRIVERS if data["engine"] == 1 else DRIVERS
    ):
        raise ValueError("The pack must retain every built-in engine family.")
    for key, profile in data["profiles"].items():
        exact(
            profile,
            {
                "label",
                "driver",
                "sections",
                "documentation",
                "timeoutSeconds",
                "transforms",
                "variants",
                "sectionOrder",
                "documentationOrder",
            },
        )
        if (
            not isinstance(profile["sectionOrder"], list)
            or len(profile["sectionOrder"]) != len(profile["sections"])
            or set(profile["sectionOrder"]) != set(profile["sections"])
        ):
            raise ValueError("Section order must list each collection section exactly once.")
        if key != "paloalto_panos" and profile["sectionOrder"][:1] != ["identity"]:
            raise ValueError("Identity must be collected before other sections.")
        if (
            not isinstance(profile["documentationOrder"], list)
            or len(profile["documentationOrder"]) != len(profile["documentation"])
            or set(profile["documentationOrder"]) != set(profile["documentation"])
        ):
            raise ValueError("Documentation order must list every section exactly once.")
        text(profile["label"], 120)
        if profile["driver"] != DRIVERS[key]:
            raise ValueError("Packs cannot introduce executable drivers.")
        for field in ("sections", "documentation"):
            command_map(profile[field])
        if key != "paloalto_panos" and "identity" not in profile["sections"]:
            raise ValueError("Identity collection cannot be removed.")
        timeout(profile["timeoutSeconds"])
        transforms(profile["transforms"])
        ids = set()
        for variant in rows(profile["variants"], 8):
            exact(variant, {"id", "containsAll", "sections", "documentation", "timeoutSeconds", "transforms"})
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", text(variant["id"], 64)) or variant["id"] in ids:
                raise ValueError("Invalid or duplicate variant ID.")
            ids.add(variant["id"])
            selectors(variant["containsAll"])
            command_map(variant["sections"])
            command_map(variant["documentation"])
            # Identity is collected before a variant can be selected.
            if "identity" in variant["sections"]:
                raise ValueError("Variants cannot retroactively change identity commands.")
            timeout(variant["timeoutSeconds"])
            transforms(variant["transforms"])
    if (
        sum(
            len(p["transforms"]) + sum(len(v["transforms"]) for v in p["variants"])
            for p in data["profiles"].values()
        )
        > 128
    ):
        raise ValueError("Too many support parser rules.")
    for row in rows(data["identity"], 256):
        exact(row, {"containsAll", "deviceType", "platform"})
        selectors(row["containsAll"])
        if row["deviceType"] not in KINDS or row["platform"] not in {"", *data["profiles"]}:
            raise ValueError("Unknown identity engine.")
    for row in rows(data["infrastructureProducts"], 1024):
        exact(row, {"name", "kind", "deviceType", "pattern", "examples", "source"})
        for field in ("name", "kind", "source"):
            text(row[field], 256)
        if not row["source"].startswith("https://") or row["deviceType"] not in DEVICE_TYPES:
            raise ValueError("Invalid product metadata.")
        expression(row["pattern"])
        for example in rows(row["examples"], 16):
            if not matches(row["pattern"], text(example, 512)):
                raise ValueError("Product recognition fixture failed.")
    for row in rows(data["fixedEquipmentProducts"], 512):
        exact(row, {"category", "product", "pattern"})
        if row["category"] not in CATEGORIES:
            raise ValueError("Unknown fixed equipment category.")
        text(row["product"], 120)
        expression(row["pattern"])
    if len(json.dumps(data).encode()) > MAX_BYTES:
        raise ValueError("Support pack exceeds its byte limit.")
    return data


def timeout(value: Any) -> None:
    if type(value) is not int or not 5 <= value <= 90:
        raise ValueError("Command timeout must be 5–90 seconds.")


def profile_for(data: dict[str, Any], platform: str, identity: str = "") -> dict[str, Any]:
    base = data["profiles"][platform]
    result = copy.deepcopy(base)
    result["sections"] = {key: result["sections"][key] for key in base["sectionOrder"]}
    result["documentation"] = {key: result["documentation"][key] for key in base["documentationOrder"]}
    candidates = [v for v in base["variants"] if selected(v["containsAll"], identity[:65536])]
    # Ambiguous variants never silently pick the first rule.
    if len(candidates) == 1:
        variant = candidates[0]
        for key in ("sections", "documentation"):
            result[key].update(variant[key])
        result["timeoutSeconds"] = variant["timeoutSeconds"]
        result["transforms"].extend(variant["transforms"])
    return result


def normalize(profile: dict[str, Any], section: str, identity: str, output: str) -> str:
    started = time.monotonic()
    for rule in profile["transforms"]:
        if rule["section"] == section and selected(rule["containsAll"], identity or output):
            if time.monotonic() - started > 0.15:
                raise ValueError("Support-pack parsing budget exceeded.")
            output = transform(rule, output)
    return output
