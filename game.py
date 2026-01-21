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

    def generateRandomEnemy(self): # Generates one random pokemon object for an encounter
        """
        Parameters: None
        Return values: enemy=Pokemon()
        """
        playerLevels = []
        for pokemonObj in self.player.team:
            playerLevels.append(pokemonObj.leveling.lvl)
        playerLevels.sort() # Level balancing
        level = random.randint(playerLevels[0], playerLevels[len(playerLevels)-1])
        nameIndex = random.randint(0, len(self.masterList)-1)
        enemy = importPokemonByName(self.file, self.masterList[nameIndex], level)
        return enemy

    def start(self): # Program starting point
        """
        Parameters: None
        Return values: None
        """        
        self.gui.write_line("Enter a username")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self._storeUsername(self.gui.input_field.get()))

    def startMenu(self): # Initiates/Creates starting menu
        """
        Parameters: None
        Return values: None
        """
        print("Starting Menu...")
        self.gui.write_line(f"Welcome {self.username}!")
        self.gui.create_actions_box()
        options = ["New Game", "Load Game", "Quit Game"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.startMenuActions(self.gui.actions_box))        

    def startMenuActions(self, list_box): # Handles the logic for if user wants to load or create new game
        """
        Parameters: list_box=tk.Listbox
        Return values: None
        """
        userInput = list_box.curselection()
        userInput = int(userInput[0])
        print(f"User input: {userInput}")
        match userInput:
            case 0: # Prepares menu and parameters for newGameMenu() method
                self.gui.write_line("Pick your starter Pokemon!")
                options = ["Bulbasaur", "Squirtle", "Charmander", "Back"]
                self.gui.create_actions_box()
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.newGameMenu(self.gui.actions_box))

            case 1:
                self.loadGameMenu()

    def newGameMenu(self, list_box): # Menu that lets user choose starter pokemon
        """
        Parameters: list_box=tk.Listbox
        Return values: None
        """        
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
            case _:
                self.gui.clear_action_frame()
                self.startMenu()

        self.mapGui()

    def loadGameMenu(self): # Menu that lets user import own file with correct format
        """
        Parameters: None
        Return values: None
        """                
        self.gui.write_line("OBS! It has to be a file with correct csv Format and in the correct directory!\n" \
                            "Input the FULL filename/path in the field")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self.importPlayerTeam(self.gui.input_field.get()))
    
    def _storeUsername(self, input): # Updates the username attribute
        """
        Parameters: input=string
        Return values: None
        """
        if input == "":
            self.username = "Guest"
            print("Guest user")
        else:
            self.username = input
            print(f"updated - self.username={self.username}")
        self.startMenu()      

    def importPlayerTeam(self, userFile): # Imports the file that user enters
        """
        Parameters: userFile=string(file path)
        Return values: None 
        """        
        playerTeam = []
        print(f"Importing file:{userFile}")
        try:
            with open(userFile, "r", encoding="utf-8") as csvFile:
                reader = csv.DictReader(csvFile)
                for pokemonData in reader:
                    stats = Stats(pokemonData["Health"], pokemonData["Attack"], pokemonData["Defense"], pokemonData["Speed"])
                    level = Leveling(pokemonData["Level"], pokemonData["Can_evolve"], pokemonData["Stage"])
                    playerTeam.append(Pokemon(pokemonData["Pokemon_name"], stats, MoveList(Attack("Scratch")), level, pokemonData["Next_evolution"]))
            self.player = Player(self.username, playerTeam)
            print("Import successful, running game")
            self.run = True
            self.mapGui()
        except FileNotFoundError:
            print("Import failed\nError: File not found")

    def mapGui(self): # Creates/Formats the gui for the map and dpad
        """
        Parameters: None
        Return values: None
        """
        if self.run == True:
            print("Run successful")
            self.gui.disable_terminal()
            self.gui.show_map(self.map)
            self.gui.clear_action_frame()
            self.gui.write_line("Started game! Use w/a/s/d to walk around!")
    
            options = ["Team", "Quit"]
            self.gui.update_listbox(options)

            self.gui.create_dpad()
            self.gui.up.config(command = lambda: (self.map.movePlayer(0, -1), self.gui.refresh_map(self.map)))
            self.gui.down.config(command = lambda: (self.map.movePlayer(0, 1), self.gui.refresh_map(self.map)))
            self.gui.left.config(command = lambda: (self.map.movePlayer(-1, 0), self.gui.refresh_map(self.map)))
            self.gui.right.config(command = lambda: (self.map.movePlayer(1, 0), self.gui.refresh_map(self.map)))

            # menuActionIndex = self.map.userInterface()
            # match menuActionIndex:
            #     case 0:
            #         self.player.changeActivePokemon()
            #     case 1:
            #         self.run = exportPlayerTeam(self.player.team)
            #     case _:
            #         enemy = self.generateRandomEnemy()
            #         encounterInstance = Encounter(self.player, enemy)
            #         encounterInstance.startEncounter()
            #         print(encounterInstance.playerWin)
            #         if encounterInstance.playerWin == True:
            #             expGained = encounterInstance.opponent.leveling.droppedExp
            #             nextEvolutions = getEvolutionName(self.masterList, self.player.activePokemon, self.file)
            #             self.player.activePokemon.gainExp(expGained, nextEvolutions)
            #             print(self.player.activePokemon.leveling)
            #         else:
            #             continue

def exportPlayerTeam(playerTeam):
    """
    Parameters: playerTeam=[Pokemon(), ...]
    Return values: Boolean
    """
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