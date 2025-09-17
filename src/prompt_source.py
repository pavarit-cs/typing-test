# prompt_source.py
import os, json, random
from pathlib import Path

# (ถ้าอยากใช้ API: pip install requests)
try:
    import requests
except ImportError:
    requests = None

class PromptSourceError(Exception):
    pass

def _validate_and_pick(data):
    """รองรับ 2 รูปแบบ: list[str] หรือ {prompts: list[str]}"""
    if isinstance(data, list):
        prompts = data
    elif isinstance(data, dict) and isinstance(data.get("prompts"), list):
        prompts = data["prompts"]
    else:
        raise PromptSourceError("Unsupported JSON format. Expect list or {'prompts': [...]}.")

    if not prompts:
        raise PromptSourceError("Empty prompts.")
    # ตรวจว่าเป็นสตริงล้วน
    if not all(isinstance(x, str) for x in prompts):
        raise PromptSourceError("Prompts must be list of strings.")
    return prompts

def load_from_json(path="data/prompts.json"):
    p = Path(path)
    if not p.exists():
        raise PromptSourceError(f"JSON not found: {path}")
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    return _validate_and_pick(data)

def load_from_api(url, timeout=5):
    if requests is None:
        raise PromptSourceError("requests not installed. `pip install requests`")
    if not url:
        raise PromptSourceError("PROMPT_API_URL not set.")
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return _validate_and_pick(r.json())

def get_random_prompt():
    """
    เลือกแหล่งข้อมูลตาม ENV:
      PROMPT_SOURCE = 'json' (default) | 'api'
      PROMPT_JSON_PATH = path ไปยังไฟล์ (default: data/prompts.json)
      PROMPT_API_URL   = URL ของ API ที่คืน list หรือ {prompts: list}
    ถ้า API ล่ม จะ fallback เป็น JSON อัตโนมัติ (ถ้ามี)
    """
    mode = os.getenv("PROMPT_SOURCE", "json").lower()
    json_path = os.getenv("PROMPT_JSON_PATH", "data/prompts.json")
    api_url = os.getenv("PROMPT_API_URL", "")

    prompts = None
    error_msgs = []

    if mode == "api":
        try:
            prompts = load_from_api(api_url)
        except Exception as e:
            error_msgs.append(f"[API failed] {e}")
            # fallback หา JSON ต่อ
            try:
                prompts = load_from_json(json_path)
                error_msgs.append(f"[Fallback to JSON] {json_path}")
            except Exception as e2:
                error_msgs.append(f"[JSON failed] {e2}")

    else:  # json mode
        try:
            prompts = load_from_json(json_path)
        except Exception as e:
            error_msgs.append(f"[JSON failed] {e}")
            # optional: ถ้าอยากลอง API ต่อ
            if api_url:
                try:
                    prompts = load_from_api(api_url)
                    error_msgs.append(f"[Fallback to API] {api_url}")
                except Exception as e2:
                    error_msgs.append(f"[API failed] {e2}")

    if not prompts:
        raise PromptSourceError("No prompt source available:\n" + "\n".join(error_msgs))

    return random.choice(prompts)
