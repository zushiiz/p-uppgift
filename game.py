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
Moves are hardcoded to only scratch - but made to be changed easily in the future
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
        :param : None
        :return enemy: Pokemon()
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
        :param : None
        :return : None
        """        
        self.gui.write_line("Enter a username")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self._storeUsername(self.gui.input_field.get()))

    def startMenu(self): # Initiates/Creates starting menu
        """
        :param : None
        :return : None
        """
        print("Starting Menu...")
        self.gui.write_line(f"Welcome {self.username}!")
        self.gui.create_actions_box()
        options = ["New Game", "Load Game", "Quit Game"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.startMenuActions(self.gui.actions_box))        

    def startMenuActions(self, listbox): # Handles the logic for if user wants to load or create new game
        """
        :param listbox : tk.Listbox
        :return : None
        """
        userInput = listbox.curselection() # Gives tuple of indices
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
            
            case 2:
                quit()

    def newGameMenu(self, listbox): # Menu that lets user choose starter pokemon
        """
        :param listbox: tk.Listbox
        :return : None
        """        
        userInput = int(listbox.curselection()[0])
        print("New Game")
        playerTeam = []
        username = ""
        match userInput: # Can be made into a function/method
            case 0:
                playerTeam.append(importPokemonByName(self.file, "Bulbasaur"))
                self.player = Player(username, playerTeam, self.gui)
                self.run = True
            case 1:
                playerTeam.append(importPokemonByName(self.file, "Squirtle"))
                self.player = Player(username, playerTeam, self.gui)
                self.run = True
            case 2:
                playerTeam.append(importPokemonByName(self.file, "Charmander"))
                self.player = Player(username, playerTeam, self.gui)
                self.run = True
            case _:
                self.gui.clear_action_frame()
                self.startMenu()

        self.firstStart()

    def loadGameMenu(self): # Menu that lets user import own file with correct format
        """
        :param : None
        :return : None
        """                
        self.gui.write_line("OBS! It has to be a file with correct csv Format and in the correct directory!\n" \
                            "Input the FULL filename/path in the field")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self.importPlayerTeam(self.gui.input_field.get()))
    
    def _storeUsername(self, input): # Updates the username attribute
        """
        :param input: string
        :return : None
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
        :param userFile : string(file path)
        :return : None 
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
            self.firstStart()
        except FileNotFoundError:
            print("Import failed\nError: File not found")

    def firstStart(self):
        self.gui.write_line("Started game! Use w/a/s/d to walk around!")
        self.mapGui()

    def mapGui(self): # Creates/Formats the gui for the map and dpad
        """
        :param : None
        :return : None
        """
        if self.run == True:
            print("Run successful")
            # self.gui.disable_terminal()
            self.gui.show_map(self.map)
            self.gui.clear_action_frame()
    
            options = ["Team", "Quit"]
            self.gui.update_listbox(options)

            self.gui.action_button.config(command=lambda:self.mapUiMenu(self.gui.actions_box))

            self.gui.create_dpad()
            self.gui.up.config(command = lambda: (self.map.movePlayer(0, -1), self.gui.refresh_map(self.map), self.startEncounter()))
            self.gui.down.config(command = lambda: (self.map.movePlayer(0, 1), self.gui.refresh_map(self.map), self.startEncounter()))
            self.gui.left.config(command = lambda: (self.map.movePlayer(-1, 0), self.gui.refresh_map(self.map), self.startEncounter()))
            self.gui.right.config(command = lambda: (self.map.movePlayer(1, 0), self.gui.refresh_map(self.map), self.startEncounter()))
    
    def mapUiMenu(self, listbox):
        userInput = listbox.curselection()
        userInput = userInput[0]
        options = []
        self.gui.disable_map()
        self.gui.destroy_dpad()

        match userInput:
            case 0: # Team
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.changeTeamOrder(self.gui.actions_box, options))

            case 1: # Quit
                self.gui.input_field()
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.changeTeamOrder(self.gui.actions_box, options))

    def changeTeamOrder(self, listbox, options):
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        if options[int(userInput[0])] == "Back":
            self.mapGui()
            return
        
        userInput = userInput[0]
        print(f"User input - changeTeamOrder(): {userInput}")

        if self.player.team[userInput].fainted == True:
            self.gui.write_line("Cannot use fainted pokemon") # HERERERE
        else:        
            self.player.changeActivePokemon(userInput)
            self.gui.write_line(f"Active pokemon is now {self.player.activePokemon}")
            self.mapGui()

    def quitMenu(self, listbox, options):
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        if options[int(userInput[0])] == "Back":
            self.mapGui()
            return
        
        userInput = userInput[0]
        print(f"User input - quitMenu(): {userInput}")

    def startEncounter(self):
        num = random.randint(1,5) # 1/5 chance for an encounter
        if num == 1:
            enemy = self.generateRandomEnemy()
            self.gui.disable_map()
            self.gui.show_terminal()
            self.gui.destroy_dpad()
            self.encounterInstance = Encounter(
                                self.player, 
                                enemy, 
                                self.gui,
                                onStop=self.encounterStopped)
            self.encounterInstance.startEncounter()

    def encounterStopped(self, instance):
        print(f"Enemy defeat: {self.encounterInstance.playerWin}")
        self.gui.write_line("Encounter finished") # Remove later
        print(self.encounterInstance.playerWin)

        if self.encounterInstance.playerWin == True:
            self.gui.write_line("You won!")

            pokemon = self.player.activePokemon # Temporary local variable for activePokemon
            expGained = self.encounterInstance.opponent.leveling.droppedExp
            print(f"Exp dropped :{expGained}")
            self.gui.write_line(f"{pokemon.name} gained {expGained} exp\n"\
                                f"{pokemon.name} {pokemon.leveling}")

            nextEvolution = getEvolution(self.masterList, pokemon, self.file)
            print(f"Pokemon evolutions: {nextEvolution}")
            pokemon.gainExp(10000000)
            
            if pokemon.leveling.lvl >= pokemon.levelToEvolve and pokemon.leveling.canEvolve == True:
                self.gui.write_line(f"{pokemon.name} is evolving!")
                self.gui.clear_action_frame()
                self.gui.create_yn_buttons()
                self.gui.yes_button.config(command=lambda:self.evolveMsg(pokemon, nextEvolution))
                self.gui.no_button.config(command=lambda:(self.gui.destroy_yn_buttons(), self.mapGui()))

            else:
                self.mapGui()

        else:
            self.mapGui()

        print(pokemon.leveling)       
    
    def evolveMsg(self, pokemon, nextEvolution):
        preEvo = pokemon.name
        pokemon.evolve(nextEvolution)
        self.gui.write_line(f"{preEvo} successfully evolved to {pokemon}")
        self.gui.destroy_yn_buttons()       
        self.mapGui()

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
            
def getEvolution(pokemonList, pokemonObj, file):
    for pokemonName in pokemonList:
        if pokemonName == pokemonObj.evolution:
            newPokemonObj = importPokemonByName(file, pokemonName)
    return newPokemonObj

def main():
    game = MainGame("data.txt") # Hardcoded :thumbs_up:
    game.start()
    game.gui.root.mainloop()

main()