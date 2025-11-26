import os
import pygame



# Path of this file
basePath = os.path.dirname(__file__)

# Path for local database
localDatabasePath = os.path.join(basePath, "LocalUserInfo.json")
localDatabasePath = os.path.abspath(localDatabasePath)

# Screens backgrounds paths
menuScreenPath = os.path.join(basePath, "..", "Media", "menu-screen.png")
menuScreenPath = os.path.abspath(menuScreenPath)
usernameScreenPath = os.path.join(basePath, "..", "Media", "username-screen.png")
usernameScreenPath = os.path.abspath(usernameScreenPath)
rankScreenPath = os.path.join(basePath, "..", "Media", "rank-screen.png")
rankScreenPath = os.path.abspath(rankScreenPath)
optionsScreenPath = os.path.join(basePath, "..", "Media", "options-screen.png")
optionsScreenPath = os.path.abspath(optionsScreenPath)
bakerScreenPath = os.path.join(basePath, "..", "Media", "baker-avenue-screen.png")
bakerScreenPath = os.path.abspath(bakerScreenPath)
usbourneScreenPath = os.path.join(basePath, "..", "Media", "usbourne-way-screen.png")
usbourneScreenPath = os.path.abspath(usbourneScreenPath)
pauseScreenPath = os.path.join(basePath, "..", "Media", "pause-screen.png")
pauseScreenPath = os.path.abspath(pauseScreenPath)
missionCompletedScreenPath = os.path.join(basePath, "..", "Media", "mission-completed-screen.png")
missionCompletedScreenPath = os.path.abspath(missionCompletedScreenPath)
fingerprintScreenPath = os.path.join(basePath, "..", "Media", "fingerprint-screen.png")
fingerprintScreenPath = os.path.abspath(fingerprintScreenPath)
lockpickScreenPath = os.path.join(basePath, "..", "Media", "lockpick-screen.png")
lockpickScreenPath = os.path.abspath(lockpickScreenPath)
gameOverScreenPath = os.path.join(basePath, "..", "Media", "game-over-screen.png")
gameOverScreenPath = os.path.abspath(gameOverScreenPath)
hackingScreenPath = os.path.join(basePath, "..", "Media", "hacking-screen.png")
hackingScreenPath = os.path.abspath(hackingScreenPath)

# Button backgrounds paths
startButtonPath = os.path.join(basePath, "..", "Media", "start-button.png")
startButtonPath = os.path.abspath(startButtonPath)
rankButtonPath = os.path.join(basePath, "..", "Media", "rank-button.png")
rankButtonPath = os.path.abspath(rankButtonPath)
optionsButtonPath = os.path.join(basePath, "..", "Media", "options-button.png")
optionsButtonPath = os.path.abspath(optionsButtonPath)
quitButtonPath = os.path.join(basePath, "..", "Media", "quit-button.png")
quitButtonPath = os.path.abspath(quitButtonPath)
againButtonPath = os.path.join(basePath, "..", "Media", "again-button.png")
againButtonPath = os.path.abspath(againButtonPath)
menuPauseButtonPath = os.path.join(basePath, "..", "Media", "menu-pause-button.png")
menuPauseButtonPath = os.path.abspath(menuPauseButtonPath)
menuMenuButtonPath = os.path.join(basePath, "..", "Media", "menu-menu-button.png")
menuMenuButtonPath = os.path.abspath(menuMenuButtonPath)
continueButtonPath = os.path.join(basePath, "..", "Media", "continue-button.png")
continueButtonPath = os.path.abspath(continueButtonPath)
bakerButtonPath = os.path.join(basePath, "..", "Media", "baker-button.png")
bakerButtonPath = os.path.abspath(bakerButtonPath)
map2ButtonPath = os.path.join(basePath, "..", "Media", "map-2-button.png")
map2ButtonPath = os.path.abspath(map2ButtonPath)
arrowPath = os.path.join(basePath, "..", "Media", "arrow.png")
arrowPath = os.path.abspath(arrowPath)

# Elements for Baker Avenue map
bakerLaserPath = os.path.join(basePath, "..", "Media", "laser-baker-sprite.png")
bakerLaserPath = os.path.abspath(bakerLaserPath)
bakerInitialPosition = (100, 710)
bakerCodeDoor = pygame.Rect(73, 256, 75, 17)
bakerLockDoor = pygame.Rect(657, 303, 75, 17)
bakerDoor = pygame.Rect(70, 775, 80, 25)
bakerServer = pygame.Rect(0, 0, 216, 94)
bakerSearchable = {"desk": pygame.Rect(562, 5, 69, 77), 
                   "sink": pygame.Rect(238, 206, 60, 102), 
                   "tv": pygame.Rect(5, 437, 66, 192), 
                   "fridge": pygame.Rect(431, 695, 89, 85)}
