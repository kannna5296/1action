import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from scheduler import start_scheduler
from commands import declare_command
from tasks import user_tasks

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

@bot.event
async def on_ready():
    print(f"✅ 1action ready!")
    await bot.tree.sync()
    start_scheduler(bot, CHANNEL_ID)

# スラッシュコマンドを登録
bot.tree.add_command(declare_command)

bot.run(TOKEN)
