import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.tasks import TaskRepository


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

    def test_save_tasks_new_user(self):
        """新規ユーザーのタスク保存をテスト"""
        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            test_data_file = Path(temp_dir) / "tasks.json"
            task_repository = TaskRepository(str(test_data_file))

            # today_key()をモックして固定値を返すようにする
            with patch('src.tasks.today_key', return_value="2024-01-15"):
                # 新規ユーザーのタスクを保存
                user_id = "12345"
                today_task = "新しいタスク"
                task_repository.save_tasks(user_id, today_task)

                # 保存されたJSONファイルを直接読み込んで確認
                with open(test_data_file, "r", encoding="UTF-8") as f:
                    saved_data = json.load(f)

                # 期待されるJSON構造
                expected_data = {
                    "12345": {
                        "2024-01-15": "新しいタスク"
                    }
                }

                # JSONの内容を直接比較
                assert saved_data == expected_data

    def test_save_tasks_existing_user(self):
        """既存ユーザーのタスク保存をテスト"""
        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            test_data_file = Path(temp_dir) / "tasks.json"
            task_repository = TaskRepository(str(test_data_file))

            # 既存のデータを作成
            existing_data = {
                "12345": {
                    "2024-01-15": "既存のタスク"
                }
            }
            with open(test_data_file, "w", encoding="UTF-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            # today_key()をモックして固定値を返すようにする
            with patch('src.tasks.today_key', return_value="2024-01-16"):
                # 同じユーザーの新しいタスクを保存
                user_id = "12345"
                today_task = "新しいタスク"
                task_repository.save_tasks(user_id, today_task)

                # 保存されたJSONファイルを直接読み込んで確認
                with open(test_data_file, "r", encoding="UTF-8") as f:
                    saved_data = json.load(f)

                # 期待されるJSON構造（既存のタスクも残る）
                expected_data = {
                    "12345": {
                        "2024-01-15": "既存のタスク",
                        "2024-01-16": "新しいタスク"
                    }
                }

                # JSONの内容を直接比較
                assert saved_data == expected_data

    def test_save_tasks_multiple_users(self):
        """複数ユーザーのタスク保存をテスト"""
        # 一時的なディレクトリでテスト
        with tempfile.TemporaryDirectory() as temp_dir:
            test_data_file = Path(temp_dir) / "tasks.json"
            task_repository = TaskRepository(str(test_data_file))

            # today_key()をモックして固定値を返すようにする
            with patch('src.tasks.today_key', return_value="2024-01-15"):
                # 複数ユーザーのタスクを保存
                task_repository.save_tasks("12345", "ユーザー1のタスク")
                task_repository.save_tasks("67890", "ユーザー2のタスク")

                # 保存されたJSONファイルを直接読み込んで確認
                with open(test_data_file, "r", encoding="UTF-8") as f:
                    saved_data = json.load(f)

                # 期待されるJSON構造
                expected_data = {
                    "12345": {
                        "2024-01-15": "ユーザー1のタスク"
                    },
                    "67890": {
                        "2024-01-15": "ユーザー2のタスク"
                    }
                }

                # JSONの内容を直接比較
                assert saved_data == expected_data
