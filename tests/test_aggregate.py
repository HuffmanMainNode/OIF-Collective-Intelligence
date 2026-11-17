import unittest

from oif_collective.aggregate import aggregate_observations


class AggregateTests(unittest.TestCase):
    def test_quorum_counts_distinct_sources(self):
        items = [
            {"claim_key": "c", "source_id": "a", "position": "supports"},
            {"claim_key": "c", "source_id": "a", "position": "supports"},
        ]
        self.assertEqual(aggregate_observations(items, 2)[0]["status"], "insufficient_independent_sources")

    def test_preserves_dissent(self):
        items = [
            {"claim_key": "c", "source_id": "a", "position": "supports"},
            {"claim_key": "c", "source_id": "b", "position": "supports"},
            {"claim_key": "c", "source_id": "c", "position": "contradicts"},
            {"claim_key": "c", "source_id": "d", "position": "contradicts"},
        ]
        result = aggregate_observations(items, 2)[0]
        self.assertEqual(result["status"], "contested")
        self.assertFalse(result["truth_established"])

    def test_invalid_position_rejected(self):
        with self.assertRaises(ValueError):
            aggregate_observations([{"claim_key": "c", "source_id": "a", "position": "maybe"}])

    def test_quorum_must_be_positive(self):
        with self.assertRaises(ValueError):
            aggregate_observations([], 0)


if __name__ == "__main__":
    unittest.main()
