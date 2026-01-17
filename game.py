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

        self.player = None
        self.map = Map()
        self.run = False
    
    def generateRandomEnemy(self):
        playerLevels = []
        for pokemon in self.player.team:
            playerLevels.append(pokemon.leveling.lvl)
        playerLevels.sort()
        level = random.randint(playerLevels[0], playerLevels[len(playerLevels)-1])
        nameIndex = random.randint(0, len(self.masterList)-1)
        enemy = importPokemonByName(self.file, self.masterList[nameIndex], level)
        return enemy

    def mainGameLoop(self):
        while self.run:
            x = self.map.userInterface()
            match x:
                case 0:
                    self.player.changeActivePokemon()
                case 1:
                    self.run = exportPlayerTeam(self.player.team)
                case _:
                    enemy = self.generateRandomEnemy()
                    encounterInstance = Encounter(self.player, enemy)
                    encounterInstance.startEncounter()
                    print(encounterInstance.playerWin)
                    if encounterInstance.playerWin == True:
                        expGained = encounterInstance.opponent.leveling.droppedExp
                        updatedEvoultion, canStillEvolve = getEvolutionName(self.masterList, self.player.activePokemon, self.file)
                        self.player.activePokemon.gainExp(10000000, updatedEvoultion, canStillEvolve)
                        self.player.activePokemon.stats.increaseAllStats(self.player.activePokemon.leveling.lvl)
                        print(self.player.activePokemon.leveling)
                    else:
                        continue

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
                        username = input("Input username:")
                        print("Pick your starter!\n"\
                              "[0] Bulbasaur\n"\
                              "[1] Squirtle\n"\
                              "[2] Charmander\n") # No way back, might change later
                        
                        playerStarter = input(":")
                        playerTeam = []
                        match playerStarter:
                            case "0":
                                playerTeam.append(importPokemonByName(self.file, "Bulbasaur"))
                                self.player = Player(username, playerTeam)
                            case "1":
                                playerTeam.append(importPokemonByName(self.file, "Squirtle"))
                                self.player = Player(username, playerTeam)
                            case "2":
                                playerTeam.append(importPokemonByName(self.file, "Charmander"))
                                self.player = Player(username, playerTeam)
                        self.run = True
                        break

                    case 1:
                        userFile = input("OBS! It has to be a file with correct csv Format and in the correct directory!\n" \
                        "Input the FULL filename: ")
                        team = importPlayerTeam(userFile)
                        username = input("Input username:")
                        self.player = Player(username, team)
                        self.importedTeam = True
                        self.run = True
                        break
                    case 2:
                        break
            
            except ValueError:
                print("Enter int") #Change later
                continue
        self.mainGameLoop()

def importPlayerTeam(fileName):
    playerTeam = []
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for object in reader:

            stats = Stats(object["Health"], object["Attack"], object["Defense"], object["Speed"])
            level = Leveling(object["Level"], object["Can_evolve"], object["Stage"])
            playerTeam.append(Pokemon(object["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, object["Next_evolution"]))
    return playerTeam

def exportPlayerTeam(playerTeam):
    while True:
        print("[2] Back")
        userFile = input("Avoid special characters such as '. , ? !' or numbers '1 2 3 4'\n"\
                         "Entering previous file name will override old saves\n"\
                         "Input team name:")
        if userFile.isalpha():
            with open(userFile + ".csv" , "w", encoding="utf-8") as newFile:
                newFile.write("Pokemon_name,Health,Attack,Defense,Speed,Type,Level,Can_evolve,Stage,Next_evolution" + "\n")
                for pokemon in playerTeam:
                    # pokemon.name
                    # pokemon.stats.baseHp
                    # pokemon.stats.baseAtk
                    # pokemon.stats.baseDef
                    # pokemon.stats.spd
                    typing = "n/a"
                    # pokemon.leveling.lvl
                    # pokemon.leveling.can
                    # pokemon.leveling.stage
                    data = f"{pokemon.name},{pokemon.stats.baseHp},{pokemon.stats.baseAtk},{pokemon.stats.baseDef},{pokemon.stats.spd},{typing},{pokemon.leveling.lvl},{pokemon.leveling.canEvolve},{pokemon.leveling.stage}\n"
                    newFile.write(data)
                return False
        elif userFile == "2":
            return True
        else:
            print("Please enter valid input!")
    
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
            
def getEvolutionName(pokemonList, pokemonObj, file):
    for e in pokemonList:
        if e == pokemonObj.evolution:
            p = importPokemonByName(file, e)
            if p.leveling.canEvolve == False:
                return e, False
            else:
                break
    return e, True

def main():
    game = MainGame("data.txt")
    game.startMenu()

main()