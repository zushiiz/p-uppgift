from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
from map import Map
import csv, random

# def importPokemon(fileName):
#     pokemonList = []
#     with open(fileName, "r", encoding="utf-8") as csvFile:
#         reader = csv.DictReader(csvFile)
#         for object in reader:
#             stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
#             level = Leveling(object["Level"], object["Can_evolve"], object["Stage"])
#             pokemonList.append(Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"]))
#     return pokemonList

def importPokemonNames(fileName):
    pokemonList = []
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            pokemonList.append(object["Pokemon_name"])
    return pokemonList

def importPokemonByName(fileName, pokemonName):
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            if object["Pokemon_name"].lower() == pokemonName.lower():
                stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
                level = Leveling(object["Level"], object["Can_evolve"], object["Stage"])
                return Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"])

def mainLoop():
    map = Map()
    while True:
        Map().userInterface()

def generatePokemon(player, pokemonNames):
    playerLevels = []
    for pokemon in player.team:
        playerLevels.append(pokemon.level.lvl)
    playerLevels.sort()
    level = random.randint(playerLevels[0], len(playerLevels)-1)
    nameIndex = random.randint(0, len(pokemonNames)-1)

    enemy = importPokemonByName("data.txt", pokemonNames[nameIndex])

def main():
    l = importPokemonNames("data.txt")
    for e in l:
        print(e)

    # p = importPokemonByName("data.txt", l[random.randint(0,len(l)-1)])
    # print(p)
    playerTeam = [importPokemonByName("data.txt", "Bulbasaur"), importPokemonByName("data.txt", "Charmander"), importPokemonByName("data.txt", "Bulbasaur")]
    enemy = importPokemonByName("data.txt", "Squirtle")
    player = Player("Me", playerTeam)

    encounter = Encounter(player, enemy)
    encounter.startEncounter()
    print("Encounter stopped")


main()