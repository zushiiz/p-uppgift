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
        self.levelToEvolve = 16

        self.fainted = False

    def __str__(self):
        if self.fainted == True:
            return (f"{self.name}, fainted")
        return (f"{self.name}, lvl:{self.leveling.lvl}")
    
    def gainExp(self, exp, nextEvolutions):
        self.leveling.increaseExperience(exp)
        self.stats.increaseAllStats(self.leveling.lvl)
        nameKeyList = []
        nameKeysDict = nextEvolutions.keys()
        for key in nameKeysDict:
            nameKeyList.append(key)
        nextEvolutionName = nameKeyList[0]

        while self.leveling.lvl >= self.levelToEvolve and self.leveling.canEvolve == True:          
            userInput = input(f"{self.name} is evolving! y/n?").lower()
            match userInput:
                case "y":
                    print(nextEvolutionName)
                    canStillEvolve = nextEvolutions[nextEvolutionName]                    
                    self.evolve(nextEvolutionName, canStillEvolve)
                    self.levelToEvolve = 36
                case "n":
                    break
                case _:
                    continue
            if self.leveling.lvl >= self.levelToEvolve and self.leveling.canEvolve == True:  
                nextEvolutionName = nameKeyList[1]
            else:
                break
        
    def evolve(self, newName, canStillEvolve):
        self.name = newName
        self.leveling.stage += 1  
        self.stats.increaseAllBaseStats()
        self.leveling.canEvolve = canStillEvolve
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        print(round(dmg*0.3-(self.stats.defense*0.1)))
        self.stats.decreaseHealth(round(dmg * 0.3 - (self.stats.defense * 0.1)))
        if self.stats.hp <= 0:
            self.fainted = True
