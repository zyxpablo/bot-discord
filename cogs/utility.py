import discord
from discord.ext import commands
from datetime import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Affiche la latence du bot"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latence: {latency}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='help')
    async def help(self, ctx):
        """Affiche l'aide du bot"""
        embed = discord.Embed(
            title="📚 Aide du Bot",
            description="Voici les commandes disponibles",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🛡️ Modération",
            value="""
`!kick <membre> [raison]` - Expulser un membre
`!ban <membre> [raison]` - Bannir un membre
`!unban <user>` - Débannir un utilisateur
`!mute <membre> [raison]` - Rendre muet un membre
`!unmute <membre>` - Rétablir la parole
`!warn <membre> [raison]` - Avertir un membre
`!clean [nombre]` - Supprimer des messages
`!slowmode [secondes]` - Définir le slowmode
            """,
            inline=False
        )

        embed.add_field(
            name="👤 Utilisateurs",
            value="""
`!userinfo [@membre]` - Info sur un utilisateur
`!avatar [@membre]` - Avatar d'un utilisateur
`!serverinfo` - Info du serveur
            """,
            inline=False
        )

        embed.add_field(
            name="🎭 Rôles",
            value="""
`!addrole <membre> <rôle>` - Ajouter un rôle
`!removerole <membre> <rôle>` - Retirer un rôle
            """,
            inline=False
        )

        embed.add_field(
            name="⚙️ Utilitaires",
            value="""
`!ping` - Latence du bot
`!help` - Cette aide
            """,
            inline=False
        )

        embed.set_footer(text="Utilisez !help <commande> pour plus de détails")
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Affiche les infos d'un utilisateur"""
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title=f"👤 Infos de {member.name}",
            color=member.color,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Pseudo", value=member.mention)
        embed.add_field(name="Compte créé", value=member.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Rejoint le serveur", value=member.joined_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Rôles", value=" ".join([r.mention for r in member.roles[1:]]) or "Aucun")
        embed.add_field(name="Statut", value=str(member.status).capitalize())
        embed.set_footer(text=f"Demandé par {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Affiche l'avatar d'un utilisateur"""
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title=f"Avatar de {member.name}",
            color=discord.Color.blurple()
        )
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """Affiche les infos du serveur"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Serveur: {guild.name}",
            color=discord.Color.blurple(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Propriétaire", value=guild.owner.mention)
        embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"))
        embed.add_field(name="Membres", value=guild.member_count)
        embed.add_field(name="Rôles", value=len(guild.roles))
        embed.add_field(name="Salons", value=len(guild.channels))
        embed.add_field(name="Niveau de vérification", value=str(guild.verification_level).capitalize())
        embed.set_footer(text=f"Demandé par {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Ajoute un rôle à un membre"""
        if role in member.roles:
            await ctx.send(f"❌ {member.mention} a déjà le rôle {role.mention}!")
            return

        await member.add_roles(role)
        embed = discord.Embed(
            title="✅ Rôle ajouté",
            description=f"{role.mention} ajouté à {member.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='removerole')
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Retire un rôle à un membre"""
        if role not in member.roles:
            await ctx.send(f"❌ {member.mention} n'a pas le rôle {role.mention}!")
            return

        await member.remove_roles(role)
        embed = discord.Embed(
            title="✅ Rôle retiré",
            description=f"{role.mention} retiré à {member.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
