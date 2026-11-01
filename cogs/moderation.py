import discord
from discord import app_commands
from discord.ext import commands

class ModerationCog(commands.Cog):
    """Cog para herramientas de moderación del servidor."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulsa a un miembro del servidor")
    @app_commands.describe(miembro="El miembro a expulsar", razon="Motivo de la expulsión")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self, 
        interaction: discord.Interaction, 
        miembro: discord.Member, 
        razon: str = "No especificada"
    ):
        """Expulsa a un usuario si el moderador y el bot tienen permisos."""
        if miembro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                "❌ No puedes expulsar a alguien con un rol igual o superior al tuyo.",
                ephemeral=True
            )
            return

        await miembro.kick(reason=f"Por {interaction.user}: {razon}")
        await interaction.response.send_message(
            f"👢 **{miembro.mention}** ha sido expulsado.\n**Motivo:** {razon}"
        )

    @app_commands.command(name="ban", description="Banea a un miembro del servidor")
    @app_commands.describe(miembro="El miembro a banear", razon="Motivo del baneo")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self, 
        interaction: discord.Interaction, 
        miembro: discord.Member, 
        razon: str = "No especificada"
    ):
        """Banea a un usuario si el moderador y el bot tienen permisos."""
        if miembro.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                "❌ No puedes banear a alguien con un rol igual o superior al tuyo.",
                ephemeral=True
            )
            return

        await miembro.ban(reason=f"Por {interaction.user}: {razon}")
        await interaction.response.send_message(
            f"🔨 **{miembro.mention}** ha sido baneado.\n**Motivo:** {razon}"
        )

    @app_commands.command(name="clear", description="Elimina una cantidad determinada de mensajes del canal")
    @app_commands.describe(cantidad="Cantidad de mensajes a borrar (1 a 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, cantidad: app_commands.Range[int, 1, 100]):
        """Borra mensajes del canal actual."""
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=cantidad)
        await interaction.followup.send(
            f"🧹 Se han eliminado `{len(deleted)}` mensajes.",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
