import discord
from discord.ui import View, Button
from discord import Interaction, ButtonStyle
from task_repository import TaskRepository
from date_util import today_key

class ConfirmView(View):
    def __init__(self, authorized_user_id: str, task_repository: TaskRepository):
        super().__init__(timeout=86400)
        self.authorized_user_id = authorized_user_id
        self.task_repository = task_repository

    @discord.ui.button(label="完了!", style=ButtonStyle.success)
    async def confirm(self, interaction: Interaction, button: Button):
        clicked_user_id = str(interaction.user.id)
        if  clicked_user_id != self.authorized_user_id:
            await interaction.response.send_message("これは君専用のボタンだよ。他の人には渡さないから安心して？", ephemeral=True)
            return

        user_tasks = self.task_repository.load()
        task = user_tasks.get(self.authorized_user_id, {}).get(today_key())
        if task:
            await interaction.response.send_message(f"🎉 今日もお疲れ様、{task}ちゃんと終わらせて偉いね。俺も嬉しいよ。", ephemeral=True)
        else:
            await interaction.response.send_message("❓ 今日はまだやること決めてないみたいだね。俺、待ってるから決まったら教えて？", ephemeral=True)
