#!/usr/bin/env python3
"""Validate the captured Nova design source against its no-claim manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "ui-runtime" / "machine" / "design-source-manifest.json"
SCHEMA = ROOT / "docs" / "ui-runtime" / "machine" / "design-source-manifest.schema.json"
TOKENS = ROOT / "design" / "tokens.json"


def fail(message: str) -> None:
    print(f"design-source validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read manifest or schema: {exc}")

    if schema.get("properties", {}).get("schema_version", {}).get("const") != 1:
        fail("manifest schema must declare schema_version 1")
    missing = [key for key in schema.get("required", []) if key not in manifest]
    if missing:
        fail(f"manifest fields missing: {', '.join(missing)}")
    if manifest.get("schema_version") != 1:
        fail("manifest schema_version is not 1")
    if manifest.get("status") != "primary_visual_reference_no_claim":
        fail("manifest status must remain primary_visual_reference_no_claim")

    source = ROOT / manifest["source_path"]
    if not source.is_file():
        fail(f"source file is missing: {manifest['source_path']}")
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest().upper()
    if digest != manifest["sha256"]:
        fail(f"SHA-256 mismatch: expected {manifest['sha256']}, got {digest}")
    if len(data) != manifest["byte_length"]:
        fail(f"byte length mismatch: expected {manifest['byte_length']}, got {len(data)}")
    line_count = len(source.read_text(encoding="utf-8").splitlines())
    if line_count != manifest["line_count"]:
        fail(f"line count mismatch: expected {manifest['line_count']}, got {line_count}")

    try:
        tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read shared design tokens: {exc}")
    if tokens.get("source") != manifest["source_path"]:
        fail("shared design tokens point at a different source path")
    if tokens.get("source_sha256") != digest:
        fail(
            "shared design tokens are stale: "
            f"expected source_sha256 {digest}, got {tokens.get('source_sha256')}"
        )

    print(
        "design-source validation passed: "
        f"{manifest['source_path']} sha256={digest} "
        f"bytes={len(data)} lines={line_count} tokens-provenance-ok no-claim"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
