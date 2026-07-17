# Secure Development, Provenance, and AI-assisted Coding

Status: secure-development baseline  
Owner: security, build, supply chain, agent operations, and release

Turing maps its development process to NIST SSDF 1.1. NIST SSDF 1.2 remains a draft as of the research date and is tracked rather than represented as final. NIST SP 800-218A supplements the baseline for AI-related development.

SLSA 1.2 Source and Build concepts inform source review and build provenance. Each release records source commit, review attestations, agent-run manifests, toolchains, build environment, dependencies, generated inputs, SBOM, license notices, vulnerability state, artifact digests, signatures, and reproducibility results.

OpenSSF Scorecard and scanners are supplementary signals, not security certification. Evidence must remain reviewable when services or tools are unavailable.
