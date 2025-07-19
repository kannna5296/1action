夢のない話はこちら

## ディレクトリ構成

```
.
├── src/
│   ├── bot.py                # エントリーポイント
│   ├── commands.py           # スラッシュコマンド定義
│   ├── scheduler.py          # 定期通知・スケジューラー
│   ├── s3_client.py          # S3永続化クライアント
│   ├── channel_repository.py # チャンネル設定管理
│   ├── task_repository.py    # タスク管理
│   ├── config.py             # 環境変数一元管理
│   ├── logger.py             # ロギング
│   ├── views.py              # Discord UI拡張
│   └── date_util.py          # 日付ユーティリティ
├── requirements.txt
├── env.example
├── Dockerfile
├── test/
│   └── test_tasks.py         # タスク管理のテスト
```

---

## セットアップ

### 1. 必要な環境変数

`.env.example` を参考に `.env` を作成し、各種トークンやIDを設定してください。

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
CHANNEL_ID=1234567890123456789
INITIAL_CHANNEL_ID=1234567890123456789
SCHEDULER_TYPE=cron
CRON_TIME=7,30
INTERVAL_MINUTES=60
NOTIFY_USER_IDS=1234567890123456789,9876543210987654321
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

- **DISCORD_BOT_TOKEN**: Discord Botのトークン
- **CHANNEL_ID**: 通知用チャンネルID
- **AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY**: S3永続化用のAWS認証情報
- その他、スケジューラーや通知ユーザーの設定も可能

### 2. 依存パッケージのインストール

```sh
pip install -r requirements.txt
```

### 3. Botの起動

```sh
python -m src.bot
```

---

## Dockerでの利用

```sh
docker build -t 1action-bot .
docker run --env-file .env 1action-bot
```