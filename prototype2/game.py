from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
import csv
import random

def importPokemon(fileName):
    pokemonList = []
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
            level = Leveling(object["Level"], object["Evolve"], object["Stage"])
            pokemonList.append(Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"]))
    return pokemonList
#change
def main():
    l = importPokemon("data.txt")
    p1 = Pokemon("aba")
    p2 = Pokemon("bab")
    p1.gainExp(10000, l)
    p1.attack(p2, 0)
    p1.gainExp(100000, l)
    print(p1.name)

main()