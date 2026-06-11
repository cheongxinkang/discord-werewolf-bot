from discord.ext import commands

class GameRole(commands.bot):
    def __init__(self, bot, alignment):
        self.bot = bot
        self.alignment = alignment