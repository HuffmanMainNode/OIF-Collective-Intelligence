# OIF Collective Intelligence

**A source-independent claim aggregation primitive for federated intelligence systems.**

Collective Intelligence focuses on how separate contributors can combine findings without erasing disagreement. This initial library groups observations by claim key, counts distinct source identities, and reports whether a configurable quorum has been reached. It does not infer truth from popularity, treat correlated sources as independent, or implement distributed consensus.

## Implemented

- Claim grouping by stable claim key.
- Distinct-source counting to avoid duplicate submissions inflating quorum.
- Explicit support and contradiction tallies.
- Quorum status and dissent preservation.
- Deterministic report output, fixture, and tests.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
oif-collective-report examples/observations.json
```

## Interpretation rules

- One source identity counts once per claim key and position.
- A source may submit a support or contradiction observation.
- Quorum means a configured number of distinct source IDs, not truth.
- Correlated sources may still share a common upstream error.
- Minority findings remain visible in the report.

## Scope

This repository owns aggregation and disagreement representation. Individual research provenance is handled by [OIF-Research-Observatory](https://github.com/HuffmanMainNode/OIF-Research-Observatory), while swarm resource assignment is handled by [OI-Swarm-Intelligence](https://github.com/HuffmanMainNode/OI-Swarm-Intelligence).
