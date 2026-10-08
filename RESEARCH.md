# User brief and research — 8 October 2026

State: RESEARCHED → BUILDING.

User: Web release engineers checking captured endpoint headers.

Painful task: Header changes can violate an intended cache scope, TTL cap or Vary requirement while still looking plausible in review.

Smallest useful capability: Preserve repeated fields, detect duplicate directives and malformed TTLs, assert required/forbidden directives, shared-TTL caps and Vary headers.

Demand is inferred from the documented workflows and review risks. No verified request for this product, adoption, performance advantage or exhaustive feature gap is claimed. Search and repository/README/code/issue reads occurred on 8 October 2026; current exact stars and last-push timestamps below are observations, not quality scores.

Queries: `http cache semantics sort:stars; cache-control in:name sort:stars`. Live GitHub search used `sort:stars`. Broad queries return unrelated repository/readme matches; irrelevant results were excluded. Coverage is limited, not an exhaustive global ranking. The highest-star relevant comparable among those examined is [kornelski/http-cache-semantics](https://github.com/kornelski/http-cache-semantics) at 261 stars.

| Comparable | Stars | Last push (UTC) | License | Workflow, setup, capabilities and tradeoffs |
|---|---:|---|---|---|
| [kornelski/http-cache-semantics](https://github.com/kornelski/http-cache-semantics) | 261 | 2026-10-04T02:55:02Z | BSD-2-Clause | JavaScript CachePolicy models reuse, Vary, freshness and revalidation. Runnable documented API examples. Broad runtime cache semantics; our tool asserts captured-header deployment intent only. |
| [pquerna/cachecontrol](https://github.com/pquerna/cachecontrol) | 150 | 2026-03-19T22:10:38Z | Apache-2.0 | Go high/low-level parsing API returns named noncacheability reasons and expiry. Requires Go integration; broader cache decisions than our offline header expectation gate. |
| [tusbar/cache-control](https://github.com/tusbar/cache-control) | 41 | 2026-09-03T20:03:54Z | MIT | TypeScript parse/format API with extensive numeric-header examples and extension fields. A header library; our tool is a captured-response contract CLI. |

Reliability/support observations are limited to public docs, latest source and open issue samples; alternatives were not installed or benchmarked in this run. Examples prove our behavior only. No comparative speed, memory, accuracy or time-to-result measurement was made. Licenses are metadata observations; no competitor implementation/prose was reused.

Acceptance: documented clean install; accepted example; meaningful rejected/input-error examples; deterministic JSON reports; core invariants covered by the unit tests; all remote matrix checks must pass on the intended default head before LIVE. The exact scope/non-goals are in README.md.

Discovery path: relevant GitHub topics and a clear README/linked portfolio index. No messages or third-party issue advertising planned, and no organic growth promise.

Portfolio distinction: compared against all 143 existing repository names/descriptions and relevant CSV/HTTP/parser tools. This is not a fork or a variant of an existing launch. The five candidates address spatial delivery, cache deployment intent, CSP inheritance changes, crawler route expectations and cross-export identifier mapping respectively. masklink-audit does not reconcile numeric CSV differences like table-reconcile, transform data or copy a redaction engine. They are separate user tasks, not subdivisions of one product.

## Commit-linked observations

- [kornelski/http-cache-semantics source snapshot](https://github.com/kornelski/http-cache-semantics/tree/b1d4bd682fbab0252985de45219f4e7497c0067c) — open issue sample: [#65](https://github.com/kornelski/http-cache-semantics/issues/65), [#64](https://github.com/kornelski/http-cache-semantics/issues/64), [#63](https://github.com/kornelski/http-cache-semantics/issues/63).
- [pquerna/cachecontrol source snapshot](https://github.com/pquerna/cachecontrol/tree/ff73c64d4b12a03dea25fca244d1ef016eca57c5) — open issue sample: [#32](https://github.com/pquerna/cachecontrol/issues/32), [#31](https://github.com/pquerna/cachecontrol/issues/31), [#29](https://github.com/pquerna/cachecontrol/issues/29).
- [tusbar/cache-control source snapshot](https://github.com/tusbar/cache-control/tree/8bf12d0d074e361403c8f61413d8da909dbd7e69) — open issue sample: [#413](https://github.com/tusbar/cache-control/issues/413), [#412](https://github.com/tusbar/cache-control/issues/412), [#411](https://github.com/tusbar/cache-control/issues/411).

Standards consulted: [GeoJSON RFC 7946](https://www.rfc-editor.org/rfc/rfc7946.html), [HTTP caching RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), [Robots RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html), [CSP3](https://www.w3.org/TR/CSP3/). Only the relevant standard informs each bounded tool; conformance is not claimed.
