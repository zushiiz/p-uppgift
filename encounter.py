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
        self.opponentStatus = self.opponent.fainted

    def startEncounter(self):
        print("Encounter start")
        print(f"You've encountered a wild {self.opponent}!")
        print(f"{self.player} sent out {self.playerPokemon}")        
        while self.stop == False:
            self.playerAction()

    def playerAction(self):
        validInput = False
        while validInput == False:
            print("[0] Fight \n" \
                  "[1] Pokemon \n" \
                  "[2] Items \n" \
                  "[3] Run")
            
            userInput = input("What would you like to do?:")
            match userInput:
                case "0":
                    returnedInput = self.player.attackOption()
                    if returnedInput == 4:
                        pass
                    else:
                        enemyAttack = self.opponent.attacks[random.randint(0, (len(self.opponent.attacks)-1))]
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
                            break
                        elif faintedObject == self.playerPokemon and fainted == True:
                            if self.checkPlayerStatus():
                                self.stopEncounter()
                                break
                            else:
                                self.player.swapAction()
                        else:
                            pass

                case "1":
                    self.player.swapAction()
                case "2":
                    self.player.itemsAction()
                case "3":
                    self.stop = True
                    break
                case _:
                    pass             
    
    def stopEncounter(self):
        self.stop = True

    def checkPlayerStatus(self):
        for pokemon in self.player.team:
            amountFaintedPokemon = 0
            while amountFaintedPokemon != len(self.player.team):
                if pokemon.status == True:
                    amountFaintedPokemon += 1
                else:
                    return False
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
            


