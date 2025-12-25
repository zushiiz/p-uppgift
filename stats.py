class Stats():
    def __init__(self, health = 70, attack = 81, defense = 75, speed = 70):
        self.MaxHp = int(health)
        self.atk = int(attack)
        self.defense = int(defense)
        self.spd = int(speed)

        self.hp = self.MaxHp

        self.baseAtk = 2
        self.baseHp = 10
        self.baseDef = 10        

    def __str__(self):
        return (f"HP: {self.hp}, ATK: {self.atk}, DEF: {self.defense}")

        # Dubbelkolla all matte
    def increaseHealth(self, amount):
        self.hp += amount

    def decreaseHealth(self, amount):
         self.hp -= amount

    def increaseMaxHealth(self):
        self.MaxHp += round(self.baseHp * 1.1) 
        if self.hp > 0:
            self.hp = self.MaxHp
    
    def increaseAttack(self):
        self.atk += round(self.baseAtk * 1.02)

    def increaseDefense(self):
        self.defense += round(self.baseDef * 1.02) 

    def increaseSpeed(self):
        self.spd = round(self.spd * 1.02) 

    def increaseAllStats(self):
        self.increaseMaxHealth()
        self.increaseAttack()
        self.increaseDefense()
        self.increaseSpeed()
