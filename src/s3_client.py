import os
import json
import boto3
from botocore.exceptions import ClientError
from config import Config
from logger import logger

class S3Client:
    def __init__(self):
        self.bucket = "1action"
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=Config.get("AWS_SECRET_ACCESS_KEY"),
            region_name="ap-northeast-1",
        )

    def load_json(self, key: str) -> dict:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            logger.info(f"{key} をS3から読み込みました")
            return json.loads(obj['Body'].read())
        except self.s3.exceptions.NoSuchKey:
            logger.info(f"{key} をS3から読み込みました (Keyがなかったです)")
            return {}
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.info(f"{key} をS3から読み込みました (Keyがなかったです)")
                return {}
            logger.error(f"{key} をS3から読み込めませんでした: {str(e)}")
            raise

    def save_json(self, data: dict, key: str) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2)
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=body.encode('utf-8'))
        logger.info(f"{key} をS3に保存しました")
