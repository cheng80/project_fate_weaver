from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.data_loader import load_project_data


class DataLoaderTests(unittest.TestCase):
    def test_loads_console_validation_scenario(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))

        self.assertEqual("mvp0_console_test", loaded.scenario.id)
        self.assertIn("health", loaded.bundle.statuses)
        self.assertGreaterEqual(len(loaded.bundle.events), 12)
        self.assertIn("combat_response", loaded.bundle.choice_types)


if __name__ == "__main__":
    unittest.main()

