from discord import app_commands, Interaction
from views import ConfirmView
from tasks import save_tasks, load_tasks
from date_util import today_key

#Bot独自のスラッシュコマンドを指定できる
@app_commands.command(name="declare", description="今日やることを宣言しよう！")
@app_commands.describe(today_task="今日やること")
async def declare_command(interaction: Interaction, today_task: str):
    user_id = interaction.user.id

    # タスク永続化
    save_tasks(user_id, today_task)

    # ボタン作る
    view = ConfirmView(user_id)

    # レスポンス
    await interaction.response.send_message(
        f"📝 『{today_task}』 を今日のやることに登録したよ！達成できたらボタン押してね👇",
        view=view
    )
