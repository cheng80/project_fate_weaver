from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from fateweaver.validator import validate_scenario_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
ITEM_GATED_SURFACE_CARDS = {
    "find_dry_refuge",
    "ration_the_last_supplies",
    "signal_from_high_ground",
}


class GameplayP0StandardRunTests(unittest.TestCase):
    def test_standard_run_scenario_validates(self) -> None:
        self.assertEqual([], validate_scenario_file(PROJECT_ROOT, SCENARIO_PATH))

    def test_standard_run_surfaces_json_text_mud_and_ending(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = _run_standard_scenario(Path(tmpdir))
            text_path = log_path.with_suffix(".txt")
            log = json.loads(log_path.read_text(encoding="utf-8"))
            text_log = text_path.read_text(encoding="utf-8")

        turns = list(log["turns"])
        presented_ids = [_card_id(card) for turn in turns for card in turn["presented_cards"]]
        selected_ids = [card_id for turn in turns for card_id in turn["selected_cards"]]
        event_counts = Counter(str(turn["event_id"]) for turn in turns)
        top_repeat = Counter(presented_ids).most_common(1)[0]
        final_turn = turns[-1]

        self.assertGreaterEqual(len(turns), 25)
        self.assertLessEqual(len(turns), 35)
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in turns))
        self.assertGreaterEqual(len(set(presented_ids)), 15)
        self.assertGreaterEqual(len(set(selected_ids)), 8)
        self.assertGreaterEqual(len(event_counts), 5)
        self.assertLessEqual(top_repeat[1], 10)
        self.assertTrue(ITEM_GATED_SURFACE_CARDS.issubset(set(presented_ids)))
        self.assertGreaterEqual(len(final_turn["clues"]), 3)
        self.assertGreaterEqual(len(final_turn["omens"]), 1)
        self.assertEqual("success", log["quest_report"]["result_type"])
        self.assertIn("ending", log["quest_report"])
        self.assertEqual("prepared_frontier_route", log["quest_report"]["ending"]["id"])
        self.assertIn("Run Ending: prepared_frontier_route", text_log)
        self.assertIn("[Run 종료]", text_log)


def _run_standard_scenario(logs_dir: Path) -> Path:
    command = [
        ".venv/bin/python",
        "tools/console_simulator.py",
        "--scenario",
        str(SCENARIO_PATH),
        "--seed",
        "42",
        "--runs",
        "1",
        "--logs",
        str(logs_dir),
        "--profile",
        "balanced",
    ]
    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env={**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"},
        check=True,
        capture_output=True,
        text=True,
    )
    return next(logs_dir.glob("*.json"))


def _card_id(card: dict[str, object]) -> str:
    return str(card.get("card_id") or card.get("id"))


if __name__ == "__main__":
    unittest.main()
