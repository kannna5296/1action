import json
from pathlib import Path
import os
from date_util import today_key

# タスクはJSONで永続化する
DATA_FILE = Path("tasks.json")

def load_tasks() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tasks(user_id: int, today_task: str) -> None:

    user_tasks = load_tasks()

    # 初めてのユーザのためにobject化
    if user_id not in user_tasks:
        user_tasks[user_id] = {}
    user_tasks[user_id][today_key()] = today_task

    with open(DATA_FILE, "w", encoding="UTF-8") as f:
        json.dump(user_tasks, f, ensure_ascii=False, indent=2)
    print("✅ tasks.json に保存しました")  # ← これを入れる
