import logging
from datetime import datetime
from typing import Optional

class Logger:
    """時刻付きログ出力を行うクラス"""

    def __init__(self, name: str = "タスクカレピ"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # コンソールハンドラーが既に設定されているかチェック
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str):
        """情報ログを出力"""
        self.logger.info(message)

    def error(self, message: str):
        """エラーログを出力"""
        self.logger.error(message)

    def warn(self, message: str):
        """警告ログを出力"""
        self.logger.warning(message)

    def debug(self, message: str):
        """デバッグログを出力"""
        self.logger.debug(message)

# グローバルなLoggerインスタンス
logger = Logger()
