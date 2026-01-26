class Stats():
    """
    Class desc:
    Stores and handle all numbered stats for a Pokemon-object

    Notes:
    Math is not fine tuned, balancing issue
    """
    def __init__(self, health = 70, attack = 81, defense = 75, speed = 70): # Defines attributes for the class when initializing
        """
        :param health: integer
        :param attack: integer
        :param defense: integer
        :param speed: integer
        """
        self.baseAtk = int(attack) # Base stats
        self.baseHp = int(health)
        self.baseDef = int(defense)
        self.spd = int(speed)      
        
        self.maxHp = self.baseHp # Main stats
        self.hp = self.maxHp
        self.atk = self.baseAtk
        self.defense = self.baseDef

    def __str__(self): # Returns all main stats as string
        return (f"HP: {self.hp}, ATK: {self.atk}, DEF: {self.defense}")
    
    def increaseHealth(self, amount): # Increases health data by a given amount and caps it off at max
        """
        :param amount: integer
        """
        self.hp += amount
        if self.hp > self.maxHp:
            self.hp = self.maxHp

    def decreaseHealth(self, amount): # Decreases health data by a given amount
        """
        :param amount: integer
        """         
        self.hp -= amount

    def increaseMaxHealth(self, lvl): # Increases max health relative to level
        """
        :param lvl: integer
        """        
        self.maxHp = self.baseHp + round(lvl * 1.6) 
        if self.hp > 0:
            self.hp = self.maxHp
        else:
            self.hp = 0
    
    def increaseAttack(self, lvl): # Increases attack relative to level
        """
        :param lvl: integer
        """        
        self.atk = self.baseAtk + round(lvl * 1.5)

    def increaseDefense(self, lvl): # Increases defense relative to level
        self.defense = self.baseDef + round(lvl * 1.4)

    def increaseSpeed(self): # Increases speed
        self.spd = round(self.spd * 1.1) 

    def increaseAllBaseStats(self): # Increases base stats, used for when pokemon evolves
        self.baseHp += 3
        self.baseAtk += 2
        self.baseDef += 1

    def increaseAllStats(self, pokemonLevel): # Calls all the increase stats methods, used for when pokemon levels up
        """
        :param pokemonLevel: integer
        """        
        self.increaseMaxHealth(pokemonLevel)
        self.increaseAttack(pokemonLevel)
        self.increaseDefense(pokemonLevel)
        self.increaseSpeed()