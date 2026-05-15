# Bot Discord - Gestion de Serveur

Un bot Discord simple et efficace pour gérer votre serveur avec des commandes de modération, gestion d'utilisateurs et plus.

## 🚀 Installation

### 1. Prérequis
- Python 3.8+
- Un compte Discord
- Un serveur Discord

### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration du token
1. Renommez `.env.example` en `.env`
2. Remplacez `ton_token_discord_ici` par votre token Discord
3. Pour obtenir votre token:
   - Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
   - Créez une nouvelle application
   - Allez dans "Bot" et cliquez "Add Bot"
   - Copiez le token sous "TOKEN"

### 4. Créer une invitation pour le bot
1. Dans Developer Portal, allez dans "OAuth2" → "URL Generator"
2. Sélectionnez les scopes: `bot`
3. Sélectionnez les permissions:
   - Manage Guild
   - Manage Roles
   - Kick Members
   - Ban Members
   - Manage Messages
   - Manage Channels
4. Copiez l'URL générée et ouvrez-la pour inviter le bot

### 5. Lancer le bot
```bash
python main.py
```

Le bot affichera "Bot_name est connecté!" dans la console.

## 📋 Commandes Disponibles

### 🛡️ Modération
- `!kick <@membre> [raison]` - Expulser un membre
- `!ban <@membre> [raison]` - Bannir un membre
- `!unban <user>` - Débannir un utilisateur
- `!mute <@membre> [raison]` - Rendre muet un membre
- `!unmute <@membre>` - Rétablir la parole
- `!warn <@membre> [raison]` - Avertir un membre
- `!clean [nombre]` - Supprimer les X derniers messages (défaut: 10, max: 100)
- `!slowmode [secondes]` - Définir le délai entre messages (0 pour désactiver)

### 👤 Utilisateurs
- `!userinfo [@membre]` - Afficher les infos d'un utilisateur
- `!avatar [@membre]` - Afficher l'avatar d'un utilisateur
- `!serverinfo` - Afficher les infos du serveur

### 🎭 Rôles
- `!addrole <@membre> <rôle>` - Ajouter un rôle
- `!removerole <@membre> <rôle>` - Retirer un rôle

### 🎉 Bienvenue
- `!setwelcome <#salon> <message>` - Configurer le message d'accueil
- `!setwelcomeembed <#salon>` - Configurer un embed d'accueil
- `!welcomemessage` - Afficher la configuration actuelle

**Variables disponibles pour le message d'accueil:**
- `{member}` - Mention du nouveau membre
- `{guild}` - Nom du serveur
- `{count}` - Nombre total de membres

### 🎫 Système de Tickets
- `!setuptickets [#salon]` - Configurer le système de tickets
- `!closeticket` - Fermer le ticket actuel
- `!addticket <@membre>` - Ajouter un membre au ticket
- `!removeticket <@membre>` - Retirer un membre du ticket

**Comment ça marche:**
1. Les utilisateurs cliquent sur le bouton "Créer un ticket"
2. Un salon privé est créé pour eux
3. Les modérateurs peuvent ajouter/retirer des membres
4. Fermer le ticket supprime le salon

### 🎨 Embeds Personnalisés

**Embeds simples:**
- `!embedsimple <titre> | <description>` - Créer un embed simple
- `!embedcouleur <couleur_hex> <titre> | <description>` - Embed avec couleur (ex: FF5733)
- `!embedimage <url> <titre> | <description>` - Embed avec image principale
- `!embedthumbnail <url> <titre> | <description>` - Embed avec petite image

**Embeds avancés (étape par étape):**
- `!embednew` - Créer un nouvel embed
  - `!embednew titre <titre>` - Définir le titre
  - `!embednew description <description>` - Définir la description
  - `!embednew couleur <couleur_hex>` - Changer la couleur
  - `!embednew champ <nom> <valeur>` - Ajouter un champ
  - `!embednew image <url>` - Ajouter une image
  - `!embednew thumbnail <url>` - Ajouter une petite image
  - `!embednew auteur <nom>` - Ajouter un auteur
  - `!embednew footer <texte>` - Ajouter un pied de page
  - `!embednew apercu` - Voir un aperçu
  - `!embednew envoyer [#salon]` - Envoyer l'embed

