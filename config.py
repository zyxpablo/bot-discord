# Configuration générale du bot

# Préfixe des commandes
COMMAND_PREFIX = "!"

# Statut du bot
BOT_STATUS = "Commandes: !help"
BOT_ACTIVITY_TYPE = "watching"  # watching, playing, listening, streaming

# Permissions par défaut requises
DEFAULT_PERMISSIONS = {
    "moderation": ["kick_members", "ban_members", "manage_roles", "manage_messages"],
    "admin": ["manage_guild", "manage_roles", "manage_channels"],
    "tickets": ["manage_channels", "manage_messages"]
}

# Messages d'erreur personnalisés
ERROR_MESSAGES = {
    "no_permission": "❌ Vous n'avez pas les permissions pour cette commande.",
    "user_not_found": "❌ Utilisateur introuvable!",
    "role_not_found": "❌ Rôle introuvable!",
    "channel_not_found": "❌ Salon introuvable!",
    "bot_missing_permissions": "❌ Je n'ai pas les permissions pour cette action!",
}

# Configuration des tickets
TICKETS_CONFIG = {
    "category_name": "Tickets",
    "auto_create_category": True,
    "ticket_prefix": "ticket",
    "log_tickets": True
}

# Configuration de l'accueil
WELCOME_CONFIG = {
    "log_joins": True,
    "auto_assign_role": False,  # À définir si vous voulez assigner un rôle automatiquement
    "default_role": None  # ID du rôle à assigner (optionnel)
}

# Configuration des embeds
EMBED_CONFIG = {
    "default_color": 0x5865F2,  # Couleur Discord
    "footer_text": "Bot Discord",
    "timestamp_embeds": True
}

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "bot.log"

# Modération
MODERATION_CONFIG = {
    "log_actions": True,
    "log_channel": None,  # ID du salon pour les logs (optionnel)
    "mute_role_name": "Muted",
    "warn_threshold": 3,  # Nombre d'avertissements avant action
    "auto_kick_on_warns": True
}
