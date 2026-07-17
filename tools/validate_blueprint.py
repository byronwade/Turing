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
                       '11-pre-build-readiness-checklist.md',
                       '12-agent-execution-and-production-readiness.md',
                      'README.md'],
 'market-strategy': ['01-market-method-and-segments.md',
                     '02-competitive-feature-matrix.md',
                     '03-user-demand-and-switching-barriers.md',
                     '04-project-native-workspaces.md',
                     '05-time-machine-and-continuity.md',
                     '06-resource-truth-and-lifecycle-control.md',
                     '07-trustworthy-ai-and-agent-differentiation.md',
                     '08-research-canvas-and-developer-mode.md',
                     '09-migration-portability-collaboration-and-sync.md',
                     '10-feature-prioritization-and-validation.md',
                     'README.md'],
 'ui-runtime': ['01-goals-trust-boundary-and-working-hypothesis.md',
                '02-framework-landscape-and-selection-method.md',
                '03-rust-state-command-and-adapter-architecture.md',
                '04-page-surface-compositor-and-process-integration.md',
                '05-slint-adapter-component-model-and-exit-strategy.md',
                '06-react-design-lab-tokens-and-authoring-workflow.md',
                '07-windowing-input-ime-accessibility-and-platform.md',
                '08-performance-memory-binary-and-energy-budgets.md',
                '09-testing-observability-recovery-and-release-gates.md',
                '10-prototype-plan-decision-record-and-migration.md',
                'README.md'],
 'agent-execution': ['01-agent-trust-model-and-authority.md',
                     '02-task-decomposition-and-execution-graph.md',
                     '03-branch-pr-review-and-merge-policy.md',
                     '04-tools-network-files-secrets-and-credentials.md',
                     '05-specification-test-and-evidence-workflow.md',
                     '06-model-prompt-environment-and-run-provenance.md',
                     '07-checkpoints-recovery-retries-and-rollback.md',
                     '08-independent-verification-and-adversarial-review.md',
                     '09-security-embargo-release-and-incident-boundaries.md',
                     '10-cost-resource-and-concurrency-budgets.md',
                     '11-human-handoff-and-escalation.md',
                     'README.md'],
 'production-readiness': ['01-stable-v1-scope-and-non-scope.md',
                          '02-supported-platform-and-hardware-matrix.md',
                          '03-release-channels-and-promotion-policy.md',
                          '04-product-slos-and-error-budgets.md',
                          '05-compatibility-and-conformance-gates.md',
                          '06-security-and-vulnerability-response-gates.md',
                          '07-accessibility-and-usability-conformance.md',
                          '08-data-loss-migration-and-recovery-gates.md',
                          '09-update-rollout-rollback-and-kill-switches.md',
                          '10-service-dependencies-and-offline-behavior.md',
                          '11-support-end-of-life-and-deprecation.md',
                          '12-production-readiness-review.md',
                          '13-secure-development-provenance-and-ai-assisted-coding.md',
                          '14-legal-signing-and-human-release-authority.md',
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
    RESEARCH / "browser-market-gap-2026-07.md",
    RESEARCH / "native-ui-framework-evaluation-2026-07.md",
    RESEARCH / "pre-build-readiness-gap-audit-2026-07.md",
    RESEARCH / "agent-execution-production-readiness-audit-2026-07.md",
    DOCS / "templates" / "agent-task.md",
    DOCS / "templates" / "agent-run-review.md",
    DOCS / "templates" / "production-readiness-review.md",
    DOCS / "templates" / "release-exception.md",
    DOCS / "templates" / "incident-exercise.md",
    DOCS / "templates" / "ui-framework-experiment.md",
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
    DOCS / "market-strategy" / "machine" / "feature-opportunities.json",
    DOCS / "ui-runtime" / "machine" / "framework-candidates.json",
    DOCS / "ui-runtime" / "machine" / "ui-performance-budgets.json",
    MACHINE / "pre-build-readiness.json",
    DOCS / "agent-execution" / "machine" / "agent-capability-matrix.json",
    DOCS / "agent-execution" / "machine" / "agent-run-manifest.schema.json",
    DOCS / "agent-execution" / "machine" / "execution-task.schema.json",
    DOCS / "agent-execution" / "machine" / "evidence-bundle.schema.json",
    DOCS / "agent-execution" / "machine" / "escalation-policy.json",
    DOCS / "agent-execution" / "machine" / "prohibited-agent-actions.json",
    DOCS / "production-readiness" / "machine" / "stable-scope.json",
    DOCS / "production-readiness" / "machine" / "supported-platforms.json",
    DOCS / "production-readiness" / "machine" / "release-channels.json",
    DOCS / "production-readiness" / "machine" / "product-slos.json",
    DOCS / "production-readiness" / "machine" / "release-gates.json",
    DOCS / "production-readiness" / "machine" / "service-dependencies.json",
    DOCS / "production-readiness" / "machine" / "vulnerability-slas.json",
    DOCS / "production-readiness" / "machine" / "update-trust-roles.json",
    DOCS / "production-readiness" / "machine" / "secure-development-controls.json",
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
    ROOT / "target",
    ROOT / "prototype" / "target",
    ROOT / "tools" / "__pycache__",
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
    r"\b(?:REQ-[A-Z0-9-]+|R-\d{3}|ADR-\d{4}|WP-\d{3}|RQ-\d{2}|OP-\d{3}|UIF-\d{3}|UIB-\d{3}|PB-\d{3}|AEX(?:-[A-Z]+)?-\d{3}|PRG-\d{3}|SLO-\d{3}|SRC-\d{3}|"
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
        if path.suffix == ".json" and (path.is_relative_to(MACHINE) or path.is_relative_to(DOCS / "market-strategy" / "machine") or path.is_relative_to(DOCS / "ui-runtime" / "machine") or path.is_relative_to(DOCS / "agent-execution" / "machine") or path.is_relative_to(DOCS / "production-readiness" / "machine")):
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


def check_professional_controls() -> None:
    owners = load_json(MACHINE / "professional-owners.json")
    rules = load_json(MACHINE / "professional-review-rules.json")
    if not isinstance(owners, dict) or not isinstance(owners.get("owners"), list):
        fail("professional-owners.json must contain an owners array")
    if not isinstance(rules, dict) or not isinstance(rules.get("rules"), list):
        fail("professional-review-rules.json must contain a rules array")

    owner_scopes = [item.get("scope") for item in owners["owners"]]
    if len(owner_scopes) != len(set(owner_scopes)):
        fail("professional owner scopes must be unique")
    required_owner_scopes = {"product", "market-strategy"}
    missing_owner_scopes = required_owner_scopes - set(owner_scopes)
    if missing_owner_scopes:
        fail(
            "missing professional owner scopes: "
            + ", ".join(sorted(missing_owner_scopes))
        )

    allowed_reviewers = set(owner_scopes) | {"owner"}
    rule_ids = [item.get("id") for item in rules["rules"]]
    if len(rule_ids) != len(set(rule_ids)):
        fail("professional review rule IDs must be unique")
    if "REV-MARKET" not in rule_ids:
        fail("professional review rules must include REV-MARKET")
    for rule in rules["rules"]:
        reviewers = rule.get("reviewers")
        if not isinstance(reviewers, list) or not reviewers:
            fail(f"{rule.get('id')}: reviewers must be a non-empty array")
        unknown = set(reviewers) - allowed_reviewers
        if unknown:
            fail(
                f"{rule.get('id')}: unknown reviewer scopes: "
                + ", ".join(sorted(unknown))
            )

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    if "\n\n| [Market Strategy and Differentiation]" in docs_index:
        fail("docs/README.md separates market strategy from the books table")
    market_research_row = (
        "| [Browser market gap and differentiation research — July 2026]"
    )
    if market_research_row not in docs_index:
        fail("docs/README.md active research table is missing the market-gap report")

    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    if "\n\n- [Market Strategy and Differentiation]" in blueprint_index:
        fail("Blueprint index separates market strategy from the engineering-book list")
    if "../research/browser-market-gap-2026-07.md" not in blueprint_index:
        fail("Blueprint current reports are missing the market-gap report")


def check_market_opportunities() -> None:
    path = DOCS / "market-strategy" / "machine" / "feature-opportunities.json"
    payload = load_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("opportunities"), list):
        fail("feature-opportunities.json must contain an opportunities array")
    opportunities = payload["opportunities"]
    ids = [item.get("id") for item in opportunities]
    expected = [f"OP-{index:03d}" for index in range(1, 15)]
    if ids != expected:
        fail(f"market opportunity IDs must be contiguous OP-001 through OP-014; found {ids}")
    required = {"id", "name", "priority", "status", "market_gap", "primary_segments", "dependencies", "risk", "evidence_required"}
    for item in opportunities:
        missing = required - set(item)
        if missing:
            fail(f"{item.get('id')}: missing opportunity fields: {', '.join(sorted(missing))}")
        if item.get("status") != "proposed":
            fail(f"{item.get('id')}: market opportunities remain proposed until reviewed promotion")
        for field in ("primary_segments", "dependencies", "risk", "evidence_required"):
            if not isinstance(item.get(field), list) or not item[field]:
                fail(f"{item.get('id')}: {field} must be a non-empty array")



