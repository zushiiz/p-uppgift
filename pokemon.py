from attack import *
from stats import Stats
from leveling import Leveling

class Pokemon(): 
    def __init__(self, name, stats = Stats(), moves = MoveList(Attack("Scratch")), leveling = Leveling(), nextEvolution = "Abba"): #Change some default data
        self.name = name

        self.stats = stats
        self.leveling = leveling
        self.attacks = moves

        self.evolution = nextEvolution
        self.levelToEvolve = 16

        self.fainted = False

    def __str__(self):
        return (f"{self.name},\nlvl.{self.leveling.lvl}")
    
    def gainExp(self, exp, pokemonList):
        self.leveling.increaseExperience(exp, self.stats)
        while self.leveling.lvl >= self.levelToEvolve:
            userInput = input(f"{self.name} is evolving! y/n?").lower()
            match userInput:
                case "y":
                    updatedEvolution = getEvolutionName(pokemonList, self)
                    self.evolve(updatedEvolution)
                case "n":
                    break
                case _:
                    pass
    
    def evolve(self, newNextEvolution):
        self.name = self.evolution
        self.stats.baseAtk += 1
        self.stats.baseHp += 1
        self.stats.baseDef += 1
        self.evolution = newNextEvolution
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        self.stats.decreaseHealth(round((self.stats.defense * 0.001) * dmg))
        if self.stats.hp <= 0:
            self.fainted = True
        else:
            pass

def getEvolutionName(pokemonList, pokemonObj):
    for e in pokemonList:
        if e.name == pokemonObj.evolution:
            if pokemonObj.leveling.canEvole == False:
                return e.name
            else:
                return e.evolution
        else: # Byt till pass?
            print("bombaclat")