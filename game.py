from pokemon import Pokemon
from attack import *
from leveling import Leveling
from stats import Stats
from player import Player
from encounter import Encounter
from map import Map
from gui import GUI
import csv, random

"""
Notes:
Jolteon and Flareon doesnt exist
Bit unbalanced in base stats
No type advantage
No IV farming
No team amount cap
Moves are hardcoded to only scratch for now
Currently there is no error handling for faulty file format

NEED TO CHECK THE MATH ON TS

"""
class MainGame:
    def __init__(self, fileName):
        self.file = fileName
        self.masterList = importPokemonNames(self.file) # All pokemon names

        self.player = None
        self.username = None
        self.map = Map()
        self.run = False
        self.gui = GUI()

    def generateRandomEnemy(self):
        playerLevels = []
        for pokemonObj in self.player.team:
            playerLevels.append(pokemonObj.leveling.lvl)
        playerLevels.sort()
        level = random.randint(playerLevels[0], playerLevels[len(playerLevels)-1])
        nameIndex = random.randint(0, len(self.masterList)-1)
        enemy = importPokemonByName(self.file, self.masterList[nameIndex], level)
        return enemy

    def mainGameLoop(self):
        while self.run:
            menuActionIndex = self.map.userInterface()
            match menuActionIndex:
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
                        nextEvolutions = getEvolutionName(self.masterList, self.player.activePokemon, self.file)
                        self.player.activePokemon.gainExp(expGained, nextEvolutions)
                        print(self.player.activePokemon.leveling)
                    else:
                        continue

    def startMenu(self): # Could split into more functions/methods, also there is no back option from case 0 and 1

        print("Welcome!")

        self.gui.write_line(f"Welcome {self.username}!")

        self.gui.create_actions_box()
        options = ["New Game", "Load Game", "Quit Game"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.startMenuActions(self.gui.actions_box))        
        
        self.mainGameLoop()

    def startMenuActions(self, list_box):     
        userInput = list_box.curselection()
        userInput = int(userInput[0])
        print(userInput)
        match userInput:
            case 0:
                self.gui.write_line("Pick your starter Pokemon!")
                options = ["Bulbasaur", "Squirtle", "Charmander", "Back"]
                self.gui.create_actions_box()
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.newGameMenu(self.gui.actions_box))

            case 1:
                # team = importPlayerTeam()
                # username = input("Input username:")
                # self.player = Player(username, team)
                # self.run = True
                self.loadGameMenu()

    def newGameMenu(self, list_box):
        userInput = int(list_box.curselection()[0])
        print("New Game")
        playerTeam = []
        username = ""
        match userInput:
            case 0:
                playerTeam.append(importPokemonByName(self.file, "Bulbasaur"))
                self.player = Player(username, playerTeam)
                self.run = True
            case 1:
                playerTeam.append(importPokemonByName(self.file, "Squirtle"))
                self.player = Player(username, playerTeam)
                self.run = True
            case 2:
                playerTeam.append(importPokemonByName(self.file, "Charmander"))
                self.player = Player(username, playerTeam)
                self.run = True
            case 3:
                self.gui.clear_action_frame()
                self.startMenu()
        self.mainGameLoop()

    def loadGameMenu(self):
        self.gui.write_line("OBS! It has to be a file with correct csv Format and in the correct directory!\n" \
                            "Input the FULL filename/path in the field")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self.importPlayerTeam(self.gui.input_field.get()))

    def start(self):
        self.gui.write_line("Enter a username")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self._storeUsername(self.gui.input_field.get()))
    
    def _storeUsername(self, input):
        self.username = input
        self.startMenu()
        print(self.username)

    def importPlayerTeam(self, userFile):
        playerTeam = []
        print(userFile)
        try:
            with open(userFile, "r", encoding="utf-8") as csvFile:
                reader = csv.DictReader(csvFile)
                for pokemonData in reader:
                    stats = Stats(pokemonData["Health"], pokemonData["Attack"], pokemonData["Defense"], pokemonData["Speed"])
                    level = Leveling(pokemonData["Level"], pokemonData["Can_evolve"], pokemonData["Stage"])
                    playerTeam.append(Pokemon(pokemonData["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, pokemonData["Next_evolution"]))
            self.player = Player(self.username, playerTeam)
            self.run = True
            self.mainGameLoop()
        except FileNotFoundError:
            print("File not found")


def exportPlayerTeam(playerTeam):
    while True:
        print("[2] Back")
        userFile = input("Avoid special characters such as '. , ? !' or numbers '1 2 3 4'\n"\
                         "Entering previous file name will override old saves\n"\
                         "Input team name:")
        if userFile.isalpha():
            with open(userFile + ".csv" , "w", encoding="utf-8") as newFile:
                newFile.write("Pokemon_name,Health,Attack,Defense,Speed,Type,Level,Can_evolve,Stage,Next_evolution" + "\n")
                for pokeObj in playerTeam:
                    # pokemon.name
                    # pokemon.stats.baseHp
                    # pokemon.stats.baseAtk
                    # pokemon.stats.baseDef
                    # pokemon.stats.spd
                    typing = "n/a"
                    # pokemon.leveling.lvl
                    # pokemon.leveling.can
                    # pokemon.leveling.stage
                    data = f"{pokeObj.name},{pokeObj.stats.baseHp},{pokeObj.stats.baseAtk},{pokeObj.stats.baseDef},{pokeObj.stats.spd},{typing},{pokeObj.leveling.lvl},{pokeObj.leveling.canEvolve},{pokeObj.leveling.stage}\n"
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
        for pokemonData in reader:
            pokemonList.append(pokemonData["Pokemon_name"])
    return pokemonList

def importPokemonByName(fileName, pokemonName, level = None):
    with open(fileName, "r", encoding="utf-8") as csvFile:
        reader = csv.DictReader(csvFile)
        for pokemonData in reader:
            if pokemonData["Pokemon_name"].lower() == pokemonName.lower():
                if level == None:
                    level = pokemonData["Level"]
                stats = Stats(pokemonData["Health"], pokemonData["Attack"], pokemonData["Defense"], pokemonData["Speed"])
                level = Leveling(level, pokemonData["Can_evolve"], pokemonData["Stage"])
                return Pokemon(pokemonData["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, pokemonData["Next_evolution"])
            
def getEvolutionName(pokemonList, pokemonObj, file):
    evolutionDict = {}
    for pokemonName in pokemonList:
        if pokemonName == pokemonObj.evolution:
            pokemonObj = importPokemonByName(file, pokemonName)
            evolutionDict[pokemonObj.name] = True
            if pokemonObj.leveling.canEvolve == True:
                evolutionDict[importPokemonByName(file, pokemonObj.evolution).name] = False
            else:
                break
    return evolutionDict

def main():

    game = MainGame("data.txt") # Hardcoded :thumbs_up:
    game.start()
    game.gui.root.mainloop()

main()