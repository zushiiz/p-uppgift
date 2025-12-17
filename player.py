class Player:
    def __init__(self, username = "Guest", team = ["Empty"]):
        self.name = username
        self.team = team
        self.activePokemon = team[0]

        self.potions = 10
        healingAmount = 100

        self.pokeballs = 10
        catchRate = 50
    
    def __str__(self):
        return (f"User: {self.name}")
    
    def attackOption(self):
        validInput = False
        while validInput == False:
            amountOfAttacks = []
            for i in range(len(self.activePokemon.attacks)):
                print(f"[{i}] {self.activePokemon.attacks[i]}")
                amountOfAttacks.append(i)
                i += 1
            print(f"[4] Back")
            try:
                userInput = int(input("What would you like to do?:"))
                if userInput == 4:
                    return userInput
                elif userInput in amountOfAttacks:
                    return userInput
                else:
                    print("Please enter a valid digit")
                    pass
            except ValueError:
                print("Please enter a valid digit")
                pass
    
    def swapOption(self, back = True):
        while True:
            pokemonPositions = {}
            for i in range(len(self.team)):
                if self.team[i] == self.activePokemon:
                    pass
                else:
                    print(f"[{i}] {self.team[i]}")
                    pokemonPositions[i] = self.team[i]
                    i += 1
            if back == True:
                print(f"[4] Back")
            try:
                userInput = int(input("What would you like to do?:"))
                if userInput == 4 and back == True:
                    return userInput
                elif userInput in pokemonPositions.keys():
                    if pokemonPositions[userInput].fainted == True:
                        print(f"{pokemonPositions[userInput]} has fainted and cannot be sent out")
                        pass
                    else:
                        print(f"{self.name} swapped out {self.activePokemon} for {pokemonPositions[userInput]}")
                        self.activePokemon = pokemonPositions[userInput]
                        return self.activePokemon
                else:
                    print("Please enter a valid digit")
                    pass                   
            except ValueError:
                print("Please enter a valid digit")
                pass

    def itemsOption():
        return None 

    def runOption():
        return None     