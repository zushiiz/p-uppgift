class MoveList(list):
    def __init__(self, *args):
        super().__init__(args)
        if len(self) > 4: # Felhantering för fler än 4 moves
            return -1
        else:
            pass

    def __str__(self):
        attacks = ""
        for e in self:
            attacks += str(e) + "; "
        return attacks

class Attack():
    def __init__(self, attackName = "untitled", attackMultiplier = 1):
        self.name = attackName
        self.atkMul = int(attackMultiplier)
    
    def attack(self, dmg):
        return self.atkMul * dmg

class Stats():
    def __init__(self, health = 70, attack = 81, defense = 75, speed = 70):
        self.hp = health
        self.atk = attack
        self.defense = defense
        self.spd = speed

        # Dubbelkolla all matte
    def increaseHealth(self):
        self.hp += round(self.baseHp * 1.1) 

    def decreaseHealth(self, ammount):
         self.hp -= ammount
    
    def increaseAttack(self):
        self.atk += round(self.baseAtk * 1.02)

    def increaseDefense(self):
        self.defense += round(self.baseDef * 1.02) 

    def increaseSpeed(self):
        self.spd = round(self.spd * 1.02) 

    def increaseAllStats(self):
        self.increaseHealth()
        self.increaseAttack()
        self.increaseDefense()
        self.increaseSpeed()

class Leveling():
    def __init__(self, level = 1, evolve = True, stage = 1, evolutions = []):
        self.lvl = int(level)
        self.exp = 0
        self.droppedExp = (self.lvl * 10000) // 6
        self._nextLvl = (self.lvl * 10000) // 5

        self.nextEvo = 16
    
        self.evole = evolve
        if self.evole == True:
            self.evolutions = evolutions
        int(self.evolutionStage) = stage
    
    def increaseExperience(self, ammount, stats):
        self.exp += ammount
        while self.exp >= self._nextLvl:
            self.exp -= self._nextLvl
            self.levelUp(stats)
            if self.lvl >= self.nextEvo
    
    def levelUp(self, stats):
        self.lvl += 1
        self._nextLvl = (self.lvl * 10000) // 5
        self.droppedExp = (self.lvl * 10000) // 6
        stats.increaseAllStats()

    def evolve(self):
        self.leveling.evolutionStage += 1
        self.name = self.leveling.evolutions[self.leveling.evolutionStage]    

class Pokemon(): # Dela upp i mer objekt, stats-objekt, evolution, leveling
    def __init__(self, name, stats = Stats(), moves = MoveList(Attack("Scratch")), leveling = Leveling()):
        self.name = name

        self.stats = stats
        self.leveling = leveling
        self.attacks = moves

        self.baseAtk = 2
        self.baseHp = 10
        self.baseDef = 10

        self.fainted = False

    def __str__(self):
        return (f"{self.name},\nlvl.{self.lvl}")
    
    # def info(self):
    #     print(f"Name: {self.name}\nLevel: {self.lvl} exp: {self.exp}/{self._nextLvl} \nHealth: {self.hp}\nAttack: {self.atk}\nDefense: {self.defense}\n")

    def gainExp(self, exp):
        self.leveling.increaseExperience(exp, self.stats)
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        self.stats.decreaseHealth(round((self.defense * 0.001) * dmg))
        if self.stats.hp <= 0:
            self.fainted = True
        else:
            pass

def main():
    p1 = Pokemon("aba")
    p2 = Pokemon("bab")
    p2.info()
    p1.info()
    p1.gainExp(10000)
    p1.attack(p2, 0)
    p1.info()
    p2.info()
    p1.gainExp(1000000)
    p1.info()

main()