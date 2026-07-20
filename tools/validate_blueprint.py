#!/usr/bin/env python3
"""Validate the Turing repository without third-party Python packages."""

from __future__ import annotations

import json
import re
import subprocess
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
                       '13-build-readiness-operating-board.md',
                       '14-adr-0009-source-strategy-decision-packet.md',
                       '15-adr-0009-evidence-traceability-matrix.md',
                       '16-adr-0009-decision-draft.md',
                       '17-build-readiness-task-queue.md',
                       '18-documentation-readiness-evidence-matrix.md',
                       '19-github-issue-handoff.md',
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
    RESEARCH / "toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
    RESEARCH / "native-ui-framework-bakeoff-inventory-2026-07.md",
    RESEARCH / "native-ui-component-fixture-inventory-2026-07.md",
    RESEARCH / "window-input-accessibility-spike-inventory-2026-07.md",
    RESEARCH / "page-surface-composition-inventory-2026-07.md",
    RESEARCH / "fresh-host-reproduction-inventory-2026-07.md",
    RESEARCH / "pre-build-readiness-gap-audit-2026-07.md",
    RESEARCH / "implementation-kickoff-review-inventory-2026-07.md",
    RESEARCH / "build-readiness-dependency-graph-inventory-2026-07.md",
    RESEARCH / "documentation-readiness-completion-audit-2026-07.md",
    RESEARCH / "profile-session-format-inventory-2026-07.md",
    RESEARCH / "research-package-update-lab-inventory-2026-07.md",
    RESEARCH / "incident-patch-rehearsal-inventory-2026-07.md",
    RESEARCH / "backup-ownership-gap-inventory-2026-07.md",
    RESEARCH / "ipc-capability-boundary-inventory-2026-07.md",
    RESEARCH / "sandbox-probe-inventory-2026-07.md",
    RESEARCH / "wp-003-sandbox-probe-plan-2026-07.md",
    RESEARCH / "full-implementation-game-plan-audit-2026-07.md",
    RESEARCH / "agent-execution-production-readiness-audit-2026-07.md",
    RESEARCH / "benchmark-statistics-analysis-contract-2026-07.md",
    RESEARCH / "servo-unsafe-ffi-contract-review-2026-07.md",
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
    MACHINE / "benchmark-claim-bundle.schema.json",
    MACHINE
    / "benchmark-claim-bundles"
    / "no-claim-public-claim-template.json",
    MACHINE / "benchmark-readiness-review.schema.json",
    MACHINE
    / "benchmark-readiness-reviews"
    / "no-claim-benchmark-readiness-template.json",
    MACHINE / "benchmark-statistics-analysis.schema.json",
    MACHINE
    / "benchmark-statistics-analyses"
    / "no-claim-statistics-analysis-plan.json",
    MACHINE / "benchmark-manifest.schema.json",
    MACHINE / "process-capabilities.json",
    MACHINE / "requirements.json",
    MACHINE / "risks.json",
    MACHINE / "build-readiness-task-queue.json",
    MACHINE / "ipc-capability-boundary.schema.json",
    MACHINE / "ipc-capability-boundary.json",
    MACHINE / "ipc-schema-source.schema.json",
    MACHINE
    / "ipc-schema-sources"
    / "no-claim-control-envelope-template.json",
    MACHINE / "ipc-readiness-review.schema.json",
    MACHINE
    / "ipc-readiness-reviews"
    / "no-claim-ipc-readiness-template.json",
    MACHINE / "research-readiness-crosswalk.schema.json",
    MACHINE / "research-readiness-crosswalk.json",
    MACHINE / "adr-0009-evidence.schema.json",
    MACHINE / "adr-0009-evidence.json",
    MACHINE / "adr-0009-decision-review.schema.json",
    MACHINE
    / "adr-0009-decision-reviews"
    / "no-claim-decision-review-template.json",
    MACHINE / "servo-local-compatibility-corpus.schema.json",
    MACHINE / "servo-local-compatibility-https-harness.schema.json",
    MACHINE
    / "servo-local-compatibility-corpora"
    / "no-claim-tiny-adr0009.corpus.json",
    MACHINE
    / "servo-local-compatibility-harnesses"
    / "no-claim-https-host-alias.plan.json",
    MACHINE / "professional-owners.json",
    MACHINE / "professional-traceability.json",
    MACHINE / "requirement-verification-matrix.json",
    MACHINE / "professional-phase-gates.json",
    MACHINE / "professional-review-rules.json",
    MACHINE / "professional-exceptions.json",
    DOCS / "market-strategy" / "machine" / "feature-opportunities.json",
    DOCS / "ui-runtime" / "machine" / "framework-candidates.json",
    DOCS / "ui-runtime" / "machine" / "ui-performance-budgets.json",
    DOCS / "ui-runtime" / "machine" / "adapter-contract-inventory.schema.json",
    DOCS / "ui-runtime" / "machine" / "adapter-contract-inventory.json",
    DOCS / "ui-runtime" / "machine" / "framework-bakeoff-inventory.schema.json",
    DOCS / "ui-runtime" / "machine" / "framework-bakeoff-inventory.json",
    DOCS / "ui-runtime" / "machine" / "component-fixture-inventory.schema.json",
    DOCS / "ui-runtime" / "machine" / "component-fixture-inventory.json",
    DOCS / "ui-runtime" / "machine" / "page-surface-composition.schema.json",
    DOCS / "ui-runtime" / "machine" / "page-surface-composition.json",
    DOCS / "ui-runtime" / "machine" / "native-ui-readiness-review.schema.json",
    DOCS
    / "ui-runtime"
    / "machine"
    / "native-ui-readiness-reviews"
    / "no-claim-native-ui-readiness-template.json",
    DOCS / "accessibility" / "machine" / "window-input-accessibility-spike.schema.json",
    DOCS / "accessibility" / "machine" / "window-input-accessibility-spike.json",
    DOCS / "storage" / "machine" / "profile-session-format-inventory.schema.json",
    DOCS / "storage" / "machine" / "profile-session-format-inventory.json",
    DOCS / "storage" / "machine" / "profile-session-schema-package.schema.json",
    DOCS
    / "storage"
    / "machine"
    / "profile-session-schema-packages"
    / "no-claim-profile-session-schema-template.json",
    DOCS / "storage" / "machine" / "profile-session-readiness-review.schema.json",
    DOCS
    / "storage"
    / "machine"
    / "profile-session-readiness-reviews"
    / "no-claim-profile-session-readiness-template.json",
    DOCS / "release-operations" / "machine" / "research-package-update-lab.schema.json",
    DOCS / "release-operations" / "machine" / "research-package-update-lab.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-lab-package.schema.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-lab-packages"
    / "no-claim-update-lab-template.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-readiness-review.schema.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-readiness-reviews"
    / "no-claim-research-package-update-readiness-template.json",
    DOCS / "security-engine" / "machine" / "incident-patch-rehearsal.schema.json",
    DOCS / "security-engine" / "machine" / "incident-patch-rehearsal.json",
    DOCS / "security-engine" / "machine" / "incident-patch-rehearsal-record.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "incident-patch-rehearsal-records"
    / "no-claim-incident-patch-rehearsal-template.json",
    DOCS / "security-engine" / "machine" / "incident-patch-readiness-review.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "incident-patch-readiness-reviews"
    / "no-claim-incident-patch-readiness-template.json",
    DOCS / "security-engine" / "machine" / "sandbox-probe-inventory.schema.json",
    DOCS / "security-engine" / "machine" / "sandbox-probe-inventory.json",
    DOCS / "security-engine" / "machine" / "sandbox-probe-package.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "sandbox-probe-packages"
    / "no-claim-expected-deny-template.json",
    DOCS / "security-engine" / "machine" / "sandbox-readiness-review.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "sandbox-readiness-reviews"
    / "no-claim-sandbox-readiness-template.json",
    ROOT / "schemas" / "sandbox" / "probe-catalog.json",
    ROOT / "schemas" / "sandbox" / "probe-evidence.schema.json",
    DOCS / "project-buildout" / "machine" / "backup-ownership-gap.schema.json",
    DOCS / "project-buildout" / "machine" / "backup-ownership-gap.json",
    DOCS / "project-buildout" / "machine" / "backup-owner-qualification-record.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "backup-owner-qualification-records"
    / "no-claim-backup-owner-qualification-template.json",
    DOCS / "project-buildout" / "machine" / "backup-ownership-readiness-review.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "backup-ownership-readiness-reviews"
    / "no-claim-backup-ownership-readiness-template.json",
    DOCS / "project-buildout" / "machine" / "fresh-host-reproduction.schema.json",
    DOCS / "project-buildout" / "machine" / "fresh-host-reproduction.json",
    DOCS / "project-buildout" / "machine" / "fresh-host-run-record.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "fresh-host-runs"
    / "no-claim-run-record-template.json",
    DOCS / "project-buildout" / "machine" / "fresh-host-readiness-review.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "fresh-host-readiness-reviews"
    / "no-claim-fresh-host-readiness-template.json",
    DOCS / "project-buildout" / "machine" / "implementation-kickoff-review.schema.json",
    DOCS / "project-buildout" / "machine" / "implementation-kickoff-review.json",
    DOCS / "project-buildout" / "machine" / "build-readiness-dependency-graph.schema.json",
    DOCS / "project-buildout" / "machine" / "build-readiness-dependency-graph.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "documentation-readiness-completion-audit.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "documentation-readiness-completion-audit.json",
    DOCS / "project-buildout" / "machine" / "github-issue-handoff.schema.json",
    DOCS / "project-buildout" / "machine" / "github-issue-handoff.json",
    DOCS / "project-buildout" / "machine" / "build-readiness-closure-review.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "build-readiness-closure-reviews"
    / "no-claim-build-readiness-closure-template.json",
    MACHINE / "implementation-execution-graph.json",
    MACHINE / "implementation-milestone-gates.json",
    MACHINE / "implementation-interface-freezes.json",
    MACHINE / "implementation-evidence-catalog.json",
    MACHINE / "implementation-task-sequence.json",
    MACHINE / "pre-build-readiness.json",
    DOCS / "agent-execution" / "machine" / "agent-capability-matrix.json",
    DOCS / "agent-execution" / "machine" / "agent-run-manifest.schema.json",
    DOCS / "agent-execution" / "machine" / "execution-task.schema.json",
    DOCS / "agent-execution" / "machine" / "task-approval-template.schema.json",
    DOCS
    / "agent-execution"
    / "machine"
    / "task-approval-templates"
    / "no-claim-task-approval-template.json",
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

REQUIRED_ADR_0009_EVIDENCE_FILES = [
    ROOT / "tools" / "validate_adr_0009_evidence.py",
    MACHINE / "adr-0009-evidence.schema.json",
    MACHINE / "adr-0009-evidence.json",
    MACHINE / "adr-0009-decision-review.schema.json",
    MACHINE
    / "adr-0009-decision-reviews"
    / "no-claim-decision-review-template.json",
]

REQUIRED_SERVO_LOCAL_COMPATIBILITY_CORPUS_FILES = [
    ROOT / "tools" / "validate_servo_local_compatibility_corpus.py",
    ROOT / "tools" / "validate_servo_local_compatibility_https_harness.py",
    ROOT / "tools" / "serve_servo_local_compatibility_corpus.py",
    MACHINE / "servo-local-compatibility-corpus.schema.json",
    MACHINE / "servo-local-compatibility-https-harness.schema.json",
    MACHINE
    / "servo-local-compatibility-corpora"
    / "no-claim-tiny-adr0009.corpus.json",
    MACHINE
    / "servo-local-compatibility-harnesses"
    / "no-claim-https-host-alias.plan.json",
]

REQUIRED_BENCHMARK_MANIFEST_FILES = [
    ROOT / "tools" / "validate_benchmark_manifests.py",
    MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.sample.json",
    MACHINE / "benchmark-manifests" / "no-claim-runner-smoke.raw-artifacts.json",
]

REQUIRED_BENCHMARK_HARDWARE_FILES = [
    ROOT / "tools" / "validate_benchmark_hardware.py",
    MACHINE / "benchmark-hardware.schema.json",
    MACHINE / "benchmark-hardware" / "current-windows-high-end.candidate.json",
]

REQUIRED_BENCHMARK_OS_CONTROL_FILES = [
    ROOT / "tools" / "validate_benchmark_os_controls.py",
    MACHINE / "benchmark-os-control.schema.json",
    MACHINE / "benchmark-os-controls" / "current-windows-high-end.candidate.json",
]

REQUIRED_BENCHMARK_RESOURCE_ATTRIBUTION_FILES = [
    ROOT / "tools" / "validate_benchmark_resource_attribution.py",
    MACHINE / "benchmark-resource-attribution.schema.json",
    MACHINE / "benchmark-resource-attribution" / "semantic-owners.v1.json",
]

REQUIRED_BENCHMARK_COMPETITOR_VERSION_FILES = [
    ROOT / "tools" / "validate_benchmark_competitor_versions.py",
    MACHINE / "benchmark-competitor-version.schema.json",
    MACHINE / "benchmark-competitor-versions"
    / "current-desktop-release-candidates.2026-07.json",
]

REQUIRED_BENCHMARK_COMPETITOR_LOCAL_INSTALL_FILES = [
    ROOT / "tools" / "validate_benchmark_competitor_local_installs.py",
    MACHINE / "benchmark-competitor-local-install.schema.json",
    MACHINE / "benchmark-competitor-local-installs"
    / "current-windows-high-end.candidate.json",
]

REQUIRED_BENCHMARK_BROWSER_PIN_CAPTURE_FILES = [
    ROOT / "tools" / "capture_benchmark_browser_pins.py",
    ROOT / "tools" / "validate_benchmark_browser_pin_capture.py",
    MACHINE / "benchmark-browser-pin-capture.schema.json",
    MACHINE / "benchmark-browser-pin-captures"
    / "current-windows-high-end.no-claim.plan.json",
]

REQUIRED_BENCHMARK_BROWSER_PIN_DIAGNOSTIC_FILES = [
    ROOT / "tools" / "validate_benchmark_browser_pin_diagnostics.py",
    MACHINE / "benchmark-browser-pin-diagnostic.schema.json",
    MACHINE / "benchmark-browser-pin-diagnostics"
    / "current-windows-high-end.chrome-edge.no-claim.2026-07.json",
]

REQUIRED_BENCHMARK_CORPUS_FILES = [
    ROOT / "tools" / "validate_benchmark_corpus.py",
    MACHINE / "benchmark-corpus.schema.json",
    MACHINE / "benchmark-corpora" / "no-claim-smoke.corpus.json",
    ROOT / "docs" / "research" / "benchmark-corpus-expansion-2026-07.md",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "static-document" / "index.html",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "app-like" / "index.html",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "accessibility-form" / "index.html",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "international-text" / "index.html",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "hostile-markup" / "index.html",
    ROOT / "benchmarks" / "corpus" / "no-claim-smoke" / "media-document" / "index.html",
    ROOT
    / "benchmarks"
    / "corpus"
    / "no-claim-smoke"
    / "service-worker-contract"
    / "index.html",
]

REQUIRED_BENCHMARK_NETWORK_PROFILE_FILES = [
    ROOT / "tools" / "run_benchmark_server_profile.py",
    ROOT / "tools" / "run_benchmark_smoke.py",
    ROOT / "tools" / "serve_benchmark_profile.py",
    ROOT / "tools" / "validate_benchmark_network_profile.py",
    MACHINE / "benchmark-network-profile.schema.json",
    MACHINE / "benchmark-network-profiles" / "no-claim-local-static.profile.json",
]

REQUIRED_BENCHMARK_TAB_SCENARIO_FILES = [
    ROOT / "tools" / "validate_benchmark_tab_scenarios.py",
    MACHINE / "benchmark-tab-scenario.schema.json",
    MACHINE
    / "benchmark-tab-scenarios"
    / "no-claim-30-tab-smoke.scenarios.json",
]

REQUIRED_BENCHMARK_ARTIFACT_PACKAGE_FILES = [
    ROOT / "tools" / "validate_benchmark_artifact_packages.py",
    MACHINE / "benchmark-artifact-package.schema.json",
    MACHINE
    / "benchmark-artifact-packages"
    / "no-claim-trace-package.plan.json",
]

REQUIRED_BENCHMARK_LAUNCH_RUNNER_FILES = [
    ROOT / "tools" / "run_benchmark_browser_launch.py",
    ROOT / "tools" / "validate_benchmark_launch_runners.py",
    MACHINE / "benchmark-launch-runner.schema.json",
    MACHINE
    / "benchmark-launch-runners"
    / "no-claim-browser-launch.plan.json",
]

REQUIRED_BENCHMARK_CLAIM_BUNDLE_FILES = [
    ROOT / "tools" / "validate_benchmark_claim_bundles.py",
    MACHINE / "benchmark-claim-bundle.schema.json",
    MACHINE
    / "benchmark-claim-bundles"
    / "no-claim-public-claim-template.json",
]

REQUIRED_BENCHMARK_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_benchmark_readiness_review.py",
    MACHINE / "benchmark-readiness-review.schema.json",
    MACHINE
    / "benchmark-readiness-reviews"
    / "no-claim-benchmark-readiness-template.json",
]

REQUIRED_BENCHMARK_STATISTICS_ANALYSIS_FILES = [
    ROOT / "tools" / "validate_benchmark_statistics_analysis.py",
    MACHINE / "benchmark-statistics-analysis.schema.json",
    MACHINE
    / "benchmark-statistics-analyses"
    / "no-claim-statistics-analysis-plan.json",
    RESEARCH / "benchmark-statistics-analysis-contract-2026-07.md",
]

REQUIRED_UI_ADAPTER_CONTRACT_FILES = [
    ROOT / "tools" / "validate_ui_adapter_contract.py",
    RESEARCH / "toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
]

REQUIRED_UI_COMPONENT_FIXTURE_FILES = [
    ROOT / "tools" / "validate_ui_component_fixtures.py",
    RESEARCH / "native-ui-component-fixture-inventory-2026-07.md",
]

REQUIRED_FRAMEWORK_BAKEOFF_FILES = [
    ROOT / "tools" / "validate_framework_bakeoff.py",
    RESEARCH / "native-ui-framework-bakeoff-inventory-2026-07.md",
]

REQUIRED_FRESH_HOST_REPRODUCTION_FILES = [
    ROOT / "tools" / "validate_fresh_host_reproduction.py",
    RESEARCH / "fresh-host-reproduction-inventory-2026-07.md",
]

REQUIRED_FRESH_HOST_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_fresh_host_readiness_review.py",
    DOCS / "project-buildout" / "machine" / "fresh-host-readiness-review.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "fresh-host-readiness-reviews"
    / "no-claim-fresh-host-readiness-template.json",
]

REQUIRED_WINDOW_INPUT_ACCESSIBILITY_SPIKE_FILES = [
    ROOT / "tools" / "validate_window_input_accessibility_spike.py",
    RESEARCH / "window-input-accessibility-spike-inventory-2026-07.md",
]

REQUIRED_PAGE_SURFACE_COMPOSITION_FILES = [
    ROOT / "tools" / "validate_page_surface_composition.py",
    RESEARCH / "page-surface-composition-inventory-2026-07.md",
]

REQUIRED_NATIVE_UI_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_native_ui_readiness_review.py",
    DOCS / "ui-runtime" / "machine" / "native-ui-readiness-review.schema.json",
    DOCS
    / "ui-runtime"
    / "machine"
    / "native-ui-readiness-reviews"
    / "no-claim-native-ui-readiness-template.json",
]

REQUIRED_PROFILE_SESSION_FORMAT_FILES = [
    ROOT / "tools" / "validate_profile_session_formats.py",
    RESEARCH / "profile-session-format-inventory-2026-07.md",
    DOCS / "storage" / "machine" / "profile-session-schema-package.schema.json",
    DOCS
    / "storage"
    / "machine"
    / "profile-session-schema-packages"
    / "no-claim-profile-session-schema-template.json",
]

REQUIRED_PROFILE_SESSION_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_profile_session_readiness_review.py",
    DOCS / "storage" / "machine" / "profile-session-readiness-review.schema.json",
    DOCS
    / "storage"
    / "machine"
    / "profile-session-readiness-reviews"
    / "no-claim-profile-session-readiness-template.json",
]

REQUIRED_RESEARCH_PACKAGE_UPDATE_LAB_FILES = [
    ROOT / "tools" / "validate_research_package_update_lab.py",
    RESEARCH / "research-package-update-lab-inventory-2026-07.md",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-lab-package.schema.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-lab-packages"
    / "no-claim-update-lab-template.json",
]

REQUIRED_RESEARCH_PACKAGE_UPDATE_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_research_package_update_readiness_review.py",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-readiness-review.schema.json",
    DOCS
    / "release-operations"
    / "machine"
    / "research-package-update-readiness-reviews"
    / "no-claim-research-package-update-readiness-template.json",
]

REQUIRED_INCIDENT_PATCH_REHEARSAL_FILES = [
    ROOT / "tools" / "validate_incident_patch_rehearsal.py",
    RESEARCH / "incident-patch-rehearsal-inventory-2026-07.md",
    DOCS / "security-engine" / "machine" / "incident-patch-rehearsal-record.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "incident-patch-rehearsal-records"
    / "no-claim-incident-patch-rehearsal-template.json",
]

REQUIRED_INCIDENT_PATCH_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_incident_patch_readiness_review.py",
    DOCS / "security-engine" / "machine" / "incident-patch-readiness-review.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "incident-patch-readiness-reviews"
    / "no-claim-incident-patch-readiness-template.json",
]

REQUIRED_BACKUP_OWNERSHIP_GAP_FILES = [
    ROOT / "tools" / "validate_backup_ownership_gap.py",
    RESEARCH / "backup-ownership-gap-inventory-2026-07.md",
    DOCS / "project-buildout" / "machine" / "backup-owner-qualification-record.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "backup-owner-qualification-records"
    / "no-claim-backup-owner-qualification-template.json",
]

REQUIRED_BACKUP_OWNERSHIP_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_backup_ownership_readiness_review.py",
    DOCS / "project-buildout" / "machine" / "backup-ownership-readiness-review.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "backup-ownership-readiness-reviews"
    / "no-claim-backup-ownership-readiness-template.json",
]

REQUIRED_IMPLEMENTATION_KICKOFF_REVIEW_FILES = [
    ROOT / "tools" / "validate_implementation_kickoff_review.py",
    RESEARCH / "implementation-kickoff-review-inventory-2026-07.md",
]

REQUIRED_BUILD_READINESS_DEPENDENCY_GRAPH_FILES = [
    ROOT / "tools" / "validate_build_readiness_dependency_graph.py",
    RESEARCH / "build-readiness-dependency-graph-inventory-2026-07.md",
]

REQUIRED_DOCUMENTATION_READINESS_COMPLETION_AUDIT_FILES = [
    ROOT / "tools" / "validate_documentation_readiness_completion_audit.py",
    RESEARCH / "documentation-readiness-completion-audit-2026-07.md",
]

REQUIRED_BUILD_INFORMATION_READINESS_FILES = [
    ROOT / "tools" / "validate_build_information_readiness.py",
    RESEARCH / "build-information-readiness-ledger-2026-07.md",
    DOCS
    / "project-buildout"
    / "machine"
    / "build-information-readiness-ledger.schema.json",
    DOCS
    / "project-buildout"
    / "machine"
    / "build-information-readiness-ledger.json",
]

REQUIRED_IMPLEMENTATION_PLAN_FILES = [
    ROOT / "tools" / "validate_implementation_plan.py",
    RESEARCH / "full-implementation-game-plan-audit-2026-07.md",
    DOCS / "project-buildout" / "implementation-plan" / "README.md",
    MACHINE / "implementation-execution-graph.json",
    MACHINE / "implementation-milestone-gates.json",
    MACHINE / "implementation-interface-freezes.json",
    MACHINE / "implementation-evidence-catalog.json",
    MACHINE / "implementation-task-sequence.json",
]

REQUIRED_GITHUB_ISSUE_HANDOFF_FILES = [
    ROOT / "tools" / "validate_github_issue_handoff.py",
    DOCS / "project-buildout" / "19-github-issue-handoff.md",
    DOCS / "project-buildout" / "machine" / "github-issue-handoff.schema.json",
    DOCS / "project-buildout" / "machine" / "github-issue-handoff.json",
]

REQUIRED_IPC_CAPABILITY_BOUNDARY_FILES = [
    ROOT / "tools" / "validate_ipc_capability_boundaries.py",
    RESEARCH / "ipc-capability-boundary-inventory-2026-07.md",
    MACHINE / "ipc-schema-source.schema.json",
    MACHINE
    / "ipc-schema-sources"
    / "no-claim-control-envelope-template.json",
]

REQUIRED_IPC_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_ipc_readiness_review.py",
    MACHINE / "ipc-readiness-review.schema.json",
    MACHINE
    / "ipc-readiness-reviews"
    / "no-claim-ipc-readiness-template.json",
]

REQUIRED_SANDBOX_PROBE_INVENTORY_FILES = [
    ROOT / "tools" / "validate_sandbox_probe_inventory.py",
    RESEARCH / "sandbox-probe-inventory-2026-07.md",
    DOCS / "security-engine" / "machine" / "sandbox-probe-package.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "sandbox-probe-packages"
    / "no-claim-expected-deny-template.json",
]

REQUIRED_SANDBOX_CONTRACT_FILES = [
    ROOT / "tools" / "validate_sandbox_contracts.py",
    RESEARCH / "wp-003-sandbox-probe-plan-2026-07.md",
    ROOT / "schemas" / "sandbox" / "probe-catalog.json",
    ROOT / "schemas" / "sandbox" / "probe-evidence.schema.json",
]

