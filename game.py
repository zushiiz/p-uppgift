from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
from map import Map
import csv, random

class MainGame:
    def __init__(self, fileName):
        self.file = fileName
        self.masterList = importPokemonNames(self.file) # All pokemon names

        playerTeam = [importPokemonByName(self.file, "Bulbasaur"), importPokemonByName(self.file, "Charmander"), importPokemonByName(self.file, "Bulbasaur")]
        self.player = Player("Me", playerTeam)   

        self.enemy = None
         
    
    def generateRandomEnemy(self):
        playerLevels = []
        for pokemon in self.player.team:
            playerLevels.append(pokemon.leveling.lvl)
        playerLevels.sort()
        level = random.randint(playerLevels[0], len(playerLevels)-1)
        nameIndex = random.randint(0, len(self.masterList)-1)
        self.enemy = importPokemonByName(self.file, self.masterList[nameIndex], level)
    
    def startMenu(self):
        while True:
            print("Welcome!")
            print("[0] New Game\n" \
                  "[1] Load Game\n" \
                  "[2] Quit Game")
            try:
                userInput = int(input("What would you like to do?:"))
                match userInput:
                    case 0:
                        break
                    case 1:
                        #import a team
                        break
            except ValueError:
                print("Enter int") #Change later
                continue

        



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

def importPokemonByName(fileName, pokemonName, level = None):
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:
            if object["Pokemon_name"].lower() == pokemonName.lower():
                if level == None:
                    level = object["Level"]
                stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
                level = Leveling(level, object["Can_evolve"], object["Stage"])
                return Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"])

# def mainLoop():
#     map = Map()
#     while True:
#         Map().userInterface()

# def generatePokemon(player, pokemonNames):
#     playerLevels = []
#     for pokemon in player.team:
#         playerLevels.append(pokemon.level.lvl)
#     playerLevels.sort()
#     level = random.randint(playerLevels[0], len(playerLevels)-1)
#     nameIndex = random.randint(0, len(pokemonNames)-1)

#     enemy = importPokemonByName("data.txt", pokemonNames[nameIndex])

def main():
    # l = importPokemonNames("data.txt")
    # for e in l:
    #     print(e)

    # # p = importPokemonByName("data.txt", l[random.randint(0,len(l)-1)])
    # # print(p)
    # playerTeam = [importPokemonByName("data.txt", "Bulbasaur"), importPokemonByName("data.txt", "Charmander"), importPokemonByName("data.txt", "Bulbasaur")]
    # enemy = importPokemonByName("data.txt", "Squirtle")
    # player = Player("Me", playerTeam)

    # encounter = Encounter(player, enemy)
    # encounter.startEncounter()
    # print("Encounter stopped")
    game = MainGame("data.txt")
    game.generateRandomPokemon()


main()