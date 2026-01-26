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
P-Uppgift 200 Pokemon

This project is a simple recreation of game features of a turn-based combat game, Pokemon
Program is written in a object-oriented format, similar to C#
camelCase is used as standard for variables, functions, methods
pascalCase is used for classes
snake_case is used for all gui related variables, functions, methods

Changes to game-features:
No handling types - would require a matrix that holds all the typing data
Max 6 per team cap - needs a storing system for game better flow which is currently not included
Max 4 moves cap - this would be needed if the pokemons actually had movesets, but currently everything just uses scratch
Main game logic - runs through class methods instead of file functions

Game related notes:
Jolteon and Flareon doesnt exist
Bit unbalanced in base stats
No IV farming
No team amount cap
No revives
Sloppy silver tape gui
Moves are hardcoded to only scratch - but made to be changed easily in the future
Math has not been fine tuned
Could have more thorough error handling

"""
class MainGame:
    """
    Class desc:
    Main game controller that manages game flow, menus, player creation,
    map exploration, encounters, saving/loading, and GUI coordination
    Acts as central systems hub
    """
    def __init__(self, filename): # Defines attributes for the class when initializing
        """
        :param filename: string (file formatted)
        initializes class: main()
        """
        self.file = filename
        self.masterList = importPokemonNames(self.file) # All pokemon names

        self.player = None
        self.username = None
        self.map = Map()
        self.run = False
        self.gui = GUI()

    def generateRandomEnemy(self): # Generates one random pokemon object for an encounter
        """
        :return enemy: Pokemon()
        calls method: startEncounter()
        """
        playerLevels = []
        for pokemonObj in self.player.team:
            playerLevels.append(pokemonObj.leveling.lvl)
        playerLevels.sort() # Level balancing
        level = random.randint(playerLevels[0], playerLevels[len(playerLevels)-1])
        nameIndex = random.randint(0, len(self.masterList)-1)
        enemy = importPokemonByName(self.file, self.masterList[nameIndex], level)
        return enemy

    def start(self): # Program starting point menu formatting
        """
        calls method: main()
        method calls: _storeUsername()
        """
        self.gui.write_line("Enter a username")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self._storeUsername(self.gui.input_field.get()))

    def startMenu(self): # Formats starting menu
        """
        calls method: _storeUsername(), newGameMenu() 
        method calls: startMenuActions()
        """
        print("Starting Menu...")
        self.gui.write_line(f"Welcome {self.username}!")
        options = ["New Game", "Load Game", "Quit Game"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.startMenuActions(self.gui.actions_box))        

    def startMenuActions(self, listbox): # Handles the logic for if user wants to load or create new game
        """
        :param listbox : tk.Listbox
        calls method: StartMenu()
        method calls: newGameMenu(), loadGameMenu(), quit()
        """
        optionIndex = checkOptionIndex(listbox)
        print(f"User input: {optionIndex}")

        match optionIndex: # Prepares menu and parameters for newGameMenu() method
            case 0: 
                self.gui.write_line("Pick your starter Pokemon!")
                options = ["Bulbasaur", "Squirtle", "Charmander", "Back"]
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.newGameMenu(self.gui.actions_box))

            case 1:
                self.loadGameMenu()
            case 2:
                quit()

    def newGameMenu(self, listbox): # Menu that lets user choose starter pokemon
        """
        :param listbox: tk.Listbox
        calls method: startMenuActions()
        method calls: firstStart()
        """        
        userInput = checkOptionIndex(listbox)
        print("New Game")
        playerTeam = []
        match userInput: # Can be made into a function/method
            case 0:
                playerTeam.append(importPokemonByName(self.file, "Bulbasaur"))
                self.player = Player(self.username, playerTeam)
                self.run = True
            case 1:
                playerTeam.append(importPokemonByName(self.file, "Squirtle"))
                self.player = Player(self.username, playerTeam)
                self.run = True
            case 2:
                playerTeam.append(importPokemonByName(self.file, "Charmander"))
                self.player = Player(self.username, playerTeam)
                self.run = True
            case _:
                self.gui.clear_action_frame()
                self.startMenu()

        self.firstStart()

    def loadGameMenu(self): # Menu that lets user import own file with correct format   
        """
        calls method: startMenuActions()
        method calls: importPlayerTeam()
        """   
        self.gui.write_line("OBS! It has to be a file with correct csv Format and in the correct directory!\n" \
                            "Input the FULL filename/path in the field")
        self.gui.create_input_field()
        self.gui.action_button.config(command = lambda: self.importPlayerTeam(self.gui.input_field.get()))
    
    def _storeUsername(self, input): # Updates the username attribute
        """
        :param input: string
        calls method: start()
        method calls: startMenu()
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
        calls method: loadGameMenu()
        method calls: firstStart()
        """        
        playerTeam = []
        print(f"Importing file:{userFile}")
        try:
            with open(userFile, "r", encoding="utf-8") as csvFile:
                reader = csv.DictReader(csvFile)
                for pokemonData in reader:
                    stats = Stats(pokemonData["Health"], pokemonData["Attack"], pokemonData["Defense"], pokemonData["Speed"])
                    level = Leveling(pokemonData["Level"], pokemonData["Can_evolve"], pokemonData["Stage"])
                    playerTeam.append(Pokemon(pokemonData["Pokemon_name"], stats, Movelist(Attack("Scratch")), level, pokemonData["Next_evolution"]))
            self.player = Player(self.username, playerTeam)
            print("Import successful, running game")
            self.run = True
            self.firstStart()
        except FileNotFoundError:
            raise FileNotFoundError(f"Pokemon data file not found: {userFile}")
        except KeyError as e:
            raise ValueError(f"Missing value: {e}")

    def firstStart(self): # Runs once on start
        """
        calls method: importPlayerTeam
        method calls: mapGui()
        """
        self.gui.write_line("Started game! Use w/a/s/d to walk around!")
        self.mapGui()

    def mapGui(self): # Creates/Formats the ui for the map and dpad
        """
        calls method: firstStart(), mapUiMenu(), changeTeamOrder(), startEncounter(), evolveMsg()
        method calls: startEncounter(), mapUiMenu()
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
    
    def mapUiMenu(self, listbox): # Formats ui when player wants to quit or change team during the map interface
        """
        :param listbox: tk.Listbox()
        calls method: mapGui()
        method calls: changeTeamOrder(), quitMenu(), mapGui()
        """
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
                self.gui.create_input_field()
                self.gui.create_back_button()
                self.gui.write_line("Avoid special characters such as '. , ? !' or numbers '1 2 3 4'\n"\
                                    "Entering previous file name will override old saves\n"\
                                    "File type is not needed (ex: .txt, .csv etc)")

                self.gui.action_button.config(command = lambda:self.quitMenu(self.gui.input_field.get()))
                self.gui.back_button.config(command=lambda:(self.mapGui(), self.gui.back_button.destroy())) # Probably bad logic

    def changeTeamOrder(self, listbox, options): # Logic that changes the team order
        """
        :param listbox: tk.Listbox()
        :param options: [string, ...]
        calls method: mainUiMenu()
        method calls: mapGui()
        """
        userInput = checkOptionIndex(listbox, options)
        if not userInput:
            self.mapGui()
        print(f"User input - changeTeamOrder(): {userInput}")

        if self.player.team[userInput].fainted == True:
            self.gui.write_line("Cannot use fainted pokemon")
        else:        
            self.player.changeActivePokemon(userInput)
            self.gui.write_line(f"Active pokemon is now {self.player.activePokemon}")
            self.mapGui()

    def quitMenu(self, filename): # Calls exportPlayerTeam() function to save then quits
        """
        :param filename: string (file formatted)
        calls method: mapUiMenu(), encounterStopped()
        """
        exportPlayerTeam(self.player.team, filename)    
        self.gui.write_line("Press enter again to close program")    
        self.gui.action_button.config(command=lambda:quit())

    def startEncounter(self): # Chance to instantiate and start an encounter
        """ Should 
        calls method: mapGui()
        method calls: Encounter.start()
        """
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
            self.encounterInstance.start()

    def encounterStopped(self, instance): # Logic for after an encounter ends (ex. gaining exp, game over, etc)
        """
        :param instance: Encounter()
        calls method: Encounter.stopEncounter()
        method calls: mapGui(), evolveMsg()
        """
        print(f"Enemy defeat: {self.encounterInstance.playerWin}")
        self.gui.write_line("Encounter finished") # Remove later
        print(f"Player win: {self.encounterInstance.playerWin}")
        print(f"Game over: {self.encounterInstance.gameOver}")

        if self.encounterInstance.playerWin == True:
            self.gui.write_line("You won!")

            pokemon = self.player.activePokemon # Temporary local variable for activePokemon
            expGained = self.encounterInstance.opponent.leveling.droppedExp
            print(f"Exp dropped :{expGained}")
            self.gui.write_line(f"{pokemon.name} gained {expGained} exp\n"\
                                f"{pokemon.name} {pokemon.leveling}")

            nextEvolution = getEvolution(self.masterList, pokemon, self.file)
            print(f"Pokemon evolutions: {nextEvolution}")
            pokemon.gainExp(expGained)
            
            if pokemon.leveling.lvl >= pokemon.levelToEvolve and pokemon.leveling.canEvolve == True: # Evolving logic
                self.gui.write_line(f"{pokemon.name} is evolving!")
                self.gui.clear_action_frame()
                self.gui.create_yn_buttons()
                self.gui.yes_button.config(command=lambda:self.evolveMsg(pokemon, nextEvolution))
                self.gui.no_button.config(command=lambda:(self.gui.destroy_yn_buttons(), self.mapGui()))

            else:
                self.mapGui()
        # Game over logic
        elif self.encounterInstance.gameOver == True:
            self.gui.write_line("Game Over, enter teamname to save your team")
            self.gui.write_line("Avoid special characters such as '. , ? !' or numbers '1 2 3 4'\n"\
                                "Entering previous file name will override old saves\n"\
                                "File type is not needed (ex: .txt, .csv etc)")
            self.gui.create_input_field()
            self.gui.action_button.config(command = lambda:self.quitMenu(self.gui.input_field.get()))

        else: # Player run
            self.mapGui()    
    
    def evolveMsg(self, pokemon, nextEvolution): # Updates Pokemon-object to its data for evolution
        """
        :param pokemon: Pokemon()
        :param nextEvolution: pokemon()
        calls method: encounterStopped()
        method calls: mapGui()
        """
        preEvo = pokemon.name
        pokemon.evolve(nextEvolution)
        self.gui.write_line(f"{preEvo} successfully evolved to {pokemon}")
        self.gui.destroy_yn_buttons()       
        self.mapGui()

