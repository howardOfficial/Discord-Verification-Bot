import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import os

TOKEN = 'ТВОЙ_ТОКЕН_ОТ_DISCORD_DEVELOPER_PORTAL'

VERIFIED_ROLE_ID = 123456789012345678  # Замените на реальный ID роли

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Проверить статус", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_callback(self, interaction: discord.Interaction, button: Button):
        # Скрытый ответ (видит только нажавший)
        await interaction.response.send_message("⏳ Проверяю ваш статус... Пожалуйста, подождите.", ephemeral=True)
        
        # Имитация проверки (ожидание 15 секунд)
        await asyncio.sleep(15)
        
        # Выдаем роль
        guild = interaction.guild
        role = guild.get_role(VERIFIED_ROLE_ID)
        member = interaction.user
        
        if role and role not in member.roles:
            try:
                await member.add_roles(role)
                # Отправляем сообщение в ЛС с кнопкой
                try:
                    await member.send("✅ Вы успешно прошли верификацию! Роль выдана.")
                except discord.Forbidden:
                    pass
            except discord.Forbidden:
                await interaction.followup.send("❌ У бота нет прав на выдачу этой роли. Обратитесь к администратору.", ephemeral=True)
        else:
            await interaction.followup.send("✅ Вы уже верифицированы.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')
    # Регистрируем View для кнопки (чтобы работала после перезапуска)
    bot.add_view(VerifyView())

@bot.command()
async def setup_verify(ctx):
    """Команда для отправки сообщения с кнопкой верификации в канал."""
    embed = discord.Embed(
        title="Верификация участника",
        description="Нажмите на кнопку ниже, чтобы пройти проверку и получить доступ к серверу.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=VerifyView())

if __name__ == '__main__':
    bot.run(TOKEN)