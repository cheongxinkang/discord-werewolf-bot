"""
A game of werewolf where there are a set number of roles and you can define more.

The game then proceeds to play with players sending in their votes for their roles and/or village lynching
"""
class WerewolfGame:
    roles = dict()
    available_roles = ["werewolf","villager","seer",""]
    players = set()

    def __init__(self, num_players):
        self.populateRoles(num_players)

    def populateRoles(self, num_players):
        self.roles["werewolf"]= 2

    def getRoles(self):
        return 0

    def addRole(self, role_name):
        return 0
    
    def register(self, player_name):
        self.players.add(player_name)
    
    def run(self):
        # this has the logic for running the whole game
        # it ends when the game has ended
        # it will have to wait for responses which makes this really difficult
        # actually
        return 0