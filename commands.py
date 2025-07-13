from discord import app_commands, Interaction
from views import ConfirmView
from tasks import user_tasks, today_key

#Bot独自のスラッシュコマンドを指定できる
@app_commands.command(name="declare", description="今日やることを宣言しよう！")
@app_commands.describe(task="今日やること")
async def declare_command(interaction: Interaction, task: str):
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
