#!/usr/bin/env python3
"""Validate the implementation master plan against canonical program records."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLUEPRINT = DOCS / "blueprint-v1"
MACHINE = BLUEPRINT / "machine"
PLAN = DOCS / "project-buildout" / "implementation-plan"

PLAN_CHAPTERS = [
    "README.md",
    "01-program-sequence-and-critical-path.md",
    "02-agent-operating-protocol.md",
    "03-architecture-decisions-and-interface-freezes.md",
    "04-m0-m1-foundation-shell-security.md",
    "05-m2-static-web-engine.md",
    "06-m3-javascript-runtime.md",
    "07-m4-navigation-network-storage.md",
    "08-m5-developer-preview.md",
    "09-m6-jit-media-plugins-agents.md",
    "10-m7-beta-hardening.md",
    "11-m8-stable-release.md",
    "12-m9-parity-and-continuous-maintenance.md",
    "13-cross-cutting-verification-and-evidence.md",
    "14-staffing-delivery-and-capacity.md",
    "15-stop-replan-and-risk-controls.md",
    "16-work-package-playbooks.md",
    "17-delivery-checklists-and-handoffs.md",
]

MACHINE_FILES = {
    "graph": MACHINE / "implementation-execution-graph.json",
    "milestones": MACHINE / "implementation-milestone-gates.json",
    "freezes": MACHINE / "implementation-interface-freezes.json",
    "evidence": MACHINE / "implementation-evidence-catalog.json",
    "sequence": MACHINE / "implementation-task-sequence.json",
    "backlog": MACHINE / "backlog.json",
    "prebuild": MACHINE / "pre-build-readiness.json",
}

EXPECTED_EVIDENCE = [
    "EV-SPEC",
    "EV-UNIT",
    "EV-CONFORMANCE",
    "EV-SECURITY",
    "EV-PRIVACY",
    "EV-PERF",
    "EV-A11Y",
    "EV-RELIABILITY",
    "EV-COMPAT",
    "EV-OPERATIONS",
    "EV-DOCS",
]


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        fail(f"{path.relative_to(ROOT)} must be a schema_version 1 object")
    return payload


def check_files_and_index() -> None:
    missing = [name for name in PLAN_CHAPTERS if not (PLAN / name).is_file()]
    if missing:
        fail("missing implementation-plan chapters: " + ", ".join(missing))
    missing_machine = [
        path.relative_to(ROOT) for path in MACHINE_FILES.values() if not path.is_file()
    ]
    if missing_machine:
        fail("missing implementation machine records: " + ", ".join(map(str, missing_machine)))

    index = (PLAN / "README.md").read_text(encoding="utf-8")
    for name in PLAN_CHAPTERS[1:]:
        if f"]({name})" not in index:
            fail(f"implementation-plan README does not link {name}")

    required_inbound = {
        ROOT / "README.md": "docs/project-buildout/implementation-plan/README.md",
        ROOT / "AGENTS.md": "docs/project-buildout/implementation-plan/README.md",
        DOCS / "README.md": "project-buildout/implementation-plan/README.md",
        DOCS / "project-buildout" / "README.md": "implementation-plan/README.md",
        BLUEPRINT / "14-roadmap-work-breakdown.md": "project-buildout/implementation-plan/README.md",
        BLUEPRINT / "19-initial-backlog.md": "project-buildout/implementation-plan/README.md",
    }
    for path, marker in required_inbound.items():
        if marker not in path.read_text(encoding="utf-8"):
            fail(f"{path.relative_to(ROOT)} does not link the implementation master plan")


def check_graph() -> None:
    backlog = load_json(MACHINE_FILES["backlog"])
    graph = load_json(MACHINE_FILES["graph"])
    requirements = load_json(MACHINE / "requirements.json")
    backlog_items = backlog.get("work_packages") or backlog.get("items")
    nodes = graph.get("nodes")
    if not isinstance(backlog_items, list) or not all(isinstance(item, dict) for item in backlog_items):
        fail("backlog.json must contain work_packages")
    if not isinstance(nodes, list) or not all(isinstance(item, dict) for item in nodes):
        fail("implementation-execution-graph.json must contain nodes")

    backlog_map = {str(item.get("id")): item for item in backlog_items}
    graph_map = {str(item.get("id")): item for item in nodes}
    expected_ids = [f"WP-{index:03d}" for index in range(1, 21)]
    if list(backlog_map) != expected_ids:
        fail(f"backlog work packages must be WP-001 through WP-020; found {list(backlog_map)}")
    if list(graph_map) != expected_ids:
        fail(f"execution graph nodes must be WP-001 through WP-020; found {list(graph_map)}")

    for identifier in expected_ids:
        backlog_item = backlog_map[identifier]
        graph_item = graph_map[identifier]
        if graph_item.get("milestone") != backlog_item.get("milestone"):
            fail(f"{identifier}: milestone differs between backlog and execution graph")
        if graph_item.get("depends_on") != backlog_item.get("depends_on"):
            fail(f"{identifier}: dependencies differ between backlog and execution graph")
        gates = graph_item.get("decision_gates")
        if not isinstance(gates, list) or not all(isinstance(item, str) for item in gates):
            fail(f"{identifier}: decision_gates must be a string array")

    for identifier, item in graph_map.items():
        for dependency in item["depends_on"]:
            if dependency not in graph_map:
                fail(f"{identifier}: unknown dependency {dependency}")

    requirement_items = requirements.get("requirements")
    if not isinstance(requirement_items, list) or not all(isinstance(item, dict) for item in requirement_items):
        fail("requirements.json must contain requirements")
    requirement_ids = {str(item.get("id")) for item in requirement_items}
    covered_requirements: set[str] = set()
    playbooks = (PLAN / "16-work-package-playbooks.md").read_text(encoding="utf-8")
    for identifier, item in backlog_map.items():
        mapped = item.get("requirements")
        if not isinstance(mapped, list) or not all(isinstance(value, str) for value in mapped):
            fail(f"{identifier}: requirements must be a string array")
        unknown = set(mapped) - requirement_ids
        if unknown:
            fail(f"{identifier}: unknown requirements: {', '.join(sorted(unknown))}")
        covered_requirements.update(mapped)
        section = re.search(rf"(?ms)^## {re.escape(identifier)} .*?(?=^## WP-|\Z)", playbooks)
        if section is None:
            fail(f"{identifier}: missing execution playbook section")
        for label in ("Acceptance:", "Negative tests:", "Handoff:", "Not supported:"):
            if label not in section.group(0):
                fail(f"{identifier}: playbook missing {label}")
    if covered_requirements != requirement_ids:
        missing = sorted(requirement_ids - covered_requirements)
        fail("requirements lack work-package coverage: " + ", ".join(missing))


def check_milestones() -> None:
    payload = load_json(MACHINE_FILES["milestones"])
    items = payload.get("milestones")
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        fail("implementation-milestone-gates.json must contain milestones")
    ids = [item.get("id") for item in items]
    expected = [f"M{index}" for index in range(10)]
    if ids != expected:
        fail(f"milestone IDs must be M0 through M9; found {ids}")
    for item in items:
        for field in ("entry", "blocking_outputs", "exit_evidence", "prohibited_claims"):
            value = item.get(field)
            if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
                fail(f"{item.get('id')}: {field} must be a string array")


def check_freezes_and_evidence() -> None:
    freezes = load_json(MACHINE_FILES["freezes"]).get("freezes")
    if not isinstance(freezes, list) or not all(isinstance(item, dict) for item in freezes):
        fail("implementation-interface-freezes.json must contain freezes")
    ids = [item.get("id") for item in freezes]
    expected = [f"IF-{index:03d}" for index in range(8)]
    if ids != expected:
        fail(f"interface freeze IDs must be IF-000 through IF-007; found {ids}")

    classes = load_json(MACHINE_FILES["evidence"]).get("classes")
    if not isinstance(classes, list) or not all(isinstance(item, dict) for item in classes):
        fail("implementation-evidence-catalog.json must contain classes")
    class_ids = [item.get("id") for item in classes]
    if class_ids != EXPECTED_EVIDENCE:
        fail(f"evidence classes differ from canonical order: {class_ids}")


def check_sequence_and_status() -> None:
    sequence = load_json(MACHINE_FILES["sequence"])
    waves = sequence.get("waves")
    if not isinstance(waves, list) or not all(isinstance(item, dict) for item in waves):
        fail("implementation-task-sequence.json must contain waves")
    ids = [item.get("id") for item in waves]
    expected = [f"WAVE-{index:02d}" for index in range(11)]
    if ids != expected:
        fail(f"implementation waves must be WAVE-00 through WAVE-10; found {ids}")
    if "Only a separately reviewed TASK manifest" not in str(sequence.get("rule")):
        fail("task sequence must state that it does not authorize implementation")

    prebuild = load_json(MACHINE_FILES["prebuild"])
    if prebuild.get("status") != "not_ready_for_broad_implementation":
        fail("implementation plan must not promote broad implementation readiness")
    plan = prebuild.get("implementation_plan")
    if not isinstance(plan, dict) or plan.get("status") != "ready_as_execution_documentation":
        fail("pre-build readiness must record execution documentation status")
    if prebuild.get("contained_m0_authorization") != "ready":
        fail("contained M0 authorization unexpectedly changed")

    release = load_json(DOCS / "production-readiness" / "machine" / "release-gates.json")
    if release.get("status") != "not_ready_for_production":
        fail("implementation documentation must not promote production readiness")


def check_roadmap_numbering() -> None:
    roadmap = (BLUEPRINT / "14-roadmap-work-breakdown.md").read_text(encoding="utf-8")
    section = roadmap.split("## 13. Canonical work packages", 1)
    if len(section) != 2:
        fail("roadmap lacks canonical work-package section")
    ids = re.findall(r"\*\*(WP-\d{3}) —", section[1])
    expected = [f"WP-{index:03d}" for index in range(1, 21)]
    if ids[:20] != expected:
        fail(f"roadmap WP numbering is not synchronized: {ids[:20]}")


def main() -> int:
    try:
        check_files_and_index()
        check_graph()
        check_milestones()
        check_freezes_and_evidence()
        check_sequence_and_status()
        check_roadmap_numbering()
    except ValueError as error:
        print(f"implementation plan validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "implementation plan validation passed: "
        "20 work packages, 10 milestones, 8 interface freezes, "
        "11 evidence classes, 11 planned waves"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
