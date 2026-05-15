# ⚡ Démarrage Rapide

## 1️⃣ Préparation (5 minutes)

### Obtenir un token Discord
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez "New Application" et donnez un nom à votre bot
3. Allez dans l'onglet "Bot" et cliquez "Add Bot"
4. Cliquez "Copy" sous TOKEN
5. Collez le token dans un fichier `.env`:
```
DISCORD_TOKEN=votre_token_ici
```

### Inviter le bot à votre serveur
1. Dans Developer Portal, allez à "OAuth2" → "URL Generator"
2. Cochez `bot` dans "SCOPES"
3. Cochez ces permissions:
   - ✅ Manage Guild
   - ✅ Manage Roles
   - ✅ Kick Members
   - ✅ Ban Members
   - ✅ Manage Messages
   - ✅ Manage Channels
4. Copiez l'URL générée et ouvrez-la pour inviter le bot

## 2️⃣ Installation (2 minutes)

```bash
# Installez les dépendances
pip install -r requirements.txt

# Lancez le bot
python main.py
```

Vous devriez voir: `YourBotName est connecté!`

## 3️⃣ Configuration de Base (5 minutes)

### Configurer un message d'accueil
```
!setwelcome #accueil Bienvenue {member}! Tu es le {count}ème membre! 🎉
```

### Configurer les tickets
```
!setuptickets #tickets
```

## 4️⃣ Premiers Tests

**Dans Discord:**
1. Tapez `!ping` → Vous devriez voir la latence
2. Tapez `!help` → Vous devriez voir toutes les commandes
3. Tapez `!serverinfo` → Vous devriez voir les infos du serveur

## ✅ Vous êtes prêt!

Le bot est maintenant opérationnel! Consultez le [README.md](README.md) pour toutes les commandes disponibles.

## 🎨 Premiers embeds

### Simple
```
!embedsimple Titre | Description
```

### Avec couleur
```
!embedcouleur FF5733 Annonce | Contenu ici
```

### Avancé
```
!embednew
!embednew titre 📢 Annonce
!embednew description Ceci est une annonce
!embednew couleur 0000FF
!embednew envoyer #annonces
```

## 🆘 Besoin d'aide?

- **Le bot ne démarre pas?** Vérifiez que le token dans `.env` est correct
- **Les commandes ne marchent pas?** Utilisez `!help` pour voir les commandes disponibles
- **Problème de permissions?** Assurez-vous que le bot a les permissions nécessaires sur le serveur

Consultez [README.md](README.md) pour le troubleshooting complet.
