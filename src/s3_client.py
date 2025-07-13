import os
import json
import boto3
from botocore.exceptions import ClientError

class S3Client:
    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET_NAME")
        self.key = os.getenv("S3_KEY_TASKS_JSON")
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

    def load_json(self) -> dict:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=self.key)
            print("✅ tasks.json をS3から読み込みました")
            return json.loads(obj['Body'].read())
        except self.s3.exceptions.NoSuchKey:
            return {}
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return {}
            raise

    def save_json(self, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2)
        self.s3.put_object(Bucket=self.bucket, Key=self.key, Body=body.encode('utf-8'))
        print("✅ tasks.json をS3に保存しました")
