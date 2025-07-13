from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

def start_scheduler(bot: Bot, channel_id: str):
    scheduler = AsyncIOScheduler()

    async def send_morning_message():
        print("起動してますよ")
        channel = bot.get_channel(channel_id)
        guild = channel.guild
        for member in guild.members:
            print(member)
            if member.bot:
                continue
            print("辿り着いた")
            await channel.send(f"{member.mention} おはよう☀ 今日のやることを `/declare` で教えてね！")

    scheduler.add_job(send_morning_message, CronTrigger(hour=11, minute=36, timezone="Asia/Tokyo"))
    scheduler.start()
