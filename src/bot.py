import uuid
import discord
from discord.ext import commands
from dotenv import load_dotenv
from task_repository import TaskRepository
import os

from scheduler import start_scheduler
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
    print("✅ スラッシュコマンドを同期しました")
    print(f"✅ 1action ready!")
    # Botが最初に問いかけてくるチャンネルにメッセージを送信
    # initial_channel = bot.get_channel(INITIAL_CHANNEL_ID)
    # if initial_channel and isinstance(initial_channel, discord.TextChannel):
    #     await initial_channel.send("👋 1action Botがこのチャンネルで起動しました！ 時間になったら、TODOお聞きしますね。")
    #     print(f"✅ 初期メッセージをチャンネル {initial_channel.name} に送信しました")

    # start_scheduler(bot, CHANNEL_ID)

# スラッシュコマンドを登録
bot.tree.add_command(declare_task)
bot.tree.add_command(init_channel)
print("✅ スラッシュコマンドを登録しました")

bot.run(TOKEN)
