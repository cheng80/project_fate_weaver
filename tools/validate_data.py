from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root / "src"))
    from fateweaver.validator import validate_scenario_file

    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()
    scenario_path = Path(args.scenario)
    path = scenario_path if scenario_path.is_absolute() else project_root / scenario_path
    try:
        errors = validate_scenario_file(project_root, path)
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"VALIDATION: ERROR {error}")
        return 1
    if errors:
        for error in errors:
            print(f"VALIDATION: ERROR {error}")
        return 1
    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
