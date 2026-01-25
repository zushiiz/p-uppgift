class Movelist(list):
    """
    Class desc:
    Stores all moves for one Pokemon-object
    Inherits list
    """
    def __init__(self, *args): # *args make it possible to initialize the class with any amount of args as elements
        super().__init__(args)
        if len(self) > 4: # Temporary gate, this only sends error, no solution. Probably not gonna fix it for now since I'm not adding more date for attacks
            return -1
        else:
            pass

    def __str__(self):
        attacks = ""
        for e in self:
            attacks += str(e) + "; "
        return attacks

class Attack():
    """
    Class desc:
    Stores data for an attack, ex: name, strength(atkMul)
    """
    def __init__(self, attackName = "untitled", attackMultiplier = 1):
        self.name = attackName
        self.atkMul = int(attackMultiplier)
    
    def __str__(self):
        return self.name

    def attack(self, dmg):
        return self.atkMul * dmg