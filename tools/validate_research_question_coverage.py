#!/usr/bin/env python3
"""Validate complete, explicit coverage of the numbered research program."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/blueprint-v1/machine/research-question-coverage.json"
SCHEMA = ROOT / "docs/blueprint-v1/machine/research-question-coverage.schema.json"
PROGRAM = ROOT / "docs/blueprint-v1/22-research-program.md"
CROSSWALK = ROOT / "docs/blueprint-v1/machine/research-readiness-crosswalk.json"
TASK_QUEUE = ROOT / "docs/blueprint-v1/machine/build-readiness-task-queue.json"
HUMAN_AUDIT = ROOT / "docs/research/research-question-coverage-audit-2026-07.md"
PROGRESS_SNAPSHOT = ROOT / "docs/project-buildout/22-build-readiness-progress-snapshot.md"

# These rows previously passed identifier-only validation while pointing to
# unrelated research domains. Keep a small, explicit guard until the registry
# has a versioned title field shared with the Blueprint.
DEFERRED_ROUTE_TERMS: dict[str, tuple[str, ...]] = {
    "RQ-24": ("agent", "provider", "tool"),
    "RQ-26": ("network", "fetch"),
    "RQ-28": ("media", "codec", "pdf"),
    "RQ-32": ("extension", "sync"),
    "RQ-41": ("dependency", "foundation"),
    "RQ-42": ("plug-in", "wasm"),
    "RQ-43": ("embedding", "abi"),
    "RQ-51": ("resource", "tab"),
    "RQ-52": ("agent", "confirmation"),
    "RQ-58": ("readiness", "gate"),
    "RQ-59": ("agent", "authority"),
    "RQ-61": ("stable", "platform"),
    "RQ-62": ("slo", "error"),
    "RQ-65": ("service", "offline"),
}


def fail(message: str) -> None:
    print(f"research-question coverage validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def strings(value: object, label: str, minimum: int) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{label} must contain at least {minimum} non-empty strings")
    return value


def main() -> int:
    try:
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        program = PROGRAM.read_text(encoding="utf-8")
        crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
        human_audit = HUMAN_AUDIT.read_text(encoding="utf-8")
        progress_snapshot = PROGRESS_SNAPSHOT.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read source: {exc}")

    if schema.get("properties", {}).get("schema_version", {}).get("const") != 1:
        fail("schema must declare schema_version 1")
    if audit.get("schema_version") != 1 or audit.get("status") != "no_claim_research_question_coverage_audit":
        fail("audit status or schema_version is invalid")
    claim = nonempty(audit.get("claim_status"), "claim_status").lower()
    for phrase in ("no-claim", "does not", "approve", "compatibility", "performance"):
        if phrase not in claim:
            fail(f"claim_status must preserve {phrase!r} boundary")
    if not (ROOT / audit.get("program_source", "")).is_file() or not (ROOT / audit.get("crosswalk_source", "")).is_file():
        fail("program_source and crosswalk_source must resolve")
    if not (ROOT / audit.get("progress_snapshot_source", "")).is_file():
        fail("progress_snapshot_source must resolve")
    required_commands = strings(audit.get("validation_commands"), "validation_commands", 3)
    if "python3 -B tools/validate_research_question_coverage.py" not in required_commands:
        fail("validation_commands must include this validator")
    unsupported = strings(audit.get("unsupported"), "unsupported", 8)
    if not any("deferred" in value.lower() for value in unsupported):
        fail("unsupported must explain deferred-question boundaries")

    program_ids = set(re.findall(r"^## (RQ-[0-9]{2})\s+—", program, re.MULTILINE))
    if len(program_ids) != 66:
        fail(f"research program must contain 66 numbered questions, found {len(program_ids)}")
    crosswalk_ids: set[str] = set()
    research_evidence_by_question: dict[str, set[str]] = {}
    task_queue = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    task_by_id = {task.get("id"): task for task in task_queue.get("tasks", [])}
    for lane in crosswalk.get("lanes", []):
        questions = lane.get("research_questions", [])
        evidence = lane.get("evidence_start", [])
        for question in questions:
            crosswalk_ids.add(question)
            research_evidence_by_question.setdefault(question, set()).update(
                entry for entry in evidence if entry.startswith("docs/research/")
            )
    if not crosswalk_ids <= program_ids:
        fail("crosswalk contains a research question absent from the program")

    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        fail("crosswalk lanes must be a non-empty array")
    evidence_entries = 0
    for index, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            fail(f"crosswalk lanes[{index}] must be an object")
        lane_id = nonempty(lane.get("id"), f"crosswalk lanes[{index}].id")
        task_ids = strings(lane.get("tasks"), f"crosswalk {lane_id}.tasks", 1)
        requirements = strings(lane.get("requirements"), f"crosswalk {lane_id}.requirements", 1)
        risks = strings(lane.get("risks"), f"crosswalk {lane_id}.risks", 1)
        work_packages = strings(lane.get("work_packages"), f"crosswalk {lane_id}.work_packages", 0)
        expected_requirements = {
            requirement
            for task_id in task_ids
            for requirement in task_by_id.get(task_id, {}).get("requirements", [])
        }
        expected_risks = {
            risk
            for task_id in task_ids
            for risk in task_by_id.get(task_id, {}).get("risks", [])
        }
        expected_work_packages = {
            work_package
            for task_id in task_ids
            for work_package in task_by_id.get(task_id, {}).get("work_packages", [])
        }
        if set(requirements) != expected_requirements:
            fail(f"crosswalk {lane_id}.requirements must mirror its task queue bindings")
        if set(risks) != expected_risks:
            fail(f"crosswalk {lane_id}.risks must mirror its task queue bindings")
        if set(work_packages) != expected_work_packages:
            fail(f"crosswalk {lane_id}.work_packages must mirror its task queue bindings")
        evidence = strings(lane.get("evidence_start"), f"crosswalk {lane_id}.evidence_start", 1)
        strings(lane.get("next_proof"), f"crosswalk {lane_id}.next_proof", 1)
        strings(lane.get("claim_boundary"), f"crosswalk {lane_id}.claim_boundary", 1)
        for entry in evidence:
            evidence_entries += 1
            candidate = (ROOT / entry).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                fail(f"crosswalk {lane_id}.evidence_start escapes repository: {entry}")
            if not candidate.exists():
                fail(f"crosswalk {lane_id}.evidence_start does not resolve: {entry}")

    expected_audit_sentence = (
        f"The current crosswalk routes all {len(crosswalk_ids)} active questions to research evidence; "
        f"it has {len(lanes)} lanes and {evidence_entries} evidence-start entries, all of which resolve "
        "to an existing file or directory."
    )
    if expected_audit_sentence not in human_audit:
        fail("human research-question coverage audit is stale relative to the machine crosswalk")
    expected_snapshot_sentence = (
        f"Research-route coverage is mechanically checked: all `{len(crosswalk_ids)}/{len(crosswalk_ids)}` active research questions "
        f"have at least one `docs/research/` route, and all `{evidence_entries}/{evidence_entries}` crosswalk evidence paths "
        "resolve to existing repository files or directories."
    )
    if expected_snapshot_sentence not in progress_snapshot:
        fail("build-readiness progress snapshot is stale relative to the machine crosswalk")

    active = strings(audit.get("active_question_ids"), "active_question_ids", 1)
    active_set = set(active)
    if len(active_set) != len(active) or active_set != crosswalk_ids:
        fail("active_question_ids must exactly match crosswalk research_questions")
    missing_research_routes = sorted(
        question for question in active_set if not research_evidence_by_question.get(question)
    )
    if missing_research_routes:
        fail(
            "active questions must each have at least one docs/research evidence route: "
            + ", ".join(missing_research_routes)
        )
    deferred = audit.get("deferred_questions")
    if not isinstance(deferred, list):
        fail("deferred_questions must be an array")
    deferred_ids: set[str] = set()
    for index, record in enumerate(deferred):
        if not isinstance(record, dict):
            fail(f"deferred_questions[{index}] must be an object")
        question_id = nonempty(record.get("question_id"), f"deferred_questions[{index}].question_id")
        if question_id in deferred_ids:
            fail(f"duplicate deferred question: {question_id}")
        deferred_ids.add(question_id)
        if record.get("status") != "deferred_outside_current_prebuild_crosswalk":
            fail(f"deferred_questions[{index}] has invalid status")
        for key in ("reason", "owner_route", "revisit_trigger"):
            nonempty(record.get(key), f"deferred_questions[{index}].{key}")
        strings(record.get("required_future_evidence"), f"deferred_questions[{index}].required_future_evidence", 3)
        route_text = " ".join(
            [
                record["owner_route"],
                record["revisit_trigger"],
                *record["required_future_evidence"],
            ]
        ).lower()
        missing_terms = [
            term for term in DEFERRED_ROUTE_TERMS.get(question_id, ()) if term not in route_text
        ]
        if missing_terms:
            fail(
                f"deferred_questions[{index}] {question_id} route is missing semantic terms: "
                + ", ".join(missing_terms)
            )
    if deferred_ids != program_ids - active_set:
        fail("deferred_questions must exactly cover every program question outside the active crosswalk")
    if active_set & deferred_ids:
        fail("a question cannot be both active and deferred")

    route_index = audit.get("deferred_route_index")
    if not isinstance(route_index, list) or not route_index:
        fail("deferred_route_index must be a non-empty array")
    route_ids: set[str] = set()
    for index, route in enumerate(route_index):
        if not isinstance(route, dict):
            fail(f"deferred_route_index[{index}] must be an object")
        question_id = nonempty(route.get("question_id"), f"deferred_route_index[{index}].question_id")
        if question_id in route_ids:
            fail(f"duplicate deferred route index question: {question_id}")
        route_ids.add(question_id)
        if route.get("route_status") != "planned_research_route":
            fail(f"deferred_route_index[{index}] must remain planned_research_route")
        routes = strings(route.get("research_routes"), f"deferred_route_index[{index}].research_routes", 1)
        for entry in routes:
            candidate = (ROOT / entry).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                fail(f"deferred route escapes repository: {entry}")
            if not candidate.exists():
                fail(f"deferred route does not resolve: {entry}")
    if route_ids != deferred_ids:
        fail("deferred_route_index must exactly cover deferred_questions")

    print(
        f"research-question coverage validation passed: {len(program_ids)} questions, "
        f"{len(active_set)} active, {len(deferred_ids)} explicitly deferred, "
        f"{evidence_entries} crosswalk evidence paths resolved, "
        f"{len(missing_research_routes)} active questions missing research routes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
