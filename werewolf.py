"""
A game of werewolf where there are a set number of roles and you can define more.

The game then proceeds to play with players sending in their votes for their roles and/or village lynching
"""
class WerewolfGame:
    roles = dict()
    available_roles = ["werewolf","villager","seer",""]
    players = set()
    mod = None
    has_game_started = False

    def __init__(self):
        None

    def populate_roles(self, num_players):
        n = num_players
        self.roles["seer"] = 1
        self.roles["doctor"] = 1
        self.roles["hunter"] = 1
        if 6 <= n < 9:
            self.roles["werewolf"] = 2
            self.roles["villager"] = n - 5
            return "Assigned roles."
        elif 9 <= n < 13:
            self.roles["werewolf"] = 3
            self.roles["villager"] = n - 6
            return "Assigned roles."
        elif 13 <= n < 17:
            self.roles["werewolf"] = 4
            self.roles["villager"] = n - 7
            return "Assigned roles."
        elif 17 <= n < 21:
            self.roles["werewolf"] = 5
            self.roles["villager"] = n - 8
            return "Assigned roles."
        else:
            self.roles.clear()
            return "Unable to assign."


    def get_roles(self):
        return_string = "The current roles are as follows,"
        for role in self.roles:
            return_string += "\n"
            return_string += f"{role}: {self.roles[role]}"
        return return_string

    def add_role(self, role_name):
        return 0
    
    def remove_role(self, role_name):
        return 0
    
    def register(self, player_name):
        print(self.has_game_started)
        if not self.has_game_started:
            self.players.add(player_name)
            return "You have successfully registered!"
        else:
            return "Game has started, please wait until it ends to join in."

    def get_players(self):
        return_string = "The current list of players are: "
        for player in self.players:
            return_string += f"{player.name}, "

        return return_string[:len(return_string)-2]

    def register_mod(self, player):
        if self.mod is None:
            self.mod = player
            return f"{self.mod.name} is now the moderator of your werewolf game."
        else:
            return f"There is already a moderator in your werewolf game: {self.mod.name}."
        
    def is_mod(self, user):
        return user.id == self.mod.id

    def assign_roles(self, user):
        if user.id == self.mod.id:
            self.has_game_started = True
            return "Roles have been assigned"
        else:
            return "You are not the moderator."
    
    def run(self):
        # this has the logic for running the whole game
        # it ends when the game has ended
        # it will have to wait for responses which makes this really difficult
        # actually
        return 0