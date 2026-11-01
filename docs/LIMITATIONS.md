## CP09 update — 28 October 2026

[Current checkpoint](checkpoints/CP09_ELEVEN_ISSUERS_AND_ROBUSTNESS.md): 11 financial research issuers, 16 evidence records, 71 facts; eight new reviewed PDFs, 44 reproducible facts. 128 backend tests and four frontend race tests pass. [Robustness matrix](ROBUSTNESS_MATRIX.md) distinguishes implemented controls from remaining gaps. Coverage remains historical/partial; deployment and live Gemini evaluation are pending deferred configuration. Earlier entries below are historical.

# Known limitations — honest release state

## HIGH / release blockers
- No verified public deployment or GitHub URL. No cloud account connected or purchase made. Assessment submission remains incomplete.
- Source redistribution permission has not been certified. Snapshots are intended for local research; review terms before public hosting.
- Original ENAM assessment PDFs absent. Requirements were inferred from the two provided Markdown documents.
- Primary research covers one issuer with four manually verified source notes. Original PDF extraction/download for those sources did not succeed here. Generic CLI acquisition is not automatic full ingestion/indexing or fresh-data polling.
- Runtime AI is deliberately not implemented. Broad natural-language reasoning returns retrieval-only/no-model status. No claims of Gemini performance, quotas or API credits.

## MEDIUM
- 18 watchlist labels are illustrative. Current listings/symbol transitions are not certified; only three have EOD data. Not a fixed ticker whitelist: valid unfamiliar symbols return missing coverage.
- Data is an imported snapshot, not live. The daily digest uses current clock; it will naturally empty after the snapshot ages. FY25 replay remains accessible.
- Document-note hashes identify derived notes, not original PDF bytes. No claim of full-file cryptographic provenance.
- Initial FY25 guidance only. Later revisions, all prior-four-quarter guidance and more company cases are absent. Revenue constant-currency growth cannot be compared with quarterly INR growth.
- Financial facts are curated backend records; not automated table extraction. Missing EBITDA stays missing; bank financial data absent.
- Deduplication groups exact attachment URLs/hashes only. Differently named cross-exchange copies and semantic followups may remain separate. Revision preservation/cache invalidation primitives are tested synthetically, not demonstrated with a real corrected filing pair.
- No calendar-aware missing-session audit or automated corporate-action feed. A supplied corporate-action flag suppresses anomalies, but real flags are not populated. Raw-price observations require source inspection.
- Process-local rate limits and counters. Single process supported; no shared multi-instance quota store, model concurrency mechanism or model-budget implementation needed/claimed for this no-model release.
- CLI imports are quarantined as raw/unverified files, not automatically promoted into served verified research.

## LOW
- Plain browser JavaScript instead of requested Next.js/TypeScript/Tailwind; no frontend build or frontend unit-test framework.
- Mobile browser checks were interactive at an observed CSS width of 375, not automated device-lab coverage. Financial tables scroll within their container.
- Provider links may fail later or block direct downloads. Local source notes preserve only minimal evidence, not full reports.
- SQLite has no migrations or admin UI; app supports a small single-user local assessment demo.
- One upstream TestClient deprecation warning remains; tests pass.
