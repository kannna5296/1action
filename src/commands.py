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

@app_commands.command(name="init_channel", description="Botと会話するチャンネルを設定します")
@app_commands.describe(channel="Botを設定したいチャンネル")
async def init_channel(interaction: Interaction, channel: discord.TextChannel):
    if not interaction.guild:
        await interaction.response.send_message("このコマンドはサーバ内でのみ使用できます。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)

    channel_repository = ChannelRepository(guid_id)
    channel_repository.save(channel.id)

    await interaction.response.send_message(
        f"✅ TODO確認チャンネルを {channel.mention} に設定しました！\n"
        f"Botが再起動すると、このチャンネルに最初のメッセージが送信されます。",
        ephemeral=True
    )
