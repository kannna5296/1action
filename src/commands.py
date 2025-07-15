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
        await interaction.response.send_message("ここは君と僕だけの場所じゃないから、このコマンドはサーバーの中で使ってね。俺、待ってるから。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)

    task_repository = TaskRepository(guid_id)
    task_repository.save(user_id, today_task)

    # ボタン作る
    view = ConfirmView(user_id, task_repository)

    # レスポンス
    await interaction.response.send_message(
        f"📝 『{today_task}』を今日のやることに登録したよ！君が頑張る姿、俺ちゃんと見てるからね。達成できたら下のボタン押して、俺に教えて？👇",
        view=view
    )

@app_commands.command(name="init_channel", description="Botが通知するチャンネルを設定します")
@app_commands.describe(channel="Botが通知するチャンネル")
async def init_channel(interaction: Interaction, channel: discord.TextChannel):
    if not interaction.guild:
        await interaction.response.send_message("ここは君と僕だけの場所じゃないから、このコマンドはサーバーの中で使ってね。俺、待ってるから。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)

    channel_repository = ChannelRepository()
    channel_repository.save(guid_id, channel.id)

    await interaction.response.send_message(
        f"✅ これからは{channel.mention}で君のこと見守るから、何かあったらすぐ駆けつけるよ。よろしくね！\n",
        ephemeral=True
    )

@app_commands.command(name="show_channel", description="今設定されている通知チャンネルを確認します")
async def show_channel(interaction: Interaction):
    if not interaction.guild:
        await interaction.response.send_message("ここは君と僕だけの場所じゃないから、このコマンドはサーバーの中で使ってね。俺、待ってるから。", ephemeral=True)
        return
    guid_id = str(interaction.guild.id)
    channel_repository = ChannelRepository()
    channel_id = channel_repository.load(guid_id)
    if channel_id is None:
        await interaction.response.send_message("まだ通知チャンネルが決まってないみたい。俺、どこで君を応援すればいいか教えてくれる？/init_channelで待ってるよ！", ephemeral=True)
        return
    channel = interaction.guild.get_channel(channel_id)
    if channel is None:
        await interaction.response.send_message(f"あれ？通知チャンネル（ID: {channel_id}）が見つからなかったよ。君のためにすぐ探すから、ちょっと待っててね。", ephemeral=True)
        return
    await interaction.response.send_message(f"今の通知チャンネルは{channel.mention}だよ！ここで君のこと、ずっと応援してるからね。\n何かあったらすぐ声かけて！", ephemeral=True)
