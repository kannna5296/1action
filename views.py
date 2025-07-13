import discord
from discord.ui import View, Button
from discord import Interaction, ButtonStyle
from tasks import load_tasks
from date_util import today_key

class ConfirmView(View):
    def __init__(self, user_id):
        super().__init__(timeout=86400)
        self.user_id = user_id

    @discord.ui.button(label="完了!", style=ButtonStyle.success)
    async def confirm(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなた専用のボタンだよ！", ephemeral=True)
            return

        user_tasks = load_tasks()
        task = user_tasks.get(str(self.user_id), {}).get(today_key())
        if task:
            await interaction.response.send_message(f"🎉 お疲れ様！『{task}』完了したね！", ephemeral=True)
        else:
            await interaction.response.send_message("❓ 今日のやることが未登録みたい！", ephemeral=True)
