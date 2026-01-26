class Movelist(list):
    """
    Class desc:
    Stores all moves for one Pokemon-object
    Inherits list
    """
    def __init__(self, *args): # Defines attributes for the class when initializing
        # *args make it possible to initialize the class with any amount of args as elements
        super().__init__(args)
        if len(self) > 4: # Temporary gate, this only sends error, no solution. Probably not gonna fix it for now since I'm not adding more date for attacks
            raise Exception("Movelist cannot contain more than 4 attack-objects")

    def __str__(self): # Returns a string with the name of every attack in the movelist
        attacks = ""
        for e in self:
            attacks += str(e) + "; "
        return attacks

class Attack():
    """
    Class desc:
    Stores data for an attack, ex: name, strength(atkMul)
    """
    def __init__(self, attackName = "untitled", attackMultiplier = 1): # Defines attributes for the class when initializing
        """
        :param attackName: string
        :param attackMultiplier: integer
        """
        self.name = attackName
        self.atkMul = int(attackMultiplier)
    
    def __str__(self): # returns name 
        return self.name

    def attack(self, dmg): # returns a damage value
        return self.atkMul * dmg