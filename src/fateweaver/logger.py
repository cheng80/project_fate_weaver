from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias

from fateweaver.models import JsonValue


RunLog: TypeAlias = dict[str, JsonValue]


def save_run_log(log: RunLog, logs_dir: Path, filename: str) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / filename
    with path.open("w", encoding="utf-8") as handle:
        json.dump(log, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_run_log(logs_dir: Path, scenario_id: str, seed: int, run_number: int, payload: RunLog) -> Path:
    log = {
        "schema_version": "console_validation_log_v0.1",
        "scenario_id": scenario_id,
        "seed": seed,
        "run_id": f"{scenario_id}-{seed}-{run_number:04d}",
        **payload,
    }
    return save_run_log(log, logs_dir, f"run_{scenario_id}_{seed}_{run_number:04d}.json")
