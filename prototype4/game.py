from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
from map import Map
import csv, random, copy
"""
Prototyp 4

Notering - Inget är färdigt och ändringar i metoder och attributer kommer fortfarande ske
Lagt till:
map.py
lagt till en karta med movement-mechanics, up, ner, vänster, höger

för det mesta skrivit klart player-action logiken för en encounter, vilket inkluderar:
byta ut pokemon,
items för healing/pokeballs,

lagt till nya funktioner för ett nytt import system av pokemon för att undvika hantera för många klasser samtidigt

Ändringar:
Små attribut datatyps förändringar för vissa klasser
Max-health mechanic
Lagt till en enemyAttackMetod i encounter för bättre logik
Förändrat pass till continue på ställen där det är färdigt


"""
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

def mapUI():
    pass

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