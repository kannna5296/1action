# Python 3.13ベースイメージ（debianベース）
FROM python:3.13-slim

# 必要なパッケージのインストール
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

# 依存関係のインストール
COPY requirements.txt .
RUN pip install -r requirements.txt
