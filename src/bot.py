import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from scheduler import start_scheduler
from commands import declare_task, init_channel

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID_STR = os.getenv("CHANNEL_ID")
# Botが最初に問いかけてくるチャンネルID（オプション）
INITIAL_CHANNEL_ID_STR = os.getenv("INITIAL_CHANNEL_ID")

if not TOKEN or not CHANNEL_ID_STR:
    raise ValueError("Required environment variables not set")
CHANNEL_ID = int(CHANNEL_ID_STR)
INITIAL_CHANNEL_ID = int(INITIAL_CHANNEL_ID_STR) if INITIAL_CHANNEL_ID_STR else CHANNEL_ID

@bot.event
async def on_ready():
    print(f"✅ 1action ready!")

    # 登録されているコマンドを確認
    print(f"登録されているコマンド: {[cmd.name for cmd in bot.tree.get_commands()]}")

    # スラッシュコマンドを同期（コマンド登録後に実行）
    await bot.tree.sync()
    print("✅ スラッシュコマンドを同期しました")

    # Botが最初に問いかけてくるチャンネルにメッセージを送信
    initial_channel = bot.get_channel(INITIAL_CHANNEL_ID)
    if initial_channel and isinstance(initial_channel, discord.TextChannel):
        await initial_channel.send("👋 1action Botがこのチャンネルで起動しました！ 時間になったら、TODOお聞きしますね。")
        print(f"✅ 初期メッセージをチャンネル {initial_channel.name} に送信しました")

    start_scheduler(bot, CHANNEL_ID)

# スラッシュコマンドを登録
bot.tree.add_command(declare_task)
bot.tree.add_command(init_channel)
print("✅ スラッシュコマンドを登録しました")

bot.run(TOKEN)
