# Security · RunwayBase Agent

## Principles
- Least privilege, defense-in-depth, PII-free by design.

## Secrets management
- Store all credentials in a vault; inject at runtime (not in images).
- Rotate keys regularly; scope to minimal permissions.

## Network & access
- Restrict admin/API access via auth and IP allowlists for admin.
- Egress control: limit outbound to required destinations; proxy pool allowlist.

## Data handling
- No PII collected; raw HTML retained for limited time per retention policy.
- Encrypt data at rest (managed services) and TLS in transit.

## App security
- Input validation for APIs; rate limiting; request logging.
- Dependency scanning and updates; SAST/DAST in CI.

## Threat model (high-level)
- Abuse of crawlers → mitigate with robots compliance, rate limits, and identification.
- Credential leakage → mitigate with vault and rotation.
- Index poisoning → validate inputs, sanitize HTML, strip scripts.

## Incident response
- Triage, contain, eradicate, recover; postmortem within 5 business days.
- Audit logs for admin actions; time-synced logs for forensics.