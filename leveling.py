class Leveling():
    def __init__(self, level = 1, evolve = True, evolutionStage = 0):
        self.lvl = int(level)
        self.exp = 0

        self.droppedExp = (self.lvl * 10000) // 6
        self._nextLvl = (self.lvl * 10000) // 5
    
        match evolve:
            case "False":
                self.canEvolve = False
            case "True":
                self.canEvolve = True
            case _:
                self.canEvolve = evolve
        self.stage = int(evolutionStage)
    
    def __str__(self):
        return f"{self.exp}/{self._nextLvl}"

    def increaseExperience(self, ammount):
        self.exp += ammount
        while self.exp >= self._nextLvl:
            self.exp -= self._nextLvl
            self.levelUp()

    def levelUp(self):
        self.lvl += 1
        self._nextLvl = (self.lvl * 10000) // 5
        self.droppedExp = (self.lvl * 10000) // 6
