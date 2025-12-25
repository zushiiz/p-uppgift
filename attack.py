class MoveList(list):
    def __init__(self, *args):
        super().__init__(args)
        if len(self) > 4: # Check for better logic, possibly could remove this
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
    
    def __str__(self):
        return self.name

    def attack(self, dmg):
        return self.atkMul * dmg