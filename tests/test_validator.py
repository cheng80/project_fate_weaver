from dataclasses import replace
from pathlib import Path
import unittest

from fateweaver.data_loader import load_project_data
from fateweaver.validator import validate_bundle


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestValidator(unittest.TestCase):
    def test_validate_bundle_when_real_scenario_then_no_errors(self) -> None:
        # Given
        bundle, scenario = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")

        # When
        errors = validate_bundle(bundle, scenario)

        # Then
        self.assertEqual([], errors)

    def test_validate_bundle_when_initial_item_missing_then_reports_error(self) -> None:
        # Given
        bundle, scenario = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")
        broken = replace(scenario, initial_items=("missing_item",))

        # When
        errors = validate_bundle(bundle, broken)

        # Then
        self.assertIn("Unknown initial item: missing_item", errors)

    def test_validate_bundle_when_choice_type_missing_then_reports_error(self) -> None:
        # Given
        bundle, scenario = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/mvp0_console_test.yaml")
        first = bundle.events[0]
        broken_choice = replace(first.choices[0], choice_type="missing_type")
        broken_event = replace(first, choices=(broken_choice, *first.choices[1:]))
        broken_bundle = replace(bundle, events=(broken_event, *bundle.events[1:]))

        # When
        errors = validate_bundle(broken_bundle, scenario)

        # Then
        self.assertIn("Unknown choice type missing_type in cursed_well/pass", errors)


if __name__ == "__main__":
    unittest.main()
