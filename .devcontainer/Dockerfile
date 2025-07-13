# Python 3.13ベースイメージ（開発用）
FROM python:3.13-slim

# 必要なパッケージのインストール（開発用）
RUN apt-get update && apt-get install -y \
    curl git build-essential tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ作成
WORKDIR /workspace

# pip最新版
RUN pip install --upgrade pip

# 開発用の依存関係をインストール（requirements.txtは後でコピー）
COPY ../requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# 開発用の設定
# - 非rootユーザーは作成しない（開発環境では不要）
# - ヘルスチェックは不要
# - CMDは不要（devcontainerが管理）
