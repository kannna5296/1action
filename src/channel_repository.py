from s3_client import S3Client

class ChannelRepository:
    def __init__(self, server_id: str):
        self.file_name = f"{server_id}_channel.json"
        self.client = S3Client()

    def load(self) -> list:
        data = self.client.load_json(self.file_name)
        # channelsキーがなければ空リスト
        return data.get("channels", []) if isinstance(data, dict) else []

    def save(self, channel_id: int) -> None:
        data = self.client.load_json(self.file_name)
        if not isinstance(data, dict):
            data = {}
        channels = data.get("channels", [])
        if channel_id not in channels:
            channels.append(channel_id)
        data["channels"] = channels
        self.client.save_json(data, self.file_name)
