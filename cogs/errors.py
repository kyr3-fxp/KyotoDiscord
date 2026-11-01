import logging
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("ErrorHandler")

class ErrorHandler(commands.Cog):
    """Manejador global de errores para comandos convencionales y Slash Commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Registrar el error handler global para interacciones de slash commands
        self.old_tree_error = bot.tree.on_error
        bot.tree.on_error = self.on_app_command_error

    def cog_unload(self):
        # Restaurar handler original al descargar el cog si fuera necesario
        self.bot.tree.on_error = self.old_tree_error

    async def on_app_command_error(
        self, 
        interaction: discord.Interaction, 
        error: app_commands.AppCommandError
    ):
        """Captura global de errores en Slash Commands (app_commands)."""
        command_name = interaction.command.name if interaction.command else "desconocido"
        user = interaction.user
        
        # Desempaquetar el error si está envuelto en CommandInvokeError
        original_error = getattr(error, 'original', error)

        # 1. Permisos faltantes del usuario
        if isinstance(error, app_commands.MissingPermissions) or isinstance(original_error, app_commands.MissingPermissions):
            missing = ", ".join(getattr(error, "missing_permissions", []))
            message = f"🚫 **Acceso Denegado**: No tienes los permisos necesarios para ejecutar este comando (`{missing}`)."
            logger.warning(f"Permisos insuficientes para el usuario {user} (ID: {user.id}) al usar /{command_name}: {missing}")

        # 2. Cooldown / Espera entre usos
        elif isinstance(error, app_commands.CommandOnCooldown) or isinstance(original_error, app_commands.CommandOnCooldown):
            retry_after = round(getattr(error, "retry_after", 0), 1)
            message = f"⏳ **Comando en enfriamiento**: Por favor espera `{retry_after}s` antes de volver a usarlo."
            logger.info(f"Comando /{command_name} en cooldown para {user} ({retry_after}s restantes).")

        # 3. Argumentos inválidos
        elif isinstance(error, (app_commands.TransformerError, commands.BadArgument)) or isinstance(original_error, (app_commands.TransformerError, commands.BadArgument)):
            message = "⚠️ **Argumento inválido**: Verifica los valores proporcionados al ejecutar el comando."
            logger.warning(f"Argumento inválido en /{command_name} por {user}: {error}")

        # 4. Error genérico / no controlado
        else:
            message = "❌ **Ocurrió un error inesperado** al procesar el comando. El incidente ha sido registrado."
            logger.error(
                f"Excepción en slash command '/{command_name}' invocado por {user} (ID: {user.id}): {error}", 
                exc_info=error
            )

        # Responder al usuario de manera efímera (solo visible para él)
        try:
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        except Exception as e:
            logger.error(f"Fallo al enviar mensaje de error efímero a {user}: {e}", exc_info=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Captura de errores para comandos tradicionales con prefijo (e.g. !ping)."""
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)
        cmd_name = ctx.command.name if ctx.command else "desconocido"
        user = ctx.author

        if isinstance(error, commands.MissingPermissions):
            missing = ", ".join(error.missing_permissions)
            msg = f"🚫 No tienes permisos para usar `{cmd_name}` ({missing})."
            logger.warning(f"Permisos insuficientes para {user} en !{cmd_name}")
            await ctx.reply(msg, mention_author=False)

        elif isinstance(error, commands.CommandOnCooldown):
            msg = f"⏳ Comando en enfriamiento. Espera `{round(error.retry_after, 1)}s`."
            logger.info(f"Comando !{cmd_name} en cooldown para {user}.")
            await ctx.reply(msg, mention_author=False)

        elif isinstance(error, commands.BadArgument):
            msg = "⚠️ Argumento incorrecto o inválido."
            logger.warning(f"BadArgument en !{cmd_name} por {user}: {error}")
            await ctx.reply(msg, mention_author=False)

        elif isinstance(error, commands.CommandNotFound):
            pass # Ignorar comandos inexistentes si se prefiere

        else:
            logger.error(f"Error no controlado en comando tradicional !{cmd_name} por {user}: {error}", exc_info=error)
            await ctx.reply("❌ Ocurrió un error inesperado al procesar este comando.", mention_author=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))