### ⚙️ Utilitaires
- `!ping` - Afficher la latence du bot
- `!help` - Afficher cette aide

## 📁 Structure du Projet

```
bot-discord/
├── main.py              # Fichier principal du bot
├── requirements.txt     # Dépendances Python
├── .env                 # Configuration (créé à partir de .env.example)
├── .env.example         # Template de configuration
├── README.md            # Cette documentation
└── cogs/
    ├── moderation.py    # Commandes de modération
    └── utility.py       # Commandes utilitaires
```

## ⚙️ Configuration Recommandée

### Permissions du bot
Accordez au bot les permissions suivantes sur votre serveur:
- **Administrateur** (idéal) ou
- Permissions individuelles:
  - Gérer le serveur
  - Gérer les rôles
  - Expulser des membres
  - Bannir des membres
  - Gérer les messages
  - Gérer les salons

### Hiérarchie des rôles
Placez le rôle du bot au-dessus des rôles que vous voulez qu'il gère.

## 🔧 Personnalisation

### Changer le préfixe des commandes
Dans `main.py`, changez:
```python
bot = commands.Bot(command_prefix='!', ...)
```
Remplacez `'!'` par le caractère de votre choix.

### Ajouter une nouvelle commande
1. Créez un nouveau cog dans le dossier `cogs/`
2. Définissez votre classe et vos commandes
3. N'oubliez pas la fonction `setup(bot)` à la fin

Exemple:
```python
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mycommand')
    async def my_command(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## ⚠️ Notes Importantes

- Le bot doit avoir les permissions nécessaires pour chaque action
- Les commandes de modération ne marchent que si le bot a les permissions appropriées
- Le rôle "Muted" est créé automatiquement lors du premier `!mute`
- Le bot ne peut pas manager les rôles au-dessus du sien

## 🎨 Guide des Couleurs HEX

Voici quelques couleurs HEX populaires:

| Couleur | Code | Exemple |
|---------|------|---------|
| 🔴 Rouge | FF0000 | `!embedcouleur FF0000 Erreur \| Un problème est survenu` |
| 🟢 Vert | 00FF00 | `!embedcouleur 00FF00 Succès \| Opération réussie` |
| 🔵 Bleu | 0000FF | `!embedcouleur 0000FF Info \| Information importante` |
| 🟡 Jaune | FFFF00 | `!embedcouleur FFFF00 Attention \| À noter` |
| 🟣 Violet | 9D00FF | `!embedcouleur 9D00FF Spécial \| Contenu exclusive` |
| 🟠 Orange | FF7F00 | `!embedcouleur FF7F00 Avertissement \| Soyez prudents` |

Trouvez plus de couleurs sur [htmlcolorcodes.com](https://www.htmlcolorcodes.com/)

## 💡 Exemples d'Utilisation

### Exemple 1: Message d'accueil personnalisé
```
!setwelcome #accueil Bienvenue {member}! 🎉 Tu es le {count}ème membre de {guild}
```

### Exemple 2: Créer un embed avec image
```
!embedimage https://example.com/image.png Titre | Description de l'image
```

### Exemple 3: Créer un embed complexe
```
!embednew
!embednew titre 📢 Annonce importante
!embednew description Ceci est une annonce pour tous les membres
!embednew couleur FF5733
!embednew champ 📅 Date | 15 mai 2026
!embednew champ 👥 Participants | Tous les membres
!embednew footer Annonce du serveur
!embednew apercu
!embednew envoyer #annonces
```

## 🆘 Troubleshooting

**Le bot ne démarre pas:**
- Vérifiez que le token dans `.env` est correct
- Vérifiez que Discord.py est bien installé
- Vérifiez les erreurs dans la console

**Les commandes ne marchent pas:**
- Vérifiez que le bot a les permissions nécessaires
- Vérifiez la hiérarchie des rôles
- Vérifiez que vous utilisez le bon préfixe

**Le bot se déconnecte:**
- Vérifiez votre connexion internet
- Vérifiez que le token est valide
- Vérifiez les logs pour les erreurs

## 📝 Licence

Ce projet est libre d'utilisation. Modifiez-le à votre guise!
