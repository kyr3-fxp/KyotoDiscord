import discord
from discord import app_commands
from discord.ext import commands

class GeneralCog(commands.Cog):
    """Cog para comandos generales y de utilidad."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Muestra la latencia actual del bot en milisegundos")
    async def ping(self, interaction: discord.Interaction):
        """Comando de prueba /ping que calcula la latencia websocket del bot."""
        latency_ms = round(self.bot.latency * 1000)
        
        # Mensaje de interacción asíncrona
        await interaction.response.send_message(
            f"🏓 **¡Pong!** Latencia: `{latency_ms}ms`",
            ephemeral=False
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))