REQUIRED_SANDBOX_READINESS_REVIEW_FILES = [
    ROOT / "tools" / "validate_sandbox_readiness_review.py",
    DOCS / "security-engine" / "machine" / "sandbox-readiness-review.schema.json",
    DOCS
    / "security-engine"
    / "machine"
    / "sandbox-readiness-reviews"
    / "no-claim-sandbox-readiness-template.json",
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
    r"TASK-\d{6}|EXP-[A-Z0-9-]+|ENGINE-P-\d{3}|[A-Z]+-GATE-\d+)\b"
)
TASK_ID = re.compile(r"^TASK-[0-9]{6}$")
PB_ID = re.compile(r"^PB-[0-9]{3}$")


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
        for path in [
            *REQUIRED_DOCS,
            *REQUIRED_MACHINE_FILES,
            *REQUIRED_ADR_0009_EVIDENCE_FILES,
            *REQUIRED_SERVO_LOCAL_COMPATIBILITY_CORPUS_FILES,
            *REQUIRED_BENCHMARK_MANIFEST_FILES,
            *REQUIRED_BENCHMARK_HARDWARE_FILES,
            *REQUIRED_BENCHMARK_OS_CONTROL_FILES,
            *REQUIRED_BENCHMARK_RESOURCE_ATTRIBUTION_FILES,
            *REQUIRED_BENCHMARK_COMPETITOR_VERSION_FILES,
            *REQUIRED_BENCHMARK_COMPETITOR_LOCAL_INSTALL_FILES,
            *REQUIRED_BENCHMARK_BROWSER_PIN_CAPTURE_FILES,
            *REQUIRED_BENCHMARK_BROWSER_PIN_DIAGNOSTIC_FILES,
            *REQUIRED_BENCHMARK_CORPUS_FILES,
            *REQUIRED_BENCHMARK_NETWORK_PROFILE_FILES,
            *REQUIRED_BENCHMARK_TAB_SCENARIO_FILES,
            *REQUIRED_BENCHMARK_ARTIFACT_PACKAGE_FILES,
            *REQUIRED_BENCHMARK_LAUNCH_RUNNER_FILES,
            *REQUIRED_BENCHMARK_CLAIM_BUNDLE_FILES,
            *REQUIRED_BENCHMARK_READINESS_REVIEW_FILES,
            *REQUIRED_BENCHMARK_STATISTICS_ANALYSIS_FILES,
            *REQUIRED_UI_ADAPTER_CONTRACT_FILES,
            *REQUIRED_UI_COMPONENT_FIXTURE_FILES,
            *REQUIRED_FRAMEWORK_BAKEOFF_FILES,
            *REQUIRED_FRESH_HOST_REPRODUCTION_FILES,
            *REQUIRED_FRESH_HOST_READINESS_REVIEW_FILES,
            *REQUIRED_WINDOW_INPUT_ACCESSIBILITY_SPIKE_FILES,
            *REQUIRED_PAGE_SURFACE_COMPOSITION_FILES,
            *REQUIRED_NATIVE_UI_READINESS_REVIEW_FILES,
            *REQUIRED_PROFILE_SESSION_FORMAT_FILES,
            *REQUIRED_PROFILE_SESSION_READINESS_REVIEW_FILES,
            *REQUIRED_RESEARCH_PACKAGE_UPDATE_LAB_FILES,
            *REQUIRED_RESEARCH_PACKAGE_UPDATE_READINESS_REVIEW_FILES,
            *REQUIRED_INCIDENT_PATCH_REHEARSAL_FILES,
            *REQUIRED_INCIDENT_PATCH_READINESS_REVIEW_FILES,
            *REQUIRED_BACKUP_OWNERSHIP_GAP_FILES,
            *REQUIRED_BACKUP_OWNERSHIP_READINESS_REVIEW_FILES,
            *REQUIRED_IMPLEMENTATION_KICKOFF_REVIEW_FILES,
            *REQUIRED_BUILD_READINESS_DEPENDENCY_GRAPH_FILES,
            *REQUIRED_DOCUMENTATION_READINESS_COMPLETION_AUDIT_FILES,
            *REQUIRED_BUILD_INFORMATION_READINESS_FILES,
            *REQUIRED_IMPLEMENTATION_PLAN_FILES,
            *REQUIRED_GITHUB_ISSUE_HANDOFF_FILES,
            *REQUIRED_IPC_CAPABILITY_BOUNDARY_FILES,
            *REQUIRED_IPC_READINESS_REVIEW_FILES,
            *REQUIRED_SANDBOX_PROBE_INVENTORY_FILES,
            *REQUIRED_SANDBOX_CONTRACT_FILES,
            *REQUIRED_SANDBOX_READINESS_REVIEW_FILES,
        ]
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
        if path.suffix == ".jsx" and path.is_relative_to(DOCS / "ui-runtime" / "design-lab"):
            continue
        if path.suffix == ".json" and (path.is_relative_to(MACHINE) or path.is_relative_to(DOCS / "market-strategy" / "machine") or path.is_relative_to(DOCS / "ui-runtime" / "machine") or path.is_relative_to(DOCS / "accessibility" / "machine") or path.is_relative_to(DOCS / "storage" / "machine") or path.is_relative_to(DOCS / "platform" / "machine") or path.is_relative_to(DOCS / "web-platform" / "machine") or path.is_relative_to(DOCS / "release-operations" / "machine") or path.is_relative_to(DOCS / "security-engine" / "machine") or path.is_relative_to(DOCS / "project-buildout" / "machine") or path.is_relative_to(DOCS / "agent-execution" / "machine") or path.is_relative_to(DOCS / "production-readiness" / "machine") or path.is_relative_to(DOCS / "research" / "machine")):
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
    if len(work_ids) != 20:
        fail(f"expected 20 work packages, found {len(work_ids)}")
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
    if work_ids != [f"WP-{index:03d}" for index in range(1, 21)]:
        fail("work-package IDs must be contiguous WP-001 through WP-020")

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


