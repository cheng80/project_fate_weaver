from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.data_loader import load_project_data
from fateweaver.state_manager import apply_choice_result


class StateManagerTests(unittest.TestCase):
    def test_apply_choice_result_clamps_status_and_updates_inventory(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))

        state = apply_choice_result(
            {"health": 9, "food": 0, "money": 0, "reputation": 0, "curse": 1},
            ("rope",),
            (),
            {"status": {"health": 5, "food": -2}, "add_item": ["torch"], "remove_item": ["rope"], "add_run_tag": ["tested"]},
            loaded.bundle.statuses,
        )

        self.assertEqual(10, state.status["health"])
        self.assertEqual(0, state.status["food"])
        self.assertEqual(("torch",), state.inventory)
        self.assertEqual(("tested",), state.run_tags)


if __name__ == "__main__":
    unittest.main()

