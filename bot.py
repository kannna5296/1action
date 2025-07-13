import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# Bot生成
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# スケジューラ
scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"1action get ready!!!")
    scheduler.add_job(send_morning_message, CronTrigger(hour=7, minute=30))
    scheduler.start()

async def send_morning_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("おはようございます ☀️ 今日のやることをコメントしてね！")

# @client.event
# async def on_message(message):
#     """何か受信したメッセージに対して反応するアクション"""
#     #Bot自身からのメッセージには反応しない
#     if message.author == client.user :
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send('Hello!')

bot.run(TOKEN)