def check_build_readiness_task_queue() -> None:
    queue_path = MACHINE / "build-readiness-task-queue.json"
    queue = load_json(queue_path)
    requirements = load_json(MACHINE / "requirements.json")
    risks = load_json(MACHINE / "risks.json")
    owners = load_json(MACHINE / "professional-owners.json")
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    if not isinstance(queue, dict) or not isinstance(queue.get("tasks"), list):
        fail("build-readiness-task-queue.json must contain a tasks array")
    if queue.get("schema_version") != 1:
        fail("build-readiness-task-queue.json must use schema_version 1")
    if queue.get("status") != "proposed_queue_not_execution_authority":
        fail("build-readiness task queue must remain proposed and non-authoritative")
    if queue.get("source") != "docs/project-buildout/17-build-readiness-task-queue.md":
        fail("build-readiness task queue source must point to the human queue document")
    claim_status = queue.get("claim_status")
    if not isinstance(claim_status, str):
        fail("build-readiness task queue is missing claim_status")
    for phrase in [
        "no task is approved",
        "no task is approved, running, accepted",
        "Chrome-class",
        "production claims",
    ]:
        if phrase not in claim_status:
            fail(f"build-readiness task queue claim_status must mention: {phrase}")

    task_schema = DOCS / "agent-execution" / "machine" / "execution-task.schema.json"
    if queue.get("task_schema") != "docs/agent-execution/machine/execution-task.schema.json":
        fail("build-readiness task queue must reference the execution-task schema")
    load_json(task_schema)

    requirement_ids = {
        item.get("id")
        for item in requirements.get("requirements", [])
        if isinstance(item, dict)
    }
    risk_ids = {
        item.get("id") for item in risks.get("risks", []) if isinstance(item, dict)
    }
    owner_scopes = {
        item.get("scope") for item in owners.get("owners", []) if isinstance(item, dict)
    }
    readiness_ids = {
        item.get("id") for item in readiness.get("items", []) if isinstance(item, dict)
    }
    task_to_readiness: dict[str, set[str]] = {}
    for lane in crosswalk.get("lanes", []):
        if not isinstance(lane, dict):
            continue
        for task_id in lane.get("tasks", []):
            task_to_readiness.setdefault(task_id, set()).update(lane.get("readiness_items", []))
    routed_readiness = {
        readiness_id
        for lane in crosswalk.get("lanes", [])
        if isinstance(lane, dict)
        for readiness_id in lane.get("readiness_items", [])
    }
    missing_routes = sorted(
        item.get("id")
        for item in readiness.get("items", [])
        if isinstance(item, dict)
        and item.get("status") in {"partial", "blocked", "documented_no_runner", "documented_no_source", "not_started"}
        and item.get("id") not in routed_readiness
    )
    if missing_routes:
        fail(
            "non-ready PB items must have a research crosswalk route: "
            + ", ".join(missing_routes)
        )
    required_fields = {
        "schema_version",
        "id",
        "status",
        "owner",
        "independent_reviewer",
        "requirements",
        "risks",
        "allowed_paths",
        "prohibited_paths",
        "preconditions",
        "acceptance_criteria",
        "negative_tests",
        "resource_budget",
        "rollback",
        "dependencies",
    }
    budget_fields = {
        "wall_seconds",
        "cpu_seconds",
        "memory_bytes",
        "disk_bytes",
        "network_bytes",
        "max_workers",
        "max_retries",
    }
    tasks = queue["tasks"]
    ids = [task.get("id") for task in tasks if isinstance(task, dict)]
    expected_ids = [f"TASK-{index:06d}" for index in range(1, 11)]
    if ids != expected_ids:
        fail(f"build-readiness task IDs must be TASK-000001 through TASK-000010; found {ids}")
    seen: set[str] = set()
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            fail("build-readiness task entries must be objects")
        task_id = task.get("id")
        if not isinstance(task_id, str) or not TASK_ID.match(task_id):
            fail(f"invalid build-readiness task id: {task_id}")
        missing = required_fields - set(task)
        if missing:
            fail(f"{task_id}: missing task fields: {', '.join(sorted(missing))}")
        if task.get("schema_version") != 1:
            fail(f"{task_id}: schema_version must be 1")
        if task.get("status") != "proposed":
            fail(f"{task_id}: task queue entries must remain proposed until owner approval")
        readiness_items = task.get("readiness_items")
        if (
            not isinstance(readiness_items, list)
            or not readiness_items
            or not all(isinstance(value, str) and PB_ID.fullmatch(value) for value in readiness_items)
        ):
            fail(f"{task_id}: readiness_items must be a non-empty PB-* array")
        if set(readiness_items) != task_to_readiness.get(task_id, set()):
            fail(
                f"{task_id}: readiness_items must match the research-crosswalk task mapping; "
                f"found {readiness_items}"
            )
        for field in ("owner", "independent_reviewer"):
            value = task.get(field)
            if value not in owner_scopes:
                fail(f"{task_id}: unknown {field}: {value}")
        if task["owner"] == task["independent_reviewer"]:
            fail(f"{task_id}: owner and independent_reviewer must differ")
        unknown_requirements = set(task.get("requirements", [])) - requirement_ids
        if unknown_requirements:
            fail(f"{task_id}: unknown requirements: {', '.join(sorted(unknown_requirements))}")
        unknown_risks = set(task.get("risks", [])) - risk_ids
        if unknown_risks:
            fail(f"{task_id}: unknown risks: {', '.join(sorted(unknown_risks))}")
        for field in ("requirements", "risks", "allowed_paths", "preconditions", "acceptance_criteria"):
            values = task.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{task_id}: {field} must be a non-empty array")
            if not all(isinstance(value, str) and value for value in values):
                fail(f"{task_id}: {field} entries must be non-empty strings")
        for field in ("prohibited_paths", "negative_tests", "dependencies"):
            values = task.get(field)
            if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
                fail(f"{task_id}: {field} entries must be strings")
        for allowed_path in task["allowed_paths"]:
            if not (ROOT / allowed_path).exists():
                fail(f"{task_id}: allowed path does not exist: {allowed_path}")
        unknown_dependencies = set(task.get("dependencies", [])) - set(expected_ids)
        if unknown_dependencies:
            fail(f"{task_id}: unknown task dependencies: {', '.join(sorted(unknown_dependencies))}")
        forward_dependencies = [
            dependency
            for dependency in task.get("dependencies", [])
            if expected_ids.index(dependency) >= index
        ]
        if forward_dependencies:
            fail(f"{task_id}: dependencies must reference earlier queue entries")
        budget = task.get("resource_budget")
        if not isinstance(budget, dict) or set(budget) != budget_fields:
            fail(f"{task_id}: resource_budget must declare the standard budget fields")
        for field, value in budget.items():
            if not isinstance(value, int) or value < 0:
                fail(f"{task_id}: resource_budget.{field} must be a non-negative integer")
        if budget["wall_seconds"] <= 0 or budget["max_workers"] <= 0:
            fail(f"{task_id}: wall_seconds and max_workers must be positive")
        rollback = task.get("rollback")
        if not isinstance(rollback, dict) or set(rollback) != {"strategy", "evidence_required"}:
            fail(f"{task_id}: rollback must declare strategy and evidence_required")
        if not isinstance(rollback["strategy"], str) or not rollback["strategy"]:
            fail(f"{task_id}: rollback.strategy must be a non-empty string")
        if not isinstance(rollback["evidence_required"], list) or not rollback["evidence_required"]:
            fail(f"{task_id}: rollback.evidence_required must be a non-empty array")
        seen.add(task_id)
    if seen != set(expected_ids):
        fail("build-readiness task queue did not validate every expected task")

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    start_here = (DOCS / "start-here.md").read_text(encoding="utf-8")
    project_index = (DOCS / "project-buildout" / "README.md").read_text(encoding="utf-8")
    board = (DOCS / "project-buildout" / "13-build-readiness-operating-board.md").read_text(encoding="utf-8")
    repository_map = (DOCS / "repository-map.md").read_text(encoding="utf-8")
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for label, text in [
        ("docs/README.md", docs_index),
        ("docs/start-here.md", start_here),
        ("project-buildout index", project_index),
        ("build readiness board", board),
        ("repository map", repository_map),
        ("root README", root_readme),
    ]:
        if "17-build-readiness-task-queue.md" not in text:
            fail(f"{label} is missing the build-readiness task queue link")
    if "build-readiness-task-queue.json" not in docs_index or "build-readiness-task-queue.json" not in board:
        fail("task queue machine registry must be linked from docs index and operating board")

    project_required = [
        "source strategy, fresh-host reproducibility, IPC boundaries",
        "native-shell toolkit and page-surface selection",
        "package/update authority, incident-response decisions",
        "backup ownership, readiness promotion, and release authority as owner-only decisions",
    ]
    missing_project_required = [
        phrase for phrase in project_required if phrase not in project_index
    ]
    if missing_project_required:
        fail(
            "project-buildout index is missing current owner-only continuation controls: "
            + ", ".join(missing_project_required)
        )

    board_required = [
        "`TASK-000001` through `TASK-000010` provide task-shaped handoffs",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, and ownership work",
    ]
    missing_board_required = [phrase for phrase in board_required if phrase not in board]
    if missing_board_required:
        fail(
            "build readiness board is missing current lane/task continuation controls: "
            + ", ".join(missing_board_required)
        )

    ipc_task = next((task for task in tasks if task.get("id") == "TASK-000003"), None)
    if not isinstance(ipc_task, dict):
        fail("build-readiness task queue is missing TASK-000003")
    ipc_task_text = " ".join(
        value
        for field in ("acceptance_criteria", "negative_tests")
        for value in ipc_task.get(field, [])
        if isinstance(value, str)
    )
    for phrase in [
        "malformed",
        "oversized",
        "stale",
        "duplicate",
        "reordered",
        "unauthorized",
        "wrong-principal",
        "timeout",
        "cancellation",
    ]:
        if phrase not in ipc_task_text:
            fail(f"TASK-000003 must require IPC negative coverage for {phrase}")

    human_queue = (DOCS / "project-buildout" / "17-build-readiness-task-queue.md").read_text(
        encoding="utf-8"
    )
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        for phrase in ("wrong-principal", "timeout", "cancellation"):
            if phrase not in text:
                fail(f"{label} is missing IPC negative-test coverage for {phrase}")

    sandbox_task = next((task for task in tasks if task.get("id") == "TASK-000004"), None)
    if not isinstance(sandbox_task, dict):
        fail("build-readiness task queue is missing TASK-000004")
    sandbox_task_text = " ".join(
        value
        for field in ("acceptance_criteria", "negative_tests")
        for value in sandbox_task.get(field, [])
        if isinstance(value, str)
    ).lower().replace("shared memory", "shared-memory")
    sandbox_roles = [
        "renderer",
        "network",
        "storage",
        "gpu",
        "decoder",
        "extension",
        "devtools",
        "agent",
        "updater",
    ]
    sandbox_surfaces = [
        "file",
        "socket",
        "process",
        "registry",
        "device",
        "shared-memory",
        "credential",
        "debug",
        "profile",
        "ipc",
    ]
    for phrase in [*sandbox_roles, *sandbox_surfaces]:
        if phrase not in sandbox_task_text:
            fail(f"TASK-000004 must require sandbox probe coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = text.lower().replace("shared memory", "shared-memory")
        for phrase in [*sandbox_roles, *sandbox_surfaces]:
            if phrase not in normalized:
                fail(f"{label} is missing sandbox probe coverage for {phrase}")

    profile_task = next((task for task in tasks if task.get("id") == "TASK-000007"), None)
    if not isinstance(profile_task, dict):
        fail("build-readiness task queue is missing TASK-000007")

    def normalize_profile_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("private-session", "private session"),
            ("crash-recovery", "crash recovery"),
            ("protected-work", "protected work"),
            ("data-loss", "data loss"),
            ("real-profile", "real profile"),
            ("user-data", "user data"),
            ("credential-storage", "credential storage"),
            ("profile-format", "profile format"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    profile_task_text = normalize_profile_text(
        " ".join(
            value
            for field in ("preconditions", "acceptance_criteria", "negative_tests")
            for value in profile_task.get(field, [])
            if isinstance(value, str)
        )
    )
    profile_terms = [
        "profile",
        "space",
        "session",
        "snapshot",
        "migration",
        "disk full",
        "power loss",
        "corruption",
        "downgrade",
        "export",
        "deletion",
        "private session",
        "crash recovery",
        "protected work",
        "privacy",
        "data loss",
        "sync",
        "credential storage",
        "real profile",
        "user data",
        "production profile format",
    ]
    for phrase in profile_terms:
        if phrase not in profile_task_text:
            fail(f"TASK-000007 must require profile/session coverage for {phrase}")
    for phrase in ["checked no-claim schema-package template"]:
        if phrase not in profile_task_text:
            fail(f"TASK-000007 must require profile/session coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_profile_text(text)
        for phrase in profile_terms:
            if phrase not in normalized:
                fail(f"{label} is missing profile/session coverage for {phrase}")
        for phrase in ["checked no-claim schema-package template"]:
            if phrase not in normalized:
                fail(f"{label} is missing profile/session coverage for {phrase}")

    native_task = next((task for task in tasks if task.get("id") == "TASK-000006"), None)
    if not isinstance(native_task, dict):
        fail("build-readiness task queue is missing TASK-000006")

    def normalize_native_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("page surface", "page-surface"),
            ("gpu loss", "gpu-loss"),
            ("design token", "design-token"),
            ("component fixture", "component-fixture"),
            ("frame pacing", "frame-pacing"),
            ("trusted chrome", "trusted-chrome"),
            ("release path ui", "release-path ui"),
            ("page tree", "page-tree"),
            ("drag/drop", "drag-drop"),
            ("drag drop", "drag-drop"),
            ("screen reader", "screen-reader"),
            ("assistive technology", "assistive-technology"),
            ("high-contrast", "high contrast"),
            ("reduced-motion", "reduced motion"),
            ("renderer-hang", "renderer hang"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    native_evidence_terms = [
        "equivalent",
        "adapter",
        "page-surface",
        "design-token",
        "component",
        "accessibility",
        "ime",
        "keyboard",
        "page-tree",
        "clipboard",
        "drag-drop",
        "localization",
        "zoom",
        "high contrast",
        "reduced motion",
        "screen-reader",
        "manual assistive-technology",
        "crash",
        "renderer hang",
        "gpu-loss",
        "startup",
        "memory",
        "binary",
        "latency",
        "frame-pacing",
        "energy",
        "license",
        "dependency",
        "provenance",
    ]
    native_prohibited_terms = [
        "electron",
        "tauri",
        "system webview",
        "node",
        "react",
        "runtime dom",
        "css parser",
    ]
    native_task_text = normalize_native_text(
        " ".join(
            value
            for field in (
                "allowed_paths",
                "prohibited_paths",
                "preconditions",
                "acceptance_criteria",
                "negative_tests",
            )
            for value in native_task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in [*native_evidence_terms, *native_prohibited_terms]:
        if phrase not in native_task_text:
            fail(f"TASK-000006 must require native shell coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_native_text(text)
        for phrase in native_evidence_terms:
            if phrase not in normalized:
                fail(f"{label} is missing native shell evidence coverage for {phrase}")

    ownership_task = next((task for task in tasks if task.get("id") == "TASK-000008"), None)
    if not isinstance(ownership_task, dict):
        fail("build-readiness task queue is missing TASK-000008")

    def normalize_ownership_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("java script", "javascript"),
            ("ui runtime", "ui-runtime"),
            ("privacy data", "privacy-data"),
            ("release operations", "release-operations"),
            ("human release authority", "human-release-authority"),
            ("incident response", "incident-response"),
            ("legal community", "legal-community"),
            ("documentation research", "documentation-research"),
            ("agent operations", "agent-operations"),
            ("review rule", "review-rule"),
            ("escalation policy", "escalation-policy"),
            ("repository access", "repository-access"),
            ("no-stale-access", "stale privileged access"),
            ("stale access", "stale privileged access"),
            ("ownerless path", "ownerless protected path"),
            ("ownerless protected-path", "ownerless protected path"),
            ("primary-only path", "primary-only path"),
            ("primary only", "primary-only"),
            ("blocked-status", "blocked status"),
            ("single owner", "single-owner"),
            ("single-owner-risk", "single-owner residual-risk"),
            ("residual risk", "residual-risk"),
            ("two person", "two-person"),
            ("supported version", "supported-version"),
            ("security disclosure", "security-disclosure"),
            ("incident-closure", "incident closure"),
            ("incident closure", "incident closure"),
            ("legal-approval", "legal approval"),
            ("legal approval", "legal approval"),
            ("update trust", "update trust"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    ownership_terms = [
        "qualified backup",
        "program",
        "architecture",
        "security",
        "release-operations",
        "human-release-authority",
        "incident-response",
        "legal-community",
        "support",
        "quality",
        "supply-chain",
        "documentation-research",
        "product",
        "platform",
        "engine",
        "javascript",
        "networking",
        "storage",
        "performance",
        "accessibility",
        "ui-runtime",
        "agent-operations",
        "privacy-data",
        "role level",
        "subsystem competence",
        "representative path coverage",
        "recent review record",
        "availability",
        "succession",
        "recusal",
        "inactivity",
        "removal",
        "emergency replacement",
        "codeowners",
        "review-rule",
        "escalation-policy",
        "signing",
        "disclosure",
        "package",
        "ci",
        "service",
        "repository-access",
        "stale privileged access",
        "ownerless protected path",
        "primary-only",
        "blocked status",
        "single-owner",
        "residual-risk",
        "two-person control",
        "stable signing",
        "update trust",
        "supported-version",
        "irreversible",
        "migration",
        "release promotion",
        "legal approval",
        "incident closure",
    ]
    ownership_task_text = normalize_ownership_text(
        " ".join(
            value
            for field in (
                "preconditions",
                "acceptance_criteria",
                "negative_tests",
            )
            for value in ownership_task.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in ownership_terms:
        if phrase not in ownership_task_text:
            fail(f"TASK-000008 must require ownership coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_ownership_text(text)
        for phrase in ownership_terms:
            if phrase not in normalized:
                fail(f"{label} is missing ownership coverage for {phrase}")

    updater_task = next((task for task in tasks if task.get("id") == "TASK-000009"), None)
    if not isinstance(updater_task, dict):
        fail("build-readiness task queue is missing TASK-000009")

    def normalize_operational_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("build id", "build ID"),
            ("artifact hash", "artifact hashes"),
            ("artifact size", "artifact sizes"),
            ("no stable support", "no-stable-support"),
            ("stable support", "stable-support"),
            ("minimum-secure-version", "minimum secure version"),
            ("wrong-target", "wrong target"),
            ("wrong target", "wrong target"),
            ("partial-write", "partial write"),
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("revoked-version", "revoked version"),
            ("vulnerable-version", "vulnerable version"),
            ("crash loop", "crash-loop"),
            ("offline roots", "offline root"),
            ("stable-channel", "stable channel"),
            ("real-updater", "real updater"),
            ("user-profile", "user profile"),
            ("release-readiness", "release readiness"),
            ("private-intake", "private intake"),
            ("affected-version", "affected version"),
            ("embargoed ci", "embargoed CI"),
            ("cve", "CVE"),
            ("user/admin", "user and admin"),
            ("incident class", "incident-class"),
            ("stable-promotion", "stable promotion"),
            ("signing-authority", "signing authority"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    updater_task_text = normalize_operational_text(
        " ".join(
            value
            for field in (
                "prohibited_paths",
                "preconditions",
                "acceptance_criteria",
                "negative_tests",
            )
            for value in updater_task.get(field, [])
            if isinstance(value, str)
        )
    )
    updater_terms = [
        "signed research-package",
        "source commit",
        "build id",
        "channel",
        "platform",
        "architecture",
        "toolchain",
        "feature set",
        "sbom",
        "provenance",
        "symbols",
        "notices",
        "artifact hashes",
        "artifact sizes",
        "no-stable-support",
        "role separation",
        "signature threshold",
        "expiry",
        "minimum secure version",
        "rollout",
        "mirrors",
        "tamper",
        "replay",
        "wrong target",
        "partial write",
        "disk full",
        "power loss",
        "rollback",
        "vulnerable version",
        "migration",
        "downgrade",
        "crash-loop",
        "privacy-preserving",
        "production signing",
        "offline root",
        "stable channel",
        "public binary distribution",
        "real updater",
        "real user profile",
    ]
    for phrase in updater_terms:
        if phrase not in updater_task_text:
            fail(f"TASK-000009 must require updater lab coverage for {phrase}")
    for phrase in ["checked no-claim update-lab package template"]:
        if phrase not in updater_task_text:
            fail(f"TASK-000009 must require updater lab coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_operational_text(text)
        for phrase in updater_terms:
            if phrase not in normalized:
                fail(f"{label} is missing updater lab evidence coverage for {phrase}")
        for phrase in ["checked no-claim update-lab package template"]:
            if phrase not in normalized:
                fail(f"{label} is missing updater lab evidence coverage for {phrase}")

    incident_task = next((task for task in tasks if task.get("id") == "TASK-000010"), None)
    if not isinstance(incident_task, dict):
        fail("build-readiness task queue is missing TASK-000010")
    incident_task_text = normalize_operational_text(
        " ".join(
            value
            for field in (
                "prohibited_paths",
                "preconditions",
                "acceptance_criteria",
                "negative_tests",
            )
            for value in incident_task.get(field, [])
            if isinstance(value, str)
        )
    )
    incident_terms = [
        "private intake",
        "access control",
        "acknowledgement",
        "reproduction",
        "severity",
        "asset analysis",
        "affected version",
        "embargo",
        "sanitized evidence",
        "protected patch branch",
        "embargoed ci",
        "regression",
        "backport",
        "signing",
        "update dry run",
        "staged rollout",
        "minimum secure version",
        "revocation",
        "release notes",
        "user and admin communication",
        "cve",
        "credit",
        "coordinated disclosure",
        "postmortem",
        "incident-class",
        "active exploitation",
        "update or signing compromise",
        "dependency vulnerability",
        "data loss",
        "privacy leak",
        "sandbox regression",
        "malicious extension",
        "provider",
        "service outage",
        "role matrix",
        "timing targets",
        "escalation",
        "secret rotation",
        "agent",
        "stable promotion",
        "signing authority",
    ]
    for phrase in incident_terms:
        if phrase not in incident_task_text:
            fail(f"TASK-000010 must require incident rehearsal coverage for {phrase}")
    for phrase in ["checked no-claim incident patch rehearsal template"]:
        if phrase not in incident_task_text:
            fail(f"TASK-000010 must require incident rehearsal coverage for {phrase}")
    for label, text in [
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_operational_text(text)
        for phrase in incident_terms:
            if phrase not in normalized:
                fail(f"{label} is missing incident rehearsal evidence coverage for {phrase}")
        for phrase in ["checked no-claim incident patch rehearsal template"]:
            if phrase not in normalized:
                fail(f"{label} is missing incident rehearsal evidence coverage for {phrase}")


def check_research_readiness_crosswalk() -> None:
    crosswalk_path = MACHINE / "research-readiness-crosswalk.json"
    schema_path = MACHINE / "research-readiness-crosswalk.schema.json"
    crosswalk = load_json(crosswalk_path)
    schema = load_json(schema_path)
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    research_program = (BLUEPRINT / "22-research-program.md").read_text(encoding="utf-8")
    research_index = (RESEARCH / "README.md").read_text(encoding="utf-8")

    if not isinstance(schema, dict) or schema.get("title") != "Turing Research Readiness Crosswalk":
        fail("research-readiness-crosswalk.schema.json must define the research crosswalk schema")
    if not isinstance(crosswalk, dict) or not isinstance(crosswalk.get("lanes"), list):
        fail("research-readiness-crosswalk.json must contain a lanes array")
    if crosswalk.get("schema_version") != 1:
        fail("research-readiness-crosswalk.json must use schema_version 1")
    if crosswalk.get("status") != "no_claim_research_control":
        fail("research-readiness-crosswalk.json must remain a no-claim research control")
    if (
        crosswalk.get("source")
        != "docs/research/README.md#build-readiness-research-crosswalk"
    ):
        fail("research-readiness-crosswalk.json must point to the research crosswalk section")
    claim_status = crosswalk.get("claim_status")
    if not isinstance(claim_status, str):
        fail("research-readiness-crosswalk.json is missing claim_status")
    for phrase in [
        "no readiness gate",
        "no task",
        "Chrome-class",
        "production",
    ]:
        if phrase not in claim_status:
            fail(f"research-readiness-crosswalk claim_status must mention: {phrase}")

    readiness_ids = {
        item.get("id")
        for item in readiness.get("items", [])
        if isinstance(item, dict)
    }
    task_ids = {
        item.get("id")
        for item in task_queue.get("tasks", [])
        if isinstance(item, dict)
    }
    research_question_ids = set(
        re.findall(r"^## (RQ-[0-9]{2})\b", research_program, re.MULTILINE)
    )

    expected = {
        "research-lane-source-strategy-adr-0009": {
            "readiness_items": ["PB-002"],
            "tasks": ["TASK-000001"],
            "research_questions": [
                "RQ-44",
                "RQ-46",
                "RQ-47",
                "RQ-15",
                "RQ-16",
                "RQ-25",
                "RQ-31",
            ],
        },
        "research-lane-fresh-host-build-confidence": {
            "readiness_items": ["PB-008", "PB-009", "PB-020"],
            "tasks": ["TASK-000002"],
            "research_questions": ["RQ-46", "RQ-47", "RQ-31"],
        },
        "research-lane-kernel-process-authority-ipc": {
            "readiness_items": ["PB-011"],
            "tasks": ["TASK-000003"],
            "research_questions": ["RQ-02", "RQ-13", "RQ-20", "RQ-22", "RQ-36"],
        },
        "research-lane-sandbox-probes": {
            "readiness_items": ["PB-012"],
            "tasks": ["TASK-000004"],
            "research_questions": ["RQ-20", "RQ-38", "RQ-31"],
        },
        "research-lane-benchmark-extreme-performance-lab": {
            "readiness_items": ["PB-013"],
            "tasks": ["TASK-000005"],
            "research_questions": ["RQ-16", "RQ-23", "RQ-34", "RQ-35", "RQ-37"],
        },
        "research-lane-native-shell-page-surface": {
            "readiness_items": ["PB-003", "PB-004", "PB-005", "PB-014", "PB-015"],
            "tasks": ["TASK-000006"],
            "research_questions": [
                "RQ-04",
                "RQ-05",
                "RQ-29",
                "RQ-30",
                "RQ-40",
                "RQ-55",
                "RQ-56",
                "RQ-57",
            ],
        },
        "research-lane-profile-space-session-snapshot-migration": {
            "readiness_items": ["PB-016"],
            "tasks": ["TASK-000007"],
            "research_questions": ["RQ-14", "RQ-27", "RQ-49", "RQ-50", "RQ-53", "RQ-54"],
        },
        "research-lane-research-package-updater-lab": {
            "readiness_items": ["PB-017"],
            "tasks": ["TASK-000009"],
            "research_questions": ["RQ-31", "RQ-63", "RQ-64", "RQ-66"],
        },
        "research-lane-security-incident-patch-rehearsal": {
            "readiness_items": ["PB-018"],
            "tasks": ["TASK-000010"],
            "research_questions": ["RQ-31", "RQ-60", "RQ-66"],
        },
        "research-lane-ownership-review-capacity": {
            "readiness_items": ["PB-019", "PB-020"],
            "tasks": ["TASK-000008"],
            "research_questions": [
                "RQ-25",
                "RQ-31",
                "RQ-45",
                "RQ-47",
                "RQ-48",
                "RQ-60",
                "RQ-66",
            ],
        },
    }

    required_fields = {
        "id",
        "title",
        "readiness_items",
        "tasks",
        "requirements",
        "risks",
        "research_questions",
        "evidence_start",
        "next_proof",
        "claim_boundary",
    }
    lanes = crosswalk["lanes"]
    lane_ids = [lane.get("id") for lane in lanes if isinstance(lane, dict)]
    if lane_ids != list(expected):
        fail(
            "research-readiness crosswalk lanes must stay in the approved order; found: "
            + ", ".join(str(item) for item in lane_ids)
        )
    for lane in lanes:
        if not isinstance(lane, dict):
            fail("research-readiness crosswalk lanes must be objects")
        lane_id = lane.get("id")
        missing_fields = required_fields - set(lane)
        if missing_fields:
            fail(f"{lane_id}: missing crosswalk fields: {', '.join(sorted(missing_fields))}")
        if set(lane) != required_fields:
            extra_fields = set(lane) - required_fields
            fail(f"{lane_id}: unexpected crosswalk fields: {', '.join(sorted(extra_fields))}")
        for field in ("title",):
            if not isinstance(lane.get(field), str) or not lane[field]:
                fail(f"{lane_id}: {field} must be a non-empty string")
        for field in (
            "readiness_items",
            "tasks",
            "requirements",
            "risks",
            "research_questions",
            "evidence_start",
            "next_proof",
            "claim_boundary",
        ):
            values = lane.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{lane_id}: {field} must be a non-empty array")
            if not all(isinstance(value, str) and value for value in values):
                fail(f"{lane_id}: {field} entries must be non-empty strings")
        for field in ("readiness_items", "tasks", "research_questions"):
            if lane[field] != expected[lane_id][field]:
                fail(
                    f"{lane_id}: {field} must match the approved crosswalk mapping; "
                    f"found {lane[field]}"
                )
        task_by_id = {
            item.get("id"): item
            for item in task_queue.get("tasks", [])
            if isinstance(item, dict)
        }
        expected_requirements = {
            requirement
            for task_id in lane["tasks"]
            for requirement in task_by_id.get(task_id, {}).get("requirements", [])
        }
        expected_risks = {
            risk
            for task_id in lane["tasks"]
            for risk in task_by_id.get(task_id, {}).get("risks", [])
        }
        if set(lane["requirements"]) != expected_requirements:
            fail(f"{lane_id}: requirements must mirror its task queue bindings")
        if set(lane["risks"]) != expected_risks:
            fail(f"{lane_id}: risks must mirror its task queue bindings")
        unknown_readiness = set(lane["readiness_items"]) - readiness_ids
        if unknown_readiness:
            fail(
                f"{lane_id}: unknown PB references: "
                + ", ".join(sorted(unknown_readiness))
            )
        unknown_tasks = set(lane["tasks"]) - task_ids
        if unknown_tasks:
            fail(f"{lane_id}: unknown TASK references: " + ", ".join(sorted(unknown_tasks)))
        unknown_research = set(lane["research_questions"]) - research_question_ids
        if unknown_research:
            fail(
                f"{lane_id}: unknown RQ references: "
                + ", ".join(sorted(unknown_research))
            )
        for path_text in lane["evidence_start"]:
            if not (ROOT / path_text).exists():
                fail(f"{lane_id}: evidence_start path does not exist: {path_text}")
        for reference in [
            *lane["readiness_items"],
            *lane["tasks"],
            *lane["research_questions"],
        ]:
            if reference not in research_index:
                fail(f"{lane_id}: research index prose is missing reference {reference}")

    sandbox_lane = next(
        (lane for lane in lanes if lane.get("id") == "research-lane-sandbox-probes"),
        None,
    )
    if not isinstance(sandbox_lane, dict):
        fail("research-readiness crosswalk is missing the sandbox probe lane")
    sandbox_text = " ".join(sandbox_lane.get("next_proof", [])).lower().replace(
        "shared memory", "shared-memory"
    )
    sandbox_roles = [
        "renderer",
        "network",
        "storage",
        "gpu",
        "decoder",
        "extension",
        "devtools",
        "agent",
        "updater",
    ]
    sandbox_surfaces = [
        "file",
        "socket",
        "process",
        "registry",
        "device",
        "shared-memory",
        "credential",
        "debug",
        "profile",
        "ipc",
    ]
    research_index_normalized = research_index.lower().replace(
        "shared memory", "shared-memory"
    )
    for phrase in [*sandbox_roles, *sandbox_surfaces]:
        if phrase not in sandbox_text:
            fail(f"sandbox research crosswalk must require proof for {phrase}")
        if phrase not in research_index_normalized:
            fail(f"research index sandbox lane must require proof for {phrase}")

    profile_lane = next(
        (
            lane
            for lane in lanes
            if lane.get("id") == "research-lane-profile-space-session-snapshot-migration"
        ),
        None,
    )
    if not isinstance(profile_lane, dict):
        fail("research-readiness crosswalk is missing the profile/session lane")

    def normalize_profile_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("private-session", "private session"),
            ("crash-recovery", "crash recovery"),
            ("protected-work", "protected work"),
            ("data-loss", "data loss"),
            ("real-profile", "real profile"),
            ("user-data", "user data"),
            ("credential-storage", "credential storage"),
            ("profile-format", "profile format"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    profile_terms = [
        "profile",
        "space",
        "session",
        "snapshot",
        "migration",
        "disk full",
        "power loss",
        "corruption",
        "downgrade",
        "export",
        "deletion",
        "private session",
        "crash recovery",
        "protected work",
        "privacy",
        "data loss",
        "sync",
        "credential storage",
        "real profile",
        "user data",
        "production profile format",
    ]
    profile_text = normalize_profile_text(" ".join(profile_lane.get("next_proof", [])))
    research_index_profile_text = normalize_profile_text(research_index)
    for phrase in profile_terms:
        if phrase not in profile_text:
            fail(f"profile/session research crosswalk must require proof for {phrase}")
        if phrase not in research_index_profile_text:
            fail(f"research index profile/session lane must require proof for {phrase}")
    for phrase in ["checked no-claim schema-package template"]:
        if phrase not in profile_text:
            fail(f"profile/session research crosswalk must require proof for {phrase}")
        if phrase not in research_index_profile_text:
            fail(f"research index profile/session lane must require proof for {phrase}")

    native_lane = next(
        (lane for lane in lanes if lane.get("id") == "research-lane-native-shell-page-surface"),
        None,
    )
    if not isinstance(native_lane, dict):
        fail("research-readiness crosswalk is missing the native shell lane")

    def normalize_native_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("page surface", "page-surface"),
            ("gpu loss", "gpu-loss"),
            ("design token", "design-token"),
            ("component fixture", "component-fixture"),
            ("frame pacing", "frame-pacing"),
            ("trusted chrome", "trusted-chrome"),
            ("release path ui", "release-path ui"),
            ("page tree", "page-tree"),
            ("drag/drop", "drag-drop"),
            ("drag drop", "drag-drop"),
            ("screen reader", "screen-reader"),
            ("assistive technology", "assistive-technology"),
            ("high-contrast", "high contrast"),
            ("reduced-motion", "reduced motion"),
            ("renderer-hang", "renderer hang"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    native_terms = [
        "equivalent",
        "adapter",
        "page-surface",
        "design-token",
        "component",
        "accessibility",
        "ime",
        "keyboard",
        "page-tree",
        "clipboard",
        "drag-drop",
        "localization",
        "zoom",
        "high contrast",
        "reduced motion",
        "screen-reader",
        "manual assistive-technology",
        "crash",
        "renderer hang",
        "gpu-loss",
        "startup",
        "memory",
        "binary",
        "latency",
        "frame-pacing",
        "energy",
        "license",
        "dependency",
        "provenance",
    ]
    native_text = normalize_native_text(" ".join(native_lane.get("next_proof", [])))
    research_index_native_text = normalize_native_text(research_index)
    for phrase in native_terms:
        if phrase not in native_text:
            fail(f"native shell research crosswalk must require proof for {phrase}")
        if phrase not in research_index_native_text:
            fail(f"research index native shell lane must require proof for {phrase}")

    def normalize_operational_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("build id", "build id"),
            ("artifact hash", "artifact hashes"),
            ("artifact size", "artifact sizes"),
            ("no stable support", "no-stable-support"),
            ("minimum-secure-version", "minimum secure version"),
            ("wrong-target", "wrong target"),
            ("partial-write", "partial write"),
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("vulnerable-version", "vulnerable version"),
            ("crash loop", "crash-loop"),
            ("stable-channel", "stable channel"),
            ("public-distribution", "public distribution"),
            ("release-readiness", "release readiness"),
            ("supported-security", "supported security"),
            ("rollback-safety", "rollback safety"),
            ("migration-safety", "migration safety"),
            ("private-intake", "private intake"),
            ("affected-version", "affected version"),
            ("embargoed ci", "embargoed ci"),
            ("user/admin", "user and admin"),
            ("cve", "cve"),
            ("stable-promotion", "stable promotion"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    updater_lane = next(
        (lane for lane in lanes if lane.get("id") == "research-lane-research-package-updater-lab"),
        None,
    )
    if not isinstance(updater_lane, dict):
        fail("research-readiness crosswalk is missing the updater lab lane")
    updater_terms = [
        "signed research-package",
        "source commit",
        "build id",
        "channel",
        "platform",
        "architecture",
        "toolchain",
        "feature set",
        "sbom",
        "provenance",
        "symbols",
        "notices",
        "artifact hashes",
        "artifact sizes",
        "no-stable-support",
        "role separation",
        "signature threshold",
        "expiry",
        "minimum secure version",
        "rollout",
        "mirrors",
        "tamper",
        "replay",
        "wrong target",
        "partial write",
        "disk full",
        "power loss",
        "rollback",
        "vulnerable version",
        "migration",
        "downgrade",
        "crash-loop",
        "privacy-preserving",
        "production updater",
        "stable channel",
        "public distribution",
        "production signing",
        "offline root",
        "real updater",
        "real user profile",
        "release readiness",
        "supported security",
    ]
    updater_text = normalize_operational_text(
        " ".join(
            [
                *updater_lane.get("next_proof", []),
                *updater_lane.get("claim_boundary", []),
            ]
        )
    )
    research_index_operational_text = normalize_operational_text(research_index)
    for phrase in updater_terms:
        if phrase not in updater_text:
            fail(f"updater research crosswalk must require proof or boundary for {phrase}")
        if phrase not in research_index_operational_text:
            fail(f"research index updater lane must require proof or boundary for {phrase}")
    for phrase in ["checked no-claim update-lab package template"]:
        if phrase not in updater_text:
            fail(f"updater research crosswalk must require proof or boundary for {phrase}")
        if phrase not in research_index_operational_text:
            fail(f"research index updater lane must require proof or boundary for {phrase}")

    incident_lane = next(
        (
            lane
            for lane in lanes
            if lane.get("id") == "research-lane-security-incident-patch-rehearsal"
        ),
        None,
    )
    if not isinstance(incident_lane, dict):
        fail("research-readiness crosswalk is missing the incident rehearsal lane")
    incident_terms = [
        "private intake",
        "access control",
        "acknowledgement",
        "reproduction",
        "severity",
        "asset analysis",
        "affected version",
        "embargo",
        "sanitized evidence",
        "protected patch branch",
        "embargoed ci",
        "regression",
        "backport",
        "signing",
        "update dry run",
        "staged rollout",
        "minimum secure version",
        "revocation",
        "release notes",
        "user and admin communication",
        "cve",
        "credit",
        "coordinated disclosure",
        "postmortem",
        "incident-class",
        "active exploitation",
        "update or signing compromise",
        "dependency vulnerability",
        "data loss",
        "privacy leak",
        "sandbox regression",
        "malicious extension",
        "provider",
        "service outage",
        "role matrix",
        "timing targets",
        "escalation",
        "secret rotation",
        "agent",
        "stable promotion",
        "signing authority",
    ]
    incident_text = normalize_operational_text(
        " ".join(
            [
                *incident_lane.get("next_proof", []),
                *incident_lane.get("claim_boundary", []),
            ]
        )
    )
    for phrase in incident_terms:
        if phrase not in incident_text:
            fail(f"incident research crosswalk must require proof or boundary for {phrase}")
        if phrase not in research_index_operational_text:
            fail(f"research index incident lane must require proof or boundary for {phrase}")

    ownership_lane = next(
        (lane for lane in lanes if lane.get("id") == "research-lane-ownership-review-capacity"),
        None,
    )
    if not isinstance(ownership_lane, dict):
        fail("research-readiness crosswalk is missing the ownership lane")

    def normalize_ownership_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("ui runtime", "ui-runtime"),
            ("privacy data", "privacy-data"),
            ("release operations", "release-operations"),
            ("human release authority", "human-release-authority"),
            ("incident response", "incident-response"),
            ("legal community", "legal-community"),
            ("documentation research", "documentation-research"),
            ("agent operations", "agent-operations"),
            ("review rule", "review-rule"),
            ("escalation policy", "escalation-policy"),
            ("repository access", "repository-access"),
            ("no stale access", "stale privileged access"),
            ("stale access", "stale privileged access"),
            ("ownerless-path", "ownerless protected path"),
            ("ownerless protected-path", "ownerless protected path"),
            ("primary-only path", "primary-only path"),
            ("primary only", "primary-only"),
            ("blocked-status", "blocked status"),
            ("single-owner-risk", "single-owner residual-risk"),
            ("residual risk", "residual-risk"),
            ("two-person-control", "two-person control"),
            ("two person", "two-person"),
            ("supported-version", "supported-version"),
            ("update-trust", "update trust"),
            ("irreversible-migration", "irreversible migration"),
            ("incident-closure", "incident closure"),
            ("legal-approval", "legal approval"),
            ("security-disclosure", "security-disclosure"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    ownership_terms = [
        "qualified backup",
        "program",
        "architecture",
        "security",
        "release-operations",
        "human-release-authority",
        "incident-response",
        "legal-community",
        "support",
        "quality",
        "supply-chain",
        "documentation-research",
        "product",
        "platform",
        "engine",
        "javascript",
        "networking",
        "storage",
        "performance",
        "accessibility",
        "ui-runtime",
        "agent-operations",
        "privacy-data",
        "role level",
        "subsystem competence",
        "representative path coverage",
        "recent review record",
        "availability",
        "succession",
        "recusal",
        "inactivity",
        "removal",
        "emergency replacement",
        "codeowners",
        "review-rule",
        "escalation-policy",
        "signing",
        "disclosure",
        "package",
        "ci",
        "service",
        "repository-access",
        "stale privileged access",
        "ownerless protected path",
        "primary-only",
        "blocked status",
        "single-owner",
        "residual-risk",
        "two-person control",
        "production authority",
        "release authority",
        "signing authority",
        "update trust",
        "supported-version",
        "irreversible migration",
        "incident closure",
        "legal approval",
        "security-disclosure",
        "placeholder ownership",
    ]
    ownership_text = normalize_ownership_text(
        " ".join(
            [
                *ownership_lane.get("next_proof", []),
                *ownership_lane.get("claim_boundary", []),
            ]
        )
    )
    research_index_ownership_text = normalize_ownership_text(research_index)
    for phrase in ownership_terms:
        if phrase not in ownership_text:
            fail(f"ownership research crosswalk must require proof or boundary for {phrase}")
        if phrase not in research_index_ownership_text:
            fail(f"research index ownership lane must require proof or boundary for {phrase}")

    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    repository_map = (DOCS / "repository-map.md").read_text(encoding="utf-8")
    policy = (DOCS / "documentation-policy.md").read_text(encoding="utf-8")
    for label, text in [
        ("docs/README.md", docs_index),
        ("Blueprint index", blueprint_index),
        ("repository map", repository_map),
        ("documentation policy", policy),
        ("research index", research_index),
    ]:
        if "research-readiness-crosswalk.json" not in text:
            fail(f"{label} is missing the research-readiness crosswalk registry link")
    if "research-readiness-crosswalk.schema.json" not in research_index:
        fail("research index must link the research-readiness crosswalk schema")


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



def check_ui_adapter_contract() -> None:
    validator = ROOT / "tools" / "validate_ui_adapter_contract.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        fail(detail or "UI adapter contract validation failed")


def check_ui_component_fixtures() -> None:
    validator = ROOT / "tools" / "validate_ui_component_fixtures.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "UI component fixture validation failed")


def check_framework_bakeoff() -> None:
    validator = ROOT / "tools" / "validate_framework_bakeoff.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "framework bake-off validation failed")


def check_fresh_host_reproduction() -> None:
    validator = ROOT / "tools" / "validate_fresh_host_reproduction.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "fresh-host reproduction validation failed")
    run_record_validator = ROOT / "tools" / "validate_fresh_host_run_records.py"
    run_record_result = subprocess.run(
        [sys.executable, "-B", str(run_record_validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if run_record_result.returncode != 0:
        detail = "\n".join(
            line
            for line in [run_record_result.stdout.strip(), run_record_result.stderr.strip()]
            if line
        )
        fail(detail or "fresh-host run-record validation failed")


def check_fresh_host_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_fresh_host_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "fresh-host readiness-review validation failed")


def check_window_input_accessibility_spike() -> None:
    validator = ROOT / "tools" / "validate_window_input_accessibility_spike.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "window/input/accessibility spike validation failed")


def check_page_surface_composition() -> None:
    validator = ROOT / "tools" / "validate_page_surface_composition.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "page-surface composition validation failed")


def check_native_ui_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_native_ui_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "native UI readiness-review validation failed")


def check_profile_session_formats() -> None:
    validator = ROOT / "tools" / "validate_profile_session_formats.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "profile/session format validation failed")


def check_profile_session_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_profile_session_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "profile/session readiness-review validation failed")


def check_research_package_update_lab() -> None:
    validator = ROOT / "tools" / "validate_research_package_update_lab.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "research package/update lab validation failed")


def check_research_package_update_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_research_package_update_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "research package/update readiness-review validation failed")


def check_incident_patch_rehearsal() -> None:
    validator = ROOT / "tools" / "validate_incident_patch_rehearsal.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "incident patch rehearsal validation failed")


def check_incident_patch_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_incident_patch_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "incident/patch readiness-review validation failed")


def check_backup_ownership_gap() -> None:
    validator = ROOT / "tools" / "validate_backup_ownership_gap.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "backup ownership gap validation failed")


def check_backup_ownership_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_backup_ownership_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "backup ownership readiness-review validation failed")


def check_implementation_kickoff_review() -> None:
    validator = ROOT / "tools" / "validate_implementation_kickoff_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "implementation kickoff review validation failed")


def check_build_readiness_dependency_graph() -> None:
    validator = ROOT / "tools" / "validate_build_readiness_dependency_graph.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "build readiness dependency graph validation failed")


def check_documentation_readiness_completion_audit() -> None:
    validator = ROOT / "tools" / "validate_documentation_readiness_completion_audit.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "documentation readiness completion audit validation failed")


def check_ipc_capability_boundaries() -> None:
    validator = ROOT / "tools" / "validate_ipc_capability_boundaries.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "IPC capability boundary validation failed")


def check_ipc_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_ipc_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "IPC readiness-review validation failed")


def check_sandbox_probe_inventory() -> None:
    validator = ROOT / "tools" / "validate_sandbox_probe_inventory.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "sandbox probe inventory validation failed")


def check_implementation_plan() -> None:
    validator = ROOT / "tools" / "validate_implementation_plan.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "implementation plan validation failed")


def check_github_issue_handoff() -> None:
    validator = ROOT / "tools" / "validate_github_issue_handoff.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "GitHub issue handoff validation failed")


def check_sandbox_contracts() -> None:
    validator = ROOT / "tools" / "validate_sandbox_contracts.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "sandbox contract validation failed")


def check_sandbox_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_sandbox_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "sandbox readiness-review validation failed")


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
    expected_allowed_now = [
        "documentation",
        "research",
        "contained M0 source tasks in the root Cargo workspace",
        "typed kernel, identity, IPC, and toolkit-neutral UI-model foundations",
        "native UI comparison prototypes isolated from production crates",
        "expected-deny sandbox probes",
        "benchmark corpus and no-claim measurement tooling",
        "profile, Space, session, snapshot, and migration schema prototypes",
        "signed research-package and updater-laboratory prototypes with no production keys or real updater",
        "private-intake tabletop and emergency patch rehearsal documentation",
        "task-scoped diagnostic tooling",
    ]
    if readiness.get("allowed_now") != expected_allowed_now:
        fail("pre-build readiness allowed_now must stay scoped to contained/no-claim M0 work")

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
        elif item.get("status") == "not_selected":
            for field in ("not_selected_reason", "revisit_trigger"):
                value = item.get(field)
                if not isinstance(value, str) or len(value) < 30:
                    fail(f"{item.get('id')}: not_selected item requires {field}")
        elif not isinstance(item.get("evidence_required"), list) or not item["evidence_required"]:
            fail(f"{item.get('id')}: non-ready item requires evidence_required")

    gap_audit_path = RESEARCH / "pre-build-readiness-gap-audit-2026-07.md"
    gap_audit = gap_audit_path.read_text(encoding="utf-8")
    status_labels = {
        "ready": "Ready",
        "partial": "Partial",
        "blocked": "Blocked",
        "not_selected": "Not selected",
        "not_started": "Not started",
        "documented_no_source": "Documented no source",
        "documented_no_runner": "Documented no runner",
        "proposed": "Proposed",
    }
    for item in readiness_items:
        item_id = item.get("id")
        expected_label = status_labels[item.get("status")]
        match = re.search(
            rf"^\|\s*`{re.escape(str(item_id))}`[^|]*\|\s*([^|]+?)\s*\|",
            gap_audit,
            re.MULTILINE,
        )
        if not match:
            fail(f"{gap_audit_path}: missing status row for {item_id}")
        if match.group(1).strip().lower() != expected_label.lower():
            fail(
                f"{gap_audit_path}: {item_id} status drifted; "
                f"expected {expected_label}, found {match.group(1).strip()}"
            )

    if readiness_by_id := {item.get("id"): item for item in readiness_items}:
        if readiness_by_id.get("PB-008", {}).get("status") == "partial" and readiness_by_id.get("PB-009", {}).get("status") == "partial":
            continuation_match = re.search(
                r"^2\. Continue `PB-008` and `PB-009`",
                gap_audit,
                re.MULTILINE,
            )
            if not continuation_match:
                fail(
                    f"{gap_audit_path}: first continuation path must route the partial PB-008/PB-009 toolchain and fresh-host lane together"
                )

    pb003 = next((item for item in readiness_items if item.get("id") == "PB-003"), None)
    if not isinstance(pb003, dict):
        fail("pre-build readiness is missing PB-003")
    if pb003.get("status") != "partial":
        fail("PB-003 must remain partial while only no-claim adapter contract evidence exists")
    pb003_evidence = pb003.get("evidence")
    required_pb003_evidence = [
        "docs/research/toolkit-neutral-ui-adapter-contract-inventory-2026-07.md",
        "docs/ui-runtime/machine/adapter-contract-inventory.schema.json",
        "docs/ui-runtime/machine/adapter-contract-inventory.json",
        "tools/validate_ui_adapter_contract.py",
    ]
    if not isinstance(pb003_evidence, list):
        fail("PB-003 must list no-claim adapter contract evidence")
    missing_pb003_evidence = [
        path for path in required_pb003_evidence if path not in pb003_evidence
    ]
    if missing_pb003_evidence:
        fail(
            "PB-003 evidence is missing adapter contract records: "
            + ", ".join(missing_pb003_evidence)
        )
    pb003_required = " ".join(
        value for value in pb003.get("evidence_required", []) if isinstance(value, str)
    )
    pb003_required = pb003_required.lower()
    for old, new in [
        ("toolkit neutral", "toolkit-neutral"),
        ("adapter contract", "adapter-contract"),
        ("native adapter", "native-adapter"),
        ("update authority", "update-authority"),
        ("owner review", "owner-review"),
    ]:
        pb003_required = pb003_required.replace(old, new)
    for phrase in [
        "adr-0013",
        "toolkit-neutral state",
        "command",
        "surface",
        "accessibility",
        "diagnostic",
        "adapter-contract",
        "native-adapter prototype",
        "navigation",
        "profile",
        "permission",
        "credential",
        "agent",
        "plug-in",
        "persistence",
        "update-authority",
        "owner-review",
    ]:
        if phrase not in pb003_required:
            fail(f"PB-003 evidence_required must include {phrase}")

    pb004 = next((item for item in readiness_items if item.get("id") == "PB-004"), None)
    if not isinstance(pb004, dict):
        fail("pre-build readiness is missing PB-004")
    if pb004.get("status") != "partial":
        fail("PB-004 must remain partial while only no-claim framework bake-off evidence exists")
    pb004_evidence = pb004.get("evidence")
    required_pb004_evidence = [
        "docs/research/native-ui-framework-bakeoff-inventory-2026-07.md",
        "docs/ui-runtime/machine/framework-bakeoff-inventory.schema.json",
        "docs/ui-runtime/machine/framework-bakeoff-inventory.json",
        "tools/validate_framework_bakeoff.py",
    ]
    if not isinstance(pb004_evidence, list):
        fail("PB-004 must list no-claim framework bake-off evidence")
    missing_pb004_evidence = [
        path for path in required_pb004_evidence if path not in pb004_evidence
    ]
    if missing_pb004_evidence:
        fail(
            "PB-004 evidence is missing framework bake-off records: "
            + ", ".join(missing_pb004_evidence)
        )
    pb004_required = " ".join(
        value for value in pb004.get("evidence_required", []) if isinstance(value, str)
    )
    pb004_required = pb004_required.lower()
    for old, new in [
        ("owner approved", "owner-approved"),
        ("reference shell", "reference-shell"),
        ("three adapter", "three-adapter"),
        ("gpu loss", "gpu-loss"),
        ("gpu device loss", "gpu-loss"),
        ("frame pacing", "frame-pacing"),
        ("runtime react", "runtime-react"),
        ("runtime dom", "runtime-dom"),
        ("runtime css", "runtime-css"),
        ("system webview", "system-webview"),
    ]:
        pb004_required = pb004_required.replace(old, new)
    for phrase in [
        "three-adapter",
        "owner-approved reduced reference-shell bake-off",
        "equivalent shell tasks",
        "adr-0014",
        "accessibility",
        "ime",
        "keyboard",
        "crash",
        "gpu-loss",
        "startup",
        "memory",
        "binary",
        "latency",
        "frame-pacing",
        "energy",
        "license",
        "dependency",
        "provenance",
        "owner review",
        "electron",
        "tauri",
        "system-webview",
        "node",
        "runtime-react",
        "runtime-dom",
        "runtime-css parser",
    ]:
        if phrase not in pb004_required:
            fail(f"PB-004 evidence_required must include {phrase}")

    pb005 = next((item for item in readiness_items if item.get("id") == "PB-005"), None)
    if not isinstance(pb005, dict):
        fail("pre-build readiness is missing PB-005")
    if pb005.get("status") != "partial":
        fail("PB-005 must remain partial while only no-claim page-surface composition evidence exists")
    pb005_evidence = pb005.get("evidence")
    required_pb005_evidence = [
        "docs/research/page-surface-composition-inventory-2026-07.md",
        "docs/ui-runtime/machine/page-surface-composition.schema.json",
        "docs/ui-runtime/machine/page-surface-composition.json",
        "tools/validate_page_surface_composition.py",
    ]
    if not isinstance(pb005_evidence, list):
        fail("PB-005 must list no-claim page-surface composition evidence")
    missing_pb005_evidence = [
        path for path in required_pb005_evidence if path not in pb005_evidence
    ]
    if missing_pb005_evidence:
        fail(
            "PB-005 evidence is missing page-surface composition records: "
            + ", ".join(missing_pb005_evidence)
        )
    pb005_required = " ".join(
        value for value in pb005.get("evidence_required", []) if isinstance(value, str)
    )
    pb005_required = pb005_required.lower()
    for old, new in [
        ("ui gate", "ui-gate"),
        ("page surface", "page-surface"),
        ("renderer crash", "renderer-crash"),
        ("gpu device loss", "gpu-device-loss"),
        ("gpu loss", "gpu-device-loss"),
        ("surface handles", "surface-handles"),
        ("surface handle", "surface-handle"),
        ("software fallback", "software-fallback"),
        ("frame pacing", "frame-pacing"),
    ]:
        pb005_required = pb005_required.replace(old, new)
    for phrase in [
        "ui-gate-7",
        "adr-0016",
        "renderer-produced page textures",
        "resize",
        "scale",
        "damage",
        "input",
        "ime",
        "accessibility",
        "occlusion",
        "capture",
        "renderer-crash",
        "gpu-device-loss",
        "typed page-surface-handles",
        "document",
        "device generations",
        "brokered surface-handle",
        "software-fallback",
        "stale",
        "latency",
        "frame-pacing",
        "owner review",
    ]:
        if phrase not in pb005_required:
            fail(f"PB-005 evidence_required must include {phrase}")

    pb014 = next((item for item in readiness_items if item.get("id") == "PB-014"), None)
    if not isinstance(pb014, dict):
        fail("pre-build readiness is missing PB-014")
    if pb014.get("status") != "partial":
        fail("PB-014 must remain partial while only no-claim planning evidence exists")
    pb014_evidence = pb014.get("evidence")
    required_pb014_evidence = [
        "docs/research/native-ui-component-fixture-inventory-2026-07.md",
        "docs/ui-runtime/machine/component-fixture-inventory.schema.json",
        "docs/ui-runtime/machine/component-fixture-inventory.json",
        "tools/validate_ui_component_fixtures.py",
    ]
    if not isinstance(pb014_evidence, list):
        fail("PB-014 must list no-claim planning evidence")
    missing_pb014_evidence = [
        path for path in required_pb014_evidence if path not in pb014_evidence
    ]
    if missing_pb014_evidence:
        fail(
            "PB-014 evidence is missing fixture inventory records: "
            + ", ".join(missing_pb014_evidence)
        )
    pb014_required = " ".join(
        value for value in pb014.get("evidence_required", []) if isinstance(value, str)
    )
    pb014_required = pb014_required.lower()
    for old, new in [
        ("screen reader", "screen-reader"),
        ("forced color", "forced-color"),
        ("high contrast", "high-contrast"),
        ("reduced motion", "reduced-motion"),
        ("error state", "error-state"),
        ("browser_chrome", "browser chrome"),
        ("recovery_ui", "recovery ui"),
    ]:
        pb014_required = pb014_required.replace(old, new)
    for phrase in [
        "rendered fixture pack",
        "adapter-specific",
        "browser chrome",
        "tabs",
        "spaces",
        "command field",
        "permission prompts",
        "agent confirmations",
        "resource manager",
        "settings",
        "recovery ui",
        "keyboard",
        "focus",
        "screen-reader",
        "forced-color",
        "high-contrast",
        "reduced-motion",
        "density",
        "localization",
        "error-state",
        "owner review",
    ]:
        if phrase not in pb014_required:
            fail(f"PB-014 evidence_required must include {phrase}")

    pb015 = next((item for item in readiness_items if item.get("id") == "PB-015"), None)
    if not isinstance(pb015, dict):
        fail("pre-build readiness is missing PB-015")
    if pb015.get("status") != "partial":
        fail("PB-015 must remain partial while only no-claim workflow inventory evidence exists")
    pb015_evidence = pb015.get("evidence")
    required_pb015_evidence = [
        "docs/research/window-input-accessibility-spike-inventory-2026-07.md",
        "docs/accessibility/machine/window-input-accessibility-spike.schema.json",
        "docs/accessibility/machine/window-input-accessibility-spike.json",
        "tools/validate_window_input_accessibility_spike.py",
    ]
    if not isinstance(pb015_evidence, list):
        fail("PB-015 must list no-claim workflow inventory evidence")
    missing_pb015_evidence = [
        path for path in required_pb015_evidence if path not in pb015_evidence
    ]
    if missing_pb015_evidence:
        fail(
            "PB-015 evidence is missing window/input/accessibility spike records: "
            + ", ".join(missing_pb015_evidence)
        )
    pb015_required = " ".join(
        value for value in pb015.get("evidence_required", []) if isinstance(value, str)
    )
    pb015_required = pb015_required.lower()
    for old, new in [
        ("gpu loss", "gpu-loss"),
        ("gpu device loss", "gpu-loss"),
        ("page tree", "page-tree"),
        ("drag/drop", "drag-drop"),
        ("drag drop", "drag-drop"),
        ("assistive technology", "assistive-technology"),
        ("screen reader", "screen-reader"),
        ("high-contrast", "high contrast"),
        ("reduced-motion", "reduced motion"),
        ("reference platform", "reference-platform"),
    ]:
        pb015_required = pb015_required.replace(old, new)
    for phrase in [
        "reference-platform",
        "workflow matrix",
        "windowing",
        "input",
        "ime",
        "accessibility",
        "page-tree composition",
        "clipboard",
        "drag-drop",
        "localization",
        "zoom",
        "high contrast",
        "forced colors",
        "reduced motion",
        "crash recovery",
        "renderer hang",
        "gpu-loss",
        "manual assistive-technology",
        "screen-reader",
        "platform accessibility tree",
        "latency",
        "owner review",
        "ui-gate-7",
        "ui-gate-10",
    ]:
        if phrase not in pb015_required:
            fail(f"PB-015 evidence_required must include {phrase}")

    pb011 = next((item for item in readiness_items if item.get("id") == "PB-011"), None)
    if not isinstance(pb011, dict):
        fail("pre-build readiness is missing PB-011")
    if pb011.get("status") != "partial":
        fail("PB-011 must remain partial while only no-claim boundary inventory, schema-source template, and readiness-review template exist")
    pb011_evidence = pb011.get("evidence")
    required_pb011_evidence = [
        "docs/research/ipc-capability-boundary-inventory-2026-07.md",
        "docs/blueprint-v1/machine/ipc-capability-boundary.schema.json",
        "docs/blueprint-v1/machine/ipc-capability-boundary.json",
        "docs/blueprint-v1/machine/ipc-schema-source.schema.json",
        "docs/blueprint-v1/machine/ipc-schema-sources/no-claim-control-envelope-template.json",
        "docs/blueprint-v1/machine/ipc-readiness-review.schema.json",
        "docs/blueprint-v1/machine/ipc-readiness-reviews/no-claim-ipc-readiness-template.json",
        "tools/validate_ipc_capability_boundaries.py",
        "tools/validate_ipc_readiness_review.py",
    ]
    if not isinstance(pb011_evidence, list):
        fail("PB-011 must list no-claim boundary inventory evidence")
    missing_pb011_evidence = [
        path for path in required_pb011_evidence if path not in pb011_evidence
    ]
    if missing_pb011_evidence:
        fail(
            "PB-011 evidence is missing IPC capability boundary records: "
            + ", ".join(missing_pb011_evidence)
        )
    pb011_required = " ".join(
        value for value in pb011.get("evidence_required", []) if isinstance(value, str)
    )
    for phrase in [
        "schema generator",
        "checked no-claim schema-source template",
        "checked no-claim IPC readiness-review template",
        "wire encoding decision",
        "connection authentication",
        "bounded queues",
        "backpressure",
        "malformed",
        "oversized",
        "stale",
        "duplicate",
        "reordered",
        "unauthorized",
        "wrong-principal",
        "timeout",
        "cancellation",
        "owner-reviewed IPC readiness review",
    ]:
        if phrase not in pb011_required:
            fail(f"PB-011 evidence_required must include {phrase}")

    prebuild_audit = (RESEARCH / "pre-build-readiness-gap-audit-2026-07.md").read_text(
        encoding="utf-8"
    )
    prebuild_checklist = (
        DOCS / "project-buildout" / "11-pre-build-readiness-checklist.md"
    ).read_text(encoding="utf-8")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        for phrase in ("wrong-principal", "timeout", "cancellation"):
            if phrase not in text:
                fail(f"{label} is missing PB-011 negative coverage for {phrase}")

    pb012 = next((item for item in readiness_items if item.get("id") == "PB-012"), None)
    if not isinstance(pb012, dict):
        fail("pre-build readiness is missing PB-012")
    if pb012.get("status") != "partial":
        fail("PB-012 must remain partial while only no-claim sandbox probe inventory, operation/evidence contract, probe-package template, and readiness-review template exist")
    pb012_evidence = pb012.get("evidence")
    required_pb012_evidence = [
        "docs/research/sandbox-probe-inventory-2026-07.md",
        "docs/research/wp-003-sandbox-probe-plan-2026-07.md",
        "docs/security-engine/machine/sandbox-probe-inventory.schema.json",
        "docs/security-engine/machine/sandbox-probe-inventory.json",
        "docs/security-engine/machine/sandbox-probe-package.schema.json",
        "docs/security-engine/machine/sandbox-probe-packages/no-claim-expected-deny-template.json",
        "docs/security-engine/machine/sandbox-readiness-review.schema.json",
        "docs/security-engine/machine/sandbox-readiness-reviews/no-claim-sandbox-readiness-template.json",
        "schemas/sandbox/probe-catalog.json",
        "schemas/sandbox/probe-evidence.schema.json",
        "tools/validate_sandbox_contracts.py",
        "tools/validate_sandbox_probe_inventory.py",
        "tools/validate_sandbox_readiness_review.py",
    ]
    if not isinstance(pb012_evidence, list):
        fail("PB-012 must list no-claim sandbox probe inventory evidence")
    missing_pb012_evidence = [
        path for path in required_pb012_evidence if path not in pb012_evidence
    ]
    if missing_pb012_evidence:
        fail(
            "PB-012 evidence is missing sandbox probe inventory records: "
            + ", ".join(missing_pb012_evidence)
        )
    pb012_required = " ".join(
        value for value in pb012.get("evidence_required", []) if isinstance(value, str)
    ).lower().replace("shared memory", "shared-memory")
    sandbox_roles = [
        "renderer",
        "network",
        "storage",
        "gpu",
        "decoder",
        "extension",
        "devtools",
        "agent",
        "updater",
    ]
    sandbox_surfaces = [
        "file",
        "socket",
        "process",
        "registry",
        "device",
        "shared-memory",
        "credential",
        "debug",
        "profile",
        "ipc",
    ]
    sandbox_required_terms = [
        *sandbox_roles,
        *sandbox_surfaces,
        "packaged expected-deny probes",
        "checked no-claim probe-package template",
        "checked no-claim sandbox readiness-review template",
        "effective platform policy",
        "host-safe",
        "owner review",
        "owner-reviewed sandbox readiness review",
    ]
    for phrase in sandbox_required_terms:
        if phrase not in pb012_required:
            fail(f"PB-012 evidence_required must include {phrase}")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        normalized = text.lower().replace("shared memory", "shared-memory")
        for phrase in [*sandbox_roles, *sandbox_surfaces]:
            if phrase not in normalized:
                fail(f"{label} is missing PB-012 sandbox coverage for {phrase}")

    pb016 = next((item for item in readiness_items if item.get("id") == "PB-016"), None)
    if not isinstance(pb016, dict):
        fail("pre-build readiness is missing PB-016")
    if pb016.get("status") != "partial":
        fail("PB-016 must remain partial while only no-claim planning evidence exists")
    pb016_evidence = pb016.get("evidence")
    required_pb016_evidence = [
        "docs/research/profile-session-format-inventory-2026-07.md",
        "docs/storage/machine/profile-session-format-inventory.schema.json",
        "docs/storage/machine/profile-session-format-inventory.json",
        "docs/storage/machine/profile-session-schema-package.schema.json",
        "docs/storage/machine/profile-session-schema-packages/no-claim-profile-session-schema-template.json",
        "tools/validate_profile_session_formats.py",
    ]
    if not isinstance(pb016_evidence, list):
        fail("PB-016 must list no-claim planning evidence")
    missing_pb016_evidence = [
        path for path in required_pb016_evidence if path not in pb016_evidence
    ]
    if missing_pb016_evidence:
        fail(
            "PB-016 evidence is missing profile/session records: "
            + ", ".join(missing_pb016_evidence)
        )

    def normalize_profile_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("private-session", "private session"),
            ("crash-recovery", "crash recovery"),
            ("protected-work", "protected work"),
            ("data-loss", "data loss"),
            ("real-profile", "real profile"),
            ("user-data", "user data"),
            ("credential-storage", "credential storage"),
            ("profile-format", "profile format"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    profile_terms = [
        "profile",
        "space",
        "session",
        "snapshot",
        "migration",
        "disk full",
        "power loss",
        "corruption",
        "downgrade",
        "export",
        "deletion",
        "private session",
        "crash recovery",
        "protected work",
        "privacy",
        "data loss",
        "sync",
        "credential storage",
        "real profile",
        "user data",
        "production profile format",
    ]
    pb016_required = normalize_profile_text(
        " ".join(
            value for value in pb016.get("evidence_required", []) if isinstance(value, str)
        )
    )
    for phrase in profile_terms:
        if phrase not in pb016_required:
            fail(f"PB-016 evidence_required must include {phrase}")
    for phrase in [
        "checked no-claim schema-package template",
        "schemas beyond the checked no-claim schema-package template",
    ]:
        if phrase not in pb016_required:
            fail(f"PB-016 evidence_required must include {phrase}")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        normalized = normalize_profile_text(text)
        for phrase in profile_terms:
            if phrase not in normalized:
                fail(f"{label} is missing PB-016 profile/session coverage for {phrase}")

    native_pb_ids = {"PB-003", "PB-004", "PB-005", "PB-014", "PB-015"}
    native_items = [
        item for item in readiness_items if item.get("id") in native_pb_ids
    ]
    if {item.get("id") for item in native_items} != native_pb_ids:
        fail("pre-build readiness is missing one or more native shell PB entries")

    def normalize_native_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("page surface", "page-surface"),
            ("gpu loss", "gpu-loss"),
            ("design token", "design-token"),
            ("component fixture", "component-fixture"),
            ("frame pacing", "frame-pacing"),
            ("trusted chrome", "trusted-chrome"),
            ("release path ui", "release-path ui"),
            ("page tree", "page-tree"),
            ("drag/drop", "drag-drop"),
            ("drag drop", "drag-drop"),
            ("screen reader", "screen-reader"),
            ("assistive technology", "assistive-technology"),
            ("high-contrast", "high contrast"),
            ("reduced-motion", "reduced motion"),
            ("renderer-hang", "renderer hang"),
        ]:
            normalized = normalized.replace(old, new)
        return normalized

    native_terms = [
        "toolkit-neutral",
        "state",
        "command",
        "surface",
        "diagnostic",
        "adapter",
        "equivalent",
        "page-surface",
        "design-token",
        "component",
        "accessibility",
        "ime",
        "keyboard",
        "page-tree",
        "clipboard",
        "drag-drop",
        "localization",
        "zoom",
        "high contrast",
        "reduced motion",
        "screen-reader",
        "manual assistive-technology",
        "crash",
        "renderer hang",
        "gpu-loss",
        "startup",
        "memory",
        "binary",
        "latency",
        "frame-pacing",
        "energy",
        "license",
        "dependency",
        "provenance",
    ]
    native_readiness_text = normalize_native_text(
        " ".join(
            value
            for item in native_items
            for field in ("evidence", "evidence_required")
            for value in item.get(field, [])
            if isinstance(value, str)
        )
    )
    for phrase in native_terms:
        if phrase not in native_readiness_text:
            fail(f"native shell PB evidence_required must include {phrase}")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        normalized = normalize_native_text(text)
        for phrase in native_terms:
            if phrase not in normalized:
                fail(f"{label} is missing native shell coverage for {phrase}")

    pb017 = next((item for item in readiness_items if item.get("id") == "PB-017"), None)
    pb018 = next((item for item in readiness_items if item.get("id") == "PB-018"), None)
    if not isinstance(pb017, dict):
        fail("pre-build readiness is missing PB-017")
    if not isinstance(pb018, dict):
        fail("pre-build readiness is missing PB-018")
    if pb017.get("status") != "partial":
        fail("PB-017 must remain partial while only no-claim planning evidence exists")
    pb017_evidence = pb017.get("evidence")
    required_pb017_evidence = [
        "docs/research/research-package-update-lab-inventory-2026-07.md",
        "docs/release-operations/machine/research-package-update-lab.schema.json",
        "docs/release-operations/machine/research-package-update-lab.json",
        "docs/release-operations/machine/research-package-update-lab-package.schema.json",
        "docs/release-operations/machine/research-package-update-lab-packages/no-claim-update-lab-template.json",
        "tools/validate_research_package_update_lab.py",
    ]
    if not isinstance(pb017_evidence, list):
        fail("PB-017 must list no-claim planning evidence")
    missing_pb017_evidence = [
        path for path in required_pb017_evidence if path not in pb017_evidence
    ]
    if missing_pb017_evidence:
        fail(
            "PB-017 evidence is missing research package/update lab records: "
            + ", ".join(missing_pb017_evidence)
        )
    if pb018.get("status") != "partial":
        fail("PB-018 must remain partial while only no-claim planning evidence exists")
    pb018_evidence = pb018.get("evidence")
    required_pb018_evidence = [
        "docs/research/incident-patch-rehearsal-inventory-2026-07.md",
        "docs/security-engine/machine/incident-patch-rehearsal.schema.json",
        "docs/security-engine/machine/incident-patch-rehearsal.json",
        "docs/security-engine/machine/incident-patch-rehearsal-record.schema.json",
        "docs/security-engine/machine/incident-patch-rehearsal-records/no-claim-incident-patch-rehearsal-template.json",
        "tools/validate_incident_patch_rehearsal.py",
    ]
    if not isinstance(pb018_evidence, list):
        fail("PB-018 must list no-claim planning evidence")
    missing_pb018_evidence = [
        path for path in required_pb018_evidence if path not in pb018_evidence
    ]
    if missing_pb018_evidence:
        fail(
            "PB-018 evidence is missing incident patch rehearsal records: "
            + ", ".join(missing_pb018_evidence)
        )

    def normalize_operational_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("build id", "build id"),
            ("artifact hash", "artifact hashes"),
            ("artifact size", "artifact sizes"),
            ("no stable support", "no-stable-support"),
            ("minimum-secure-version", "minimum secure version"),
            ("wrong-target", "wrong target"),
            ("partial-write", "partial write"),
            ("disk-full", "disk full"),
            ("power-loss", "power loss"),
            ("user-profile", "user profile"),
            ("vulnerable-version", "vulnerable version"),
            ("crash loop", "crash-loop"),
            ("stable-channel", "stable channel"),
            ("private-intake", "private intake"),
            ("affected-version", "affected version"),
            ("embargoed ci", "embargoed ci"),
            ("user/admin", "user and admin"),
            ("cve", "cve"),
            ("stable-promotion", "stable promotion"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    updater_terms = [
        "signed research-package",
        "source commit",
        "build id",
        "channel",
        "platform",
        "architecture",
        "toolchain",
        "feature set",
        "sbom",
        "provenance",
        "symbols",
        "notices",
        "artifact hashes",
        "artifact sizes",
        "no-stable-support",
        "role separation",
        "signature threshold",
        "expiry",
        "minimum secure version",
        "rollout",
        "mirrors",
        "tamper",
        "replay",
        "wrong target",
        "partial write",
        "disk full",
        "power loss",
        "rollback",
        "vulnerable version",
        "migration",
        "downgrade",
        "crash-loop",
        "privacy-preserving",
        "production signing",
        "offline root",
        "stable channel",
        "public binary distribution",
        "real updater",
        "real user profile",
    ]
    pb017_required = normalize_operational_text(
        " ".join(
            value for value in pb017.get("evidence_required", []) if isinstance(value, str)
        )
    )
    for phrase in updater_terms:
        if phrase not in pb017_required:
            fail(f"PB-017 evidence_required must include {phrase}")
    for phrase in [
        "checked no-claim update-lab package template",
        "beyond the checked no-claim update-lab package template",
    ]:
        if phrase not in pb017_required:
            fail(f"PB-017 evidence_required must include {phrase}")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        normalized = normalize_operational_text(text)
        for phrase in updater_terms:
            if phrase not in normalized:
                fail(f"{label} is missing PB-017 updater coverage for {phrase}")

    incident_terms = [
        "private intake",
        "access control",
        "acknowledgement",
        "reproduction",
        "severity",
        "asset analysis",
        "affected version",
        "embargo",
        "sanitized evidence",
        "protected patch branch",
        "embargoed ci",
        "regression",
        "backport",
        "signing",
        "update dry run",
        "staged rollout",
        "minimum secure version",
        "revocation",
        "release notes",
        "user and admin communication",
        "cve",
        "credit",
        "coordinated disclosure",
        "postmortem",
        "incident-class",
        "active exploitation",
        "update or signing compromise",
        "dependency vulnerability",
        "data loss",
        "privacy leak",
        "sandbox regression",
        "malicious extension",
        "provider",
        "service outage",
        "role matrix",
        "timing targets",
        "escalation",
        "secret rotation",
        "agent",
        "stable promotion",
        "signing authority",
    ]
    pb018_required = normalize_operational_text(
        " ".join(
            value for value in pb018.get("evidence_required", []) if isinstance(value, str)
        )
    )
    for phrase in incident_terms:
        if phrase not in pb018_required:
            fail(f"PB-018 evidence_required must include {phrase}")
    for phrase in [
        "checked no-claim incident patch rehearsal template",
        "beyond the checked no-claim incident patch rehearsal template",
    ]:
        if phrase not in pb018_required:
            fail(f"PB-018 evidence_required must include {phrase}")
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
    ]:
        normalized = normalize_operational_text(text)
        for phrase in incident_terms:
            if phrase not in normalized:
                fail(f"{label} is missing PB-018 incident coverage for {phrase}")

    pb019 = next((item for item in readiness_items if item.get("id") == "PB-019"), None)
    if not isinstance(pb019, dict):
        fail("pre-build readiness is missing PB-019")
    if pb019.get("status") != "blocked":
        fail("PB-019 must remain blocked while backup ownership is only checked gap evidence")
    pb019_evidence = pb019.get("evidence")
    required_pb019_evidence = [
        "docs/research/backup-ownership-gap-inventory-2026-07.md",
        "docs/project-buildout/machine/backup-ownership-gap.schema.json",
        "docs/project-buildout/machine/backup-ownership-gap.json",
        "docs/project-buildout/machine/backup-owner-qualification-record.schema.json",
        "docs/project-buildout/machine/backup-owner-qualification-records/no-claim-backup-owner-qualification-template.json",
        "tools/validate_backup_ownership_gap.py",
    ]
    if not isinstance(pb019_evidence, list):
        fail("PB-019 must list checked blocked gap inventory evidence")
    missing_pb019_evidence = [
        path for path in required_pb019_evidence if path not in pb019_evidence
    ]
    if missing_pb019_evidence:
        fail(
            "PB-019 evidence is missing backup ownership gap records: "
            + ", ".join(missing_pb019_evidence)
        )

    def normalize_ownership_text(text: str) -> str:
        normalized = text.lower()
        for old, new in [
            ("ui runtime", "ui-runtime"),
            ("privacy data", "privacy-data"),
            ("release operations", "release-operations"),
            ("human release authority", "human-release-authority"),
            ("incident response", "incident-response"),
            ("legal community", "legal-community"),
            ("documentation research", "documentation-research"),
            ("agent operations", "agent-operations"),
            ("review rule", "review-rule"),
            ("escalation policy", "escalation-policy"),
            ("repository access", "repository-access"),
            ("no stale access", "stale privileged access"),
            ("stale access", "stale privileged access"),
            ("ownerless-path", "ownerless protected path"),
            ("ownerless protected-path", "ownerless protected path"),
            ("primary-only path", "primary-only path"),
            ("primary only", "primary-only"),
            ("blocked-status", "blocked status"),
            ("single-owner-risk", "single-owner residual-risk"),
            ("residual risk", "residual-risk"),
            ("two person", "two-person"),
            ("supported-version", "supported-version"),
            ("security disclosure", "security-disclosure"),
            ("incident-closure", "incident closure"),
            ("legal-approval", "legal approval"),
            ("update-trust", "update trust"),
        ]:
            normalized = normalized.replace(old.lower(), new.lower())
        return normalized

    ownership_terms = [
        "qualified backup",
        "program",
        "architecture",
        "security",
        "release-operations",
        "human-release-authority",
        "incident-response",
        "legal-community",
        "support",
        "quality",
        "supply-chain",
        "documentation-research",
        "product",
        "platform",
        "engine",
        "javascript",
        "networking",
        "storage",
        "performance",
        "accessibility",
        "ui-runtime",
        "agent-operations",
        "privacy-data",
        "role level",
        "subsystem competence",
        "representative path coverage",
        "recent review record",
        "availability",
        "succession",
        "recusal",
        "inactivity",
        "removal",
        "emergency replacement",
        "codeowners",
        "review-rule",
        "escalation-policy",
        "signing",
        "disclosure",
        "package",
        "ci",
        "service",
        "repository-access",
        "stale privileged access",
        "ownerless protected path",
        "primary-only",
        "blocked status",
        "single-owner",
        "residual-risk",
        "two-person control",
        "update trust",
        "supported-version",
        "security-disclosure",
        "irreversible",
        "migration",
        "release promotion",
        "legal approval",
        "incident closure",
    ]
    pb019_required = normalize_ownership_text(
        " ".join(
            value for value in pb019.get("evidence_required", []) if isinstance(value, str)
        )
    )
    for phrase in ownership_terms:
        if phrase not in pb019_required:
            fail(f"PB-019 evidence_required must include {phrase}")
    for phrase in [
        "checked no-claim backup-owner qualification template",
        "beyond the checked no-claim backup-owner qualification template",
    ]:
        if phrase not in pb019_required:
            fail(f"PB-019 evidence_required must include {phrase}")
    board = (DOCS / "project-buildout" / "13-build-readiness-operating-board.md").read_text(
        encoding="utf-8"
    )
    human_queue = (DOCS / "project-buildout" / "17-build-readiness-task-queue.md").read_text(
        encoding="utf-8"
    )
    for label, text in [
        ("pre-build readiness audit", prebuild_audit),
        ("pre-build readiness checklist", prebuild_checklist),
        ("build readiness board", board),
        ("build readiness task queue", human_queue),
    ]:
        normalized = normalize_ownership_text(text)
        for phrase in ownership_terms:
            if phrase not in normalized:
                fail(f"{label} is missing PB-019 ownership coverage for {phrase}")
        for phrase in ["checked no-claim backup-owner qualification template"]:
            if phrase not in normalized:
                fail(f"{label} is missing PB-019 ownership coverage for {phrase}")

    owner_records = owners.get("owners", []) if isinstance(owners, dict) else []
    if any(item.get("backup") is None for item in owner_records if isinstance(item, dict)):
        if pb019.get("status") != "blocked":
            fail("PB-019 must remain blocked while any professional owner backup is null")

    pb020 = next((item for item in readiness_items if item.get("id") == "PB-020"), None)
    if not isinstance(pb020, dict):
        fail("pre-build readiness is missing PB-020")
    if pb020.get("status") != "partial":
        fail("PB-020 must remain partial until owner review resolves remaining P0 items")
    pb020_evidence = pb020.get("evidence")
    required_pb020_evidence = [
        "docs/project-buildout/11-pre-build-readiness-checklist.md",
        "docs/project-buildout/13-build-readiness-operating-board.md",
        "docs/project-buildout/17-build-readiness-task-queue.md",
        "docs/project-buildout/18-documentation-readiness-evidence-matrix.md",
        "docs/blueprint-v1/machine/build-readiness-task-queue.json",
        "docs/research/implementation-kickoff-review-inventory-2026-07.md",
        "docs/project-buildout/machine/implementation-kickoff-review.schema.json",
        "docs/project-buildout/machine/implementation-kickoff-review.json",
        "docs/research/build-readiness-dependency-graph-inventory-2026-07.md",
        "docs/project-buildout/machine/build-readiness-dependency-graph.schema.json",
        "docs/project-buildout/machine/build-readiness-dependency-graph.json",
        "docs/research/documentation-readiness-completion-audit-2026-07.md",
        "docs/project-buildout/machine/documentation-readiness-completion-audit.schema.json",
        "docs/project-buildout/machine/documentation-readiness-completion-audit.json",
        "docs/project-buildout/machine/build-readiness-closure-review.schema.json",
        "docs/project-buildout/machine/build-readiness-closure-reviews/no-claim-build-readiness-closure-template.json",
        "docs/research/m0-build-foundation-2026-07.md",
        "tools/validate_implementation_kickoff_review.py",
        "tools/validate_build_readiness_dependency_graph.py",
        "tools/validate_documentation_readiness_completion_audit.py",
        "tools/validate_blueprint.py",
        "tools/check.ps1",
    ]
    if not isinstance(pb020_evidence, list):
        fail("PB-020 must list implementation kickoff review evidence")
    missing_pb020_evidence = [
        path for path in required_pb020_evidence if path not in pb020_evidence
    ]
    if missing_pb020_evidence:
        fail(
            "PB-020 evidence is missing kickoff review records: "
            + ", ".join(missing_pb020_evidence)
        )
    pb020_required = " ".join(
        value for value in pb020.get("evidence_required", []) if isinstance(value, str)
    ).lower()
    for old, new in [
        ("source-strategy", "source strategy"),
        ("fresh host", "fresh-host"),
        ("native shell", "native-shell"),
        ("profile session", "profile/session"),
        ("package update", "package/update"),
    ]:
        pb020_required = pb020_required.replace(old, new)
    for phrase in [
        "implementation kickoff review inventory",
        "build-readiness dependency graph",
        "dependency graph",
        "documentation-readiness completion audit",
        "completion audit",
        "all-information-ready-for-building",
        "remaining p0 items",
        "m1 expansion",
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
        "build-readiness closure-review template",
        "closure-review",
    ]:
        if phrase not in pb020_required:
            fail(f"PB-020 evidence_required must include {phrase}")

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
    if "twenty-seven detailed engineering and product books" not in root_readme:
        fail("root README detailed-book count is stale")
    templates_index = (DOCS / "templates" / "README.md").read_text(encoding="utf-8")
    if "ui-framework-experiment.md" not in templates_index:
        fail("templates index is missing the UI framework experiment")
    issue_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "engineering.yml").read_text(encoding="utf-8")
    for identifier in ("OP-...", "UIF-...", "UIB-...", "PB-...", "TASK-..."):
        if identifier not in issue_template:
            fail(f"engineering issue template is missing identifier: {identifier}")
    project_index = (DOCS / "project-buildout" / "README.md").read_text(encoding="utf-8")
    if "11-pre-build-readiness-checklist.md" not in project_index:
        fail("project-buildout index is missing pre-build readiness checklist")


def check_adr_0009_evidence_controls() -> None:
    validator = ROOT / "tools" / "validate_adr_0009_evidence.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "ADR-0009 evidence validation failed")

    evidence = load_json(MACHINE / "adr-0009-evidence.json")
    if evidence.get("schema_version") != 1:
        fail("adr-0009-evidence.json must use schema_version 1")
    if evidence.get("adr_id") != "ADR-0009":
        fail("adr-0009-evidence.json must track ADR-0009")
    if evidence.get("readiness_gate") != "PB-002":
        fail("adr-0009-evidence.json must track PB-002")
    if evidence.get("decision_status") != "no_source_strategy_decision":
        fail("ADR-0009 must remain no_source_strategy_decision until owner review")
    claim_status = evidence.get("claim_status")
    if not isinstance(claim_status, str):
        fail("adr-0009-evidence.json is missing claim_status")
    for phrase in [
        "no Servo source strategy",
        "no dependency approval",
        "no component approval",
        "no performance claim",
        "no release-code authorization",
    ]:
        if phrase not in claim_status:
            fail(f"ADR-0009 claim_status must mention: {phrase}")

    owners = load_json(MACHINE / "professional-owners.json")
    owner_scopes = {item.get("scope") for item in owners.get("owners", [])}
    items = evidence.get("items")
    if not isinstance(items, list):
        fail("adr-0009-evidence.json must contain an items array")
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    expected_ids = [f"ADR9-EV-{index:03d}" for index in range(1, 19)]
    if ids != expected_ids:
        fail(f"ADR-0009 evidence IDs must be ADR9-EV-001 through ADR9-EV-018; found {ids}")

    allowed_status = {
        "partial",
        "missing",
        "captured",
        "owner_review_required",
        "owner_reviewed",
        "blocked",
    }
    required_fields = {
        "id",
        "decision_area",
        "status",
        "owner_scopes",
        "existing_evidence",
        "missing_outputs",
        "next_action",
    }
    for item in items:
        if not isinstance(item, dict):
            fail("ADR-0009 evidence items must be objects")
        missing = required_fields - set(item)
        if missing:
            fail(f"{item.get('id')}: missing ADR-0009 evidence fields: {', '.join(sorted(missing))}")
        status = item.get("status")
        if status not in allowed_status:
            fail(f"{item.get('id')}: unknown ADR-0009 evidence status: {status}")
        scopes = item.get("owner_scopes")
        if not isinstance(scopes, list) or not scopes:
            fail(f"{item.get('id')}: owner_scopes must be a non-empty array")
        unknown_scopes = sorted(set(scopes) - owner_scopes)
        if unknown_scopes:
            fail(f"{item.get('id')}: unknown owner scopes: {', '.join(unknown_scopes)}")
        for field in ("decision_area", "next_action"):
            if not isinstance(item.get(field), str) or not item[field]:
                fail(f"{item.get('id')}: {field} must be a non-empty string")
        for field in ("existing_evidence", "missing_outputs"):
            if not isinstance(item.get(field), list) or any(
                not isinstance(value, str) or not value for value in item[field]
            ):
                fail(f"{item.get('id')}: {field} must be an array of strings")
        if status in {"partial", "owner_review_required"} and not item["existing_evidence"]:
            fail(f"{item.get('id')}: {status} items require existing_evidence")
        if status != "owner_reviewed" and not item["missing_outputs"]:
            fail(f"{item.get('id')}: unresolved items require missing_outputs")
        if status == "blocked":
            blockers = item.get("blocked_by")
            if not isinstance(blockers, list) or not blockers:
                fail(f"{item.get('id')}: blocked items require blocked_by")
            if any(blocker not in expected_ids for blocker in blockers):
                fail(f"{item.get('id')}: blocked_by contains an unknown ADR9-EV id")
        elif "blocked_by" in item:
            fail(f"{item.get('id')}: only blocked items may declare blocked_by")

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    readiness_items = readiness.get("items") if isinstance(readiness, dict) else []
    pb002 = next((item for item in readiness_items if item.get("id") == "PB-002"), None)
    if not isinstance(pb002, dict) or pb002.get("status") != "blocked":
        fail("PB-002 must remain blocked while ADR-0009 evidence is unresolved")
    if "docs/blueprint-v1/machine/adr-0009-evidence.json" not in pb002.get("evidence", []):
        fail("PB-002 evidence must include adr-0009-evidence.json")


def check_servo_local_compatibility_corpus() -> None:
    validator = ROOT / "tools" / "validate_servo_local_compatibility_corpus.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "Servo local compatibility corpus validation failed")
    server = ROOT / "tools" / "serve_servo_local_compatibility_corpus.py"
    server_result = subprocess.run(
        [sys.executable, "-B", str(server), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if server_result.returncode != 0:
        detail = "\n".join(
            line
            for line in [server_result.stdout.strip(), server_result.stderr.strip()]
            if line
        )
        fail(detail or "Servo local compatibility route self-test failed")
    try:
        route_summary = json.loads(server_result.stdout)
    except json.JSONDecodeError as error:
        fail(f"Servo local compatibility route self-test emitted invalid JSON: {error}")
    if route_summary.get("artifact_id") != "ADR9.EV013.NOCLAIM_ROUTE_SELF_TEST.2026_07":
        fail("Servo local compatibility route self-test emitted the wrong artifact_id")
    for key in [
        "server_started",
        "server_shutdown",
    ]:
        if route_summary.get(key) is not True:
            fail(f"Servo local compatibility route self-test must set {key}=true")
    for key in [
        "external_network_used",
        "dns_os_modified",
        "https_used",
        "tls_certificate_provided",
        "browser_launched",
        "compatibility_result_generated",
        "wpt_result_generated",
        "test262_result_generated",
    ]:
        if route_summary.get(key) is not False:
            fail(f"Servo local compatibility route self-test must set {key}=false")
    routes_checked = route_summary.get("routes_checked")
    if not isinstance(routes_checked, list) or len(routes_checked) != 10:
        fail("Servo local compatibility route self-test must check 10 fixture routes")
    harness_validator = ROOT / "tools" / "validate_servo_local_compatibility_https_harness.py"
    harness_result = subprocess.run(
        [sys.executable, "-B", str(harness_validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if harness_result.returncode != 0:
        detail = "\n".join(
            line
            for line in [harness_result.stdout.strip(), harness_result.stderr.strip()]
            if line
        )
        fail(detail or "Servo local compatibility HTTPS harness validation failed")

    manifest_path = (
        "docs/blueprint-v1/machine/servo-local-compatibility-corpora/"
        "no-claim-tiny-adr0009.corpus.json"
    )
    schema_path = "docs/blueprint-v1/machine/servo-local-compatibility-corpus.schema.json"
    https_schema_path = "docs/blueprint-v1/machine/servo-local-compatibility-https-harness.schema.json"
    https_plan_path = (
        "docs/blueprint-v1/machine/servo-local-compatibility-harnesses/"
        "no-claim-https-host-alias.plan.json"
    )
    validator_path = "tools/validate_servo_local_compatibility_corpus.py"
    https_validator_path = "tools/validate_servo_local_compatibility_https_harness.py"
    server_path = "tools/serve_servo_local_compatibility_corpus.py"
    fixture_root_path = "benchmarks/compatibility/adr0009/no-claim-tiny"
    required_paths = [
        schema_path,
        https_schema_path,
        manifest_path,
        https_plan_path,
        fixture_root_path,
        validator_path,
        https_validator_path,
        server_path,
    ]

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items") if isinstance(readiness, dict) else []
    pb002 = next((item for item in items if isinstance(item, dict) and item.get("id") == "PB-002"), None)
    if not isinstance(pb002, dict):
        fail("pre-build-readiness.json is missing PB-002")
    evidence = pb002.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-002 evidence must be an array")
    missing_pb002 = [path for path in required_paths if path not in evidence]
    if missing_pb002:
        fail("PB-002 evidence is missing local compatibility corpus paths: " + ", ".join(missing_pb002))
    required = pb002.get("evidence_required")
    if not isinstance(required, list) or not any(
        "local compatibility corpus HTTPS execution and browser-run evidence" in str(item)
        for item in required
    ):
        fail("PB-002 evidence_required must keep local compatibility browser runs missing")

    adr = load_json(MACHINE / "adr-0009-evidence.json")
    adr_items = adr.get("items") if isinstance(adr, dict) else []
    adr013 = next(
        (
            item
            for item in adr_items
            if isinstance(item, dict) and item.get("id") == "ADR9-EV-013"
        ),
        None,
    )
    if not isinstance(adr013, dict):
        fail("adr-0009-evidence.json is missing ADR9-EV-013")
    if adr013.get("status") != "partial":
        fail("ADR9-EV-013 must remain partial until browser-run evidence exists")
    existing = adr013.get("existing_evidence")
    if not isinstance(existing, list):
        fail("ADR9-EV-013 existing_evidence must be an array")
    missing_adr = [
        path
        for path in [
            schema_path,
            https_schema_path,
            manifest_path,
            https_plan_path,
            fixture_root_path,
            validator_path,
            https_validator_path,
            server_path,
        ]
        if path not in existing
    ]
    if missing_adr:
        fail("ADR9-EV-013 existing_evidence is missing local corpus paths: " + ", ".join(missing_adr))
    missing_outputs = adr013.get("missing_outputs")
    if not isinstance(missing_outputs, list) or not any(
        "host-alias browser runs" in str(item) for item in missing_outputs
    ):
        fail("ADR9-EV-013 missing_outputs must keep HTTPS/host-alias browser runs missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes") if isinstance(crosswalk, dict) else []
    source_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-source-strategy-adr-0009"
        ),
        None,
    )
    if not isinstance(source_lane, dict):
        fail("research-readiness-crosswalk.json is missing source-strategy lane")
    evidence_start = source_lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("source-strategy lane evidence_start must be an array")
    missing_lane = [path for path in required_paths if path not in evidence_start]
    if missing_lane:
        fail("source-strategy lane is missing local corpus paths: " + ", ".join(missing_lane))

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks") if isinstance(task_queue, dict) else []
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000001"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000001")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000001 allowed_paths must be an array")
    if (
        schema_path not in allowed_paths
        or https_schema_path not in allowed_paths
        or https_plan_path not in allowed_paths
        or fixture_root_path not in allowed_paths
        or validator_path not in allowed_paths
        or https_validator_path not in allowed_paths
        or server_path not in allowed_paths
    ):
        fail("TASK-000001 allowed_paths must include local compatibility schema, HTTPS harness plan, fixtures, validators, and route self-test")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "local compatibility corpus HTTPS/browser execution" in str(item) for item in acceptance
    ):
        fail("TASK-000001 acceptance criteria must mention local compatibility HTTPS/browser execution")

    docs_to_check = {
        DOCS / "README.md": "no-claim [local compatibility corpus manifest]",
        RESEARCH / "README.md": "checked no-claim local corpus manifest, fixtures, HTTP route self-test, and HTTPS host-alias harness plan",
        RESEARCH / "servo-local-compatibility-corpus-2026-07.md": "Checked No-Claim HTTPS Harness Plan",
        DOCS / "repository-map.md": "ADR9-EV-013` local compatibility corpus",
        DOCS / "project-buildout" / "15-adr-0009-evidence-traceability-matrix.md": "checked [HTTPS host-alias harness plan]",
        DOCS / "project-buildout" / "14-adr-0009-source-strategy-decision-packet.md": "checked [local compatibility corpus manifest]",
    }
    for path, phrase in docs_to_check.items():
        if phrase not in path.read_text(encoding="utf-8"):
            fail(f"{relative(path)} is missing local compatibility corpus coverage: {phrase}")


def check_agent_execution_controls() -> None:
    base = DOCS / "agent-execution" / "machine"
    matrix = load_json(base / "agent-capability-matrix.json")
    run_schema = load_json(base / "agent-run-manifest.schema.json")
    task_schema = load_json(base / "execution-task.schema.json")
    task_approval_schema = load_json(base / "task-approval-template.schema.json")
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
    for schema, name in (
        (run_schema, "agent run"),
        (task_schema, "execution task"),
        (task_approval_schema, "task approval template"),
        (evidence_schema, "evidence bundle"),
    ):
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


def check_task_approval_templates() -> None:
    validator = ROOT / "tools" / "validate_task_approval_templates.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        fail(detail or "task approval template validation failed")


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
    performance_slo_metadata = {
        "SLO-004": ("startup", ["REQ-PERF-001"]),
        "SLO-005": ("interaction", ["REQ-PERF-001"]),
        "SLO-006": ("frame_pacing", ["REQ-PERF-001"]),
        "SLO-007": ("memory_lifecycle", ["REQ-PERF-002", "REQ-PERF-003"]),
        "SLO-008": ("energy", ["REQ-PERF-001", "REQ-PERF-003"]),
    }
    for slo_id, (lane, requirements) in performance_slo_metadata.items():
        item = next(slo for slo in slo_items if slo.get("id") == slo_id)
        if item.get("target") is not None:
            fail(f"{slo_id} target must remain unset until reviewed benchmark evidence exists")
        if item.get("evidence_lane") != lane:
            fail(f"{slo_id} evidence lane must remain {lane}")
        if item.get("requirements") != requirements:
            fail(f"{slo_id} requirement mapping must remain {requirements}")
        if item.get("minimum_evidence_level") != "1":
            fail(f"{slo_id} minimum evidence level must remain Level 1")
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


def check_benchmark_manifests() -> None:
    validator = ROOT / "tools" / "validate_benchmark_manifests.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark manifest validation failed")


def check_benchmark_hardware() -> None:
    validator = ROOT / "tools" / "validate_benchmark_hardware.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark hardware validation failed")


def check_benchmark_os_controls() -> None:
    validator = ROOT / "tools" / "validate_benchmark_os_controls.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark OS-control validation failed")


def check_benchmark_resource_attribution() -> None:
    validator = ROOT / "tools" / "validate_benchmark_resource_attribution.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark resource-attribution validation failed")


def check_benchmark_competitor_versions() -> None:
    validator = ROOT / "tools" / "validate_benchmark_competitor_versions.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark competitor-version validation failed")


def check_benchmark_competitor_local_installs() -> None:
    validator = ROOT / "tools" / "validate_benchmark_competitor_local_installs.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark competitor local-install validation failed")


def check_benchmark_browser_pin_capture() -> None:
    validator = ROOT / "tools" / "validate_benchmark_browser_pin_capture.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark browser-pin capture validation failed")


def check_benchmark_browser_pin_capture_self_test() -> None:
    runner = ROOT / "tools" / "capture_benchmark_browser_pins.py"
    result = subprocess.run(
        [sys.executable, "-B", str(runner), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark browser-pin capture self-test failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"benchmark browser-pin capture self-test emitted invalid JSON: {error}")
    if payload.get("artifact_id") != "NOCLAIM.BROWSER_PIN_CAPTURE.2026_07":
        fail("benchmark browser-pin capture self-test emitted the wrong artifact_id")
    claim_status = payload.get("claim_status")
    if not isinstance(claim_status, str):
        fail("benchmark browser-pin capture self-test is missing claim_status")
    for phrase in ["no browser was launched", "no browser-reported version", "no performance claim"]:
        if phrase not in claim_status:
            fail(f"benchmark browser-pin capture self-test claim_status must mention: {phrase}")
    targets = payload.get("target_summaries")
    if not isinstance(targets, list) or not targets:
        fail("benchmark browser-pin capture self-test emitted no target summaries")
    first = targets[0]
    if not isinstance(first, dict):
        fail("benchmark browser-pin capture self-test target summary must be an object")
    if first.get("browser_launched") is not False:
        fail("benchmark browser-pin capture self-test must not launch a browser")
    check = first.get("prohibited_path_check")
    if not isinstance(check, dict) or check.get("prohibited_access_detected") is not False:
        fail("benchmark browser-pin capture self-test must report no prohibited access")


def check_benchmark_browser_pin_diagnostics() -> None:
    validator = ROOT / "tools" / "validate_benchmark_browser_pin_diagnostics.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark browser-pin diagnostic validation failed")


def check_benchmark_corpus() -> None:
    validator = ROOT / "tools" / "validate_benchmark_corpus.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark corpus validation failed")
    required_paths = [
        "docs/research/benchmark-corpus-expansion-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-corpora/no-claim-smoke.corpus.json",
        "benchmarks/corpus/no-claim-smoke/accessibility-form/index.html",
        "benchmarks/corpus/no-claim-smoke/international-text/index.html",
        "benchmarks/corpus/no-claim-smoke/hostile-markup/index.html",
        "benchmarks/corpus/no-claim-smoke/media-document/index.html",
        "benchmarks/corpus/no-claim-smoke/service-worker-contract/index.html",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing expanded corpus paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "reviewed representative offline corpus" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep reviewed representative corpus missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if (
        not isinstance(lane_evidence, list)
        or "docs/research/benchmark-corpus-expansion-2026-07.md" not in lane_evidence
    ):
        fail("benchmark lane evidence_start is missing benchmark corpus expansion")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "expanded generated no-claim corpus" in str(item) for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry expanded no-claim corpus")

    doc_requirements = {
        RESEARCH / "benchmark-corpus-expansion-2026-07.md": [
            "seven generated local fixtures",
            "service-worker fixture checks only",
            "reviewed representative corpus",
        ],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "seven generated local fixtures",
            "reviewed representative offline corpus",
        ],
        DOCS / "repository-map.md": ["service-worker-contract", "no reviewed representative corpus"],
        DOCS / "benchmark-lab" / "02-corpus-servers-and-network-control.md": [
            "service-worker-contract",
            "reviewed representative corpus",
        ],
        DOCS / "performance" / "05-benchmarks-statistics-and-regression-governance.md": [
            "service-worker-contract",
            "not reviewed representative corpus evidence",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing expanded benchmark corpus coverage: "
                + ", ".join(missing)
            )


def check_benchmark_network_profile() -> None:
    validator = ROOT / "tools" / "validate_benchmark_network_profile.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark network profile validation failed")
    required_paths = [
        "docs/research/benchmark-server-lifecycle-self-test-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json",
        "tools/validate_benchmark_network_profile.py",
        "tools/serve_benchmark_profile.py",
        "tools/run_benchmark_server_profile.py",
        "tools/run_benchmark_smoke.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing network-profile paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "browser-run server evidence" in str(item) for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep browser-run server proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in [
        "docs/research/benchmark-server-lifecycle-self-test-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-network-profiles/no-claim-local-static.profile.json",
        "tools/run_benchmark_server_profile.py",
    ]:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "browser-run server evidence" in str(item) for item in next_proof
    ):
        fail("benchmark lane next_proof must require browser-run server evidence")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    if "tools/run_benchmark_server_profile.py" not in allowed_paths:
        fail("TASK-000005 allowed_paths is missing tools/run_benchmark_server_profile.py")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "runner-managed server lifecycle self-test" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry server lifecycle self-test")

    doc_requirements = {
        DOCS / "repository-map.md": ["run_benchmark_server_profile.py"],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "runner-managed server lifecycle self-test",
            "browser-run server evidence",
        ],
        DOCS / "benchmark-lab" / "02-corpus-servers-and-network-control.md": [
            "runner-managed server lifecycle self-test",
            "server-startup",
            "server-shutdown",
        ],
        DOCS / "performance" / "05-benchmarks-statistics-and-regression-governance.md": [
            "runner-managed server lifecycle self-test",
        ],
        DOCS / "benchmark-lab" / "README.md": [
            "Benchmark server lifecycle self-test",
        ],
        DOCS / "performance" / "README.md": [
            "Benchmark server lifecycle self-test",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "runner-managed server lifecycle self-test",
            "browser-run server evidence",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "runner-managed server lifecycle self-test",
        ],
        BLUEPRINT / "22-research-program.md": [
            "run_benchmark_server_profile.py --self-test",
            "browser-run server evidence",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing benchmark network-profile coverage: "
                + ", ".join(missing)
            )


def check_benchmark_tab_scenarios() -> None:
    validator = ROOT / "tools" / "validate_benchmark_tab_scenarios.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark tab scenario validation failed")

    required_paths = [
        "docs/research/benchmark-30-tab-scenario-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-tab-scenario.schema.json",
        "docs/blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json",
        "tools/validate_benchmark_tab_scenarios.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail("PB-013 evidence is missing tab-scenario paths: " + ", ".join(missing_evidence))
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "runner-generated 30-tab mixed and all-live raw artifacts" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep runner-generated 30-tab proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in [
        "docs/research/benchmark-30-tab-scenario-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json",
    ]:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "runner-generated 30-tab results" in str(item) for item in next_proof
    ):
        fail("benchmark lane next_proof must require runner-generated 30-tab results")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-tab-scenarios/",
        "docs/research/benchmark-30-tab-scenario-contract-2026-07.md",
        "tools/validate_benchmark_tab_scenarios.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000005 allowed_paths is missing {required}")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "checked no-claim 30-tab mixed and all-live scenario manifests" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry checked 30-tab scenarios")

    doc_requirements = {
        DOCS / "README.md": ["Benchmark 30-tab scenario contract"],
        RESEARCH / "README.md": [
            "Benchmark 30-tab scenario contract",
            "no-claim 30-tab scenarios",
            "runner-generated 30-tab results",
        ],
        DOCS / "repository-map.md": [
            "validate_benchmark_tab_scenarios.py",
            "benchmark-tab-scenarios/no-claim-30-tab-smoke.scenarios.json",
        ],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "Benchmark 30-Tab Scenario Contract",
            "PB13-EV-008",
            "runner-generated 30-tab output",
        ],
        RESEARCH / "chrome-class-performance-runbook-2026-07.md": [
            "runner-generated 30-tab mixed/all-live raw artifacts",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "Benchmark 30-tab scenario contract",
            "checked no-claim 30-tab mixed/all-live scenario manifest",
            "runner-generated 30-tab raw artifacts",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "Benchmark 30-tab scenario contract",
            "30-tab denominator shape",
        ],
        BLUEPRINT / "09-performance-memory.md": [
            "no-claim 30-tab smoke scenario manifest",
            "not a memory, energy, Chrome-class, or performance result",
        ],
        DOCS / "benchmark-lab" / "05-memory-process-topology-and-thirty-tabs.md": [
            "Current No-Claim Scenario Record",
            "not the final Tier M workload",
        ],
        DOCS / "benchmark-lab" / "README.md": ["Benchmark 30-tab scenario contract"],
        DOCS / "performance" / "README.md": ["Benchmark 30-tab scenario contract"],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing benchmark tab-scenario coverage: "
                + ", ".join(missing)
            )


def check_benchmark_artifact_packages() -> None:
    validator = ROOT / "tools" / "validate_benchmark_artifact_packages.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark artifact package validation failed")

    required_paths = [
        "docs/research/benchmark-trace-artifact-package-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-artifact-package.schema.json",
        "docs/blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json",
        "tools/validate_benchmark_artifact_packages.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing artifact-package paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "runner-generated trace and artifact package root" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep runner-generated trace package proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in [
        "docs/research/benchmark-trace-artifact-package-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-artifact-packages/no-claim-trace-package.plan.json",
    ]:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "runner-generated trace package" in str(item) for item in next_proof
    ):
        fail("benchmark lane next_proof must require runner-generated trace package proof")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-artifact-packages/",
        "docs/research/benchmark-trace-artifact-package-contract-2026-07.md",
        "tools/validate_benchmark_artifact_packages.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000005 allowed_paths is missing {required}")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "checked no-claim trace and artifact package contract" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry checked artifact-package contract")

    doc_requirements = {
        DOCS / "README.md": ["Benchmark trace/artifact package contract"],
        RESEARCH / "README.md": [
            "Benchmark trace/artifact package contract",
            "no-claim trace/artifact package",
            "runner-generated trace package",
        ],
        DOCS / "repository-map.md": [
            "validate_benchmark_artifact_packages.py",
            "benchmark-artifact-packages/no-claim-trace-package.plan.json",
        ],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "Benchmark Trace/Artifact Package Contract",
            "PB13-EV-007",
            "runner-generated trace and artifact package root",
        ],
        RESEARCH / "chrome-class-performance-runbook-2026-07.md": [
            "runner-generated trace package with ETW or equivalent traces",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "Benchmark trace/artifact package contract",
            "checked no-claim trace/artifact package contract",
            "runner-generated trace package",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "Benchmark trace/artifact package contract",
            "trace/artifact retention and redaction contract",
        ],
        BLUEPRINT / "09-performance-memory.md": [
            "no-claim trace and artifact package contract",
            "not an ETW, Perfetto, memory, energy, Chrome-class, or performance result",
        ],
        DOCS / "benchmark-lab" / "07-statistics-artifacts-regressions-and-claims.md": [
            "Current No-Claim Artifact Package Contract",
            "not a captured trace bundle",
        ],
        DOCS / "benchmark-lab" / "README.md": [
            "Benchmark trace/artifact package contract"
        ],
        DOCS / "performance" / "05-benchmarks-statistics-and-regression-governance.md": [
            "Versioned trace/artifact package contracts"
        ],
        DOCS / "performance" / "README.md": [
            "Benchmark trace/artifact package contract"
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing benchmark artifact-package coverage: "
                + ", ".join(missing)
            )


