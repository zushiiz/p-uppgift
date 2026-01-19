class Leveling():
    def __init__(self, level = 1, evolve = True, evolutionStage = 0):
        self.lvl = int(level)
        self.exp = 0 # Current amount of exp
        self.droppedExp = (self.lvl * 10000) // 6 # Amount of exp dropped when defeated
        self._nextLvl = (self.lvl * 10000) // 5 # Amount of exp needed for the next level

        # Handles the self.canEvolve attribute to correct datatype since the parameter evolve is read as a string from the file
        match evolve: 
            case "False":
                self.canEvolve = False
            case "True":
                self.canEvolve = True
            case _:
                self.canEvolve = evolve
        self.stage = int(evolutionStage)
    
    def __str__(self):
        return f"Lvl. {self.lvl}: {self.exp}/{self._nextLvl}"

    # This method handles the amount of the incoming exp a pokemon will gain and how that affects the level
    # methods called: self.levelUp()
    def increaseExperience(self, ammount):
        self.exp += ammount
        while self.exp >= self._nextLvl:
            self.exp -= self._nextLvl
            self.levelUp()

    # This method will be looped to handle the level stat and all the requirements for the next level
    def levelUp(self):
        self.lvl += 1
        self._nextLvl = (self.lvl * 10000) // 5
        self.droppedExp = (self.lvl * 10000) // 6
