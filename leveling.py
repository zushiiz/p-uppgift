class Leveling():
    def __init__(self, level = 1, evolve = True, stage = 0):
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
        self.evolutionStage = int(stage)
    
    def __str__(self):
        return f"{self.exp}/{self._nextLvl}"

    def increaseExperience(self, ammount, stats):
        self.exp += ammount
        while self.exp >= self._nextLvl:
            self.exp -= self._nextLvl
            self.levelUp(stats)

    def levelUp(self, stats):
        self.lvl += 1
        self._nextLvl = (self.lvl * 10000) // 5
        self.droppedExp = (self.lvl * 10000) // 6
        stats.increaseAllStats()
