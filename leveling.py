class Leveling():
    """
    Class desc:
    Stores and handles most level related data
    """
    def __init__(self, level = 1, evolve = True, evolutionStage = 0): # Defines attributes for the class when initializing
        """
        :param level: integer
        :param evolve: boolean
        :param evolutionStage: integer
        """
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
    
    def __str__(self): # Returns level, exp and amount of exp for next level as string
        return f"Lvl. {self.lvl}: {self.exp}/{self._nextLvl}"

    def increaseExperience(self, ammount): # Increases exp and calls levelUp()-method when threshold reached
        self.exp += ammount
        while self.exp >= self._nextLvl:
            self.exp -= self._nextLvl
            self.levelUp()

    def levelUp(self): # Increases level and recalculates exp needed for next level
        self.lvl += 1
        self._nextLvl = (self.lvl * 10000) // 5
        self.droppedExp = (self.lvl * 10000) // 6