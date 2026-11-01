import discord
from discord import app_commands
from discord.ext import commands

class InfoCog(commands.Cog):
    """Cog para comandos informativos y de consulta del servidor y usuarios."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Muestra información detallada sobre un usuario")
    @app_commands.describe(usuario="Usuario a consultar (deja en blanco para ver tu perfil)")
    async def userinfo(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Devuelve un Embed con los detalles de una cuenta."""
        target = usuario or interaction.user
        
        # Formatear fechas
        created_at = discord.utils.format_dt(target.created_at, style="F")
        joined_at = discord.utils.format_dt(target.joined_at, style="F") if target.joined_at else "Desconocido"

        # Roles (excluyendo @everyone)
        roles = [role.mention for role in reversed(target.roles) if role.name != "@everyone"]
        roles_str = ", ".join(roles[:10]) if roles else "Ninguno"
        if len(roles) > 10:
            roles_str += f" y {len(roles) - 10} más..."

        embed = discord.Embed(
            title=f"Información de {target.display_name}",
            color=target.color if target.color.value != 0 else discord.Color.blurple()
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="🆔 ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="🤖 ¿Es bot?", value="Sí" if target.bot else "No", inline=True)
        embed.add_field(name="👑 Rol Principal", value=target.top_role.mention, inline=True)
        embed.add_field(name="📅 Cuenta creada", value=created_at, inline=False)
        embed.add_field(name="📥 Se unió al servidor", value=joined_at, inline=False)
        embed.add_field(name=f"🎭 Roles ({len(roles)})", value=roles_str, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Muestra información y estadísticas del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        """Devuelve un Embed con estadísticas de la comunidad."""
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("❌ Este comando solo puede usarse en un servidor.", ephemeral=True)
            return

        created_at = discord.utils.format_dt(guild.created_at, style="F")
        total_members = guild.member_count
        channels_text = len(guild.text_channels)
        channels_voice = len(guild.voice_channels)

        embed = discord.Embed(
            title=f"Información de {guild.name}",
            color=discord.Color.gold()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.add_field(name="🆔 ID del Servidor", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="👑 Propietario", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="👥 Total Miembros", value=f"`{total_members}`", inline=True)
        embed.add_field(name="💬 Canales de Texto", value=f"`{channels_text}`", inline=True)
        embed.add_field(name="🔊 Canales de Voz", value=f"`{channels_voice}`", inline=True)
        embed.add_field(name="✨ Nivel de Boost", value=f"Nivel `{guild.premium_tier}` ({guild.premium_subscription_count} boosts)", inline=True)
        embed.add_field(name="📅 Creación del Servidor", value=created_at, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))
