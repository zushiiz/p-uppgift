from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
import csv
import random

def getEvolutionName(pokemonList, pokemonObj):
    for e in pokemonList:
        if e.name == pokemonObj.evolution:
            if pokemonObj.leveling.canEvole == False:
                return e.name
            else:
                return e.evolution
        else: # Byt till pass?
            print("bombaclat")

def main():
    p1 = Pokemon("aba")
    p2 = Pokemon("bab")
    p1.gainExp(10000)
    p1.attack(p2, 0)
    p1.gainExp(10000000)
    print(p1.name)

main()