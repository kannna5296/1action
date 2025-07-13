from discord import app_commands, Interaction
from views import ConfirmView
from tasks import today_key, save_tasks, load_tasks

#Bot独自のスラッシュコマンドを指定できる
@app_commands.command(name="declare", description="今日やることを宣言しよう！")
@app_commands.describe(today_task="今日やること")
async def declare_command(interaction: Interaction, today_task: str):
    user_id = interaction.user.id
    today = today_key()

    user_tasks = load_tasks()
    if user_id not in user_tasks:
        user_tasks[user_id] = {}
    user_tasks[user_id][today] = today_task
    save_tasks(user_tasks)  # 登録後に保存！

    view = ConfirmView(user_id, today)
    await interaction.response.send_message(
        f"📝 『{today_task}』 を今日のやることに登録したよ！達成できたらボタン押してね👇",
        view=view
    )
