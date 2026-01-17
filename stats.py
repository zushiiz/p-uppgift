class Stats():
    def __init__(self, health = 70, attack = 81, defense = 75, speed = 70):
        self.baseAtk = int(attack)
        self.baseHp = int(health)
        self.baseDef = int(defense)
        self.spd = int(speed)      
        
        self.MaxHp = self.baseHp
        self.hp = self.MaxHp

        self.atk = self.baseAtk
        self.defense = self.baseDef

    def __str__(self):
        return (f"HP: {self.hp}, ATK: {self.atk}, DEF: {self.defense}")

        # Dubbelkolla all matte
    def increaseHealth(self, amount):
        self.hp += amount

    def decreaseHealth(self, amount):
         self.hp -= amount

    def increaseMaxHealth(self, lvl):
        self.MaxHp = self.baseHp + round(lvl * 1.6) 
        if self.hp > 0:
            self.hp = self.MaxHp
        else:
            self.hp = 0
    
    def increaseAttack(self, lvl):
        self.atk = self.baseAtk + round(lvl * 1.5)

    def increaseDefense(self, lvl):
        self.defense = self.baseDef + round(lvl * 1.4)

    def increaseSpeed(self):
        self.spd = round(self.spd * 1.1) 

    def increaseAllStats(self, pokemonLevel):
        self.increaseMaxHealth(pokemonLevel)
        self.increaseAttack(pokemonLevel)
        self.increaseDefense(pokemonLevel)
        self.increaseSpeed()
