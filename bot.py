import os
import discord
import werewolf

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
GUILD = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)
game = werewolf.WerewolfGame()

def is_mod():
      async def predicate(ctx):
            return game.is_mod(ctx.author)
      return commands.check(predicate)

# ==========================================
#  DM-ONLY COMMANDS (For Moderator Only)
# ==========================================


@bot.command()
@commands.dm_only() 
@is_mod()
async def cmds(ctx):
    await ctx.send("The commands available to you: !assign_roles")


@bot.command()
@commands.dm_only()
@is_mod()
async def assign_roles(ctx):
    await ctx.send(game.assign_roles(ctx.author))


@bot.command()
@commands.dm_only()
@is_mod()
async def create_roles(ctx, num: int):
      await ctx.send(game.populate_roles(num))


@bot.command()
@commands.dm_only()
@is_mod()
async def add_role(ctx, name:str, num: int):
      await ctx.send(game.add_role(name, num))


@bot.command()
@commands.dm_only()
@is_mod()
async def remove_role(ctx, name:str, num: int):
      await ctx.send(game.remove_role(name, num))


@bot.command()
@commands.dm_only()
@is_mod()
async def get_player_roles(ctx):
      await ctx.send(game.list_player_roles(ctx.author))


# ==========================================
#  SERVER CHANNEL COMMANDS (Anyone Can Use)
# ==========================================

@bot.tree.command(name="register", description="Register for Werewolf game")
async def register(interaction: discord.Interaction):
    await interaction.response.send_message(game.register(interaction.user), ephemeral=True)


@bot.tree.command(name="players", description="Lists current players for the game")
async def players(interaction: discord.Interaction):
      players_message = game.getPlayers()
      await interaction.response.send_message(players_message, ephemeral=True)


@bot.tree.command(name="claim_mod", description="Become the moderator of this werewolf game")
async def claim_mod(interaction: discord.Interaction):
      await interaction.response.send_message(game.register_mod(interaction.user))
      await interaction.user.send("You're the moderator of the werewolf game. DM me privately for mod commands. Use !cmds for list of commands.")


@bot.tree.command(name="unclaim_mod", description="Remove the moderator of this werewolf game")
async def unclaim_mod(interaction: discord.Interaction):
      await interaction.response.send_message(game.unclaim_mod(interaction.user))


@bot.tree.command(name="get_roles", description="Get the list of roles in the game.")
async def get_roles(interaction: discord.Interaction):
      await interaction.response.send_message(game.get_roles())


# Manual Sync Method
@bot.command()
@commands.is_owner()  # Restricts execution to the bot owner only
async def sync(ctx: commands.Context, guild_id: str = GUILD):
    # if guild_id is None:
    #     # Sync globally across all servers (Can take a few minutes to cache)
    #     synced = await bot.tree.sync()
    #     await ctx.send(f"Successfully synced {len(synced)} global commands.")
    # else:
        # Instantly sync to a specific test server for development
        guild_obj = discord.Object(id=int() if not guild_id.isdigit() else int(guild_id))
        bot.tree.copy_global_to(guild=guild_obj)
        synced = await bot.tree.sync(guild=guild_obj)
        await ctx.send(f"Successfully synced {len(synced)} commands to guild {guild_id}.")

bot.run(os.getenv("API_KEY"))
