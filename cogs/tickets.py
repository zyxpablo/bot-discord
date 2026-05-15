import discord
from discord.ext import commands
import json
import os

TICKETS_CONFIG = "tickets_config.json"

class TicketButton(discord.ui.Button):
    def __init__(self, cog):
        super().__init__(label="📩 Créer un ticket", style=discord.ButtonStyle.success)
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        # Vérifier si l'utilisateur a déjà un ticket ouvert
        existing = discord.utils.get(guild.channels, name=f"ticket-{member.id}")
        if existing:
            await interaction.response.send_message(
                "❌ Tu as déjà un ticket ouvert!",
                ephemeral=True
            )
            return

        # Créer le salon du ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{member.name}",
            overwrites=overwrites,
            category=discord.utils.get(guild.categories, name="Tickets") or None
        )

        # Envoyer le message de bienvenue dans le ticket
        embed = discord.Embed(
            title="🎫 Nouveau Ticket",
            description=f"Merci {member.mention} d'avoir créé un ticket!\n\nDécris ton problème ci-dessous et notre équipe t'aidera.",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Clique sur 'Fermer le ticket' pour le fermer")

        view = TicketCloseView(self.cog)
        await ticket_channel.send(embed=embed, view=view)

        await interaction.response.send_message(
            f"✅ Ticket créé: {ticket_channel.mention}",
            ephemeral=True
        )

class TicketCloseButton(discord.ui.Button):
    def __init__(self, cog):
        super().__init__(label="❌ Fermer le ticket", style=discord.ButtonStyle.danger)
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        # Vérifier les permissions
        if not interaction.user.guild_permissions.manage_channels and interaction.user.id != int(interaction.channel.name.split('-')[1]):
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission de fermer ce ticket!",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="⏳ Fermeture du ticket",
            description="Ce ticket sera fermé dans 5 secondes...",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketCloseView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.add_item(TicketCloseButton(cog))

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_config()

    def load_config(self):
        if os.path.exists(TICKETS_CONFIG):
            with open(TICKETS_CONFIG, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        with open(TICKETS_CONFIG, 'w') as f:
            json.dump(self.config, f, indent=4)

    @commands.command(name='setuptickets')
    @commands.has_permissions(manage_guild=True)
    async def setuptickets(self, ctx, channel: discord.TextChannel = None):
        """Configure le système de tickets

        Crée un message avec un bouton pour créer des tickets
        """
        if not channel:
            channel = ctx.channel

        guild_id = str(ctx.guild.id)
        if guild_id not in self.config:
            self.config[guild_id] = {}

        # Créer la catégorie "Tickets" si elle n'existe pas
        tickets_category = discord.utils.get(ctx.guild.categories, name="Tickets")
        if not tickets_category:
            tickets_category = await ctx.guild.create_category("Tickets")

        self.config[guild_id]['tickets_category'] = tickets_category.id
        self.config[guild_id]['tickets_channel'] = channel.id
        self.save_config()

        # Envoyer le message avec le bouton
        embed = discord.Embed(
            title="🎫 Système de Tickets",
            description="Clique sur le bouton ci-dessous pour créer un ticket et nous contacter!",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="Comment ça marche?",
            value="""
1. Clique sur 'Créer un ticket'
2. Décris ton problème dans le salon créé
3. Un modérateur t'aidera
4. Ferme le ticket quand c'est résolu
            """,
            inline=False
        )
        embed.set_footer(text="Les tickets fermés ne peuvent pas être rouverts")

        view = discord.ui.View(timeout=None)
        view.add_item(TicketButton(self))

        await channel.send(embed=embed, view=view)

        embed_config = discord.Embed(
            title="✅ Système de tickets configuré",
            description=f"Le bouton pour créer des tickets est dans {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed_config)

    @commands.command(name='closeticket')
    @commands.has_permissions(manage_channels=True)
    async def closeticket(self, ctx):
        """Ferme le ticket actuel"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("❌ Cette commande ne marche que dans un ticket!")
            return

        embed = discord.Embed(
            title="⏳ Fermeture du ticket",
            description="Ce ticket sera fermé dans 5 secondes...",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        import asyncio
        await asyncio.sleep(5)
        await ctx.channel.delete()

    @commands.command(name='addticket')
    @commands.has_permissions(manage_channels=True)
    async def addticket(self, ctx, member: discord.Member):
        """Ajoute un membre au ticket actuel"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("❌ Cette commande ne marche que dans un ticket!")
            return

        if member.bot:
            await ctx.send("❌ Tu ne peux pas ajouter un bot!")
            return

        await ctx.channel.set_permissions(member, view_channel=True, send_messages=True)

        embed = discord.Embed(
            title="✅ Membre ajouté",
            description=f"{member.mention} a été ajouté au ticket",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='removeticket')
    @commands.has_permissions(manage_channels=True)
    async def removeticket(self, ctx, member: discord.Member):
        """Retire un membre du ticket actuel"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("❌ Cette commande ne marche que dans un ticket!")
            return

        await ctx.channel.set_permissions(member, view_channel=False, send_messages=False)

        embed = discord.Embed(
            title="✅ Membre retiré",
            description=f"{member.mention} a été retiré du ticket",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
