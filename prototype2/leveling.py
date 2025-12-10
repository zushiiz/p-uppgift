class Leveling():
    def __init__(self, level = 1, evolve = True, stage = 0):
        self.lvl = int(level)
        self.exp = 0

        self.droppedExp = (self.lvl * 10000) // 6
        self._nextLvl = (self.lvl * 10000) // 5
    
        self.canEvole = evolve
        self.evolutionStage = stage
    
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
