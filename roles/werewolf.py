from game_role import GameRole
from enums.alignment import Alignment

class Werewolf(GameRole):
    def __init__(self, bot):
        super().__init__(bot, Alignment.evil)

    