#!/bin/sh

# 成功判定（importできるか）
if python -c "import discord" > /dev/null 2>&1; then
  echo "[HealthCheck] OK: discord module available"
  exit 0
else
  echo "[HealthCheck] ERROR: discord module not available" >&2
  exit 1
fi
