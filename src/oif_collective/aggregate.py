"""Aggregate independent-source observations without treating quorum as truth."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def aggregate_observations(observations: list[dict[str, Any]], quorum: int = 2) -> list[dict[str, Any]]:
    if quorum < 1:
        raise ValueError("quorum must be at least 1")
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"supports": set(), "contradicts": set()})
    for item in observations:
        key, source, position = item.get("claim_key"), item.get("source_id"), item.get("position")
        if not isinstance(key, str) or not key or not isinstance(source, str) or not source:
            raise ValueError("each observation requires claim_key and source_id")
        if position not in {"supports", "contradicts"}:
            raise ValueError("position must be supports or contradicts")
        grouped[key][position].add(source)

    report = []
    for key in sorted(grouped):
        support = sorted(grouped[key]["supports"])
        contradiction = sorted(grouped[key]["contradicts"])
        support_quorum = len(support) >= quorum
        contradiction_quorum = len(contradiction) >= quorum
        if support_quorum and contradiction_quorum:
            status = "contested"
        elif support_quorum:
            status = "support_quorum"
        elif contradiction_quorum:
            status = "contradiction_quorum"
        else:
            status = "insufficient_independent_sources"
        report.append({
            "claim_key": key,
            "status": status,
            "supporting_sources": support,
            "contradicting_sources": contradiction,
            "quorum_required": quorum,
            "truth_established": False,
        })
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate source-distinct observations.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--quorum", type=int, default=2)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(aggregate_observations(data["observations"], args.quorum), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
