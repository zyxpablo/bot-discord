import discord
from discord.ext import commands
import json
import os

WELCOME_CONFIG = "welcome_config.json"

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_config()

    def load_config(self):
        if os.path.exists(WELCOME_CONFIG):
            with open(WELCOME_CONFIG, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        with open(WELCOME_CONFIG, 'w') as f:
            json.dump(self.config, f, indent=4)

    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel, *, message: str):
        """Configure le message d'accueil

        Utilise {member} pour le pseudo, {guild} pour le nom du serveur, {count} pour le nombre de membres
        """
        guild_id = str(ctx.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}

        self.config[guild_id]['welcome_channel'] = channel.id
        self.config[guild_id]['welcome_message'] = message
        self.save_config()

        embed = discord.Embed(
            title="✅ Message d'accueil configuré",
            description=f"Le message d'accueil sera envoyé dans {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Message:", value=message[:1024], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='setwelcomeembed')
    @commands.has_permissions(manage_guild=True)
    async def setwelcomeembed(self, ctx, channel: discord.TextChannel):
        """Configure le message d'accueil avec un embed préfait

        Répond avec un menu interactif
        """
        guild_id = str(ctx.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}

        embed = discord.Embed(
            title="🎉 Bienvenue!",
            description="Nous sommes heureux de te voir rejoindre notre communauté!",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="Comment ça marche?",
            value="Prends connaissance des règles et amuse-toi bien!",
            inline=False
        )
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text=f"Merci de rejoindre {ctx.guild.name}!")

        self.config[guild_id]['welcome_channel'] = channel.id
        self.config[guild_id]['welcome_embed'] = True
        self.save_config()

        await channel.send(embed=embed)
        await ctx.send(f"✅ Embed d'accueil envoyé dans {channel.mention}!")

    @commands.command(name='welcomemessage')
    @commands.has_permissions(manage_guild=True)
    async def welcomemessage(self, ctx):
        """Affiche la configuration du message d'accueil"""
        guild_id = str(ctx.guild.id)

        if guild_id not in self.config or 'welcome_channel' not in self.config[guild_id]:
            await ctx.send("❌ Aucun message d'accueil configuré!")
            return

        channel = self.bot.get_channel(self.config[guild_id]['welcome_channel'])
        message = self.config[guild_id].get('welcome_message', 'Aucun message')

        embed = discord.Embed(
            title="📋 Configuration du message d'accueil",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Salon", value=channel.mention if channel else "Supprimé")
        embed.add_field(name="Message", value=message[:1024], inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Envoie le message d'accueil quand quelqu'un rejoint"""
        guild_id = str(member.guild.id)

        if guild_id not in self.config or 'welcome_channel' not in self.config[guild_id]:
            return

        channel = self.bot.get_channel(self.config[guild_id]['welcome_channel'])
        if not channel:
            return

        # Si embed personnalisé
        if self.config[guild_id].get('welcome_embed'):
            embed = discord.Embed(
                title="🎉 Bienvenue!",
                description=f"{member.mention} vient de rejoindre le serveur!",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Membres", value=f"Tu es le {member.guild.member_count}ème membre!")
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=f"Bienvenue sur {member.guild.name}!")
            await channel.send(embed=embed)
            return

        # Message personnalisé
        message = self.config[guild_id].get('welcome_message', 'Bienvenue!')
        message = message.replace('{member}', member.mention)
        message = message.replace('{guild}', member.guild.name)
        message = message.replace('{count}', str(member.guild.member_count))

        await channel.send(message)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
