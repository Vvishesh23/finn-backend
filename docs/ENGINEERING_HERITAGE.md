# Engineering heritage

## Inspired principles
Point-in-time evidence, provenance, separate economic/publication dates, financial dimension checks, prior-session baselines, immutable evidence and honest missing-data states were described in the supplied brief.

## Independent FINN implementation
New `analytics.py` for cutoffs/grouping/calculation; `models.py` for input contracts; `store.py` for raw records and caches; `research.py` for bounded plans and source references. Tests exercise synthetic edge cases and real public-source fixtures.

## Explicit exclusions
No external HDD, previous repository, private dataset, trading strategy, broker account, credentials, backtests or prior UI assets accessed or imported. No broad disk search performed.

## Verification evidence
The visible build session starts from an empty generated workspace. Public acquisition logs and imported metadata identify the sources. Test command: `python -m pytest backend/tests -q`. This is an independently authored prototype, not a certified production investment system.
