import uuid
import discord
from discord.ext import commands
from dotenv import load_dotenv
from task_repository import TaskRepository
import os

from scheduler import Scheduler
from commands import declare_task, init_channel

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Required environment variables not set")

@bot.event
async def on_ready():
    await bot.tree.sync()
    scheduler = Scheduler(bot)
    scheduler.start()
    print(f"✅ 1action ready!")

# スラッシュコマンドを登録
bot.tree.add_command(declare_task)
bot.tree.add_command(init_channel)

bot.run(TOKEN)
