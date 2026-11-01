import os
import sys
import logging
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 1. Configuración de Logging con marcas de tiempo legibles
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("DiscordBot")

# 2. Carga segura de variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID") # Opcional: para sincronización rápida en desarrollo

if not TOKEN:
    logger.critical("No se encontró la variable DISCORD_TOKEN en el archivo .env")
    sys.exit(1)

# 3. Configuración de Intents requeridos
intents = discord.Intents.default()
intents.message_content = True  # Manejo de contenido de mensajes

# 4. Definición de la subclase del Bot con soporte para Cogs y Sync
class KyotoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Carga dinámica de cogs en el arranque."""
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        if os.path.exists(cogs_dir):
            for filename in os.listdir(cogs_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    cog_name = f"cogs.{filename[:-3]}"
                    try:
                        await self.load_extension(cog_name)
                        logger.info(f"Cog cargado exitosamente: {cog_name}")
                    except Exception as e:
                        logger.error(f"Error cargando el cog {cog_name}: {e}", exc_info=True)

    async def on_ready(self):
        """Evento on_ready con sincronización de slash commands."""
        logger.info(f"Bot conectado como: {self.user.name} (ID: {self.user.id})")
        logger.info(f"Conectado a {len(self.guilds)} servidores.")

        try:
            # Sincronización por servidor si está definido en .env (instantáneo para pruebas)
            if GUILD_ID:
                guild_obj = discord.Object(id=int(GUILD_ID))
                self.tree.copy_global_to(guild=guild_obj)
                synced_guild = await self.tree.sync(guild=guild_obj)
                logger.info(f"Sincronizados {len(synced_guild)} slash commands en el servidor (Guild: {GUILD_ID}).")

            # Sincronización global
            synced_global = await self.tree.sync()
            logger.info(f"Sincronizados {len(synced_global)} slash commands a nivel global.")
        except Exception as e:
            logger.error(f"Error sincronizando slash commands: {e}", exc_info=True)

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name="/ping | Kyoto Bot"
            )
        )

bot = KyotoBot()

if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