def check_ui_runtime_controls() -> None:
    candidates = load_json(DOCS / "ui-runtime" / "machine" / "framework-candidates.json")
    budgets = load_json(DOCS / "ui-runtime" / "machine" / "ui-performance-budgets.json")
    readiness = load_json(MACHINE / "pre-build-readiness.json")

    candidate_items = candidates.get("candidates") if isinstance(candidates, dict) else None
    if not isinstance(candidate_items, list):
        fail("framework-candidates.json must contain a candidates array")
    candidate_ids = [item.get("id") for item in candidate_items]
    expected_candidates = [f"UIF-{index:03d}" for index in range(1, 10)]
    if candidate_ids != expected_candidates:
        fail(f"UI framework IDs must be UIF-001 through UIF-009; found {candidate_ids}")
    if candidates.get("selection_status") != "not_selected":
        fail("UI framework must remain not_selected until an accepted ADR changes it")

    budget_items = budgets.get("budgets") if isinstance(budgets, dict) else None
    if not isinstance(budget_items, list):
        fail("ui-performance-budgets.json must contain a budgets array")
    budget_ids = [item.get("id") for item in budget_items]
    expected_budgets = [f"UIB-{index:03d}" for index in range(1, 13)]
    if budget_ids != expected_budgets:
        fail(f"UI budget IDs must be UIB-001 through UIB-012; found {budget_ids}")

    required_candidate_fields = {"id", "name", "role", "runtime_model", "webview", "javascript_runtime", "maturity", "license", "blocking_evidence"}
    for item in candidate_items:
        missing = required_candidate_fields - set(item)
        if missing:
            fail(f"{item.get('id')}: missing UI candidate fields: {', '.join(sorted(missing))}")
        if not isinstance(item.get("blocking_evidence"), list) or not item["blocking_evidence"]:
            fail(f"{item.get('id')}: blocking_evidence must be a non-empty array")

    required_budget_fields = {"id", "name", "type"}
    for item in budget_items:
        missing = required_budget_fields - set(item)
        if missing:
            fail(f"{item.get('id')}: missing UI budget fields: {', '.join(sorted(missing))}")
        if item.get("type") not in {"hard", "measured"}:
            fail(f"{item.get('id')}: unknown UI budget type")

    readiness_items = readiness.get("items") if isinstance(readiness, dict) else None
    if not isinstance(readiness_items, list):
        fail("pre-build-readiness.json must contain an items array")
    readiness_ids = [item.get("id") for item in readiness_items]
    expected_readiness = [f"PB-{index:03d}" for index in range(1, 21)]
    if readiness_ids != expected_readiness:
        fail(f"pre-build readiness IDs must be PB-001 through PB-020; found {readiness_ids}")
    if readiness.get("status") != "not_ready_for_broad_implementation":
        fail("pre-build readiness remains not_ready_for_broad_implementation until reviewed promotion")
    if readiness.get("gate") != "PB-GATE-0":
        fail("pre-build readiness must identify PB-GATE-0")

    owners = load_json(MACHINE / "professional-owners.json")
    owner_scopes = {item.get("scope") for item in owners.get("owners", [])}
    allowed_status = {"ready", "partial", "proposed", "not_started", "not_selected", "documented_no_source", "documented_no_runner", "blocked"}
    for item in readiness_items:
        if item.get("status") not in allowed_status:
            fail(f"{item.get('id')}: unknown pre-build readiness status")
        if item.get("owner_scope") not in owner_scopes:
            fail(f"{item.get('id')}: unknown owner scope: {item.get('owner_scope')}")
        if item.get("status") == "ready":
            if not isinstance(item.get("evidence"), list) or not item["evidence"]:
                fail(f"{item.get('id')}: ready item requires evidence")
        elif not isinstance(item.get("evidence_required"), list) or not item["evidence_required"]:
            fail(f"{item.get('id')}: non-ready item requires evidence_required")

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_links = [
        "ui-runtime/README.md",
        "research/native-ui-framework-evaluation-2026-07.md",
        "research/pre-build-readiness-gap-audit-2026-07.md",
    ]
    for link in required_links:
        if link not in docs_index:
            fail(f"docs/README.md is missing native UI link: {link}")
    if "../ui-runtime/README.md" not in blueprint_index:
        fail("Blueprint index is missing the Native UI Runtime book")
    if "docs/ui-runtime/README.md" not in root_readme:
        fail("root README is missing the Native UI Runtime book")
    if "twenty-five detailed engineering and product books" not in root_readme:
        fail("root README detailed-book count is stale")
    templates_index = (DOCS / "templates" / "README.md").read_text(encoding="utf-8")
    if "ui-framework-experiment.md" not in templates_index:
        fail("templates index is missing the UI framework experiment")
    issue_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "engineering.yml").read_text(encoding="utf-8")
    for identifier in ("OP-...", "UIF-...", "UIB-...", "PB-..."):
        if identifier not in issue_template:
            fail(f"engineering issue template is missing identifier: {identifier}")
    project_index = (DOCS / "project-buildout" / "README.md").read_text(encoding="utf-8")
    if "11-pre-build-readiness-checklist.md" not in project_index:
        fail("project-buildout index is missing pre-build readiness checklist")


