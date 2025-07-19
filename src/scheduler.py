import traceback
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from discord.ext.commands import Bot
from discord import TextChannel
from morning_message import message_list
import random

from repository.channel_repository import ChannelRepository
from config import Config
from logger import logger

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.repo = ChannelRepository()

    # IFで設計できそう
    def start(self):
        scheduler_type = Config.get("SCHEDULER_TYPE", "cron").lower()
        env = Config.get("ENVIRONMENT", "prod").lower()
        send_method = self.send_morning_message_local if env == "local" else self.send_morning_message

        scheduler_type = Config.get("SCHEDULER_TYPE", "cron").lower()
        if scheduler_type == "interval":
            interval_minutes = int(Config.get("INTERVAL_MINUTES", "60"))
            self.scheduler.add_job(
                send_method,
                IntervalTrigger(minutes=interval_minutes, timezone="Asia/Tokyo")
            )
            logger.info(f"Interval型スケジューラーを設定しました（{interval_minutes}分間隔）")
        else:
            cron_time = Config.get("CRON_TIME", "7,30")
            hour, minute = map(int, cron_time.split(","))
            self.scheduler.add_job(
                send_method,
                CronTrigger(hour=hour, minute=minute, timezone="Asia/Tokyo")
            )
            logger.info(f"Cron型スケジューラーを設定しました 日本時間（{hour}時{minute}分）")
        self.scheduler.start()

    async def send_morning_message(self):
        try:
            for guild in self.bot.guilds:
                logger.info(f"サーバID {guild.id} について、タスク確認通知を開始します")
                channel_id = self.repo.load(str(guild.id))
                if channel_id is None:
                    logger.info("チャンネルIDが設定されていないので、処理をスキップしました")
                    continue
                channel = self.bot.get_channel(channel_id)
                if not isinstance(channel, TextChannel):
                    continue
                for member in guild.members:
                    if member.bot:
                        continue
                    list = random.choice(message_list)
                    await channel.send(list["message"].replace("{member.mention}", str(member.mention)))
                    logger.info(f"{member.id} に今日のタスク確認通知を行いました")

        except Exception as e:
            logger.error("定時通知送信でエラーが起きました " + str(e))
            traceback.print_exc()

    async def send_morning_message_local(self):
        guild_id = Config.get("LOCAL_GUILD_ID", "").lower()
        member_id = Config.get("LOCAL_MEMBER_ID", "").lower()
        logger.info(f"サーバID {guild_id} について、タスク確認通知を開始します")
        channel_id = self.repo.load(str(guild_id))
        if channel_id is None:
            logger.info("チャンネルIDが設定されていないので、処理をスキップしました")
            return
        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, TextChannel):
            return
        await channel.send("[開発用] /declare_taskで今日のTODO報告をお願いします")
        logger.info(f"{member_id} に今日のタスク確認通知を行いました")
