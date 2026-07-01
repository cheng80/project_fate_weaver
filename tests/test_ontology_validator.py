from __future__ import annotations

import shutil
import unittest
from pathlib import Path

import yaml

from fateweaver.ontology_validator import validate_ontology_core


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class OntologyValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = PROJECT_ROOT / ".omo/ulw-loop/tmp/ontology-validator-test"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        shutil.copytree(PROJECT_ROOT / "data", self.tmp / "data")

    def tearDown(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_core_seed_validates(self) -> None:
        self.assertEqual([], validate_ontology_core(PROJECT_ROOT))

    def test_duplicate_entity_id_is_reported(self) -> None:
        raw = _ontology_raw(self.tmp)
        first = dict(raw["ontology_core"]["entities"][0])
        raw["ontology_core"]["entities"].append(first)
        _write_ontology(self.tmp, raw)

        errors = validate_ontology_core(self.tmp)

        self.assertTrue(any("Duplicate ontology entity id" in error for error in errors), errors)

    def test_relation_with_unknown_subject_is_reported(self) -> None:
        raw = _ontology_raw(self.tmp)
        raw["ontology_core"]["relations"][0]["subject"] = "quest.missing"
        _write_ontology(self.tmp, raw)

        errors = validate_ontology_core(self.tmp)

        self.assertTrue(any("Unknown relation subject quest.missing" in error for error in errors), errors)

    def test_rule_with_unknown_weight_tag_is_reported(self) -> None:
        raw = _ontology_raw(self.tmp)
        raw["ontology_core"]["rules"][0]["then"]["add_event_weight"]["tags"] = ["missing_weight_tag"]
        _write_ontology(self.tmp, raw)

        errors = validate_ontology_core(self.tmp)

        self.assertTrue(any("Unknown rule weight tag missing_weight_tag" in error for error in errors), errors)


def _ontology_raw(root: Path) -> dict[str, object]:
    return yaml.safe_load((root / "data/core/ontology.yaml").read_text(encoding="utf-8"))


def _write_ontology(root: Path, raw: dict[str, object]) -> None:
    (root / "data/core/ontology.yaml").write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
