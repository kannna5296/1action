import json
from pathlib import Path
import os

# タスクはJSONで永続化する
DATA_FILE = Path("tasks.json")

def load_tasks() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tasks(user_tasks: dict) -> None:
    with open(DATA_FILE, "w", encoding="UTF-8") as f:
        json.dump(user_tasks, f, ensure_ascii=False, indent=2)
    print("✅ tasks.json に保存しました")  # ← これを入れる
