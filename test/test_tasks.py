import pytest
import json
import tempfile
import os
from pathlib import Path
from tasks import TaskRepository


class TestTaskRepository:
    """TaskRepositoryクラスのテストクラス"""

    def test_load_tasks_when_file_not_exists(self):
        """ファイルが存在しない場合、空の辞書を返すことをテスト"""
        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            # テスト用のJSONファイルパスを設定
            test_data_file = Path(temp_dir) / "tasks.json"

            # ファイルが存在しないことを確認
            assert not test_data_file.exists()

            # TaskRepositoryのインスタンスを作成（テスト用パスを指定）
            task_repository = TaskRepository(str(test_data_file))

            # load_tasksを実行
            result = task_repository.load_tasks()

            # 空の辞書が返されることを確認
            assert result == {}

    def test_load_tasks_when_file_exists(self):
        """ファイルが存在する場合、正しくJSONを読み込むことをテスト"""
        # テスト用のJSONデータ
        test_data = {
            "user1": {
                "2024-01-15": "テストタスク1",
                "2024-01-16": "テストタスク2"
            },
            "user2": {
                "2024-01-15": "ユーザー2のタスク"
            }
        }

        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            test_data_file = Path(temp_dir) / "tasks.json"

            # テスト用のJSONファイルを作成（UTF-8で保存）
            with open(test_data_file, "w", encoding="UTF-8") as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)

            # ファイルが作成されたことを確認
            assert test_data_file.exists()

            # TaskRepositoryのインスタンスを作成（テスト用パスを指定）
            task_repository = TaskRepository(str(test_data_file))

            # load_tasksを実行
            result = task_repository.load_tasks()

            # 正しく読み込まれたことを確認
            assert result == test_data
            assert "user1" in result
            assert "user2" in result
            assert result["user1"]["2024-01-15"] == "テストタスク1"
            assert result["user2"]["2024-01-15"] == "ユーザー2のタスク"

    def test_load_tasks_with_empty_file(self):
        """空のJSONファイルの場合のテスト"""
        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            test_data_file = Path(temp_dir) / "tasks.json"

            # 空のJSONファイルを作成
            with open(test_data_file, "w", encoding="UTF-8") as f:
                json.dump({}, f)

            # TaskRepositoryのインスタンスを作成（テスト用パスを指定）
            task_repository = TaskRepository(str(test_data_file))

            # load_tasksを実行
            result = task_repository.load_tasks()

            # 空の辞書が返されることを確認
            assert result == {}
