import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
GUILD = os.getenv("GUILD_ID")

load_dotenv()

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading the !sync text prefix command

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. Define a sample global slash command
@bot.tree.command(name="ping", description="Responds with a pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")

@bot.tree.command(name="register", description="Register for Werewolf game")
async def register(interaction: discord.Interaction):
    await interaction.response.send_message('Registering!', ephemeral=True)

# 2. Define the manual sync prefix command
@bot.command()
@commands.is_owner()  # Restricts execution to the bot owner only
async def sync(ctx: commands.Context, guild_id: str = None):
    if guild_id is None:
        # Sync globally across all servers (Can take a few minutes to cache)
        synced = await bot.tree.sync()
        await ctx.send(f"Successfully synced {len(synced)} global commands.")
    else:
        # Instantly sync to a specific test server for development
        guild_obj = discord.Object(id=int() if not guild_id.isdigit() else int(guild_id))
        bot.tree.copy_global_to(guild=guild_obj)
        synced = await bot.tree.sync(guild=guild_obj)
        await ctx.send(f"Successfully synced {len(synced)} commands to guild {guild_id}.")

bot.run(os.getenv("API_KEY"))
