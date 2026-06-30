from __future__ import annotations

from typing import Final, assert_never

from fateweaver.models import JsonMap, JsonValue

MISSING: Final = "-"


def json_maps(value: JsonValue | None) -> tuple[JsonMap, ...]:
    match value:
        case list():
            maps: list[JsonMap] = []
            for item in value:
                match item:
                    case dict():
                        maps.append(item)
                    case None | bool() | str() | int() | float() | list():
                        continue
                    case unreachable:
                        assert_never(unreachable)
            return tuple(maps)
        case None | bool() | str() | int() | float() | dict():
            return ()
        case unreachable:
            assert_never(unreachable)


def json_map(value: JsonValue | None) -> JsonMap:
    match value:
        case dict():
            return value
        case None | bool() | str() | int() | float() | list():
            return {}
        case unreachable:
            assert_never(unreachable)


def json_values(value: JsonValue | None) -> tuple[JsonValue, ...]:
    match value:
        case list():
            return tuple(value)
        case None | bool() | str() | int() | float() | dict():
            return ()
        case unreachable:
            assert_never(unreachable)


def text(value: JsonValue | None) -> str:
    match value:
        case None:
            return MISSING
        case bool():
            return str(value).lower()
        case str():
            return value
        case int() | float():
            return str(value)
        case list():
            return ", ".join(text(item) for item in value) or MISSING
        case dict():
            return ", ".join(f"{key}={text(nested)}" for key, nested in sorted(value.items())) or MISSING
        case unreachable:
            assert_never(unreachable)
