import os
import discord
from dotenv import load_dotenv
from discord import app_commands
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
    await bot.tree.sync()
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

user_tasks = {}  # ユーザーIDをキーにしたやることメモ

# Bot専用のスラッシュコマンドを指定できる
@bot.tree.command(name="declare", description="今日やることを宣言しよう！")
@app_commands.describe(task="今日やること")
async def declare(interaction: discord.Interaction, task: str):
    user_tasks[interaction.user.id] = task
    await interaction.response.send_message(
        f"📝 やることを記録したよ！ → 「{task}」", ephemeral=True
    )

bot.run(TOKEN)