def check_benchmark_launch_runners() -> None:
    validator = ROOT / "tools" / "validate_benchmark_launch_runners.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark launch runner validation failed")

    required_paths = [
        "docs/research/benchmark-browser-launch-runner-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-launch-runner.schema.json",
        "docs/blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json",
        "tools/run_benchmark_browser_launch.py",
        "tools/validate_benchmark_launch_runners.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing launch-runner paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "implemented browser benchmark launch runner" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep implemented browser launch runner proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in [
        "docs/research/benchmark-browser-launch-runner-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-launch-runners/no-claim-browser-launch.plan.json",
        "tools/run_benchmark_browser_launch.py",
    ]:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "implemented browser launch runner" in str(item) for item in next_proof
    ):
        fail("benchmark lane next_proof must require implemented browser launch runner proof")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-launch-runners/",
        "docs/research/benchmark-browser-launch-runner-contract-2026-07.md",
        "tools/run_benchmark_browser_launch.py",
        "tools/validate_benchmark_launch_runners.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000005 allowed_paths is missing {required}")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "checked no-claim browser launch-runner contract" in str(item)
        and "checked no-browser browser launch-runner self-test" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry checked launch-runner contract and self-test")

    doc_requirements = {
        DOCS / "README.md": ["Benchmark browser launch-runner contract"],
        RESEARCH / "README.md": [
            "Benchmark browser launch-runner contract",
            "no-claim browser launch-runner contract",
            "checked no-browser browser launch-runner self-test",
            "implemented browser launch runner",
        ],
        DOCS / "repository-map.md": [
            "run_benchmark_browser_launch.py",
            "validate_benchmark_launch_runners.py",
            "benchmark-launch-runners/no-claim-browser-launch.plan.json",
        ],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "Benchmark Browser Launch Runner Contract",
            "PB13-EV-005",
            "checked no-browser browser launch-runner self-test",
            "implemented browser benchmark launch runner",
        ],
        RESEARCH / "chrome-class-performance-runbook-2026-07.md": [
            "checked browser launch-runner contract",
            "checked no-browser browser launch-runner self-test",
            "implemented browser launch runner",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "Benchmark browser launch-runner contract",
            "checked no-claim browser launch-runner contract",
            "checked no-browser browser launch-runner self-test",
            "implemented browser benchmark launch runner",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "Benchmark browser launch-runner contract",
            "checked no-browser browser launch-runner self-test",
            "launch-runner timeout, cache/profile, failure, and artifact contract",
        ],
        BLUEPRINT / "09-performance-memory.md": [
            "no-claim browser launch-runner contract",
            "no-browser browser launch-runner self-test",
            "not a browser launch, trace, raw-sample, memory, energy, Chrome-class, or performance result",
        ],
        DOCS / "benchmark-lab" / "02-corpus-servers-and-network-control.md": [
            "Current No-Claim Launch Runner Contract",
            "checked no-browser browser launch-runner self-test",
            "not a browser-run launch implementation",
        ],
        DOCS / "benchmark-lab" / "README.md": [
            "Benchmark browser launch-runner contract",
            "Benchmark browser launch-runner self-test",
        ],
        DOCS / "performance" / "05-benchmarks-statistics-and-regression-governance.md": [
            "Versioned browser launch-runner contracts",
            "checked no-browser launch-runner self-test",
        ],
        DOCS / "performance" / "README.md": [
            "Benchmark browser launch-runner contract",
            "Benchmark browser launch-runner self-test",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing benchmark launch-runner coverage: "
                + ", ".join(missing)
            )


