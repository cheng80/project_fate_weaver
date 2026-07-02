from __future__ import annotations

import unittest

from fateweaver.game_semantics import SemanticContext, evaluate_semantic_rules
from fateweaver.models import JsonMap


class GameSemanticsTests(unittest.TestCase):
    def test_evaluator_matches_state_fact_without_game_specific_context(self) -> None:
        core: JsonMap = {
            "state_facts": [
                {"id": "state.low_energy", "source": "resource", "key": "energy", "op": "lte", "value": 2},
            ],
            "rules": [
                {
                    "id": "rule.low_energy_recover",
                    "when": {"state_fact": "state.low_energy"},
                    "then": {
                        "suggest_intent": "intent.recover",
                        "add_event_weight": {"tags": ["rest"], "amount": 3},
                    },
                },
            ],
        }

        inference = evaluate_semantic_rules(
            core,
            SemanticContext(
                active_entities=(),
                active_tags=(),
                resources={"energy": 1},
                inventory=(),
                markers=(),
                counters={},
            ),
        )

        self.assertIn("state.low_energy", inference["active_state_facts"])
        self.assertIn("intent.recover", inference["situation_intents"])
        self.assertEqual("rule.low_energy_recover", inference["trace"][0]["rule_id"])


if __name__ == "__main__":
    unittest.main()
