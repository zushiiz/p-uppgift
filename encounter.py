import random

class Encounter:
    """
    Class desc:
    Controls a turn-based battle encounter between the player and an opponent
    Handles turn flow, player actions (fight, swap, items, run), combat resolution, fainting, catching Pokémon, and GUI interaction within an encounter
    """
    def __init__(self, player, opponent, gui, onStop): # Defines attributes for the class when initializing
        """
        :param player: Player()
        :param opponent: Pokemon()
        :param gui: Gui()
        :param onStop: stoppedEncounter()
        initializes class: MainGame.startEncounter()
        """
        self.player = player
        self.playerPokemon = self.player.activePokemon
        self.opponent = opponent
        self.gui = gui
        self.turn = 1
        self.onStop = onStop # Method
        self.stop = False
        self.playerWin = False
        self.gameOver = False
    
    def nextTurn(self): # +1 turn, sending you to the starting encounter ui
        """
        calls method: playerFightMenu(), playerSwapMenu(), playerItemsMenu(), potionsMenu()
        method calls: playerAction()
        """
        self.turn += 1

        print(f"Turn: {self.turn}")
        self.gui.write_line(
            "========================================\n"\
            f"Turn: {self.turn}\n"\
            "========================================")
                
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction())        

    def start(self): # Starts encounter logic
        """
        calls method: MainGame.startEncounter()
        method calls: playerAction()
        """
        print("Encounter start")
        self.gui.write_line(f"You've encountered a wild {self.opponent}!")
        self.gui.write_line(f"{self.player} sent out {self.playerPokemon}")
        self.gui.write_line(
            "========================================\n"\
            f"Turn: {self.turn}\n"\
            "========================================")

        # Items refresh
        self.player.potions = 1
        self.player.pokeballs = 10

        # options listbox
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction())

    def backToEncounterMenu(self): # Takes you back to the first encounter ui
        """
        calls method: playerFightMenu(), playerSwapMenu(), playerItemsMenu(), potionsMenu()
        method calls: playerAction()
        """
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction())

    def playerAction(self): # Interface logic that calls the one of the four actions players can (fight, swap, items, run) do
        """
        calls method: nextTurn(), start(), backToEncounter()
        method calls: playerFightMenu(), playerSwapMenu(), playerItemsMenu(), stopEncounter()
        """
        actionIndex = self.gui.checkOptionIndex()
        print(f"Option index - playerAction(): {actionIndex}")
        options = []        
        match actionIndex:
            case 0: # Fight
                for e in self.player.activePokemon.movelist:
                    options.append(e)
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerFightMenu(options))
                
            case 1: # Team
                for e in self.player.team:
                    if e == self.playerPokemon:
                        continue
                    else:
                        options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerSwapMenu(options))

            case 2: # Items
                options = [f"Healing potion - {self.player.potions}/10", f"Pokeballs - {self.player.pokeballs}/10", "Back"]
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerItemsMenu(options))

            case 3: # Run
                self.gui.write_line("You've fled from the encounter")
                self.stopEncounter()

            case _: # Should never run, but just in case
                raise IndexError(f"Invalid action index: {actionIndex}")

    def playerFightMenu(self, options): # Fight logic 
        """
        :param options: [string, ...]
        calls method: playerAction()
        method calls:  stopEncounter(), nextTurn()
        """
        atkIndex = self.gui.checkOptionIndex(options)
        print(f"optionIndex - playerFightMenu() - {atkIndex}")
        if atkIndex == "Back":
            self.backToEncounterMenu()
            return

        enemyAtkIndex = random.randint(0, (len(self.opponent.movelist)-1))
        faintedObject = None # Redundant
        fainted = None

        # Turn order
        if self.playerPokemon.stats.spd >= self.opponent.stats.spd:
            print("Player speed > enemy")
            faintedObject, fainted = self.fight(atkIndex, enemyAtkIndex, self.playerPokemon, self.opponent)
        else:
            print("Enemy speed > Player")
            faintedObject, fainted = self.fight(enemyAtkIndex, atkIndex, self.opponent, self.playerPokemon)                     

        # Post damage logic
        if faintedObject == self.opponent and fainted == True: # Opponent loss
            print(f"{faintedObject} fainted. Stats: {faintedObject.stats}")
            self.playerWin = True
            self.stopEncounter()

        elif faintedObject == self.playerPokemon and fainted == True: # Player loss
            if self.checkPlayerStatus():
                print("Player defeat. Stopping encounter")

                self.gui.write_line(f"All {self.player}'s pokemon have died")
                self.gameOver = True
                self.stopEncounter()
                
            else: # I think this has some logic errors?
                # If player has more pokemons
                self.gui.write_line(f"{self.playerPokemon} has fainted!\n"\
                                    "Who would you like to send out?")
                options = []
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerSwapMenu(options, faint = True))
                
                print(f"{self.player} sent out {self.playerPokemon}")
        else:
            self.nextTurn()
        
    def playerSwapMenu(self, options, faint = False): # Swapping out active pokemon 
        # There is one instance where fainted pokemon can be sent out...
        """
        :param options: [string, ...]
        :param faint: boolean
        calls method: playerAction(), playerFightMenu()
        method calls: backToEncounter(), enemyAttack(), nextTurn()
        """
        actionIndex = self.gui.checkOptionIndex(options)
        print(f"Option index - playerSwapMenu() - {actionIndex}")
        if actionIndex == "Back":
            self.backToEncounterMenu()
            return
        
        if self.player.team[actionIndex].fainted == True:
            self.gui.write_line("Cannot send out fainted pokemon")
        
        else:
            self.player.swapOption(actionIndex)
            self.playerPokemon = self.player.activePokemon
            self.gui.write_line(f"{self.player.name} sent out {self.playerPokemon}")
            if not faint:
                self.enemyAttack()
            self.nextTurn()
    
    def playerItemsMenu(self, options): # Interface logic to either choose potion or pokeball
        """
        :param options: [string, ...]
        calls method: playerAction()
        method calls: potionsMenu(), nextTurn()
        """
        actionIndex = self.gui.checkOptionIndex(options)
        print(f"Option index - playerItemsMenu() - {actionIndex}")
        if actionIndex == "Back":
            self.backToEncounterMenu()
            return
        
        options = []
        match actionIndex:
            case 0:
                if self.player.potions <= 0:
                    self.gui.write_line("You don't have any potions left")
                    return
                self.gui.write_line("Choose a pokemon to heal")
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.potionMenu(options))
            
            case 1:
                if self.player.pokeballs <= 0:
                    self.gui.write_line("You don't have any pokeballs left")
                    return                
                self.catchPokemon()
                if self.stop == False:
                    self.nextTurn()

    def potionMenu(self, options): # Calls methods to heal the chosen pokemon
        """
        :param options: [string, ...]
        calls method: playerItemsMenu() 
        method calls: backToEncounter(), enemyAttack(), nextTurn()
        """        
        actionIndex = self.gui.checkOptionIndex(options)
        print(f"Option index - potionMenu() - {actionIndex}")        
        if actionIndex == "Back":
            self.backToEncounterMenu()
            return

        if self.player.team[actionIndex].fainted == True: #Silvertape fix
            self.gui.write_line("Pokemon has already fainted, cannot heal")
            return
        else:
            pokemon = self.player.team[actionIndex]
            self.player.healPokemon(pokemon)
            self.gui.write_line(f"Healed {pokemon.name}! Hp: {pokemon.stats.hp}/{pokemon.stats.maxHp}")
            self.enemyAttack()
            if self.stop == False:
                self.nextTurn()

    def checkPlayerStatus(self): # Checks status on all pokemon in players team
        """
        :return : boolean (True if all pokemons have fainted)
        """
        amount = 0
        for e in self.player.team:
            print(f"{e}, {e.fainted}")
            if e.fainted == True:
                amount += 1
            else:
                return False
        if amount == len(self.player.team):
            return True

    def fight(self, atkIndex1, atkIndex2, object1, object2): # Takes to Pokemon-objects and inflicts damage on eachother
        """
        :param atkIndex1: integer
        :param atkIndex2: integer
        :param object1: Pokemon()
        :param object2: Pokemon()
        
        :return : Pokemon() or None
        :return : boolean
        """
        print("Pre damage report:\n"\
            f"{object1}. {object1.stats}. {object1.movelist[atkIndex1]}\n"\
            f"{object2}. {object2.stats}. {object2.movelist[atkIndex2]}")

        self.gui.write_line(f"{object1.name} used {object1.movelist[atkIndex1]}")
        object1.attack(object2, atkIndex1)
        self.gui.write_line(f"{object2.name} - Hp: {object2.stats.hp}/{object2.stats.maxHp}")

        if object2.fainted == True:
            print(f"{object2} fainted")
            return object2, True
        else:
            self.gui.write_line(f"{object2.name} used {object2.movelist[atkIndex2]}")
            object2.attack(object1, atkIndex2)
            self.gui.write_line(f"{object1.name} - Hp: {object1.stats.hp}/{object1.stats.maxHp}")

            print("Post damage report:\n"\
                f"{object1}. {object1.stats}. {object1.movelist[atkIndex1]}\n"\
                f"{object2}. {object2.stats}. {object2.movelist[atkIndex2]}")
            
            if object1.fainted == True:
                print(f"{object1} fainted")
                return object1, True
            else:
                print("No faint")
                return None, False
            
    def catchPokemon(self): # Chance to add enemy pokemon to team and end encounter
        if len(self.player.team) >= 6:
            self.gui.write_line("You cannot have more than 6 pokemon!")
            return

        self.gui.write_line(f"{self.player} used Pokeball!")
        if random.randint(1, 4) == 1:
            self.gui.write_line(f"{self.opponent} was caught!")
            self.player.team.append(self.opponent) # No limit
            self.stopEncounter()
            return
        else:
            self.gui.write_line(f"{self.opponent} escaped!")
            self.enemyAttack()
        self.player.pokeballs -= 1

    def enemyAttack(self): # Enemy attacks player pokemon, also handles a bit of logic if player pokemon faints, should probably move it somewhere
        
        enemyAttack = random.randint(0, (len(self.opponent.movelist)-1))
        self.gui.write_line(f"{self.opponent.name} used {self.opponent.movelist[enemyAttack]}")
        self.opponent.attack(self.playerPokemon, enemyAttack)
        self.gui.write_line(f"{self.playerPokemon.name} - Hp: {self.playerPokemon.stats.hp}/{self.playerPokemon.stats.maxHp}")
        print(f"{self.opponent} used {self.opponent.movelist[enemyAttack]}")
        print(self.playerPokemon.stats)
        print(self.opponent.stats)

        if self.playerPokemon.stats.hp <= 0: #THIS LOGIC CURRENTLY DOES NOT WORK 
            if self.checkPlayerStatus():
                print("Player defeat. Stopping encounter")

                self.gui.write_line(f"All {self.player}'s pokemon have died")
                self.gameOver = True
                self.stopEncounter()
                return
            else:

                self.gui.write_line(f"{self.playerPokemon} has fainted!\n"\
                                    "Who would you like to send out?")
                options = []
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerSwapMenu(options, faint = True))
                
                print(f"{self.player} sent out {self.playerPokemon}")                                

    def stopEncounter(self): # Stops encounter and runs onStop function in game.py
        """
        calls method: playerAction(), playerFightMenu(), enemyAttack()
        method calls: MainGame.stoppedEcnounter()
        """
        self.stop = True
        self.onStop(self)