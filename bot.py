from datetime import date
import os
import discord
from dotenv import load_dotenv
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Bot生成
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# スケジューラ
scheduler = AsyncIOScheduler()

user_tasks = {}  # ユーザーIDをキーにしたやることメモ

@bot.event
async def on_ready():
    print(f"1action get ready!!!")
    await bot.tree.sync()
    scheduler.add_job(send_morning_message, CronTrigger(hour=11, minute=17, timezone='Asia/Tokyo'))
    scheduler.start()

async def send_morning_message():
    channel = bot.get_channel(CHANNEL_ID)
    guild = channel.guild
    for member in guild.members:
        if member.bot:
            continue
        await channel.send(f"{member.mention} おはよう☀ 今日のやることを `/declare` で教えてね！")

def today_key():
    return date.today().isoformat()

# Bot専用のスラッシュコマンドを指定できる
@bot.tree.command(name="declare", description="今日やることを宣言しよう！")
@app_commands.describe(task="今日やること")
async def declare(interaction: Interaction, task: str):
    uid = interaction.user.id
    today = today_key()

    if uid not in user_tasks:
        user_tasks[uid] = {}
    user_tasks[uid][today] = task

    view = ConfirmView(uid, today)
    await interaction.response.send_message(
        f"📝 『{task}』 を今日のやることに登録したよ！達成できたらボタン押してね👇",
        view=view
    )

from discord.ui import View, Button

class ConfirmView(View):
    def __init__(self, user_id, date_key):
        super().__init__(timeout=86400)  # 1日有効
        self.user_id = user_id
        self.date_key = date_key

    @discord.ui.button(label="OK！やったよ", style=ButtonStyle.success)
    async def confirm(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなた専用のボタンだよ！", ephemeral=True)
            return

        task = user_tasks.get(self.user_id, {}).get(self.date_key)
        if task:
            await interaction.response.send_message(f"🎉 お疲れ様！『{task}』完了したね！", ephemeral=True)
        else:
            await interaction.response.send_message("❓ 今日のやることが未登録みたい！", ephemeral=True)

bot.run(TOKEN)
