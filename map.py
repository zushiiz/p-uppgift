class Map: 
    """
    Class desc:
    Creates map and tracks/updates player position
    """
    def __init__(self, height = 10, width = 10): # Defines attributes for the class when initializing
        """
        :param height: integer
        :param width: integer
        """
        self.h = height
        self.w = width
        self.mapIcon = "o"

        # Creates a grid made of lists in the given width and height
        self.grid = [[self.mapIcon for _ in range(self.w)] for _ in range(self.h)]

        self.playerIcon = "p"
        self.playerX = 1
        self.playerY = 1
        self.grid[self.playerY][self.playerX] = self.playerIcon

    def __str__(self): # Returns all map elements as a grid, though x and y are inverted
        visualizedMap = ""
        for col in self.grid:
            for row in col:
                visualizedMap += str(row) + " "
            visualizedMap += "\n"
        return visualizedMap
    
    # x and y has now been switched for the ui-format, not changed here
    def movePlayer(self, y, x): # Updates a players x and y position
        """
        :param y: integer
        :param x: integer
        """
        y = self.playerY + y
        x = self.playerX + x
        try:
            if y < 0 or x < 0:
                print("Cannot move there")
            else:
                self.grid[y][x] = self.playerIcon
                self.grid[self.playerY][self.playerX] = self.mapIcon        
                self.playerY = y
                self.playerX = x
        except IndexError:
            raise IndexError("Out of bounds")