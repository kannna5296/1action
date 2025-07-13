# Python 3.13ベースイメージ（debianベース）
FROM python:3.13-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    curl git build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ作成
WORKDIR /workspace

# pip最新版
RUN pip install --upgrade pip

# devcontainer実行時に requirements.txt からインストールされる
