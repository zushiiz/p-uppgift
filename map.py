import random
class Map: # [y][x] coordinate type
    def __init__(self, height = 10, width = 15):
        self.h = height
        self.w = width
        self.mapIcon = "o"
        self.grid = [[self.mapIcon for _ in range(self.w)] for _ in range(self.h)]

        self.playerIcon = "p"
        self.playerX = 1
        self.playerY = 1
        self.grid[self.playerY][self.playerX] = self.playerIcon

    def __str__(self):
        visualizedMap = ""
        for col in self.grid:
            for row in col:
                visualizedMap += str(row) + " "
            visualizedMap += "\n"
        return visualizedMap
    
    def movePlayer(self, y, x):
        try:
            print(y)
            print(x)
            if y < 0 or x < 0:
                print("Cannot move there")
            else:
                self.grid[y][x] = self.playerIcon
                self.grid[self.playerY][self.playerX] = self.mapIcon            
                self.playerY = y
                self.playerX = x
        except IndexError:
            print("Cannot move there")

    def userInterface(self):
        i = 0
        while i != 1:
            print(self)
            try:
                userInput = int(input("Move\n" \
                                      "[0] Up\n" \
                                      "[1] Down\n" \
                                      "[2] Left\n" \
                                      "[3] Right\n" \
                                      "[4] Team\n" \
                                      "[5] Save and quit\n" \
                                      ":"))
                match userInput:
                    case 0:
                        self.movePlayer(self.playerY-1, self.playerX)
                    case 1:
                        self.movePlayer(self.playerY+1, self.playerX)
                    case 2:
                        self.movePlayer(self.playerY, self.playerX-1)
                    case 3:
                        self.movePlayer(self.playerY, self.playerX+1)
                    case 4:
                        return 0
                    case 5:
                        return 1
                    case _:
                        print("Invalid input")
                        continue        
                i = random.randint(1, 5)
            except ValueError:
                print("Invalid input")
                continue
            return None