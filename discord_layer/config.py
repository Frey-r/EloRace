import os
import dotenv
from elorace.logger_config import get_logger
import discord


logger = get_logger(__name__)
dotenv.load_dotenv()

class Config:
    def __init__(self):
        # Configuraciones básicas del bot
        self.bot_token = os.getenv("DISCORDAPITOKEN")
        self.bot_prefix = "!"
        self.application_id = os.getenv("APPLICATION_ID")  # Para comandos slash
        
        # Configuraciones de permisos
        self.bot_admins = []
        self.bot_owner = None
        self.bot_moderators = []
        self.allowed_roles = []
        
        # Configuraciones de canales y servidores
        self.bot_channels = []
        self.bot_guilds = []
        self.log_channel_id = None
        self.command_channels = []  # Canales donde se permiten comandos
        self.announcement_channel = None
        
        # Configuraciones de la API
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
        self.api_token = os.getenv("API_TOKEN")
        
        # Configuraciones de cooldowns y límites
        self.command_cooldown = 3  # segundos
        self.max_warnings = 3
        self.timeout_duration = 300  # segundos
        
        # Configuraciones de características
        self.enable_logging = True
        self.enable_error_reporting = True
        self.debug_mode = os.getenv("DEBUG", "False").lower() == "true"
        
        # Configuraciones de mensajes
        self.welcome_message = "Gracias por agregarme a tu servidor, puedes usar !help para ver los comandos disponibles"
        self.help_message = "Usa !help para ver los comandos disponibles"
        
        # Intents de Discord
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.presences = True
        self.intents.typing = True
        self.intents.message_content = True
        self.intents.guilds = True
        self.intents.reactions = True
        self.intents.voice_states = True
        
        # Configuraciones de respaldo y persistencia
        self.database_url = os.getenv("DATABASE_URL")
        self.backup_channel_id = None
        
        # Configuraciones específicas del juego
        self.default_elo = 1000
        self.k_factor = 32
        self.min_players_for_match = 2
        self.max_players_for_match = 8
        
        # Configuraciones de roles automáticos
        self.auto_roles = {
            "newcomer": None,  # ID del rol
            "racer": None,
            "player": None
        }
        
        # Emojis personalizados
        #self.custom_emojis = {
        #    "success": "✅",
        #    "error": "❌",
        #    "warning": "⚠️"
        #}

    def validate_config(self):
        """Valida que todas las configuraciones necesarias estén presentes"""
        if not self.bot_token:
            logger.error("Bot token no encontrado en variables de entorno")
            raise ValueError("Bot token no encontrado en variables de entorno")
        
        if not self.application_id:
            logger.warning("Application ID no configurado - los comandos slash podrían no funcionar")
            
        if not self.api_url:
            logger.warning("API URL no configurada - algunas funciones podrían no estar disponibles")