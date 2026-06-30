from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MERCHANT_PACK_CARDS = {
    "question_merchant_about_pack",
    "inspect_lost_pack_tracks",
    "follow_bandit_scuff_marks",
    "recover_lost_merchant_pack",
    "return_pack_honestly",
    "negotiate_bonus_payment",
    "hide_valuable_trinket",
}


class GameplayP0MerchantLostPackTests(unittest.TestCase):
    def test_merchant_lost_pack_success_partial_failure(self) -> None:
        # Given
        cases = (
            ("data/scenarios/merchant_lost_pack_recovery.yaml", "success"),
            ("data/scenarios/merchant_lost_pack_recovery_partial.yaml", "partial_success"),
            ("data/scenarios/merchant_lost_pack_recovery_failure.yaml", "failure"),
        )

        # When
        reports = {expected: _run_scenario(path)["quest_report"] for path, expected in cases}

        # Then
        self.assertEqual("success", reports["success"]["result_type"])
        self.assertEqual("partial_success", reports["partial_success"]["result_type"])
        self.assertEqual("failure", reports["failure"]["result_type"])
        self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
        self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
        self.assertEqual("completed", _objective_status(reports["success"], "locate_lost_pack"))
        self.assertEqual("completed", _objective_status(reports["success"], "resolve_pack_ownership"))
        self.assertEqual("completed", _objective_status(reports["success"], "return_to_village"))
        self.assertEqual("completed", _objective_status(reports["success"], "survive_expedition"))
        self.assertEqual("completed", _objective_status(reports["success"], "negotiate_bonus_payment"))
        self.assertEqual("completed", _objective_status(reports["success"], "preserve_merchant_trust"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "locate_lost_pack"))
        self.assertEqual("failed", _objective_status(reports["partial_success"], "resolve_pack_ownership"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "return_to_village"))
        self.assertEqual("recovery_failed", _objective_reason(reports["partial_success"], "resolve_pack_ownership"))
        self.assertEqual("failed", _objective_status(reports["failure"], "locate_lost_pack"))
        self.assertEqual("failed", _objective_status(reports["failure"], "resolve_pack_ownership"))
        self.assertEqual("failed", _objective_status(reports["failure"], "return_to_village"))
        self.assertIn("primary_objective_failed", reports["failure"]["failure_reasons"])
        self.assertEqual("objective_failed", reports["failure"]["failure_kind"])
        self.assertEqual("alive", reports["failure"]["character_outcome"])

    def test_merchant_lost_pack_storylet_hints_and_logs(self) -> None:
        # Given
        payload = _run_scenario("data/scenarios/merchant_lost_pack_recovery.yaml")
        text_log = payload["_text_log"]

        # Then
        self.assertEqual("merchant_lost_pack_recovery", payload["quest"]["id"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        hinted_turns = [turn for turn in payload["turns"] if turn["card_candidate_hints"]]
        self.assertTrue(hinted_turns)
        hinted_ids = {card_id for turn in hinted_turns for card_id in turn["card_candidate_hints"]}
        self.assertIn("inspect_lost_pack_tracks", hinted_ids)
        self.assertIn("return_pack_honestly", hinted_ids)
        self.assertIn("negotiate_bonus_payment", hinted_ids)
        self.assertTrue(any(turn["repeat_memory_snapshot"] is not None for turn in payload["turns"]))
        self.assertTrue(any("matched_storylet_hints" in card for turn in payload["turns"] for card in turn["card_candidate_pool"]))
        self.assertIn("Quest: 상인의 잃어버린 짐", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("선택:", text_log)
        self.assertIn("Quest Report:", text_log)
        self.assertIn("결과 유형: success", text_log)

    def test_merchant_lost_pack_money_reputation_paths(self) -> None:
        # Given
        success = _run_scenario("data/scenarios/merchant_lost_pack_recovery.yaml")
        partial = _run_scenario("data/scenarios/merchant_lost_pack_recovery_partial.yaml")

        # Then
        success_resources = success["quest_report"]["resource_summary"]
        partial_resources = partial["quest_report"]["resource_summary"]
        self.assertGreater(int(success_resources["money"]), int(partial_resources["money"]))
        self.assertGreater(int(success_resources["reputation"]), int(partial_resources["reputation"]))
        self.assertIn("reputation", success["quest_report"]["score_breakdown"])
        self.assertIn("resource_management", success["quest_report"]["score_breakdown"])
        success_cards = _all_presented_and_selected_cards(success)
        partial_cards = _all_presented_and_selected_cards(partial)
        self.assertIn("negotiate_bonus_payment", success_cards)
        self.assertIn("hide_valuable_trinket", partial_cards)

    def test_merchant_lost_pack_quest_id_gate_preserves_existing_quests(self) -> None:
        # Given
        payloads = (
            _run_scenario("data/scenarios/tutorial_herb_quest.yaml"),
            _run_scenario("data/scenarios/forest_path_scouting_tutorial.yaml"),
            _run_scenario("data/scenarios/missing_porter_search_intro.yaml"),
        )

        # Then
        self.assertTrue(all(payload["quest_report"]["result_type"] == "success" for payload in payloads))
        for payload in payloads:
            self.assertFalse(MERCHANT_PACK_CARDS.intersection(_all_presented_and_selected_cards(payload)))


def _run_scenario(scenario_path: str) -> JsonMap:
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                sys.executable,
                "tools/console_simulator.py",
                "--scenario",
                scenario_path,
                "--seed",
                "42",
                "--runs",
                "1",
                "--logs",
                tmp,
                "--profile",
                "balanced",
            ],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            text=True,
            timeout=15,
        )
        json_logs = list(Path(tmp).glob("run_*.json"))
        text_logs = list(Path(tmp).glob("run_*.txt"))
        payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
        payload["_text_log"] = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    if len(json_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    if len(text_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    return payload


def _objective_status(report: JsonMap, objective_id: str) -> str:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return str(objective["status"])
    raise AssertionError(f"missing objective result: {objective_id}")


def _objective_reason(report: JsonMap, objective_id: str) -> str:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return str(objective["reason"])
    raise AssertionError(f"missing objective result: {objective_id}")


def _all_presented_and_selected_cards(payload: JsonMap) -> set[str]:
    presented = {card["card_id"] for turn in payload["turns"] for card in turn["presented_cards"]}
    selected = {card_id for turn in payload["turns"] for card_id in turn["selected_cards"]}
    return presented.union(selected)


if __name__ == "__main__":
    unittest.main()
