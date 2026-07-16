#!/usr/bin/env python3
"""Validate the Turing repository without third-party Python packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLUEPRINT = DOCS / "blueprint-v1"
MACHINE = BLUEPRINT / "machine"
RESEARCH = DOCS / "research"

CHAPTERS = [
    (1, "charter-and-principles"),
    (2, "capability-parity"),
    (3, "language-and-dependency-strategy"),
    (4, "system-architecture"),
    (5, "web-engine"),
    (6, "javascript-runtime"),
    (7, "network-storage-media"),
    (8, "security-and-sandbox"),
    (9, "performance-memory"),
    (10, "ai-agent-platform"),
    (11, "product-ui-devtools"),
    (12, "testing-compatibility"),
    (13, "build-release-operations"),
    (14, "roadmap-work-breakdown"),
    (15, "risk-register"),
    (16, "governance-contributing"),
    (17, "architecture-decisions"),
    (18, "source-bibliography"),
    (19, "initial-backlog"),
    (20, "definition-of-done"),
    (21, "product-requirements"),
    (22, "research-program"),
]

DETAILED_BOOKS = {'engine': ['01-pipeline-and-artifacts.md',
            '02-html-parser-and-dom.md',
            '03-css-cascade-and-invalidation.md',
            '04-layout-and-fragmentation.md',
            '05-paint-compositor-and-gpu.md',
            '06-text-fonts-and-i18n.md',
            '07-images-media-svg-and-canvas.md',
            '08-input-editing-accessibility.md',
            '09-memory-data-structures-and-observability.md',
            'README.md'],
 'javascript': ['01-front-end-bytecode-interpreter.md',
                '02-values-objects-shapes-and-inline-caches.md',
                '03-garbage-collection-and-host-lifetimes.md',
                '04-jit-tiering-ir-and-deoptimization.md',
                '05-webassembly-webidl-and-event-loop.md',
                '06-runtime-security-testing-and-performance.md',
                'README.md'],
 'security-engine': ['01-threat-model-and-process-isolation.md',
                     '02-sandbox-brokers-and-platform-containment.md',
                     '03-memory-safety-jit-and-exploit-hardening.md',
                     '04-web-security-privacy-and-trusted-ui.md',
                     '05-update-supply-chain-and-vulnerability-response.md',
                     '06-security-verification-and-release-gates.md',
                     '07-speculation-timers-and-side-channels.md',
                     '08-native-parser-and-codec-isolation.md',
                     '09-heap-sandboxes-pointer-tables-and-jit-compartments.md',
                     '10-capability-provenance-attenuation-and-revocation.md',
                     '11-developer-extension-automation-and-agent-attack-surfaces.md',
                     '12-anti-phishing-reputation-and-trusted-ui.md',
                     'README.md'],
 'developer-experience': ['01-protocol-architecture-and-versioning.md',
                          '02-devtools-workflows-and-ui.md',
                          '03-observability-tracing-and-replay.md',
                          '04-automation-headless-and-reproducibility.md',
                          '05-debugging-memory-performance-and-security.md',
                          '06-deterministic-replay-virtual-time-and-state-capture.md',
                          '07-source-maps-live-editing-and-local-development.md',
                          '08-diagnostic-bundles-and-automatic-reduction.md',
                          '09-generated-sdks-plugins-and-compatibility-adapters.md',
                          '10-integrated-accessibility-security-network-and-storage-debugging.md',
                          'README.md'],
 'api-design': ['01-design-principles.md',
                '02-async-streaming-and-cancellation.md',
                '03-schemas-errors-versioning-and-compatibility.md',
                '04-sdk-generation-authentication-and-redaction.md',
                'README.md'],
 'performance': ['01-performance-model-and-critical-path.md',
                 '02-memory-allocation-and-cache-policy.md',
                 '03-scheduler-parallelism-and-latency.md',
                 '04-graphics-energy-startup-and-recovery.md',
                 '05-benchmarks-statistics-and-regression-governance.md',
                 '06-data-locality-cpu-caches-and-numa.md',
                 '07-allocators-virtual-memory-and-page-reclamation.md',
                 '08-ipc-shared-memory-serialization-and-batching.md',
                 '09-pgo-lto-binary-layout-and-startup.md',
                 '10-causal-profiling-and-regression-diagnosis.md',
                 'README.md'],
 'ai': ['01-agent-architecture-and-trust-boundaries.md',
        '02-semantic-observations-and-redaction.md',
        '03-actions-grants-confirmation-and-audit.md',
        '04-memory-planning-multi-agent-and-lifecycle.md',
        '05-providers-local-models-mcp-and-tools.md',
        '06-evaluation-safety-performance-and-usability.md',
        'README.md'],
 'competitive': ['01-chromium-blink-v8.md',
                 '02-webkit-javascriptcore.md',
                 '03-gecko-spidermonkey.md',
                 '04-servo.md',
                 '05-ladybird.md',
                 '06-browser-products.md',
                 '07-comparison-scorecard-and-adoption-rules.md',
                 'README.md'],
 'networking': ['01-identities-and-request-context.md',
                '02-network-service-and-brokers.md',
                '03-dns-proxies-and-connection-racing.md',
                '04-tls-certificates-and-client-auth.md',
                '05-http1-http2-http3-and-quic.md',
                '06-fetch-redirects-cors-and-security-policy.md',
                '07-cache-preload-speculation-and-service-workers.md',
                '08-cookies-partitioning-and-tracking-resistance.md',
                '09-streaming-websocket-webtransport-and-downloads.md',
                '10-observability-testing-and-resource-budgets.md',
                'README.md'],
 'storage': ['01-storage-keys-buckets-and-partitioning.md',
             '02-quota-eviction-and-pressure.md',
             '03-indexeddb-transactions-and-durability.md',
             '04-cache-storage-service-workers-and-background-work.md',
             '05-cookies-sessions-and-private-data.md',
             '06-profile-history-bookmarks-settings-and-journals.md',
             '07-migrations-corruption-disk-full-and-power-loss.md',
             '08-encryption-credentials-clearing-and-export.md',
             '09-observability-repair-and-testing.md',
             'README.md'],
 'media-documents': ['01-decoder-processes-and-input-limits.md',
                     '02-images-fonts-color-and-animation.md',
                     '03-audio-video-clocks-buffering-and-seeking.md',
                     '04-webrtc-capture-and-devices.md',
                     '05-codecs-hardware-acceleration-and-licensing.md',
                     '06-drm-and-content-decryption-boundaries.md',
                     '07-pdf-viewer-and-document-security.md',
                     '08-printing-pagination-accessibility-and-quality.md',
                     'README.md'],
 'platform': ['01-browser-chrome-scene-graph-and-trusted-surfaces.md',
              '02-windows-surfaces-displays-and-lifecycle.md',
              '03-input-ime-clipboard-and-drag-drop.md',
              '04-macos-integration.md',
              '05-windows-integration.md',
              '06-linux-integration.md',
              '07-credentials-notifications-and-external-protocols.md',
              '08-packaging-startup-power-and-support-matrix.md',
              'README.md'],
 'accessibility': ['01-engine-semantics-and-tree-generation.md',
                   '02-names-relations-text-ranges-and-editing.md',
                   '03-cross-process-and-cross-origin-composition.md',
                   '04-platform-accessibility-bridges.md',
                   '05-browser-ui-devtools-automation-and-agents.md',
                   '06-latency-event-coalescing-and-resource-use.md',
                   '07-testing-assistive-technology-matrices-and-release-gates.md',
                   'README.md'],
 'release-operations': ['01-build-identity-and-hermetic-toolchains.md',
                        '02-reproducible-builds-provenance-and-sbom.md',
                        '03-signing-keys-and-package-attestation.md',
                        '04-platform-packaging-and-installers.md',
                        '05-update-metadata-rollout-and-rollback.md',
                        '06-profile-migrations-and-downgrade-protection.md',
                        '07-crash-reporting-symbols-and-redaction.md',
                        '08-vulnerability-response-and-supported-lifecycle.md',
                        'README.md'],
 'extensions-enterprise': ['01-extension-processes-worlds-and-isolation.md',
                           '02-permissions-host-grants-and-user-control.md',
                           '03-event-driven-background-work-and-quotas.md',
                           '04-declarative-network-rules-and-native-messaging.md',
                           '05-extension-updates-devtools-and-agents.md',
                           '06-enterprise-policy-precedence-and-audit.md',
                           '07-accounts-sync-encryption-conflicts-and-quotas.md',
                           'README.md'],
 'web-platform': ['01-user-needs-and-design-principles.md',
                  '02-feature-lifecycle-and-standards-participation.md',
                  '03-tests-interop-and-dependency-graphs.md',
                  '04-privacy-security-accessibility-and-abuse-review.md',
                  '05-experiments-deprecation-and-compatibility-interventions.md',
                  '06-governance-evidence-and-public-dashboard.md',
                  'README.md'],
 'benchmark-lab': ['01-hardware-os-power-and-thermal-control.md',
                   '02-corpus-servers-and-network-control.md',
                   '03-startup-navigation-and-input-latency.md',
                   '04-frame-pacing-raster-composite-and-gpu.md',
                   '05-memory-process-topology-and-thirty-tabs.md',
                   '06-energy-accessibility-developer-agent-and-recovery.md',
                   '07-statistics-artifacts-regressions-and-claims.md',
                   'README.md'],
 'quality-assurance': ['01-conformance-suites-and-reduced-tests.md',
                       '02-fuzzing-property-model-and-formal-methods.md',
                       '03-differential-testing-and-oracles.md',
                       '04-fault-injection-chaos-and-long-duration.md',
                       '05-security-assurance-and-independent-review.md',
                       '06-flakes-release-evidence-and-go-no-go.md',
                       'README.md'],
 'product-experience': ['01-tabs-groups-workspaces-and-command-field.md',
                        '02-onboarding-migration-profiles-and-private-sessions.md',
                        '03-permissions-credentials-agents-and-trusted-ux.md',
                        '04-resource-manager-lifecycle-and-recovery.md',
                        '05-settings-updates-support-usability-and-accessibility.md',
                        'README.md'],
 'technology-stack': ['README.md'],
 'plugins': ['README.md'],
 'embedding': ['README.md'],
 'project-buildout': ['01-program-lifecycle-and-phase-gates.md',
                      '02-ownership-codeowners-and-maintainer-ladder.md',
                      '03-rfc-adr-and-design-review-process.md',
                      '04-requirements-traceability-and-evidence.md',
                      '05-repository-build-toolchain-and-coding-standards.md',
                      '06-api-schema-configuration-and-version-governance.md',
                      '07-cross-cutting-security-performance-accessibility-privacy.md',
                      '08-release-incident-legal-data-and-support.md',
                      '09-servo-adoption-decision-framework.md',
                      '10-product-localization-documentation-and-sustainability.md',
                      'README.md']}

REQUIRED_DOCS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    DOCS / "README.md",
    DOCS / "start-here.md",
    DOCS / "documentation-policy.md",
    DOCS / "repository-map.md",
    DOCS / "contributing.md",
    DOCS / "security.md",
    DOCS / "prototype.md",
    DOCS / "research-log.md",
    RESEARCH / "README.md",
    RESEARCH / "browser-engine-landscape-2026-07.md",
    RESEARCH / "documentation-expansion-audit-2026-07.md",
    RESEARCH / "performance-security-developer-expansion-audit-2026-07.md",
    BLUEPRINT / "README.md",
    *[BLUEPRINT / f"{number:02d}-{slug}.md" for number, slug in CHAPTERS],
    *[
        DOCS / directory / filename
        for directory, filenames in DETAILED_BOOKS.items()
        for filename in filenames
    ],
    ROOT / "prototype" / "Cargo.toml",
    ROOT / "prototype" / "src" / "main.rs",
    ROOT / "tools" / "check_documentation_change.py",
    ROOT / ".github" / "workflows" / "repository-validation.yml",
]

REQUIRED_MACHINE_FILES = [
    MACHINE / "agent-action.schema.json",
    MACHINE / "backlog.json",
    MACHINE / "benchmark-manifest.schema.json",
    MACHINE / "process-capabilities.json",
    MACHINE / "requirements.json",
    MACHINE / "risks.json",
    MACHINE / "professional-owners.json",
    MACHINE / "professional-traceability.json",
    MACHINE / "professional-phase-gates.json",
    MACHINE / "professional-review-rules.json",
    MACHINE / "professional-exceptions.json",
]

ALLOWED_MARKDOWN_OUTSIDE_DOCS = {
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / ".github" / "pull_request_template.md",
}

FORBIDDEN_LEGACY_PATHS = [
    ROOT / "START_HERE.md",
    ROOT / "blueprint-v1",
    ROOT / "prototype" / "README.md",
    ROOT / "bootstrap",
    ROOT / ".github" / "workflows" / "blueprint-v1-validation.yml",
    ROOT / ".github" / "workflows" / "bootstrap.yml",
    ROOT / ".github" / "workflows" / "bootstrap-repair.yml",
    ROOT / ".github" / "workflows" / "expand-bootstrap.yml",
    ROOT / ".github" / "workflows" / "research-wave4-main-finalize.yml",
    ROOT / ".github" / "workflows" / "professional-buildout-expand.yml",
    ROOT / "tools" / "professional_buildout_generator.py",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
STABLE_ID = re.compile(
    r"\b(?:REQ-[A-Z0-9-]+|R-\d{3}|ADR-\d{4}|WP-\d{3}|RQ-\d{2}|"
    r"EXP-[A-Z0-9-]+|ENGINE-P-\d{3}|[A-Z]+-GATE-\d+)\b"
)


def fail(message: str) -> None:
    raise ValueError(message)


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{relative(path)}: invalid JSON: {error}")


def check_required_files() -> None:
    missing = [
        relative(path)
        for path in [*REQUIRED_DOCS, *REQUIRED_MACHINE_FILES]
        if not path.is_file()
    ]
    if missing:
        fail("missing required files: " + ", ".join(map(str, missing)))
    stale = [relative(path) for path in FORBIDDEN_LEGACY_PATHS if path.exists()]
    if stale:
        fail("forbidden legacy paths remain: " + ", ".join(map(str, stale)))


def check_document_locations() -> None:
    outside = [
        relative(path)
        for path in ROOT.rglob("*.md")
        if not path.is_relative_to(DOCS) and path not in ALLOWED_MARKDOWN_OUTSIDE_DOCS
    ]
    if outside:
        fail(
            "canonical Markdown must live under docs/; unexpected files: "
            + ", ".join(map(str, sorted(outside)))
        )
    for path in DOCS.rglob("*"):
        if not path.is_file() or path.suffix == ".md":
            continue
        if path.is_relative_to(MACHINE) and path.suffix == ".json":
            continue
        fail(f"unsupported documentation file type: {relative(path)}")


def check_book_topology() -> None:
    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    for directory, filenames in DETAILED_BOOKS.items():
        index_path = DOCS / directory / "README.md"
        if f"{directory}/README.md" not in docs_index:
            fail(f"docs/README.md does not link detailed book: {directory}")
        if f"../{directory}/README.md" not in blueprint_index:
            fail(f"docs/blueprint-v1/README.md does not link detailed book: {directory}")
        index_text = index_path.read_text(encoding="utf-8")
        for filename in filenames:
            if filename == "README.md":
                continue
            if f"({filename})" not in index_text:
                fail(f"{relative(index_path)} does not link child document: {filename}")


def check_json_registries() -> None:
    requirements = load_json(MACHINE / "requirements.json")
    risks = load_json(MACHINE / "risks.json")
    backlog = load_json(MACHINE / "backlog.json")
    for path in REQUIRED_MACHINE_FILES[:4]:
        load_json(path)
    if not isinstance(requirements, dict) or not isinstance(
        requirements.get("requirements"), list
    ):
        fail("requirements.json must contain a requirements array")
    if not isinstance(risks, dict) or not isinstance(risks.get("risks"), list):
        fail("risks.json must contain a risks array")
    if not isinstance(backlog, dict) or not isinstance(backlog.get("items"), list):
        fail("backlog.json must contain an items array")

    requirement_ids = [item.get("id") for item in requirements["requirements"]]
    risk_ids = [item.get("id") for item in risks["risks"]]
    work_ids = [item.get("id") for item in backlog["items"]]
    if len(requirement_ids) != 46:
        fail(f"expected 46 requirements, found {len(requirement_ids)}")
    if len(risk_ids) != 40:
        fail(f"expected 40 risks, found {len(risk_ids)}")
    if len(work_ids) != 18:
        fail(f"expected 18 work packages, found {len(work_ids)}")
    if len(requirement_ids) != len(set(requirement_ids)):
        fail("duplicate requirement IDs")
    if len(risk_ids) != len(set(risk_ids)):
        fail("duplicate risk IDs")
    if len(work_ids) != len(set(work_ids)):
        fail("duplicate work-package IDs")
    if requirement_ids != sorted(requirement_ids):
        fail("requirements must be sorted by stable ID")
    if risk_ids != [f"R-{index:03d}" for index in range(1, 41)]:
        fail("risk IDs must be contiguous R-001 through R-040")
    if work_ids != [f"WP-{index:03d}" for index in range(1, 19)]:
        fail("work-package IDs must be contiguous WP-001 through WP-018")

    requirement_set = set(requirement_ids)
    work_set = set(work_ids)
    for item in backlog["items"]:
        unknown_dependencies = set(item.get("depends_on", [])) - work_set
        if unknown_dependencies:
            fail(
                f"{item.get('id')}: unknown work-package dependencies: "
                + ", ".join(sorted(unknown_dependencies))
            )
        unknown_requirements = set(item.get("requirements", [])) - requirement_set
        if unknown_requirements:
            fail(
                f"{item.get('id')}: unknown requirements: "
                + ", ".join(sorted(unknown_requirements))
            )


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    if not target:
        return None
    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"{relative(source)} links outside repository: {target}")
    return resolved


def check_markdown() -> tuple[int, int]:
    markdown_files = sorted(ROOT.rglob("*.md"))
    links_checked = 0
    identifiers: set[str] = set()
    referenced_docs: set[Path] = set()

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        if "\r" in text:
            fail(f"{relative(path)} contains CR line endings")
        for line_number, line in enumerate(text.splitlines(), start=1):
            trailing = line[len(line.rstrip(" \t")) :]
            if trailing and trailing != "  ":
                fail(
                    f"{relative(path)}:{line_number} has accidental trailing whitespace"
                )
        identifiers.update(STABLE_ID.findall(text))
        for raw_target in MARKDOWN_LINK.findall(text):
            resolved = local_target(path, raw_target)
            if resolved is None:
                continue
            if not resolved.exists():
                fail(f"{relative(path)} has broken link: {raw_target}")
            if resolved.is_dir():
                fail(
                    f"{relative(path)} links to a directory instead of an indexed file: "
                    f"{raw_target}"
                )
            if resolved.suffix == ".md" and resolved.is_relative_to(DOCS):
                referenced_docs.add(resolved)
            links_checked += 1

    if len(markdown_files) < 204:
        fail(f"expected at least 204 Markdown documents, found {len(markdown_files)}")
    if len(identifiers) < 115:
        fail(f"expected at least 115 stable identifiers in prose, found {len(identifiers)}")
    canonical_docs = set(DOCS.rglob("*.md"))
    unindexed = sorted(canonical_docs - {DOCS / "README.md"} - referenced_docs)
    if unindexed:
        fail(
            "canonical documents without an inbound Markdown link: "
            + ", ".join(map(str, (relative(path) for path in unindexed)))
        )
    return len(markdown_files), links_checked


def check_policy_markers() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    required_phrases = [
        "Canonical project documentation lives in `docs/`",
        "Every change must update every affected document",
        "detailed engineering book",
        "docs/repository-map.md",
        "python3 tools/validate_blueprint.py",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in agents]
    if missing:
        fail("AGENTS.md is missing mandatory policy markers: " + ", ".join(missing))
    if "docs/contributing.md" not in (ROOT / "CONTRIBUTING.md").read_text(
        encoding="utf-8"
    ):
        fail("root CONTRIBUTING.md must point to docs/contributing.md")
    if "docs/security.md" not in (ROOT / "SECURITY.md").read_text(encoding="utf-8"):
        fail("root SECURITY.md must point to docs/security.md")


def check_source_hygiene() -> None:
    forbidden_suffixes = {".pem", ".key", ".p12", ".pfx"}
    forbidden_names = {".env", ".env.local", "id_rsa", "id_ed25519"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in forbidden_suffixes or path.name in forbidden_names:
            fail(f"forbidden secret-like file: {relative(path)}")


def main() -> int:
    try:
        check_required_files()
        check_document_locations()
        check_book_topology()
        check_json_registries()
        markdown_count, links_checked = check_markdown()
        check_policy_markers()
        check_source_hygiene()
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "validation passed: "
        f"{markdown_count} Markdown files, {links_checked} relative links, "
        "23 detailed engineering books, 46 requirements, 40 risks, "
        "18 work packages, 11 machine-readable registries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
