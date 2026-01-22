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
        
        match userInput:
            case 0: #Finished mostly
                self.gui.create_actions_box()
                options = []
                for e in self.player.activePokemon.attacks:
                    options.append(e)
                options.append("Back")
                self.gui.update_listbox(options)
                self.gui.action_button.config(command = lambda:self.playerFightMenu(self.gui.actions_box))
                
            case 1:
                pass
                # Switch
            case 2:
                # Items
                pass
            case 3:
                # Run
                pass
            case _: # Should never run, but just in case
                print(f"Invalid action index: {userInput}")

    def playerFightMenu(self, listbox): # Finish
        userInput = listbox.curselection()
        
        if len(userInput) == 0:
            raise ValueError("No actions selected")
        
        userInput = userInput[0]
        print(f"User input - fightMenu(): {userInput}")

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
        if faintedObject == self.opponent and fainted == True:
            self.stopEncounter()
            print(f"{faintedObject} fainted. Stats: {faintedObject.stats}")
            self.playerWin = True
        elif faintedObject == self.playerPokemon and fainted == True:
            if self.checkPlayerStatus():
                print("Player defeat. Stopping encounter")

                self.gui.write_line(f"All {self.player}'s pokemon have died")
                self.stopEncounter()
                
            else: # Check this logic
                self.playerPokemon = self.player.swapOption(back = False)
                self.gui.write
                print(f"{self.player} sent out {self.playerPokemon}")
        else:
            self.nextTurn()   
        
        #         case "1":
        #             playerActionIndex = self.player.swapOption()
        #             if playerActionIndex == 6:
        #                 continue
        #             else: # check logic for pokemon if it dies instantly, this loops needs to rerun
        #                 self.playerPokemon = playerActionIndex
        #                 self.enemyAttack()
                
        #         case "2":
        #             playerActionIndex = self.player.itemsOption()
        #             if playerActionIndex == 1:
        #                 if self.catchPokemon():
        #                     self.stopEncounter()
        #                     break
        #                 else:
        #                     self.enemyAttack()
        #             elif playerActionIndex == 2:
        #                 continue
        #             else:
        #                 self.enemyAttack()

        #         case "3":
        #             self.stop = True
        #             break
                
        #         case _:
        #             continue          
            
        #     self.nextTurn()

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
        print(f"{self.player} used Pokeball!")
        if random.randint(1, 4) == 1:
            print(f"{self.opponent} was caught!")
            self.player.team.append(self.opponent) # Måste lägga cap
            return True
        else:
            print(f"{self.opponent} escaped!")
            return False

    def enemyAttack(self):
        enemyAttack = random.randint(0, (len(self.opponent.attacks)-1))
        self.opponent.attack(self.playerPokemon, enemyAttack)
        print(f"{self.opponent} used {self.opponent.attacks[enemyAttack]}")
        print(self.playerPokemon.stats)
        print(self.opponent.stats)

    def stopEncounter(self):
        self.stop = True
        self.onStop(self)