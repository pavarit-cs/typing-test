from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence, TypedDict

DEFAULT_STATS_FILENAME = "stats.json"


class StatRecord(TypedDict, total=False):
    timestamp: str
    duration_sec: float
    accuracy_pct: float
    wpm: float
    prompt_length: int
    input_length: int
    correct_chars: int
    incorrect_chars: int
    prompt: str
    mode: str


def _package_dir() -> Path:
    return Path(__file__).resolve().parent


def _resolve_stats_path(explicit: str | Path | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    env = os.getenv("TYPING_STATS_PATH", "").strip()
    if env:
        return Path(env).expanduser().resolve()

    return (_package_dir() / "data" / DEFAULT_STATS_FILENAME).resolve()


def load_stats(path: str | Path | None = None) -> list[StatRecord]:
    stats_path = _resolve_stats_path(path)
    if not stats_path.exists():
        return []

    try:
        with stats_path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return []

    if isinstance(raw, list):
        result: list[StatRecord] = []
        for item in raw:
            if isinstance(item, dict):
                result.append(item)  # type: ignore[arg-type]
        return result

    return []


def append_stat(record: StatRecord, path: str | Path | None = None) -> Path:
    stats_path = _resolve_stats_path(path)
    records = load_stats(stats_path)
    records.append(record)

    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)

    return stats_path


def create_stat_record(
    *,
    duration_sec: float,
    accuracy_pct: float,
    wpm: float,
    prompt_length: int,
    input_length: int,
    correct_chars: int,
    incorrect_chars: int,
    prompt: str,
    mode: str | None = None,
) -> StatRecord:
    record: StatRecord = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duration_sec": round(duration_sec, 4),
        "accuracy_pct": round(accuracy_pct, 2),
        "wpm": round(wpm, 2),
        "prompt_length": prompt_length,
        "input_length": input_length,
        "correct_chars": correct_chars,
        "incorrect_chars": incorrect_chars,
        "prompt": prompt,
    }
    if mode:
        record["mode"] = mode
    return record


def summarize_stats(records: Sequence[StatRecord]) -> dict[str, float | int | str | None]:
    if not records:
        return {
            "total_sessions": 0,
            "avg_wpm": 0.0,
            "avg_accuracy": 0.0,
            "best_wpm": None,
            "best_wpm_timestamp": None,
            "best_accuracy": None,
            "best_accuracy_timestamp": None,
        }

    total = len(records)

    def _extract(record: StatRecord, key: str) -> float:
        value = record.get(key)
        try:
            return float(value) if value is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    wpm_values = [_extract(record, "wpm") for record in records]
    accuracy_values = [_extract(record, "accuracy_pct") for record in records]

    best_wpm_record = max(records, key=lambda rec: _extract(rec, "wpm"))
    best_accuracy_record = max(records, key=lambda rec: _extract(rec, "accuracy_pct"))

    return {
        "total_sessions": total,
        "avg_wpm": round(sum(wpm_values) / total, 2),
        "avg_accuracy": round(sum(accuracy_values) / total, 2),
        "best_wpm": best_wpm_record.get("wpm"),
        "best_wpm_timestamp": best_wpm_record.get("timestamp"),
        "best_accuracy": best_accuracy_record.get("accuracy_pct"),
        "best_accuracy_timestamp": best_accuracy_record.get("timestamp"),
    }


def recent_stats(records: Sequence[StatRecord], limit: int = 5) -> list[StatRecord]:
    if limit <= 0:
        return []
    return list(records[-limit:])


__all__ = [
    "StatRecord",
    "append_stat",
    "create_stat_record",
    "load_stats",
    "recent_stats",
    "summarize_stats",
]
