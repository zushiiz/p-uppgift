from attack import *
from stats import Stats
from leveling import Leveling

class Pokemon(): 
    def __init__(self, name, stats = Stats(), moves = MoveList(Attack("Scratch")), leveling = Leveling(False), nextEvolution = "a"): #Change some default data
        self.name = name

        self.stats = stats
        self.leveling = leveling
        if self.leveling.lvl > 1:
            self.stats.increaseAllStats(self.leveling.lvl)
        self.attacks = moves

        self.evolution = nextEvolution
        self.levelToEvolve = 16

        self.fainted = False

    def __str__(self):
        if self.fainted == True:
            return (f"{self.name}, fainted")
        return (f"{self.name}, lvl:{self.leveling.lvl}")
    
    def gainExp(self, exp, updatedEvolution, canStillEvolve):
        self.leveling.increaseExperience(exp)
        while self.leveling.lvl >= self.levelToEvolve and self.leveling.canEvolve == True:
            userInput = input(f"{self.name} is evolving! y/n?").lower()
            match userInput:
                case "y":
                    self.evolve(updatedEvolution, canStillEvolve)
                case "n":
                    break
                case _:
                    continue
    
    def evolve(self, newNextEvolution, canStillEvolve):
        self.name = self.evolution
        self.leveling.evolutionStage += 1        
        self.leveling.canEvolve = canStillEvolve
        self.evolution = newNextEvolution      
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        self.stats.decreaseHealth(round((self.stats.defense * 0.001) * dmg))
        if self.stats.hp <= 0:
            self.fainted = True
