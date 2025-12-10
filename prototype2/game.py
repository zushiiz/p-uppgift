from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
import csv
import random
"""
Prototyp2

Notering - Inget är färdigt och ändringar i metoder och attributer kommer fortfarande ske
Lagt till:
Pokemon klass
En klass som hanterar en pokemons stats, hp, attacker, osv
Dens attribut är klasserna under och några fler

Attack klass
Gör inte så mycket just nu, beräknar hur mycket skada en attack gör

Moveset klass
En pokemon kan bara ha en viss mängd attacker så denna klass hanterar det

Leveling klass
Hanterar en pokemons exp nivå, level, om den kan evolva osv

Stats klass
Hanterar en pokemons stats som är nummer, såsom hp, atk, def, spd och har metoder för att öka/minska

importPokemon funktion
tar in en fil och skapar en lista av Pokemon objekt baserat på fildatan

Ändringar:
Tog bort "print("Hello World!)"
"""

def importPokemon(fileName):
    pokemonList = []
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            # Work in progress
            stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
            level = Leveling(object["Level"], object["Can_evolve"], object["Stage"])
            pokemonList.append(Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"]))
    return pokemonList

def main():
    l = importPokemon("data.txt")
    p1 = Pokemon("aba")
    p2 = Pokemon("bab")
    p1.gainExp(10000, l)
    p1.attack(p2, 0)
    p1.gainExp(100000, l)
    print(p1.name)

main()