from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.ontology_reasoner import OntologyReasonerContext, load_ontology_core, run_reasoner


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class OntologyReasonerTests(unittest.TestCase):
    def test_low_food_produces_resource_recovery_trace(self) -> None:
        core = load_ontology_core(PROJECT_ROOT)
        inference = run_reasoner(
            core,
            OntologyReasonerContext(
                quest_id="survive_the_storm_pass",
                region="forest",
                status={"health": 8, "food": 2, "money": 4, "reputation": 1, "curse": 1},
                inventory=("torch",),
                clues=(),
                omens=(),
                quest_progress={},
                next_event_tags=(),
            ),
        )

        self.assertIn("state.low_food", inference["active_state_facts"])
        self.assertIn("intent.resource_recovery", inference["situation_intents"])
        self.assertTrue(any(trace["rule_id"] == "rule.low_food_seek_recovery" for trace in inference["trace"]))
        self.assertTrue(
            any(
                modifier["target"] == "event" and "hunger" in modifier["tags"]
                for modifier in inference["event_weight_modifiers"]
            ),
            inference,
        )

    def test_missing_clue_and_relation_rule_are_traceable(self) -> None:
        core = load_ontology_core(PROJECT_ROOT)
        inference = run_reasoner(
            core,
            OntologyReasonerContext(
                quest_id="survive_the_storm_pass",
                region="forest",
                status={"health": 9, "food": 9, "money": 4, "reputation": 1, "curse": 1},
                inventory=("camp_tarp",),
                clues=(),
                omens=(),
                quest_progress={},
                next_event_tags=("storm",),
            ),
        )

        rule_ids = {str(trace["rule_id"]) for trace in inference["trace"]}
        self.assertIn("rule.storm_pass_shelter", rule_ids)
        self.assertIn("rule.missing_storm_clue", rule_ids)
        self.assertIn("rule.forest_route_commitment", rule_ids)

    def test_high_curse_produces_next_fact_without_runtime_llm_reasoning(self) -> None:
        core = load_ontology_core(PROJECT_ROOT)
        inference = run_reasoner(
            core,
            OntologyReasonerContext(
                quest_id="survive_the_storm_pass",
                region="forest",
                status={"health": 7, "food": 7, "money": 4, "reputation": 1, "curse": 5},
                inventory=(),
                clues=("storm_warning",),
                omens=("black_cloud",),
                quest_progress={},
                next_event_tags=(),
            ),
        )

        self.assertIn("fact.inferred.intent.omen_escalation", inference["next_facts"])
        self.assertIn("intent.omen_escalation", inference["situation_intents"])


if __name__ == "__main__":
    unittest.main()
