from __future__ import annotations

import unittest

from fateweaver.gameplay_p0_rules import select_cards
from tests.test_gameplay_balance_pass import _cards, _state


class ResourceAlternativeSurfaceGateTests(unittest.TestCase):
    def test_balanced_profile_uses_resource_at_food_caution(self) -> None:
        selected, _combo = select_cards(_cards(), (), _state(status={"health": 8, "food": 3, "money": 20}), "balanced")

        self.assertEqual("resource_alternative", selected[0].slot_role)


if __name__ == "__main__":
    unittest.main()
