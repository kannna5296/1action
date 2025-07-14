# Python 3.13ベースイメージ
FROM python:3.13-slim

# 非rootユーザーを作成
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 作業ディレクトリ設定
WORKDIR /app

# タイムゾーン設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# システムパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip最新版にアップグレード
RUN pip install --upgrade pip

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY src/ ./src/
COPY pyproject.toml .

# ファイルの所有者を変更
RUN chown -R appuser:appuser /app

# 非rootユーザーに切り替え
USER appuser

# 環境変数設定
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# ヘルスチェック
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /healthcheck.sh

# アプリケーション起動
CMD ["python", "-m", "src.bot"]