def check_benchmark_claim_bundles() -> None:
    validator = ROOT / "tools" / "validate_benchmark_claim_bundles.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark claim-bundle validation failed")

    required_paths = [
        "docs/blueprint-v1/machine/benchmark-claim-bundle.schema.json",
        "docs/blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json",
        "tools/validate_benchmark_claim_bundles.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing claim-bundle paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "owner-reviewed claim bundle" in str(item)
        and "checked no-claim claim-bundle template" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep owner-reviewed claim-bundle proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-claim-bundles/no-claim-public-claim-template.json",
        "tools/validate_benchmark_claim_bundles.py",
    ]:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "claim bundles beyond the checked no-claim claim-bundle template" in str(item)
        for item in next_proof
    ):
        fail("benchmark lane next_proof must require owner-reviewed claim bundles")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-claim-bundles/",
        "docs/blueprint-v1/machine/benchmark-claim-bundle.schema.json",
        "tools/validate_benchmark_claim_bundles.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000005 allowed_paths is missing {required}")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "checked no-claim claim-bundle template" in str(item)
        and "owner-reviewed public-claim evidence" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry checked claim-bundle template")


def check_benchmark_readiness_review() -> None:
    validator = ROOT / "tools" / "validate_benchmark_readiness_review.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark readiness-review validation failed")


