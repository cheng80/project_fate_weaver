from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GameplayP0Tests(unittest.TestCase):
    def test_tutorial_herb_quest_cli_outputs_p0_run_contract(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "balanced",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            text_logs = list(Path(tmp).glob("run_*.txt"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(json_logs), result.stdout + result.stderr)
        self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
        self.assertEqual("herb_gathering_tutorial", payload["quest"]["id"])
        self.assertEqual(3, payload["run_clock"]["max_days"])
        self.assertEqual(4, payload["run_clock"]["turns_per_day"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        self.assertTrue(any(turn["multi_select"]["selected"] for turn in payload["turns"]))
        self.assertIn("quest_report", payload)
        self.assertIn(payload["quest_report"]["result_type"], {"success", "partial_success", "failure"})
        first_turn = payload["turns"][0]
        self.assertIn("run_clock", first_turn)
        self.assertIn("quest_progress", first_turn)
        self.assertIn("score", first_turn)
        self.assertIn("next_event_tags", first_turn)
        self.assertIn("[Day 1 / Morning / Turn 1]", text_log)
        self.assertIn("Quest: 약초 채집 의뢰", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("Quest Progress:", text_log)
        self.assertIn("Score Change:", text_log)
        self.assertIn("Quest Report:", text_log)


if __name__ == "__main__":
    unittest.main()
