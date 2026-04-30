# Observability and security checks

Mirrors the author-side `observability-and-security.md`. Cross-cutting concerns architects most commonly bolt on post-hoc; this is where the artifact specifies where they enter. Five soft-reject checks total — three security, two observability.

## check.security.trust-zones-not-drawn (soft)

**Check that** trust zones are drawn explicitly with named boundary crossings.

**Reject when** the document does not enumerate trust zones (typically: internet, authenticated user session, internal service mesh, service process), OR does not state what crosses each boundary with what guarantees.

**Approve when** zones are enumerated and each crossing is named with the controls applied (TLS termination, JWT validation, mTLS, rate limit at gateway, etc.).

**Evidence pattern:** quote the section heading or the relevant body line; note which crossings are missing.

**recommended_action:** *"Draw trust zones explicitly. STRIDE controls per crossing are how the threat model becomes auditable; an undrawn boundary is one nobody is responsible for."*

## check.security.authn-authz-evaluation-layer-unnamed (soft)

**Check that** authn/authz at every externally callable interface names the evaluation layer (gateway / middleware / handler).

**Reject when** authn or authz is mentioned but the evaluation layer is not named — leaving it to be discovered or duplicated per component.

**Approve when** every externally callable interface entry states authentication (with claims propagated) AND authorisation with the evaluation layer named.

**Note:** this overlaps with `check.interface.missing-authn-authz` (which fires when authn/authz is wholly absent). This check fires when authn/authz is named but the layer is missing — a softer but still-soft-reject failure.

**recommended_action:** *"Name the evaluation layer per externally callable interface. Putting authn/authz in DD alone duplicates the decision per component; naming the layer once at Architecture stops the duplication."*

## check.security.secrets-flow-unspecified (soft)

**Check that** secrets flow is specified: origin, in-memory holders, bearer-only components, forbidden surfaces.

**Reject when** the document mentions secrets (DB credentials, API keys, signing keys, OIDC tokens) but does not specify origin (secret manager / KMS / OIDC), in-memory holders, OR forbidden surfaces (logs, metrics, traces, exception messages).

**Approve when** every named secret has all four populated.

**recommended_action:** *"Specify secrets flow per secret: origin, in-memory holders, bearer-only components, forbidden surfaces. The shape of every leakage incident is in these omissions."*

## check.observability.telemetry-emergence-unspecified (soft)

**Check that** telemetry emergence points are specified: which logs, what metrics, what traces, common context fields.

**Reject when** the document mentions observability or "we use OpenTelemetry" without naming the common context fields (request id, tenant, subject, correlation id, span context), the SLO-bearing metrics, OR the trace propagation strategy across cross-process calls.

**Approve when** logs/metrics/traces are specified with common fields, SLO-bearing metrics named, and trace propagation across boundaries stated (typically W3C TraceContext).

**recommended_action:** *"Name telemetry emergence points: common context fields on every record, SLO-bearing metrics, trace propagation across cross-process boundaries. Observability bolted on at incident time always misses the context that would have made the incident short."*

## check.observability.sampling-policy-unspecified (soft)

**Check that** the trace-sampling policy is specified.

**Reject when** the document names tracing without specifying a sampling policy (typical baseline: 100% errors + 1% successes), OR specifies a policy that is incoherent (sampling all errors at 1% would lose error visibility).

**Approve when** the sampling policy is concrete and defensible (100% errors + 1% successes, head-based vs tail-based stated, exemplar linkage to metrics named where relevant).

**recommended_action:** *"State the sampling policy. 'We trace everything' is not a policy — it is a billing event."*

## STRIDE coverage as a Quality Bar item

STRIDE per zone crossing is a Quality Bar Yes/No item rather than a stand-alone check id, because the level of STRIDE coverage required is scope-dependent (a payment service crosses every category; an internal-only metrics scraper does not). When STRIDE is partially or wholly absent on a security-critical scope, surface a `check.security.trust-zones-not-drawn` finding (the umbrella check) and cite the absent threat categories in evidence.

Cross-link: `quality-bar-gate.md` (Security & Observability card); `interface-contract-checks.md` (`check.interface.missing-authn-authz`); `composition-patterns-checks.md` (middleware stack ordering — security middleware is part of this).
