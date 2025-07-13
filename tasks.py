from datetime import date

# 一時的にメモリに保持（のちにJSONやDBに）
user_tasks = {}

def today_key():
    return date.today().isoformat()
