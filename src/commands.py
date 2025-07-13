import discord
from discord import app_commands, Interaction
from views import ConfirmView
from tasks import TaskRepository
import os

# TaskRepositoryのインスタンス
task_repository = TaskRepository()

#Bot独自のスラッシュコマンドを指定できる
@app_commands.command(name="declare_task", description="今日やることを宣言しよう！")
@app_commands.describe(today_task="今日やること")
async def declare_task(interaction: Interaction, today_task: str):
    user_id = str(interaction.user.id)

    # タスク永続化
    task_repository.save_tasks(user_id, today_task)

    # ボタン作る
    view = ConfirmView(user_id, task_repository)

    # レスポンス
    await interaction.response.send_message(
        f"📝 『{today_task}』 を今日のやることに登録したよ！達成できたらボタン押してね👇",
        view=view
    )

@app_commands.command(name="init_channel", description="Botと会話するチャンネルを設定します")
@app_commands.describe(channel="設定したいチャンネル")
async def init_channel(interaction: Interaction, channel: discord.TextChannel):
    # 環境変数を更新（実際の実装ではデータベースや設定ファイルを使用することを推奨）
    os.environ["INITIAL_CHANNEL_ID"] = str(channel.id)

    await interaction.response.send_message(
        f"✅ 初期チャンネルを {channel.mention} に設定しました！\n"
        f"Botが再起動すると、このチャンネルに最初のメッセージが送信されます。",
        ephemeral=True
    )
