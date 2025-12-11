from player import Player
from pokemon import Pokemon

class Encounter:
    def __init__(self, player, opponent):

        self.player = player
        self.opponent = opponent
        self.turn = 1
        self.stop = False

    def startEncounter(self):
        while self.stop != False:
            print("Encounter start")
            print(f"You've encountered a wild {self.opponent}!")
            print(f"{self.player} sent out {self.player.activePokemon}")
            self.player.getActionInput()

