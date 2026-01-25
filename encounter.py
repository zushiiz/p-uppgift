import random

class Encounter:
    def __init__(self, player, opponent, gui, onStop):

        self.player = player
        self.playerPokemon = self.player.activePokemon
        self.opponent = opponent
        self.gui = gui
        self.turn = 1
        self.onStop = onStop
        self.stop = False
        self.playerWin = False
        self.gameOver = False
    
    def nextTurn(self):
        self.turn += 1

        print(f"Turn: {self.turn}")
        self.gui.write_line(
            "========================================\n"\
            f"Turn: {self.turn}\n"\
            "========================================")
                
        self.gui.create_actions_box()
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction(self.gui.actions_box))        

    def startEncounter(self):
        """
        :param : None
        :return : None
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

        self.gui.create_actions_box()
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction(self.gui.actions_box))

    def backToEncounterMenu(self):
        self.gui.create_actions_box()
        options = ["Fight", "Pokemon", "Items", "Run"]
        self.gui.update_listbox(options)
        self.gui.action_button.config(command = lambda:self.playerAction(self.gui.actions_box))

    def playerAction(self, listbox): 
        userInput = listbox.curselection()

        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        userInput = userInput[0]
        print(f"playerAction(): {userInput}")

        print(f"User input - playerAction(): {userInput}")
        self.gui.create_actions_box()
        options = []        
        match userInput:
            case 0: # Fight
                for e in self.player.activePokemon.attacks:
                    options.append(e)
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerFightMenu(self.gui.actions_box, options))
                
            case 1: # Team
                for e in self.player.team:
                    if e == self.playerPokemon:
                        continue
                    else:
                        options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerSwapMenu(self.gui.actions_box, options))

            case 2: # Items
                options = [f"Healing potion - {self.player.potions}/10", f"Pokeballs - {self.player.pokeballs}/10", "Back"]
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerItemsMenu(self.gui.actions_box, options))

            case 3: # Run
                self.gui.write_line("You've fled from the encounter")
                self.stopEncounter()
            case _: # Should never run, but just in case
                print(f"Invalid action index: {userInput}")

    def playerFightMenu(self, listbox, options): # Finish
        userInput = listbox.curselection()

        if len(userInput) == 0:
            raise ValueError("No actions selected")

        if options[int(userInput[0])] == "Back":
            self.backToEncounterMenu()
            return
        
        userInput = userInput[0]
        print(f"User input - playerFightMenu(): {userInput}")

        enemyAttack = random.randint(0, (len(self.opponent.attacks)-1))
        faintedObject = None # Redundant
        fainted = None

        # Turn order
        if self.playerPokemon.stats.spd >= self.opponent.stats.spd:
            print("Player speed > enemy")
            faintedObject, fainted = self.fight(userInput, enemyAttack, self.playerPokemon, self.opponent)
        else:
            print("Enemy speed > Player")
            faintedObject, fainted = self.fight(enemyAttack, userInput, self.opponent, self.playerPokemon)                     

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
                self.gui.create_actions_box()
                options = []
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerSwapMenu(self.gui.actions_box, options, faint = True))
                
                print(f"{self.player} sent out {self.playerPokemon}")
        else:
            self.nextTurn()
        
    def playerSwapMenu(self, listbox, options, faint = False): # There is one instance where fainted pokemon can be sent out...
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        if options[int(userInput[0])] == "Back":
            self.backToEncounterMenu()
            return
        
        userInput = userInput[0]
        print(f"User input - playerSwapMenu(): {userInput}")
        
        if self.player.team[userInput].fainted == True:
            self.gui.write_line("Cannot send out fainted pokemon")
        
        else:
            self.player.swapOption(userInput)
            self.playerPokemon = self.player.activePokemon
            self.gui.write_line(f"{self.player.name} sent out {self.playerPokemon}")
            if not faint:
                self.enemyAttack()
            self.nextTurn()
    
    def playerItemsMenu(self, listbox, options):
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        if options[int(userInput[0])] == "Back":
            self.backToEncounterMenu()
            return                
        
        userInput = userInput[0]
        options = []
        match userInput:
            case 0:
                if self.player.potions <= 0:
                    self.gui.write_line("You don't have any potions left")
                    return
                self.gui.write_line("Choose a pokemon to heal")
                for e in self.player.team:
                    options.append(f"{e.name} - {e.stats.hp}/{e.stats.maxHp}")
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.potionMenu(self.gui.actions_box, options))
            
            case 1:
                if self.player.pokeballs <= 0:
                    self.gui.write_line("You don't have any pokeballs left")
                    return                
                self.catchPokemon()
                self.nextTurn()

    def potionMenu(self, listbox, options):
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        if options[int(userInput[0])] == "Back":
            self.backToEncounterMenu()
            return
        userInput = userInput[0]
        if self.player.team[userInput].fainted == True: #Silvertape fix
            self.gui.write_line("Pokemon has already fainted, cannot heal")
            return
        else:
            pokemon = self.player.team[userInput]
            self.player.healPokemon(pokemon)
            self.gui.write_line(f"Healed {pokemon.name}! Hp: {pokemon.stats.hp}/{pokemon.stats.maxHp}")
            self.enemyAttack()
            self.nextTurn()

    def checkPlayerStatus(self): # True if all fainted 
        amount = 0
        for e in self.player.team:
            print(f"{e}, {e.fainted}")
            if e.fainted == True:
                amount += 1
            else:
                return False
        if amount == len(self.player.team):
            return True

    def fight(self, attack1, attack2, object1, object2):
        print("Pre damage report:\n"\
            f"{object1}. {object1.stats}. {object1.attacks[attack1]}\n"\
            f"{object2}. {object2.stats}. {object2.attacks[attack2]}")

        self.gui.write_line(f"{object1.name} used {object1.attacks[attack1]}")
        object1.attack(object2, attack1)
        self.gui.write_line(f"{object2.name} - Hp: {object2.stats.hp}/{object2.stats.maxHp}")

        if object2.fainted == True:
            print(f"{object2} fainted")
            return object2, True
        else:
            self.gui.write_line(f"{object2.name} used {object2.attacks[attack2]}")
            object2.attack(object1, attack2)
            self.gui.write_line(f"{object1.name} - Hp: {object1.stats.hp}/{object1.stats.maxHp}")

            print("Post damage report:\n"\
                f"{object1}. {object1.stats}. {object1.attacks[attack1]}\n"\
                f"{object2}. {object2.stats}. {object2.attacks[attack2]}")
            
            if object1.fainted == True:
                print(f"{object1} fainted")
                return object1, True
            else:
                print("No faint")
                return None, False
            
    def catchPokemon(self):
        self.gui.write_line(f"{self.player} used Pokeball!")
        if random.randint(1, 4) == 1:
            self.gui.write_line(f"{self.opponent} was caught!")
            self.player.team.append(self.opponent) # No limit
            self.stopEncounter()
        else:
            self.gui.write_line(f"{self.opponent} escaped!")
            self.enemyAttack()
        self.player.pokeballs -= 1

    def enemyAttack(self): # When only enemy attacks
        enemyAttack = random.randint(0, (len(self.opponent.attacks)-1))
        self.gui.write_line(f"{self.opponent.name} used {self.opponent.attacks[enemyAttack]}")
        self.opponent.attack(self.playerPokemon, enemyAttack)
        self.gui.write_line(f"{self.playerPokemon.name} - Hp: {self.playerPokemon.stats.hp}/{self.playerPokemon.stats.maxHp}")
        print(f"{self.opponent} used {self.opponent.attacks[enemyAttack]}")
        print(self.playerPokemon.stats)
        print(self.opponent.stats)

    def stopEncounter(self):
        self.stop = True
        self.onStop(self)