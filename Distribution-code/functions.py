import config
import datetime 
import json
import pygame 
import random
import requests
import time



class Preference:
    def __init__(self, username: str="Guest", up: int=pygame.K_w, down: int=pygame.K_s, left: int=pygame.K_a,
                 right: int=pygame.K_d, interact: int=pygame.K_f, use: int=pygame.K_e, volume: int=0.5):
        self.__buttonUp = up
        self.__buttonDown = down
        self.__buttonLeft = left
        self.__buttonRight = right
        self.__buttonInteract = interact
        self.__buttonUse = use
        self.__volume = volume
        self.__username = username
        self.__lastTime = "0:00:00.00"

    def __dir__(self):
        return [pygame.key.name(self.__buttonUp), pygame.key.name(self.__buttonDown), 
                pygame.key.name(self.__buttonRight), pygame.key.name(self.__buttonLeft),
                pygame.key.name(self.__buttonUse), pygame.key.name(self.__buttonInteract)]

    # Getter method for self.__volume
    @property
    def volume(self):
        return self.__volume
    
    # Getter method for self.__buttonInteract
    @property
    def buttonInteract(self):
        return self.__buttonInteract
    
    # Getter method for self.__buttonUse
    @property
    def buttonUse(self):
        return self.__buttonUse

    # Getter method for self.__buttonUp
    @property
    def buttonUp(self):
        return self.__buttonUp

    # Getter method for self.__buttonDown
    @property
    def buttonDown(self):
        return self.__buttonDown
    
    # Getter method for self.__buttonLeft
    @property
    def buttonLeft(self):
        return self.__buttonLeft
    
    # Getter method for self.__buttonRight
    @property
    def buttonRight(self):
        return self.__buttonRight
    
    # Getter method for self.__username
    @property
    def username(self):
        return self.__username
    
    # Getter method for self.__lastTime
    @property
    def lastTime(self):
        return self.__lastTime
    
    # Setter method for self.__lastTime
    @lastTime.setter
    def lastTime(self, lastTime: str):
        if lastTime is not None:
                self.__lastTime = lastTime

    # Setter method for self.__buttonUp
    @username.setter
    def username(self, username: str):
        if username is not None:
            self.__username = username

    # Setter method for self.__buttonUp
    @buttonUp.setter
    def buttonUp(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonUp = key

    # Setter method for self.__buttonDown
    @buttonDown.setter
    def buttonDown(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonDown = key

    # Setter method for self.__buttonRight
    @buttonRight.setter
    def buttonRight(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonRight = key

    # Setter method for self.__buttonLeft
    @buttonLeft.setter
    def buttonLeft(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonLeft = key

    # Setter method for self.__buttonUse
    @buttonUse.setter
    def buttonUse(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonUse = key

    # Setter method for self.__buttonInteract
    @buttonInteract.setter
    def buttonInteract(self, key: int):
        if key is not None:
            if pygame.key.name(key).isalpha():
                self.__buttonInteract = key

    # Setter method for self.__volume
    @volume.setter
    def volume(self, value: int):
        if value is not None:
            if value >= 0 and value <= 1:
                self.__volume = value

    def save(self) -> None:
        # Get the user data from database
        with open(config.localDatabasePath, "r") as f:
            userData = json.load(f)

        # Modify database with preferences data
        userData[0]["username"] = self.__username
        userData[0]["controls"]["up"] = self.__buttonUp
        userData[0]["controls"]["down"] = self.__buttonDown
        userData[0]["controls"]["left"] = self.__buttonLeft
        userData[0]["controls"]["right"] = self.__buttonRight
        userData[0]["controls"]["use"] = self.__buttonUse
        userData[0]["controls"]["interact"] = self.__buttonInteract
        userData[0]["volume"] = self.__volume

        # Write the changes in database
        with open(config.localDatabasePath, "w") as f:
            json.dump(userData, f)

    def check_best_score(self, map: str) -> None:
        # Open local database and get the information stored in JSON format
        with open(config.localDatabasePath, "r") as f:
            localData = json.load(f)

        bestTime = localData[0]["bestTime"][map] # Access the best time registered in the database
        lastTime = self.__lastTime # Access the last time
        # Get the number of seconds based on the string h:mm:ss.msms
        lastTimeSeconds = int(lastTime[0]) * 3600 + int(lastTime[2:4]) * 60 + int(lastTime[5:7]) + int(lastTime[8:]) / 100 
        bestTimeSeconds = int(bestTime[0]) * 3600 + int(bestTime[2:4]) * 60 + int(bestTime[5:7]) + int(bestTime[8:]) / 100
        if lastTimeSeconds < bestTimeSeconds: # Compare the amonuts of seconds
            bestTime = self.__lastTime # If it's lower time it store as the best time
            # Send the best result to the server
            request = requests.post("http://127.0.0.1:5000/bestTime", json={"bestTime": bestTime, "map": map, "username": self.__username})
        localData[0]["bestTime"][map] = bestTime # Update the local data

        # Open and write the updated data
        with open(config.localDatabasePath, "w") as f:
            json.dump(localData, f)

class System:
    def __init__(self, preferences: Preference):
        self.__screenObj = pygame.display.set_mode((800, 800))
        self.__screenName = ""
        self.__background = None
        self.__button = None
        self.__gameplay = None
        self.__minigame = None
        self.__textbox = ""
        self.__preferences = preferences

    # Getter method for self.__screenObj
    @property
    def screenObj(self):
        return self.__screenObj

    # Enable the access of the private attribute screenName
    @property
    def screenName(self):
        return self.__screenName
    
    # Enable the access of the private attribute minigame
    @property
    def minigame(self):
        return self.__minigame

    # Getter method for self.__button
    @property
    def button(self):
        return self.__button
    
    # Getter method for self.__preferences
    @property
    def preferences(self):
        return self.__preferences
    
    # Getter method for self.__gameplay
    @property
    def gameplay(self):
        return self.__gameplay
    
    # Getter method for self.__textbox
    @property
    def texbox(self):
        return self.__textbox
    
    # Setter method for self.__textbox
    @texbox.setter
    def textbox(self, newText: str):
        if newText is not None:
            self.__textbox = newText

    def render_screen(self, nextScreen: str) -> None:
        #Reset the textbox and buttons
        self.__button = None
        self.__textbox = None

        # Uses the next screen actions
        match nextScreen:
            case "menu":
                self.__gameplay = None
                # Create the buttons: start, rank, option and quit, the format is [name, (x-coordinate, y-coordinate)]
                self.__button = Button(buttons=[["start", (239, 275)], ["rank", (267, 400)], ["options", (175, 525)], ["quit", (276, 650)]],
                                        system=self)
                # Load the menu background, menu-screen.png
                self.__background = pygame.image.load(config.menuScreenPath).convert_alpha()
            case "username":
                # Load the username-screen that is the username registed screen, texbox starts empty
                self.__background = pygame.image.load(config.usernameScreenPath).convert_alpha()
                self.__textbox = ""
            case "rank":
                # Load the rank background, rank-screen.png
                self.__background = pygame.image.load(config.rankScreenPath)
            case "options":
                # Create the arrow for options selection, the format is [name, [x-coordinate, y-coordinate]]
                self.__button = Button(buttons=[["arrow", [590, 275]]], system=self)
                # Load the username-screen that is the options screen, here user can change the predefined keys and volume
                self.__background = pygame.image.load(config.optionsScreenPath).convert_alpha()
            case "start":
                # Create the buttons: map 1 and map 2, the format is [name, (x-coordinate, y-coordinate)]
                self.__button = Button(buttons=[["baker", (250, 350)], ["usbourne", (250, 500)]], system=self)
                # Loads the map selection background, it's the same of menu but with different buttons
                self.__background = pygame.image.load(config.menuScreenPath).convert_alpha() 
            case "baker":
                self.__minigame = None # Reset the minigame
                if self.__gameplay is None: # Only creates a new gameplay if there isn't already one
                    laser = Sprite(image=config.bakerLaserPath, coordinate=(385, 22)) # Create the laser sprite
                    timeNow = datetime.datetime.now() # Get the current time
                    server = pygame.Rect(0, 5, 216, 94) # Create the server hitbox
                    guard = Guard(image=config.guardSpritePath, coordinate=(330, 600), system=self) # Create the guard sprite
                    player = Player(system=self, coordinate=config.bakerInitialPosition) # Create the player sprite
                    codeDoor = Sprite(image=config.codeDoorPath, coordinate=(73, 256)) # Create the sprite of the door with code lock
                    lockDoor = Sprite(image=config.lockDoorPath, coordinate=(657, 303)) # Create the sprite of the door with normal lock
                    # Store and control the information about the current gameplay session
                    self.__gameplay = Gameplay(map="baker", startTime=timeNow, walls=config.bakerWalls, searchablePlaces=config.bakerSearchable,
                                                player=player, guard=guard, laser=laser, system=self, statueCoordinate=(425, 60),
                                                door=config.bakerDoor, codeDoor=codeDoor, lockDoor=lockDoor, server=server) 
                # Load the map 1 background, Baker Avenue
                self.__background = pygame.image.load(config.bakerScreenPath).convert_alpha()
            case "usbourne":
                self.__minigame = None # Reset the minigame
                if self.__gameplay is None: # Only creates a new gameplay if there isn't already one
                    laser = Sprite(image=config.usbourneLaserPath, coordinate=(601, 22))
                    timeNow = datetime.datetime.now() # Get the current time
                    server = pygame.Rect(5, 703, 214, 78) # Create the server hitbox
                    player = Player(system=self, coordinate=config.usbourneInitialPosition) # Create the guard sprite
                    guard = Guard(image=config.guardSpritePath, coordinate=(380, 600), system=self) # Create the player sprite
                    codeDoor = Sprite(image=config.codeDoorPath, coordinate=(322, 223)) # Create the sprite of the door with code lock
                    lockDoor = Sprite(image=config.lockDoorPath, coordinate=(322, 670)) # Create the sprite of the door with normal lock
                    # Store and control the information about the current gameplay session
                    self.__gameplay = Gameplay(map="usbourne", startTime=timeNow, walls=config.usbourneWalls, 
                                               searchablePlaces=config.usbourneSearchable, player=player, guard=guard, 
                                               laser=laser, system=self, statueCoordinate=(690, 80), door=config.usbourneDoor, 
                                               codeDoor=codeDoor, lockDoor=lockDoor, server=server)
                # Load the map 2 background, Usbourne Way
                self.__background = pygame.image.load(config.usbourneScreenPath).convert_alpha()
            case "pause":
                # Create the buttons: continue and menu, the format is [name, (x-coordinate, y-coordinate)]
                self.__button = Button(buttons=[["continue", (135, 300)], ["menu-pause", (260, 475)]], system=self)
                # Load pause screen, here player choose to return to menu or continue the mission
                self.__background = pygame.image.load(config.pauseScreenPath).convert_alpha()
            case "mission-completed":
                self.__minigame = None # Reset the minigame
                # Load the menu background, menu-screen.png
                self.__background = pygame.image.load(config.missionCompletedScreenPath).convert_alpha()
            case "fingerprint":
                sequence = random.sample(range(0, 10), 3)
                self.__minigame = Fingerprint(correctSequence=sequence, system=self)
                # The background of fingerprint minigame screen
                self.__background = pygame.image.load(config.fingerprintScreenPath).convert_alpha()
            case "lockpick":
                sequence = config.lockpickSequence.copy() 
                random.shuffle(sequence)
                self.__minigame = Lockpick(correctSequence=sequence, system=self)
                # The background of lockpick minigame screen
                self.__background = pygame.image.load(config.lockpickScreenPath).convert_alpha() 
            case "hacking":
                elements = random.choice(config.hackingSequences)
                self.__minigame = Hacking(correctSequence=elements[1], system=self, word=elements[0])
                self.__background = pygame.image.load(config.hackingScreenPath)
            case "game-over":
                self.__minigame = None
                self.__background = pygame.image.load(config.gameOverScreenPath).convert_alpha()
        self.__screenName = nextScreen
        self.__screenObj.blit(self.__background, (0, 0))
        self.display_buttons() # Display the buttons (screens with buttons)
        self.display_textbox() # Display the textbox (username register screen only)
        self.display_rank() # Display the rank (rank screen only)
        self.display_options() # Display the preferences (options screen only)
        self.display_sprites() # Display the sprites (Baker Avenue and Usbourne Way screens)
        self.display_result() # Display the final time (mission completed only)

    def update_screen(self) -> None:
        self.__screenObj.blit(self.__background, (0,0)) # Print background
        self.display_buttons() # Display buttons
        self.display_textbox() # Display textbox
        self.display_rank() # Display users in ranking
        self.display_options() # Display the current options
        self.display_sprites() # Display the sprites
        self.display_result() # Display the final time (mission completed only)
        self.display_sequence() # Starts the minigame displaying the sequence
    
    def display_buttons(self) -> None:
        #Check if there is some button
        if self.__button is not None:
            buttons = self.__button.buttons # List of all buttons
            selectedButtonIndex = self.__button.selectedButtonIndex # The position in the list of the selected button
            backgrounds = self.__button.backgrounds # Buttons backgrounds

            #Select the buttons in list, each one has a format [name, (x-coordinate, y-coordinate)]
            for button in buttons:
                img = pygame.image.load(backgrounds[button[0]]).convert_alpha() # Load button background

                # Check if it's the selected button
                if button == buttons[selectedButtonIndex]:
                    width = img.get_width() 
                    height = img.get_height() 
                    # Change the sizes by a facto 1.3
                    newWidth = width * 1.3
                    newHeight = height * 1.3
                    img = pygame.transform.scale(img, (newWidth, newHeight)) # Change the button scale
                    x = button[1][0]
                    y = button[1][1]
                    self.__screenObj.blit(img, (x - ((newWidth - width)/2), y - ((newHeight - height)/2))) # Recalculate the position
                                                                                                           # in screen and print it
                    continue
                self.__screenObj.blit(img, button[1]) # Print button in normal scale and position
        
    def display_textbox(self) -> None:
        # Check if there is textbox
        if self.__textbox is not None:
            font = pygame.font.Font(None, 48) # Uses the standar font and size 48
            text_surface = font.render(self.__textbox, True, (0, 0, 0)) # Render the font with black colour
            text_rect = text_surface.get_rect(center=(400, 400)) # Create a surface for textbox
            self.__screenObj.blit(text_surface, text_rect) # Print the surface

    def display_rank(self) -> None:
        if self.__screenName == "rank":
            # Request the JSON file to the server and extract the content from response
            response = requests.get("http://127.0.0.1:5000/rank")
            rank = response.json()

            font = pygame.font.Font(None, 24) # Uses the standard font and size 48

            # It will print the Baker Avenue ranking
            baker = rank["Baker"] # Get the list for Baker Avenue rank
            for x in range(len(baker)): # It will pass through all possible indexes
                userB = baker[x] # Get element in that index, it has the format [username, time in seconds]
                text_surface = font.render(f"{userB[0]} -> {str(userB[1])}", True, (235, 165, 59)) # Render the font with black colour
                text_rect = text_surface.get_rect(topleft=(150, 265 + 50 * x)) # Create a surface for textbox, we can adjust the y-coordinate 
                                                                              # of each y-coordinate of each  buttons based on its index
                self.__screenObj.blit(text_surface, text_rect) # Print the surface

            # It will print the Usbourne Way ranking
            usbourne = rank["Usbourne"] # Get the list for Usbourne Way rank
            for x in range(len(usbourne)): # It will pass through all possible indexes
                userU = usbourne[x] # Get element in that index,  it has the format [username, time in seconds]
                text_surface = font.render(f"{userU[0]} -> {str(userU[1])}", True, (235, 165, 59)) # Render the font with black colour
                text_rect = text_surface.get_rect(topleft=(535, 265 + 50 * x)) # Create a surface for textbox, we can adjust the y-coordinate 
                                                                              # of each y-coordinate of each  buttons based on its index
                self.__screenObj.blit(text_surface, text_rect) # Print the surface

    def display_options(self) -> None:
        if self.__screenName == "options":
            # Creare a rectangle 10x20 and print it in the middle of volume bar
            rect = pygame.Rect(242 + 300 * self.__preferences.volume, 275, 10, 20) # The position in bar is defined by volume,
                                                                                   # that is a factor of original volume
            pygame.draw.rect(self.__screenObj, (235, 165, 59), rect) # Print with peach colour

            # Print each button current preference in the correct place
            keys = self.__preferences.__dir__() # Return the lits of button preferences [up, down, right, left, use, interaction]
            font = pygame.font.Font(None, 48) # Uses the standard text and size 48
            for x in range(6): # Pass through the index of all buttons preferences in the list
                key = keys[x] # Get the button preference in index x
                text_surface = font.render(key, True, (235, 165, 59)) # Render the font with peach colour
                text_rect = text_surface.get_rect(center=(570, 350 + 70 * x)) # Create a surface for textbox
                self.__screenObj.blit(text_surface, text_rect) # Print the text
        
    def display_sprites(self) -> None:
        if self.__screenName in ["baker",  "usbourne"]: # Only displays sprites during gameplay screens
            if not self.__gameplay.player.rect.colliderect(config.inventoryArea): # Won't display the main character above the inventory
                self.__screenObj.blit(self.__gameplay.player.image, self.__gameplay.player.rect) # Print the main character
            if not self.__gameplay.guard.rect.colliderect(config.inventoryArea): # Won't display the guard above the inventory
                self.__screenObj.blit(self.__gameplay.guard.image, self.__gameplay.guard.rect) # Display the guard
            if self.__gameplay.statue is not None: # Only display if the statue wasn't stolen yet
                self.__screenObj.blit(self.__gameplay.statue.image, self.__gameplay.statue.rect) # Print the statue
            if self.__gameplay.codeDoor is not None: # Only display if the fingerprint minigame isn't comepleted and door still in its place
                # It prints the door in the original direction if it's the baker map
                if self.__gameplay.map == "baker": 
                    self.__screenObj.blit(self.__gameplay.codeDoor.image, self.__gameplay.codeDoor.rect)
                # It rotates the door before print if it's the usbourne map
                else:
                    rotatedImg = pygame.transform.rotate(self.__gameplay.codeDoor.image, 90) # Rotate in the top left vertex
                    rotateRect = rotatedImg.get_rect(topleft=self.__gameplay.codeDoor.rect.topleft) # Create the new hitbox
                    self.__screenObj.blit(rotatedImg, rotateRect)
            if self.__gameplay.lockDoor is not None: # Only display if the lockpick minigame isn't comepleted and door still in its place
                # It prints the door in the original direction if it's the baker map
                if self.__gameplay.map == "baker": 
                    self.__screenObj.blit(self.__gameplay.lockDoor.image, self.__gameplay.lockDoor.rect)
                # It rotates the door before print if it's the usbourne map
                else:
                    rotatedImg = pygame.transform.rotate(self.__gameplay.lockDoor.image, 90) # Rotate in the top left vertex
                    rotateRect = rotatedImg.get_rect(topleft=self.__gameplay.lockDoor.rect.topleft) # Create the new hitbox
                    self.__screenObj.blit(rotatedImg, rotateRect)
            if self.__gameplay.laser is not None: # Display laser if the hacking minigame isn't completed
                self.__screenObj.blit(self.__gameplay.laser.image, self.__gameplay.laser.rect)

    def display_result(self) -> None:
        if self.__screenName == "mission-completed": # Display the final result only on the mission completed screen
            font = pygame.font.Font(None, 80) # Uses the standar font and size 48
            text_surface = font.render(self.__preferences.lastTime, True, (235, 165, 59)) # Render the font with peach colour
            text_rect = text_surface.get_rect(topleft=(95, 640)) # Create a surface for textbox
            self.__screenObj.blit(text_surface, text_rect) # Print the result

    def display_sequence(self) -> None:
        if self.__minigame is not None:
            self.__minigame.start()

class Minigame:
    def __init__(self, correctSequence: list, system: System):
        self.__correctSequence = correctSequence
        self.__userSequence = []
        self.__system = system

    # Getter method for self.__correctSequence
    @property
    def correctSequence(self):
        return self.__correctSequence
    
    # Getter method for self.__system
    @property
    def system(self):
        return self.__system
    
    # Getter method for self.__userSequence
    @property
    def userSequence(self):
        return self.__userSequence
    
    # Setter method for self.__correctSequence
    @correctSequence.setter
    def correctSequence(self, value: list):
        if type(value) == list:
            self.__correctSequence = value

    # Setter method for self.__userSequence
    @userSequence.setter
    def userSequence(self, value: list):
        if type(value) == list:
            self.__userSequence = value

    def check(self) -> None:
        if self.__userSequence != self.__correctSequence:
            self.__system.gameplay.player.lives -= 1
            if self.__system.gameplay.map == "baker":
                self.__system.gameplay.player.rect.topleft = config.bakerInitialPosition
            else:
                self.__system.gameplay.player.rect.topleft = config.usbourneInitialPosition
            self.__system.render_screen(nextScreen=self.__system.gameplay.map)

class Fingerprint(Minigame):
    def start(self) -> None:
        num1 = self.correctSequence[0]
        weakFinger = pygame.image.load(config.weakFingerprintPath).convert_alpha()
        self.system.screenObj.blit(weakFinger, config.numbersPositions[num1])
        num2 = self.correctSequence[1]
        midFinger = pygame.image.load(config.midFingerprintPath).convert_alpha()
        self.system.screenObj.blit(midFinger, config.numbersPositions[num2])
        num3 = self.correctSequence[2]
        strongFinger = pygame.image.load(config.strongFingerprintPath)
        self.system.screenObj.blit(strongFinger, config.numbersPositions[num3])

    def check(self) -> None:
        super().check()
        if self.userSequence == self.correctSequence:
            if self.system.gameplay.map == "baker":
                self.system.gameplay.walls.remove(config.bakerCodeDoor)
            else:
                self.system.gameplay.walls.remove(config.usbourneCodeDoor)
            self.system.gameplay.codeDoor = None
            self.system.render_screen(nextScreen=self.system.gameplay.map)

class Hacking(Minigame):
    def __init__(self, correctSequence: list, system: System, word: str):
        super().__init__(correctSequence=correctSequence, system=system)
        self.__word = word

    def start(self) -> None:
        font = pygame.font.Font(None, 48)
        text = font.render(self.__word, True, (0, 255, 0))
        rect = text.get_rect(center=(400, 400))
        self.system.screenObj.blit(text, rect)

    def check(self) -> None:
        super().check()
        if self.userSequence == self.correctSequence:
            self.system.gameplay.laser = None
            self.system.render_screen(nextScreen=self.system.gameplay.map)

class Lockpick(Minigame):
    def __init__(self, correctSequence: list, system: System):
        super().__init__(correctSequence=correctSequence, system=system)
        self.__printableSequence = correctSequence.copy()

    def start(self) -> None:
        try:
            time.sleep(0.5)
            item = self.__printableSequence[0]
            match item:
                case pygame.K_LEFT:
                    img = pygame.image.load(config.lockpickBackgrounds[pygame.K_LEFT])
                    self.system.screenObj.blit(img, (334, 519))
                case pygame.K_RIGHT:
                    img = pygame.image.load(config.lockpickBackgrounds[pygame.K_RIGHT])
                    self.system.screenObj.blit(img, (334, 519))
                case pygame.K_UP:
                    img = pygame.image.load(config.lockpickBackgrounds[pygame.K_UP])
                    self.system.screenObj.blit(img, (334, 519))
                case pygame.K_DOWN:
                    img = pygame.image.load(config.lockpickBackgrounds[pygame.K_DOWN])
                    self.system.screenObj.blit(img, (334, 519))
            self.__printableSequence.remove(item)
        except:
            return
        
    def check(self) -> None:
        super().check()
        if self.userSequence == self.correctSequence:
            if self.system.gameplay.map == "baker":
                self.system.gameplay.walls.remove(config.bakerLockDoor)
            else:
                self.system.gameplay.walls.remove(config.usbourneLockDoor)
            self.system.gameplay.lockDoor = None
            self.system.render_screen(nextScreen=self.system.gameplay.map)

class Sprite:
    def __init__(self, image: str, coordinate: tuple):
        self.__image = pygame.image.load(image).convert_alpha()
        self.__rect = self.__image.get_rect(topleft=coordinate)

    # Getter method for self.__image
    @property
    def image(self):
        return self.__image
    
    # Getter method for self.__rect
    @property
    def rect(self):
        return self.__rect

class Guard(Sprite):
    def __init__(self, image: str, coordinate: tuple, system: System):
        super().__init__(image=image, coordinate=coordinate)
        self.__moveX = 5
        self.__moveY = 0
        self.__system = system

    def move(self) -> None:
        if self.__system.screenName in ["baker", "usbourne"]:
            self.rect.x += self.__moveX
            self.rect.y += self.__moveY
        if self.__system.screenName == "baker":
            if self.rect.topleft == (330, 330):
                self.__moveX = 0
                self.__moveY = 5
            elif self.rect.topleft == (330, 600):
                self.__moveX = 5
                self.__moveY = 0
            elif self.rect.topleft == (615, 600):
                self.__moveX = 0
                self.__moveY = -5
            elif self.rect.topleft == (615, 330):
                self.__moveX = -5
                self.__moveY = 0
        else:
            if self.rect.topleft == (380, 400):
                self.__moveX = 0
                self.__moveY = 5
            elif self.rect.topleft == (380, 600):
                self.__moveX = 5
                self.__moveY = 0
            elif self.rect.topleft == (705, 600):
                self.__moveX = 0
                self.__moveY = -5
            elif self.rect.topleft == (705, 400):
                self.__moveX = -5
                self.__moveY = 0

class Player(Sprite):
    def __init__(self, system: System, coordinate: tuple):
        super().__init__(image=config.mainSpritePath, coordinate=coordinate)
        self.__lives = 3
        self.__inventory = []
        self.__system = system

    # Getter method for self.__inventory
    @property
    def inventory(self):
        return self.__inventory
    
    # Getter method for self.__lives
    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, value: int):
        if value is not None:
            self.__lives = value

    def movement(self) -> None:
        keys = pygame.key.get_pressed() # Provide a dict that says if key is pressed or not, uses True and False values
        if keys[self.__system.preferences.buttonUp]: # If up button is being pressed
            self.rect.y -= 4 # Velocity of 4 pixels
            wall = self.check_collision() # Check if collided with something
            if wall is not None: # Only if collided
                self.rect.top = wall.bottom # The player will be blocked to pass through the wall
        if keys[self.__system.preferences.buttonDown]: # If down button is being pressed
            self.rect.y += 4 # Velocity of 4 pixels
            wall = self.check_collision() # Check if collided with something
            if wall is not None: # Only if collided
                self.rect.bottom = wall.top # The player will be blocked to pass through the wall
        if keys[self.__system.preferences.buttonRight]: # If right button is being pressed
            self.rect.x += 4 # Velocity of 4 pixels
            wall = self.check_collision()  # Check if collided with something
            if wall is not None: # Only if collided
                self.rect.right = wall.left # The player will be blocked to pass through the wall
        if keys[self.__system.preferences.buttonLeft]: # If left button is being pressed
            self.rect.x -= 4 # Velocity of 4 pixels
            wall = self.check_collision()  # Check if collided with something
            if wall is not None: # Only if collided
                self.rect.left = wall.right # The player will be blocked to pass through the wall

    def check_collision(self) -> pygame.Rect:
        for wall in self.__system.gameplay.walls: # Access each wall in the list of the map walls
            if self.rect.colliderect(wall): # Check if collided with some wall in the list
                return wall # Return the wall collided
        if self.__system.gameplay.statue is not None: # Check if statue wasn't taken yet
            if self.rect.colliderect(self.__system.gameplay.statue.rect): # Check if player collided with statue
                self.__inventory.append("Statue") # Add statue to the inventory if collision happened
                self.__system.gameplay.statue = None # Reset the statue sprite
                return
        if self.rect.colliderect(self.__system.gameplay.door) and "Statue" in self.__inventory: # Check if the player touched the main door
                                                                                                  # with the statue in its inventory 
            currentTime = datetime.datetime.now() # Get the time that mission finished
            timeUsed = str(currentTime - self.__system.gameplay.startTime) # Find the time used in the mission by substracting the final time
                                                                           # from the start time
            self.__system.preferences.lastTime = timeUsed[:-4] # Transform the result in the string h:mm:ss.msms limiting the time decimal
                                                               # to 2
            self.__system.preferences.check_best_score(map=self.__system.gameplay.map) # Check if it was the best time
            self.__system.render_screen(nextScreen="mission-completed") # Render the mission completed screen
            return
        if self.__system.gameplay.laser is not None: # Check if the laser is active
            if self.rect.colliderect(self.__system.gameplay.laser.rect): # Check the collision with the laser
                self.__lives -= 1 # Player lose 1 live if collied with the laser
                # The player will return to the initial position according to the map.
                if self.__system.gameplay.map == "baker":
                    self.rect.topleft = config.bakerInitialPosition       
                else:
                    self.rect.topleft = config.usbourneInitialPosition
                return
        if self.rect.colliderect(self.__system.gameplay.guard.rect): # Check the collision with the guard
            self.__lives -= 1 # Player lose 1 live if collied with the guard
            # The player will return to the initial position according to the map.
            if self.__system.gameplay.map == "baker":
                self.rect.topleft = config.bakerInitialPosition
            else:
                self.rect.topleft = config.usbourneInitialPosition
            return
            
    def interact(self) -> None:
        searchablePlaces = self.__system.gameplay.searchablePlaces # The places where there are items
        for searchable in searchablePlaces: 
            if self.rect.colliderect(searchablePlaces[searchable]): # Check collision with the searchable place
                match searchable: # The item to be added in the inventory depends on the place
                    # The lockpick is inside the fridge
                    case "fridge":
                        if "Lockpick" not in self.__inventory:
                            self.__inventory.append("Lockpick") 
                            return
                    # The UV light is inside the tv support
                    case "tv":
                        if "UV light" not in self.__inventory:
                            self.__inventory.append("UV light")
                            return
                    # The chip is inside the desk
                    case "desk":
                        if "Chip" not in self.__inventory:
                            self.__inventory.append("Chip")
    
    def use(self) -> None:
        if self.__system.gameplay.codeDoor is not None:
            if self.rect.colliderect(self.__system.gameplay.codeDoor.rect) and "UV light" in self.__inventory:
                self.__system.render_screen(nextScreen="fingerprint")
        if self.__system.gameplay.lockDoor is not None:
            if self.rect.colliderect(self.__system.gameplay.lockDoor.rect) and "Lockpick" in self.__inventory:
                self.__system.render_screen(nextScreen="lockpick")
        if self.__system.gameplay.server is not None:
            if self.rect.colliderect(self.__system.gameplay.server) and "Chip" in self.__inventory:
                self.__system.render_screen(nextScreen="hacking")

    def display_inventory(self) -> None:
        if self.__system.screenName in ["baker", "usbourne"]: # Only prints on gameplay screens
            font = pygame.font.Font(None, 25) 
            for index in range(len(self.__inventory)): # Range of all indexes of the inventory
                text = font.render(self.__inventory[index], True, (235, 165, 59))
                rect = text.get_rect(topleft=(633, 644 + 35 * index)) # The index is used to create a spacing between printed items
                self.__system.screenObj.blit(text, rect)

class Gameplay:
    def __init__(self, map: str, startTime: datetime.timedelta, walls: list, searchablePlaces: list, player: Player,
                  guard: Guard, laser: Sprite, system: System, statueCoordinate: tuple, door: pygame.Rect,
                  codeDoor: Sprite, lockDoor: Sprite, server: pygame.rect.Rect):
        self.__map = map
        self.__startTime = startTime
        self.__walls = walls.copy()
        self.__searchablePlaces = searchablePlaces
        self.__player = player
        self.__guard = guard
        self.__laser = laser
        self.__door = door
        self.__server = server
        self.__statue = Sprite(image=config.statueSpritePath, coordinate=statueCoordinate)
        self.__system = system
        self.__codeDoor = codeDoor
        self.__lockDoor = lockDoor
    
    # Getter method for self.__guard
    @property
    def guard(self):
        return self.__guard

    # Getter method for self.__server
    @property
    def server(self):
        return self.__server

    # Getter method for self.__walls
    @property
    def walls(self):
        return self.__walls
    
    # Getter method for self.__player
    @property
    def player(self):
        return self.__player
    
    # Getter method for self.__map
    @property
    def map(self):
        return self.__map
    
    # Getter method for self.__searchablePlaces
    @property
    def searchablePlaces(self):
        return self.__searchablePlaces
    
    # Getter method for self.__codeDoor
    @property
    def codeDoor(self):
        return self.__codeDoor
    
    # Getter method for self.__lockDoor
    @property
    def lockDoor(self):
        return self.__lockDoor

    # Getter method for self.__door
    @property
    def door(self):
        return self.__door
    
    # Getter method for self.__startTime
    @property
    def startTime(self):
        return self.__startTime

    # Getter method for self.__statue
    @property
    def statue(self):
        return self.__statue
    
    # Getter method for self.__laser
    @property
    def laser(self):
        return self.__laser

    # Setter method for self.__laser
    @laser.setter
    def laser(self, value):
        self.__laser = value

    # Setter method for self.__statue
    @statue.setter
    def statue(self, value):
        self.__statue = value

    # Setter method for self.__codeDoor
    @codeDoor.setter
    def codeDoor(self, value):
        self.__codeDoor = value

    # Setter method for self.__lockDoor
    @lockDoor.setter
    def lockDoor(self, value):
        self.__lockDoor = value

    def update_status(self) -> None:
        currentTime = datetime.datetime.now() # Get the current time
        timeUsed = str(currentTime - self.__startTime) # Find the time used so far by subtracting the current time from the start one
        timeUsed = timeUsed[:-4] # Limit the seconds to 2 decimal places
        font = pygame.font.Font(None, 40) 
        # Print the time 
        text = font.render(timeUsed, True, (235, 165, 59))
        rect = text.get_rect(topleft=(440, 5))
        self.__system.screenObj.blit(text, rect)
        # Print the lives
        text = font.render(str(self.__player.lives), True, (235, 165, 59))
        rect = text.get_rect(topleft=(275, 5))
        self.__system.screenObj.blit(text, rect)

class Button:
    def __init__(self, buttons: list, system: System):
        self.__buttons = buttons
        self.__selectedButtonIndex = 0
        self.__system = system
        self.__backgrounds = {
            "start": config.startButtonPath,
            "rank": config.rankButtonPath,
            "options": config.optionsButtonPath,
            "quit": config.quitButtonPath,
            "again": config.againButtonPath,
            "menu-pause": config.menuPauseButtonPath,
            "menu-menu": config.menuMenuButtonPath,
            "continue": config.continueButtonPath,
            "baker": config.bakerButtonPath,
            "usbourne": config.map2ButtonPath,
            "arrow": config.arrowPath
        }

    # buttons getter method
    @property
    def buttons(self):
        return self.__buttons
    
    # selectedButtonIndex getter method
    @property
    def selectedButtonIndex(self):
        return self.__selectedButtonIndex

    # backgrounds getter method
    @property
    def backgrounds(self):
        return self.__backgrounds
    
    def selection_general(self, key: int) -> None:
        # Selection based on constant value of the key pressed
        match key:
            # Access the system object to access the preferences and after get the constant of up button
            case self.__system.preferences.buttonUp:
                self.__selectedButtonIndex = (self.__selectedButtonIndex - 1) % len(self.__buttons) # Decrease the index 
                                                                                                    # without exceed the index
                # Access the system object to access the preferences and after get the constant of down button
            case self.__system.preferences.buttonDown:
                self.__selectedButtonIndex = (self.__selectedButtonIndex + 1) % len(self.__buttons) # Increase the index 
                                                                                                    # without exceed the index

    def selection_menu(self, key: int) -> None:
        # Uses the general selection for W and S buttons
        self.selection_general(key=key)
        # The RETURN key is responsible to confirm the selection
        if key == pygame.K_RETURN:
            # Selection based on the button selected
            match self.__buttons[self.__selectedButtonIndex][0]:
                case "start":
                    self.__system.render_screen(nextScreen="start") # Render start screen
                case "rank":
                    self.__system.render_screen(nextScreen="rank") # Render rank screen
                case "options":
                    self.__system.render_screen(nextScreen="options") # Render rank screen
                case "quit":
                    pygame.quit() # Stop the game

    def selection_start(self, key: int) -> None:
        # Uses the general selection for W and S buttons
        self.selection_general(key=key)
        match key:
            case pygame.K_RETURN:
                match self.__buttons[self.__selectedButtonIndex][0]:
                    case "baker":
                        self.__system.render_screen(nextScreen="baker")
                    case "usbourne":
                        self.__system.render_screen(nextScreen="usbourne")
            case pygame.K_ESCAPE:
                self.__system.render_screen(nextScreen="menu")

    def selection_pause(self, key: int) -> None:
        self.selection_general(key=key)
        if key == pygame.K_RETURN:
            match self.__buttons[self.__selectedButtonIndex][0]:
                case "continue":
                    self.__system.render_screen(nextScreen=self.__system.gameplay.map)
                case "menu-pause":
                    self.__system.render_screen(nextScreen="menu")

    def selection_options(self, event: pygame.event.Event) -> None:
        # Selection case the SHIFT is held
        if event.mod & pygame.KMOD_SHIFT:
            # Selection with the y coodinate, buttons has the format [[button name, [x, y]]] in this case
            match self.__buttons[0][1][1]:
                case 345: # y-position of up button preference
                    self.__system.preferences.buttonUp = event.key # Change the up button preference
                case 415: # y-position of down button preference
                    self.__system.preferences.buttonDown = event.key # Change the down button preference
                case 485: # y-position of right button preference
                    self.__system.preferences.buttonRight = event.key # Change the right button preference
                case 555: # y-position of left button preference
                    self.__system.preferences.buttonLeft = event.key # Change the left button preference
                case 625: # y-position of use button preference
                    self.__system.preferences.buttonUse = event.key # Change the use button preference
                case 695: # y-position of interaction button preference
                    self.__system.preferences.buttonInteract = event.key # Change the interact button preference
        else: 
            match event.key: # Use the integer constant of the key to select
                case self.__system.preferences.buttonUp: # up selection
                    new = self.__buttons[0][1][1] - 70 # find the new y position for the arrow
                    if new >= 275: # check if it isn't below the y position of the first preference
                        self.__buttons[0][1][1] = new # set the new preference
                case self.__system.preferences.buttonDown: # down selection
                    new = self.__buttons[0][1][1] + 70 # find the new y position for the arrow
                    if new <= 695: # check if it isn't above the y position of the last preference
                        self.__buttons[0][1][1] = new # set the new preference
                case self.__system.preferences.buttonLeft: # left selection
                    if self.__buttons[0][1][1] == 275: # It will restrict it to volume preference
                        self.__system.preferences.volume -= 0.05 # decrease the volume by 0.05, min of 0
                case self.__system.preferences.buttonRight: # right selection
                    if self.__buttons[0][1][1] == 275: # restrict it to volume preference
                        self.__system.preferences.volume += 0.05 # increase the volume by 0.05, max of 1
                case pygame.K_ESCAPE: # ESC selection
                    self.__system.preferences.save() # Method to save the current preferences in the local database
                    pygame.mixer.music.set_volume(self.__system.preferences.volume) # Use the new volume
                    self.__system.render_screen(nextScreen="menu") # Return to menu

def textbox_handling(system: System, key: int) -> None:
    # Use the key int constant to chosse the correct action
    match key:
        # RETURN key confirm the username
        case pygame.K_RETURN:
            if system.texbox != "":
                request = requests.post("http://127.0.0.1:5000/register", json={"username": system.texbox})
                status = request.json()["success"]
                if status:
                    system.preferences.username = system.textbox # store username into preferences attributes
                    system.preferences.save() # Save current preferences attributes into local database
                    # Render the menu screen
                    system.render_screen(nextScreen="menu")
                else:
                    system.textbox = "Unavailable"
        # BACKSCPACE delete one character
        case pygame.K_BACKSPACE:
            system.textbox = system.textbox[:-1] # Create a new string cutting off the last charactex of textbox
        # Any other character
        case _:
            if pygame.key.name(key).isalnum() and len(system.textbox) < 10: # Limit the username to 16 alphanumeric characters
                system.textbox =  system.textbox + pygame.key.name(key) # append the new character to the texbox
