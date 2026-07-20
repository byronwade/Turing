#!/usr/bin/env python3
"""Validate shared control fields across no-claim review templates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COMMON_FIELDS = {
    "schema_version",
    "status",
    "updated",
    "claim_status",
    "source_records",
    "review_scope",
    "rejection_rules",
    "unsupported_boundaries",
    "validation_commands",
    "owner_review_axes",
}
EXPECTED = 11


def fail(path: Path, message: str) -> None:
    raise SystemExit(f"{path}: {message}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(path, f"cannot load JSON: {exc}")
    if not isinstance(value, dict):
        fail(path, "template must be an object")
    return value


def string(path: Path, value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(path, f"{field} must be a non-empty string")
    return value


def strings(path: Path, value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(path, f"{field} must be a non-empty array")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(string(path, item, f"{field}[{index}]"))
    return result


def entries(path: Path, value: Any, field: str) -> None:
    if not isinstance(value, list) or not value:
        fail(path, f"{field} must be a non-empty array")
    for index, item in enumerate(value):
        if isinstance(item, str) and item.strip():
            continue
        if isinstance(item, dict) and item:
            continue
        fail(path, f"{field}[{index}] must be a non-empty string or object")


def validate(path: Path) -> None:
    template = load(path)
    if template.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    status = string(path, template.get("status"), "status")
    if not status.startswith("no_claim_") or not status.endswith("_template"):
        fail(path, "status must identify a no_claim template")
    updated = string(path, template.get("updated"), "updated")
    if not DATE.fullmatch(updated):
        fail(path, "updated must use YYYY-MM-DD")
    claim_status = string(path, template.get("claim_status"), "claim_status")
    if "template" not in claim_status.lower() or "no" not in claim_status.lower():
        fail(path, "claim_status must preserve the no-claim template boundary")
    identity = template.get("review_id", template.get("closure_review_id"))
    string(path, identity, "review_id or closure_review_id")
    review_scope = template.get("review_scope")
    if not isinstance(review_scope, dict) or not review_scope:
        fail(path, "review_scope must be a non-empty object")
    records = strings(path, template.get("source_records"), "source_records")
    if len(records) != len(set(records)):
        fail(path, "source_records must not contain duplicate paths")
    for record in records:
        relative = Path(record)
        if relative.is_absolute() or ".." in relative.parts:
            fail(path, f"source record must be repository-relative: {record}")
        if not (ROOT / relative).exists():
            fail(path, f"source record does not exist: {record}")
    entries(path, template.get("rejection_rules"), "rejection_rules")
    strings(path, template.get("unsupported_boundaries"), "unsupported_boundaries")
    strings(path, template.get("validation_commands"), "validation_commands")
    owner_axes = template.get("owner_review_axes", template.get("claim_review_axes"))
    if not isinstance(owner_axes, list) or not owner_axes:
        fail(path, "owner_review_axes must be a non-empty array")
    status_fields = {"readiness_status", "decision_status", "closure_status"}
    if not status_fields.intersection(template):
        fail(path, "template must expose a readiness, decision, or closure status field")
    for key, value in template.items():
        if key.endswith("_axes") and (not isinstance(value, list) or not value):
            fail(path, f"{key} must be a non-empty array")
    def reject_true(value: Any, location: str) -> None:
        if isinstance(value, bool) and value:
            fail(path, f"no-claim template contains true at {location}")
        if isinstance(value, dict):
            for child, child_value in value.items():
                reject_true(child_value, f"{location}.{child}")
        elif isinstance(value, list):
            for index, child_value in enumerate(value):
                reject_true(child_value, f"{location}[{index}]")
    reject_true(template, "$")


def main() -> int:
    paths = sorted(
        path
        for path in DOCS.rglob("no-claim-*.json")
        if any(
            marker in part
            for part in path.parts
            for marker in ("readiness-reviews", "decision-reviews", "closure-reviews")
        )
    )
    if len(paths) != EXPECTED:
        fail(DOCS, f"expected {EXPECTED} no-claim review templates, found {len(paths)}")
    for path in paths:
        validate(path)
    print(f"readiness-review template validation passed: {len(paths)} templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
