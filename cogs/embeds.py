import discord
from discord.ext import commands
import json

class EmbedBuilderModal(discord.ui.Modal):
    def __init__(self, title="Créer un Embed"):
        super().__init__(title=title)
        self.embed_data = {}

        self.title_input = discord.ui.TextInput(
            label="Titre",
            placeholder="Le titre de l'embed",
            required=False,
            max_length=256
        )
        self.description_input = discord.ui.TextInput(
            label="Description",
            placeholder="La description de l'embed",
            required=False,
            style=discord.TextStyle.long,
            max_length=4000
        )
        self.add_item(self.title_input)
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction):
        self.embed_data['title'] = self.title_input.value or "Sans titre"
        self.embed_data['description'] = self.description_input.value or "Sans description"
        await interaction.response.defer()

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='embed')
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx):
        """Crée un embed personnalisé de manière interactive"""
        modal = EmbedBuilderModal()
        await ctx.interaction.response.send_modal(modal) if hasattr(ctx, 'interaction') else None

        embed = discord.Embed(
            title="🎨 Créateur d'Embed",
            description="Utilise les sous-commandes pour créer ton embed",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="Commandes disponibles:",
            value="""
`!embed simple <titre> <description>` - Créer un embed simple
`!embed couleur <couleur_hex>` - Changer la couleur (ex: FF5733)
`!embed image <url>` - Ajouter une image
`!embed thumbnail <url>` - Ajouter une petite image
`!embed auteur <nom>` - Ajouter un auteur
`!embed footer <texte>` - Ajouter un pied de page
`!embed champ <nom> <valeur> [inline]` - Ajouter un champ
            """,
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name='embedsimple')
    @commands.has_permissions(manage_messages=True)
    async def embedsimple(self, ctx, *, content: str):
        """Crée un embed simple

        Utilise | pour séparer le titre de la description
        Exemple: !embedsimple Titre | Description ici
        """
        try:
            parts = content.split('|', 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else "Sans description"
        except:
            await ctx.send("❌ Format incorrect! Utilise: !embedsimple Titre | Description")
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Créé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name='embedcouleur')
    @commands.has_permissions(manage_messages=True)
    async def embedcouleur(self, ctx, color: str, *, content: str):
        """Crée un embed avec une couleur personnalisée

        La couleur doit être en HEX sans # (ex: FF5733)
        Utilise | pour séparer le titre de la description
        """
        try:
            color_int = int(color, 16)
            color_obj = discord.Color(color_int)
        except:
            await ctx.send("❌ Couleur invalide! Utilise le format HEX (ex: FF5733)")
            return

        try:
            parts = content.split('|', 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else "Sans description"
        except:
            await ctx.send("❌ Format incorrect!")
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color_obj
        )
        embed.set_footer(text=f"Créé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name='embedimage')
    @commands.has_permissions(manage_messages=True)
    async def embedimage(self, ctx, url: str, *, content: str):
        """Crée un embed avec une image

        Utilise | pour séparer le titre de la description
        """
        try:
            parts = content.split('|', 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else "Sans description"
        except:
            await ctx.send("❌ Format incorrect!")
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blurple()
        )
        embed.set_image(url=url)
        embed.set_footer(text=f"Créé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name='embedthumbnail')
    @commands.has_permissions(manage_messages=True)
    async def embedthumbnail(self, ctx, url: str, *, content: str):
        """Crée un embed avec une petite image (thumbnail)

        Utilise | pour séparer le titre de la description
        """
        try:
            parts = content.split('|', 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else "Sans description"
        except:
            await ctx.send("❌ Format incorrect!")
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=url)
        embed.set_footer(text=f"Créé par {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.group(name='embednew', invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def embednew(self, ctx):
        """Crée un embed complexe étape par étape

        Utilise les sous-commandes pour construire ton embed
        """
        ctx.embed_builder = {
            'title': 'Sans titre',
            'description': '',
            'color': discord.Color.blurple(),
            'fields': [],
            'image': None,
            'thumbnail': None,
            'author': None,
            'footer': None
        }
        await ctx.send("✅ Embed créé! Utilise les commandes ci-dessous pour le personnaliser")

    @embednew.command(name='titre')
    async def embed_titre(self, ctx, *, title: str):
        """Change le titre de l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['title'] = title
        await ctx.send(f"✅ Titre défini à: {title}")

    @embednew.command(name='description')
    async def embed_description(self, ctx, *, description: str):
        """Change la description de l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['description'] = description
        await ctx.send(f"✅ Description mise à jour")

    @embednew.command(name='couleur')
    async def embed_couleur(self, ctx, color: str):
        """Change la couleur de l'embed (HEX)"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        try:
            color_int = int(color, 16)
            ctx.embed_builder['color'] = discord.Color(color_int)
            await ctx.send(f"✅ Couleur changée à: #{color}")
        except:
            await ctx.send("❌ Couleur invalide! Utilise le format HEX (ex: FF5733)")

    @embednew.command(name='champ')
    async def embed_champ(self, ctx, name: str, *, value: str):
        """Ajoute un champ à l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['fields'].append({'name': name, 'value': value})
        await ctx.send(f"✅ Champ '{name}' ajouté!")

    @embednew.command(name='image')
    async def embed_image(self, ctx, url: str):
        """Ajoute une image à l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['image'] = url
        await ctx.send(f"✅ Image ajoutée!")

    @embednew.command(name='thumbnail')
    async def embed_thumbnail(self, ctx, url: str):
        """Ajoute une petite image à l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['thumbnail'] = url
        await ctx.send(f"✅ Thumbnail ajoutée!")

    @embednew.command(name='auteur')
    async def embed_auteur(self, ctx, *, name: str):
        """Ajoute un auteur à l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['author'] = name
        await ctx.send(f"✅ Auteur défini à: {name}")

    @embednew.command(name='footer')
    async def embed_footer(self, ctx, *, text: str):
        """Ajoute un pied de page à l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return
        ctx.embed_builder['footer'] = text
        await ctx.send(f"✅ Footer défini!")

    @embednew.command(name='apercu')
    async def embed_preview(self, ctx):
        """Affiche un aperçu de l'embed"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return

        builder = ctx.embed_builder
        embed = discord.Embed(
            title=builder['title'],
            description=builder['description'],
            color=builder['color']
        )

        for field in builder['fields']:
            embed.add_field(name=field['name'], value=field['value'], inline=False)

        if builder['image']:
            embed.set_image(url=builder['image'])
        if builder['thumbnail']:
            embed.set_thumbnail(url=builder['thumbnail'])
        if builder['author']:
            embed.set_author(name=builder['author'])
        if builder['footer']:
            embed.set_footer(text=builder['footer'])

        await ctx.send(embed=embed)

    @embednew.command(name='envoyer')
    async def embed_send(self, ctx, channel: discord.TextChannel = None):
        """Envoie l'embed dans un salon"""
        if not hasattr(ctx, 'embed_builder'):
            await ctx.send("❌ Crée d'abord un embed avec !embednew")
            return

        if not channel:
            channel = ctx.channel

        builder = ctx.embed_builder
        embed = discord.Embed(
            title=builder['title'],
            description=builder['description'],
            color=builder['color']
        )

        for field in builder['fields']:
            embed.add_field(name=field['name'], value=field['value'], inline=False)

        if builder['image']:
            embed.set_image(url=builder['image'])
        if builder['thumbnail']:
            embed.set_thumbnail(url=builder['thumbnail'])
        if builder['author']:
            embed.set_author(name=builder['author'])
        if builder['footer']:
            embed.set_footer(text=builder['footer'])

        await channel.send(embed=embed)
        await ctx.send(f"✅ Embed envoyé dans {channel.mention}!")

async def setup(bot):
    await bot.add_cog(Embeds(bot))
