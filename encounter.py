from player import Player
from pokemon import Pokemon

class Encounter:
    def __init__(self, player, opponent):

        self.player = player
        self.playerPokemon = self.player.activePokemon
        self.opponent = opponent
        self.turn = 1
        self.stop = False

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
                    print(returnedInput)
                case "1":
                    self.player.swapAction()
                case "2":
                    self.player.itemsAction()
                case "3":
                    self.stop = True
                    break
                case _:
                    pass
    
    def fight(self):
        return None