def check_benchmark_statistics_analysis() -> None:
    validator = ROOT / "tools" / "validate_benchmark_statistics_analysis.py"
    result = subprocess.run(
        [sys.executable, "-B", str(validator)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark statistics-analysis validation failed")

    required_paths = [
        "docs/research/benchmark-statistics-analysis-contract-2026-07.md",
        "docs/blueprint-v1/machine/benchmark-statistics-analysis.schema.json",
        "docs/blueprint-v1/machine/benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json",
        "tools/validate_benchmark_statistics_analysis.py",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb013 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-013"),
        None,
    )
    if not isinstance(pb013, dict):
        fail("pre-build-readiness.json is missing PB-013")
    evidence = pb013.get("evidence")
    if not isinstance(evidence, list):
        fail("PB-013 evidence must be an array")
    missing_evidence = [path for path in required_paths if path not in evidence]
    if missing_evidence:
        fail(
            "PB-013 evidence is missing statistics-analysis paths: "
            + ", ".join(missing_evidence)
        )
    evidence_required = pb013.get("evidence_required")
    if not isinstance(evidence_required, list) or not any(
        "checked no-claim statistics-analysis contract" in str(item)
        and "owner-reviewed statistics-analysis plan reference" in str(item)
        and "owner-reviewed statistics analysis" in str(item)
        for item in evidence_required
    ):
        fail("PB-013 evidence_required must keep owner-reviewed statistics-analysis plan and analysis proof missing")

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    benchmark_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-benchmark-extreme-performance-lab"
        ),
        None,
    )
    if not isinstance(benchmark_lane, dict):
        fail("research-readiness-crosswalk.json is missing benchmark lane")
    lane_evidence = benchmark_lane.get("evidence_start")
    if not isinstance(lane_evidence, list):
        fail("benchmark lane evidence_start must be an array")
    for required in required_paths:
        if required not in lane_evidence:
            fail(f"benchmark lane evidence_start is missing {required}")
    next_proof = benchmark_lane.get("next_proof")
    if not isinstance(next_proof, list) or not any(
        "owner-reviewed statistics-analysis plan reference" in str(item)
        and
        "owner-reviewed statistics analysis beyond the checked no-claim statistics-analysis contract"
        in str(item)
        for item in next_proof
    ):
        fail("benchmark lane next_proof must require owner-reviewed statistics-analysis plan and analysis")

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task = next(
        (
            item
            for item in tasks
            if isinstance(item, dict) and item.get("id") == "TASK-000005"
        ),
        None,
    )
    if not isinstance(task, dict):
        fail("build-readiness-task-queue.json is missing TASK-000005")
    allowed_paths = task.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000005 allowed_paths must be an array")
    for required in [
        "docs/blueprint-v1/machine/benchmark-statistics-analyses/",
        "docs/blueprint-v1/machine/benchmark-statistics-analysis.schema.json",
        "docs/research/benchmark-statistics-analysis-contract-2026-07.md",
        "tools/validate_benchmark_statistics_analysis.py",
    ]:
        if required not in allowed_paths:
            fail(f"TASK-000005 allowed_paths is missing {required}")
    acceptance = task.get("acceptance_criteria")
    if not isinstance(acceptance, list) or not any(
        "checked no-claim statistics-analysis contract" in str(item)
        and "owner-reviewed statistics-analysis plan reference" in str(item)
        and "owner-reviewed analysis evidence" in str(item)
        for item in acceptance
    ):
        fail("TASK-000005 acceptance criteria must carry checked statistics-analysis contract and plan scope")

    doc_requirements = {
        DOCS / "README.md": ["Benchmark statistics analysis contract"],
        RESEARCH / "README.md": [
            "Benchmark statistics analysis contract",
            "checked no-claim statistics-analysis contract",
            "owner-reviewed statistics analysis beyond the checked no-claim statistics-analysis contract",
        ],
        DOCS / "repository-map.md": [
            "validate_benchmark_statistics_analysis.py",
            "benchmark-statistics-analyses/no-claim-statistics-analysis-plan.json",
        ],
        RESEARCH / "performance-benchmark-readiness-packet-2026-07.md": [
            "Benchmark Statistics Analysis Contract",
            "PB13-EV-006",
            "checked no-claim statistics-analysis contract",
        ],
        RESEARCH / "chrome-class-performance-runbook-2026-07.md": [
            "checked no-claim statistics-analysis contract",
            "owner-reviewed statistics analysis",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "Benchmark statistics analysis contract",
            "checked no-claim statistics-analysis contract",
            "owner-reviewed statistics analysis",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "Benchmark statistics analysis contract",
            "statistics-analysis sample design, uncertainty, denominator, and rejection contract",
            "validate_benchmark_statistics_analysis.py",
        ],
        BLUEPRINT / "09-performance-memory.md": [
            "checked no-claim statistics-analysis contract",
            "no confidence interval from measured browser data",
        ],
        DOCS / "benchmark-lab" / "07-statistics-artifacts-regressions-and-claims.md": [
            "Current No-Claim Statistics-Analysis Contract",
            "validate_benchmark_statistics_analysis.py",
        ],
        DOCS / "benchmark-lab" / "README.md": [
            "Benchmark statistics analysis contract",
        ],
        DOCS / "performance" / "05-benchmarks-statistics-and-regression-governance.md": [
            "Versioned statistics-analysis contracts",
            "validate_benchmark_statistics_analysis.py",
        ],
        DOCS / "performance" / "README.md": [
            "Benchmark statistics analysis contract",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing benchmark statistics-analysis coverage: "
                + ", ".join(missing)
            )


def check_benchmark_browser_launch_runner_self_test() -> None:
    runner = ROOT / "tools" / "run_benchmark_browser_launch.py"
    result = subprocess.run(
        [sys.executable, "-B", str(runner), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark browser launch-runner self-test failed")
    try:
        artifact = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"benchmark browser launch-runner emitted invalid JSON: {error}")
    if artifact.get("artifact_id") != "NOCLAIM.BENCHMARK_BROWSER_LAUNCH_SELF_TEST.2026_07":
        fail("benchmark browser launch-runner emitted the wrong artifact_id")
    claim_status = artifact.get("claim_status")
    if not isinstance(claim_status, str):
        fail("benchmark browser launch-runner is missing claim_status")
    for phrase in [
        "no browser run",
        "no browser launched",
        "no benchmark result",
        "no performance claim",
    ]:
        if phrase not in claim_status:
            fail(f"benchmark browser launch-runner claim_status must mention: {phrase}")
    if artifact.get("browser_launched") is not False:
        fail("benchmark browser launch-runner must state browser_launched=false")
    if artifact.get("benchmark_result_generated") is not False:
        fail("benchmark browser launch-runner must state benchmark_result_generated=false")
    if artifact.get("claim_mode") != "no-claim":
        fail("benchmark browser launch-runner must keep claim_mode=no-claim")
    if artifact.get("registry_references_checked") is not True:
        fail("benchmark browser launch-runner must check registry references")
    if artifact.get("artifact_root_behavior_checked") is not True:
        fail("benchmark browser launch-runner must check artifact-root behavior")
    required_arguments = artifact.get("required_arguments_checked")
    if not isinstance(required_arguments, list) or "--artifact-root" not in required_arguments:
        fail("benchmark browser launch-runner must check required arguments")
    forbidden_arguments = artifact.get("forbidden_arguments_checked")
    if not isinstance(forbidden_arguments, list) or "--claim" not in forbidden_arguments:
        fail("benchmark browser launch-runner must check forbidden arguments")
    files = artifact.get("artifact_files")
    if not isinstance(files, list) or len(files) != 5:
        fail("benchmark browser launch-runner must produce five artifact file records")


def check_benchmark_profile_server_self_test() -> None:
    server = ROOT / "tools" / "serve_benchmark_profile.py"
    result = subprocess.run(
        [sys.executable, "-B", str(server), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark profile server self-test failed")
    try:
        artifact = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"benchmark profile server self-test emitted invalid JSON: {error}")
    if artifact.get("artifact_id") != "NOCLAIM.NETWORK_PROFILE_SELF_TEST.2026_07":
        fail("benchmark profile server self-test emitted the wrong artifact_id")
    claim_status = artifact.get("claim_status")
    if not isinstance(claim_status, str):
        fail("benchmark profile server self-test is missing claim_status")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(f"benchmark profile server self-test claim_status must mention: {phrase}")
    routes = artifact.get("routes_checked")
    if not isinstance(routes, list) or len(routes) < 2:
        fail("benchmark profile server self-test must check at least two routes")


def check_benchmark_server_profile_runner_self_test() -> None:
    runner = ROOT / "tools" / "run_benchmark_server_profile.py"
    result = subprocess.run(
        [sys.executable, "-B", str(runner), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark server profile runner self-test failed")
    try:
        artifact = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"benchmark server profile runner emitted invalid JSON: {error}")
    if artifact.get("artifact_id") != "NOCLAIM.NETWORK_PROFILE_SERVER_RUN.2026_07":
        fail("benchmark server profile runner emitted the wrong artifact_id")
    claim_status = artifact.get("claim_status")
    if not isinstance(claim_status, str):
        fail("benchmark server profile runner is missing claim_status")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(f"benchmark server profile runner claim_status must mention: {phrase}")
    if artifact.get("server_started") is not True:
        fail("benchmark server profile runner must state server_started=true")
    if artifact.get("server_shutdown") is not True:
        fail("benchmark server profile runner must state server_shutdown=true")
    if artifact.get("browser_launched") is not False:
        fail("benchmark server profile runner must state browser_launched=false")
    if artifact.get("benchmark_result_generated") is not False:
        fail("benchmark server profile runner must state benchmark_result_generated=false")
    if artifact.get("external_network_used") is not False:
        fail("benchmark server profile runner must state external_network_used=false")
    routes = artifact.get("routes_checked")
    if not isinstance(routes, list) or len(routes) < 2:
        fail("benchmark server profile runner must check at least two routes")
    files = artifact.get("artifact_files")
    if not isinstance(files, list) or len(files) != 5:
        fail("benchmark server profile runner must produce five artifact file records")


def check_benchmark_smoke_runner_self_test() -> None:
    runner = ROOT / "tools" / "run_benchmark_smoke.py"
    result = subprocess.run(
        [sys.executable, "-B", str(runner), "--self-test"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = "\n".join(
            line for line in [result.stdout.strip(), result.stderr.strip()] if line
        )
        fail(detail or "benchmark smoke runner self-test failed")
    try:
        artifact = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"benchmark smoke runner emitted invalid JSON: {error}")
    if artifact.get("artifact_id") != "NOCLAIM.BENCHMARK_SMOKE_RUNNER.2026_07":
        fail("benchmark smoke runner emitted the wrong artifact_id")
    claim_status = artifact.get("claim_status")
    if not isinstance(claim_status, str):
        fail("benchmark smoke runner is missing claim_status")
    for phrase in ["no browser run", "no benchmark result", "no performance claim"]:
        if phrase not in claim_status:
            fail(f"benchmark smoke runner claim_status must mention: {phrase}")
    hardware_id = artifact.get("hardware_id")
    if not isinstance(hardware_id, str) or not hardware_id.startswith(
        "TURING.BENCHMARK.HARDWARE."
    ):
        fail("benchmark smoke runner is missing a benchmark hardware registry id")
    os_control_id = artifact.get("os_control_id")
    if not isinstance(os_control_id, str) or not os_control_id.startswith(
        "TURING.BENCHMARK.OS_CONTROL."
    ):
        fail("benchmark smoke runner is missing a benchmark OS-control registry id")
    resource_attribution_id = artifact.get("resource_attribution_id")
    if not isinstance(resource_attribution_id, str) or not resource_attribution_id.startswith(
        "TURING.BENCHMARK.RESOURCE_ATTRIBUTION."
    ):
        fail("benchmark smoke runner is missing a benchmark resource-attribution registry id")
    files = artifact.get("artifact_files")
    if not isinstance(files, list) or len(files) != 3:
        fail("benchmark smoke runner must produce three artifact file records")


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


def check_professional_traceability_design_routes() -> None:
    path = MACHINE / "professional-traceability.json"
    payload = load_json(path)
    items = payload.get("requirements")
    if not isinstance(items, list):
        fail("professional-traceability.json must contain requirements")

    requirements_payload = load_json(MACHINE / "requirements.json")
    requirements = requirements_payload.get("requirements")
    if not isinstance(requirements, list):
        fail("requirements.json must contain requirements")
    expected_ids = [
        item.get("id")
        for item in requirements
        if isinstance(item, dict)
    ]
    actual_ids = [
        item.get("id")
        for item in items
        if isinstance(item, dict)
    ]
    if actual_ids != expected_ids:
        fail("professional traceability requirement order differs from requirements.json")

    for item in items:
        if not isinstance(item, dict):
            fail("professional-traceability requirements must be objects")
        requirement_id = item.get("id")
        design = item.get("design")
        if not isinstance(design, list) or not design:
            fail(f"{requirement_id}: design route is missing")
        if not all(isinstance(ref, str) and ref for ref in design):
            fail(f"{requirement_id}: design routes must be non-empty strings")
        for ref in design:
            if not (ROOT / ref).is_file():
                fail(f"{requirement_id}: design route is missing: {ref}")
        for field in ("source", "tests", "reviews", "evidence"):
            if not isinstance(item.get(field), list):
                fail(f"{requirement_id}: {field} must be an array")


def check_requirement_verification_matrix() -> None:
    matrix = load_json(MACHINE / "requirement-verification-matrix.json")
    lanes = matrix.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        fail("requirement-verification-matrix.json must contain lanes")

    requirements_payload = load_json(MACHINE / "requirements.json")
    requirements = requirements_payload.get("requirements")
    if not isinstance(requirements, list):
        fail("requirements.json must contain requirements")
    expected_ids = {
        item.get("id")
        for item in requirements
        if isinstance(item, dict)
    }

    backlog = load_json(MACHINE / "backlog.json")
    work_packages = backlog.get("items")
    if not isinstance(work_packages, list):
        fail("backlog.json must contain items")
    expected_work_packages = {
        item.get("id")
        for item in work_packages
        if isinstance(item, dict)
    }

    catalog = load_json(MACHINE / "implementation-evidence-catalog.json")
    evidence_classes = catalog.get("classes")
    if not isinstance(evidence_classes, list):
        fail("implementation-evidence-catalog.json must contain classes")
    expected_evidence_classes = {
        item.get("id")
        for item in evidence_classes
        if isinstance(item, dict)
    }

    seen_ids: list[str] = []
    seen_lanes: set[str] = set()
    required_fields = (
        "work_packages",
        "source_documents",
        "evidence_classes",
        "test_layers",
        "negative_and_failure_cases",
        "required_artifacts",
    )
    for lane in lanes:
        if not isinstance(lane, dict):
            fail("requirement verification lanes must be objects")
        lane_id = lane.get("id")
        if not isinstance(lane_id, str) or not lane_id:
            fail("requirement verification lane id is missing")
        if lane_id in seen_lanes:
            fail(f"duplicate requirement verification lane: {lane_id}")
        seen_lanes.add(lane_id)
        requirement_ids = lane.get("requirement_ids")
        if not isinstance(requirement_ids, list) or not requirement_ids:
            fail(f"{lane_id}: requirement_ids must be a non-empty array")
        seen_ids.extend(requirement_ids)
        for field in required_fields:
            values = lane.get(field)
            if not isinstance(values, list) or not values:
                fail(f"{lane_id}: {field} must be a non-empty array")
            if not all(isinstance(value, str) and value for value in values):
                fail(f"{lane_id}: {field} values must be non-empty strings")
        if not isinstance(lane.get("next_proof"), str) or not lane["next_proof"]:
            fail(f"{lane_id}: next_proof must be a non-empty string")
        unknown_packages = sorted(set(lane["work_packages"]) - expected_work_packages)
        if unknown_packages:
            fail(f"{lane_id}: unknown work packages: " + ", ".join(unknown_packages))
        unknown_classes = sorted(set(lane["evidence_classes"]) - expected_evidence_classes)
        if unknown_classes:
            fail(f"{lane_id}: unknown evidence classes: " + ", ".join(unknown_classes))
        for source in lane["source_documents"]:
            if not (ROOT / source).is_file():
                fail(f"{lane_id}: source document is missing: {source}")

    if len(seen_ids) != len(set(seen_ids)):
        fail("requirement verification matrix contains duplicate requirement IDs")
    if set(seen_ids) != expected_ids:
        missing = sorted(expected_ids - set(seen_ids))
        unknown = sorted(set(seen_ids) - expected_ids)
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if unknown:
            details.append("unknown: " + ", ".join(unknown))
        fail("requirement verification matrix coverage differs from requirements.json (" + "; ".join(details) + ")")


def check_research_log_chronology() -> None:
    path = DOCS / "research-log.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    heading_re = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — .+")
    dated_headings = [
        (line_number, match.group(1), line)
        for line_number, line in enumerate(lines, start=1)
        if (match := heading_re.match(line))
    ]
    if not dated_headings:
        fail("research log contains no dated entries")

    dates = [date for _, date, _ in dated_headings]
    expected = sorted(dates, reverse=True)
    if dates != expected:
        for (line_number, previous, _), (_, current, _) in zip(
            dated_headings, dated_headings[1:]
        ):
            if previous < current:
                fail(
                    "research log dated entries must be newest-first; "
                    f"{current} appears after {previous} near line {line_number}"
                )
        fail("research log dated entries must be newest-first")

    template_lines = [
        line_number
        for line_number, line in enumerate(lines, start=1)
        if line == "## Entry template"
    ]
    if len(template_lines) != 1:
        fail("research log must contain exactly one entry template")
    template_line = template_lines[0]
    later_entry = next(
        (line_number for line_number, _, _ in dated_headings if line_number > template_line),
        None,
    )
    if later_entry is not None:
        fail(
            "research log entry template must remain after all dated entries; "
            f"found dated entry after template near line {later_entry}"
        )

    required_phrases = [
        "## 2026-07-18 — Benchmark statistics-analysis contract",
        "`PB13-EV-006` have a checked no-claim statistics-analysis contract",
        "sample design, warmup, randomization or paired order, noise study, uncertainty, effect size, outlier policy, multiple-comparison interpretation, metric-family summaries, denominator publication, and rejection rules",
        "The raw-result lane needs a checked analysis contract before a runner can turn raw samples into benchmark evidence",
        "does not analyze measured browser performance, produce confidence intervals from real samples, approve thresholds, or support benchmark-ready, public performance, Chrome-class, faster, lower-memory, lower-energy, competitor-result, production, or implementation claims",
        "## 2026-07-18 — GitHub issue handoff snapshot",
        "post-cleanup GitHub issue and stale-PR state be recorded as a checked offline handoff",
        "Captured the cleaned-up issue/PR state after closing issue #1, updating issue #3, closing stale PRs #42/#43",
        "Use GitHub issues as coordination pointers only",
        "does not approve tasks, promote readiness, prove implementation, or replace live GitHub checks",
        "## 2026-07-18 — Benchmark server lifecycle self-test",
        "`PB13-EV-004` have checked runner-managed server startup, route-check, shutdown, and artifact-hash evidence",
        "starts the local HTTP/1.1 loopback server on an ephemeral port",
        "The benchmark network lane needs server lifecycle evidence before browser-run measurement",
        "does not produce browser-run server evidence, modify OS DNS resolver state, exercise TLS, HTTP/2, HTTP/3, proxy, authentication, cache-revalidation, or network shaping",
        "## 2026-07-18 — Benchmark browser launch-runner contract",
        "`PB13-EV-005` have a checked no-claim browser launch-runner contract",
        "required and forbidden command arguments, current no-claim registry references, launch-stage coverage",
        "checked no-browser browser launch-runner self-test",
        "The browser benchmark launch path needs a checked contract before implementation",
        "does not implement a browser-run launch runner, launch a browser, capture traces, produce raw samples, prove memory or energy behavior, promote `PB-013`",
        "## 2026-07-18 — Benchmark trace/artifact package contract",
        "`PB13-EV-007` have a checked no-claim trace/artifact package contract",
        "runner-owned root policy, ETW or equivalent trace class, Perfetto-compatible trace class, tab lifecycle log class",
        "Trace and artifact package evidence needs a checked contract before a runner can persist raw benchmark artifacts",
        "does not launch a browser, capture ETW or Perfetto traces, produce raw samples, prove memory or energy behavior, promote `PB-013`",
        "## 2026-07-18 — Benchmark 30-tab scenario contract",
        "`PB13-EV-008` have checked mixed-state and all-live 30-tab scenario records",
        "exact 30-tab totals, lifecycle state-count parity, corpus case references, network-profile route coverage",
        "The 30-tab workload needs a checked denominator record before a runner can emit raw artifacts",
        "does not launch a browser, produce raw artifacts, prove memory or energy behavior, promote `PB-013`",
        "## 2026-07-18 — Direct command and line-ending handoff tightening",
        "distinguish wrapper-managed handoff validation from direct Cargo invocation while matching the expanded LF policy",
        "root README and documentation-readiness matrix that direct Cargo commands are behavior-equivalent to the wrappers but inherit the caller's `CARGO_TARGET_DIR`",
        "Handoff docs must not imply direct Cargo invocation provides the same target-directory hygiene",
        "does not prove fresh-host reproduction, promote `PB-009`, or change any product-readiness or browser-capability claim",
        "## 2026-07-18 — Machine wrapper parity",
        "machine readiness records list the PowerShell validation wrappers",
        "Added `tools/bootstrap.ps1`, `tools/doctor.ps1`, and `tools/check.ps1` beside the existing POSIX wrapper paths",
        "Machine records must expose the same Windows validation entry points",
        "does not promote `PB-009`, approve `TASK-000002`, prove independent fresh-host reproduction, or change any browser capability claim",
        "## 2026-07-18 — First-entry validation handoff surfaces",
        "Start Here page, documentation index, and build-readiness operating board",
        "Added aggregate validation wrapper guidance to the first-entry handoff surfaces",
        "full direct command family back to the documentation-readiness matrix",
        "does not approve tasks, promote readiness, prove semantic documentation completeness, or change any browser capability claim",
        "## 2026-07-18 — Agent and PR Windows wrapper handoff alignment",
        "root agent instructions, PR template, prototype guide, repository map, and documentation-readiness matrix",
        "Replaced stale Windows guidance that asked maintainers to set `CARGO_TARGET_DIR` manually",
        "Agent and pull-request handoff surfaces should name the Windows wrapper directly",
        "does not change M0 gate status, product platform support, release support, or browser capability claims",
        "## 2026-07-18 — Staged diff command-list alignment",
        "direct local-check command lists include the staged diff hygiene gate",
        "Added `git diff --cached --check` beside `git diff --check`",
        "agents, contributors, pull requests, and documentation-readiness handoffs",
        "does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim",
        "## 2026-07-18 — Windows PowerShell validation wrappers",
        "first-class PowerShell wrappers",
        "set `CARGO_TARGET_DIR` under the system temporary directory when unset",
        "Windows maintainers can run `.\\tools\\bootstrap.ps1`, `.\\tools\\doctor.ps1`, and `.\\tools\\check.ps1` directly from PowerShell",
        "does not change product platform support, cross-platform preview status, readiness gates, or browser capability claims",
        "## 2026-07-18 — Markdown and workflow line-ending policy",
        "Markdown and GitHub workflow templates",
        "Added `*.md`, `*.yml`, and `*.yaml` LF rules to `.gitattributes`",
        "Markdown and GitHub YAML are covered",
        "Existing historical blobs were not renormalized in this change",
        "source-control hygiene only; it does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim",
        "## 2026-07-18 — Local aggregate diff hygiene coverage",
        "complete local `xtask check` path enforce the same diff whitespace hygiene",
        "Added `git diff --check` and `git diff --cached --check` to `xtask check`",
        "aggregate local check covers both unstaged and staged diff whitespace",
        "does not prove semantic documentation completeness, approve tasks, or promote any readiness or browser capability claim",
        "## 2026-07-18 — CI committed-diff whitespace enforcement",
        "same `git diff --check` whitespace gate that local contributor, agent, and pull-request handoff guidance requires",
        "root commits or zero `before` values use `git diff-tree --check --root -r`",
        "uploads `diff-whitespace.log` with the other validation diagnostics",
        "does not prove documentation semantic completeness, promote build readiness, approve tasks, or change any browser capability claim",
        "## 2026-07-18 — Aggregate xtask ADR evidence coverage",
        "aggregate `xtask check` path run the same ADR-0009 evidence validator",
        "python3 -B tools/validate_adr_0009_evidence.py",
        "repository validation workflow with an ADR-0009 evidence step and uploaded diagnostic log",
        "This aligns `tools/check.sh`, `xtask check`, contributor guidance, agent guidance, CI validation, and GitHub handoff guidance",
        "does not resolve ADR-0009, unblock `PB-002`",
        "## 2026-07-18 — GitHub handoff template validation refresh",
        "current validation family, core registry review, and proposed task identifiers",
        "pull request template with proposed task/readiness fields",
        "engineering issue template placeholder to include `TASK-*` identifiers",
        "Template fields do not approve tasks, promote readiness, or prove support status",
        "## 2026-07-18 — Agent and contributor validation command refresh",
        "root agent instructions and canonical contributor guide list the current repository checks",
        "validate_adr_0009_evidence.py",
        "git diff --check",
        "cargo run --locked -p xtask -- check",
        "`CARGO_TARGET_DIR` outside the repository",
        "validation guidance only; it does not promote readiness",
        "## 2026-07-18 — Root and Start Here registry continuity",
        "root stop/resume path and Start Here stop/resume map",
        "requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas",
        "governance control only; it does not approve tasks, promote readiness, or prove implementation status",
        "## 2026-07-18 — Blueprint and docs registry entry points",
        "Do the main documentation index and Blueprint index route maintainers to the same core program-registry map as the repository map?",
        "The Blueprint index now names the core machine companions for requirements, risks, backlog, readiness, task queue, process capabilities, workspace/toolchains, professional controls, and agent action schema",
        "not implementation proof or readiness promotion",
        "## 2026-07-18 — Core machine-registry navigation",
        "core program-registry table",
        "requirements, risks, work packages, pre-build readiness, the proposed task queue, process capabilities, workspace/toolchains, professional controls, and the agent action schema",
        "not evidence that features are implemented, tasks are approved, mitigations are complete, or production support exists",
        "## 2026-07-18 — Contained-M0 allowed-now boundary",
        "`allowed_now` is an authorization boundary, not a feature roadmap",
        "benchmark corpus and no-claim measurement tooling",
        "private-intake tabletop documentation",
        "No readiness item was promoted, no proposed `TASK-*` item was approved",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership lanes",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail("research log is missing current governance chronology: " + ", ".join(missing))


def check_repository_map_core_registries() -> None:
    path = DOCS / "repository-map.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "### Core program registries",
        "| Control area | Registry or artifact | Owning prose | Boundary |",
        "requirements.json",
        "Blueprint 21",
        "Stable `REQ-*` records only",
        "risks.json",
        "Risk tracking only; does not prove mitigation or readiness",
        "backlog.json",
        "Dependency and sequencing records only; not task execution approval",
        "pre-build-readiness.json",
        "`PB-GATE-0` contained/no-claim M0 authorization only",
        "GitHub issue handoff",
        "github-issue-handoff.json",
        "Coordination snapshot only; no task approval",
        "build-readiness-task-queue.json",
        "Proposed `TASK-*` handoffs only; no execution approval",
        "process-capabilities.json",
        "Deny-by-default role policy draft; no platform sandbox proof",
        "workspace-components.json",
        "toolchains.json",
        "M0 build foundation only; no product platform or release support claim",
        "professional-owners.json",
        "professional-traceability.json",
        "professional-phase-gates.json",
        "professional-review-rules.json",
        "professional-exceptions.json",
        "Provisional research-phase controls; missing backups keep `PB-019` blocked",
        "agent-action.schema.json",
        "Schema control only; no agent authority or provider approval",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail("repository map is missing core program-registry navigation: " + ", ".join(missing))


def check_index_machine_registry_navigation() -> None:
    docs_index = (DOCS / "README.md").read_text(encoding="utf-8")
    blueprint_index = (BLUEPRINT / "README.md").read_text(encoding="utf-8")
    policy = (DOCS / "documentation-policy.md").read_text(encoding="utf-8")
    docs_required = [
        "core machine-registry navigation",
        "core program registries](repository-map.md#core-program-registries)",
        "requirements, risks, work packages, readiness gates, proposed tasks, process capabilities, workspace/toolchains, professional controls, and agent action schemas",
    ]
    blueprint_required = [
        "repository map core program registries](../repository-map.md#core-program-registries)",
        "requirements.json",
        "risks.json",
        "backlog.json",
        "pre-build-readiness.json",
        "build-readiness-task-queue.json",
        "process-capabilities.json",
        "workspace-components.json",
        "toolchains.json",
        "professional-owners.json",
        "professional-traceability.json",
        "professional-phase-gates.json",
        "professional-review-rules.json",
        "professional-exceptions.json",
        "agent-action.schema.json",
        "adr-0009-evidence.json",
        "benchmark registries remain no-claim controls",
    ]
    policy_required = [
        "repository-map core registry coverage",
        "research-index lane and crosswalk coverage",
    ]
    for label, text, required in [
        ("docs index", docs_index, docs_required),
        ("Blueprint index", blueprint_index, blueprint_required),
        ("documentation policy", policy, policy_required),
    ]:
        missing = [phrase for phrase in required if phrase not in text]
        if missing:
            fail(f"{label} is missing machine-registry navigation: " + ", ".join(missing))


def check_research_index_lanes() -> None:
    path = RESEARCH / "README.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "## Current implementation-research lanes",
        "| Lane | Start from | Next evidence to produce | Must not claim |",
        "| Source strategy and `ADR-0009` |",
        "| Fresh-host build confidence |",
        "| Kernel, process authority, and IPC |",
        "| Sandbox probes |",
        "| Benchmark and extreme-performance lab |",
        "no-claim 30-tab scenarios",
        "runner-generated 30-tab results",
        "| Native shell and page-surface composition |",
        "| Profile, Space, session, snapshot, and migration formats |",
        "| Research package identity and updater lab |",
        "| Security incident and patch rehearsal |",
        "| Ownership and review capacity |",
        "Every lane remains subject to the machine readiness registry",
        "no-claim boundaries in the operating board",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "research index is missing implementation-lane handoff coverage: "
            + ", ".join(missing)
        )

    lane_rows = [
        line
        for line in text.splitlines()
        if line.startswith("| ") and line.count("|") >= 4
    ]
    if not any("Must not claim" in line for line in lane_rows):
        fail("research index implementation-lane table must include a Must not claim column")
    required_claim_guards = [
        "Servo adoption",
        "Broad M1 readiness",
        "Renderer security",
        "Sandbox readiness",
        "Faster",
        "UI toolkit selection",
        "Real-profile migration",
        "Production updater",
        "Production-safe browsing",
        "Broad readiness",
    ]
    missing_claim_guards = [
        phrase for phrase in required_claim_guards if phrase not in text
    ]
    if missing_claim_guards:
        fail(
            "research index implementation lanes are missing claim boundaries: "
            + ", ".join(missing_claim_guards)
        )

    required_crosswalk_phrases = [
        "## Build-readiness research crosswalk",
        "Use this crosswalk when adding or continuing research.",
        "### Source Strategy And `ADR-0009`",
        "`PB-002` and `TASK-000001`",
        "`RQ-44`, `RQ-46`, `RQ-47`, `RQ-15`, `RQ-16`, `RQ-25`, and `RQ-31`",
        "### Fresh-Host Build Confidence",
        "`PB-009`, `PB-020`, and `TASK-000002`",
        "`RQ-46`, `RQ-47`, and `RQ-31`",
        "### Kernel, Process Authority, And IPC",
        "`PB-011` and `TASK-000003`",
        "`RQ-02`, `RQ-13`, `RQ-20`, `RQ-22`, and `RQ-36`",
        "### Sandbox Probes",
        "`PB-012` and `TASK-000004`",
        "`RQ-20`, `RQ-38`, and `RQ-31`",
        "### Benchmark And Extreme-Performance Lab",
        "`PB-013` and `TASK-000005`",
        "`RQ-16`, `RQ-23`, `RQ-34`, `RQ-35`, and `RQ-37`",
        "### Native Shell And Page-Surface Composition",
        "`PB-003`, `PB-004`, `PB-005`, `PB-014`, `PB-015`, and `TASK-000006`",
        "`RQ-04`, `RQ-05`, `RQ-29`, `RQ-30`, `RQ-40`, `RQ-55`, `RQ-56`, and `RQ-57`",
        "### Profile, Space, Session, Snapshot, And Migration Formats",
        "`PB-016` and `TASK-000007`",
        "`RQ-14`, `RQ-27`, `RQ-49`, `RQ-50`, `RQ-53`, and `RQ-54`",
        "### Research Package Identity And Updater Lab",
        "`PB-017` and `TASK-000009`",
        "`RQ-31`, `RQ-63`, `RQ-64`, and `RQ-66`",
        "### Security Incident And Patch Rehearsal",
        "`PB-018` and `TASK-000010`",
        "`RQ-31`, `RQ-60`, and `RQ-66`",
        "### Ownership And Review Capacity",
        "`PB-019`, `PB-020`, and `TASK-000008`",
        "`RQ-25`, `RQ-31`, `RQ-45`, `RQ-47`, `RQ-48`, `RQ-60`, and `RQ-66`",
        "Claim boundary:",
    ]
    missing_crosswalk = [
        phrase for phrase in required_crosswalk_phrases if phrase not in text
    ]
    if missing_crosswalk:
        fail(
            "research index is missing build-readiness research crosswalk coverage: "
            + ", ".join(missing_crosswalk)
        )


def check_start_here_continuation() -> None:
    path = DOCS / "start-here.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "Use this stop/resume map before continuing:",
        "Status and gate truth:",
        "Documentation readiness completion audit:",
        "GitHub issue handoff:",
        "project-buildout/19-github-issue-handoff.md",
        "Core registry navigation:",
        "core program registries](repository-map.md#core-program-registries)",
        "requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas",
        "Research lane selection:",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership",
        "Task shaping:",
        "No proposed `TASK-*` item is execution approval.",
        "Source-strategy blocker:",
        "Chrome-class and extreme-performance evidence:",
        "Operating controls:",
        "## Validation Before Handoff",
        "sh tools/check.sh",
        ".\\tools\\check.ps1",
        "documentation-readiness-evidence-matrix.md#validation-commands",
        "passing check proves only the current M0 repository validation scope",
        "contained M0 and no-claim evidence work only",
        "does not approve broad M1 expansion",
        "benchmark-ready browser pins",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "start-here.md is missing current stop/resume map coverage: "
            + ", ".join(missing)
        )


def check_root_readme_continuation() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "## Current stop/resume path",
        "[`docs/start-here.md`](docs/start-here.md)",
        "Build Readiness Operating Board",
        "Documentation Readiness Completion Audit",
        "GitHub Issue Handoff",
        "GitHub issue handoff validation",
        "core program registries](docs/repository-map.md#core-program-registries)",
        "requirements, risks, work packages, readiness gates, proposed tasks, process authority, workspace/toolchains, professional controls, or agent action schemas",
        "Research Index",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership",
        "Build Readiness Task Queue",
        "`ADR-0009` source-strategy blocker",
        "Chrome-class and extreme-performance work",
        "contained M0 and no-claim evidence work only",
        "does not approve broad M1 implementation",
        "benchmark-ready browser pins",
        "docs/start-here.md",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "root README is missing current stop/resume path coverage: "
            + ", ".join(missing)
        )


def check_docs_index_continuation() -> None:
    path = DOCS / "README.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "## Current stop/resume path",
        "Use this path before expanding implementation:",
        "Confirm gate truth",
        "Documentation Readiness Completion Audit",
        "GitHub Issue Handoff",
        "research index lane map",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership",
        "proposed `TASK-*` entries are not execution approval",
        "ADR-0009 source packet",
        "Chrome-class and extreme-performance work",
        "Benchmark 30-tab scenario contract",
        "Run the aggregate validation wrapper before handoff",
        "sh tools/check.sh",
        ".\\tools\\check.ps1",
        "documentation readiness matrix](project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands)",
        "contained M0 and no-claim evidence work only",
        "does not approve broad M1 implementation",
        "benchmark-ready browser pins",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "docs/README.md is missing current stop/resume path coverage: "
            + ", ".join(missing)
        )


def check_documentation_readiness_matrix() -> None:
    path = DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "# Documentation Readiness Evidence Matrix",
        "Status: documentation-readiness control; no readiness promotion",
        "The documentation system is organized enough for contained M0 implementation tasks",
        "`PB-001` can stay `ready` only while the evidence below remains current",
        "## Objective-To-Evidence Matrix",
        "| Objective requirement | Current evidence | What the evidence proves | What remains outside the proof |",
        "Coherent first-entry documentation",
        "Stop/resume continuity",
        "Documentation readiness completion audit",
        "Build information readiness gap ledger",
        "GitHub issue and stale-PR cleanup handoff",
        "not complete enough for broad M1 expansion",
        "research lane set",
        "package/update and incident-response boundaries",
        "Consistent tracking across human and machine records",
        "Deep research tied to build blockers",
        "`TASK-000001` through `TASK-000010`",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, and ownership",
        "Source strategy ready to continue safely",
        "Chrome-competitor and extreme-performance work prepared without misleading claims",
        "30-tab denominator shape",
        "Build work can be shaped without over-authorizing agents",
        "Documentation topology and links are enforceable",
        "Build and compile gates remain reproducible for M0",
        "validate_documentation_readiness_completion_audit.py",
        "validate_build_information_readiness.py",
        "validate_github_issue_handoff.py",
        "Definition of Done",
        "documentation-readiness DoD coverage",
        "## Required Continuation Checks",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native-shell, profile/session, package/update, incident-response, or ownership",
        "fresh-host reproducibility, IPC boundary",
        "documentation-readiness or handoff criteria",
        "## Drift Triggers",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native UI/native-shell, profile/session, package/update, incident-response, ownership, or release-control blocker",
        "## Validation Commands",
        "## Claim Boundary",
        "does not approve broad M1 implementation",
        "benchmark-ready browser pins",
        "production updater",
        "incident closure",
        "Chrome-class comparison",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "documentation-readiness evidence matrix is missing required coverage: "
            + ", ".join(missing)
        )
    focused_validator_commands = [
        f"python3 -B {relative(validator).as_posix()}"
        for validator in sorted((ROOT / "tools").glob("validate_*.py"))
    ]
    missing_validator_commands = [
        command for command in focused_validator_commands if command not in text
    ]
    if missing_validator_commands:
        fail(
            "documentation-readiness evidence matrix is missing focused validation commands: "
            + ", ".join(missing_validator_commands)
        )

    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb001 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-001"),
        None,
    )
    if not isinstance(pb001, dict):
        fail("pre-build-readiness.json is missing PB-001")
    evidence = pb001.get("evidence")
    if not isinstance(evidence, list) or (
        "docs/project-buildout/18-documentation-readiness-evidence-matrix.md"
        not in evidence
    ):
        fail("PB-001 evidence must include the documentation-readiness evidence matrix")

    required_link_files = [
        ROOT / "README.md",
        DOCS / "README.md",
        DOCS / "start-here.md",
        DOCS / "documentation-policy.md",
        DOCS / "repository-map.md",
        DOCS / "project-buildout" / "README.md",
        DOCS / "project-buildout" / "11-pre-build-readiness-checklist.md",
        RESEARCH / "pre-build-readiness-gap-audit-2026-07.md",
    ]
    for link_path in required_link_files:
        if "18-documentation-readiness-evidence-matrix.md" not in link_path.read_text(
            encoding="utf-8"
        ):
            fail(
                f"{relative(link_path)} must link the documentation-readiness evidence matrix"
            )


