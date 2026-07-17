# Service Dependencies and Offline Behavior

Status: service architecture framework  
Owner: operations, privacy, security, product, and support

Potential services include update distribution, crash symbols, optional telemetry, phishing reputation, Plug-in distribution/revocation, encrypted sync, account recovery, optional remote AI routing, and compatibility configuration.

For each service, document whether ordinary browsing works without it, data classes, retention, encryption, authentication, availability, disaster recovery, abuse controls, rate limits, regional constraints, cost, replacement, shutdown, export, and self-hosting boundary.

Optional service failure must degrade safely. A cloud outage cannot silently disable local browsing, profile access, security indicators, or user export.
