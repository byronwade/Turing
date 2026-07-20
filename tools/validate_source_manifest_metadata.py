#!/usr/bin/env python3
"""Validate shared freshness and identity invariants for source manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(path: Path, message: str) -> None:
    raise SystemExit(f"{path}: {message}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(path, f"cannot load JSON: {exc}")
    if not isinstance(value, dict):
        fail(path, "manifest must be an object")
    return value


def require_string(path: Path, value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(path, f"{field} must be a non-empty string")
    return value


def require_date(path: Path, value: Any, field: str) -> str:
    value = require_string(path, value, field)
    if not DATE.fullmatch(value):
        fail(path, f"{field} must use YYYY-MM-DD")
    return value


def validate(path: Path) -> None:
    manifest = load(path)
    updated = require_date(path, manifest.get("updated"), "updated")
    sources = manifest.get("sources")
    documents = manifest.get("source_documents")
    if not isinstance(sources, list) or not sources:
        fail(path, "sources must be a non-empty array")
    if not isinstance(documents, list) or not documents:
        fail(path, "source_documents must be a non-empty array")

    source_ids: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            fail(path, f"sources[{index}] must be an object")
        source_id = require_string(path, source.get("source_id"), f"sources[{index}].source_id")
        if source_id in source_ids:
            fail(path, f"duplicate source_id: {source_id}")
        source_ids.append(source_id)
        for field in ("title", "publisher", "url"):
            require_string(path, source.get(field), f"sources[{index}].{field}")
        observation = source.get("observation", source.get("scope"))
        require_string(path, observation, f"sources[{index}].observation_or_scope")
        consequence_fields = [key for key in source if key.endswith("_consequence")]
        if not consequence_fields or not any(
            isinstance(source[key], str) and source[key].strip()
            for key in consequence_fields
        ):
            fail(path, f"sources[{index}] must have a non-empty *_consequence field")
        retrieved = require_date(
            path, source.get("retrieved"), f"sources[{index}].retrieved"
        )
        if retrieved > updated:
            fail(path, f"sources[{index}].retrieved is newer than updated")

    document_paths: list[str] = []
    for index, document in enumerate(documents):
        document_path = require_string(path, document, f"source_documents[{index}]")
        relative = Path(document_path)
        if relative.is_absolute() or ".." in relative.parts:
            fail(path, f"source_documents[{index}] must be repository-relative")
        if document_path in document_paths:
            fail(path, f"duplicate source document: {document_path}")
        document_paths.append(document_path)
        if not (ROOT / relative).is_file():
            fail(path, f"source document does not exist: {document_path}")


def main() -> int:
    paths = sorted(DOCS.rglob("*-source-manifest.json"))
    paths.append(DOCS / "blueprint-v1" / "machine" / "adr-0009-source-observation-manifest.json")
    paths = [path for path in paths if path.name != "design-source-manifest.json"]
    if len(paths) != 12:
        fail(DOCS, f"expected 12 source manifests, found {len(paths)}")
    for path in paths:
        validate(path)
    print(f"source-manifest metadata validation passed: {len(paths)} manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
