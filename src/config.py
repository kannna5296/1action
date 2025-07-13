import os

class Config:
    @staticmethod
    def get(key: str, default=None):
        value = os.environ.get(key, default)
        if value is None:
            raise ValueError(f"環境変数 {key} が設定されていません")
        return value

    @staticmethod
    def validate():
        required_keys = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "DISCORD_BOT_TOKEN",
            # 必要に応じて追加
        ]
        for key in required_keys:
            if not os.environ.get(key):
                raise EnvironmentError(f"必須環境変数 {key} が未設定です")
