from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from fateweaver.models import JsonMap, JsonValue


@dataclass(frozen=True, slots=True)
class YamlTypeError(TypeError):
    label: str
    expected: str

    def __str__(self) -> str:
        return f"{self.label} must be {self.expected}"


def read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    return as_mapping(loaded, str(path))


def mapping_at(raw: JsonMap, key: str) -> JsonMap:
    return as_mapping(raw.get(key, {}), key)


def list_at(raw: JsonMap, key: str) -> list[JsonValue]:
    return as_list(raw.get(key, []), key)


def as_mapping(value: JsonValue, label: str = "value") -> JsonMap:
    if not isinstance(value, dict):
        raise YamlTypeError(label, "a mapping")
    return {str(key): item for key, item in value.items()}


def as_list(value: JsonValue, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise YamlTypeError(label, "a list")
    return value


def optional_string(raw: JsonMap, key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise YamlTypeError(key, "a string")
    return value


def string_tuple(value: JsonValue, *, strict: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list):
        if strict:
            raise YamlTypeError("value", "a list")
        return ()
    return tuple(str(item) for item in value)


def string_list_at(raw: JsonMap, key: str) -> list[str]:
    values = as_list(raw.get(key, []), key)
    strings: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise YamlTypeError(f"{key} values", "strings")
        strings.append(value)
    return strings
