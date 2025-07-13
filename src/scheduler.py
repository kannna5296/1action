import os
import traceback
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from discord.ext.commands import Bot
from discord import TextChannel

from channel_repository import ChannelRepository
from config import Config

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    async def send_morning_message(self):
        try:
            for guild in self.bot.guilds:
                repo = ChannelRepository(str(guild.id))
                channel_ids = repo.load()
                for channel_id in channel_ids:
                    channel = self.bot.get_channel(channel_id)
                    if not isinstance(channel, TextChannel):
                        continue
                    for member in guild.members:
                        if member.bot:
                            continue
                        await channel.send(f"{member.mention} おはよう☀ 今日のやることを `/declare_task` で教えてね！")
        except Exception as e:
            traceback.print_exc()

    def start(self):
        scheduler_type = Config.get("SCHEDULER_TYPE", "cron").lower()
        if scheduler_type == "interval":
            interval_minutes = int(Config.get("INTERVAL_MINUTES", "60"))
            self.scheduler.add_job(
                self.send_morning_message,
                IntervalTrigger(minutes=interval_minutes, timezone="Asia/Tokyo")
            )
            print(f"✅ Interval型スケジューラーを設定しました（{interval_minutes}分間隔）")
        else:
            cron_time = Config.get("CRON_TIME", "7,30")
            hour, minute = map(int, cron_time.split(","))
            self.scheduler.add_job(
                self.send_morning_message,
                CronTrigger(hour=hour, minute=minute, timezone="Asia/Tokyo")
            )
            print(f"✅ Cron型スケジューラーを設定しました 日本時間（{hour}時{minute}分）")
        self.scheduler.start()
