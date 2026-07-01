from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from fateweaver.validator import validate_scenario_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
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
        final_turn = turns[-1]

        self.assertLess(len(turns), 25)
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in turns))
        self.assertTrue(final_turn["quest_success"])
        self.assertTrue(final_turn["reward_granted"])
        self.assertFalse(final_turn["completion_blocked_by_min_turns"])
        self.assertTrue(final_turn["run_complete"])
        self.assertEqual({"money": 2, "reputation": 1}, final_turn["reward_delta"])
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
if __name__ == "__main__":
    unittest.main()
