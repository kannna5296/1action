import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from discord.ext.commands import Bot
from discord import TextChannel

def start_scheduler(bot: Bot, channel_id: int):
    scheduler = AsyncIOScheduler()

    async def send_morning_message():
        channel = bot.get_channel(channel_id)
        if not isinstance(channel, TextChannel):
            return

        guild = channel.guild
        for member in guild.members:
            print(member)
            if member.bot:
                continue
            await channel.send(f"{member.mention} おはよう☀ 今日のやることを `/declare` で教えてね！")
            print("やること確認を通知しました！")

    # 環境変数からスケジューラー設定を取得
    scheduler_type = os.getenv("SCHEDULER_TYPE", "cron").lower()

    if scheduler_type == "interval":
        # Interval型の場合
        interval_minutes = int(os.getenv("INTERVAL_MINUTES", "60"))
        scheduler.add_job(
            send_morning_message,
            IntervalTrigger(minutes=interval_minutes, timezone="Asia/Tokyo")
        )
        print(f"✅ Interval型スケジューラーを設定しました（{interval_minutes}分間隔）")
    else:
        # Cron型の場合（デフォルト）
        cron_time = os.getenv("CRON_TIME", "7,30")
        hour, minute = map(int, cron_time.split(","))
        scheduler.add_job(
            send_morning_message,
            CronTrigger(hour=hour, minute=minute, timezone="Asia/Tokyo")
        )
        print(f"✅ Cron型スケジューラーを設定しました 日本時間（{hour}時{minute}分）")

    scheduler.start()
