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

            userInput = input("What would you like to do?:")
            if userInput == "4":
                return int(userInput)
            try:
                if int(userInput) in amountOfAttacks:
                    return int(userInput)
                else:
                    print("Please enter a valid digit")
                    pass
            except:
                print("Please enter a valid digit")
                pass
    
    def swapOption():
        return None    
    
    def itemsOption():
        return None 

    def runOption():
        return None     