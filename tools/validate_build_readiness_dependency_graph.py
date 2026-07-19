#!/usr/bin/env python3
"""Validate the checked no-claim build-readiness dependency graph."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MACHINE = DOCS / "blueprint-v1" / "machine"
DEFAULT_GRAPH = (
    DOCS / "project-buildout" / "machine" / "build-readiness-dependency-graph.json"
)

GRAPH_ID = re.compile(r"^PB020\.DEPENDENCY_GRAPH\.[A-Z0-9._-]+$")

REQUIRED_READINESS_ITEMS = {
    "PB-002": "blocked",
    "PB-003": "partial",
    "PB-004": "partial",
    "PB-005": "partial",
    "PB-008": "partial",
    "PB-009": "partial",
    "PB-011": "partial",
    "PB-012": "partial",
    "PB-013": "documented_no_runner",
    "PB-014": "partial",
    "PB-015": "partial",
    "PB-016": "partial",
    "PB-017": "partial",
    "PB-018": "partial",
    "PB-019": "blocked",
    "PB-020": "partial",
}

REQUIRED_TASKS = {f"TASK-{number:06d}" for number in range(1, 11)}

REQUIRED_SOURCE_RECORDS = {
    "docs/project-buildout/11-pre-build-readiness-checklist.md",
    "docs/project-buildout/13-build-readiness-operating-board.md",
    "docs/project-buildout/17-build-readiness-task-queue.md",
    "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
    "docs/project-buildout/23-owner-decision-closure-board.md",
    "docs/research/implementation-kickoff-review-inventory-2026-07.md",
    "docs/project-buildout/machine/implementation-kickoff-review.json",
    "docs/blueprint-v1/machine/pre-build-readiness.json",
    "docs/blueprint-v1/machine/build-readiness-task-queue.json",
    "docs/blueprint-v1/machine/research-readiness-crosswalk.json",
    "docs/blueprint-v1/machine/backlog.json",
    "docs/agent-execution/README.md",
    "docs/production-readiness/README.md",
    "docs/blueprint-v1/20-definition-of-done.md",
}

REQUIRED_NODES = {
    "PB-GATE-0",
    *REQUIRED_READINESS_ITEMS.keys(),
    *REQUIRED_TASKS,
    "ADR-0009",
    "ADR-0013",
    "ADR-0014",
    "ADR-0016",
    "UI-GATE-7",
}

REQUIRED_READINESS_TO_TASK_EDGES = {
    ("PB-002", "TASK-000001"),
    ("PB-008", "TASK-000002"),
    ("PB-009", "TASK-000002"),
    ("PB-011", "TASK-000003"),
    ("PB-012", "TASK-000004"),
    ("PB-013", "TASK-000005"),
    ("PB-003", "TASK-000006"),
    ("PB-004", "TASK-000006"),
    ("PB-005", "TASK-000006"),
    ("PB-014", "TASK-000006"),
    ("PB-015", "TASK-000006"),
    ("PB-016", "TASK-000007"),
    ("PB-019", "TASK-000008"),
    ("PB-017", "TASK-000009"),
    ("PB-018", "TASK-000010"),
}

REQUIRED_DECISION_EDGES = {
    ("ADR-0009", "PB-002"),
    ("ADR-0013", "PB-003"),
    ("ADR-0014", "PB-004"),
    ("ADR-0016", "PB-005"),
    ("UI-GATE-7", "PB-005"),
    ("UI-GATE-7", "PB-015"),
}

REQUIRED_PARALLEL_LANES = {
    "source-strategy-research",
    "fresh-host-reproduction",
    "ipc-and-sandbox-prototypes",
    "benchmark-lab-contracts",
    "native-shell-research",
    "profile-package-incident-ownership",
}

REQUIRED_CLAIM_PHRASES = [
    "no task approval",
    "no readiness promotion",
    "no broad m1 implementation",
    "no developer preview",
    "no beta",
    "no stable",
    "no production",
    "no chrome-class",
    "no performance",
    "no compatibility",
    "no security",
    "no accessibility",
    "no release readiness",
    "no daily-driver",
]

REQUIRED_PB020_EVIDENCE = [
    "docs/research/build-readiness-dependency-graph-inventory-2026-07.md",
    "docs/project-buildout/machine/build-readiness-dependency-graph.schema.json",
    "docs/project-buildout/machine/build-readiness-dependency-graph.json",
    "tools/validate_build_readiness_dependency_graph.py",
]

REQUIRED_PB020_REQUIRED_TERMS = [
    "build-readiness dependency graph",
    "dependency graph",
    "remaining p0 items",
    "source strategy",
    "fresh-host",
    "ipc",
    "sandbox",
    "benchmark",
    "native-shell",
    "profile/session",
    "package/update",
    "incident response",
    "backup ownership",
    "owner review",
    "release authority",
]


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def require_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        fail(f"{key} must be a non-empty array")
    return value


def normalize(value: str) -> str:
    normalized = value.lower().replace("_", "-")
    for old, new in [
        ("m1", "m1"),
        ("chrome class", "chrome-class"),
        ("fresh host", "fresh-host"),
        ("source-strategy", "source strategy"),
        ("profile session", "profile/session"),
        ("profile-session", "profile/session"),
        ("package update", "package/update"),
        ("package-update", "package/update"),
        ("incident-response", "incident response"),
        ("backup-ownership", "backup ownership"),
    ]:
        normalized = normalized.replace(old, new)
    return normalized


def check_no_duplicates(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        fail(f"duplicate {label}: {', '.join(duplicates)}")


def validate_graph(path: Path) -> None:
    data = load_json(path)
    if not isinstance(data, dict):
        fail(f"{path}: graph must be an object")
    if data.get("schema_version") != 1:
        fail(f"{path}: schema_version must be 1")
    graph_id = text(data.get("graph_id"))
    if not GRAPH_ID.fullmatch(graph_id):
        fail(f"{path}: invalid graph_id {graph_id!r}")
    if data.get("status") != "no_claim_dependency_graph":
        fail(f"{path}: status must be no_claim_dependency_graph")

    boundary_text = normalize(
        " ".join(
            [
                text(data.get("claim_status")),
                *[text(value) for value in require_list(data, "unsupported_boundaries")],
            ]
        )
    )
    for phrase in REQUIRED_CLAIM_PHRASES:
        if phrase not in boundary_text:
            fail(f"{path}: missing claim boundary phrase: {phrase}")

    source_records = set(text(value) for value in require_list(data, "source_records"))
    missing_sources = sorted(REQUIRED_SOURCE_RECORDS - source_records)
    if missing_sources:
        fail(f"{path}: missing source records: {', '.join(missing_sources)}")
    for source in REQUIRED_SOURCE_RECORDS:
        if not (ROOT / source).exists():
            fail(f"{path}: referenced source record does not exist: {source}")

    readiness_by_id = load_readiness()
    task_by_id = load_tasks()

    nodes = require_list(data, "nodes")
    node_by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        if not isinstance(node, dict):
            fail(f"{path}: nodes entries must be objects")
        node_id = text(node.get("id"))
        if node_id in node_by_id:
            fail(f"{path}: duplicate node {node_id}")
        node_by_id[node_id] = node
        for key in ["summary", "claim_boundary"]:
            if len(text(node.get(key))) < 20:
                fail(f"{path}: node {node_id} has short {key}")
        source_ref = text(node.get("source_ref")).split("#", 1)[0]
        if not (ROOT / source_ref).exists():
            fail(f"{path}: node {node_id} source_ref does not exist: {source_ref}")

    missing_nodes = sorted(REQUIRED_NODES - set(node_by_id))
    if missing_nodes:
        fail(f"{path}: missing required nodes: {', '.join(missing_nodes)}")

    for item_id, expected_status in REQUIRED_READINESS_ITEMS.items():
        node = node_by_id[item_id]
        if node.get("type") != "readiness_item":
            fail(f"{path}: {item_id} must be a readiness_item node")
        registry_item = readiness_by_id[item_id]
        if node.get("status") != expected_status:
            fail(f"{path}: {item_id} node status must be {expected_status}")
        if registry_item.get("status") != expected_status:
            fail(f"pre-build-readiness.json: {item_id} status drifted")
        if node.get("owner_scope") != registry_item.get("owner_scope"):
            fail(f"{path}: {item_id} owner_scope does not match readiness registry")

    for task_id in REQUIRED_TASKS:
        node = node_by_id[task_id]
        if node.get("type") != "task":
            fail(f"{path}: {task_id} must be a task node")
        task = task_by_id[task_id]
        if node.get("status") != task.get("status"):
            fail(f"{path}: {task_id} status does not match task queue")
        if node.get("owner_scope") != task.get("owner"):
            fail(f"{path}: {task_id} owner_scope does not match task queue owner")

    for decision_id in ["ADR-0009", "ADR-0013", "ADR-0014", "ADR-0016"]:
        if node_by_id[decision_id].get("type") != "decision":
            fail(f"{path}: {decision_id} must be a decision node")
    if node_by_id["UI-GATE-7"].get("type") != "evidence_gate":
        fail(f"{path}: UI-GATE-7 must be an evidence_gate node")

    edges = require_list(data, "edges")
    edge_pairs_by_type: dict[str, set[tuple[str, str]]] = {}
    edge_keys: list[str] = []
    for edge in edges:
        if not isinstance(edge, dict):
            fail(f"{path}: edges entries must be objects")
        source = text(edge.get("from"))
        target = text(edge.get("to"))
        edge_type = text(edge.get("type"))
        if source not in node_by_id:
            fail(f"{path}: edge references missing source node {source}")
        if target not in node_by_id:
            fail(f"{path}: edge references missing target node {target}")
        edge_keys.append(f"{source}->{target}:{edge_type}")
        edge_pairs_by_type.setdefault(edge_type, set()).add((source, target))
        if len(text(edge.get("reason"))) < 20:
            fail(f"{path}: edge {source}->{target} has short reason")
        if "claim" not in normalize(text(edge.get("no_claim_boundary"))):
            fail(f"{path}: edge {source}->{target} no_claim_boundary must mention claim")
    check_no_duplicates(edge_keys, "edge")

    task_dependency_edges = edge_pairs_by_type.get("task_dependency", set())
    for task_id, task in task_by_id.items():
        for dependency in task.get("dependencies", []):
            if (dependency, task_id) not in task_dependency_edges:
                fail(f"{path}: missing task dependency edge {dependency}->{task_id}")

    readiness_to_task_edges = edge_pairs_by_type.get("readiness_to_task", set())
    missing_readiness_edges = sorted(
        REQUIRED_READINESS_TO_TASK_EDGES - readiness_to_task_edges
    )
    if missing_readiness_edges:
        fail(f"{path}: missing readiness_to_task edges: {missing_readiness_edges}")

    decision_edges = edge_pairs_by_type.get("decision_required", set())
    missing_decision_edges = sorted(REQUIRED_DECISION_EDGES - decision_edges)
    if missing_decision_edges:
        fail(f"{path}: missing decision_required edges: {missing_decision_edges}")

    kickoff_edges = edge_pairs_by_type.get("kickoff_dependency", set())
    for item_id in REQUIRED_READINESS_ITEMS:
        if item_id == "PB-020":
            continue
        if (item_id, "PB-020") not in kickoff_edges:
            fail(f"{path}: missing kickoff dependency edge {item_id}->PB-020")

    lanes = require_list(data, "parallel_no_claim_lanes")
    lane_ids = [text(lane.get("id")) for lane in lanes if isinstance(lane, dict)]
    check_no_duplicates(lane_ids, "parallel lane ids")
    missing_lanes = sorted(REQUIRED_PARALLEL_LANES - set(lane_ids))
    if missing_lanes:
        fail(f"{path}: missing parallel no-claim lanes: {', '.join(missing_lanes)}")
    for lane in lanes:
        if not isinstance(lane, dict):
            fail(f"{path}: parallel_no_claim_lanes entries must be objects")
        stop_text = normalize(text(lane.get("must_stop_before")))
        for phrase in ["stop", "claim"]:
            if phrase not in stop_text:
                fail(f"{path}: lane {lane.get('id')} must_stop_before must mention {phrase}")

    check_readiness_pb020()


def load_readiness() -> dict[str, dict[str, Any]]:
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    if not isinstance(readiness, dict):
        fail("pre-build-readiness.json must be an object")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain items")
    by_id = {item.get("id"): item for item in items if isinstance(item, dict)}
    for item_id in REQUIRED_READINESS_ITEMS:
        if item_id not in by_id:
            fail(f"pre-build-readiness.json missing {item_id}")
    return by_id


def load_tasks() -> dict[str, dict[str, Any]]:
    queue = load_json(MACHINE / "build-readiness-task-queue.json")
    if not isinstance(queue, dict):
        fail("build-readiness-task-queue.json must be an object")
    tasks = queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    by_id = {task.get("id"): task for task in tasks if isinstance(task, dict)}
    missing = sorted(REQUIRED_TASKS - set(by_id))
    if missing:
        fail(f"build-readiness-task-queue.json missing tasks: {', '.join(missing)}")
    return by_id


def check_readiness_pb020() -> None:
    readiness = load_readiness()
    pb020 = readiness["PB-020"]
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial while dependency graph is no-claim")
    evidence = pb020.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-020 evidence must be an array")
    missing = [value for value in REQUIRED_PB020_EVIDENCE if value not in evidence]
    if missing:
        fail("PB-020 evidence is missing dependency graph files: " + ", ".join(missing))
    evidence_required = normalize(
        " ".join(value for value in pb020.get("evidence_required", []) if isinstance(value, str))
    )
    for term in REQUIRED_PB020_REQUIRED_TERMS:
        if term not in evidence_required:
            fail(f"PB-020 evidence_required must mention {term}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "graph",
        nargs="?",
        type=Path,
        default=DEFAULT_GRAPH,
        help="Path to build-readiness-dependency-graph.json",
    )
    args = parser.parse_args(argv)
    validate_graph(args.graph)
    print("build readiness dependency graph validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
