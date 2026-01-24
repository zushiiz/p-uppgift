class Player:
    def __init__(self, username = "Guest", team = ["Empty"], gui = None):
        self.name = username
        self.team = team
        self.activePokemon = team[0]

        self.potions = 10
        self.pokeballs = 10

        self.gui = gui
    
    def __str__(self):
        return (f"User: {self.name}")

        # while True:
        #     amountOfAttacks = []
        #     for i in range(len(self.activePokemon.attacks)):
        #         print(f"[{i}] {self.activePokemon.attacks[i]}")
        #         amountOfAttacks.append(i)
        #         i += 1
        #     print(f"[4] Back")
        #     try:
        #         userInput = int(input("What would you like to do?:"))
        #         if userInput == 4:
        #             return userInput
        #         elif userInput in amountOfAttacks:
        #             return userInput
        #         else:
        #             print("Please enter a valid digit")
        #             continue
        #     except ValueError:
        #         print("Please enter a digit")
        #         continue
    
    def swapOption(self, userInput): #Back is backbutton [4], back button is also hardcoded right now, need to test with more pokemon, alt. change it to b instad of 4
        print(f"Swapped {self.activePokemon} to {self.team[userInput]}")
        self.activePokemon = self.team[userInput+1] # Silvertape fix bruuuh
        
        # while True:
        #     pokemonPositions = {}
        #     for i in range(len(self.team)):
        #         if self.team[i] == self.activePokemon:
        #             continue
        #         else:
        #             print(f"[{i}] {self.team[i]}")
        #             pokemonPositions[i] = self.team[i]
        #             i += 1
        #     if back == True:
        #         print(f"[6] Back")
        #     try:
        #         userInput = int(input("What would you like to do?:"))
        #         if userInput == 6 and back == True:
        #             return userInput
        #         elif userInput in pokemonPositions.keys():
        #             if pokemonPositions[userInput].fainted == True:
        #                 print(f"{pokemonPositions[userInput]} has fainted and cannot be sent out")
        #                 continue
        #             else:
        #                 print(f"{self.name} swapped out {self.activePokemon} for {pokemonPositions[userInput]}")
        #                 self.activePokemon = pokemonPositions[userInput]
        #                 return self.activePokemon
        #         else:
        #             print("Please enter a valid digit")
        #             continue                   
        #     except ValueError:
        #         print("Please enter a digit")
        #         continue

    def itemsOption(self): # Max ammount is hardcoded for now
        while True:
            print(f"[0] Healing potions: {self.potions}/10")
            print(f"[1] Pokeballs: {self.pokeballs}/10")
            print("[2] Back")

            try:
                userInput = int(input("What would you like to do?:"))
                match userInput:
                    case 0 if self.potions > 0:
                        playerActionIndex = self.healPokemon()
                        if playerActionIndex != 6:
                            break
                    case 0 if self.potions <= 0:
                        print("You don't have any potions left!")
                        continue
                    case 1 if self.pokeballs > 0:
                        self.pokeballs -= 1
                        return userInput
                    case 1 if self.pokeballs <= 0:
                        print("You don't have any pokeballs left!")
                        continue
                    case 2:
                        return userInput
                    case _:
                        print("Please enter a valid digit")
                        continue                                        
            except ValueError:
                print("Please enter a valid digit")
                continue                
    
    def healPokemon(self):
        while True:
            pokemonPositions = {}
            for i in range(len(self.team)):
                print(f"[{i}] {self.team[i]}")
                pokemonPositions[i] = self.team[i]
                i += 1
            print("[6] Back")

            try:
                userInput = int(input("Which pokemon do you want to heal?"))
                if userInput == 6:
                    return userInput
                elif userInput in pokemonPositions.keys() and pokemonPositions[userInput].fainted == False:
                    pokemonPositions[userInput].stats.increaseHealth(100) #Healing amount hardcoded
                    self.potions -= 1
                    print(f"After healing {pokemonPositions[userInput].stats}")
                    break
                else:
                    print("Please enter a valid digit")
                    continue                    
            except ValueError:
                print("Please enter a digit")
                continue

    def changeActivePokemon(self):
        print("Choose active Pokemon!")
        pokemonPositions = {}
        for i in range(len(self.team)):
            print(f"[{i}] {self.team[i].name}")
            pokemonPositions[i] = self.team[i]
            i += 1
        while True:
            try:
                userInput = int(input(":"))
                if userInput in pokemonPositions.keys():
                    self.team.insert(0, self.team.pop(userInput))
                    self.activePokemon = self.team[0]
                    break
                else:
                    continue
            except ValueError:
                continue
