from player import Player
from pokemon import Pokemon
import random

class Encounter:
    def __init__(self, player, opponent):

        self.player = player
        self.playerPokemon = self.player.activePokemon
        self.opponent = opponent
        self.turn = 1
        self.stop = False
        self.playerWin = False

    def startEncounter(self):
        print("Encounter start")
        print(f"You've encountered a wild {self.opponent}!")
        print(f"{self.player} sent out {self.playerPokemon}")        
        while self.stop == False:
            self.playerAction()
    
    def stopEncounter(self):
        self.stop = True
    
    def nextTurn(self):
        self.turn += 1

    def playerAction(self):
        validInput = False
        while validInput == False:
            print(f"========================================================================\nTurn: {self.turn}")
            print("[0] Fight \n" \
                  "[1] Pokemon \n" \
                  "[2] Items \n" \
                  "[3] Run")
            
            userInput = input("What would you like to do?:")
            match userInput:
                case "0":
                    returnedInput = self.player.attackOption()
                    if returnedInput == 4:
                        continue
                    else:
                        enemyAttack = random.randint(0, (len(self.opponent.attacks)-1))
                        faintedObject = None
                        fainted = None
                        if self.playerPokemon.stats.spd >= self.opponent.stats.spd:
                            faintedObject, fainted = self.fight(returnedInput, enemyAttack, self.playerPokemon, self.opponent)
                        else:
                            faintedObject, fainted = self.fight(enemyAttack, returnedInput, self.opponent, self.playerPokemon)                     

                        if faintedObject == self.opponent and fainted == True:
                            self.stopEncounter()
                            print(f"{faintedObject} fainted!")
                            print(faintedObject.stats)
                            self.playerWin = True
                            break
                        elif faintedObject == self.playerPokemon and fainted == True:
                            if self.checkPlayerStatus():
                                self.stopEncounter()
                                break
                            else: # Check this logic
                                self.playerPokemon = self.player.swapOption(back = False)
                                print(f"{self.player} sent out {self.playerPokemon}")
                        else:
                            self.nextTurn()
                            continue

                case "1":
                    returnedInput = self.player.swapOption()
                    if returnedInput == 6:
                        continue
                    else: # check logic for pokemon if it dies instantly, this loops needs to rerun
                        self.playerPokemon = returnedInput
                        self.enemyAttack()
                
                case "2":
                    returnedInput = self.player.itemsOption()
                    if returnedInput == 1:
                        if self.catchPokemon():
                            self.stopEncounter()
                            break
                        else:
                            self.enemyAttack()
                    elif returnedInput == 2:
                        continue
                    else:
                        self.enemyAttack()

                case "3":
                    self.stop = True
                    break
                
                case _:
                    continue          
            
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
        print(object1.stats)
        print(object2.stats)        
        print(f"{object1} used {object1.attacks[attack1]}")
        object1.attack(object2, attack1)
        if object2.fainted == True:
            return object2, True
        else:
            print(f"{object2} used {object2.attacks[attack2]}")
            object2.attack(object1, attack2)
            print(object1.stats)
            print(object2.stats)
            if object1.fainted == True:
                return object1, True
            else:
                return None, False
            
    def catchPokemon(self):
        print(f"{self.player} used Pokeball!")
        if random.randint(1, 10) == 1: # After caught it doesnt go anywhere for now
            print(f"{self.opponent} was caught!")
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