import json
import os
from date_util import today_key
import boto3
from botocore.exceptions import ClientError

class TaskRepository:
    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET_NAME")
        self.key = os.getenv("S3_KEY_TASKS_JSON")
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

    def load_tasks(self) -> dict:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=self.key)
            return json.loads(obj['Body'].read())
        except self.s3.exceptions.NoSuchKey:
            return {}
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return {}
            raise

    def save_tasks(self, user_id: str, today_task: str) -> None:
        user_tasks = self.load_tasks()
        if user_id not in user_tasks:
            user_tasks[user_id] = {}
        user_tasks[user_id][today_key()] = today_task
        data = json.dumps(user_tasks, ensure_ascii=False, indent=2)
        self.s3.put_object(Bucket=self.bucket, Key=self.key, Body=data.encode('utf-8'))
        print("✅ tasks.json をS3に保存しました")
