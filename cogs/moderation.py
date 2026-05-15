import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Pas de raison spécifiée"):
        """Expulse un membre du serveur"""
        if member == ctx.author:
            await ctx.send("❌ Vous ne pouvez pas vous expulser vous-même!")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Vous ne pouvez pas expulser quelqu'un de rang égal ou supérieur!")
            return

        await member.kick(reason=reason)
        embed = discord.Embed(
            title="⚠️ Membre expulsé",
            description=f"{member.mention} a été expulsé",
            color=discord.Color.orange()
        )
        embed.add_field(name="Raison", value=reason)
        embed.set_footer(text=f"Modérateur: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Pas de raison spécifiée"):
        """Bannit un membre du serveur"""
        if member == ctx.author:
            await ctx.send("❌ Vous ne pouvez pas vous bannir vous-même!")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Vous ne pouvez pas bannir quelqu'un de rang égal ou supérieur!")
            return

        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Membre banni",
            description=f"{member.mention} a été banni",
            color=discord.Color.red()
        )
        embed.add_field(name="Raison", value=reason)
        embed.set_footer(text=f"Modérateur: {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="Débannissement"):
        """Débannit un utilisateur"""
        try:
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(
                title="✅ Utilisateur débanni",
                description=f"{user} a été débanni",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("❌ Cet utilisateur n'est pas banni!")

    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: str = None, *, reason="Pas de raison"):
        """Rend muet un membre"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)

        await member.add_roles(muted_role)
        embed = discord.Embed(
            title="🔇 Membre rendu muet",
            description=f"{member.mention} a été rendu muet",
            color=discord.Color.blue()
        )
        embed.add_field(name="Raison", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Rétablit la parole à un membre"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"✅ {member.mention} peut de nouveau parler!")
        else:
            await ctx.send("❌ Ce membre n'est pas rendu muet!")

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Pas de raison"):
        """Avertit un membre"""
        embed = discord.Embed(
            title="⚠️ Avertissement",
            description=f"{member.mention} a reçu un avertissement",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Raison", value=reason)
        embed.set_footer(text=f"Modérateur: {ctx.author}")
        await ctx.send(embed=embed)
        try:
            await member.send(f"Vous avez reçu un avertissement sur {ctx.guild.name}: {reason}")
        except:
            pass

    @commands.command(name='clean')
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount: int = 10):
        """Supprime les X derniers messages"""
        if amount > 100:
            await ctx.send("❌ Vous ne pouvez supprimer que 100 messages max!")
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ {len(deleted) - 1} messages supprimés!", delete_after=3)

    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Définit le délai entre les messages"""
        if seconds < 0 or seconds > 21600:
            await ctx.send("❌ Entrez un nombre entre 0 et 21600 secondes!")
            return

        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("✅ Slowmode désactivé!")
        else:
            await ctx.send(f"✅ Slowmode défini à {seconds}s!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