def check_agent_execution_controls() -> None:
    base = DOCS / "agent-execution" / "machine"
    matrix = load_json(base / "agent-capability-matrix.json")
    run_schema = load_json(base / "agent-run-manifest.schema.json")
    task_schema = load_json(base / "execution-task.schema.json")
    evidence_schema = load_json(base / "evidence-bundle.schema.json")
    escalation = load_json(base / "escalation-policy.json")
    prohibited = load_json(base / "prohibited-agent-actions.json")

    controls = matrix.get("controls") if isinstance(matrix, dict) else None
    if not isinstance(controls, list):
        fail("agent-capability-matrix.json must contain controls")
    ids = [item.get("id") for item in controls]
    expected = [f"AEX-{index:03d}" for index in range(1, 21)]
    if ids != expected:
        fail(f"agent capability controls must be AEX-001 through AEX-020; found {ids}")
    if matrix.get("status") != "deny_by_default":
        fail("agent capability matrix must remain deny_by_default")
    for schema, name in ((run_schema, "agent run"), (task_schema, "execution task"), (evidence_schema, "evidence bundle")):
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"{name} schema must be JSON Schema 2020-12")
    if not isinstance(escalation.get("triggers"), list) or not escalation["triggers"]:
        fail("escalation policy must contain triggers")
    if not isinstance(prohibited.get("actions"), list) or not prohibited["actions"]:
        fail("prohibited agent actions must contain actions")

    agents = (DOCS / "agent-execution" / "README.md").read_text(encoding="utf-8")
    root_agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "cannot approve or merge its own" not in agents:
        fail("agent execution book is missing no-self-approval rule")
    if "Production implementation-agent controls" not in root_agents:
        fail("AGENTS.md is missing production implementation-agent controls")


