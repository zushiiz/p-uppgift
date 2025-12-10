class Stats():
    def __init__(self, health = 70, attack = 81, defense = 75, speed = 70):
        self.hp = int(health)
        self.atk = int(attack)
        self.defense = int(defense)
        self.spd = int(speed)

        self.baseAtk = 2
        self.baseHp = 10
        self.baseDef = 10        

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
