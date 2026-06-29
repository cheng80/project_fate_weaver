from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root / "src"))
    from fateweaver.analyzer import analyze_logs

    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", default="logs")
    args = parser.parse_args()
    logs_path = Path(args.logs)
    path = logs_path if logs_path.is_absolute() else project_root / logs_path
    try:
        metrics = analyze_logs(path)
    except ValueError as error:
        print(f"ANALYSIS: ERROR {error}")
        return 1
    print(json.dumps(metrics, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
