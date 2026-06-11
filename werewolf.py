import json
import random

"""
A game of werewolf where there are a set number of roles and you can define more.

The game then proceeds to play with players sending in their votes for their roles and/or village lynching
"""
class WerewolfGame:
    available_roles = ["werewolf","villager","seer","doctor","hunter","tracker",
                       "tanner","spellcaster","guard","tough villager","witch",
                       "vigilante","sneaky werewolf", "werewolf cub","town crier",
                       "lovers","chupacabra","graverobber"]
    players = set()
    mod = None
    has_game_started = False
    player_assignment = dict()

    def __init__(self):
        with open("roles.json", "r") as file:
            self.ROLE_DATA = json.load(file)
        self.roles = dict()
        

    
    def get_player_assignment(self):
        return self.player_assignment


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


    def add_role(self, role_name, num):
        if not self.has_game_started:
            self.roles[role_name] = self.roles.get(role_name, 0) + num
            return f"{num} {role_name} have been added."
        else:
            return "Game has started, you cannot add a new role now."
    

    def remove_role(self, role_name, num):
        if not self.has_game_started:
            if role_name in self.roles:
                self.roles[role_name] = self.roles[role_name] - num
                if self.roles[role_name] < 0:
                    self.roles.pop(role_name)
                return f"{num} {role_name} have been removed."
            else:
                return "Role was not in the game."
        else:
            return "Game has started, you cannot remove a role now."
    

    def register(self, player):
        if not self.has_game_started:
            self.players.add(player)
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
        

    def unclaim_mod(self, player):
        if self.is_admin_or_mod(player.roles) or self.is_mod(player):
            self.mod = None
            return "Werewolf moderator has been successfully unclaimed. Please register next moderator for your game."
        else:
            return "You do not have permission to remove the moderator."
        

    def is_mod(self, user):
        if self.mod is None:
            return False
        else:
            return user.id == self.mod.id
        
    
    def is_admin_or_mod(self, roles):
        for role in roles:
            if "Moderator" in role.name or "Admin" in role.name:
                return True
        return False

    def assign_roles(self, user):
        if self.is_mod(user):

            if self.has_game_started:
                return "Game has started. You can't assign roles now."

            if (len(self.players) <= self.num_roles()):
                players = self.players.copy()
                roles = self.get_roles_as_list()
                
                while (len(players) > 0):
                    player = players.pop()
                    role = roles.pop(random.randint(0, len(roles) - 1))
                    self.player_assignment[player] = role

                self.has_game_started = True
                return "Roles have been assigned"
            else:
                return "Not enough roles to give all players."  
        else:
            return "You are not the moderator."
        
    
    def list_player_roles(self, user):
        if self.is_mod(user):
            return_string = "The player roles:"
            
            for player, role in self.player_assignment.items():
                return_string += "\n"
                return_string += f"{player}: {role}"
            
            return return_string
        else:
            return "You are not the moderator."
        

    def end_game(self, user):
        if self.is_mod(user):
            self.has_game_started = False
            return "Game has ended."
        else:
            return "You are not the moderator."
        
    
    def num_roles(self):
        num = 0
        for _, qty in self.roles.items():
            num += qty
        return num
    

    def get_roles_as_list(self):
        list = []
        for role, qty in self.roles.items():
            for _ in range(qty):
                list.append(role)
        return list


async def run_game(guild):
    """The core engine loop that automates transitions using non-blocking sleep intervals."""
    town_channel = guild.get_channel(game.town_channel_id)
    
    while game.is_active:
        # ==========================================
        # 1. NIGHT PHASE (60 Seconds)
        # ==========================================
        await transition_to_night(guild)
        await town_channel.send("⏱️ *The night will last 60 seconds. Werewolves, choose your prey.*")
        
        # Non-blocking pause: allows the bot to listen to !kill commands inside the den
        await asyncio.sleep(60) 
        
        # ==========================================
        # 2. MORNING TRANSITION
        # ==========================================
        await transition_to_day(guild)
        
        # If a win condition was hit during morning calculations, break out immediately
        if not game.is_active:
            break
            
        # ==========================================
        # 3. DAY DISCUSSION & VOTING PHASE (120 Seconds)
        # ==========================================
        await town_channel.send("⏱️ *You have 2 minutes to discuss, accuse, and vote using `!vote @player`.*")
        
        # Wait for either the timer to expire OR a sudden majority vote to trigger early
        # We check the state every 5 seconds to see if an early execution stopped the phase
        timer = 120
        while timer > 0 and game.phase == "Voting":
            await asyncio.sleep(5)
            timer -= 5
            
        # If the timer ran out and no majority was hit, process a "No Execution" or highest vote
        if game.phase == "Voting" and game.is_active:
            await town_channel.send("⌛ **Time's up!** The sun sets and the town failed to reach a conclusive verdict.")
            # Clear votes and cycle back to night
            game.phase = "Night"
            
        # Small buffer window before the next night starts
        await asyncio.sleep(3)