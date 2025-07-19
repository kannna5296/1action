from s3_client import S3Client
from typing import Optional

class ChannelRepository:
    FILE_NAME = "channels.json"

    def __init__(self):
        self.client = S3Client()

    def load(self, server_id: str) -> Optional[int]:
        data = self.client.load_json(self.FILE_NAME)
        return data.get(str(server_id)) if isinstance(data, dict) else None

    def save(self, server_id: str, channel_id: int) -> None:
        data = self.client.load_json(self.FILE_NAME)
        if not isinstance(data, dict):
            data = {}
        data[str(server_id)] = channel_id
        self.client.save_json(data, self.FILE_NAME)
