import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} est connecté!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="le serveur | !help"
    ))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions pour cette commande.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        logger.error(f'Erreur: {error}')
        await ctx.send(f"❌ Une erreur s'est produite: {error}")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            logger.info(f'Cog chargé: {filename}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
