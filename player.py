class Player:
    """
    Class desc:
    Handles team management, swapping, and healing Pokémon
    """
    def __init__(self, username = "Guest", team = ["Empty"]): # Defines attributes for the class when initializing
        """
        :param username: string
        :param team: [Pokemon(), ...]
        """
        self.name = username
        self.team = team
        self.activePokemon = team[0]

        self.potions = 10
        self.pokeballs = 10
    
    def __str__(self): # Returns the player name as a string
        return (f"User: {self.name}")
    
    def swapOption(self, index): # Changes active pokemon for an encounter
        """
        :param index: integer
        """
        print(f"Swapped {self.activePokemon} to {self.team[index]}")
        self.activePokemon = self.team[index+1] # Silvertape fix bruuuh         
    
    def healPokemon(self, pokemon): # Increases health of a pokemon on the team
        """
        :param pokemon: Pokemon()
        """
        pokemon.stats.increaseHealth(100) #Healing amount hardcoded
        self.potions -= 1
        print(f"After healing {pokemon.stats}")

    def changeActivePokemon(self, index): # Changes team order and active pokemon
        """
        :param index: integer
        """
        self.team.insert(0, self.team.pop(index))
        self.activePokemon = self.team[0]