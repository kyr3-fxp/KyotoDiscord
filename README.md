# Kyoto Discord Bot (discord.py 2.x)

Estructura modular y lista para producción de un bot de Discord en Python utilizando discord.py 2.x, soporte para Cogs, Slash Commands automáticos, manejo global de errores y despliegue 24/7 (Docker / PM2).

---

## 📁 Estructura del Proyecto

```text
KyotoDiscord/
├── .env                  # Variables sensibles (Token, etc.)
├── .gitignore            # Archivos ignorados por Git
├── Dockerfile            # Imagen optimizada Python 3.11-slim
├── docker-compose.yml    # Orquestación con auto-restart 24/7
├── main.py               # Punto de entrada, intents, carga de Cogs y sync
├── requirements.txt      # Dependencias fijadas (discord.py, python-dotenv)
├── venv/                 # Entorno virtual de Python
└── cogs/                 # Módulos / Cogs
    ├── __init__.py
    ├── general.py        # Slash command /ping
    └── errors.py         # Manejador global de excepciones (Slash y Prefix)
```

---

## 🚀 Puesta en Marcha Local

### 1. Activar el entorno virtual

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 2. Configurar variables de entorno (`.env`)

Asegúrate de que tu archivo `.env` contenga:
```env
DISCORD_TOKEN=tu_token_aqui
# GUILD_ID=123456789012345678 # (Opcional, para pruebas inmediatas en tu servidor)
```

### 3. Ejecutar el bot

```bash
python main.py
```

---

## 🛠️ Comandos y Características

- **/ping**: Slash command que responde de forma asíncrona (`interaction.response.send_message`) con la latencia del WebSocket en milisegundos.
- **Sincronización en `on_ready`**:
  - Sincroniza globalmente con `await self.tree.sync()`.
  - Si especificas `GUILD_ID` en `.env`, copia los comandos al servidor y sincroniza al instante para pruebas rápidas sin esperar la propagación global de Discord.
- **Manejo Global de Errores (`cogs/errors.py`)**:
  - Captura excepciones como `MissingPermissions`, `CommandOnCooldown` y `BadArgument`.
  - Responde de manera efímera (`ephemeral=True`) al usuario para no interrumpir el chat público ni tumbar el bot.
  - Registra las incidencias con timestamp en consola vía `logging`.

---

## 🕒 Ejecución 24/7

### Opción A: Docker & Docker Compose (Recomendado)

1. Construir y levantar en segundo plano:
   ```bash
   docker compose up -d --build
   ```
2. Ver logs en tiempo real:
   ```bash
   docker compose logs -f
   ```
3. Detener el bot:
   ```bash
   docker compose down
   ```

### Opción B: PM2 (Process Manager)

Si cuentas con Node.js / PM2 instalado en tu servidor:

1. **Iniciar el bot con PM2 usando el entorno virtual:**
   - En Windows:
     ```bash
     pm2 start .\venv\Scripts\python.exe --name "kyoto-bot" -- main.py
     ```
   - En Linux/macOS:
     ```bash
     pm2 start ./venv/bin/python --name "kyoto-bot" -- main.py
     ```
2. **Hacer que se inicie automáticamente tras reinicios del sistema:**
   ```bash
   pm2 startup
   pm2 save
   ```
3. **Monitorear y ver logs:**
   ```bash
   pm2 logs kyoto-bot
   pm2 status
   ```
