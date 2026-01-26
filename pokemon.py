from attack import *
from stats import Stats
from leveling import Leveling

class Pokemon(): 
    """
    Class desc:
    Handles experience gain, stat scaling, attacking, taking damage, fainting, and evolution logic
    """
    def __init__(self, name, stats = Stats(), moves = Movelist(Attack("Scratch")), leveling = Leveling(), nextEvolution = "a"): # Defines attributes for the class when initializing
        """
        :param name: string
        :param stats: Stats()
        :param moves: Movelist()
        :param leveling: Leveling()
        :param nextEvolution: string
        """
        self.name = name

        self.stats = stats
        self.leveling = leveling
        if self.leveling.lvl > 1: # Adjusts stats based on level
            self.stats.increaseAllStats(self.leveling.lvl)
        self.movelist = moves

        self.evolution = nextEvolution
        # add a block to higher level to evole if its stage 1
        if self.leveling.stage == 0: # Logic here is not uuh optimal
            self.levelToEvolve = 16
        else:
            self.levelToEvolve = 32 # Temp

        self.fainted = False

    def __str__(self): # Returns name as string, adds fainted if it is fainted
        if self.fainted == True:
            return (f"{self.name}, fainted")
        return (f"{self.name}")
    
    def gainExp(self, exp): # Increases exp data
        """
        :param exp: integer
        """
        self.leveling.increaseExperience(exp)
        self.stats.increaseAllStats(self.leveling.lvl)

    def evolve(self, evolution): # Updates all necessary data when evolving
        """
        :param evolution: Pokemon()
        """
        self.name = evolution.name
        self.leveling.stage += 1
        self.levelToEvolve = 36
        self.stats.increaseAllBaseStats()
        self.leveling.canEvolve = evolution.leveling.canEvolve
    
    def attack(self, other, atkIndex): # Calls upon damaged()-method on another pokemon-object
        """
        :param other: Pokemon()
        :param attack: integer
        """
        other.damaged(self.movelist[atkIndex].attack(self.stats.atk))

    def damaged(self, dmg): # Decreases health stat
        """
        :param dmg: integer
        """
        print(f"{self.name} - Damage recieved: {round(dmg*0.3-(self.stats.defense*0.1))}")
        self.stats.decreaseHealth(round(dmg * 0.3 - (self.stats.defense * 0.1)))
        if self.stats.hp <= 0:
            self.fainted = True
