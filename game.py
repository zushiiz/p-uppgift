from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
import csv, random, copy

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

    l2 = copy.deepcopy(l)
    b1 = l2[0]
    b2 = l[0]
    # playerTeam = [b1, l[3], b2]
    # enemy = l[4]
    # player = Player("Me", playerTeam)

    # encounter = Encounter(player, enemy)
    # encounter.startEncounter()
    # print("Encounter stopped")

    b1.fainted = True
    print(b1.fainted)
    print(b2.fainted)


main()