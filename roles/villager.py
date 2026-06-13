from game_role import GameRole
from enums.alignment import Alignment

class Villager(GameRole):
    def __init__(self, bot):
        super().__init__(bot, Alignment.good)

    