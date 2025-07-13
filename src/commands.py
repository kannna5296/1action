import discord
from discord import app_commands, Interaction
from views import ConfirmView
from task_repository import TaskRepository
from channel_repository import ChannelRepository

#Bot独自のスラッシュコマンドを指定できる
@app_commands.command(name="declare_task", description="今日やることを宣言しよう！")
@app_commands.describe(today_task="今日やること")
async def declare_task(interaction: Interaction, today_task: str):
    user_id = str(interaction.user.id)
    if not interaction.guild:
        await interaction.response.send_message("このコマンドはサーバ内でのみ使用できます。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)

    task_repository = TaskRepository(guid_id)
    task_repository.save(user_id, today_task)

    # ボタン作る
    view = ConfirmView(user_id, task_repository)

    # レスポンス
    await interaction.response.send_message(
        f"📝 『{today_task}』 を今日のやることに登録したよ！達成できたらボタン押してね👇",
        view=view
    )

@app_commands.command(name="init_channel", description="Botが通知するチャンネルを設定します")
@app_commands.describe(channel="Botが通知するチャンネル")
async def init_channel(interaction: Interaction, channel: discord.TextChannel):
    if not interaction.guild:
        await interaction.response.send_message("このコマンドはサーバ内でのみ使用できます。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)

    channel_repository = ChannelRepository()
    channel_repository.save(guid_id, channel.id)

    await interaction.response.send_message(
        f"✅ Botの通知チャンネルを {channel.mention} に設定しました！\n",
        ephemeral=True
    )

@app_commands.command(name="show_channel", description="今設定されている通知チャンネルを確認します")
async def show_channel(interaction: Interaction):
    if not interaction.guild:
        await interaction.response.send_message("このコマンドはサーバ内でのみ使用できます。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)
    channel_repository = ChannelRepository()
    channel_id = channel_repository.load(guid_id)
    if channel_id is None:
        await interaction.response.send_message("通知チャンネルはまだ設定されていません。/init_channel で設定してください！", ephemeral=True)
        return
    channel = interaction.guild.get_channel(channel_id)
    if channel is None:
        await interaction.response.send_message(f"通知チャンネル（ID: {channel_id}）は見つかりませんでした。", ephemeral=True)
        return
    await interaction.response.send_message(f"現在の通知チャンネルは {channel.mention} です！\nこのチャンネルにBotから投稿が飛んできます。", ephemeral=True)
