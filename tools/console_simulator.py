from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root / "src"))
    from fateweaver.choice_scoring import VALID_AUTOPLAYER_PROFILES
    from fateweaver.simulator import run_console_simulation

    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--logs", default="logs")
    parser.add_argument("--profile", choices=VALID_AUTOPLAYER_PROFILES, default="balanced")
    args = parser.parse_args()
    scenario_path = Path(args.scenario)
    logs_path = Path(args.logs)
    logs_dir = logs_path if logs_path.is_absolute() else project_root / logs_path
    path = scenario_path if scenario_path.is_absolute() else project_root / scenario_path
    try:
        saved_paths = run_console_simulation(project_root, path, args.seed, args.runs, logs_dir, sys.stdin, sys.stdout, args.profile)
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"SIMULATOR: ERROR {error}")
        return 1
    for saved in saved_paths:
        print(f"LOG: {saved}")
        text_log_path = saved.with_suffix(".txt")
        if text_log_path.exists():
            print(f"TEXT_MUD_LOG: {text_log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
