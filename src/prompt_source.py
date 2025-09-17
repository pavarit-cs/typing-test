# src/prompt_source.py
import os, json, random
from pathlib import Path

class PromptSourceError(Exception):
    pass

def _module_dir() -> Path:
    # โฟลเดอร์ที่ไฟล์นี้อยู่ (เช่น .../project/src)
    return Path(__file__).resolve().parent

def _resolve_json_path() -> Path:
    # 1) ให้ ENV ชี้พาธได้ (ถ้าตั้ง)
    env = os.getenv("PROMPT_JSON_PATH", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    # 2) ค่าดีฟอลต์: ใช้ไฟล์ที่วาง "ข้างๆ" โมดูลนี้ใน src/
    return _module_dir() / "prompts.json"

def _normalize_prompts(data, tag_filter: str | None = None) -> list[str]:
    """
    แปลง JSON หลายรูปแบบ -> list[str] (เฉพาะ 'text')
      1) list[str]
      2) {"prompts": list[str]}
      3) {"schema_version": "...", "prompts": [ {id, text, author?, tags?}, ... ]}
    """
    if isinstance(data, list):
        if not all(isinstance(x, str) for x in data):
            raise PromptSourceError("List format must contain only strings.")
        return data

    if isinstance(data, dict):
        prompts = data.get("prompts")
        if prompts is None:
            raise PromptSourceError("Key 'prompts' not found in JSON.")

        if isinstance(prompts, list) and all(isinstance(x, str) for x in prompts):
            return prompts

        if isinstance(prompts, list) and all(isinstance(x, dict) for x in prompts):
            items = prompts
            if tag_filter:
                k = tag_filter.lower()
                filtered = [it for it in items
                            if any(isinstance(t, str) and t.lower() == k for t in (it.get("tags") or []))]
                if filtered:
                    items = filtered
            result = [it.get("text") for it in items if isinstance(it.get("text"), str) and it.get("text").strip()]
            if not result:
                raise PromptSourceError("No valid 'text' in prompts array.")
            return result

    raise PromptSourceError("Unsupported JSON format.")

def load_from_json(path: str | None = None) -> list[str]:
    p = Path(path).expanduser().resolve() if path else _resolve_json_path()
    if not p.exists():
        raise PromptSourceError(f"JSON not found: {p}")
    with p.open(encoding="utf-8") as f:
        raw = json.load(f)
    tag_filter = os.getenv("PROMPT_TAG", "").strip() or None
    return _normalize_prompts(raw, tag_filter)

def get_random_prompt() -> str:
    # จะอ่าน src/prompts.json โดยอัตโนมัติ (หรือใช้ PROMPT_JSON_PATH ถ้าตั้ง)
    prompts = load_from_json()
    return random.choice(prompts)
