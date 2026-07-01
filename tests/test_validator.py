from dataclasses import replace
from pathlib import Path
import unittest

from fateweaver.data_loader import load_project_data
from fateweaver.validator import validate_bundle


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestValidator(unittest.TestCase):
    def test_validate_bundle_when_real_scenario_then_no_errors(self) -> None:
        # Given
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")

        # When
        errors = validate_bundle(loaded.bundle, loaded.scenario)

        # Then
        self.assertEqual([], errors)

    def test_validate_bundle_when_initial_item_missing_then_reports_error(self) -> None:
        # Given
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")
        broken = replace(loaded.scenario, initial_items=("missing_item",))

        # When
        errors = validate_bundle(loaded.bundle, broken)

        # Then
        self.assertIn("Unknown initial item: missing_item", errors)

    def test_validate_bundle_when_choice_type_missing_then_reports_error(self) -> None:
        # Given
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")
        first = loaded.bundle.events[0]
        broken_choice = replace(first.choices[0], choice_type="missing_type")
        broken_event = replace(first, choices=(broken_choice, *first.choices[1:]))
        broken_bundle = replace(loaded.bundle, events=(broken_event, *loaded.bundle.events[1:]))

        # When
        errors = validate_bundle(broken_bundle, loaded.scenario)

        # Then
        self.assertIn(f"Unknown choice type missing_type in {first.id}/pass", errors)


if __name__ == "__main__":
    unittest.main()
