#!/usr/bin/env python3
"""Validate no-claim benchmark tab scenario manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "docs" / "blueprint-v1" / "machine"
DEFAULT_MANIFEST = (
    MACHINE
    / "benchmark-tab-scenarios"
    / "no-claim-30-tab-smoke.scenarios.json"
)
CORPUS_MANIFEST = MACHINE / "benchmark-corpora" / "no-claim-smoke.corpus.json"
NETWORK_PROFILE = (
    MACHINE / "benchmark-network-profiles" / "no-claim-local-static.profile.json"
)
RESOURCE_ATTRIBUTION = (
    MACHINE / "benchmark-resource-attribution" / "semantic-owners.v1.json"
)

SCENARIO_SET_ID = re.compile(r"^TURING\.BENCHMARK\.TAB_SCENARIOS\.[A-Z0-9._-]+$")
SCENARIO_ID = re.compile(r"^PB13-TABS-[A-Z0-9._-]+$")
GROUP_ID = re.compile(r"^PB13-TAB-GROUP-[A-Z0-9._-]+$")
CASE_ID = re.compile(r"^PB13-CORPUS-[A-Z0-9._-]+$")
STATES = {
    "active",
    "background",
    "throttled",
    "frozen",
    "serialized",
    "discarded",
    "crashed",
}
SCENARIO_KINDS = {"thirty_tab_mixed_state", "thirty_tab_all_live"}
STATUS_VALUES = {"sample_only_no_benchmark_result", "draft", "reviewed"}
AGENT_MODES = {"disabled", "idle", "local", "remote"}
CACHE_STATES = {"cold", "warm", "mixed"}


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


def reject_extra(
    path: Path, obj: dict[str, object], allowed: set[str], label: str
) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        fail(path, f"{label} has unsupported fields: {', '.join(extra)}")


def require_keys(
    path: Path, obj: dict[str, object], required: set[str], label: str
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        fail(path, f"{label} is missing required fields: {', '.join(missing)}")


def require_string(path: Path, obj: dict[str, object], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        fail(path, f"{label}.{key} must be a non-empty string")
    return value


def require_bool(path: Path, obj: dict[str, object], key: str, label: str) -> bool:
    value = obj.get(key)
    if not isinstance(value, bool):
        fail(path, f"{label}.{key} must be a boolean")
    return value


def require_int(path: Path, obj: dict[str, object], key: str, label: str) -> int:
    value = obj.get(key)
    if type(value) is not int or value < 0:
        fail(path, f"{label}.{key} must be a non-negative integer")
    return value


def require_string_array(
    path: Path, obj: dict[str, object], key: str, label: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(path, f"{label}.{key} must be an array of strings")
    return value


def load_corpus_cases() -> dict[str, str]:
    payload = require_object(CORPUS_MANIFEST, load_json(CORPUS_MANIFEST), "corpus")
    cases = payload.get("cases")
    if not isinstance(cases, list):
        fail(CORPUS_MANIFEST, "cases must be an array")
    result: dict[str, str] = {}
    for item in cases:
        case = require_object(CORPUS_MANIFEST, item, "case")
        case_id = require_string(CORPUS_MANIFEST, case, "case_id", "case")
        top_level_site = require_string(
            CORPUS_MANIFEST, case, "top_level_site", "case"
        )
        result[case_id] = top_level_site
    return result


def load_network_case_ids() -> set[str]:
    payload = require_object(NETWORK_PROFILE, load_json(NETWORK_PROFILE), "profile")
    routes = payload.get("routes")
    if not isinstance(routes, list):
        fail(NETWORK_PROFILE, "routes must be an array")
    case_ids: set[str] = set()
    for item in routes:
        route = require_object(NETWORK_PROFILE, item, "route")
        case_ids.add(require_string(NETWORK_PROFILE, route, "case_id", "route"))
    return case_ids


def load_reference_ids() -> tuple[str, str, str]:
    corpus = require_object(CORPUS_MANIFEST, load_json(CORPUS_MANIFEST), "corpus")
    network = require_object(NETWORK_PROFILE, load_json(NETWORK_PROFILE), "profile")
    resource = require_object(
        RESOURCE_ATTRIBUTION, load_json(RESOURCE_ATTRIBUTION), "resource_attribution"
    )
    return (
        require_string(CORPUS_MANIFEST, corpus, "corpus_id", "corpus"),
        require_string(NETWORK_PROFILE, network, "profile_id", "profile"),
        require_string(
            RESOURCE_ATTRIBUTION,
            resource,
            "resource_attribution_id",
            "resource_attribution",
        ),
    )


def validate_state_counts(
    path: Path, state_counts: dict[str, object], grouped_counts: dict[str, int], label: str
) -> None:
    reject_extra(path, state_counts, STATES, f"{label}.state_counts")
    require_keys(path, state_counts, STATES, f"{label}.state_counts")
    total = 0
    for state in STATES:
        count = require_int(path, state_counts, state, f"{label}.state_counts")
        total += count
        if count != grouped_counts.get(state, 0):
            fail(
                path,
                f"{label}.state_counts.{state}={count} does not match tab groups {grouped_counts.get(state, 0)}",
            )
    if total != 30:
        fail(path, f"{label}.state_counts must total 30, got {total}")


def validate_group(
    path: Path,
    group: object,
    seen_groups: set[str],
    corpus_cases: dict[str, str],
    network_cases: set[str],
    label: str,
) -> tuple[str, int]:
    item = require_object(path, group, label)
    required = {
        "group_id",
        "count",
        "corpus_case_id",
        "top_level_site",
        "initial_state",
        "protected",
        "revival_expected",
        "state_loss_allowed",
        "notes",
    }
    optional = {"protection_reason"}
    reject_extra(path, item, required | optional, label)
    require_keys(path, item, required, label)

    group_id = require_string(path, item, "group_id", label)
    if not GROUP_ID.fullmatch(group_id):
        fail(path, f"{label}.group_id has invalid format: {group_id}")
    if group_id in seen_groups:
        fail(path, f"duplicate group_id: {group_id}")
    seen_groups.add(group_id)

    count = require_int(path, item, "count", label)
    if count < 1:
        fail(path, f"{label}.count must be >= 1")
    case_id = require_string(path, item, "corpus_case_id", label)
    if not CASE_ID.fullmatch(case_id):
        fail(path, f"{label}.corpus_case_id has invalid format: {case_id}")
    if case_id not in corpus_cases:
        fail(path, f"{label}.corpus_case_id is not in corpus manifest: {case_id}")
    if case_id not in network_cases:
        fail(path, f"{label}.corpus_case_id is not routed by network profile: {case_id}")
    top_level_site = require_string(path, item, "top_level_site", label)
    if top_level_site != corpus_cases[case_id]:
        fail(path, f"{label}.top_level_site does not match corpus manifest for {case_id}")
    state = require_string(path, item, "initial_state", label)
    if state not in STATES:
        fail(path, f"{label}.initial_state is not allowed: {state}")
    protected = require_bool(path, item, "protected", label)
    if protected and not isinstance(item.get("protection_reason"), str):
        fail(path, f"{label}.protected groups must include protection_reason")
    if not protected and item.get("protection_reason") is not None:
        fail(path, f"{label}.unprotected groups must use null protection_reason")
    require_bool(path, item, "revival_expected", label)
    require_bool(path, item, "state_loss_allowed", label)
    require_string_array(path, item, "notes", label)
    return state, count


def validate_scenario(
    path: Path,
    scenario: object,
    seen_scenarios: set[str],
    corpus_cases: dict[str, str],
    network_cases: set[str],
) -> None:
    item = require_object(path, scenario, "scenario")
    required = {
        "scenario_id",
        "name",
        "scenario_kind",
        "tab_count",
        "cache_state",
        "agent_mode",
        "security_assumptions",
        "lifecycle",
        "tab_groups",
        "expected_m0_status",
        "measurement_claim_allowed",
    }
    reject_extra(path, item, required, "scenario")
    require_keys(path, item, required, "scenario")

    scenario_id = require_string(path, item, "scenario_id", "scenario")
    if not SCENARIO_ID.fullmatch(scenario_id):
        fail(path, f"scenario.scenario_id has invalid format: {scenario_id}")
    if scenario_id in seen_scenarios:
        fail(path, f"duplicate scenario_id: {scenario_id}")
    seen_scenarios.add(scenario_id)
    require_string(path, item, "name", "scenario")
    kind = require_string(path, item, "scenario_kind", "scenario")
    if kind not in SCENARIO_KINDS:
        fail(path, f"scenario.scenario_kind is not allowed: {kind}")
    if require_int(path, item, "tab_count", "scenario") != 30:
        fail(path, "scenario.tab_count must be 30")
    if require_string(path, item, "cache_state", "scenario") not in CACHE_STATES:
        fail(path, "scenario.cache_state is not allowed")
    if require_string(path, item, "agent_mode", "scenario") not in AGENT_MODES:
        fail(path, "scenario.agent_mode is not allowed")
    require_string_array(path, item, "security_assumptions", "scenario")
    require_string(path, item, "expected_m0_status", "scenario")
    if require_bool(path, item, "measurement_claim_allowed", "scenario"):
        fail(path, "scenario.measurement_claim_allowed must be false")

    lifecycle = require_object(path, item.get("lifecycle"), "scenario.lifecycle")
    lifecycle_required = {
        "all_live",
        "state_counts",
        "process_topology",
        "revival_check_required",
        "state_loss_policy",
    }
    reject_extra(path, lifecycle, lifecycle_required, "scenario.lifecycle")
    require_keys(path, lifecycle, lifecycle_required, "scenario.lifecycle")
    all_live = require_bool(path, lifecycle, "all_live", "scenario.lifecycle")
    require_string(path, lifecycle, "process_topology", "scenario.lifecycle")
    require_bool(path, lifecycle, "revival_check_required", "scenario.lifecycle")
    require_string(path, lifecycle, "state_loss_policy", "scenario.lifecycle")

    groups = item.get("tab_groups")
    if not isinstance(groups, list) or not groups:
        fail(path, "scenario.tab_groups must be a non-empty array")
    seen_groups: set[str] = set()
    grouped_counts = {state: 0 for state in STATES}
    total_groups = 0
    for index, group in enumerate(groups, start=1):
        state, count = validate_group(
            path,
            group,
            seen_groups,
            corpus_cases,
            network_cases,
            f"scenario.tab_groups[{index}]",
        )
        grouped_counts[state] += count
        total_groups += count
    if total_groups != 30:
        fail(path, f"scenario.tab_groups must total 30, got {total_groups}")

    state_counts = require_object(
        path, lifecycle.get("state_counts"), "scenario.lifecycle.state_counts"
    )
    validate_state_counts(path, state_counts, grouped_counts, "scenario.lifecycle")
    if kind == "thirty_tab_all_live":
        if not all_live:
            fail(path, "all-live scenario must set lifecycle.all_live true")
        for state in ("throttled", "frozen", "serialized", "discarded", "crashed"):
            if grouped_counts[state] != 0:
                fail(path, f"all-live scenario cannot include {state} tabs")
    if kind == "thirty_tab_mixed_state":
        if all_live:
            fail(path, "mixed-state scenario must set lifecycle.all_live false")
        if grouped_counts["serialized"] + grouped_counts["discarded"] == 0:
            fail(path, "mixed-state scenario must include serialized or discarded tabs")


def validate_manifest(path: Path, payload: object) -> None:
    corpus_id, network_id, resource_id = load_reference_ids()
    corpus_cases = load_corpus_cases()
    network_cases = load_network_case_ids()

    manifest = require_object(path, payload, "manifest")
    required = {
        "schema_version",
        "scenario_set_id",
        "status",
        "created_at",
        "claim_status",
        "corpus_id",
        "network_profile_id",
        "resource_attribution_id",
        "scenario_count",
        "scenarios",
        "unsupported_behavior",
    }
    reject_extra(path, manifest, required, "manifest")
    require_keys(path, manifest, required, "manifest")
    if manifest.get("schema_version") != 1:
        fail(path, "schema_version must be 1")
    scenario_set_id = require_string(path, manifest, "scenario_set_id", "manifest")
    if not SCENARIO_SET_ID.fullmatch(scenario_set_id):
        fail(path, f"scenario_set_id has invalid format: {scenario_set_id}")
    status = require_string(path, manifest, "status", "manifest")
    if status not in STATUS_VALUES:
        fail(path, f"status is not allowed: {status}")
    if status != "sample_only_no_benchmark_result":
        fail(path, "current checked scenario manifest must remain sample-only")
    require_string(path, manifest, "created_at", "manifest")
    claim_status = require_string(path, manifest, "claim_status", "manifest")
    for phrase in ["no benchmark result", "no Chrome-class claim", "no performance claim"]:
        if phrase not in claim_status:
            fail(path, f"claim_status must mention: {phrase}")
    if require_string(path, manifest, "corpus_id", "manifest") != corpus_id:
        fail(path, "manifest.corpus_id must match no-claim smoke corpus")
    if require_string(path, manifest, "network_profile_id", "manifest") != network_id:
        fail(path, "manifest.network_profile_id must match no-claim local static profile")
    if require_string(path, manifest, "resource_attribution_id", "manifest") != resource_id:
        fail(path, "manifest.resource_attribution_id must match semantic owner taxonomy")
    unsupported = require_string_array(
        path, manifest, "unsupported_behavior", "manifest"
    )
    for phrase in ["no browser was launched", "no benchmark result exists"]:
        if not any(phrase in item for item in unsupported):
            fail(path, f"unsupported_behavior must mention: {phrase}")

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) < 2:
        fail(path, "scenarios must contain mixed-state and all-live scenarios")
    scenario_count = require_int(path, manifest, "scenario_count", "manifest")
    if scenario_count != len(scenarios):
        fail(path, "scenario_count must equal number of scenarios")
    seen_scenarios: set[str] = set()
    kinds: set[str] = set()
    for scenario in scenarios:
        scenario_obj = require_object(path, scenario, "scenario")
        kinds.add(str(scenario_obj.get("scenario_kind")))
        validate_scenario(path, scenario, seen_scenarios, corpus_cases, network_cases)
    if not {"thirty_tab_mixed_state", "thirty_tab_all_live"}.issubset(kinds):
        fail(path, "scenario set must include mixed-state and all-live 30-tab scenarios")


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] if argv else [DEFAULT_MANIFEST]
    try:
        for path in paths:
            validate_manifest(path, load_json(path))
    except ValidationError as error:
        print(f"benchmark tab scenario validation failed: {error}", file=sys.stderr)
        return 1
    print(f"benchmark tab scenario validation passed: {len(paths)} manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
