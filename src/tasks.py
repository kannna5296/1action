from date_util import today_key
from s3_client import S3Client

class TaskRepository:
    def __init__(self, server_id: str):
        self.file_name = f"{server_id}_task.json"
        self.client = S3Client()

    def load_tasks(self) -> dict:
        return self.client.load_json(self.file_name)

    def save_tasks(self, user_id: str, today_task: str) -> None:
        user_tasks = self.load_tasks()
        if user_id not in user_tasks:
            user_tasks[user_id] = {}
        user_tasks[user_id][today_key()] = today_task
        self.client.save_json(user_tasks, self.file_name)
