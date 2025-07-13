import json
import os
from date_util import today_key

class TaskRepository:
    def __init__(self, data_file: str ="tasks.json"):
        self.data_file = data_file

    def load_tasks(self) -> dict:
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="UTF-8") as f:
                return json.load(f)
        return {}

    def save_tasks(self, user_id: str, today_task: str) -> None:
        user_tasks = self.load_tasks()

        # 初めてのユーザのためにobject化
        if user_id not in user_tasks:
            user_tasks[user_id] = {}
        user_tasks[user_id][today_key()] = today_task

        with open(self.data_file, "w", encoding="UTF-8") as f:
            json.dump(user_tasks, f, ensure_ascii=False, indent=2)
        print("✅ tasks.json に保存しました")  # ← これを入れる
