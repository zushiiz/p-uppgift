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


class Pokemon(): 
    def __init__(self, name, stats = Stats(), moves = MoveList(Attack("Scratch")), leveling = Leveling(), nextEvolution = "Abba"):
        self.name = name

        self.stats = stats
        self.leveling = leveling
        self.attacks = moves

        self.baseAtk = 2
        self.baseHp = 10
        self.baseDef = 10

        self.evolution = nextEvolution
        self.levelToEvolve = 16

        self.fainted = False

    def __str__(self):
        return (f"{self.name},\nlvl.{self.lvl}")
    
    def gainExp(self, exp, pokemonList):
        self.leveling.increaseExperience(exp, self.stats)
        while self.leveling.lvl >= self.levelToEvolve:
            userInput = input(f"{self.name} is evolving! y/n?").lower()
            match userInput:
                case "y":
                    updatedEvolution = getEvolutionName(pokemonList)
                    self.evole(updatedEvolution)
                case "n":
                    break
                case _:
                    pass
    
    def evolve(self, ):
        self.name = self.evolution
        self.baseAtk += 1
        self.baseHp += 1
        self.baseDef += 1
    
    def attack(self, other, attack): # Rename shit bruh
        other.damaged(self.attacks[attack].attack(self.stats.atk))

    def damaged(self, dmg):
        self.stats.decreaseHealth(round((self.defense * 0.001) * dmg))
        if self.stats.hp <= 0:
            self.fainted = True
        else:
            pass

def getEvolutionName(pokemonList, pokemonObj):
    for e in pokemonList:
        if e.name == pokemonObj.evolution:
            if pokemonObj.leveling.canEvole == False:
                return e.name
            else:
                return e.evolution
        else: # Byt till pass?
            print("bombaclat")

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