bakerWalls = [pygame.Rect(778, 0, 22, 800), pygame.Rect(0, 0, 22, 800), pygame.Rect(0, 0, 800, 22), pygame.Rect(0, 778, 800, 22),
              pygame.Rect(211, 0, 22, 325), pygame.Rect(211, 308, 446, 22), pygame.Rect(733, 306, 68, 22), pygame.Rect(0, 257, 75, 22),
              pygame.Rect(147, 257, 80, 22), pygame.Rect(364, 0, 22, 213), pygame.Rect(364, 279, 22, 47), pygame.Rect(170, 427, 83, 222),
              pygame.Rect(390, 413, 207, 185), pygame.Rect(520, 700, 281, 100), pygame.Rect(698, 533, 101, 268), pygame.Rect(632, 0, 168, 211),
              pygame.Rect(233, 135, 59, 51), pygame.Rect(562, 0, 69, 77), pygame.Rect(233, 206, 60, 102), pygame.Rect(0, 437, 66, 192), 
              pygame.Rect(431, 700, 89, 85), bakerServer, bakerCodeDoor, bakerLockDoor]

# Elements for Usbourne Way map
usbourneLaserPath = os.path.join(basePath, "..", "Media", "laser-usbourne-sprite.png")
usbourneLaserPath = os.path.abspath(usbourneLaserPath)
usbourneInitialPosition = (710, 365)
usbourneCodeDoor = pygame.Rect(322, 223, 17, 75)
usbourneLockDoor = pygame.Rect(322, 670, 17, 75)
usbourneDoor = pygame.Rect(770, 365, 30, 85)
usbourneServer = pygame.Rect(5, 708, 214, 78)
usbourneSearchable = {"desk": pygame.Rect(5, 241, 85, 94),
                      "fridge": pygame.Rect(469, 193, 92, 86), 
                      "tv": pygame.Rect(469, 727, 192, 52), 
                      "sink": pygame.Rect(213, 418, 102, 60)}
usbourneWalls =[pygame.Rect(778, 0, 22, 800), pygame.Rect(0, 0, 22, 800), pygame.Rect(0, 0, 800, 22), pygame.Rect(0, 778, 800, 22), 
                pygame.Rect(0, 333, 331, 22), pygame.Rect(0, 478, 331, 22), pygame.Rect(322, 166, 477, 22), pygame.Rect(322, 0, 22, 58),
                pygame.Rect(322, 132, 22, 90), pygame.Rect(322, 298, 22, 55), pygame.Rect(322, 426, 22, 244), pygame.Rect(322, 746, 22, 54),
                pygame.Rect(0, 0, 102, 243), pygame.Rect(560, 189, 223, 82), pygame.Rect(143, 423, 51, 59), pygame.Rect(104, 499, 223, 83),
                pygame.Rect(454, 497, 221, 88), pygame.Rect(0, 241, 85, 94), pygame.Rect(469, 188, 92, 86), pygame.Rect(469, 732, 192, 52),
                pygame.Rect(213, 423, 102, 60), usbourneServer, usbourneCodeDoor, usbourneLockDoor]

# Inventory rectangle
inventoryArea = pygame.Rect(608, 588, 192, 208)

# Sprites images
mainSpritePath = os.path.join(basePath, "..", "Media", "main-character.png")
mainSpritePath = os.path.abspath(mainSpritePath)
statueSpritePath = os.path.join(basePath, "..", "Media", "golden-statue.png")
statueSpritePath = os.path.abspath(statueSpritePath)
codeDoorPath = os.path.join(basePath, "..", "Media", "code-door.png")
codeDoorPath = os.path.abspath(codeDoorPath)
lockDoorPath = os.path.join(basePath, "..", "Media", "lock-door.png")
lockDoorPath = os.path.abspath(lockDoorPath)
guardSpritePath = os.path.join(basePath, "..", "Media", "guard-sprite.png")
guardSpritePath = os.path.abspath(guardSpritePath)

# Lockpick elements
lockpickSequence = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
leftArrow = os.path.join(basePath, "..", "Media", "left-arrow.png")
rightArrow = os.path.join(basePath, "..", "Media", "right-arrow.png")
upArrow = os.path.join(basePath, "..", "Media", "up-arrow.png")
downArrow = os.path.join(basePath, "..", "Media", "down-arrow.png")
lockpickBackgrounds = {pygame.K_LEFT: os.path.abspath(leftArrow), pygame.K_RIGHT: os.path.abspath(rightArrow), 
                       pygame.K_UP: os.path.abspath(upArrow), pygame.K_DOWN: os.path.abspath(downArrow)}

# Fingerprint elements
weakFingerprintPath = os.path.join(basePath, "..", "Media", "weak-finger.png")
weakFingerprintPath = os.path.abspath(weakFingerprintPath)
midFingerprintPath = os.path.join(basePath, "..", "Media", "mid-finger.png")
midFingerprintPath = os.path.abspath(midFingerprintPath)
strongFingerprintPath = os.path.join(basePath, "..", "Media", "strong-finger.png")
strongFingerprintPath = os.path.abspath(strongFingerprintPath)
numbersPositions = ((348, 614), (227, 282), (336, 282), (447, 282), (227, 392),
                     (336, 392), (447, 392), (227, 503), (336, 503), (447, 503))

# Hacking elements
hackingSequences = [["R___er", ['o', 'b', 'b']], 
                    ["Cr_m_n_l", ['i', 'i', 'a']], 
                    ["P_l_c_", ["o", "i", "e"]]]