def check_documentation_readiness_definition_of_done() -> None:
    path = BLUEPRINT / "20-definition-of-done.md"
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "## Documentation readiness or handoff change",
        "first-entry documents agree",
        "root README, Start Here, documentation index, repository map, and project-buildout handbook",
        "Documentation Readiness Evidence Matrix maps the changed claim to concrete evidence",
        "what that evidence proves, and what remains outside the proof",
        "`pre-build-readiness.json`, `TASK-000001` through `TASK-000010` in the build-readiness task queue, research-readiness crosswalk",
        "stop/resume instructions preserve gate truth",
        "current research lane set",
        "owner-only decisions, proposed-task boundaries, and unsupported-claim language",
        "primary `RQ-*`, `PB-*`, and `TASK-*` records",
        "research presence as approval",
        "source-strategy, fresh-host, IPC, sandbox, benchmark, native UI/native-shell, profile/session, package/update, incident-response, ownership, production, and release claims",
        "every new or moved document is indexed",
        "research log records material governance or evidence changes in newest-first order",
        "validators enforce any new invariant",
        "validation commands pass and the reported scope does not exceed what those checks actually prove",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        fail(
            "Definition of Done is missing documentation-readiness criteria: "
            + ", ".join(missing)
        )

    matrix = (
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md"
    ).read_text(encoding="utf-8")
    if "20-definition-of-done.md" not in matrix:
        fail("documentation-readiness matrix must link the Definition of Done")
    policy = (DOCS / "documentation-policy.md").read_text(encoding="utf-8")
    if "blueprint-v1/20-definition-of-done.md" not in policy:
        fail("documentation policy must link the Definition of Done")


