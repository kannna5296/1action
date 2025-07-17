import uuid
import discord
from discord.ext import commands
from dotenv import load_dotenv

from healthcheck import HealthCheckServer
from scheduler import Scheduler
from commands import declare_task, init_channel, show_channel
from config import Config
from logger import logger

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    await bot.tree.sync()
    scheduler = Scheduler(bot)
    scheduler.start()
    logger.info(f"✅ タスクカレピ ready!")

config = Config()
# スラッシュコマンドを登録
bot.tree.add_command(declare_task)
bot.tree.add_command(init_channel)
bot.tree.add_command(show_channel)

# ヘルスチェック用のサーバをたてる（Koyeb仕様に沿う)
server = HealthCheckServer()
server.start()

#　Bot開始
bot.run(Config.get("DISCORD_BOT_TOKEN", ""))
