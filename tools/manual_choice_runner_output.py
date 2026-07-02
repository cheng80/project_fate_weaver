from __future__ import annotations

import json
from pathlib import Path


def write_outputs(output_dir: Path, seed: int, log: dict, trace: list[dict]) -> tuple[Path, Path, Path, Path]:
    from fateweaver.text_mud_log import render_text_mud_log

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"manual_seed_{seed}.json"
    text_path = output_dir / f"manual_seed_{seed}_text_mud.txt"
    trace_path = output_dir / f"manual_seed_{seed}_choice_trace.json"
    summary_path = output_dir / f"manual_seed_{seed}_summary.json"
    summary = {
        "manual_choice_mode": True,
        "choice_source": log["choice_source"],
        "agent_policy": log.get("agent_policy"),
        "turn_count": len(log["turns"]),
        "ending": log["quest_report"].get("ending"),
        "result_type": log["quest_report"].get("result_type"),
        "selected_indexes": [entry["selected_index"] for entry in trace],
        "selected_card_ids": [entry["selected_card_id"] for entry in trace],
        "unused_choices": log["unused_choices"],
        "stop_reason": log["stop_reason"],
        "manual_stop_reason": log["manual_stop_reason"],
    }
    json_path.write_text(json.dumps(log, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text_path.write_text(render_text_mud_log(log), encoding="utf-8")
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return json_path, text_path, trace_path, summary_path
