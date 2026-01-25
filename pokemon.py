from attack import *
from stats import Stats
from leveling import Leveling

class Pokemon(): 
    def __init__(self, name, stats = Stats(), moves = MoveList(Attack("Scratch")), leveling = Leveling(), nextEvolution = "a"): #Change some default data
        self.name = name

        self.stats = stats
        self.leveling = leveling
        if self.leveling.lvl > 1:
            self.stats.increaseAllStats(self.leveling.lvl)
        self.attacks = moves

        self.evolution = nextEvolution
        #add a block to higher level to evole if its stage 1
        if self.leveling.stage == 0: # Logic here is not uuh optimal
            self.levelToEvolve = 16
        else:
            self.levelToEvolve = 32 # Temp

        self.fainted = False

    def __str__(self):
        if self.fainted == True:
            return (f"{self.name}, fainted")
        return (f"{self.name}, lvl:{self.leveling.lvl}")
    
    def gainExp(self, exp):
        self.leveling.increaseExperience(exp)
        self.stats.increaseAllStats(self.leveling.lvl)

    def evolve(self, evolution):
        self.name = evolution.name
        self.leveling.stage += 1
        self.levelToEvolve = 36
        self.stats.increaseAllBaseStats()
        self.leveling.canEvolve = evolution.leveling.canEvolve
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        print(round(dmg*0.3-(self.stats.defense*0.1)))
        self.stats.decreaseHealth(round(dmg * 0.3 - (self.stats.defense * 0.1)))
        if self.stats.hp <= 0:
            self.fainted = True
