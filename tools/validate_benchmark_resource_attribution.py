#!/usr/bin/env python3
"""Validate benchmark resource-attribution taxonomy manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
MANIFEST_DIR = MACHINE / "benchmark-resource-attribution"
DEFAULT_MANIFESTS = [MANIFEST_DIR / "semantic-owners.v1.json"]

RESOURCE_ATTRIBUTION_ID = re.compile(
    r"^TURING\.BENCHMARK\.RESOURCE_ATTRIBUTION\.[A-Z0-9._-]+$"
)
OWNER_ID = re.compile(r"^[a-z0-9][a-z0-9-]+$")

REQUIRED_OWNER_IDS = [
    "browser-ui-profile",
    "document-frame-site-instance",
    "javascript-heap-code-metadata",
    "dom-style-layout-paint-accessibility",
    "images-fonts-canvas-media",
    "network-buffers-cache",
    "storage-transactions-mappings",
    "gpu-textures-buffers-pipelines",
    "extension",
    "devtools",
    "agent-model",
    "shared-service",
    "unknown",
]

REQUIRED_METRIC_IDS = {
    "cpu_time_ns",
    "queue_wait_ns",
    "wakeups",
    "private_working_set_bytes",
    "resident_bytes",
    "committed_bytes",
    "shared_bytes",
    "compressed_bytes",
    "swap_bytes",
    "gpu_allocated_bytes",
    "network_bytes",
    "disk_io_bytes",
    "energy_estimate_joules",
    "model_tokens",
    "provider_cost_estimate",
}

REQUIRED_RULE_IDS = {"direct", "sampled", "shared_charged", "unknown"}


class ValidationError(ValueError):
    pass


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{relative(path)}: {message}")


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(path, f"invalid JSON: {error}")


def require_object(path: Path, value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(path, f"{label} must be an object")
    return value


def reject_extra(path: Path, obj: dict[str, object], allowed: set[str], label: str) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(path: Path, obj: dict[str, object], required: set[str], label: str) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str, *, min_items: int = 0
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        fail(path, f"{label}.{key} must be an array of non-empty strings")
    if len(value) < min_items:
        fail(path, f"{label}.{key} must contain at least {min_items} item(s)")
    return value


def validate_owner_classes(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "owner_classes must be a non-empty array")
    allowed = {
        "id",
        "title",
        "principal_scope",
        "charge_policy",
        "required_metrics",
        "examples",
    }
    seen: list[str] = []
    for index, item in enumerate(value, start=1):
        owner = require_object(path, item, f"owner_classes[{index}]")
        reject_extra(path, owner, allowed, f"owner_classes[{index}]")
        require_keys(path, owner, allowed, f"owner_classes[{index}]")
        owner_id = require_string(path, owner, "id", f"owner_classes[{index}]")
        if not OWNER_ID.fullmatch(owner_id):
            fail(path, f"owner_classes[{index}].id has invalid format")
        seen.append(owner_id)
        for key in ["title", "principal_scope", "charge_policy"]:
            require_string(path, owner, key, f"owner_classes[{index}]")
        metrics = require_string_array(
            path, owner, "required_metrics", f"owner_classes[{index}]", min_items=1
        )
        unknown = sorted(set(metrics) - REQUIRED_METRIC_IDS)
        if unknown:
            fail(
                path,
                f"owner_classes[{index}].required_metrics contains unknown metrics: "
                + ", ".join(unknown),
            )
        require_string_array(
            path, owner, "examples", f"owner_classes[{index}]", min_items=1
        )
    if seen != REQUIRED_OWNER_IDS:
        fail(path, "owner_classes must match the required semantic owner order")


def validate_metrics(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "metrics must be a non-empty array")
    allowed = {"id", "unit", "kind", "required_scope"}
    seen: set[str] = set()
    for index, item in enumerate(value, start=1):
        metric = require_object(path, item, f"metrics[{index}]")
        reject_extra(path, metric, allowed, f"metrics[{index}]")
        require_keys(path, metric, allowed, f"metrics[{index}]")
        metric_id = require_string(path, metric, "id", f"metrics[{index}]")
        seen.add(metric_id)
        for key in ["unit", "kind", "required_scope"]:
            require_string(path, metric, key, f"metrics[{index}]")
    missing = sorted(REQUIRED_METRIC_IDS - seen)
    if missing:
        fail(path, "metrics are missing required ids: " + ", ".join(missing))


def validate_rules(path: Path, value: object) -> None:
    if not isinstance(value, list) or not value:
        fail(path, "attribution_rules must be a non-empty array")
    allowed = {"id", "description"}
    seen: set[str] = set()
    for index, item in enumerate(value, start=1):
        rule = require_object(path, item, f"attribution_rules[{index}]")
        reject_extra(path, rule, allowed, f"attribution_rules[{index}]")
        require_keys(path, rule, allowed, f"attribution_rules[{index}]")
        seen.add(require_string(path, rule, "id", f"attribution_rules[{index}]"))
        require_string(path, rule, "description", f"attribution_rules[{index}]")
    if seen != REQUIRED_RULE_IDS:
        fail(path, "attribution_rules must include direct, sampled, shared_charged, and unknown")


def validate_string_object(
    path: Path, value: object, label: str, required: set[str]
) -> None:
    obj = require_object(path, value, label)
    reject_extra(path, obj, required, label)
    require_keys(path, obj, required, label)
    for key in sorted(required):
        value = obj[key]
        if isinstance(value, list):
            if not value or any(not isinstance(item, str) or not item for item in value):
                fail(path, f"{label}.{key} must be a non-empty string array")
        elif not isinstance(value, str) or not value:
            fail(path, f"{label}.{key} must be a non-empty string")


def validate_manifest(path: Path, payload: object) -> None:
    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "resource_attribution_id",
        "status",
        "claim_status",
        "owner_classes",
        "metrics",
        "attribution_rules",
        "shared_resource_policy",
        "collection_plan",
        "ui_reporting_contract",
        "unsupported_behavior",
        "evidence_required",
        "external_sources",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    resource_id = require_string(path, manifest, "resource_attribution_id", "manifest")
    if not RESOURCE_ATTRIBUTION_ID.fullmatch(resource_id):
        fail(path, "resource_attribution_id has invalid format")
    status = require_string(path, manifest, "status", "manifest")
    if status not in {"taxonomy_draft_no_instrumentation", "draft", "reviewed", "retired"}:
        fail(path, "status must be taxonomy_draft_no_instrumentation, draft, reviewed, or retired")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")

    validate_owner_classes(path, manifest.get("owner_classes"))
    validate_metrics(path, manifest.get("metrics"))
    validate_rules(path, manifest.get("attribution_rules"))
    validate_string_object(
        path,
        manifest.get("shared_resource_policy"),
        "shared_resource_policy",
        {"physical_total_rule", "charged_total_rule", "privacy_rule", "claim_rule"},
    )
    validate_string_object(
        path,
        manifest.get("collection_plan"),
        "collection_plan",
        {
            "minimum_browser_trace_fields",
            "minimum_platform_artifacts",
            "unsupported_collection",
        },
    )
    validate_string_object(
        path,
        manifest.get("ui_reporting_contract"),
        "ui_reporting_contract",
        {"required_views", "required_disclosures", "prohibited_ui_claims"},
    )
    unsupported = require_string_array(
        path, manifest, "unsupported_behavior", "manifest", min_items=1
    )
    for phrase in [
        "taxonomy only; no instrumentation exists",
        "no benchmark result or performance claim is supported",
    ]:
        if phrase not in unsupported:
            fail(path, f"unsupported_behavior must mention: {phrase}")
    require_string_array(path, manifest, "evidence_required", "manifest", min_items=1)
    external_sources = require_string_array(
        path, manifest, "external_sources", "manifest", min_items=1
    )
    required_source_markers = [
        "chromium.googlesource.com/chromium/src",
        "perfetto.dev/docs",
        "developer.chrome.com/docs/devtools/performance-monitor",
        "learn.microsoft.com/en-us/windows-hardware/test/wpt",
    ]
    for marker in required_source_markers:
        if not any(marker in source for source in external_sources):
            fail(path, f"external_sources must include {marker}")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else DEFAULT_MANIFESTS
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark resource-attribution validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark resource-attribution validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
