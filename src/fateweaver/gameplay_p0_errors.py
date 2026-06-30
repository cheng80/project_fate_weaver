from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MissingCardSlotError(Exception):
    slot: str

    def __str__(self) -> str:
        return f"No P0 candidate for slot: {self.slot}"


@dataclass(frozen=True, slots=True)
class ExpectedMappingError(Exception):
    value_type: str

    def __str__(self) -> str:
        return f"value must be a mapping, got {self.value_type}"
