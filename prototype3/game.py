from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
import csv
import random
"""
Prototyp 3

Notering - Inget är färdigt och ändringar i metoder och attributer kommer fortfarande ske
Lagt till:
Player klass
Encounter klass

jobbat med fight metoden (inte klar), gjort så att den kan hantera spelar input och starta en encounter

Ändringar:
Små attribut datatyps förändringar för vissa klasser
Evolution metoden hos pokemon bör fungera för det mesta nu

"""
def importPokemon(fileName):
    pokemonList = []
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
            level = Leveling(object["Level"], object["Can_evolve"], object["Stage"])
            pokemonList.append(Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"]))
    return pokemonList

def main():
    l = importPokemon("data.txt")
    playerTeam = [l[0]]
    enemy = l[4]
    player = Player("Me", playerTeam)

    encounter = Encounter(player, enemy)
    encounter.startEncounter()
    print("Encounter stopped")

main()