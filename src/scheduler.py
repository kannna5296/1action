import os
import traceback
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from discord.ext.commands import Bot
from discord import TextChannel

from channel_repository import ChannelRepository
from config import Config
from logger import logger

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    async def send_morning_message(self):
        try:
            repo = ChannelRepository()
            for guild in self.bot.guilds:
                channel_id = repo.load(str(guild.id))
                if channel_id is None:
                    continue
                channel = self.bot.get_channel(channel_id)
                if not isinstance(channel, TextChannel):
                    continue
                for member in guild.members:
                    if member.bot:
                        continue
                    await channel.send(f"{member.mention} おはよう☀ 今日も君のこと応援してるよ。やること決まったら `/declare_task` で俺に教えて？君の頑張り、ちゃんと見てるからね！")
        except Exception as e:
            logger.error("定時通知送信でエラーが起きました " + str(e))
            traceback.print_exc()

    def start(self):
        scheduler_type = Config.get("SCHEDULER_TYPE", "cron").lower()
        if scheduler_type == "interval":
            interval_minutes = int(Config.get("INTERVAL_MINUTES", "60"))
            self.scheduler.add_job(
                self.send_morning_message,
                IntervalTrigger(minutes=interval_minutes, timezone="Asia/Tokyo")
            )
            logger.info(f"Interval型スケジューラーを設定しました（{interval_minutes}分間隔）")
        else:
            cron_time = Config.get("CRON_TIME", "7,30")
            hour, minute = map(int, cron_time.split(","))
            self.scheduler.add_job(
                self.send_morning_message,
                CronTrigger(hour=hour, minute=minute, timezone="Asia/Tokyo")
            )
            logger.info(f"Cron型スケジューラーを設定しました 日本時間（{hour}時{minute}分）")
        self.scheduler.start()
