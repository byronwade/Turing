# Independent Verification and Adversarial Review

Status: operating baseline  
Owner: quality, security, accessibility, performance, and release

## Verification lanes

- **Specification:** WPT, Test262, protocol suites, and reduced normative tests.
- **Implementation:** code-owner and architecture review independent of the authoring run.
- **Security:** threat-model delta, fuzzing, sanitizers, Miri where applicable, sandbox negative tests, and exploit-chain review.
- **Performance:** immutable workloads on controlled hardware with raw samples and complete manifests.
- **Accessibility:** automated semantics plus keyboard and qualified assistive-technology evaluation.
- **Release:** clean rebuild, provenance, signatures, installation, update, rollback, migration, and crash recovery.

## Adversarial review

Review explicitly attempts to falsify the implementation, not merely confirm intended behavior. It covers stale identities, confused-deputy paths, boundary bypass, malformed data, cancellation races, partial failure, resource exhaustion, secret leakage, downgrade, replay, and unsafe recovery.

A verifier cannot silently patch the implementation it is certifying; findings return to a new implementation task.