def check_production_readiness_controls() -> None:
    base = DOCS / "production-readiness" / "machine"
    stable = load_json(base / "stable-scope.json")
    platforms = load_json(base / "supported-platforms.json")
    channels = load_json(base / "release-channels.json")
    slos = load_json(base / "product-slos.json")
    gates = load_json(base / "release-gates.json")
    services = load_json(base / "service-dependencies.json")
    vuln = load_json(base / "vulnerability-slas.json")
    update = load_json(base / "update-trust-roles.json")
    secure = load_json(base / "secure-development-controls.json")

    if stable.get("decision_state") != "unapproved":
        fail("stable scope must remain unapproved until reviewed promotion")
    if platforms.get("status") != "none_selected":
        fail("supported platform matrix must remain none_selected")
    if channels.get("status") != "framework_only":
        fail("release channels must remain framework_only")
    slo_items = slos.get("slos") if isinstance(slos, dict) else None
    if not isinstance(slo_items, list):
        fail("product-slos.json must contain slos")
    slo_ids = [item.get("id") for item in slo_items]
    if slo_ids != [f"SLO-{index:03d}" for index in range(1, 17)]:
        fail(f"SLO IDs must be SLO-001 through SLO-016; found {slo_ids}")
    gate_items = gates.get("gates") if isinstance(gates, dict) else None
    if not isinstance(gate_items, list):
        fail("release-gates.json must contain gates")
    gate_ids = [item.get("id") for item in gate_items]
    if gate_ids != [f"PRG-{index:03d}" for index in range(1, 21)]:
        fail(f"production gate IDs must be PRG-001 through PRG-020; found {gate_ids}")
    if gates.get("status") != "not_ready_for_production" or any(item.get("state") != "not_ready" for item in gate_items):
        fail("production release gates must remain not_ready")
    if not isinstance(services.get("services"), list) or not services["services"]:
        fail("service-dependencies.json must contain services")
    if vuln.get("status") != "draft_no_commitment":
        fail("vulnerability SLAs must remain draft_no_commitment")
    role_ids = [item.get("id") for item in update.get("roles", [])]
    if role_ids != ["UPDATE-ROOT", "UPDATE-TARGETS", "UPDATE-SNAPSHOT", "UPDATE-TIMESTAMP"]:
        fail(f"update trust roles are incomplete: {role_ids}")
    secure_ids = [item.get("id") for item in secure.get("controls", [])]
    if secure_ids != [f"SRC-{index:03d}" for index in range(1, 16)]:
        fail(f"secure development controls must be SRC-001 through SRC-015; found {secure_ids}")

    production = (DOCS / "production-readiness" / "README.md").read_text(encoding="utf-8")
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "not_ready_for_production" not in production:
        fail("production readiness book is missing canonical not-ready state")
    if "not ready for production or stable release" not in root_readme:
        fail("root README is missing production readiness warning")

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

    if len(markdown_files) < 253:
        fail(f"expected at least 253 Markdown documents, found {len(markdown_files)}")
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


def check_research_question_ids() -> None:
    path = BLUEPRINT / "22-research-program.md"
    text = path.read_text(encoding="utf-8")
    ids = re.findall(r"^## RQ-(\d{2})\b", text, re.MULTILINE)
    if not ids:
        fail("research program contains no RQ headings")
    expected = [f"{index:02d}" for index in range(1, int(ids[-1]) + 1)]
    if ids != expected:
        fail(
            "research-question headings must be globally unique and contiguous; "
            f"expected RQ-01 through RQ-{expected[-1]}, found: "
            + ", ".join(f"RQ-{item}" for item in ids)
        )


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
        check_professional_controls()
        check_market_opportunities()
        check_ui_runtime_controls()
        check_agent_execution_controls()
        check_production_readiness_controls()
        markdown_count, links_checked = check_markdown()
        check_research_question_ids()
        check_policy_markers()
        check_source_hygiene()
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "validation passed: "
        f"{markdown_count} Markdown files, {links_checked} relative links, "
        "27 detailed engineering books, 46 requirements, 40 risks, "
        "18 work packages, 30 machine-readable registries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
