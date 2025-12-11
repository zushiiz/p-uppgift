class Player:
    def __init__(self, username = "Guest", team = ["Empty"]):
        self.name = username
        self.team = team
        self.firstSlot = team[0]

        self.potions = 10
        healingAmount = 100

        self.pokeballs = 10
        catchRate = 50
    
    def __str__(self):
        return (f"User: {self.name}")
    
    def playerInput(self, input):
        match input:
            case "0":
                self.attackOption()
            case "1":
                self.swapOption()
            case "2":
                self.itemsOption()
            case "3":
                self.runOption()
            case _:
                pass
    
    def attackOption():
        return None
    
    def swapOption():
        return None    
    
    def itemsOption():
        return None 

    def runOption():
        return None     