def check_policy_markers() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    required_phrases = [
        "Canonical project documentation lives in `docs/`",
        "Every change must update every affected document",
        "detailed engineering book",
        "docs/repository-map.md",
        "python3 -B tools/validate_blueprint.py",
        "python3 -B tools/validate_adr_0009_evidence.py",
        "git diff --check",
        "git diff --cached --check",
        "cargo fmt --all -- --check",
        "cargo run --locked -p xtask -- check",
        "`CARGO_TARGET_DIR` outside the repository",
        ".\\tools\\check.ps1` is the Windows PowerShell wrapper",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in agents]
    if missing:
        fail("AGENTS.md is missing mandatory policy markers: " + ", ".join(missing))
    contributing = (DOCS / "contributing.md").read_text(encoding="utf-8")
    contributing_required = [
        "python3 -B tools/validate_blueprint.py",
        "python3 -B tools/validate_adr_0009_evidence.py",
        "git diff --check",
        "git diff --cached --check",
        "cargo fmt --all -- --check",
        "cargo run --locked -p xtask -- check",
        "`CARGO_TARGET_DIR` outside the repository",
        "CI also checks committed PR and push ranges with `git diff --check`",
        "local unstaged and staged diff whitespace checks",
    ]
    missing_contributing = [
        phrase for phrase in contributing_required if phrase not in contributing
    ]
    if missing_contributing:
        fail(
            "docs/contributing.md is missing current local-check markers: "
            + ", ".join(missing_contributing)
        )
    if "docs/contributing.md" not in (ROOT / "CONTRIBUTING.md").read_text(
        encoding="utf-8"
    ):
        fail("root CONTRIBUTING.md must point to docs/contributing.md")
    if "docs/security.md" not in (ROOT / "SECURITY.md").read_text(encoding="utf-8"):
        fail("root SECURITY.md must point to docs/security.md")


def check_github_handoff_templates() -> None:
    pr_template = (ROOT / ".github" / "pull_request_template.md").read_text(
        encoding="utf-8"
    )
    issue_template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "engineering.yml"
    ).read_text(encoding="utf-8")
    pr_required = [
        "Proposed task or readiness records:",
        "Core program registries reviewed:",
        "Core program registries](../docs/repository-map.md#core-program-registries)",
        "python3 -B tools/validate_blueprint.py",
        "python3 -B tools/validate_adr_0009_evidence.py",
        "git diff --check",
        "git diff --cached --check",
        "cargo fmt --all -- --check",
        "cargo run --locked -p xtask -- check",
        "`CARGO_TARGET_DIR` outside the repository",
        ".\\tools\\check.ps1` runs the aggregate check",
    ]
    issue_required = [
        "TASK-...",
        "Requirement, risk, ADR, work-package, milestone, research, or experiment IDs",
    ]
    missing_pr = [phrase for phrase in pr_required if phrase not in pr_template]
    if missing_pr:
        fail(
            "pull request template is missing current handoff guidance: "
            + ", ".join(missing_pr)
        )
    missing_issue = [
        phrase for phrase in issue_required if phrase not in issue_template
    ]
    if missing_issue:
        fail(
            "engineering issue template is missing current handoff guidance: "
            + ", ".join(missing_issue)
        )


def check_xtask_aggregate_check() -> None:
    xtask = (ROOT / "tools" / "xtask" / "src" / "main.rs").read_text(
        encoding="utf-8"
    )
    workflow = (
        ROOT / ".github" / "workflows" / "repository-validation.yml"
    ).read_text(encoding="utf-8")
    xtask_required = [
        '["-B", "tools/validate_blueprint.py"]',
        '["-B", "tools/validate_implementation_plan.py"]',
        '["-B", "tools/validate_github_issue_handoff.py"]',
        '["-B", "tools/validate_contained_m0_start_state.py"]',
        '["-B", "tools/validate_build_information_readiness.py"]',
        '["-B", "tools/validate_adr_0009_evidence.py"]',
        '["-B", "tools/validate_build_foundation.py"]',
        '["-B", "tools/validate_evidence_bundles.py"]',
        '["diff", "--check"]',
        '["diff", "--cached", "--check"]',
        "cargo run --locked -p xtask -- check",
    ]
    missing_xtask = [phrase for phrase in xtask_required if phrase not in xtask]
    if missing_xtask:
        fail(
            "xtask aggregate check is missing current validation coverage: "
            + ", ".join(missing_xtask)
        )

    workflow_required = [
        "Validate GitHub issue handoff records",
        "python3 -B tools/validate_github_issue_handoff.py > github-issue-handoff-validation.log",
        "github-issue-handoff-validation.log",
        "Validate contained M0 start state",
        "python3 -B tools/validate_contained_m0_start_state.py > contained-m0-start-state-validation.log",
        "contained-m0-start-state-validation.log",
        "Validate build information readiness",
        "python3 -B tools/validate_build_information_readiness.py > build-information-readiness-validation.log",
        "build-information-readiness-validation.log",
        "Validate ADR-0009 evidence records",
        "python3 -B tools/validate_adr_0009_evidence.py > adr-0009-evidence-validation.log",
        "adr-0009-evidence-validation.log",
        "Check committed diff whitespace",
        "git diff-tree --check --root -r \"$head\" > diff-whitespace.log",
        "git diff --check \"$base\" \"$head\" > diff-whitespace.log",
        "diff-whitespace.log",
    ]
    missing_workflow = [phrase for phrase in workflow_required if phrase not in workflow]
    if missing_workflow:
        fail(
            "repository validation workflow is missing ADR-0009 evidence coverage: "
            + ", ".join(missing_workflow)
        )

    doc_requirements = {
        ROOT / "README.md": [
            "CI for documentation, implementation-plan validation, GitHub issue handoff validation, contained M0 start-state validation, build-information readiness validation, ADR-0009 evidence validation, committed-diff whitespace, build-foundation validation",
            "`xtask check` runs documentation validation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation",
            "contained M0 start-state validation",
            "build-information readiness validation",
            "local unstaged and staged diff whitespace checks",
            "cargo run --locked -p xtask -- check",
        ],
        DOCS / "prototype.md": [
            "cargo fmt --manifest-path prototype/Cargo.toml -- --check",
            "cargo test --manifest-path prototype/Cargo.toml --all-targets",
            "documentation validation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation, evidence-bundle validation, contained M0 start-state validation, build-information readiness validation, diff whitespace checks, and `xtask check`",
        ],
        RESEARCH / "m0-build-foundation-2026-07.md": [
            "`check` runs documentation validation, implementation-plan validation, GitHub issue handoff validation, ADR-0009 evidence validation",
            "contained M0 start-state validation",
            "build-information readiness validation",
            "local unstaged and staged diff whitespace checks",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing aggregate-check guidance: "
                + ", ".join(missing)
        )


def check_line_ending_policy() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    required_rules = [
        "*.md text eol=lf",
        "*.rs text eol=lf",
        "*.toml text eol=lf",
        "*.yml text eol=lf",
        "*.yaml text eol=lf",
        "*.json text eol=lf",
        "*.html text eol=lf",
        "*.ps1 text eol=lf",
        "*.py text eol=lf",
        "*.sh text eol=lf",
    ]
    missing_rules = [rule for rule in required_rules if rule not in attributes]
    if missing_rules:
        fail(".gitattributes is missing LF policy rules: " + ", ".join(missing_rules))

    repository_map = (DOCS / "repository-map.md").read_text(encoding="utf-8")
    required_map_phrases = [
        "Markdown, GitHub YAML, Rust, and repository tooling files on LF line endings",
        "documentation diffs, workflow checks, `rustfmt`, and validation",
        "historical file renormalization is a separate source-control cleanup",
    ]
    missing_map = [
        phrase for phrase in required_map_phrases if phrase not in repository_map
    ]
    if missing_map:
        fail(
            "repository map is missing line-ending policy coverage: "
            + ", ".join(missing_map)
        )

    operating_board = (
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md"
    ).read_text(encoding="utf-8")
    required_board_phrases = [
        "Will Windows checkouts preserve source newlines?",
        "Markdown, GitHub YAML, Rust, JSON, scripts, and repository tooling files are pinned to LF",
        "historical renormalization is separate cleanup",
    ]
    missing_board = [
        phrase for phrase in required_board_phrases if phrase not in operating_board
    ]
    if missing_board:
        fail(
            "build readiness operating board is missing line-ending policy coverage: "
            + ", ".join(missing_board)
        )


def check_windows_tool_wrappers() -> None:
    wrapper_expectations = {
        ROOT / "tools" / "bootstrap.ps1": [
            "turing-bootstrap-target",
            "cargo run --locked -p xtask -- bootstrap",
        ],
        ROOT / "tools" / "doctor.ps1": [
            "turing-doctor-target",
            "cargo run --locked -p xtask -- doctor",
        ],
        ROOT / "tools" / "check.ps1": [
            "turing-check-target",
            "cargo run --locked -p xtask -- check",
        ],
    }
    for path, phrases in wrapper_expectations.items():
        if not path.is_file():
            fail(f"missing Windows wrapper: {relative(path)}")
        text = path.read_text(encoding="utf-8")
        required = [
            "CARGO_TARGET_DIR",
            "[System.IO.Path]::GetTempPath()",
            "exit $LASTEXITCODE",
            *phrases,
        ]
        missing = [phrase for phrase in required if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing wrapper contract: "
                + ", ".join(missing)
            )

    doc_requirements = {
        ROOT / "README.md": [
            "Run on Windows PowerShell:",
            ".\\tools\\bootstrap.ps1",
            ".\\tools\\doctor.ps1",
            ".\\tools\\check.ps1",
            "Direct Cargo commands are behavior-equivalent, but they inherit the caller's `CARGO_TARGET_DIR`",
        ],
        DOCS / "contributing.md": [
            ".\\tools\\check.ps1` is the Windows PowerShell wrapper",
            "Both include local unstaged and staged diff whitespace checks",
        ],
        DOCS / "repository-map.md": [
            "bootstrap.sh` and `bootstrap.ps1",
            "doctor.sh` and `doctor.ps1",
            "check.sh` and `check.ps1",
            "run `sh tools/check.sh` or `.\\tools\\check.ps1`",
        ],
        DOCS / "research" / "m0-build-foundation-2026-07.md": [
            "Windows PowerShell:",
            ".\\tools\\bootstrap.ps1",
            "The POSIX and PowerShell wrappers delegate to the same `xtask` commands",
        ],
        DOCS / "project-buildout" / "11-pre-build-readiness-checklist.md": [
            "Windows PowerShell wrappers are equivalent",
            ".\\tools\\check.ps1",
        ],
        ROOT / "AGENTS.md": [
            ".\\tools\\check.ps1` is the Windows PowerShell wrapper",
            "Both set `CARGO_TARGET_DIR` outside the repository by default",
        ],
        ROOT / ".github" / "pull_request_template.md": [
            "On Windows PowerShell, `.\\tools\\check.ps1` runs the aggregate check",
        ],
        DOCS / "prototype.md": [
            "On Windows PowerShell, use the equivalent wrapper:",
            ".\\tools\\check.ps1",
        ],
        DOCS / "project-buildout" / "18-documentation-readiness-evidence-matrix.md": [
            "On Windows PowerShell, `.\\tools\\check.ps1` runs the aggregate `xtask check` path",
            "direct Cargo commands above inherit the caller's `CARGO_TARGET_DIR`",
        ],
        DOCS / "start-here.md": [
            "## Validation Before Handoff",
            "sh tools/check.sh",
            ".\\tools\\check.ps1",
            "project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands",
        ],
        DOCS / "README.md": [
            "Run the aggregate validation wrapper before handoff",
            ".\\tools\\check.ps1",
            "project-buildout/18-documentation-readiness-evidence-matrix.md#validation-commands",
        ],
        DOCS / "project-buildout" / "13-build-readiness-operating-board.md": [
            "## Validation entry points",
            "sh tools/check.sh",
            ".\\tools\\check.ps1",
            "18-documentation-readiness-evidence-matrix.md#validation-commands",
            "A passing check proves only the contained M0 repository validation scope",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in phrases if phrase not in text]
        if missing:
            fail(
                f"{relative(path)} is missing Windows wrapper guidance: "
                + ", ".join(missing)
            )

    wrapper_paths = [
        "tools/bootstrap.sh",
        "tools/bootstrap.ps1",
        "tools/doctor.sh",
        "tools/doctor.ps1",
        "tools/check.sh",
        "tools/check.ps1",
    ]
    fresh_host_paths = [
        "docs/research/fresh-host-reproduction-inventory-2026-07.md",
        "docs/project-buildout/machine/fresh-host-reproduction.schema.json",
        "docs/project-buildout/machine/fresh-host-reproduction.json",
        "docs/project-buildout/machine/fresh-host-run-record.schema.json",
        "docs/project-buildout/machine/fresh-host-runs/no-claim-run-record-template.json",
        "docs/project-buildout/machine/fresh-host-readiness-review.schema.json",
        "docs/project-buildout/machine/fresh-host-readiness-reviews/no-claim-fresh-host-readiness-template.json",
        "tools/validate_fresh_host_reproduction.py",
        "tools/validate_fresh_host_run_records.py",
        "tools/validate_fresh_host_readiness_review.py",
    ]
    toolchain_paths = [
        "rust-toolchain.toml",
        "docs/blueprint-v1/machine/toolchains.json",
        "docs/project-buildout/machine/build-information-readiness-ledger.json",
    ]
    readiness = load_json(MACHINE / "pre-build-readiness.json")
    items = readiness.get("items")
    if not isinstance(items, list):
        fail("pre-build-readiness.json must contain an items array")
    pb009 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-009"),
        None,
    )
    if not isinstance(pb009, dict):
        fail("pre-build-readiness.json is missing PB-009")
    pb008 = next(
        (item for item in items if isinstance(item, dict) and item.get("id") == "PB-008"),
        None,
    )
    if not isinstance(pb008, dict):
        fail("pre-build-readiness.json is missing PB-008")
    pb008_evidence = pb008.get("evidence")
    if not isinstance(pb008_evidence, list):
        fail("PB-008 evidence must be an array")
    missing_pb008 = [path for path in toolchain_paths if path not in pb008_evidence]
    if missing_pb008:
        fail("PB-008 evidence is missing toolchain paths: " + ", ".join(missing_pb008))
    pb009_evidence = pb009.get("evidence")
    if not isinstance(pb009_evidence, list):
        fail("PB-009 evidence must be an array")
    missing_pb009 = [
        path for path in [*wrapper_paths, *fresh_host_paths] if path not in pb009_evidence
    ]
    if missing_pb009:
        fail("PB-009 evidence is missing wrapper or fresh-host paths: " + ", ".join(missing_pb009))

    crosswalk = load_json(MACHINE / "research-readiness-crosswalk.json")
    lanes = crosswalk.get("lanes")
    if not isinstance(lanes, list):
        fail("research-readiness-crosswalk.json must contain lanes")
    fresh_host_lane = next(
        (
            lane
            for lane in lanes
            if isinstance(lane, dict)
            and lane.get("id") == "research-lane-fresh-host-build-confidence"
        ),
        None,
    )
    if not isinstance(fresh_host_lane, dict):
        fail("research readiness crosswalk is missing fresh-host lane")
    evidence_start = fresh_host_lane.get("evidence_start")
    if not isinstance(evidence_start, list):
        fail("fresh-host lane evidence_start must be an array")
    missing_lane = [
        path for path in [*toolchain_paths, *wrapper_paths, *fresh_host_paths] if path not in evidence_start
    ]
    if missing_lane:
        fail(
            "fresh-host research lane is missing wrapper or fresh-host paths: "
            + ", ".join(missing_lane)
        )

    task_queue = load_json(MACHINE / "build-readiness-task-queue.json")
    tasks = task_queue.get("tasks")
    if not isinstance(tasks, list):
        fail("build-readiness-task-queue.json must contain tasks")
    task_000002 = next(
        (
            task
            for task in tasks
            if isinstance(task, dict) and task.get("id") == "TASK-000002"
        ),
        None,
    )
    if not isinstance(task_000002, dict):
        fail("build readiness task queue is missing TASK-000002")
    allowed_paths = task_000002.get("allowed_paths")
    if not isinstance(allowed_paths, list):
        fail("TASK-000002 allowed_paths must be an array")
    missing_task_paths = [
        path for path in [*toolchain_paths, *wrapper_paths, *fresh_host_paths] if path not in allowed_paths
    ]
    if missing_task_paths:
        fail(
            "TASK-000002 allowed_paths is missing wrapper or fresh-host paths: "
            + ", ".join(missing_task_paths)
        )


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
        check_build_readiness_task_queue()
        check_research_readiness_crosswalk()
        check_benchmark_manifests()
        check_benchmark_hardware()
        check_benchmark_os_controls()
        check_benchmark_resource_attribution()
        check_benchmark_competitor_versions()
        check_benchmark_competitor_local_installs()
        check_benchmark_browser_pin_capture()
        check_benchmark_browser_pin_capture_self_test()
        check_benchmark_browser_pin_diagnostics()
        check_benchmark_corpus()
        check_benchmark_network_profile()
        check_benchmark_tab_scenarios()
        check_benchmark_artifact_packages()
        check_benchmark_launch_runners()
        check_benchmark_claim_bundles()
        check_benchmark_readiness_review()
        check_benchmark_statistics_analysis()
        check_benchmark_browser_launch_runner_self_test()
        check_benchmark_profile_server_self_test()
        check_benchmark_server_profile_runner_self_test()
        check_benchmark_smoke_runner_self_test()
        check_professional_controls()
        check_market_opportunities()
        check_fresh_host_reproduction()
        check_fresh_host_readiness_review()
        check_ui_adapter_contract()
        check_ui_component_fixtures()
        check_framework_bakeoff()
        check_window_input_accessibility_spike()
        check_page_surface_composition()
        check_native_ui_readiness_review()
        check_profile_session_formats()
        check_profile_session_readiness_review()
        check_research_package_update_lab()
        check_research_package_update_readiness_review()
        check_incident_patch_rehearsal()
        check_incident_patch_readiness_review()
        check_backup_ownership_gap()
        check_backup_ownership_readiness_review()
        check_implementation_kickoff_review()
        check_build_readiness_dependency_graph()
        check_documentation_readiness_completion_audit()
        check_implementation_plan()
        check_github_issue_handoff()
        check_ipc_capability_boundaries()
        check_ipc_readiness_review()
        check_sandbox_probe_inventory()
        check_sandbox_contracts()
        check_sandbox_readiness_review()
        check_ui_runtime_controls()
        check_adr_0009_evidence_controls()
        check_servo_local_compatibility_corpus()
        check_agent_execution_controls()
        check_task_approval_templates()
        check_production_readiness_controls()
        markdown_count, links_checked = check_markdown()
        check_research_question_ids()
        check_professional_traceability_design_routes()
        check_requirement_verification_matrix()
        check_research_log_chronology()
        check_repository_map_core_registries()
        check_index_machine_registry_navigation()
        check_research_index_lanes()
        check_start_here_continuation()
        check_root_readme_continuation()
        check_docs_index_continuation()
        check_documentation_readiness_matrix()
        check_documentation_readiness_definition_of_done()
        check_policy_markers()
        check_github_handoff_templates()
        check_xtask_aggregate_check()
        check_line_ending_policy()
        check_windows_tool_wrappers()
        check_source_hygiene()
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print(
        "validation passed: "
        f"{markdown_count} Markdown files, {links_checked} relative links, "
        "27 detailed engineering books, 46 requirements, 40 risks, "
        "20 work packages, 120 core machine-readable registries, "
        "research-readiness crosswalk, ADR-0009 decision-review template, benchmark manifest, hardware, OS-control, resource attribution, "
        "competitor versions, competitor local installs, browser-pin capture, "
        "browser-pin capture self-test, browser-pin diagnostics, corpus, "
        "network profile fixtures, tab scenarios, artifact packages, launch runners, benchmark claim-bundle template, benchmark readiness-review template, benchmark statistics-analysis contract, launch-runner self-test, server self-test, server lifecycle self-test, smoke runner self-test, fresh-host reproduction, fresh-host run-record template, fresh-host readiness-review template, UI adapter contract, UI component fixtures, framework bake-off, window/input/accessibility spike, page-surface composition, native UI readiness-review template, profile/session formats, profile/session schema-package template, profile/session readiness-review template, research package/update lab, research package/update lab-package template, research package/update readiness-review template, incident patch rehearsal, incident patch rehearsal-record template, incident/patch readiness-review template, backup ownership gap, backup-owner qualification template, backup ownership readiness-review template, implementation kickoff review, build-readiness dependency graph, documentation-readiness completion audit, implementation master plan, GitHub issue handoff, build-readiness closure-review template, task approval template, IPC capability boundary, IPC schema-source template, IPC readiness-review template, sandbox probe inventory, sandbox probe contract, sandbox probe-package template, sandbox readiness-review template, Servo local compatibility corpus route self-test, Servo local compatibility HTTPS harness plan, "
        "research-log chronology, repository-map core registries, index/root/start machine-registry navigation, "
        "research-index lanes/crosswalk, start-here continuation, "
        "documentation-readiness evidence/DoD, "
        "docs index continuation, root README continuation, agent/contributor check guidance, "
        "GitHub handoff templates, xtask aggregate-check coverage, CI committed-diff whitespace, "
        "local aggregate diff hygiene, line-ending policy, and Windows wrappers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