def exportPlayerTeam(playerTeam, userFile): # Creates new file, formats and saves the players team
    """
    :params playerTeam: [Pokemon(), ...]
    :params userFile: string
    :Return : Boolean
    calls method: quitMenu()
    """
    try:
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
    except OSError as e:
        raise OSError(f"Invalid filename: {e}")
    
def importPokemonNames(filename): # Imports all pokemon names from a file and returns a list of all of them
    """
    :param filename: string (file formatted)
    :return pokemonList: [Pokemon().name, ...] (strings)
    """
    pokemonList = []
    try:
        with open(filename, "r", encoding="utf-8") as csvFile:
            reader = csv.DictReader(csvFile)
            for pokemonData in reader:
                pokemonList.append(pokemonData["Pokemon_name"])
        return pokemonList
    except FileNotFoundError:
        raise FileNotFoundError(f"Pokemon data file not found: {filename}")  
    except KeyError as e:
        raise ValueError(f"Missing value: {e}")

def importPokemonByName(filename, pokemonName, level = None): # Imports and instantiates a Pokemon-object based on a name
    """
    :param filename: string (file formatted)
    :param pokemonName: string
    :param level: integer
    :return : Pokemon()
    """
    try:
        with open(filename, "r", encoding="utf-8") as csvFile:
            reader = csv.DictReader(csvFile)
            for pokemonData in reader:
                if pokemonData["Pokemon_name"].lower() == pokemonName.lower():
                    if level == None:
                        level = pokemonData["Level"]
                    stats = Stats(pokemonData["Health"], pokemonData["Attack"], pokemonData["Defense"], pokemonData["Speed"])
                    level = Leveling(level, pokemonData["Can_evolve"], pokemonData["Stage"])
                    return Pokemon(pokemonData["Pokemon_name"], stats, Movelist(Attack("Scratch")), level, pokemonData["Next_evolution"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Pokemon data file not found: {filename}")

def getEvolution(pokemonList, pokemonObj, file): # Checks a pokemons next evolution and imports that pokemon
    """
    :param pokemonList: [string, ...]
    :param pokemonObj: Pokemon()
    :param file: string (file formatted)
    """
    for pokemonName in pokemonList:
        if pokemonName == pokemonObj.evolution:
            newPokemonObj = importPokemonByName(file, pokemonName)
    return newPokemonObj

def checkOptionIndex(listbox, options = []): # Checks if user selected an action MOVE TO GUI?
    optionIndex = listbox.curselection() # Gives tuple of indices
    if len(optionIndex) == 0:
        raise ValueError("No actions selected")
    elif options[int(optionIndex[0])] == "Back":
        print("Back")
        return False
    return optionIndex[0]

def main(): # Instantiates a game and starts
    game = MainGame("data.txt") # Hardcoded file :thumbs_up:
    game.start()
    game.gui.root.mainloop()

main()